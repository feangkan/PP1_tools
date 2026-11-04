"""Write the Document Register v3 in the TUTOR'S format, matched to the timeline, from register_v3.py.

Format = the course's "Document Register Sample 2026-1.docx": Date · Document · Form No. · From/To ·
Details (cost etc) · Student Contribution; grey = milestone, green = forms that are part of our assessment.

Outputs (in ../):
  document-register-v3.docx   built on the tutor's own .docx (same header, title, table style)
  document-register-v3.csv    the same 6 columns, for pasting into Google Sheets / Excel
  document-register-v3.xlsx   the same, with the grey / green highlighting
  20-document-register-v3.md  the table + what changed from v2 and why, with sources

Also checks every register date against the timeline (build_scenario1_timeline.py).

Run:  py build_register_v3.py   (needs the tutor's sample .docx at SAMPLE below)
"""
import csv
import datetime as dt
import html
import os
import re
import zipfile

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

from build_board_layout import load_events
from event_notes import SOURCES
from register_v3 import REGISTER, TUTOR_FILL, TUTOR_HEADS, tutor_rows

HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.normpath(os.path.join(HERE, ".."))
SAMPLE = (r"D:\RMIT_SEM2 26_PROPRAC 1\Assessment 3 resources"
          r"\(2.Prepare a Document Register) Document Register Sample 2026-1.docx")
ARIAL = "Arial"
GROUP = "Group: Kankawee Maksomboon · Yu-Chun Ho · Prani Patton   |   Scenario 1: additional piers to support the roof"
KEY = ("Highlighted green = forms that are part of our assessment. Grey = project milestones (no document). "
       "Grey names = contribution suggested, still to confirm.")
FOOT = "*All Architect to Contractor issuances under the SW form series are issued on behalf of the client."


def parse(d):
    parts = [int(x) for x in d.split(".")]
    return dt.date(parts[-1], parts[-2], parts[0] if len(parts) == 3 else 1)


