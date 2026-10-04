"""Board-layout timeline in Excel, one section per sheet, so each part is easy to edit.
Looks like ../timeline/soh-timeline-scenario1.png (the project board picture).

Two files
  soh_board_layout.xlsx    - our project (Scenario 1), filled in
  soh_board_template.xlsx  - the same sheets, empty, for a fresh start or another scenario

Sheets (same in both files)
  1 Cover              title, project lines, colour + shape legend, sheet index, how to edit
  2 Parties            who is who by party (Client, Architect, Builder, Engineer, Specialist consultant,
                       Supplier / manufacturer), years and sources
  3 Timeline           Design lanes D0-D4 above Contract lanes C1-C4, one shared year axis
                       (one column = one quarter), coloured by factor
  4 Timeline by party  the same timeline coloured by the party who acts
  3 Register           the Architects Register as a table (one row per document)
  4 Event cards        one card per required form / scenario event
  5 Workflow           the 10 steps of a research session, with a Done? dropdown
  6 Tasks              who does what, due, status dropdown
  7 Zoom 1961-62       the ABIC SW clock + the variation chain month by month; the diamonds are
                       formulas, so changing a date moves its diamond
  8 Events (data)      every event: summary, status, clickable source links
  9 Sources            every source key with its title, type and link
Also writes ../19-event-data.md, a reading copy of Events (data).

One source of truth: the events are read from build_scenario1_timeline.py; edit events there and
re-run both scripts. Editing directly in Excel also works (see the Cover sheet).

Run:  py build_board_layout.py [project.xlsx [template.xlsx]]
"""
import ast
import datetime as dt
import math
import os
import re
import sys

import openpyxl
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from event_notes import NOTES, PARTIES, ROLE_COLOURS, ROLES, SOURCES

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "build_scenario1_timeline.py")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "soh_board_layout.xlsx")
OUT_T = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "soh_board_template.xlsx")
D = dt.date
ARIAL = "Arial"

INK, NAVY, MUTED, RED, PAPER = "18202B", "1F4E78", "6B7280", "C00000", "FFFFFF"
FACTOR = {"Scope": "C8413B", "Time": "E0A030", "Cost": "1F7A8C",
          "Quality": "5E9E6E", "Responsibility": "7B6AA8", "Baseline": "BFBFBF"}
PHASES = [  # label, dates text, start, end (exclusive), tint
    ("P1  Client brief to Tender", "Sep 1955 – Jun 1958", D(1955, 9, 1), D(1958, 6, 1), "E6ECF3"),
    ("P2", "Jun 1958 – Mar 1959", D(1958, 6, 1), D(1959, 3, 1), "F4EBDD"),
    ("P3  Construction to Completion", "Mar 1959 – Oct 1973 (opening = PC)", D(1959, 3, 1), D(1973, 10, 1), "E8F1EA"),
    ("Defects + final cert.", "Oct 1973 – 31 May 1975", D(1973, 10, 1), D(1975, 6, 1), "EEEEEE"),
]
Y0, Y1 = 1954, 1978                      # grid years, inclusive
NQ = (Y1 - Y0 + 1) * 4                   # quarter columns
G0 = 4                                   # first grid column (D)
COL_W, COL_PX = 3.4, 29                  # quarter column width (chars) and its approx. pixels
CHAR_PX = 7.0                            # Arial 8 as rendered, average glyph width incl. spacing
SCENARIO = D(1961, 6, 1)
REQUIRED = {"SW-12", "SW-14", "SW-11", "SW-31", "GL1", "CAA", "SW 2018"}
CLAUSE = {"GL1": "Introductory letter", "CAA": "CAA 2024 (whole agreement)", "CAA D.8": "CAA D.8 additional services",
          "SW 2018": "ABIC SW 2018 + Schedule 1", "SW-12": "ABIC J1 (variation)", "SW-42": "ABIC H1–H2 (claim)",
          "SW-13": "ABIC J3 (instruction to proceed)", "SW-14": "ABIC H4 / L1 (adjustment of time)",
          "SW-11": "ABIC H4 / J5 (contract price adjustment)", "SW-31": "ABIC N11 (final certificate)",
          "CP-06": "Cost plan (QS)"}
FACTORS = ["Scope", "Time", "Cost", "Quality", "Responsibility"]

thin = Side(style="thin", color="D5D9DE")
grid = Side(style="thin", color="BFBFBF")
hair = Side(style="hair", color="D0D0D0")
redline = Side(style="medium", color=RED)
dash = Side(style="dashed", color="404040")
BOX = Border(left=grid, right=grid, top=grid, bottom=grid)


def fnt(size=9, bold=False, italic=False, color=INK):
    return Font(name=ARIAL, size=size, bold=bold, italic=italic, color=color)


def fill(hex_):
    return PatternFill(start_color=hex_, end_color=hex_, fill_type="solid")


def lighten(hex_, k=0.55):
    r, g, b = (int(hex_[i:i + 2], 16) for i in (0, 2, 4))
    return "".join(f"{int(v + (255 - v) * k):02X}" for v in (r, g, b))


def qcol(d):
    """Grid column of the quarter containing date d (clipped to the grid)."""
    k = (d.year - Y0) * 4 + (d.month - 1) // 3
    return G0 + max(0, min(NQ - 1, k))


def short(d):
    return d.strftime("%b %Y") if d.day == 1 else f"{d.day} {d.strftime('%b %Y')}"


def label_cols(text, bold=False):
    return math.ceil(len(text) * CHAR_PX * (1.12 if bold else 1.0) / COL_PX) + 1


