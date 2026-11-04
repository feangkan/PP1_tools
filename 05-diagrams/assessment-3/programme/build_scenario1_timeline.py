"""Scenario 1 project timeline in Excel, laid out like the project board
(../timeline/soh-timeline-scenario1.png): lanes grouped into a Design timeline and a
Contract timeline, each lane with its owner and checker, bars and milestones coloured by
the factor that changed, the three phases across the top, and a scenario marker.

Tabs
  1 Timeline board    - whole project 1956-1974, half-year ticks
  2 Scenario 1 Zoom   - the variation chain month by month, 1961-1962 (dates link to tab 1)
  3 Task Assignment   - who does what, due week, status dropdown

Bars = conditional formatting keyed to Start/End. Milestones = a formula that prints a
symbol in the half-year containing the date. Dates follow the group's Document Register
(Week 10/DOCUMENT REGISTER_PP1.pdf). Where the Register gives only a year, the month is an
assumption and the Status column says [A].

Run:  py build_scenario1_timeline.py [output.xlsx]   (default: soh_scenario1_timeline.xlsx next to this file)
"""
import datetime as dt
import os
import sys

import openpyxl
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "soh_scenario1_timeline.xlsx")
D = dt.date
ARIAL = "Arial"
MS, GATE = "◆", "■"
DATE_FMT = "d mmm yyyy"


def fnt(size=10, bold=False, italic=False, color="000000"):
    return Font(name=ARIAL, size=size, bold=bold, italic=italic, color=color)


def fill(hex_):
    return PatternFill(start_color=hex_, end_color=hex_, fill_type="solid")


INK, NAVY, MUTED = "18202B", "1F4E78", "595959"
FACTOR = {"Scope": "C8413B", "Time": "E0A030", "Cost": "1F7A8C",
          "Quality": "5E9E6E", "Responsibility": "7B6AA8", "Baseline": "BFBFBF"}
PHASES = [  # label, start, end (exclusive), tint
    ("P1 Brief to Tender", D(1955, 7, 1), D(1958, 7, 1), "E6ECF3"),
    ("P2", D(1958, 7, 1), D(1959, 7, 1), "F4EBDD"),
    ("P3 Construction to Completion", D(1959, 7, 1), D(1973, 7, 1), "E4EFE6"),
    ("Defects + final certificate", D(1973, 7, 1), D(1976, 1, 1), "EEEEEE"),
]
SCENARIO_DATE = D(1961, 6, 1)
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
RED_EDGE = Side(style="medium", color="C00000")

COLS = [("Lane", 5), ("Event", 58), ("Type", 10), ("Form", 11), ("From / To", 22), ("Start", 12),
        ("End", 12), ("Factor", 14), ("Status", 13), ("Contributor / checker", 20),
        ("Source", 9)]
NC = len(COLS)
C_START, C_END = 6, 7                      # column numbers of Start / End
S_COL, E_COL = get_column_letter(C_START), get_column_letter(C_END)


