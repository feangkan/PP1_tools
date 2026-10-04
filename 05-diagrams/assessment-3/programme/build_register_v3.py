"""Write Document Register v3 (original format, matched to the timeline) from register_v3.py.

Outputs (in ../):
  document-register-v3.csv    8 columns, paste back into the group's Register
  document-register-v3.xlsx   the same, with the PDF's colour key; assumed dates in italics
  20-document-register-v3.md  the table + what changed from v2 and why, with sources

Also checks every register date against the timeline (build_scenario1_timeline.py) and prints any
mismatch.

Run:  py build_register_v3.py
"""
import csv
import datetime as dt
import os

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

from build_board_layout import load_events
from event_notes import SOURCES
from register_v3 import HEADS, KIND_FILL, KIND_LABEL, REGISTER

HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.normpath(os.path.join(HERE, ".."))
ARIAL = "Arial"


def parse(d):
    parts = [int(x) for x in d.split(".")]
    return dt.date(parts[-1], parts[-2], parts[0] if len(parts) == 3 else 1)


# ---------------------------------------------------------------- consistency check vs the timeline
CHECK = {  # register title start -> timeline event name start
    "Competition Design Phase": "Competition design phase", "Competition winner": "Utzon wins first prize",
    "Introductory letter": "★ Introductory letter", "Client Architect Agreement": "★ CAA signed",
    "Tender documents": "Stage I tender documents", "Tender Return": "Tender return",
    "Contractor selection": "Contractor selection", "Simple Works Contract": "★ Simple Works Contract signed",
    "Stage I Commences": "Site possession", "Client representative change (Cahill": "Premier Cahill dies",
    "Engineer's advice": "★ Problem found", "Change to architectural services": "★ Architect notifies client",
    "Instruction- for a Variation": "★ Instruction for a Variation", "Contractor's details": "Contractor's details",
    "Instruction to proceed": "Instruction to proceed", "Instruction- Adjustment": "★ Adjustment of time",
    "Cost Plan": "Cost plan issued", "Contract Price Adjustment": "★ Contract Price Adjustment",
    "Stage II Contract signed": "Stage II agreement", "Stage 2 Contract drawings": "Stage II contract drawings",
    "Stage II Commences": "Stage II — roof shells", "Client representative change (Askin": "Askin government",
    "Architect resigns": "Utzon resigns", "Replacement architects": "Hall / Todd / Littlemore appointed",
    "Stage III Contract signed": "Stage III agreement", "Stage III Commences": "Stage III — interiors",
    "Stage 3 Contract drawings": "Stage III working drawings", "Client representative change (Hughes": "Hughes resigns",
    "Practical Completion": "Practical completion", "Final Certificate": "★ Final Certificate",
}


def check():
    rec, _, _ = load_events()
    problems = 0
    for row in REGISTER:
        key = next((k for k in CHECK if row[1].startswith(k)), None)
        if not key:
            continue
        ev = next((it for it in rec.items if it["name"].startswith(CHECK[key])), None)
        if ev is None:
            print("  no timeline event for:", row[1])
            problems += 1
            continue
        reg, tl = parse(row[0]), ev["start"]
        same = (reg == tl) if row[0].count(".") == 2 else (reg.year, reg.month) == (tl.year, tl.month)
        if not same:
            print(f"  MISMATCH {row[1]}: register {row[0]} vs timeline {tl}")
            problems += 1
    print("timeline check:", "all dates match" if not problems else f"{problems} problem(s)")


# ---------------------------------------------------------------- CSV
def write_csv(path):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(HEADS)
        for row in REGISTER:
            w.writerow(row[:8])
    print("wrote", os.path.basename(path))


# ---------------------------------------------------------------- Excel (original format)
def fill(hex_):
    return PatternFill(start_color=hex_, end_color=hex_, fill_type="solid")


