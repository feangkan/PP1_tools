"""Build an editable Excel Gantt chart matching the reference image format:
month-tick axis, colour-coded phase bars, Best/Worst case rows per Option,
built with real formulas + conditional formatting so it recalculates live.
"""
import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, NamedStyle
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter
from openpyxl.comments import Comment

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Programme Options"

ARIAL = "Arial"
INPUT_FONT = Font(name=ARIAL, size=10, color="0000FF")          # blue = editable input
FORMULA_FONT = Font(name=ARIAL, size=10, color="000000")         # black = formula
LABEL_FONT = Font(name=ARIAL, size=10)
BOLD = Font(name=ARIAL, size=10, bold=True)
TITLE_FONT = Font(name=ARIAL, size=13, bold=True)
WHITE_BOLD = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
NOTE_FONT = Font(name=ARIAL, size=9, italic=True, color="595959")

GRID_HEADER_FILL = PatternFill("solid", fgColor="404040")
SECTION_FILL = PatternFill("solid", fgColor="D9D9D9")
OPT_FILL = PatternFill("solid", fgColor="1F4E78")
YELLOW_FILL = PatternFill("solid", fgColor="FFFF00")

thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

# ---- phase colour scheme -------------------------------------------------
COLORS = {
    "podium_design": "ADD8E6",
    "constr1": "4472C4",
    "stage2_design": "C6E0B4",
    "constr2": "548235",
    "stage3_design": "FBE5D6",
    "constr3": "C55A11",
    "opt2_design": "F4B6C2",
    "opt2_constr": "7030A0",
}

# ---- grid geometry --------------------------------------------------------
GRID_START_COL = 8   # column H
TICK_STEP = 6
N_TICKS = 27          # 0,6,...,156
HEADER_ROW = 6        # shared month-tick header row

def col_letter(i):
    return get_column_letter(i)

def month_col(tick_index):
    return GRID_START_COL + tick_index

LAST_GRID_COL = month_col(N_TICKS - 1)

# ================================================================= TITLE ===
ws["A1"] = "Sydney Opera House — Design & Construction Programme Options"
ws["A1"].font = TITLE_FONT
ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=14)

ws["A2"] = ("Reconstructed in this format from the reference image supplied — phase names and duration "
            "ranges are read from that image. Overlap between phases is this workbook's own editable "
            "assumption (see the blue cells), not asserted as verified SOH history — check it against a "
            "real source before treating the bar positions as fact.")
ws["A2"].font = NOTE_FONT
ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=26)
ws.row_dimensions[2].height = 26
ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")

ws["A3"] = "Blue = editable input · Black = formula (recalculates automatically) · Bars below use conditional formatting keyed to Start/End"
ws["A3"].font = NOTE_FONT

# ===================================================== COLUMN HEADERS (row 5) ===
HEAD_ROW = 5
headers = ["Phase", "Duration range (given)", "Duration used\n(months)", "Overlap with\nprevious (months)",
           "Start\n(month)", "End\n(month)"]
for i, h in enumerate(headers, start=1):
    c = ws.cell(row=HEAD_ROW, column=i, value=h)
    c.font = WHITE_BOLD
    c.fill = GRID_HEADER_FILL
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    c.border = BORDER
ws.row_dimensions[HEAD_ROW].height = 44

# month-tick header (row 6), shared by every block below
ws.cell(row=HEAD_ROW, column=GRID_START_COL - 1, value="Months").font = WHITE_BOLD
ws.cell(row=HEAD_ROW, column=GRID_START_COL - 1).fill = GRID_HEADER_FILL
for t in range(N_TICKS):
    v = t * TICK_STEP
    c = ws.cell(row=HEAD_ROW, column=month_col(t), value=v)
    c.font = WHITE_BOLD
    c.fill = GRID_HEADER_FILL
    c.alignment = Alignment(horizontal="center")
    c.border = BORDER
    ws.column_dimensions[col_letter(month_col(t))].width = 4.2