class Board:
    def __init__(self, ws, ticks, step, year_row, tick_width, phases=True):
        self.ws, self.ticks, self.step = ws, ticks, step
        self.year_row, self.tick_row = year_row, year_row + 1
        self.phase_row = year_row + 2 if phases else None
        self.g0 = NC + 2
        self.g1 = self.g0 + len(ticks) - 1
        self.G0, self.G1 = get_column_letter(self.g0), get_column_letter(self.g1)
        self.row = (self.phase_row or self.tick_row) + 1
        self.first_event_row = self.row
        ws.sheet_view.showGridLines = False
        for i, (_, w) in enumerate(COLS, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.column_dimensions[get_column_letter(self.g0 - 1)].width = 2
        for c in range(self.g0, self.g1 + 1):
            ws.column_dimensions[get_column_letter(c)].width = tick_width
        self._header()

    def phase_of(self, t):
        for label, a, b, tint in PHASES:
            if a <= t < b:
                return label, tint
        return None, "FFFFFF"

    def _header(self):
        ws = self.ws
        dark = fill("404040")
        for i, (h, _) in enumerate(COLS, start=1):
            c = ws.cell(row=self.tick_row, column=i, value=h)
            c.font, c.fill, c.border = fnt(bold=True, color="FFFFFF"), dark, BORDER
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            ws.cell(row=self.year_row, column=i).fill = dark
        ws.cell(row=self.year_row, column=self.g0 - 1).fill = dark
        ws.cell(row=self.tick_row, column=self.g0 - 1).fill = dark
        # year labels
        start = 0
        for k in range(len(self.ticks) + 1):
            if k == len(self.ticks) or self.ticks[k].year != self.ticks[start].year:
                a, b = self.g0 + start, self.g0 + k - 1
                if b > a:
                    ws.merge_cells(start_row=self.year_row, start_column=a, end_row=self.year_row, end_column=b)
                y = ws.cell(row=self.year_row, column=a, value=str(self.ticks[start].year))
                y.font, y.alignment = fnt(9, True, color="FFFFFF"), Alignment(horizontal="center")
                for col in range(a, b + 1):
                    ws.cell(row=self.year_row, column=col).fill = dark
                start = k
        for k, t in enumerate(self.ticks):
            c = ws.cell(row=self.tick_row, column=self.g0 + k, value=t)
            c.number_format, c.fill = "mmm", dark
            c.font, c.alignment = fnt(7, True, color="FFFFFF"), Alignment(horizontal="center")
        # phase row
        if self.phase_row:
            ws.cell(row=self.phase_row, column=2,
                    value="PHASES: P1 client brief to tender · P2 tender to start of construction · P3 construction to completion"
                    ).font = fnt(9, True, color=MUTED)
            k = 0
            while k < len(self.ticks):
                label, tint = self.phase_of(self.ticks[k])
                j = k
                while j + 1 < len(self.ticks) and self.phase_of(self.ticks[j + 1])[0] == label:
                    j += 1
                a, b = self.g0 + k, self.g0 + j
                if b > a:
                    ws.merge_cells(start_row=self.phase_row, start_column=a, end_row=self.phase_row, end_column=b)
                c = ws.cell(row=self.phase_row, column=a, value=label)
                c.font, c.alignment = fnt(9, True, color=INK), Alignment(horizontal="left", vertical="center")
                for col in range(a, b + 1):
                    ws.cell(row=self.phase_row, column=col).fill = fill(tint)
                    ws.cell(row=self.phase_row, column=col).border = Border(top=thin, bottom=thin)
                k = j + 1
            ws.row_dimensions[self.phase_row].height = 18
        ws.freeze_panes = ws.cell(row=self.row, column=self.g0)

    def _tint_grid(self, r):
        """Light phase tint under the bars (conditional formatting paints on top)."""
        for k, t in enumerate(self.ticks):
            tint = self.phase_of(t)[1] if self.phase_row else "FFFFFF"
            self.ws.cell(row=r, column=self.g0 + k).fill = fill(tint)

    def group(self, text, sub):
        ws, r = self.ws, self.row
        ws.cell(row=r, column=1, value=text).font = fnt(11, True, color="FFFFFF")
        ws.cell(row=r, column=3, value=sub).font = fnt(9, italic=True, color="C9D3DF")
        for col in range(1, self.g1 + 1):
            ws.cell(row=r, column=col).fill = fill(INK)
        ws.row_dimensions[r].height = 20
        self.row += 1

    def lane(self, code, name, sub, owner):
        ws, r = self.ws, self.row
        ws.cell(row=r, column=1, value=code).font = fnt(10, True, color=MUTED)
        ws.cell(row=r, column=2, value=f"{name}  —  {sub}").font = fnt(10, True)
        o = ws.cell(row=r, column=10, value=owner)
        o.font = fnt(9, True, color=NAVY)
        for col in range(1, self.g1 + 1):
            ws.cell(row=r, column=col).fill = fill("E7EBEF")
        self.row += 1

    def _meta(self, code, name, kind, form, frm_to, factor, status, who, src=""):
        ws, r = self.ws, self.row
        vals = [code, name, kind, form, frm_to, None, None, factor, status, who, src]
        for i, v in enumerate(vals, start=1):
            if v is None:
                continue
            c = ws.cell(row=r, column=i, value=v)
            c.font = fnt(10, bold=(i == 4 and bool(form)), color=MUTED if i == 1 else "000000")
        for col in range(1, NC + 1):
            c = ws.cell(row=r, column=col)
            c.border = BORDER
            c.alignment = Alignment(vertical="center", horizontal="left" if col in (2, 5, 10) else "center")
        f = ws.cell(row=r, column=8)
        f.fill = fill(FACTOR[factor])
        f.font = fnt(9, True, color="FFFFFF")
        if "[A]" in status or "NEW" in status:
            ws.cell(row=r, column=9).fill = fill("FFF2CC")
        self._tint_grid(r)

    def _date(self, col, value, linked):
        c = self.ws.cell(row=self.row, column=col, value=value)
        c.number_format = DATE_FMT
        c.font = fnt(color="008000") if linked else (fnt() if isinstance(value, str) else fnt(color="0000FF"))

    def bar(self, code, name, start, end, factor, status, form="", frm_to="", who="", kind="Bar", linked=False,
            src=""):
        r = self.row
        self._meta(code, name, kind, form, frm_to, factor, status, who, src)
        self._date(C_START, start, linked)
        self._date(C_END, end, linked)
        rule = (f"AND({self.G0}${self.tick_row}<${E_COL}{r},"
                f"EDATE({self.G0}${self.tick_row},{self.step})>${S_COL}{r})")
        self.ws.conditional_formatting.add(f"{self.G0}{r}:{self.G1}{r}",
                                           FormulaRule(formula=[rule], fill=fill(FACTOR[factor]), stopIfTrue=True))
        self.row += 1
        return r

    def milestone(self, code, name, when, factor, status, form="", frm_to="", who="", gate=False, linked=False,
                  src=""):
        r = self.row
        sym = GATE if gate else MS
        self._meta(code, name, "Gate" if gate else ("Form" if form else "Milestone"), form, frm_to, factor, status,
                   who, src)
        self._date(C_START, when, linked)
        for k in range(len(self.ticks)):
            L = get_column_letter(self.g0 + k)
            c = self.ws.cell(row=r, column=self.g0 + k,
                             value=f'=IF(AND(${S_COL}{r}>={L}${self.tick_row},'
                                   f'${S_COL}{r}<EDATE({L}${self.tick_row},{self.step})),"{sym}","")')
            c.font, c.alignment = fnt(10, True, color="FFFFFF"), Alignment(horizontal="center")
        self.ws.conditional_formatting.add(f"{self.G0}{r}:{self.G1}{r}",
                                           FormulaRule(formula=[f'{self.G0}{r}<>""'], fill=fill(FACTOR[factor]),
                                                       stopIfTrue=True))
        self.row += 1
        return r

    def scenario_marker(self, when, label):
        """Red edge after the grid column that contains the scenario date, plus a label above the years."""
        for k, t in enumerate(self.ticks):
            nxt = self.ticks[k + 1] if k + 1 < len(self.ticks) else D(9999, 1, 1)
            if t <= when < nxt:
                col = self.g0 + k
                for r in range(self.tick_row + 1, self.row):
                    c = self.ws.cell(row=r, column=col)
                    c.border = Border(right=RED_EDGE, top=c.border.top, bottom=c.border.bottom)
                m = self.ws.cell(row=self.year_row - 1, column=col, value=f"▼ {label}")
                m.font = fnt(9, True, color="C00000")
                return


def notes(ws, row, title, lines, span):
    row += 1
    ws.cell(row=row, column=2, value=title).font = fnt(bold=True)
    row += 1
    for n in lines:
        c = ws.cell(row=row, column=2, value="• " + n)
        c.font, c.alignment = fnt(9, italic=True, color=MUTED), Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=span)
        ws.row_dimensions[row].height = 26
        row += 1
    return row