def write_register_sheet(ws, rows, blank_rows=10, title=True):
    """The Register in the group's original 8-column format with the PDF's colour key."""
    thin = Side(style="thin", color="A6A6A6")
    box = Border(left=thin, right=thin, top=thin, bottom=thin)
    ws.sheet_view.showGridLines = False
    widths = [12, 52, 11, 12, 12, 20, 33, 33]
    r0 = 1
    if title:
        ws.cell(row=1, column=1, value="Architects Document Register").font = Font(name=ARIAL, size=14, bold=True, underline="single")
        for i, (kind, label) in enumerate(KIND_LABEL.items()):
            ws.cell(row=2 + i, column=1).fill = fill(KIND_FILL[kind])
            ws.cell(row=2 + i, column=1).border = box
            ws.cell(row=2 + i, column=2, value=label).font = Font(name=ARIAL, size=8)
        ws.cell(row=6, column=2, value="Italic date = month assumed [A]. '(suggested)' = contributor or checker not "
                                       "yet confirmed by that person.").font = Font(name=ARIAL, size=8, italic=True,
                                                                                    color="6B7280")
        r0 = 8
    for i, (h, w) in enumerate(zip(HEADS, widths), start=1):
        c = ws.cell(row=r0, column=i, value=h)
        c.font = Font(name=ARIAL, size=10, bold=True)
        c.fill = fill("F2F2F2")
        c.border = box
        c.alignment = Alignment(vertical="center")
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    r = r0 + 1
    for row in rows:
        date, title_, form, frm, to, action, contrib, checker, kind, assumed = row[:10]
        for c, v in enumerate([date, title_, form, frm, to, action, contrib, checker], start=1):
            cell = ws.cell(row=r, column=c, value=v or None)
            cell.font = Font(name=ARIAL, size=9, bold=(c == 3), italic=(c == 1 and assumed),
                             color="7F7F7F" if "(suggested)" in str(v) else "000000")
            cell.border = box
            cell.alignment = Alignment(vertical="center", wrap_text=c == 2)
            if KIND_FILL[kind]:
                cell.fill = fill(KIND_FILL[kind])
        ws.row_dimensions[r].height = 15 if len(title_) <= 55 else 28
        r += 1
    for _ in range(blank_rows):
        for c in range(1, 9):
            ws.cell(row=r, column=c).border = box
        r += 1
    ws.cell(row=r + 1, column=1, value="*All Architect to Contractor Issuances under SW form series are issued on behalf of the client.").font = Font(name=ARIAL, size=8)
    ws.freeze_panes = ws.cell(row=r0 + 1, column=1)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    return r


def write_xlsx(path):
    wb = openpyxl.Workbook()
    write_register_sheet(wb.active, REGISTER)
    wb.active.title = "Register"
    wb.save(path)
    print("wrote", os.path.basename(path))


# ---------------------------------------------------------------- markdown
def write_md(path):
    def link(keys):
        out = []
        for k in [x.strip() for x in keys.replace("/", ",").split(",") if x.strip()]:
            t = SOURCES.get(k)
            out.append(f"[{k}]({t[2]})" if t and t[2] else k)
        return ", ".join(out)

    lines = [
        "# 20 — Architects Document Register v3 (matched to the timeline)",
        "",
        "- **Date:** 2026-10-04. Replaces `14-document-register-v2.md` as the working Register. **Generated** by "
        "`programme/build_register_v3.py` from `programme/register_v3.py` — edit that file, then re-run.",
        "- **Original format kept:** the same 8 columns as the group's `DOCUMENT REGISTER_PP1.pdf` (Date · Title of "
        "Form · Form No. · From · To · Action · Contributor · Checker), the same dd.mm.yyyy dates and the PDF's colour "
        "key. Paste-back files: `document-register-v3.csv`, `document-register-v3.xlsx` (with colours).",
        "- **Every date matches the timeline** (`programme/soh_board_layout.xlsx`); the build script checks this. "
        "*Italic* dates = month assumed [A]. `(suggested)` = contributor or checker not yet confirmed by that person.",
        "- Colour key: " + " · ".join(KIND_LABEL.values()) + ".",
        "",
        "## Register",
        "",
        "| " + " | ".join(HEADS) + " |",
        "|" + "---|" * len(HEADS),
    ]
    for row in REGISTER:
        date = f"*{row[0]}*" if row[9] else row[0]
        lines.append("| " + " | ".join([date] + [v or "" for v in row[1:8]]) + " |")
    lines += ["", "*All Architect to Contractor Issuances under SW form series are issued on behalf of the client.", "", "## What changed from v2, and why", "", "| Date | Row | Change | Source |", "|---|---|---|---|"]
    for row in REGISTER:
        if row[10]:
            lines.append(f"| {row[0]} | {row[1]} | {row[10]} | {link(row[11])} |")
    lines += [
        "",
        "## Still to confirm as a group",
        "",
        "- The `(suggested)` contributors and checkers (they follow the Register's own pattern: client rows to "
        "Lead 1, procurement rows to Lead 2, contract-administration rows to Lead 3).",
        "- The assumed months (*italic* dates) inside the years the Register first gave.",
        "- Whether to keep the optional SW-42 and SW-13 rows.",
        "- Who signs SW-31 in 1975: Hall, Todd & Littlemore for the architect; whether Leon Punch is still Minister "
        "for Public Works [verify].",
        "- The CAA document itself must be built on the 2024 template, not just this row.",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", os.path.basename(path))


if __name__ == "__main__":
    check()
    write_csv(os.path.join(UP, "document-register-v3.csv"))
    write_xlsx(os.path.join(UP, "document-register-v3.xlsx"))
    write_md(os.path.join(UP, "20-document-register-v3.md"))
