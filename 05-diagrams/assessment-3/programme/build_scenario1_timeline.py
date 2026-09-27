"""Scenario 1 project timeline (Sydney Opera House, additional piers) as an
editable Excel Gantt, styled after the master reference gantt_programme_options.xlsx.

Tab 1 "Scenario 1 Timeline" - whole project 1956-1974, half-year ticks.
Tab 2 "Scenario 1 Zoom"     - the variation chain month by month, 1961-1962.
                              Its dates are formulas pointing at tab 1 (enter dates once).

- Bars (date ranges)        = conditional formatting keyed to Start/End.
- Milestones (single dates) = a diamond formula in the grid cell whose period contains the date.
- "Scenario 1 numbers" box  = inputs (EOT months, price adjustment, contract sum, original PC);
                              the contractual consequences are formulas.

Dates come from the group's Document Register (Week 10/DOCUMENT REGISTER_PP1.pdf) and
13-timeline-draft-v1.md. A month inside a year the Register only gives as a year is an
assumption, marked [A] in the Status column.

Run:  py build_scenario1_timeline.py   (writes soh_scenario1_timeline.xlsx next to this file)
"""
import datetime as dt
import os

import openpyxl
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "soh_scenario1_timeline.xlsx")
D = dt.date
ARIAL = "Arial"
DIAMOND = "◆"


def fnt(size=10, bold=False, italic=False, color="000000"):
    return Font(name=ARIAL, size=size, bold=bold, italic=italic, color=color)


def fill(hex_):
    return PatternFill(start_color=hex_, end_color=hex_, fill_type="solid")


F_TITLE, F_NOTE = fnt(13, True), fnt(9, italic=True, color="595959")
F_BODY, F_BOLD = fnt(), fnt(bold=True)
F_INPUT, F_CALC = fnt(color="0000FF"), fnt()
F_LINK = fnt(color="008000")                       # green = pulled from the other tab
F_WHITE, F_WHITE_BIG = fnt(bold=True, color="FFFFFF"), fnt(12, True, color="FFFFFF")
DARK, BAND, SECTION = fill("404040"), fill("1F4E78"), fill("D9D9D9")
YELLOW, A_FILL = fill("FFFF00"), fill("FFF2CC")
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

C = {
    "design": "9DC3E6", "design_ms": "2E75B6",
    "contract": "A9D08E", "contract_ms": "548235",
    "scenario": "C00000", "scenario_bar": "F4B084",
    "baseline": "BFBFBF",
}
COLS = ["Event", "Type", "Form No.", "From → To", "Start", "End", "Status"]
WIDTHS = [60, 10, 10, 22, 13, 13, 15]
DATE_FMT = "d mmm yyyy"