def page_setup(ws):
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True


wb = openpyxl.Workbook()

# ===================================================================== TAB 1
ws = wb.active
ws.title = "Timeline board"
MAIN = "'Timeline board'"
ws["A1"] = "SYDNEY OPERA HOUSE — TIMELINE OF SIGNIFICANT PROJECT EVENTS"
ws["A1"].font = fnt(14, True)
ws["A2"] = ("PP1 Assessment 3 · A1 Timeline · Scenario 1: additional piers to support the roof · dates from the "
            "group's Document Register and sources A–J (Source column) · Status [A] (yellow) = assumed / not yet sourced")
ws["A2"].font = fnt(9, italic=True, color=MUTED)
ws["A3"] = ("Group: Kankawee Maksomboon / Prani Patton / Yu-Chun Ho     Lead 1: Kankawee Maksomboon     Lead 2: Yu-Chun Ho     Lead 3: Prani Patton     "
            "(Leads 2–3 inferred from the Register — confirm)")
ws["A3"].font = fnt(10, True, color=NAVY)

# numbers box, rows 5-11
ws["B5"] = "Scenario 1 numbers — change these, everything else follows"
ws["B5"].font = fnt(11, True, color="FFFFFF")
for c in range(1, NC + 1):
    ws.cell(row=5, column=c).fill = fill(NAVY)
box = [
    ("Site possession (Stage I start) — ABIC F1", D(1959, 3, 2), True, DATE_FMT, "Sources A, D: construction began 2 Mar 1959"),
    ("Original date for practical completion — Sched 1 item 22", D(1963, 1, 26), True, DATE_FMT, "Tutor's project information"),
    ("Adjustment of time granted by SW-14 (months)", 1, True, "0", "Tutor's worked example for Scenario 1"),
    ("Date for PC after SW-14 (this variation only)", "=EDATE(F7,F8)", False, DATE_FMT, "Formula: original PC + SW-14 months"),
    ("Contract sum at signing ($)", 9600000, True, "$#,##0", "Tutor's 'ballpark' original budget; the group may pick another"),
    ("Contract price adjustment by SW-11 ($)", 5000, True, "$#,##0", "Tutor's worked example for Scenario 1"),
    ("Contract sum after SW-11 ($) — the figure SW-31 must refer back to", "=F10+F11", False, "$#,##0",
     "Formula. Only this variation is modelled"),
]
for i, (label, val, is_in, fmt, note) in enumerate(box):
    r = 6 + i
    ws.cell(row=r, column=2, value=label).font = fnt(bold=(i == len(box) - 1))
    v = ws.cell(row=r, column=6, value=val)
    v.font, v.number_format = (fnt(color="0000FF") if is_in else fnt()), fmt
    if is_in:
        v.fill = fill("FFFF00")
    ws.cell(row=r, column=7, value=note).font = fnt(9, italic=True, color=MUTED)
POSS, PC, EOT = "$F$6", "$F$7", "$F$8"

b = Board(ws, [D(y, m, 1) for y in range(1955, 1976) for m in (1, 7)], 6, year_row=15, tick_width=3.4)

# legend above the grid (rows 5-11, grid columns)
L0 = b.g0
ws.cell(row=5, column=L0, value="COLOUR BY FACTOR").font = fnt(9, True, color=MUTED)
for i, (k, col) in enumerate([(k, v) for k, v in FACTOR.items() if k != "Baseline"]):
    r = 6 + i
    ws.cell(row=r, column=L0).fill = fill(col)
    ws.cell(row=r, column=L0 + 1, value=k).font = fnt(9)
ws.cell(row=5, column=L0 + 8, value="SYMBOLS").font = fnt(9, True, color=MUTED)
for i, (sym, txt, col) in enumerate([
        ("", "bar = date range", "9DC3E6"), (MS, "milestone / document = one date", None),
        (GATE, "CAA client-approval gate", None), ("", "planned baseline", FACTOR["Baseline"]),
        ("▼", "red column edge = our scenario (Jun 1961)", None),
        ("", "Status yellow = [A] assumption / NEW row", "FFF2CC")]):
    r = 6 + i
    c = ws.cell(row=r, column=L0 + 8, value=sym)
    c.alignment = Alignment(horizontal="center")
    c.font = fnt(10, True, color="C00000" if sym == "▼" else INK)
    if col:
        c.fill = fill(col)
    ws.cell(row=r, column=L0 + 9, value=txt).font = fnt(9)
ws.cell(row=5, column=L0 + 20, value="REQUIRED FORMS").font = fnt(9, True, color=MUTED)
ws.cell(row=6, column=L0 + 20, value="Intro letter · CAA 2024 · ABIC SW 2018 · SW-12 · SW-14 · SW-11 · SW-31").font = fnt(9)
ws.cell(row=7, column=L0 + 20, value="Optional: SW-42 claim · SW-13 instruction to proceed").font = fnt(9, italic=True, color=MUTED)

