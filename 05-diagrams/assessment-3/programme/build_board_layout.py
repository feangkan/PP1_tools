"""Board-layout timeline in Excel, laid out like ../timeline/soh-timeline-scenario1.png
(the project board picture), not like the Option 1/2 Gantt table.

Sheets
  1 Template              - the empty layout: header, legend, phases, year axis, Design / Contract
                            lanes, Architects Register lane, and the four bottom panels
                            (event card, workflow, task assignment, zoom frame)
  2 Board - Scenario 1    - the same layout filled with our project
  3 Events (data)         - every event on the board as a table, with its source key

One source of truth: the events are read from build_scenario1_timeline.py (the lanes, bars,
milestones, forms, owners and source keys there), so edit events in that file and re-run both.

Excel / Google Sheets: one column per month. Bars are filled cells with the label written in the
first cell (it overflows across the bar); milestones are a diamond with the label beside it.
Rows inside a lane are packed so that labels never collide.

Run:  py build_board_layout.py [output.xlsx]   (default: soh_board_layout.xlsx next to this file)
"""
import ast
import datetime as dt
import math
import os
import re
import sys

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "build_scenario1_timeline.py")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "soh_board_layout.xlsx")
D = dt.date
ARIAL = "Arial"

INK, NAVY, MUTED, RED, PAPER = "18202B", "1F4E78", "6B7280", "C00000", "FFFFFF"
FACTOR = {"Scope": "C8413B", "Time": "E0A030", "Cost": "1F7A8C",
          "Quality": "5E9E6E", "Responsibility": "7B6AA8", "Baseline": "BFBFBF"}
PHASES = [  # label, dates text, start, end (exclusive), tint
    ("P1  Client brief → Tender", "Sep 1955 to Jun 1958", D(1955, 9, 1), D(1958, 6, 1), "E6ECF3"),
    ("P2  Tender → Start", "Jun 1958 to Mar 1959", D(1958, 6, 1), D(1959, 3, 1), "F4EBDD"),
    ("P3  Construction → Completion", "Mar 1959 to Oct 1973 (opening = PC)", D(1959, 3, 1), D(1973, 10, 1), "E8F1EA"),
    ("Defects + final cert.", "Oct 1973 to 31 May 1975", D(1973, 10, 1), D(1975, 6, 1), "EEEEEE"),
]
Y0, Y1 = 1954, 1976                      # grid years, inclusive
NM = (Y1 - Y0 + 1) * 12                  # month columns
G0 = 4                                   # first grid column (D)
COL_W, COL_PX = 1.0, 12                  # month column width (chars) and its approx. pixels
CHAR_PX = 7.0                            # Arial 8 as rendered, average glyph width incl. spacing
SCENARIO = D(1961, 6, 1)
REQUIRED = {"SW-12", "SW-14", "SW-11", "SW-31", "GL1", "CAA", "SW 2018"}

thin = Side(style="thin", color="D5D9DE")
hair = Side(style="hair", color="D9D9D9")
redline = Side(style="medium", color=RED)
dash = Side(style="dashed", color="404040")


def fnt(size=9, bold=False, italic=False, color=INK):
    return Font(name=ARIAL, size=size, bold=bold, italic=italic, color=color)


def fill(hex_):
    return PatternFill(start_color=hex_, end_color=hex_, fill_type="solid")


def mcol(d):
    """Grid column of the month containing date d (clipped to the grid)."""
    k = (d.year - Y0) * 12 + d.month - 1
    return G0 + max(0, min(NM - 1, k))


def short(d):
    return d.strftime("%b %Y") if d.day == 1 else f"{d.day} {d.strftime('%b %Y')}"


def label_cols(text, size=8, bold=False):
    return math.ceil(len(text) * CHAR_PX * (1.12 if bold else 1.0) * size / 8 / COL_PX) + 1


def ms_left(it):
    """True when a milestone label would run off the right edge: write it to the left instead."""
    return mcol(it["start"]) + 1 + label_cols(ms_text(it), bold=is_required(it) or is_assumed(it)) > G0 + NM - 1


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
    eot = 1
    by_id = {it["id"]: it for it in rec.items}
    for it in rec.items:
        for key in ("start", "end"):
            v = it[key]
            if isinstance(v, str):
                if v.lstrip("=") in inputs:
                    it[key] = inputs[v.lstrip("=")]
                else:
                    m = re.match(r"=EDATE\(F(\d+),\$F\$8\)", v)
                    it[key] = add_months(by_id[int(m.group(1))]["start"], eot)
    tree = ast.parse(text)
    tasks = next(ast.literal_eval(n.value) for n in tree.body
                 if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "tasks")
    return rec, ns["R"], tasks