class Gantt:
    """One sheet: left-hand event table + a time grid with bars and diamonds."""

    def __init__(self, ws, ticks, step_months, year_row, first_row, tick_fmt, tick_width):
        self.ws, self.ticks, self.step = ws, ticks, step_months
        self.year_row, self.tick_row = year_row, year_row + 1
        self.g0 = len(COLS) + 2
        self.g1 = self.g0 + len(ticks) - 1
        self.G0, self.G1 = get_column_letter(self.g0), get_column_letter(self.g1)
        self.row = first_row
        ws.sheet_view.showGridLines = False
        for i, w in enumerate(WIDTHS, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.column_dimensions[get_column_letter(self.g0 - 1)].width = 2
        for c in range(self.g0, self.g1 + 1):
            ws.column_dimensions[get_column_letter(c)].width = tick_width
        self._header(tick_fmt)

    def _header(self, tick_fmt):
        ws = self.ws
        for i, h in enumerate(COLS, start=1):
            c = ws.cell(row=self.tick_row, column=i, value=h)
            c.font, c.fill, c.border = F_WHITE, DARK, BORDER
            c.alignment = Alignment(horizontal="center", vertical="center")
            ws.cell(row=self.year_row, column=i).fill = DARK
        for col in (self.g0 - 1,):
            ws.cell(row=self.tick_row, column=col).fill = DARK
            ws.cell(row=self.year_row, column=col).fill = DARK
        # year labels: merge every run of ticks sharing a year
        start = 0
        for k in range(len(self.ticks) + 1):
            if k == len(self.ticks) or self.ticks[k].year != self.ticks[start].year:
                a, b = self.g0 + start, self.g0 + k - 1
                if b > a:
                    ws.merge_cells(start_row=self.year_row, start_column=a, end_row=self.year_row, end_column=b)
                y = ws.cell(row=self.year_row, column=a, value=str(self.ticks[start].year))
                y.font, y.fill = fnt(9, True, color="FFFFFF"), DARK
                y.alignment = Alignment(horizontal="center")
                for col in range(a, b + 1):
                    ws.cell(row=self.year_row, column=col).fill = DARK
                start = k
        for k, t in enumerate(self.ticks):
            c = ws.cell(row=self.tick_row, column=self.g0 + k, value=t)
            c.number_format, c.fill = tick_fmt, DARK
            c.font = fnt(7, True, color="FFFFFF")
            c.alignment = Alignment(horizontal="center")
        ws.freeze_panes = ws.cell(row=self.tick_row + 1, column=self.g0)

    # ---- rows
    def band(self, text):
        c = self.ws.cell(row=self.row, column=1, value=text)
        c.font = F_WHITE_BIG
        for col in range(1, self.g1 + 1):
            self.ws.cell(row=self.row, column=col).fill = BAND
        self.row += 1

    def section(self, text):
        self.ws.cell(row=self.row, column=1, value=text).font = F_BOLD
        for col in range(1, len(COLS) + 1):
            self.ws.cell(row=self.row, column=col).fill = SECTION
        self.row += 1

    def _meta(self, name, kind, form, frm_to, status):
        ws, r = self.ws, self.row
        ws.cell(row=r, column=1, value=name).font = F_BODY
        ws.cell(row=r, column=2, value=kind).font = F_BODY
        ws.cell(row=r, column=3, value=form).font = F_BOLD
        ws.cell(row=r, column=4, value=frm_to).font = F_BODY
        s = ws.cell(row=r, column=7, value=status)
        s.font = F_BODY
        if "[A]" in status:
            s.fill = A_FILL
        for col in range(1, len(COLS) + 1):
            cell = ws.cell(row=r, column=col)
            cell.border = BORDER
            cell.alignment = Alignment(vertical="center", horizontal="left" if col in (1, 4) else "center")

    def _date(self, col, value, linked=False):
        c = self.ws.cell(row=self.row, column=col, value=value)
        c.number_format = DATE_FMT
        c.font = F_LINK if linked else (F_CALC if isinstance(value, str) else F_INPUT)

    def bar(self, name, start, end, color, status, form="", frm_to="", kind="Bar", linked=False):
        r = self.row
        self._meta(name, kind, form, frm_to, status)
        self._date(5, start, linked)
        self._date(6, end, linked)
        rule = f"AND({self.G0}${self.tick_row}<$F{r},EDATE({self.G0}${self.tick_row},{self.step})>$E{r})"
        self.ws.conditional_formatting.add(f"{self.G0}{r}:{self.G1}{r}",
                                           FormulaRule(formula=[rule], fill=fill(color)))
        self.row += 1
        return r

    def milestone(self, name, when, color, status, form="", frm_to="", linked=False):
        r = self.row
        self._meta(name, "Form" if form else "Milestone", form, frm_to, status)
        self._date(5, when, linked)
        for k in range(len(self.ticks)):
            L = get_column_letter(self.g0 + k)
            c = self.ws.cell(row=r, column=self.g0 + k,
                             value=f'=IF(AND($E{r}>={L}${self.tick_row},'
                                   f'$E{r}<EDATE({L}${self.tick_row},{self.step})),"{DIAMOND}","")')
            c.font = fnt(10, True, color="FFFFFF")
            c.alignment = Alignment(horizontal="center")
        self.ws.conditional_formatting.add(f"{self.G0}{r}:{self.G1}{r}",
                                           FormulaRule(formula=[f'{self.G0}{r}="{DIAMOND}"'], fill=fill(color)))
        self.row += 1
        return r

    def notes(self, title, lines, span):
        self.row += 1
        self.ws.cell(row=self.row, column=1, value=title).font = F_BOLD
        self.row += 1
        for n in lines:
            c = self.ws.cell(row=self.row, column=1, value="• " + n)
            c.font = F_NOTE
            c.alignment = Alignment(wrap_text=True, vertical="top")
            self.ws.merge_cells(start_row=self.row, start_column=1, end_row=self.row, end_column=span)
            self.ws.row_dimensions[self.row].height = 26
            self.row += 1

    def legend(self):
        self.row += 1
        self.ws.cell(row=self.row, column=1, value="Colour key").font = F_BOLD
        self.row += 1
        for label, key in [("Design thread bar (client ↔ architect)", "design"),
                           ("Design thread milestone / document", "design_ms"),
                           ("Contract thread bar (construction stage)", "contract"),
                           ("Contract thread milestone / document", "contract_ms"),
                           ("★ Scenario 1 document", "scenario"),
                           ("★ Scenario 1 work period (the extra month)", "scenario_bar"),
                           ("Planned baseline / defects period", "baseline")]:
            self.ws.cell(row=self.row, column=1, value=label).font = F_BODY
            self.ws.cell(row=self.row, column=2).fill = fill(C[key])
            self.row += 1


def page_setup(ws):
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True


wb = openpyxl.Workbook()

# =================================================================== TAB 1
ws = wb.active
ws.title = "Scenario 1 Timeline"
MAIN = "'Scenario 1 Timeline'"
ws["A1"] = "Sydney Opera House — Scenario 1 Project Timeline (additional piers to support the roof)"
ws["A1"].font = F_TITLE
ws["A2"] = ("Built from the group's Document Register (Frank / Prani / Jerry). Styled after the master reference "
            "'gantt_programme_options.xlsx' (Option 1 vs Option 2). Blue = editable input · black = formula · "
            "Status: REG = in the Register · [F] = sourced fact · [A] = our assumption (yellow). "
            "The month-by-month detail of the variation is on the 'Scenario 1 Zoom' tab.")
ws["A2"].font = F_NOTE
ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("A2:AF2")
ws.row_dimensions[2].height = 28

ws["A4"] = "Scenario 1 numbers — change these, everything else follows"
ws["A4"].font = F_WHITE_BIG
for c in range(1, len(COLS) + 1):
    ws.cell(row=4, column=c).fill = BAND
box = [
    ("Site possession (Stage I start) — ABIC F1", D(1959, 3, 2), True, DATE_FMT,
     "[verify] against the SOH Project Information PDF"),
    ("Original date for practical completion — Sched 1 item 22", D(1963, 1, 26), True, DATE_FMT,
     "Tutor's project information"),
    ("Adjustment of time granted by SW-14 (months)", 1, True, "0", "Tutor's worked example for Scenario 1"),
    ("Date for PC after SW-14 (this variation only)", "=EDATE(E6,E7)", False, DATE_FMT,
     "Formula: original PC + SW-14 months"),
    ("Contract sum at signing ($)", 9600000, True, "$#,##0",
     "Tutor's 'ballpark' original budget (~$9.6m); the group may pick another figure"),
    ("Contract price adjustment by SW-11 ($)", 5000, True, "$#,##0", "Tutor's worked example for Scenario 1"),
    ("Contract sum after SW-11 ($) — the figure SW-31 must refer back to", "=E9+E10", False, "$#,##0",
     "Formula. Only this variation is modelled; other project variations are not."),
]
for i, (label, val, is_in, fmt, note) in enumerate(box):
    r = 5 + i
    ws.cell(row=r, column=1, value=label).font = F_BOLD if i == len(box) - 1 else F_BODY
    v = ws.cell(row=r, column=5, value=val)
    v.font, v.number_format = (F_INPUT if is_in else F_CALC), fmt
    if is_in:
        v.fill = YELLOW
    ws.cell(row=r, column=6, value=note).font = F_NOTE
POSS, PC, EOT = "$E$5", "$E$6", "$E$7"

g = Gantt(ws, [D(y, m, 1) for y in range(1956, 1975) for m in (1, 7)], 6,
          year_row=13, first_row=15, tick_fmt="mmm", tick_width=3.4)
R = {}   # row numbers of events the zoom tab links to

g.band("Phase 1 — Client brief → Tender (1956–1958)")
g.section("Design thread — client ↔ architect (CAA) · Lead 1")
g.bar("Competition design phase", D(1956, 1, 1), D(1957, 1, 29), C["design"], "REG [F]",
      frm_to="NSW Govt → entrants")
g.milestone("Introductory letter (Guide Letter 1)", D(1957, 2, 1), C["design_ms"], "REG [A]",
            frm_to="Architect → Client")
g.milestone("CAA signed — must be the 2024 edition (Register says 2019)", D(1957, 2, 21),
            C["design_ms"], "REG", form="CAA", frm_to="Architect → Client")
g.bar("Podium design & documentation", D(1957, 3, 1), D(1959, 2, 1), C["design"], "[A]", frm_to="Architect")
R["roof"] = g.bar("Roof / shell design — unresolved until 1961", D(1957, 3, 1), D(1961, 10, 1),
                  C["design"], "[A] verify", frm_to="Architect + Arup")
g.section("Contract thread — procurement · Lead 2")
g.milestone("Tender documents issued", D(1958, 7, 1), C["contract_ms"], "REG [A]", frm_to="Architect → Contractor")

g.band("Phase 2 — Tender → Start of construction (1958–1959)")
g.section("Contract thread — procurement · Lead 2")
g.milestone("Tender return", D(1959, 1, 1), C["contract_ms"], "REG [A]", frm_to="Contractor → Architect")
g.milestone("Contractor selection (Civil & Civic)", D(1959, 2, 1), C["contract_ms"], "REG [A]")
g.milestone("Simple Works Contract signed", D(1959, 2, 19), C["contract_ms"], "REG", form="SW 2018",
            frm_to="Architect → Contractor")
g.milestone("Site possession — Stage I starts", f"={POSS}", C["contract_ms"], "REG [verify]",
            frm_to="Client → Contractor")
g.section("Design thread — client ↔ architect (CAA) · Lead 1")
g.milestone("Client representative changes: Premier Cahill → Askin (CAA C.3)", D(1959, 10, 1),
            C["design_ms"], "NEW [A]", frm_to="Client → Architect")

g.band("Phase 3 — Construction → Completion (1959–1974)")
g.section("Contract thread — construction · Leads 2–3")
g.bar("Planned programme at signing (baseline)", f"={POSS}", f"={PC}", C["baseline"], "[F] tutor", kind="Baseline")
R["st1"] = g.bar("Stage I — podium (Civil & Civic)", f"={POSS}", D(1962, 6, 1), C["contract"], "REG [A]")
R["st2"] = g.bar("Stage II — roof shells (Hornibrook)", D(1962, 6, 1), D(1967, 1, 1), C["contract"], "REG [A]")
g.milestone("Stage II contract drawings", D(1962, 9, 1), C["contract_ms"], "REG [A]", frm_to="Architect → Contractor")
g.bar("Stage III — interiors & glass walls", D(1967, 1, 1), D(1973, 10, 20), C["contract"], "REG [A]")
g.milestone("Stage III contract drawings", D(1968, 3, 1), C["contract_ms"], "REG [A]", frm_to="Architect → Contractor")

g.section("★ Scenario 1 chain — additional piers (Lead 3; Lead 1 on the CAA side)")
CHAIN = [  # key, name, date, status, form, from->to
    ("prob", "Design problem found: final roof loads exceed the podium columns", D(1961, 6, 1),
     "[A] verify", "", "Arup → Architect"),
    ("d8", "Architect notifies client of extra services + fee (CAA D.8)", D(1961, 7, 1),
     "NEW [A]", "CAA D.8", "Architect → Client"),
    ("sw12", "Instruction for a Variation — strengthen columns, add piers", D(1961, 8, 1),
     "REG [A] month", "SW-12", "Architect → Contractor"),
    ("sw42", "Contractor's details of claim — 1 month, $5,000 (optional form)", D(1961, 9, 1),
     "[A] optional", "SW-42", "Contractor → Architect"),
    ("sw13", "Instruction to proceed with the variation (optional form)", D(1961, 10, 1),
     "[A] optional", "SW-13", "Architect → Contractor"),
]
for key, name, when, status, form, ft in CHAIN:
    R[key] = g.milestone(name, when, C["scenario"], status, form=form, frm_to=ft)
r_work = g.row
R["work"] = g.bar("Piers work on site — the extra time", D(1961, 10, 1), f"=EDATE(E{r_work},{EOT})",
                  C["scenario_bar"], "[A]", frm_to="Contractor", kind="Work")
R["sw14"] = g.milestone("Adjustment of time — +1 month", D(1961, 11, 1), C["scenario"], "REG [A] month",
                        form="SW-14", frm_to="Architect → Contractor")
R["cp06"] = g.milestone("Cost plan issued", D(1962, 3, 1), C["contract_ms"], "REG [A] month",
                        form="CP-06", frm_to="QS → Architect")
R["sw11"] = g.milestone("Contract Price Adjustment — +$5,000", D(1962, 4, 1), C["scenario"], "REG [A] month",
                        form="SW-11", frm_to="Architect → Contractor")

g.section("Completion")
g.milestone("Practical Completion Certificate (opening 20 Oct 1973)", D(1973, 10, 20), C["contract_ms"],
            "REG [F]", frm_to="Architect → Contractor")
g.bar("Defects liability period — 12 months (ABIC M13)", D(1973, 10, 20), D(1974, 10, 20), C["baseline"],
      "[A]", kind="Period")
R["sw31"] = g.milestone("Final Certificate — refers to SW-11", D(1974, 11, 1), C["scenario"], "REG [A] month",
                        form="SW-31", frm_to="Architect → Contractor")

g.legend()
g.notes("Notes", [
    "Read with the master reference (gantt_programme_options.xlsx). Its Option 1 starts building while design is "
    "still going. That is what happened here: the roof-design bar runs over Stage I until 1961, and that overlap "
    "is the cause of Scenario 1.",
    "Grey baseline = what was planned at signing (completion 26 Jan 1963). The real building finished in 1973. "
    "SW-14 only moves the date by this one variation's month — see the box at the top.",
    "Months marked [A] are placeholders inside the year the Register gives. Agree real months as a group, then type "
    "them into the blue date cells. The diamonds here and on the Zoom tab move to match.",
    "CAA row: the Register says CAA 2019; the brief requires CAA 2024. Fix the document, not just the label.",
    "SW-42 and SW-13 are optional forms (the tutor says they can earn extra marks). Delete the rows if not used.",
], span=32)
page_setup(ws)

# =================================================================== TAB 2
z = wb.create_sheet("Scenario 1 Zoom")
z["A1"] = "Scenario 1 Zoom — the variation chain month by month (1961–1962)"
z["A1"].font = F_TITLE
z["A2"] = ("Every date here is a formula pulling from the 'Scenario 1 Timeline' tab (green text). "
           "Change dates on that tab, not here. The Final Certificate (1974) is outside this window.")
z["A2"].font = F_NOTE
z.merge_cells("A2:AB2")

zg = Gantt(z, [D(y, m, 1) for y in (1961, 1962) for m in range(1, 13)], 1,
           year_row=4, first_row=6, tick_fmt="mmm", tick_width=5.5)


def link(col, key):
    return f"={MAIN}!{col}{R[key]}"


zg.band("Context")
zg.bar("Roof / shell design — unresolved until 1961", link("E", "roof"), link("F", "roof"), C["design"],
       "[A] verify", frm_to="Architect + Arup", linked=True)
zg.bar("Stage I — podium (Civil & Civic)", link("E", "st1"), link("F", "st1"), C["contract"], "REG [A]",
       linked=True)
zg.bar("Stage II — roof shells (Hornibrook)", link("E", "st2"), link("F", "st2"), C["contract"], "REG [A]",
       linked=True)
zg.band("★ Scenario 1 chain")
for key, name, when, status, form, ft in CHAIN:
    zg.milestone(name, link("E", key), C["scenario"], status, form=form, frm_to=ft, linked=True)
zg.bar("Piers work on site — the extra time", link("E", "work"), link("F", "work"), C["scenario_bar"], "[A]",
       frm_to="Contractor", kind="Work", linked=True)
zg.milestone("Adjustment of time — +1 month", link("E", "sw14"), C["scenario"], "REG [A] month",
             form="SW-14", frm_to="Architect → Contractor", linked=True)
zg.milestone("Cost plan issued", link("E", "cp06"), C["contract_ms"], "REG [A] month",
             form="CP-06", frm_to="QS → Architect", linked=True)
zg.milestone("Contract Price Adjustment — +$5,000", link("E", "sw11"), C["scenario"], "REG [A] month",
             form="SW-11", frm_to="Architect → Contractor", linked=True)
zg.notes("Reading the chain", [
    "Order of documents follows the tutor's worked example: variation → contractor's claim → instruction to "
    "proceed → adjustment of time → price adjustment → (1974) final certificate referring to the price adjustment.",
    "The CAA D.8 row is the client-side twin of SW-12: the architect's own extra design work and fee, agreed in writing.",
], span=24)
page_setup(z)

wb.active = 0
wb.save(OUT)
print("wrote", OUT)