R = {}
F1, J2, P3 = "Kankawee Maksomboon / Prani Patton", "Yu-Chun Ho / Kankawee Maksomboon", "Prani Patton / Yu-Chun Ho"
# Source keys A-J = the group's source sheet, verified in ../15-sources-A-J-verified.md.
# REG = the group's Document Register; tutor = the tutor's instruction video.
# ---------------- DESIGN TIMELINE
b.group("DESIGN TIMELINE", "architect's services · CAA 2024")
b.lane("D0", "CAA services stage", "Sched A: A.1 Concept › A.2 DD › A.4 CD › A.6 + client approval gates",
       "Lead 1: Kankawee Maksomboon (check: Prani Patton)")
b.bar("D0", "A.1 Concept design (ends with the Red Book)", D(1957, 3, 1), D(1958, 3, 1), "Scope", "[A] start",
      form="CAA A.1", who=F1, src="B")
b.milestone("D0", "Gate: concept approved by client in writing", D(1958, 3, 1), "Scope", "[A]", gate=True, who=F1,
            src="B")
b.bar("D0", "A.2 Design development — roof unresolved until the Yellow Book", D(1958, 3, 1), D(1962, 1, 1), "Scope",
      "[F]", form="CAA A.2", who=F1, src="B")
b.bar("D0", "A.4 Construction documentation — Stage I", D(1958, 5, 1), D(1958, 12, 1), "Scope", "[A] start",
      form="CAA A.4", who=F1, src="C")
b.milestone("D0", "★ Gate SKIPPED: works start before DD approved", D(1959, 2, 1), "Scope", "[A]", gate=True, who=F1,
            src="A, B")
b.bar("D0", "A.6 Contract administration (construction + post-construction)", f"={POSS}", D(1975, 5, 31), "Time",
      "[F]", form="CAA A.6", who=F1, src="A, D")

b.lane("D1", "Client + brief", "decisions, approvals, representatives (C.3)", "Lead 1: Kankawee Maksomboon (check: Prani Patton)")
b.milestone("D1", "Competition announced by Premier Cahill (two halls)", D(1955, 9, 13), "Scope", "[F]",
            frm_to="NSW Govt to public", src="D")
b.milestone("D1", "★ Introductory letter", D(1957, 2, 11), "Scope", "REG [A]", form="GL1", frm_to="Architect to Client",
            who=F1, src="REG")
b.milestone("D1", "★ CAA 2024 signed", D(1957, 2, 21), "Scope", "REG",
            form="CAA", frm_to="Architect to Client", who=F1, src="REG")
b.milestone("D1", "Premier Cahill dies; Heffron Premier — client rep changes (CAA C.3)", D(1959, 10, 22), "Responsibility",
            "NEW [F] D: 19 Oct", frm_to="Client to Architect", who="Kankawee Maksomboon", src="U, W, D")
R["d8"] = b.milestone("D1", "★ Architect notifies client: extra services + fee (CAA D.8)", D(1961, 7, 1), "Scope",
                      "NEW [A]", form="CAA D.8", frm_to="Architect to Client", who="Kankawee Maksomboon", src="—")
b.milestone("D1", "Askin government: Minister Hughes takes over payments", D(1965, 5, 13), "Responsibility", "[F]",
            frm_to="Client", src="D, G, AD")
b.milestone("D1", "Sydney Opera House Act 1960: Minister for Public Works = constructing authority", D(1960, 1, 1),
            "Responsibility", "[F] year", frm_to="Client", src="D, Z")
b.milestone("D1", "Trust Act 1961: Sydney Opera House Trust set up", D(1961, 3, 14), "Responsibility", "[F]",
            frm_to="Client", src="V")
b.milestone("D1", "Utzon resigns", D(1966, 2, 28), "Responsibility", "[F]", frm_to="Architect to Client", src="D, G")
b.milestone("D1", "Hall / Todd / Littlemore appointed (with Farmer)", D(1966, 4, 19), "Responsibility", "[F]",
            frm_to="Client to Architects", src="D, G")
b.milestone("D1", "Govt pays $160,000 for 130 of Utzon's Stage III drawings", D(1966, 5, 17), "Cost", "[F]",
            frm_to="Client to Utzon's office", src="D")
b.milestone("D1", "Review of Program — change to the use of the halls", D(1966, 12, 12), "Scope", "[F]",
            frm_to="Architects to Client", src="D")

b.milestone("D1", "Opening Committee headed by Premier Askin", D(1972, 2, 28), "Responsibility", "[F]",
            frm_to="Client", src="D")
b.milestone("D1", "Hughes resigns; Leon Punch Minister for Public Works (CAA C.3)", D(1973, 1, 17), "Responsibility",
            "[F]", frm_to="Client to Architects", src="AD")
b.milestone("D1", "Premier Askin formally invites Utzon to the opening", D(1973, 6, 20), "Responsibility", "[F]",
            frm_to="Client to Utzon", src="AE")
b.milestone("D1", "Building handed to the Trust + Minister for Cultural Activities (Freudenstein)", D(1973, 7, 1),
            "Responsibility", "[F] year", frm_to="Client to operator", src="D")
b.milestone("D1", "Utzon declines the invitation", D(1973, 8, 1), "Responsibility", "[F]", frm_to="Utzon to Premier",
            src="AE")
b.milestone("D1", "Askin resigns; Tom Lewis Premier (client at SW-31)", D(1975, 1, 3), "Responsibility", "[F]",
            frm_to="Client", src="W")

b.lane("D2", "Architect — design output", "competition, Red Book, Yellow Book", "Lead 1: Kankawee Maksomboon (check: Prani Patton)")
b.bar("D2", "Competition design phase", D(1955, 9, 13), D(1957, 1, 29), "Scope", "REG [F]",
      frm_to="NSW Govt to entrants", src="D, I")