def add_months(d, n):
    m = d.month - 1 + n
    return D(d.year + m // 12, m % 12 + 1, 1)


# ------------------------------------------------------------------ read events from the builder
class Recorder:
    """Stands in for the builder's Board: records groups, lanes and items instead of drawing."""

    def __init__(self):
        self.groups, self.items = [], []
        self._n = 0

    @property
    def row(self):
        return self._n

    def group(self, text, sub):
        self.groups.append({"text": text, "sub": sub, "lanes": []})

    def lane(self, code, name, sub, owner):
        self.groups[-1]["lanes"].append({"code": code, "name": name, "sub": sub, "owner": owner})

    def _add(self, **kw):
        kw["id"] = self._n
        self.items.append(kw)
        self._n += 1
        return kw["id"]

    def bar(self, code, name, start, end, factor, status, form="", frm_to="", who="", kind="Bar", linked=False,
            src=""):
        return self._add(code=code, name=name, start=start, end=end, factor=factor, status=status, form=form,
                         frm_to=frm_to, who=who, kind=kind, src=src, type="bar")

    def milestone(self, code, name, when, factor, status, form="", frm_to="", who="", gate=False, linked=False,
                  src=""):
        return self._add(code=code, name=name, start=when, end=None, factor=factor, status=status, form=form,
                         frm_to=frm_to, who=who, kind="Gate" if gate else "Milestone", src=src, type="ms")

    def scenario_marker(self, when, label):
        self.scenario = (when, label)


def load_events():
    text = open(SRC, encoding="utf-8").read()
    a = text.index("R = {}")
    b_ = text.index('notes(ws, b.row, "Reading the board"')
    rec = Recorder()
    ns = {"b": rec, "D": D, "POSS": "$F$6", "PC": "$F$7", "EOT": "$F$8", "S_COL": "F", "SCENARIO_DATE": SCENARIO}
    exec(compile(text[a:b_], SRC, "exec"), ns)
    # resolve the builder's cell formulas to dates
    inputs = {"$F$6": D(1959, 3, 2), "$F$7": D(1963, 1, 26)}
    by_id = {it["id"]: it for it in rec.items}
    for it in rec.items:
        for key in ("start", "end"):
            v = it[key]
            if isinstance(v, str):
                if v.lstrip("=") in inputs:
                    it[key] = inputs[v.lstrip("=")]
                else:
                    m = re.match(r"=EDATE\(F(\d+),\$F\$8\)", v)
                    it[key] = add_months(by_id[int(m.group(1))]["start"], 1)
    tree = ast.parse(text)
    tasks = next(ast.literal_eval(n.value) for n in tree.body
                 if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "tasks")
    return rec, ns["R"], tasks


# ------------------------------------------------------------------ item text + packing
def is_assumed(it):
    return "[A]" in it["status"] or "verify" in it["status"]


def is_required(it):
    return it["name"].startswith("★") or it["form"] in REQUIRED


def party_for(it):
    """(party, named party) for an event: who acts in it. Longest matching ROLES prefix wins."""
    n = it["name"].lstrip("★ ").strip()
    keys = [k for k in ROLES if n.startswith(k)]
    return ROLES[max(keys, key=len)] if keys else ("", "")


def item_colour(it, mode):
    if mode == "party":
        party = party_for(it)[0]
        return ROLE_COLOURS.get(party, "999999")
    return FACTOR[it["factor"]]


def clean(name):
    return name.lstrip("★ ").strip()


def with_form(form, n):
    if not form or form in n or (form.startswith("CAA ") and n.startswith(form[4:])):
        return n
    return f"{form}  {n}"


def bar_text(it):
    n = clean(it["name"])
    if it["end"] and it["end"].year > Y1:
        n += f" to {it['end'].year}"
    return with_form(it["form"], n)


def ms_text(it):
    tag = "  [A]" if is_assumed(it) else ""
    return f"{with_form(it['form'], clean(it['name']))}  · {short(it['start'])}{tag}"


def bar_cols(it):
    c0 = qcol(it["start"])
    c1 = qcol(it["end"] - dt.timedelta(days=1)) if it["end"] > it["start"] else c0
    return c0, c1


def fits_inside(text, c0, c1):
    return label_cols(text) * 1.2 + 1 <= c1 - c0 + 1


def ms_left(it):
    return qcol(it["start"]) + 1 + label_cols(ms_text(it), True) > G0 + NQ - 1


def extent(it):
    if it["type"] == "ms":
        c = qcol(it["start"])
        n = label_cols(ms_text(it), is_required(it) or is_assumed(it))
        return (c - 2 - n, c) if ms_left(it) else (c - 1, c + 1 + n)
    c0, c1 = bar_cols(it)
    t = bar_text(it)
    return (c0, c1) if fits_inside(t, c0, c1) else (c0, c1 + 1 + label_cols(t))


def pack(items, min_rows):
    rows = []
    for it in sorted(items, key=lambda i: (extent(i)[0], i["id"])):
        a, b_ = extent(it)
        for row in rows:
            if all(b_ + 1 < x or a > y + 1 for x, y in row["occ"]):
                row["occ"].append((a, b_))
                row["items"].append(it)
                break
        else:
            rows.append({"occ": [(a, b_)], "items": [it]})
    while len(rows) < min_rows:
        rows.append({"occ": [], "items": []})
    return rows


def phase_of(d):
    for label, _, a, b_, _ in PHASES:
        if a <= d < b_:
            return label.replace("  ", " ")
    return "after completion" if d >= PHASES[-1][3] else "before the brief"


# ------------------------------------------------------------------ small sheet helpers
def put(ws, r, c, v=None, font=None, fl=None, al=None, border=None, fmt=None):
    cell = ws.cell(row=r, column=c)
    if v is not None:
        cell.value = v
    if font:
        cell.font = font
    if fl:
        cell.fill = fl
    if al:
        cell.alignment = al
    if border:
        cell.border = border
    if fmt:
        cell.number_format = fmt
    return cell


def band(ws, r, c0, c1, hex_):
    for c in range(c0, c1 + 1):
        ws.cell(row=r, column=c).fill = fill(hex_)


def title(ws, text, sub, width_cols):
    put(ws, 1, 1, text, fnt(16, True))
    put(ws, 2, 1, sub, fnt(9, italic=True, color=MUTED))
    ws.row_dimensions[1].height = 24


def table_head(ws, r, heads):
    for i, (h, w) in enumerate(heads, start=1):
        put(ws, r, i, h, fnt(9, True, color=PAPER), fill("404040"), Alignment(vertical="center", wrap_text=True),
            BOX)
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[r].height = 20


def page(ws, landscape=True, a3=False):
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    if a3:
        ws.page_setup.paperSize = ws.PAPERSIZE_A3
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True


def status_dv(ws, rng, options='"To do,Doing,Done"'):
    dv = DataValidation(type="list", formula1=options, allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(rng)
    c0 = rng.split(":")[0]
    col = re.match(r"[A-Z]+", c0).group(0)
    row = re.search(r"\d+", c0).group(0)
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'${col}{row}="Done"'], fill=fill("C6EFCE")))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'${col}{row}="Doing"'], fill=fill("FFEB9C")))