for i in range(1, 6 + 1):
    ws.column_dimensions[col_letter(i)].width = [42, 14, 11, 12, 13, 9][i - 1]
ws.column_dimensions[col_letter(GRID_START_COL - 1)].width = 8

ws.freeze_panes = ws.cell(row=HEAD_ROW + 1, column=GRID_START_COL)

# ================================================================ helpers ===
row = HEAD_ROW + 1

def option_header(label, dur_range, start_date_text):
    global row
    ws.cell(row=row, column=1, value=label).font = Font(name=ARIAL, size=12, bold=True, color="FFFFFF")
    for c in range(1, 7):
        ws.cell(row=row, column=c).fill = OPT_FILL
    ws.cell(row=row, column=2, value=dur_range).font = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
    ws.cell(row=row, column=3, value="Earliest Construction Date").font = Font(name=ARIAL, size=9, color="FFFFFF")
    d = ws.cell(row=row, column=5, value=start_date_text)
    d.number_format = "d mmm yyyy"
    d.font = INPUT_FONT
    d.fill = YELLOW_FILL
    date_cell = f"$E${row}"
    row += 1
    return date_cell

def section_label(text):
    global row
    ws.cell(row=row, column=1, value=text).font = BOLD
    for c in range(1, 7):
        ws.cell(row=row, column=c).fill = SECTION_FILL
    row += 1

def phase_row(name, dur_text, duration_months, overlap_months, prev_end_cell, color_hex):
    """Write one phase row with Start/End formulas and a conditional-format bar."""
    global row
    r = row
    ws.cell(row=r, column=1, value=name).font = LABEL_FONT
    ws.cell(row=r, column=2, value=dur_text).font = LABEL_FONT
    dcell = ws.cell(row=r, column=3, value=duration_months)
    dcell.font = INPUT_FONT
    dcell.fill = YELLOW_FILL
    ocell = ws.cell(row=r, column=4, value=overlap_months)
    ocell.font = INPUT_FONT
    ocell.fill = YELLOW_FILL

    start_formula = "=0" if prev_end_cell is None else f"=$F${prev_end_cell}-$D${r}"
    scell = ws.cell(row=r, column=5, value=start_formula)
    scell.font = FORMULA_FONT
    ecell = ws.cell(row=r, column=6, value=f"=$E${r}+$C${r}")
    ecell.font = FORMULA_FONT
    for c in range(1, 7):
        ws.cell(row=r, column=c).border = BORDER
        ws.cell(row=r, column=c).alignment = Alignment(horizontal="center" if c >= 3 else "left", vertical="center")

    rng = f"{col_letter(GRID_START_COL)}{r}:{col_letter(LAST_GRID_COL)}{r}"
    fill = PatternFill(start_color=color_hex, end_color=color_hex, fill_type="solid")
    formula = f"AND({col_letter(GRID_START_COL)}${HEAD_ROW}>=$E${r},{col_letter(GRID_START_COL)}${HEAD_ROW}<$F${r})"
    ws.conditional_formatting.add(rng, FormulaRule(formula=[formula], fill=fill))
    row += 1
    return r

def completion_row(label, start_date_cell, end_month_cell):
    global row
    ws.cell(row=row, column=1, value=label).font = BOLD
    c = ws.cell(row=row, column=5, value=f"=EDATE({start_date_cell},{end_month_cell})")
    c.number_format = "d mmm yyyy"
    c.font = FORMULA_FONT
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
    row += 1

def blank_row(n=1):
    global row
    row += n

# =========================================================== OPTION 1 =====
opt1_date_cell = option_header("Option 1", "72–120 months total", datetime.date(1958, 9, 25))
blank_row()