# ------------------------------------------------------------------ sheet painter
class Sheet:
    def __init__(self, ws):
        self.ws = ws
        ws.sheet_view.showGridLines = False
        ws.column_dimensions["A"].width = 6
        ws.column_dimensions["B"].width = 40
        ws.column_dimensions["C"].width = 1.5
        for k in range(NM):
            ws.column_dimensions[get_column_letter(G0 + k)].width = COL_W
        self.lane_rows = []          # every row inside a lane (for grid lines + scenario line)
        self.lane_last = set()       # last row of each lane (bottom rule)

    def put(self, r, c, v=None, font=None, fl=None, al=None):
        cell = self.ws.cell(row=r, column=c)
        if v is not None:
            cell.value = v
        if font:
            cell.font = font
        if fl:
            cell.fill = fl
        if al:
            cell.alignment = al
        return cell

    def band(self, r, c0, c1, hex_):
        for c in range(c0, c1 + 1):
            self.ws.cell(row=r, column=c).fill = fill(hex_)

    def merge(self, r0, c0, r1, c1):
        if (r1, c1) != (r0, c0):
            self.ws.merge_cells(start_row=r0, start_column=c0, end_row=r1, end_column=c1)

    # ---- header
    def header(self, title, lines, project_line, group_line, start_year_input=False):
        ws = self.ws
        self.put(1, 1, title, fnt(20, True))
        self.put(2, 1, lines, fnt(9, color=MUTED))
        self.put(3, 1, project_line, fnt(9, True, color=RED))
        self.put(4, 1, group_line, fnt(9, True, color=NAVY))
        ws.row_dimensions[1].height = 28
        # legend, top right of the grid
        lx = G0 + 120
        self.put(1, lx, "COLOUR BY FACTOR", fnt(8, True, color=MUTED))
        for i, k in enumerate(["Scope", "Time", "Cost", "Quality", "Responsibility"]):
            c = lx + i * 20
            self.band(2, c, c + 2, FACTOR[k])
            self.put(2, c + 3, k, fnt(8))
        self.put(3, lx, "SHAPES", fnt(8, True, color=MUTED))
        shapes = [("bar", "bar = date range", "9DB4C8"), ("◆", "milestone = one date", None),
                  ("base", "baseline (planned)", "EDEDED"), ("dash", "dashed = [A] assumption", None),
                  ("★", "required form / scenario", None), ("|", "scenario marker", None),
                  ("■", "CAA approval gate", None)]
        for i, (sym, txt, col) in enumerate(shapes):
            c = lx + i * 24
            cell = self.put(4, c)
            if sym in ("bar", "base"):
                self.band(4, c, c + 2, col)
                if sym == "base":
                    for k in range(c, c + 3):
                        ws.cell(row=4, column=k).border = Border(top=dash, bottom=dash)
            elif sym == "dash":
                for k in range(c, c + 3):
                    ws.cell(row=4, column=k).border = Border(top=dash, bottom=dash,
                                                             left=dash if k == c else None,
                                                             right=dash if k == c + 2 else None)
            elif sym == "|":
                cell.border = Border(left=redline)
            else:
                cell.value = sym
                cell.font = fnt(10, True, color=RED if sym == "★" else INK)
                cell.alignment = Alignment(horizontal="center")
            self.put(4, c + 3, txt, fnt(8))
        if start_year_input:
            self.put(5, 1, "Start", fnt(8, True, color=MUTED))
            yc = self.put(5, 2, Y0, fnt(9, True, color="0000FF"), fill("FFFF00"), Alignment(horizontal="left"))
            self.year_input = f"$B$5"
            self.put(5, 3, None)
            self.put(5, G0, "← first year of the grid (yellow cell): the year labels follow · one column = one month",
                     fnt(8, italic=True, color=MUTED))

    def phases(self, r, blank=False):
        ws = self.ws
        self.put(r, 2, "PHASES\nthe three periods", fnt(8, True, color=MUTED), al=Alignment(wrap_text=True, vertical="top"))
        ws.row_dimensions[r].height = 30
        for label, dates, a, b_, tint in PHASES:
            c0, c1 = mcol(a), mcol(b_) - 1
            self.band(r, c0, c1, tint)
            for c in range(c0, c1 + 1):
                ws.cell(row=r, column=c).border = Border(top=thin, bottom=thin,
                                                         left=thin if c == c0 else None,
                                                         right=thin if c == c1 else None)
            self.merge(r, c0, r, c1)
            narrow = c1 - c0 < 14
            txt = label.split("  ")[0] if narrow else label
            if not blank:
                txt += "\n" + (dates.replace(" to ", "–").replace("19", "'") if narrow else dates)
            self.put(r, c0, txt, fnt(8, True), al=Alignment(wrap_text=True, vertical="top", horizontal="left"))

    def years(self, r, formula=False, label="YEAR"):
        ws = self.ws
        self.put(r, 2, label, fnt(8, True, color=MUTED))
        for y in range(Y0, Y1 + 1):
            c = G0 + (y - Y0) * 12
            v = f'=TEXT({self.year_input}+{y - Y0},"0")' if formula else str(y)
            self.put(r, c, v, fnt(8, y % 5 == 0, color=INK if y % 5 == 0 else MUTED), al=Alignment(horizontal="left"))
            for k in range(c, c + 12):
                ws.cell(row=r, column=k).border = Border(left=thin if k == c else None, bottom=thin)

    def scenario_label(self, r, text):
        c0 = mcol(SCENARIO)
        self.band(r, c0, c0 + 56, "C8413B")
        self.put(r, c0, text, fnt(8, True, color=PAPER))

    def group_band(self, r, text, sub):
        self.band(r, 1, G0 + NM - 1, INK)
        self.put(r, 1, text, fnt(10, True, color=PAPER))
        self.put(r, G0 + 1, sub, fnt(8, italic=True, color="C9D3DF"))
        self.ws.row_dimensions[r].height = 18

    def lane_block(self, r, code, name, sub, owner, nrows):
        rows = list(range(r, r + nrows))
        self.put(r, 1, code, fnt(9, True, color=MUTED))
        self.put(r, 2, name, fnt(10, True))
        self.put(r + 1, 2, sub, fnt(7, color=MUTED))
        self.put(r + 2, 2, owner, fnt(8, True, color=NAVY))
        for rr in rows:
            self.band(rr, 1, 2, "F7F8FA")
            for k in range(NM):
                d = D(Y0 + k // 12, k % 12 + 1, 1)
                tint = next((t for _, _, a, b_, t in PHASES if a <= d < b_), None)
                if tint:
                    self.ws.cell(row=rr, column=G0 + k).fill = fill(lighten(tint))
            self.lane_rows.append(rr)
        self.lane_last.add(rows[-1])
        return rows

    def finish_grid(self, scenario=True):
        """Year grid lines, lane bottom rules and the red scenario line, merged with item borders."""
        sc = mcol(SCENARIO)
        for rr in self.lane_rows:
            last = rr in self.lane_last
            for c in [1, 2, 3] + list(range(G0, G0 + NM)):
                cell = self.ws.cell(row=rr, column=c)
                old = cell.border
                left = old.left if old.left and old.left.style else None
                if c >= G0 and (c - G0) % 12 == 0 and left is None:
                    left = hair
                if scenario and c == sc:
                    left = redline
                bottom = thin if last else (old.bottom if old.bottom and old.bottom.style else None)
                cell.border = Border(left=left, right=old.right, top=old.top, bottom=bottom)

    # ---- items
    def bar(self, r, it):
        ws = self.ws
        c0, c1 = mcol(it["start"]), mcol(it["end"] - dt.timedelta(days=1)) if it["end"] > it["start"] else mcol(it["start"])
        base = it["kind"] == "Baseline"
        assumed = is_assumed(it)
        col = "EDEDED" if base else FACTOR[it["factor"]]
        for c in range(c0, c1 + 1):
            cell = ws.cell(row=r, column=c)
            cell.fill = fill(col)
            if base or assumed:
                cell.border = Border(top=dash, bottom=dash, left=dash if c == c0 else None,
                                     right=dash if c == c1 else None)
        text = bar_text(it)
        inside = fits_inside(text, c0, c1)
        if inside:
            self.put(r, c0, text, fnt(8, True, color=INK if base else PAPER), al=Alignment(horizontal="left"))
        else:
            self.put(r, c1 + 1, text, fnt(8, False, assumed, color=INK), al=Alignment(horizontal="left"))

    def milestone(self, r, it):
        c = mcol(it["start"])
        star = is_required(it)
        if star:
            self.put(r, c - 1, "★", fnt(9, True, color=RED), al=Alignment(horizontal="center"))
        sym = "■" if it["kind"] == "Gate" else "◆"
        self.put(r, c, sym, fnt(11, True, color=FACTOR[it["factor"]]), al=Alignment(horizontal="center"))
        if ms_left(it):
            self.put(r, c - 2, ms_text(it), fnt(8, star, is_assumed(it), color=INK), al=Alignment(horizontal="right"))
        else:
            self.put(r, c + 1, ms_text(it), fnt(8, star, is_assumed(it), color=INK), al=Alignment(horizontal="left"))


def lighten(hex_, k=0.55):
    r, g, b = (int(hex_[i:i + 2], 16) for i in (0, 2, 4))
    return "".join(f"{int(v + (255 - v) * k):02X}" for v in (r, g, b))


def is_assumed(it):
    s = it["status"]
    return "[A]" in s or "verify" in s


def is_required(it):
    return it["name"].startswith("★") or it["form"] in REQUIRED


def clean(name):
    return name.lstrip("★ ").strip()


def fits_inside(text, c0, c1):
    """White bold label inside the bar: bold runs ~20% wider than the packing estimate."""
    return label_cols(text) * 1.2 + 1 <= c1 - c0 + 1


def with_form(form, n):
    if not form or form in n or (form.startswith("CAA ") and n.startswith(form[4:])):
        return n
    return f"{form}  {n}"


def bar_text(it):
    n = clean(it["name"])
    if it["end"] and it["end"].year > Y1:
        n += f"  → {it['end'].year}"
    return with_form(it["form"], n)


def ms_text(it):
    n = clean(it["name"])
    n = with_form(it["form"], n)
    tag = "  [A]" if is_assumed(it) else ""
    return f"{n}  · {short(it['start'])}{tag}"


def extent(it):
    """Columns an item occupies on its row, label included (for packing)."""
    if it["type"] == "ms":
        c = mcol(it["start"])
        n = label_cols(ms_text(it), bold=is_required(it) or is_assumed(it))
        return (c - 2 - n, c) if ms_left(it) else (c - 1, c + 1 + n)
    c0 = mcol(it["start"])
    c1 = mcol(it["end"] - dt.timedelta(days=1)) if it["end"] > it["start"] else c0
    t = bar_text(it)
    return (c0, c1) if fits_inside(t, c0, c1) else (c0, c1 + 1 + label_cols(t))


def pack(items, min_rows=3):
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


# ------------------------------------------------------------------ bottom panels
EVENT_KEYS = ["E-ID  |  Date(s)", "Event", "Timeline  /  lane", "Phase", "Initiated by  →  must respond",
              "Factor changed", "[F] fact / [A] assumption", "Documents + clause",
              "Student  (lead / research / check)"]
EVENT_SW12 = ["S1-03  |  Aug 1961  [A] month (Register: 1961)",
              "Instruction for a Variation — strengthen columns, add piers",
              "Contract  /  C3 Contract administration", "P3 Construction → Completion",
              "Architect (Utzon)  →  Contractor (Civil & Civic)", "Scope   (+ Time 1 month, Cost $5,000)",
              "[A] month; figures = tutor's worked example; lead source AC (Murray, Saga)",
              "SW-12 (J1) → SW-14 (H4/L1) → SW-11 (H4/J5); CAA D.8", "Prani  /  ________  /  Jerry"]
WORKFLOW = [
    "Research an event → write ONE event card",
    "Classify: Design or Contract timeline → choose its lane",
    "Place on the month axis: bar if a range, diamond if one date",
    "Colour by the factor that changed (Scope / Time / Cost / Quality / Resp.)",
    "Tag [F] + source key, or [A] + reason (dashed outline / italic)",
    "Note cause → consequence (which earlier card made this happen?)",
    "Planned vs actual: grey dashed baseline under the actual bar",
    "Scenario events: red star + copy into the Zoom frame (months)",
    "Card issues a document? → add the Architects Register row the same day",
    "Weekly: each lead checks their lanes; the checker filters for [A] gaps",
]
CLOCK = [("SW-12", "Variation", "J1", "before PC", True), ("notice", "Effect", "J2.3", "20 WD", False),
         ("SW-13", "Proceed?", "J3", "5 WD", False), ("SW-42", "Claim", "H1-H2", "20 WD", False),
         ("SW-14 / 11", "Decision", "H4", "20 WD", True), ("cert.", "Progress", "J5 / N4", "10 BD", False),
         ("PC", "Notice", "M4", "5 WD", False), ("DLP", "Defects", "M13", "12 mo", False),
         ("SW-49", "Final claim", "N10", "20 WD", False), ("SW-31", "Final cert.", "N11", "10 BD", True)]


def box(sh, r0, c0, r1, c1, color, width="medium", dashed=False):
    s = Side(style="dashed" if dashed else width, color=color)
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            cell = sh.ws.cell(row=r, column=c)
            o = cell.border
            cell.border = Border(left=s if c == c0 else o.left, right=s if c == c1 else o.right,
                                 top=s if r == r0 else o.top, bottom=s if r == r1 else o.bottom)


def panels(sh, r0, project, tasks=None, zoom_items=None):
    ws = sh.ws
    H = 25                                           # panel height in rows
    for r in range(r0, r0 + H + 2):
        ws.row_dimensions[r].height = 16
    # 1 event card: label col B, values D..D+68
    sh.put(r0, 1, "EVENT CARD  (one per event — copy the block)", fnt(10, True))
    e0, e1 = G0, G0 + 68
    box(sh, r0 + 1, 1, r0 + 2 + 2 * len(EVENT_KEYS), e1, INK)
    for r in range(r0 + 1, r0 + 3 + 2 * len(EVENT_KEYS)):
        ws.cell(row=r, column=1).fill = fill(FACTOR["Scope"])
    for i, k in enumerate(EVENT_KEYS):
        r = r0 + 2 + 2 * i
        sh.put(r, 2, k, fnt(8, True, color=MUTED))
        v = EVENT_SW12[i] if project else ""
        sh.merge(r, e0, r, e1 - 1)
        sh.put(r, e0, v, fnt(9, i == 1))
        for c in range(2, e1):
            ws.cell(row=r, column=c).border = Border(bottom=Side(style="thin", color="E3E7EB"))
    # 2 workflow
    w0 = G0 + 74
    sh.put(r0, w0, "WORKFLOW  (each research session)", fnt(10, True))
    for i, st in enumerate(WORKFLOW):
        r = r0 + 2 + 2 * i
        sh.put(r, w0, str(i + 1), fnt(8, True, color=PAPER), fill(INK), Alignment(horizontal="center"))
        sh.merge(r, w0, r, w0 + 1)
        sh.put(r, w0 + 3, st, fnt(9))
    # 3 task assignment
    t0, t1 = G0 + 140, G0 + 205
    sh.put(r0, t0, "TASK ASSIGNMENT  (from the Register)", fnt(10, True))
    box(sh, r0 + 1, t0, r0 + H, t1, NAVY)
    for r in range(r0 + 1, r0 + H + 1):
        sh.band(r, t0, t1, "F7FAFD")
    leads = [("Lead 1", "LEAD 1 — FRANK", "lanes D0–D4  |  checker: Prani"),
             ("Lead 2", "LEAD 2 — JERRY", "lanes C1–C2  |  checker: Frank"),
             ("Lead 3", "LEAD 3 — PRANI", "lanes C3–C4  |  checker: Jerry"),
             ("All", "ALL THREE", "before the Week 12 presentation")]
    r = r0 + 2
    for key, head, sub in leads:
        sh.put(r, t0 + 1, head, fnt(9, True, color=NAVY))
        sh.put(r, t0 + 20, sub, fnt(7, color=MUTED))
        r += 1
        items = [t[4] for t in tasks if t[0] == key] if project else ["", ""]
        for it in items:
            sh.put(r, t0 + 2, "☐", fnt(9))
            sh.put(r, t0 + 4, it, fnt(8))
            r += 1
    # 4 zoom frame
    z0, z1 = G0 + 211, G0 + NM - 1
    sh.put(r0, z0, "ZOOM FRAME  (scenario by month + ABIC SW clock)", fnt(10, True))
    box(sh, r0 + 1, z0, r0 + H, z1, RED)
    for r in range(r0 + 1, r0 + H + 1):
        sh.band(r, z0, z1, "FFF7F6")
    cw = (z1 - z0 - 2) // 5
    for i, (form, name, cl, limit, req) in enumerate(CLOCK):
        rr, cc = divmod(i, 5)
        r = r0 + 2 + rr * 4
        c = z0 + 1 + cc * cw
        for k in range(3):
            sh.band(r + k, c, c + cw - 2, PAPER)
        box(sh, r, c, r + 2, c + cw - 2, RED if req else MUTED, "medium" if req else "thin", dashed=not req)
        sh.put(r, c + 1, form, fnt(9, True, color=RED if req else INK))
        sh.put(r + 1, c + 1, f"{name} ({cl})", fnt(7))
        sh.put(r + 2, c + 1, f"limit {limit}", fnt(7, color=MUTED))
    # month grid 1961-1962, two columns per month
    gy = r0 + 11
    gx = z0 + 2
    for yi, yr in enumerate((1961, 1962)):
        sh.put(gy, gx + yi * 24, str(yr), fnt(9, True, color=RED))
        for mi, m in enumerate("J F M A M J J A S O N D".split()):
            c = gx + (yi * 12 + mi) * 2
            sh.put(gy + 1, c, m, fnt(7, color=MUTED))
            for r in range(gy + 2, r0 + H):
                ws.cell(row=r, column=c).border = Border(left=Side(style="hair", color="F0C8C3"))
    if project:
        for i, it in enumerate(zoom_items):
            d = it["start"]
            c = gx + ((d.year - 1961) * 12 + d.month - 1) * 2
            r = gy + 2 + i
            req = is_required(it)
            sh.put(r, c, "◆", fnt(10, True, color=RED if req else MUTED), al=Alignment(horizontal="center"))
            who = f"   [{it['who']}]" if it["who"] else ""
            sh.put(r, c + 1, f"{it['form'] or ''}  {clean(it['name'])}{who}".strip(), fnt(7, req))
    sh.put(r0 + H, z0 + 1, "WD = working days, BD = business days. Red = required by the brief; dashed = optional "
                           "form or step. Months inside the Register's years are [A].", fnt(7, italic=True, color=MUTED))
    return r0 + H + 1


# ------------------------------------------------------------------ build one board
def build(ws, rec, R, tasks, project):
    sh = Sheet(ws)
    if project:
        sh.header("SYDNEY OPERA HOUSE — PROJECT TIMELINE",
                  "PP1 Assessment 3  |  A1 Timeline of significant project events  |  historical dates, contemporary "
                  "instruments (CAA 2024 · ABIC Simple Works 2018)  |  one column = one month",
                  "PROJECT — Scenario 1 (additional piers). Dates = group's Document Register + sources A–AF "
                  "(see Events sheet); dashed / italic = [A] month or [verify]",
                  "Group: Frank / Prani / Jerry     Lead 1: Frank     Lead 2: Jerry     Lead 3: Prani     "
                  "Version: v2 / 4 Oct 2026 (Leads 2–3 inferred from the Register — confirm)")
    else:
        sh.header("PROJECT NAME — PROJECT TIMELINE",
                  "Unit · Assessment · A1 Timeline of significant project events  |  one column = one month",
                  "PROJECT — scenario name. Dates = Document Register + sources; dashed = [A] assumption",
                  "Group: ______ / ______ / ______     Lead 1: ______     Lead 2: ______     Lead 3: ______     "
                  "Version: __",
                  start_year_input=True)
    sh.phases(6, blank=not project)
    if project:
        sh.scenario_label(7, "OUR SCENARIO 1: additional piers to support the roof (Jun 1961)")
    else:
        sh.put(7, mcol(SCENARIO), "▼ scenario marker: move the red line to your scenario's month",
               fnt(8, True, color=RED))
    sh.years(8, formula=not project)
    ws.freeze_panes = ws.cell(row=9, column=G0)
    r = 9
    by_lane = {}
    for it in rec.items:
        by_lane.setdefault(it["code"], []).append(it)
    for g in rec.groups:
        sh.group_band(r, g["text"], g["sub"])
        r += 1
        for ln in g["lanes"]:
            rows = pack(by_lane.get(ln["code"], []) if project else [], 3 if project else 4)
            rr = sh.lane_block(r, ln["code"], ln["name"], ln["sub"], ln["owner"] if project else "Lead _: ______",
                               len(rows))
            for k, row in enumerate(rows):
                for it in row["items"]:
                    (sh.bar if it["type"] == "bar" else sh.milestone)(rr[k], it)
            r += len(rows)
    # architects register lane: the document numbers under their dates
    sh.group_band(r, "ARCHITECTS REGISTER",
                  "every card that issues a document → one Register row (Date | Document | Form No. | From/To | "
                  "Details | Student contribution)")
    r += 1
    docs = [dict(it, type="ms", name=it["form"], form="", kind="Milestone", status="")
            for it in rec.items if it["form"]] if project else []
    rows = pack(docs, 3)
    rr = sh.lane_block(r, "", "Doc refs", "form no. under the event date", "", len(rows))
    for k, row in enumerate(rows):
        for it in row["items"]:
            c = mcol(it["start"])
            sh.put(rr[k], c, "▪", fnt(9, True, color=MUTED), al=Alignment(horizontal="center"))
            sh.put(rr[k], c + 1, f"{it['name']} · {short(it['start'])}", fnt(7, color=INK))
    r += len(rows)
    sh.finish_grid(scenario=project)
    sh.years(r, formula=not project, label="")
    r += 2
    zoom = [rec.items[R[k]] for k in ("prob", "d8", "sw12", "sw42", "sw13", "work", "sw14", "cp06", "sw11")] \
        if project else []
    end = panels(sh, r, project, tasks, zoom)
    if not project:
        sh.put(end + 1, 1, "HOW TO USE: copy this sheet, rename it, type the first year (B5), then fill each lane: "
                           "colour the month cells of a bar with its factor colour and write the label in the first "
                           "cell; for a milestone type ◆ in its month and the label in the next cell. Keep one "
                           "event per row inside a lane where labels would collide; add rows as needed.",
               fnt(8, italic=True, color=MUTED))
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A3
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    return sh


def data_sheet(ws, rec):
    ws.sheet_view.showGridLines = False
    heads = [("Lane", 6), ("Type", 10), ("Event", 70), ("Form", 10), ("Start", 12), ("End", 12), ("Factor", 14),
             ("Status", 16), ("Source", 12), ("From → To", 26), ("Student", 16)]
    ws["A1"] = "EVENTS ON THE BOARD — generated from build_scenario1_timeline.py"
    ws["A1"].font = fnt(13, True)
    ws["A2"] = ("Source keys: A–J in 15-sources-A-J-verified.md · K–T in 17-interiors-1967-1975.md · U–AF in "
                "18-miro-board-verified.md · REG = Document Register · tutor = instruction video")
    ws["A2"].font = fnt(8, italic=True, color=MUTED)
    for i, (h, w) in enumerate(heads, start=1):
        c = ws.cell(row=4, column=i, value=h)
        c.font, c.fill = fnt(9, True, color=PAPER), fill("404040")
        ws.column_dimensions[get_column_letter(i)].width = w
    order = {ln["code"]: k for k, ln in enumerate(l for g in rec.groups for l in g["lanes"])}
    items = sorted(rec.items, key=lambda i: (order.get(i["code"], 99), i["start"]))
    for r, it in enumerate(items, start=5):
        vals = [it["code"], it["kind"], clean(it["name"]), it["form"], it["start"], it["end"], it["factor"],
                it["status"], it["src"], it["frm_to"], it["who"]]
        for c, v in enumerate(vals, start=1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.font = fnt(9)
            if c in (5, 6) and v:
                cell.number_format = "d mmm yyyy"
        ws.cell(row=r, column=7).fill = fill(lighten(FACTOR[it["factor"]], 0.6))
        if is_assumed(it):
            ws.cell(row=r, column=8).fill = fill("FFF2CC")
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:K{4 + len(items)}"


def main():
    rec, R, tasks = load_events()
    wb = openpyxl.Workbook()
    t = wb.active
    t.title = "Template"
    build(t, rec, R, tasks, project=False)
    b = wb.create_sheet("Board - Scenario 1")
    build(b, rec, R, tasks, project=True)
    data_sheet(wb.create_sheet("Events (data)"), rec)
    wb.active = 1
    wb.save(OUT)
    print("wrote", OUT, "-", len(rec.items), "events")


if __name__ == "__main__":
    main()