# ------------------------------------------------------------------ 1 cover
def cover(ws, project):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 26
    ws.column_dimensions["C"].width = 90
    if project:
        put(ws, 2, 2, "SYDNEY OPERA HOUSE — PROJECT TIMELINE", fnt(22, True))
        lines = [
            ("PP1 Assessment 3  |  A1 Timeline of significant project events  |  historical dates, contemporary "
             "instruments (CAA 2024 · ABIC Simple Works 2018)", MUTED, False),
            ("PROJECT — Scenario 1 (additional piers to support the roof). Dates = the group's Document Register + "
             "sources A–AF (see Events (data))", RED, True),
            ("Group: Kankawee Maksomboon / Prani Patton / Yu-Chun Ho     Lead 1: Kankawee Maksomboon     Lead 2: Yu-Chun Ho     Lead 3: Prani Patton     "
             "Version: v3 / 4 Oct 2026 (Leads 2–3 inferred from the Register — confirm)", NAVY, True),
        ]
    else:
        put(ws, 2, 2, "PROJECT NAME — PROJECT TIMELINE", fnt(22, True))
        lines = [("Unit · Assessment · A1 Timeline of significant project events", MUTED, False),
                 ("PROJECT — scenario name. Dates = Document Register + sources", RED, True),
                 ("Group: ______ / ______ / ______     Lead 1: ______     Lead 2: ______     Lead 3: ______     "
                  "Version: __", NAVY, True)]
    for i, (t, col, b) in enumerate(lines):
        put(ws, 3 + i, 2, t, fnt(10, b, color=col))
    ws.row_dimensions[2].height = 32
    r = 8
    put(ws, r, 2, "COLOUR BY FACTOR", fnt(9, True, color=MUTED))
    r += 1
    for k in FACTORS:
        put(ws, r, 2, k, fnt(9, True, color=PAPER), fill(FACTOR[k]))
        put(ws, r, 3, {"Scope": "what is being designed or built changed",
                       "Time": "dates, programme, delays, extensions of time",
                       "Cost": "budget, contract sum, fees, payments",
                       "Quality": "standards, materials, testing, defects",
                       "Responsibility": "who decides, who is engaged, who represents whom"}[k], fnt(9))
        r += 1
    r += 1
    put(ws, r, 2, "COLOUR BY PARTY  (Timeline by party sheet — same colours as the Miro Parties panel)",
        fnt(9, True, color=MUTED))
    r += 1
    for k, col in ROLE_COLOURS.items():
        put(ws, r, 2, k, fnt(9, True, color=PAPER), fill(col))
        put(ws, r, 3, {"Client": "NSW Government, Minister for Public Works, the Trust, Premiers and Ministers",
                       "Architect": "Utzon; then Hall, Todd & Littlemore (with Farmer)",
                       "Builder": "Civil & Civic (Stage I); M.R. Hornibrook (Stages II + III)",
                       "Engineer": "Ove Arup & Partners — lead structural / civil",
                       "Specialist consultant": "mechanical (Steensen & Varming), acoustics (Jordan), QS",
                       "Supplier / manufacturer": "Symonds, Waagner-Biro, GEC-Philips, AWA, K.F. Plastics, Sharp, Coburn"}[k],
            fnt(9))
        r += 1
    r += 1
    put(ws, r, 2, "SHAPES", fnt(9, True, color=MUTED))
    r += 1
    for sym, txt, col, brd in [("", "bar = a date range (filled cells, label in the first cell)", "9DB4C8", None),
                               ("◆", "milestone = one date (diamond, label in the next cell)", None, None),
                               ("■", "CAA client-approval gate", None, None),
                               ("★", "required form or scenario event (red star left of the diamond)", None, None),
                               ("", "dashed outline / italic label = [A] assumption or [verify]", None, "dash"),
                               ("", "grey dashed = planned baseline", "EDEDED", "dash"),
                               ("", "red line = our scenario (Jun 1961)", None, "red")]:
        c = put(ws, r, 2, sym, fnt(11, True, color=RED if sym == "★" else INK), fill(col) if col else None,
                Alignment(horizontal="center"))
        if brd == "dash":
            c.border = Border(left=dash, right=dash, top=dash, bottom=dash)
        elif brd == "red":
            c.border = Border(left=redline)
        put(ws, r, 3, txt, fnt(9))
        r += 1
    r += 1
    put(ws, r, 2, "SHEETS IN THIS FILE", fnt(9, True, color=MUTED))
    r += 1
    index = [("Parties", "who is who: every party by category (Client, Architect, Builder, Engineer, Specialist "
                         "consultant, Supplier / manufacturer), with years and sources"),
             ("Timeline", "Design lanes D0–D4 (CAA stages, client + brief, design output, consultants, interiors) "
                          "above Contract lanes C1–C4 (procurement + cost, construction, contract admin, fit-out)"),
             ("Timeline by party", "the same timeline, coloured by the party who acts in each event"),
             ("Register", "the Architects Register: one row per document (course sample columns)"),
             ("Event cards", "one card per required form / scenario event"),
             ("Workflow", "the 10 steps of each research session"),
             ("Tasks", "who does what, due, status"),
             ("Zoom 1961-62", "the ABIC SW clock + the variation chain month by month (diamonds follow the dates)"),
             ("Events (data)", "every event with a short summary, status and clickable source links"),
             ("Sources", "every source key: title, type (archive / official / scholarly / secondary), link")]
    for name, what in index:
        c = put(ws, r, 2, name, fnt(10, True, color="0563C1"))
        c.hyperlink = f"#'{name}'!A1"
        put(ws, r, 3, what, fnt(9))
        r += 1
    r += 1
    put(ws, r, 2, "HOW TO EDIT", fnt(9, True, color=MUTED))
    r += 1
    for t in ["Each section is its own sheet. Timelines: one column = one quarter; the exact date is written in "
              "each label.",
              "Add a milestone: copy a ◆ cell into the quarter, type the label in the next cell (or copy a whole "
              "existing milestone and edit it). Each lane has empty rows at the bottom for new events.",
              "Add a bar: select the quarters, fill them with the factor colour (Home to Fill), type the label in the "
              "first cell.",
              "Move an event: cut the ◆ cell and its label cell together and paste them in the new quarter.",
              "When you add or change an event on a timeline, change it in Events (data) and in the Register too, so "
              "the three stay the same.",
              "The Zoom sheet is formula-driven: type a new date in its Date column and the diamond moves.",
              "Google Sheets: File > Import > Upload > this .xlsx."]:
        put(ws, r, 2, "•", fnt(9))
        put(ws, r, 3, t, fnt(9), al=Alignment(wrap_text=True, vertical="top"))
        ws.row_dimensions[r].height = 26
        r += 1
    page(ws, landscape=False)