# ---- 1A Best case: minimum durations, larger fast-track overlaps ----
section_label("1A — Best case scenario (fast-tracked, minimum durations)")
r1 = phase_row("Design and documentation — Podium", "18–24", 18, 0, None, COLORS["podium_design"])
r2 = phase_row("Construction Stage 1", "18–30", 18, 6, r1, COLORS["constr1"])
r3 = phase_row("Stage 2: Shells — design and documentation", "24–42", 24, 6, r2, COLORS["stage2_design"])
r4 = phase_row("Construction Stage 2", "18–36", 18, 6, r3, COLORS["constr2"])
r5 = phase_row("Stage 3: Interiors — design and documentation", "12–18", 12, 6, r4, COLORS["stage3_design"])
r6 = phase_row("Construction Stage 3", "6–12", 6, 0, r5, COLORS["constr3"])
completion_row("Best-case predicted completion:", opt1_date_cell, f"$F${r6}")
blank_row()

# ---- 1B Worst case: maximum durations, little/no overlap ----
section_label("1B — Worst case scenario (sequential, maximum durations)")
r7 = phase_row("Design and documentation — Podium", "18–24", 24, 0, None, COLORS["podium_design"])
r8 = phase_row("Construction Stage 1", "18–30", 30, 0, r7, COLORS["constr1"])
r9 = phase_row("Stage 2: Shells — design and documentation", "24–42", 42, 6, r8, COLORS["stage2_design"])
r10 = phase_row("Construction Stage 2", "18–36", 36, 0, r9, COLORS["constr2"])
r11 = phase_row("Stage 3: Interiors — design and documentation", "12–18", 18, 6, r10, COLORS["stage3_design"])
r12 = phase_row("Construction Stage 3", "6–12", 12, 0, r11, COLORS["constr3"])
completion_row("Worst-case predicted completion:", opt1_date_cell, f"$F${r12}")
blank_row(2)

# =========================================================== OPTION 2 =====
opt2_date_cell = option_header("Option 2", "84–108 months total", datetime.date(1961, 3, 26))
blank_row()

section_label("2A — Best case scenario (minimum durations)")
r13 = phase_row("Design and documentation", "48–60", 48, 0, None, COLORS["opt2_design"])
r14 = phase_row("Construction", "36–48", 36, 0, r13, COLORS["opt2_constr"])
completion_row("Best-case predicted completion:", opt2_date_cell, f"$F${r14}")
blank_row()

section_label("2B — Worst case scenario (maximum durations)")
r15 = phase_row("Design and documentation", "48–60", 60, 0, None, COLORS["opt2_design"])
r16 = phase_row("Construction", "36–48", 48, 0, r15, COLORS["opt2_constr"])
completion_row("Worst-case predicted completion:", opt2_date_cell, f"$F${r16}")
blank_row(2)

# ================================================================ NOTES ===
ws.cell(row=row, column=1, value="Notes").font = BOLD
row += 1
notes = [
    "Duration range (given) = the min–max months read from the reference image for that phase.",
    "Duration used (months) = editable input; pre-set to the minimum for Best-case rows and the maximum for Worst-case rows.",
    "Overlap with previous (months) = editable input; how much this phase's start pulls back into the previous phase. 0 = fully sequential.",
    "Start / End (month) = formulas: Start = previous phase's End − this phase's Overlap; End = Start + Duration used.",
    "Change any blue cell and every bar, Start/End and completion date below it recalculates automatically.",
    "Option 2 shown with only two phases (Design+documentation, Construction) because the reference image gave no further breakdown for it.",
    "CHECK: Option 2 matches the reference totals exactly (84 best / 108 worst). Option 1 best case matches (72). "
    "Option 1 worst case does NOT yet match: it computes 150 months here vs 120 in the reference — one or more Option 1 "
    "phase ranges were probably misread from the image. Correct the yellow Duration cells in rows 1B if you have the real figures.",
]
for n in notes:
    nc = ws.cell(row=row, column=1, value="• " + n)
    nc.font = NOTE_FONT
    nc.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=26)
    ws.row_dimensions[row].height = 26 if len(n) > 150 else 14
    row += 1

ws.sheet_view.showGridLines = False
wb.save("gantt_programme_options.xlsx")
print("wrote gantt_programme_options.xlsx")