b.milestone("D2", "Utzon wins first prize (£5,000; 233 entries)", D(1957, 1, 29), "Scope", "[F]", src="D, I")
b.milestone("D2", "Red Book sent to the NSW Government", D(1958, 3, 1), "Scope", "[F]", frm_to="Architect to Client",
            src="B")
R["roof"] = b.bar("D2", "Roof / shell design — unresolved, overlaps Stage I", D(1958, 3, 1), D(1962, 1, 1), "Scope",
                  "[F]", frm_to="Architect + Arup", src="A, B")
R["yellow"] = b.milestone("D2", "Yellow Book — spherical shell geometry fixed", D(1962, 1, 1), "Quality", "[F]",
                          frm_to="Architect to Client", src="B")

b.lane("D3", "Consultants", "Ove Arup & Partners · CAA E.1", "Lead 1: Kankawee Maksomboon (check: Prani Patton)")
b.milestone("D3", "Ove Arup & Partners engaged (by client per brief; by Utzon per D)", D(1957, 6, 1),
            "Responsibility", "[A] date / conflict", frm_to="to Arup", src="D / brief")
b.milestone("D3", "Steensen & Varming appointed mechanical engineers", D(1957, 6, 1), "Responsibility", "[F] year",
            frm_to="to Steensen & Varming", src="AA")
b.bar("D3", "Utzon develops plywood mullions + ceilings with Ralph Symonds Ltd", D(1961, 10, 1), D(1966, 2, 28),
      "Quality", "[F]", frm_to="Architect and supplier", src="Y, X")
b.milestone("D3", "Ralph Symonds Ltd in receivership", D(1964, 2, 26), "Responsibility", "[verify]",
            frm_to="Supplier", src="X")
R["prob"] = b.milestone("D3", "★ Problem found: final roof loads exceed podium columns", D(1961, 6, 1), "Scope",
                        "[A] verify", frm_to="Arup to Architect", src="tutor")

b.lane("D4", "Interior design (after 1967)", "Hall, Todd & Littlemore + acoustician Jordan — see 17-interiors",
       "Context — all three")
b.milestone("D4", "Cabinet approves new brief: concert hall 2,800 / opera 1,500", D(1967, 3, 1),
            "Scope", "[F]", frm_to="Client to Architects", src="R, M")
b.milestone("D4", "Arup objects in writing; Major Hall stage machinery scrapped", D(1967, 3, 28), "Scope", "[F]",
            frm_to="Arup to Minister", src="S")
b.bar("D4", "White Book — first interior designs (halls, glass walls)", D(1967, 1, 1), D(1969, 12, 31), "Scope",
      "[F]", frm_to="Architects", src="H")
b.milestone("D4", "Glass walls redesigned on a steel-mullion frame (was plywood)", D(1968, 1, 1), "Quality",
            "[F] year", frm_to="Architects", src="L")
b.milestone("D4", "Glass-wall prototype specification", D(1969, 1, 1), "Quality", "[F]", frm_to="Architects",
            src="C")
b.milestone("D4", "Grand Organ report + specification (Ronald Sharp)", D(1969, 6, 1), "Scope", "[F] year",
            frm_to="Organ builder to Client", src="P")
b.milestone("D4", "Acoustic reflector shape fixed (Jordan + Hall)", D(1971, 12, 1), "Quality", "[F]",
            frm_to="Acoustician + Architect", src="M")
b.milestone("D4", "Coburn tapestry curtains hung (Opera + Drama theatres)", D(1973, 9, 1), "Quality", "[F] year",
            frm_to="Artist to Client", src="N")

# ---------------- CONTRACT TIMELINE
b.group("CONTRACT TIMELINE", "procurement + ABIC Simple Works 2018")
b.lane("C1", "Procurement + cost", "tender, contracts signed, cost plan", "Lead 2: Yu-Chun Ho (check: Kankawee Maksomboon)")
b.milestone("C1", "Opera House Lottery starts — funds the build", D(1957, 11, 25), "Cost", "[F]",
            frm_to="NSW Govt", src="Z")
b.milestone("C1", "Stage I tender documents: conditions of contract + bills of quantities", D(1958, 12, 1), "Cost",
            "REG [F]", frm_to="Architect to Contractor", who="Yu-Chun Ho?", src="C")
b.milestone("C1", "Tender return", D(1959, 1, 1), "Cost", "REG [A]", frm_to="Contractor to Architect", who="Yu-Chun Ho?",
            src="REG")
b.milestone("C1", "Contractor selection (Civil & Civic)", D(1959, 2, 1), "Cost", "REG [A]", src="REG, D")
b.milestone("C1", "★ Simple Works Contract signed", D(1959, 2, 19), "Cost", "REG", form="SW 2018",
            frm_to="Architect to Contractor", who=J2, src="REG")
b.milestone("C1", "Stage machinery contract: Waagner-Biro", D(1961, 4, 1), "Cost", "[F]", frm_to="Client and supplier",
            src="C")
R["cp06"] = b.milestone("C1", "Cost plan issued — £13.7m (= A$27.4m)", D(1962, 3, 1), "Cost", "REG [A] month",
                        form="CP-06", frm_to="QS to Architect", who="Yu-Chun Ho?", src="G")
b.milestone("C1", "Stage II agreement: Minister for Public Works + Hornibrook", D(1962, 10, 18), "Cost", "[F]",
            frm_to="Client and Contractor", src="E, C")
b.milestone("C1", "Stage III agreement: Minister for Public Works + Hornibrook", D(1966, 11, 1), "Cost", "[F]",
            frm_to="Client and Contractor", src="C")