# ------------------------------------------------------------------ 2-3 timelines
def timeline(ws, rec, groups, project, sheet_title, sheet_sub, mode="factor"):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 36
    ws.column_dimensions["C"].width = 1.5
    for k in range(NQ):
        ws.column_dimensions[get_column_letter(G0 + k)].width = COL_W
    last = G0 + NQ - 1
    title(ws, sheet_title, sheet_sub, last)
    # legend (row 3): factor or party colours
    legend = ROLE_COLOURS if mode == "party" else {k: FACTOR[k] for k in FACTORS}
    put(ws, 3, 2, "COLOUR = PARTY WHO ACTS" if mode == "party" else "COLOUR = FACTOR THAT CHANGED",
        fnt(8, True, color=MUTED))
    for i, (k, col) in enumerate(legend.items()):
        c = G0 + i * 9
        band(ws, 3, c, c + 7, col)
        put(ws, 3, c, k, fnt(8, True, color=PAPER))
    # phases (row 4), scenario (row 5), years (row 6)
    put(ws, 4, 2, "PHASES", fnt(8, True, color=MUTED))
    ws.row_dimensions[4].height = 40
    for label, dates, a, b_, tint in PHASES:
        c0, c1 = qcol(a), qcol(b_) - 1
        band(ws, 4, c0, c1, tint)
        ws.merge_cells(start_row=4, start_column=c0, end_row=4, end_column=c1)
        put(ws, 4, c0, label if not project else f"{label}\n{dates}", fnt(8, True),
            al=Alignment(wrap_text=True, vertical="top"))
    sc = qcol(SCENARIO)
    if project:
        band(ws, 5, sc, sc + 19, "C8413B")
        put(ws, 5, sc, "OUR SCENARIO 1: additional piers to support the roof (Jun 1961)", fnt(8, True, color=PAPER))
    else:
        put(ws, 5, sc, "▼ scenario: move the red line to your scenario's quarter", fnt(8, True, color=RED))

    def years(r):
        put(ws, r, 2, "YEAR", fnt(8, True, color=MUTED))
        for y in range(Y0, Y1 + 1):
            c = G0 + (y - Y0) * 4
            ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c + 3)
            put(ws, r, c, y, fnt(8, y % 5 == 0, color=INK if y % 5 == 0 else MUTED),
                al=Alignment(horizontal="left"), fmt="0")
            for k in range(c, c + 4):
                ws.cell(row=r, column=k).border = Border(left=thin if k == c else None, bottom=thin, top=thin)
    years(6)
    ws.freeze_panes = ws.cell(row=7, column=G0)

    lane_rows, lane_last = [], set()
    by_lane = {}
    for it in rec.items:
        by_lane.setdefault(it["code"], []).append(it)
    r = 7
    for g in groups:
        band(ws, r, 1, last, INK)
        put(ws, r, 1, g["text"], fnt(10, True, color=PAPER))
        put(ws, r, G0 + 1, g["sub"], fnt(8, italic=True, color="C9D3DF"))
        ws.row_dimensions[r].height = 18
        r += 1
        for ln in g["lanes"]:
            rows = pack(by_lane.get(ln["code"], []) if project else [], 3)
            rows += [{"occ": [], "items": []}] * (2 if project else 3)      # spare rows for new events
            put(ws, r, 1, ln["code"], fnt(9, True, color=MUTED))
            put(ws, r, 2, ln["name"], fnt(10, True))
            put(ws, r + 1, 2, ln["sub"], fnt(7, color=MUTED))
            put(ws, r + 2, 2, ln["owner"] if project else "Lead _: ______  (check: ______)", fnt(8, True, color=NAVY))
            for k, row in enumerate(rows):
                rr = r + k
                band(ws, rr, 1, 2, "F7F8FA")
                for q in range(NQ):
                    d = D(Y0 + q // 4, (q % 4) * 3 + 1, 1)
                    tint = next((t for _, _, a, b_, t in PHASES if a <= d < b_), None)
                    if tint:
                        ws.cell(row=rr, column=G0 + q).fill = fill(lighten(tint))
                lane_rows.append(rr)
                for it in row["items"]:
                    draw_item(ws, rr, it, mode)
            lane_last.add(r + len(rows) - 1)
            r += len(rows)
    # grid lines, lane rules, scenario line
    for rr in lane_rows:
        is_last = rr in lane_last
        for c in [1, 2, 3] + list(range(G0, last + 1)):
            cell = ws.cell(row=rr, column=c)
            o = cell.border
            left = o.left if o.left and o.left.style else None
            if c >= G0 and (c - G0) % 4 == 0 and left is None:
                left = hair
            if project and c == sc:
                left = redline
            bottom = thin if is_last else (o.bottom if o.bottom and o.bottom.style else None)
            cell.border = Border(left=left, right=o.right, top=o.top, bottom=bottom)
    years(r)
    ws.print_title_rows = "4:6"
    page(ws, a3=True)


def draw_item(ws, r, it, mode="factor"):
    if it["type"] == "bar":
        c0, c1 = bar_cols(it)
        base, assumed = it["kind"] == "Baseline", is_assumed(it)
        col = "EDEDED" if base else item_colour(it, mode)
        for c in range(c0, c1 + 1):
            cell = ws.cell(row=r, column=c)
            cell.fill = fill(col)
            if base or assumed:
                cell.border = Border(top=dash, bottom=dash, left=dash if c == c0 else None,
                                     right=dash if c == c1 else None)
        t = bar_text(it)
        if fits_inside(t, c0, c1):
            put(ws, r, c0, t, fnt(8, True, color=INK if base else PAPER), al=Alignment(horizontal="left"))
        else:
            put(ws, r, c1 + 1, t, fnt(8, False, assumed), al=Alignment(horizontal="left"))
        return
    c = qcol(it["start"])
    star = is_required(it)
    if star:
        put(ws, r, c - 1, "★", fnt(9, True, color=RED), al=Alignment(horizontal="right"))
    put(ws, r, c, "■" if it["kind"] == "Gate" else "◆", fnt(11, True, color=item_colour(it, mode)),
        al=Alignment(horizontal="center"))
    f = fnt(8, star, is_assumed(it))
    if ms_left(it):
        put(ws, r, c - 2, ms_text(it), f, al=Alignment(horizontal="right"))
    else:
        put(ws, r, c + 1, ms_text(it), f, al=Alignment(horizontal="left"))


# ------------------------------------------------------------------ 4 register
def register(ws, rec, project):
    ws.sheet_view.showGridLines = False
    title(ws, "ARCHITECTS REGISTER", "Every event that issues a document gets one row here (course sample columns). "
                                     "Sorted by date. Yellow Status = [A] assumption or [verify].", 8)
    heads = [("Date", 13), ("Document", 58), ("Form No.", 11), ("From / To", 26), ("Details / clause", 34),
             ("Student contribution", 18), ("Status", 14), ("Source", 10)]
    table_head(ws, 4, heads)
    rows = sorted((it for it in rec.items if it["form"] and not it["form"].startswith("CAA A.")),
                  key=lambda i: i["start"]) if project else []
    r = 5
    for it in rows:
        vals = [it["start"], clean(it["name"]), it["form"], it["frm_to"], CLAUSE.get(it["form"], ""), it["who"],
                it["status"], it["src"]]
        for c, v in enumerate(vals, start=1):
            put(ws, r, c, v, fnt(9, c == 3), border=BOX, fmt="d mmm yyyy" if c == 1 else None,
                al=Alignment(vertical="center", wrap_text=c in (2, 5)))
        if is_assumed(it):
            ws.cell(row=r, column=7).fill = fill("FFF2CC")
        r += 1
    for _ in range(15 if project else 30):                       # empty rows to add documents
        for c in range(1, len(heads) + 1):
            put(ws, r, c, border=BOX, fmt="d mmm yyyy" if c == 1 else None)
        r += 1
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:H{r - 1}"
    page(ws)


# ------------------------------------------------------------------ 5 event cards
CARD_KEYS = ["E-ID  |  Date(s)", "Event", "Timeline  /  lane", "Phase", "Initiated by / must respond",
             "Party (who acts)", "Factor changed", "[F] fact / [A] assumption + source", "Documents + clause",
             "Student  (lead / research / check)"]


def event_cards(ws, rec, R, project):
    ws.sheet_view.showGridLines = False
    title(ws, "EVENT CARDS", "One card per required form or scenario event. Copy a block (12 rows) to add one.", 3)
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 32
    ws.column_dimensions["C"].width = 80
    lane_name = {ln["code"]: (g["text"].split()[0].title(), ln["name"]) for g in rec.groups for ln in g["lanes"]}
    cards = []
    if project:
        picks = [it for it in rec.items if is_required(it) or it["form"] in ("SW-42", "SW-13", "CAA D.8")]
        picks += [rec.items[R[k]] for k in ("prob", "work") if rec.items[R[k]] not in picks]
        picks.sort(key=lambda i: i["start"])
        for n, it in enumerate(picks, start=1):
            tl, ln = lane_name[it["code"]]
            dates = short(it["start"]) + (f" – {short(it['end'])}" if it["end"] else "")
            cards.append((it["factor"], [
                f"S1-{n:02d}  |  {dates}", clean(it["name"]), f"{tl}  /  {it['code']} {ln}", phase_of(it["start"]),
                it["frm_to"] or "—", "  —  ".join(x for x in party_for(it) if x), it["factor"], f"{it['status']}  ·  source {it['src'] or '—'}",
                f"{it['form']}  {CLAUSE.get(it['form'], '')}".strip() or "—",
                it["who"] or "________ / ________ / ________"]))
    else:
        cards = [("Scope", [""] * len(CARD_KEYS)) for _ in range(4)]
    r = 4
    for factor, vals in cards:
        put(ws, r, 2, vals[1] if project else "EVENT CARD", fnt(10, True, color=PAPER), fill(FACTOR[factor]))
        band(ws, r, 1, 3, FACTOR[factor])
        r += 1
        for k, v in zip(CARD_KEYS, vals):
            ws.cell(row=r, column=1).fill = fill(FACTOR[factor])
            put(ws, r, 2, k, fnt(8, True, color=MUTED), border=Border(bottom=thin))
            cell = put(ws, r, 3, v, fnt(9, k == "Event"), border=Border(bottom=thin), al=Alignment(wrap_text=True))
            if k == "Party (who acts)" and v:
                party = v.split("  —  ")[0]
                if party in ROLE_COLOURS:
                    cell.fill = fill(lighten(ROLE_COLOURS[party], 0.7))
            r += 1
        r += 1
    page(ws, landscape=False)


# ------------------------------------------------------------------ 6 workflow
WORKFLOW = [
    "Research an event to write ONE event card",
    "Classify: Design or Contract timeline to choose its lane",
    "Place it on the year axis: bar if a range, diamond if one date",
    "Colour by the factor that changed (Scope / Time / Cost / Quality / Responsibility); note the party who acts",
    "Tag [F] + source key, or [A] + reason (dashed outline / italic)",
    "Note cause to consequence (which earlier card made this happen?)",
    "Planned vs actual: grey dashed baseline under the actual bar",
    "Scenario events: red star + add them to the Zoom sheet (months)",
    "Card issues a document? to add the Register row the same day",
    "Weekly: each lead checks their lanes; the checker filters for [A] gaps",
]


def workflow(ws):
    ws.sheet_view.showGridLines = False
    title(ws, "WORKFLOW", "Each research session, in this order. Tick Done as you go.", 4)
    table_head(ws, 4, [("#", 5), ("Step", 80), ("Who", 16), ("Done?", 10)])
    for i, st in enumerate(WORKFLOW):
        r = 5 + i
        put(ws, r, 1, i + 1, fnt(9, True, color=PAPER), fill(INK), Alignment(horizontal="center"), BOX)
        put(ws, r, 2, st, fnt(10), border=BOX)
        put(ws, r, 3, border=BOX)
        put(ws, r, 4, border=BOX)
        ws.row_dimensions[r].height = 20
    status_dv(ws, f"D5:D{4 + len(WORKFLOW)}", '"To do,Doing,Done"')
    page(ws)


# ------------------------------------------------------------------ 7 tasks
def tasks_sheet(ws, tasks, project):
    ws.sheet_view.showGridLines = False
    title(ws, "TASK ASSIGNMENT", "From the Register and the timelines. Status is a dropdown (To do / Doing / Done). "
                                 "Leads 2–3 inferred from the Register — confirm.", 7)
    table_head(ws, 4, [("Lead", 10), ("Name", 22), ("Lanes owned", 26), ("Checker", 22), ("Task", 72), ("Due", 16),
                       ("Status", 10)])
    rows = [list(t) + ["To do"] for t in tasks] if project else []
    rows += [[""] * 7 for _ in range(6 if project else 16)]
    for i, row in enumerate(rows):
        r = 5 + i
        for c, v in enumerate(row, start=1):
            put(ws, r, c, v or None, fnt(9, c == 2), border=BOX, al=Alignment(vertical="center", wrap_text=c == 5))
    last = 4 + len(rows)
    status_dv(ws, f"G5:G{last}")
    for lead, col in [("Lead 1", "DDEBF7"), ("Lead 2", "E2EFDA"), ("Lead 3", "FCE4D6"), ("All", "EDEDED")]:
        ws.conditional_formatting.add(f"A5:A{last}", FormulaRule(formula=[f'$A5="{lead}"'], fill=fill(col)))
    ws.freeze_panes = "A5"
    page(ws)


# ------------------------------------------------------------------ 8 zoom
CLOCK = [("SW-12", "Instruction for a variation", "J1", "before PC", "yes"),
         ("notice", "Contractor notifies the effect", "J2.3", "20 WD", ""),
         ("SW-13", "Instruction to proceed?", "J3", "5 WD", "optional"),
         ("SW-42", "Contractor's claim", "H1–H2", "20 WD", "optional"),
         ("SW-14 / SW-11", "Decision: time / price", "H4", "20 WD", "yes"),
         ("cert.", "Progress certificate", "J5 / N4", "10 BD", ""),
         ("PC", "Notice of practical completion", "M4", "5 WD", ""),
         ("DLP", "Defects liability period", "M13", "12 months", ""),
         ("SW-49", "Final claim", "N10", "20 WD", ""),
         ("SW-31", "Final certificate", "N11", "10 BD", "yes")]


def zoom(ws, rec, R, project):
    ws.sheet_view.showGridLines = False
    title(ws, "ZOOM 1961–62 — the variation chain month by month + the ABIC SW clock",
          "Diamonds are formulas: type a new date in column D and its diamond moves. Required = red.", 30)
    # ABIC clock table
    put(ws, 4, 1, "ABIC SW CLOCK", fnt(10, True, color=RED))
    for i, (h, w) in enumerate([("Form", 14), ("Step", 46), ("Clause", 26), ("Date", 13), ("Required?", 11)],
                               start=1):
        put(ws, 5, i, h, fnt(9, True, color=PAPER), fill("404040"), border=BOX)
        ws.column_dimensions[get_column_letter(i)].width = w
    put(ws, 5, 6, "Time limit", fnt(9, True, color=PAPER), fill("404040"), border=BOX)
    for k, (form, step, cl, limit, req) in enumerate(CLOCK):
        r = 6 + k
        for c, v in enumerate([form, step, cl, None, req, limit], start=1):
            put(ws, r, c, v, fnt(9, c == 1, color=RED if req == "yes" and c == 1 else INK), border=BOX)
    # month grid: event table + 24 month columns
    top = 6 + len(CLOCK) + 2
    put(ws, top, 1, "THE CHAIN", fnt(10, True, color=RED))
    hr = top + 1
    for i, h in enumerate(["Form", "Event", "Who", "Date", "Required?"], start=1):
        put(ws, hr, i, h, fnt(9, True, color=PAPER), fill("404040"), border=BOX)
    m0 = 7                                                      # first month column (G)
    ws.column_dimensions["F"].width = 10
    put(ws, hr, 6, "Start", fnt(8, True, color=MUTED))
    put(ws, hr - 1, m0, D(1961, 1, 1), fnt(9, True, color="0000FF"), fill("FFFF00"), fmt="yyyy")
    put(ws, hr - 1, m0 + 1, "← first month of the grid (input)", fnt(8, italic=True, color=MUTED))
    for k in range(24):
        c = m0 + k
        ws.column_dimensions[get_column_letter(c)].width = 4.2
        v = f"={get_column_letter(m0)}{hr - 1}" if k == 0 else f"=EDATE({get_column_letter(c - 1)}{hr},1)"
        put(ws, hr, c, v, fnt(8, True, color=PAPER), fill(RED if k % 12 == 0 else "404040"),
            Alignment(horizontal="center"), BOX, fmt="mmm")
    keys = ("prob", "d8", "sw12", "sw42", "sw13", "work", "sw14", "cp06", "sw11")
    chain = [rec.items[R[k]] for k in keys] if project else []
    n = len(chain) + (4 if project else 12)
    for i in range(n):
        r = hr + 1 + i
        it = chain[i] if i < len(chain) else None
        vals = [it["form"], clean(it["name"]), it["who"], it["start"], "yes" if is_required(it) else ""] if it \
            else [None] * 5
        for c, v in enumerate(vals, start=1):
            put(ws, r, c, v, fnt(9, c == 1 or (c == 2 and bool(it) and is_required(it))), border=BOX,
                fmt="d mmm yyyy" if c == 4 else None)
        for k in range(24):
            L = get_column_letter(m0 + k)
            put(ws, r, m0 + k, f'=IF(AND($D{r}<>"",$D{r}>={L}${hr},$D{r}<EDATE({L}${hr},1)),"◆","")',
                fnt(10, True, color=INK), al=Alignment(horizontal="center"),
                border=Border(left=hair, bottom=Side(style="hair", color="EEEEEE")))
    rng = f"{get_column_letter(m0)}{hr + 1}:{get_column_letter(m0 + 23)}{hr + n}"
    first = f"{get_column_letter(m0)}{hr + 1}"
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND({first}="◆",$E{hr + 1}="yes")'],
                                                   fill=fill("F4C7C3"), font=Font(color=RED, bold=True)))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'{first}="◆"'], fill=fill("E7EBEF")))
    put(ws, hr + n + 2, 1, "WD = working days, BD = business days. Months inside the Register's years are [A] — agree "
                           "them as a group. SW-31 (31 May 1975) is outside this window.",
        fnt(8, italic=True, color=MUTED))
    ws.freeze_panes = ws.cell(row=hr + 1, column=m0)
    page(ws)