# ---------------------------------------------------------------- consistency check vs the timeline
CHECK = {  # register title start -> timeline event name start
    "Competition Design Phase": "Competition design phase", "Competition winner": "Utzon wins first prize",
    "Introductory letter": "★ Introductory letter", "Client Architect Agreement": "★ CAA 2024 signed",
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
        w.writerow(TUTOR_HEADS)
        for vals, *_ in tutor_rows():
            w.writerow(vals)
    print("wrote", os.path.basename(path))


# ---------------------------------------------------------------- Excel (tutor's format)
def fill(hex_):
    return PatternFill(start_color=hex_, end_color=hex_, fill_type="solid")


def write_register_sheet(ws, rows, blank_rows=10, title=True):
    """The Register in the tutor's 6-column format: grey milestones, green assessment forms."""
    thin = Side(style="thin", color="7F7F7F")
    box = Border(left=thin, right=thin, top=thin, bottom=thin)
    ws.sheet_view.showGridLines = False
    widths = [12, 44, 11, 24, 46, 24]
    r0 = 1
    if title:
        ws.cell(row=1, column=1, value="Architects Register").font = Font(name=ARIAL, size=14, bold=True,
                                                                          underline="single")
        ws.cell(row=2, column=1, value=GROUP).font = Font(name=ARIAL, size=9, italic=True)
        ws.cell(row=3, column=1, value=KEY).font = Font(name=ARIAL, size=9, italic=True)
        r0 = 5
    for i, (h, w) in enumerate(zip(TUTOR_HEADS, widths), start=1):
        c = ws.cell(row=r0, column=i, value=h)
        c.font = Font(name=ARIAL, size=10, bold=True, underline="single")
        c.border = box
        c.alignment = Alignment(vertical="top", wrap_text=True)
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    r = r0 + 1
    for vals, kind, suggested, assumed in rows:
        for c, v in enumerate(vals, start=1):
            cell = ws.cell(row=r, column=c, value=v or None)
            cell.font = Font(name=ARIAL, size=9, color="808080" if (c == 6 and suggested) else "000000")
            cell.border = box
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if TUTOR_FILL[kind]:
                cell.fill = fill(TUTOR_FILL[kind])
        longest = max(len(vals[1]) / 44, len(vals[4]) / 46, len(vals[3]) / 24, 1)
        ws.row_dimensions[r].height = 13 * (int(longest) + (1 if longest % 1 else 0)) + 3
        r += 1
    for _ in range(blank_rows):
        for c in range(1, 7):
            ws.cell(row=r, column=c).border = box
        r += 1
    if title:
        ws.cell(row=r + 1, column=1, value=FOOT).font = Font(name=ARIAL, size=8)
    ws.freeze_panes = ws.cell(row=r0 + 1, column=1)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    return r


def write_xlsx(path):
    wb = openpyxl.Workbook()
    write_register_sheet(wb.active, tutor_rows())
    wb.active.title = "Register"
    wb.save(path)
    print("wrote", os.path.basename(path))


# ---------------------------------------------------------------- Word, on the tutor's own template
WIDTHS = [1304, 2143, 997, 1579, 1250, 1743]          # the sample's cell widths (dxa)
SHD = {"milestone": '<w:shd w:val="clear" w:color="auto" w:fill="D9D9D9" w:themeFill="background1" '
                    'w:themeFillShade="D9"/>',
       "form": '<w:shd w:val="clear" w:color="auto" w:fill="C5E0B3" w:themeFill="accent6" w:themeFillTint="66"/>',
       "": ""}


def _run(text, grey=False, italic=False, size=None):
    rpr = ""
    if grey or italic or size:
        rpr = "<w:rPr>" + ("<w:i/><w:iCs/>" if italic else "") + ('<w:color w:val="808080"/>' if grey else "") + \
              (f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>' if size else "") + "</w:rPr>"
    return f'<w:r>{rpr}<w:t xml:space="preserve">{html.escape(text, quote=False)}</w:t></w:r>'


def _cell(text, width, kind, grey=False):
    shd = SHD[kind]
    tcpr = f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shd}</w:tcPr>'
    para = f"<w:p>{_run(text, grey)}</w:p>" if text else "<w:p/>"
    return f"<w:tc>{tcpr}{para}</w:tc>"


def _row(vals, kind, suggested):
    cells = "".join(_cell(v, w, kind, grey=(i == 5 and suggested)) for i, (v, w) in enumerate(zip(vals, WIDTHS)))
    return f"<w:tr><w:trPr><w:cantSplit/></w:trPr>{cells}</w:tr>"


def _para(text, italic=False, size=None):
    ppr = "<w:pPr><w:rPr>" + ("<w:i/><w:iCs/>" if italic else "") + "</w:rPr></w:pPr>" if italic else ""
    return f"<w:p>{ppr}{_run(text, italic=italic, size=size)}</w:p>"


def write_docx(path):
    if not os.path.exists(SAMPLE):
        print("SKIPPED docx: tutor's sample not found at", SAMPLE)
        return
    with zipfile.ZipFile(SAMPLE) as z:
        files = {i.filename: z.read(i.filename) for i in z.infolist()}
    doc = files["word/document.xml"].decode("utf-8")
    # 1. the two italic guidance lines become our group line and colour key
    paras = re.findall(r"<w:p [^>]*>(?:(?!</w:p>).)*?</w:p>", doc, re.S)
    guide = [p for p in paras if "This is a guide only" in p or "Indicate the form" in p]
    assert len(guide) == 2, "sample layout changed"
    doc = doc.replace(guide[0], _para(GROUP, italic=True))
    doc = doc.replace(guide[1], _para(KEY, italic=True))
    # 2. keep the header row, replace the body rows with ours
    tbl = re.search(r"<w:tbl>.*?</w:tbl>", doc, re.S).group(0)
    rows = re.findall(r"<w:tr[ >].*?</w:tr>", tbl, re.S)
    body = "".join(_row(v, k, s) for v, k, s, _ in tutor_rows()) + "".join(_row([""] * 6, "", False)
                                                                          for _ in range(3))
    new_tbl = tbl.replace("".join(rows), rows[0] + body)
    # header row repeats on every page
    new_tbl = new_tbl.replace(rows[0], rows[0].replace("<w:tc>", "<w:trPr><w:tblHeader/></w:trPr><w:tc>", 1), 1)
    doc = doc.replace(tbl, new_tbl)
    # 3. footnote line after the table (from the group's Register)
    doc = doc.replace("</w:tbl>", "</w:tbl>" + _para(FOOT, size=18), 1)
    files["word/document.xml"] = doc.encode("utf-8")
    # 4. document properties: our title
    core = files["docProps/core.xml"].decode("utf-8")
    core = re.sub(r"<dc:title>.*?</dc:title>", "<dc:title>Architects Register — SOH Scenario 1</dc:title>", core)
    files["docProps/core.xml"] = core.encode("utf-8")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)
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
        "# 20 — Architects Register v3 (tutor's format, matched to the timeline)",
        "",
        "- **Date:** 2026-10-04. Replaces `14-document-register-v2.md`. **Generated** by "
        "`programme/build_register_v3.py` from `programme/register_v3.py` — edit that file, then re-run.",
        "- **Format = the course's `Document Register Sample 2026-1.docx`:** Date · Document · Form No. · From/To · "
        "Details (cost etc) · Student Contribution. **Green** = forms that are part of our assessment; **grey** = "
        "project milestones. Files: `document-register-v3.docx` (built on the tutor's own template), `.csv`, `.xlsx`.",
        "- **Every date matches the timeline** (`programme/Timeline of significant project events.xlsx`); the build script checks this. "
        "*Italic* dates here = month assumed [A]. *(suggested)* = contribution not yet confirmed by that person "
        "(grey text in the .docx / .xlsx).",
        "- Contract figures (contract sum $9,600,000; +1 month; +$5,000) are the tutor's worked example, as in "
        "`programme/soh_scenario1_timeline.xlsx`.",
        "",
        "## Register",
        "",
        "| " + " | ".join(TUTOR_HEADS) + " |",
        "|" + "---|" * len(TUTOR_HEADS),
    ]
    for vals, kind, suggested, assumed in tutor_rows():
        v = list(vals)
        v[0] = f"*{v[0]}*" if assumed else v[0]
        if kind == "form":
            v[1] = f"**{v[1]}**"
        if suggested and v[5]:
            v[5] = f"{v[5]} *(suggested)*"
        lines.append("| " + " | ".join(v) + " |")
    lines += ["", FOOT, "", "## What changed from v2, and why", "",
              "Format: switched from the group's 8-column Register (From and To split; Action; Contributor; "
              "Checker) to the tutor's 6 columns (From/To combined; Details (cost etc); Student Contribution = the "
              "contributor). The checkers are kept in `programme/register_v3.py`.", "",
              "| Date | Row | Change | Source |", "|---|---|---|---|"]
    for row in REGISTER:
        if row[10]:
            lines.append(f"| {row[0]} | {row[1]} | {row[10]} | {link(row[11])} |")
    lines += [
        "",
        "## Still to confirm as a group",
        "",
        "- The *(suggested)* contributions (they follow the Register's own pattern: client rows to Lead 1, "
        "procurement rows to Lead 2, contract-administration rows to Lead 3).",
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
    write_docx(os.path.join(UP, "document-register-v3.docx"))
    write_csv(os.path.join(UP, "document-register-v3.csv"))
    write_xlsx(os.path.join(UP, "document-register-v3.xlsx"))
    write_md(os.path.join(UP, "20-document-register-v3.md"))