b.milestone("C1", "A$22.9m spent so far", D(1966, 10, 1), "Cost", "[F]", src="AC")
b.milestone("C1", "New estimate: a further $85m, finish end 1972", D(1968, 9, 1), "Cost", "[verify]",
            frm_to="Architects to Minister", src="search")
b.milestone("C1", "Final cost $102m (excl. organ + car park) — Public Works statement", D(1974, 5, 1), "Cost", "[F]",
            src="D")

b.lane("C2", "Construction works", "site › Stage I › II › III › defects", "Lead 2: Yu-Chun Ho (check: Kankawee Maksomboon)")
b.bar("C2", "Tram depot demolished — site cleared", D(1958, 8, 1), D(1959, 3, 1), "Time", "[F] start", src="D")
b.milestone("C2", "Site possession — construction ceremony, Stage I starts", f"={POSS}", "Time", "REG [F]",
            frm_to="Client to Contractor", src="A, D")
b.bar("C2", "Planned programme at signing (baseline)", f"={POSS}", f"={PC}", "Baseline", "[F] tutor", kind="Baseline",
      src="tutor")
R["st1"] = b.bar("C2", "Stage I — podium (Civil & Civic); 2 years late", f"={POSS}", D(1963, 3, 1), "Time",
                 "[F] Feb/Mar", src="A, D")
r_work = b.row
R["work"] = b.bar("C2", "★ Piers work on site — the extra time", D(1961, 10, 1), f"=EDATE({S_COL}{r_work},{EOT})", "Time",
                  "[A]", frm_to="Contractor", kind="Work", src="tutor")
b.milestone("C2", "Stage II contract drawings", D(1962, 10, 18), "Time", "REG [A]", frm_to="Architect to Contractor",
            src="REG, E")
R["st2"] = b.bar("C2", "Stage II — roof shells (Hornibrook) to last segment", D(1963, 4, 1), D(1967, 1, 17), "Time",
                 "[F]", src="D, F")
b.bar("C2", "Stage III — interiors + glass walls (Hornibrook)", D(1967, 1, 17), D(1973, 10, 20), "Time",
      "[F] K: site 1968", src="F, J, K")
b.milestone("C2", "Stage III working drawings dated", D(1968, 7, 1), "Time", "REG [F]", frm_to="Architect to Contractor",
            src="I")
b.bar("C2", "Defects liability period — 12 months (ABIC M13)", D(1973, 10, 20), D(1974, 10, 20), "Quality", "[A]",
      kind="Period", src="—")

b.lane("C3", "Contract administration", "J1 SW-12 › H4 SW-14 / SW-11 › N11 SW-31", "Lead 3: Prani Patton (check: Yu-Chun Ho)")
R["sw12"] = b.milestone("C3", "★ Instruction for a Variation — strengthen columns, add piers", D(1961, 8, 1), "Scope",
                        "REG [A]", form="SW-12", frm_to="Architect to Contractor", who=P3, src="REG, tutor")
R["sw42"] = b.milestone("C3", "Contractor's details of claim — 1 month, $5,000 (optional)", D(1961, 9, 1), "Time",
                        "[A] optional", form="SW-42", frm_to="Contractor to Architect", src="tutor")
R["sw13"] = b.milestone("C3", "Instruction to proceed with the variation (optional)", D(1961, 10, 1), "Scope",
                        "[A] optional", form="SW-13", frm_to="Architect to Contractor", src="tutor")
R["sw14"] = b.milestone("C3", "★ Adjustment of time — +1 month", D(1961, 11, 1), "Time", "REG [A]", form="SW-14",
                        frm_to="Architect to Contractor", who=P3, src="REG, tutor")
R["sw11"] = b.milestone("C3", "★ Contract Price Adjustment — +$5,000", D(1962, 4, 1), "Cost", "REG [A]", form="SW-11",
                        frm_to="Architect to Contractor", who=P3, src="REG, tutor")
b.milestone("C3", "Practical completion — official opening", D(1973, 10, 20), "Time", "REG [F]",
            frm_to="Architect to Contractor", src="J, D")
b.milestone("C3", "★ Final Certificate — refers to SW-11 (Architects' Certificate of Completion)", D(1975, 5, 31),
            "Cost", "[F] REG: 1974", form="SW-31", frm_to="Architect to Contractor", who=P3, src="D")
b.lane("C4", "Interior works + fit-out (after 1967)", "Hornibrook + specialist packages — see 17-interiors",
       "Context — all three")
b.milestone("C4", "Waterproofing specification", D(1967, 3, 1), "Quality", "[F]", src="C")
b.bar("C4", "Stage III interiors + glass walls on site", D(1968, 1, 1), D(1973, 10, 20), "Time", "[F] year", src="K")
b.bar("C4", "Glass walls built (near complete 1971)", D(1968, 7, 1), D(1971, 12, 31), "Time", "[A] months", src="K, L, F")
b.milestone("C4", "Light-fittings agreement: architects + GEC-Philips", D(1969, 8, 1), "Cost", "[F]",
            frm_to="Architects and supplier", src="C")
b.milestone("C4", "Electronic services subcontract: Hornibrook + AWA", D(1970, 3, 1), "Cost", "[F]",
            frm_to="Contractor and subcontractor", src="C")
b.bar("C4", "Acoustic reflectors made (K.F. Plastics) + installed", D(1972, 3, 1), D(1972, 9, 5), "Quality", "[F]",
      src="M")
b.milestone("C4", "Opera Theatre stage machinery drawings (Waagner-Biro vol. 2)", D(1972, 12, 1), "Scope", "[F]",
            src="T")