# ------------------------------------------------------------------ 9 data + sources
def src_keys(src):
    return [k for k in re.split(r"[,/]\s*|\s+", src or "") if k and k in SOURCES]


def note_for(it):
    n = clean(it["name"])
    keys = [k for k in NOTES if n.startswith(k)]
    return NOTES[max(keys, key=len)] if keys else ""


def data_sheet(ws, rec, project):
    ws.sheet_view.showGridLines = False
    title(ws, "EVENTS (DATA)", "Every event on the Timeline, by lane and date: the party who acts, a short summary "
                               "and clickable source links. Source keys are explained on the Sources sheet. Yellow "
                               "Status = [A] assumption or [verify]. Filter the Party column to see one party's events.",
          11)
    heads = [("Lane", 6), ("Date", 12), ("End", 12), ("Event", 40), ("Party", 15), ("Named party", 24),
             ("Summary — what happened and why it matters", 66), ("Factor", 13), ("Status", 14), ("Source keys", 10),
             ("Link 1", 26), ("Link 2", 26), ("Link 3", 26), ("Form", 9), ("From / To", 22), ("Student", 26)]
    table_head(ws, 4, heads)
    order = {ln["code"]: k for k, ln in enumerate(l for g in rec.groups for l in g["lanes"])}
    items = sorted(rec.items, key=lambda i: (order.get(i["code"], 99), i["start"])) if project else []
    r = 5
    missing = []
    for it in items:
        summ = note_for(it)
        party, named = party_for(it)
        if not summ or not party:
            missing.append(clean(it["name"]))
        vals = [it["code"], it["start"], it["end"], clean(it["name"]), party, named, summ, it["factor"],
                it["status"], it["src"]]
        for c, v in enumerate(vals, start=1):
            put(ws, r, c, v, fnt(9, c == 4), border=BOX, fmt="d mmm yyyy" if c in (2, 3) else None,
                al=Alignment(vertical="top", wrap_text=c in (4, 6, 7)))
        if party in ROLE_COLOURS:
            ws.cell(row=r, column=5).fill = fill(ROLE_COLOURS[party])
            ws.cell(row=r, column=5).font = fnt(9, True, color=PAPER)
        keys = src_keys(it["src"])[:3]
        for j in range(3):
            cell = put(ws, r, 11 + j, border=BOX, al=Alignment(vertical="top", wrap_text=True))
            if j < len(keys):
                k = keys[j]
                t, kind, url = SOURCES[k]
                cell.value = f"{k} · {t}"
                if url:
                    cell.hyperlink = url
                    cell.font = Font(name=ARIAL, size=8, color="0563C1", underline="single")
                else:
                    cell.font = fnt(8, italic=True, color=MUTED)
        for c, v in enumerate([it["form"], it["frm_to"], it["who"]], start=14):
            put(ws, r, c, v, fnt(9, c == 14), border=BOX, al=Alignment(vertical="top", wrap_text=True))
        ws.cell(row=r, column=8).fill = fill(lighten(FACTOR[it["factor"]], 0.6))
        if is_assumed(it):
            ws.cell(row=r, column=9).fill = fill("FFF2CC")
        links_len = max([len(SOURCES[k][0]) for k in keys] or [0])
        lines = max(math.ceil(len(summ) / 74), math.ceil(len(clean(it["name"])) / 42),
                    math.ceil(len(named) / 24), math.ceil(links_len / 30), 2)
        ws.row_dimensions[r].height = 12.5 * lines + 3
        r += 1
    for _ in range(10 if project else 40):
        for c in range(1, len(heads) + 1):
            put(ws, r, c, border=BOX, fmt="d mmm yyyy" if c in (2, 3) else None,
                al=Alignment(vertical="top", wrap_text=c in (4, 6, 7)))
        r += 1
    dv = DataValidation(type="list", formula1='"' + ",".join(FACTORS + ["Baseline"]) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"H5:H{r - 1}")
    dv2 = DataValidation(type="list", formula1='"' + ",".join(ROLE_COLOURS) + '"', allow_blank=True)
    ws.add_data_validation(dv2)
    dv2.add(f"E5:E{r - 1}")
    for party, col in ROLE_COLOURS.items():          # new rows pick up the colour too
        ws.conditional_formatting.add(f"E5:E{r - 1}", FormulaRule(formula=[f'$E5="{party}"'], fill=fill(col),
                                                                   font=Font(color=PAPER, bold=True)))
    ws.freeze_panes = "E5"
    ws.auto_filter.ref = f"A4:P{r - 1}"
    page(ws, a3=True)
    if missing:
        print("events without a summary or party:", missing)
    return items


def parties_sheet(ws, project):
    ws.sheet_view.showGridLines = False
    title(ws, "PARTIES", "Who is who, by category — the group's Miro Parties panel, corrected and sourced "
                         "(18-miro-board-verified.md). Colours match the Timeline by party sheet.", 6)
    table_head(ws, 4, [("Party", 22), ("Named party", 40), ("Role on the project", 64), ("Years", 24),
                       ("Source keys", 12), ("Link", 40)])
    r = 5
    for party, named, role, years, src in (PARTIES if project else []):
        put(ws, r, 1, party, fnt(9, True, color=PAPER), fill(ROLE_COLOURS[party]), Alignment(vertical="top"), BOX)
        put(ws, r, 2, named, fnt(9, True), border=BOX, al=Alignment(wrap_text=True, vertical="top"))
        put(ws, r, 3, role, fnt(9), border=BOX, al=Alignment(wrap_text=True, vertical="top"))
        put(ws, r, 4, years, fnt(9), border=BOX, al=Alignment(vertical="top"))
        put(ws, r, 5, src, fnt(9), border=BOX, al=Alignment(vertical="top"))
        keys = src_keys(src)
        cell = put(ws, r, 6, border=BOX, al=Alignment(wrap_text=True, vertical="top"))
        if keys and SOURCES[keys[0]][2]:
            cell.value = f"{keys[0]} · {SOURCES[keys[0]][0]}"
            cell.hyperlink = SOURCES[keys[0]][2]
            cell.font = Font(name=ARIAL, size=8, color="0563C1", underline="single")
        link_len = len(SOURCES[keys[0]][0]) + 5 if keys else 0
        ws.row_dimensions[r].height = 12.5 * max(math.ceil(len(role) / 62), math.ceil(len(named) / 38),
                                                 math.ceil(link_len / 44), 1) + 4
        r += 1
    for _ in range(6 if project else 30):
        for c in range(1, 7):
            put(ws, r, c, border=BOX)
        r += 1
    dv = DataValidation(type="list", formula1='"' + ",".join(ROLE_COLOURS) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"A5:A{r - 1}")
    for party, col in ROLE_COLOURS.items():
        ws.conditional_formatting.add(f"A5:A{r - 1}", FormulaRule(formula=[f'$A5="{party}"'], fill=fill(col),
                                                                   font=Font(color=PAPER, bold=True)))
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:F{r - 1}"
    page(ws)