b.milestone("C4", "First test concert in the Concert Hall (for the builders)", D(1972, 12, 17), "Quality", "[F]",
            src="D, M")
b.milestone("C4", "First opera: War and Peace (Opera Theatre) — use before opening", D(1973, 9, 28), "Time", "[F]",
            src="Q")
b.bar("C4", "Opening festival (two weeks)", D(1973, 10, 17), D(1973, 11, 3), "Time", "[F]", src="J")
b.milestone("C4", "First public Concert Hall concert", D(1973, 9, 29), "Time", "[F]", src="D, Q")
b.bar("C4", "Grand Organ — separate contract, to 30 May 1979 ($0.4m to $1.2m)", D(1969, 6, 1), D(1979, 5, 30), "Cost",
      "[F]", src="O, D")
b.scenario_marker(SCENARIO_DATE, "OUR SCENARIO 1: additional piers (Jun 1961)")

notes(ws, b.row, "Reading the board", [
    "Design timeline D0–D3 is Lead 1's (Kankawee Maksomboon); Contract timeline C1–C2 is Lead 2's (Yu-Chun Ho); C3 is Lead 3's (Prani Patton). "
    "The Task Assignment tab lists each person's jobs.",
    "Colour = the factor that changed. ★ = required form or scenario event. The red column edge marks our scenario (Jun 1961).",
    "The design bars (D0 A.2, D2 roof) run over Stage I construction until 1961 — building started before the design was "
    "finished. That overlap is the cause of Scenario 1. Compare the master reference gantt_programme_options.xlsx (Option 1).",
    "Blue dates are inputs: agree the [A] months as a group and type them in; the symbols move. Dates on the Zoom tab follow automatically.",
    "The CAA row must be the 2024 edition (the Register says 2019). SW-42 and SW-13 are optional — delete the rows if not used.",
    "Source column: keys A–J are the group's source sheet, each verified in 15-sources-A-J-verified.md; "
    "REG = Document Register; tutor = instruction video. Conflicts (Stage I Feb/Mar 1963, who engaged Arup, "
    "SW-31 1974 vs 31 May 1975) are listed there. 16-event-summaries.md explains every event in plain words.",
    "The group's Miro board is checked note by note in 18-miro-board-verified.md (sources U–AF), including the 1973–75 run-out to the 31 May 1975 certificate.",
    "Lanes D4 and C4 (after 1967) are context for the final certificate and Part B, not Scenario 1 — sources K–T and a summary of each interior event are in 17-interiors-1967-1975.md.",
], span=NC + 30)
page_setup(ws)

# ===================================================================== TAB 2
z = wb.create_sheet("Scenario 1 Zoom")
z["A1"] = "SCENARIO 1 ZOOM — the variation chain month by month (1961–1962)"
z["A1"].font = fnt(14, True)
z["A2"] = ("Dates are formulas pulling from 'Timeline board' (green). Change dates there, not here. "
           "The Final Certificate (31 May 1975) is outside this window.")
z["A2"].font = fnt(9, italic=True, color=MUTED)
zb = Board(z, [D(y, m, 1) for y in (1961, 1962) for m in range(1, 13)], 1, year_row=4, tick_width=5.5, phases=False)


def link(col, key):
    return f"={MAIN}!{col}{R[key]}"


zb.group("CONTEXT", "why the variation happens")
zb.bar("D2", "Roof / shell design — unresolved, overlaps Stage I", link(S_COL, "roof"), link(E_COL, "roof"), "Scope",
       "[F]", linked=True, src="A, B")
zb.bar("C2", "Stage I — podium (Civil & Civic)", link(S_COL, "st1"), link(E_COL, "st1"), "Time", "[F]", linked=True,
       src="A, D")
zb.milestone("D2", "Yellow Book — spherical shell geometry fixed", link(S_COL, "yellow"), "Quality", "[F]",
             frm_to="Architect to Client", linked=True, src="B")
zb.bar("C2", "Stage II — roof shells (Hornibrook)", link(S_COL, "st2"), link(E_COL, "st2"), "Time", "[F]",
       linked=True, src="D, F")
zb.group("★ SCENARIO 1 CHAIN", "tutor's worked example: 1 month, $5,000")
zb.milestone("D3", "Problem found: final roof loads exceed podium columns", link(S_COL, "prob"), "Scope", "[A] verify",
             frm_to="Arup to Architect", linked=True, src="tutor")
zb.milestone("D1", "Architect notifies client: extra services + fee", link(S_COL, "d8"), "Scope", "NEW [A]",
             form="CAA D.8", frm_to="Architect to Client", who="Kankawee Maksomboon", linked=True, src="—")
zb.milestone("C3", "Instruction for a Variation — strengthen columns, add piers", link(S_COL, "sw12"), "Scope", "REG [A]",
             form="SW-12", frm_to="Architect to Contractor", who=P3, linked=True, src="REG, tutor")
zb.milestone("C3", "Contractor's details of claim — 1 month, $5,000 (optional)", link(S_COL, "sw42"), "Time",
             "[A] optional", form="SW-42", frm_to="Contractor to Architect", linked=True, src="tutor")
zb.milestone("C3", "Instruction to proceed with the variation (optional)", link(S_COL, "sw13"), "Scope", "[A] optional",
             form="SW-13", frm_to="Architect to Contractor", linked=True, src="tutor")
zb.bar("C2", "Piers work on site — the extra time", link(S_COL, "work"), link(E_COL, "work"), "Time", "[A]",
       frm_to="Contractor", kind="Work", linked=True, src="tutor")