def sources_sheet(ws, project):
    ws.sheet_view.showGridLines = False
    title(ws, "SOURCES", "Every source key used on the Timeline and in Events (data). Verified in "
                         "15-sources-A-J-verified.md (A–J), 17-interiors-1967-1975.md (K–T) and "
                         "18-miro-board-verified.md (U–AF).", 4)
    table_head(ws, 4, [("Key", 7), ("Source", 70), ("Type", 26), ("Link", 60)])
    r = 5
    for k, (t, kind, url) in (SOURCES.items() if project else []):
        put(ws, r, 1, k, fnt(9, True), border=BOX)
        put(ws, r, 2, t, fnt(9), border=BOX, al=Alignment(wrap_text=True))
        put(ws, r, 3, kind, fnt(9, color=RED if kind == "Unverified" else INK), border=BOX)
        cell = put(ws, r, 4, url or "— (no web link)", border=BOX)
        if url:
            cell.hyperlink = url
            cell.font = Font(name=ARIAL, size=8, color="0563C1", underline="single")
        else:
            cell.font = fnt(8, italic=True, color=MUTED)
        r += 1
    for _ in range(5 if project else 25):
        for c in range(1, 5):
            put(ws, r, c, border=BOX)
        r += 1
    ws.freeze_panes = "A5"
    page(ws)


def write_markdown(items, rec, path):
    """A reading copy of Events (data): one section per lane, summary + linked sources."""
    lanes = {ln["code"]: ln["name"] for g in rec.groups for ln in g["lanes"]}
    by = {}
    for it in items:
        by.setdefault(it["code"], []).append(it)
    out = ["# 19 — Event data: what happened, who acted, why it matters, and the sources",
           "",
           "- **Generated** by `programme/build_board_layout.py` from `programme/build_scenario1_timeline.py` "
           "(events) and `programme/event_notes.py` (summaries + source links). Edit those, then re-run; "
           "don't edit this file by hand.",
           "- Same content as the **Events (data)** and **Sources** sheets of `programme/soh_board_layout.xlsx`.",
           "- `[A]` = our assumption · `[verify]` = not yet confirmed · REG = the group's Document Register · "
           "tutor = instruction video (no web link).",
           ""]
    for code, its in by.items():
        out += [f"## {code} — {lanes.get(code, '')}", ""]
        for it in its:
            when = short(it["start"]) + (f" – {short(it['end'])}" if it["end"] else "")
            links = []
            for k in src_keys(it["src"]):
                t, kind, url = SOURCES[k]
                links.append(f"[{k}: {t}]({url})" if url else f"{k}: {t}")
            tag = f"  `{it['status']}`" if is_assumed(it) else ""
            form = f" · **{it['form']}**" if it["form"] else ""
            party, named = party_for(it)
            out.append(f"**{when} — {clean(it['name'])}**{form}{tag}  ")
            out.append(f"*Party:* {party} — {named}  ")
            out.append(f"{note_for(it)}  ")
            out.append(f"*Sources:* {' · '.join(links) or '—'}")
            out.append("")
    out += ["## Parties", "", "| Party | Named party | Role on the project | Years | Sources |",
            "|---|---|---|---|---|"]
    for party, named, role, years, src in PARTIES:
        out.append(f"| {party} | {named} | {role} | {years} | {src} |")
    out += ["", "## Source list", "", "| Key | Source | Type |", "|---|---|---|"]
    for k, (t, kind, url) in SOURCES.items():
        out.append(f"| {k} | {f'[{t}]({url})' if url else t} | {kind} |")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("wrote", os.path.normpath(path))


# ------------------------------------------------------------------ assemble
def workbook(rec, R, tasks, project, out):
    wb = openpyxl.Workbook()
    cover(wb.active, project)
    wb.active.title = "Cover"
    parties_sheet(wb.create_sheet("Parties"), project)
    g = {grp["text"]: grp for grp in rec.groups}
    timeline(wb.create_sheet("Timeline"), rec, [g["DESIGN TIMELINE"], g["CONTRACT TIMELINE"]], project,
             "PROJECT TIMELINE — Design (CAA 2024) + Contract (ABIC Simple Works 2018)",
             "Design lanes D0–D4 = Lead 1; Contract lanes C1–C2 = Lead 2, C3 = Lead 3. One column = one quarter; "
             "the exact date is in each label. Frozen: lane names + years.")
    timeline(wb.create_sheet("Timeline by party"), rec, [g["DESIGN TIMELINE"], g["CONTRACT TIMELINE"]], project,
             "PROJECT TIMELINE BY PARTY — who acts in each event",
             "Design lanes D0–D4 = Lead 1; Contract lanes C1–C2 = Lead 2, C3 = Lead 3. One column = one quarter; "
             "the exact date is in each label. Frozen: lane names + years.", mode="party")
    register(wb.create_sheet("Register"), rec, project)
    event_cards(wb.create_sheet("Event cards"), rec, R, project)
    workflow(wb.create_sheet("Workflow"))
    tasks_sheet(wb.create_sheet("Tasks"), tasks, project)
    zoom(wb.create_sheet("Zoom 1961-62"), rec, R, project)
    items = data_sheet(wb.create_sheet("Events (data)"), rec, project)
    sources_sheet(wb.create_sheet("Sources"), project)
    wb.save(out)
    print("wrote", out)
    return items


def main():
    rec, R, tasks = load_events()
    items = workbook(rec, R, tasks, True, OUT)
    workbook(rec, R, tasks, False, OUT_T)
    write_markdown(items, rec, os.path.join(HERE, "..", "19-event-data.md"))
    print(len(rec.items), "events")


if __name__ == "__main__":
    main()