zb.milestone("C3", "Adjustment of time — +1 month", link(S_COL, "sw14"), "Time", "REG [A]", form="SW-14",
             frm_to="Architect to Contractor", who=P3, linked=True, src="REG, tutor")
zb.milestone("C1", "Cost plan issued", link(S_COL, "cp06"), "Cost", "REG [A]", form="CP-06", frm_to="QS to Architect",
             who="Yu-Chun Ho?", linked=True, src="G")
zb.milestone("C3", "Contract Price Adjustment — +$5,000", link(S_COL, "sw11"), "Cost", "REG [A]", form="SW-11",
             frm_to="Architect to Contractor", who=P3, linked=True, src="REG, tutor")
notes(z, zb.row, "Reading the chain", [
    "Order follows the tutor's worked example: variation to contractor's claim to instruction to proceed to adjustment of "
    "time to price adjustment to (1974) final certificate referring to the price adjustment.",
    "The CAA D.8 row is the client-side twin of SW-12: the architect's own extra design work and fee, agreed in writing.",
], span=NC + 20)
page_setup(z)

# ===================================================================== TAB 3
t = wb.create_sheet("Task Assignment")
t.sheet_view.showGridLines = False
t["A1"] = "TASK ASSIGNMENT — from the Register and the timeline board"
t["A1"].font = fnt(14, True)
t["A2"] = "Status is a dropdown (To do / Doing / Done). Leads 2–3 are inferred from the Register's contributor / checker pattern — confirm."
t["A2"].font = fnt(9, italic=True, color=MUTED)
heads = [("Lead", 12), ("Name", 10), ("Lanes owned", 30), ("Checker", 10), ("Task", 70), ("Due", 22), ("Status", 10)]
for i, (h, w) in enumerate(heads, start=1):
    c = t.cell(row=4, column=i, value=h)
    c.font, c.fill, c.border = fnt(bold=True, color="FFFFFF"), fill("404040"), BORDER
    t.column_dimensions[get_column_letter(i)].width = w
tasks = [
    ("Lead 1", "Kankawee Maksomboon", "D0–D3 design", "Prani Patton", "Introductory letter drafted, dated 11 Feb 1957 [A]: confirm the fee (6%) and the $10,000 Mobilisation Fee", "Week 10"),
    ("Lead 1", "Kankawee Maksomboon", "D0–D3 design", "Prani Patton", "Build the CAA on the 2024 template (the Register says CAA 2019)", "Week 10"),
    ("Lead 1", "Kankawee Maksomboon", "D0–D3 design", "Prani Patton", "Add Register row: client representative change Cahill to Askin (CAA C.3)", "Week 10"),
    ("Lead 1", "Kankawee Maksomboon", "D0–D3 design", "Prani Patton", "Add Register row: CAA D.8 extra-services notice, Jul 1961", "Week 10"),
    ("Lead 2", "Yu-Chun Ho", "C1–C2 procurement + construction", "Kankawee Maksomboon", "Tender dates and contractor selection (Register gives years only)", "Week 10–11"),
    ("Lead 2", "Yu-Chun Ho", "C1–C2 procurement + construction", "Kankawee Maksomboon", "ABIC SW Schedule 1: contract sum, site possession, date for PC", "Week 11"),
    ("Lead 2", "Yu-Chun Ho", "C1–C2 procurement + construction", "Kankawee Maksomboon", "Cost plan CP-06: name the quantity surveyor or declare [A]", "Week 11"),
    ("Lead 3", "Prani Patton", "C3 contract administration", "Yu-Chun Ho", "SW-12 to SW-14 (+1 month) to SW-11 (+$5,000) to SW-31", "Week 11"),
    ("Lead 3", "Prani Patton", "C3 contract administration", "Yu-Chun Ho", "Optional: SW-42 contractor's claim + SW-13 instruction to proceed", "Week 11"),
    ("All", "All three", "—", "—", "Confirm lead roles and Scenario 1", "Next meeting"),
    ("All", "All three", "—", "—", "Agree the [A] months (yellow Status cells on the board)", "Before Week 12"),
    ("All", "All three", "—", "—", "Premier to name in 1961: tutor's Askin or historical Heffron?", "Before Week 12"),
    ("All", "All three", "—", "—", "Architect on SW-31 (1974): Utzon, or Hall / Todd / Littlemore?", "Before Week 12"),
    ("All", "All three", "—", "—", "In-progress presentation, ~8 min, face to face", "Monday Week 12"),
]
dv = DataValidation(type="list", formula1='"To do,Doing,Done"', allow_blank=False)
t.add_data_validation(dv)
for i, row in enumerate(tasks):
    r = 5 + i
    for j, v in enumerate(list(row) + ["To do"], start=1):
        c = t.cell(row=r, column=j, value=v)
        c.font, c.border = fnt(bold=(j == 2)), BORDER
        c.alignment = Alignment(vertical="center", wrap_text=(j == 5))
    dv.add(f"G{r}")
last = 4 + len(tasks)
t.conditional_formatting.add(f"G5:G{last}", FormulaRule(formula=['G5="Done"'], fill=fill("C6EFCE")))
t.conditional_formatting.add(f"G5:G{last}", FormulaRule(formula=['G5="Doing"'], fill=fill("FFEB9C")))
for i, (lead, col) in enumerate([("Lead 1", "DDEBF7"), ("Lead 2", "E2EFDA"), ("Lead 3", "FCE4D6"), ("All", "EDEDED")]):
    t.conditional_formatting.add(f"A5:A{last}", FormulaRule(formula=[f'$A5="{lead}"'], fill=fill(col)))
t.freeze_panes = "A5"
page_setup(t)

wb.active = 0
wb.save(OUT)
print("wrote", OUT)
