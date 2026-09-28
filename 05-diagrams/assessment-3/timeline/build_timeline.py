"""Build the SOH project-timeline board for Miro (Assessment 3, item A1).

Modelled on the monday.com Timeline Widget: items grouped into lanes,
bars for date ranges, diamonds for milestones, colour by one column
(here: the factor that changed), a vertical marker line, a colour legend,
and a baseline (planned vs actual).

Outputs (next to this script):
  soh-timeline-template.svg / .png   empty board -> upload to Miro, lock as background
  soh-timeline-scenario1.svg / .png  PROJECT board: Scenario 1 (additional piers), dates from the group's
                                     Document Register, team names per lane, task-assignment panel

Edit EVENTS / PHASES / LANES below and re-run:  py build_timeline.py
"""
import os
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- scale
Y0, Y1 = 1954.0, 1975.0          # time axis (years)
LEFT, W = 560, 7400              # label column width, total width
X_END = W - 80
PX_PER_YEAR = (X_END - LEFT) / (Y1 - Y0)


def x(year):
    return LEFT + (year - Y0) * PX_PER_YEAR


def ym(y, m=1, d=1):
    """Calendar date -> decimal year."""
    return y + (m - 1) / 12 + (d - 1) / 365


# ---------------------------------------------------------------- palette
INK, MUTED, RULE, PAPER, GROUND = "#18202B", "#586272", "#C9D0D8", "#FFFFFF", "#F2F4F3"
FACTORS = {  # colour by factor (tutor's board: Scope marked red)
    "Scope": "#C8413B",
    "Time": "#E0A030",
    "Cost": "#1F7A8C",
    "Quality": "#5E9E6E",
    "Responsibility": "#7B6AA8",
}
BASELINE = "#9AA3AE"
MARKER = "#C8413B"

# ---------------------------------------------------------------- structure
# Phases = the three periods asked for. Boundaries are planned-sequence
# defaults; move them once dates are verified.
PHASES = [
    ("P1  Client brief  ->  Tender", ym(1956), ym(1958, 6), "#E6ECF3"),
    ("P2  Tender  ->  Start construction", ym(1958, 6), ym(1959, 3, 2), "#F4EBDD"),
    ("P3  Construction  ->  Completion", ym(1959, 3, 2), ym(1973, 10, 20), "#E4EFE6"),
    ("Final cert.", ym(1973, 10, 20), ym(1975), "#EEEEEE"),
]

# Lane owners follow the contributor/checker pattern in the group's Register (Week 10 PDF).
# Lead 2 / Lead 3 are inferred from that pattern -- confirm with the group.
TEAM = {"L1": "Frank", "L2": "Jerry", "L3": "Prani"}
LANE_OWNER = {
    "D0": "Lead 1: Frank  (check: Prani)", "D1": "Lead 1: Frank  (check: Prani)",
    "D2": "Lead 1: Frank  (check: Prani)", "D3": "Lead 1: Frank  (check: Prani)",
    "C1": "Lead 2: Jerry  (check: Frank)", "C2": "Lead 2: Jerry  (check: Frank)",
    "C3": "Lead 3: Prani  (check: Jerry)", "REG": "All three",
}
PROJECT = False   # set in build(); lane owner lines only show on the project board

GROUPS = [
    ("DESIGN TIMELINE", "architect's services  -  CAA 2024", [
        ("D0", "CAA services stage", "Sched A: A.1 Concept > A.2 DD > A.4 CD > A.5 > A.6 + approval gates"),
        ("D1", "Client + brief", "decisions, approvals, representatives (C.3)"),
        ("D2", "Architect - design output", "competition, Red Book, Yellow Book, redesign"),
        ("D3", "Consultants - engineering", "client-engaged (E.1): architect coordinates"),
    ]),
    ("CONTRACT TIMELINE", "procurement + ABIC Simple Works 2018", [
        ("C1", "Procurement + cost", "tender, contract signed, cost plan (QS)"),
        ("C2", "Construction works", "F1 possession > works > M1 PC > M13 DLP"),
        ("C3", "Contract administration", "J1 SW-12 > H4 SW-14 / SW-11 > N11 SW-31"),
    ]),
]

TOP = 300            # below title band
PHASE_H = 110
AXIS_H = 64
GROUP_H = 58
LANE_H = 190
REG_H = 150

# ---------------------------------------------------------------- project events: Scenario 1
# Dates follow the group's Document Register (Week 10/DOCUMENT REGISTER_PP1.pdf) and
# ../programme/soh_scenario1_timeline.xlsx. Where the Register gives only a year, the month is
# an assumption: tag "A" -> dashed outline.  kind: bar | milestone | gate | baseline
def E(lane, kind, a, b, label, factor, tag, star=False, track=0, row=None):
    return dict(lane=lane, kind=kind, a=a, b=b, label=label, factor=factor, tag=tag,
                star=star, track=track, row=row)


EVENTS = [
    # D0 CAA services stage -- the "Option 1" overlap: works start before design development is done
    E("D0", "bar", ym(1957, 3), ym(1958, 3), "A.1 Concept (Red Book)", "Scope", "A", track=0),
    E("D0", "gate", ym(1958, 3), None, "Gate: concept approved", "Scope", "A", row=0),
    E("D0", "bar", ym(1958, 3), ym(1961, 10), "A.2 Design Development - roof unresolved until 1961", "Scope", "A", track=1),
    E("D0", "bar", ym(1958, 5), ym(1959, 2), "A.4 CD Stage I", "Scope", "A", track=0),
    E("D0", "gate", ym(1959, 2), None, "Gate SKIPPED: works start before DD approved", "Scope", "A", star=True, row=1),
    E("D0", "bar", ym(1959, 3, 2), ym(1974, 11), "A.6 Contract Administration (construction + post-construction)", "Time", "A", track=0),
    # D1 client + brief  (Lead 1 documents)
    E("D1", "milestone", ym(1957, 2), None, "Intro letter  [Frank / Prani]", "Scope", "A", star=True, row=0),
    E("D1", "milestone", ym(1957, 2, 21), None, "CAA signed 21 Feb 1957 - must be CAA 2024  [Frank / Prani]", "Scope", "F", star=True, row=1),
    E("D1", "milestone", ym(1959, 10), None, "NEW: client rep Cahill -> Askin (C.3)  [Frank]", "Responsibility", "A", row=0),
    E("D1", "milestone", ym(1961, 7), None, "NEW: CAA D.8 extra services + fee  [Frank]", "Scope", "A", star=True, row=1),
    E("D1", "milestone", ym(1966, 2, 28), None, "Utzon resigns", "Responsibility", "F", row=0),
    E("D1", "milestone", ym(1966, 4, 19), None, "Hall / Todd / Littlemore", "Responsibility", "F", row=1),
    # D2 design output
    E("D2", "bar", ym(1956), ym(1957, 1, 29), "Competition design phase", "Scope", "F", track=0),
    E("D2", "bar", ym(1957, 3), ym(1959, 2), "Podium design + documentation", "Scope", "A", track=0),
    E("D2", "bar", ym(1957, 3), ym(1961, 10), "Roof / shell design - unresolved (overlaps Stage I)", "Scope", "A", track=1),
    # D3 consultants
    E("D3", "milestone", ym(1957, 6), None, "Ove Arup & Partners - engaged by client (CAA E.1)", "Responsibility", "F", row=0),
    E("D3", "milestone", ym(1961, 6), None, "Problem: final roof loads exceed podium columns", "Scope", "A", star=True, row=1),
    # C1 procurement + cost  (Lead 2)
    E("C1", "milestone", ym(1958, 7), None, "Tender docs issued", "Cost", "A", row=0),
    E("C1", "milestone", ym(1959, 1), None, "Tender return", "Cost", "A", row=1),
    E("C1", "milestone", ym(1959, 2, 19), None, "ABIC SW 2018 signed 19 Feb 1959  [Jerry / Frank]", "Cost", "F", star=True, row=2),
    E("C1", "milestone", ym(1962, 3), None, "CP-06 cost plan (QS)", "Cost", "A", row=0),
    # C2 construction  (Lead 2)
    E("C2", "milestone", ym(1959, 3, 2), None, "F1 site possession 2 Mar 1959 [verify]", "Time", "F", row=0),
    E("C2", "baseline", ym(1959, 3, 2), ym(1963, 1, 26), "Planned: PC 26 Jan 1963 (Sched 1 item 22)", "Time", "F"),
    E("C2", "bar", ym(1959, 3, 2), ym(1962, 6), "Stage I podium - Civil & Civic", "Time", "A", track=0),
    E("C2", "bar", ym(1962, 6), ym(1967, 1), "Stage II shells - Hornibrook", "Time", "A", track=0),
    E("C2", "bar", ym(1967, 1), ym(1973, 10, 20), "Stage III interiors / glass", "Time", "A", track=0),
    E("C2", "bar", ym(1961, 10), ym(1961, 11), "Piers work +1 month", "Time", "A", star=True, track=1),
    E("C2", "bar", ym(1973, 10, 20), ym(1974, 10, 20), "M13 DLP 12 mo", "Quality", "A", track=1),
    # C3 contract administration  (Lead 3) -- short labels; the zoom frame has the detail
    E("C3", "milestone", ym(1961, 8), None, "SW-12", "Scope", "A", star=True, row=0),
    E("C3", "milestone", ym(1961, 9), None, "SW-42", "Time", "A", row=1),
    E("C3", "milestone", ym(1961, 10), None, "SW-13", "Scope", "A", row=2),
    E("C3", "milestone", ym(1961, 11), None, "SW-14 +1 mo", "Time", "A", star=True, row=3),
    E("C3", "milestone", ym(1962, 4), None, "SW-11 +$5,000", "Cost", "A", star=True, row=0),
    E("C3", "milestone", ym(1973, 10, 20), None, "PC certificate", "Time", "F", row=1),
    E("C3", "milestone", ym(1974, 11), None, "SW-31 final cert (refers to SW-11)", "Cost", "A", star=True, row=2),
]
SCENARIO_MARK = (ym(1961, 6), "OUR SCENARIO 1: additional piers to support the roof")

# zoom frame (project board): the chain month by month, with contributor / checker from the Register
ZOOM = [  # (year, month, form, text, who, required)
    (1961, 6, "trigger", "Roof loads exceed podium columns (Arup)", "", False),
    (1961, 7, "CAA D.8", "Extra services + fee -> client", "Frank", True),
    (1961, 8, "SW-12", "Instruction for a Variation: piers", "Prani / Jerry", True),
    (1961, 9, "SW-42", "Contractor's claim: 1 month, $5,000", "optional", False),
    (1961, 10, "SW-13", "Instruction to proceed", "optional", False),
    (1961, 11, "SW-14", "Adjustment of time +1 month", "Prani / Jerry", True),
    (1962, 3, "CP-06", "Cost plan (QS -> architect)", "Jerry?", False),
    (1962, 4, "SW-11", "Contract price adjustment +$5,000", "Prani / Jerry", True),
]


# ---------------------------------------------------------------- svg helpers
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(xx, yy, s, size=26, weight="normal", fill=INK, anchor="start"):
    return (f'<text x="{xx:.1f}" y="{yy:.1f}" font-family="Helvetica, Arial, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>')


def rect(xx, yy, w, h, fill, stroke="none", sw=0, rx=0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{xx:.1f}" y="{yy:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def line(x1, y1, x2, y2, stroke=RULE, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def diamond(cx, cy, r, fill, stroke=INK, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    pts = f"{cx},{cy-r} {cx+r},{cy} {cx},{cy+r} {cx-r},{cy}"
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="3"{d}/>'


def star(cx, cy, r, fill=MARKER):
    import math
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.pi / 2 + i * math.pi / 5
        pts.append(f"{cx + rr*math.cos(a):.1f},{cy - rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{PAPER}" stroke-width="2"/>'


# ---------------------------------------------------------------- layout
def lane_positions():
    """Return {lane_id: (y_top, y_bottom)} and list of drawing ops for lanes."""
    y = TOP + PHASE_H + AXIS_H
    pos, ops = {}, []
    for gname, gsub, lanes in GROUPS:
        ops.append(rect(0, y, W, GROUP_H, INK))
        ops.append(text(28, y + 40, gname, 30, "bold", PAPER))
        ops.append(text(28 + len(gname) * 21 + 30, y + 40, gsub, 24, "normal", "#C9D3DF"))
        y += GROUP_H
        for i, (lid, lname, lsub) in enumerate(lanes):
            ops.append(rect(0, y, W, LANE_H, PAPER if i % 2 == 0 else "#FAFBFB"))
            ops.append(line(0, y + LANE_H, W, y + LANE_H, RULE, 2))
            ops.append(text(28, y + 58, lid, 26, "bold", MUTED))
            ops.append(text(80, y + 58, lname, 30, "bold"))
            ops.append(text(80, y + 96, lsub, 22, "normal", MUTED))
            if PROJECT:
                ops.append(text(80, y + 140, LANE_OWNER[lid], 23, "bold", "#1F4E78"))
            pos[lid] = (y, y + LANE_H)
            y += LANE_H
    # documents strip
    ops.append(rect(0, y, W, GROUP_H, "#3B4655"))
    ops.append(text(28, y + 40, "ARCHITECTS REGISTER", 30, "bold", PAPER))
    ops.append(text(420, y + 40, "every card that issues a document  ->  one register row (Date | Document | Form No. | From/To | Details | Student)", 24, "normal", "#C9D3DF"))
    y += GROUP_H
    ops.append(rect(0, y, W, REG_H, "#F7F8F9"))
    ops.append(text(80, y + 60, "Doc refs", 30, "bold"))
    ops.append(text(80, y + 96, "place doc no. tags under the event", 22, "normal", MUTED))
    pos["REG"] = (y, y + REG_H)
    y += REG_H
    return pos, ops, y


def build(example):
    global PROJECT
    PROJECT = example
    pos, lane_ops, body_bottom = lane_positions()
    grid_top = TOP + PHASE_H + AXIS_H
    ops = []

    # title band
    ops.append(rect(0, 0, W, TOP - 20, GROUND))
    ops.append(text(28, 90, "SYDNEY OPERA HOUSE  -  PROJECT TIMELINE", 58, "bold"))
    ops.append(text(28, 145, "PP1 Assessment 3  |  A1 Timeline of significant project events  |  historical dates, contemporary instruments", 28, "normal", MUTED))
    sub = ("PROJECT - Scenario 1 (additional piers). Dates = group's Document Register; dashed outline = [A] month placeholder"
           if example else "TEMPLATE - lock this image as the background, then place cards / bars / diamonds on it")
    ops.append(text(28, 200, sub, 28, "bold", MARKER if example else INK))
    grp = ("Group: Frank / Prani / Jerry     Lead 1: Frank     Lead 2: Jerry     Lead 3: Prani     "
           "Version: v1 / 29 Sep 2026   (Leads 2-3 inferred from the Register - confirm)") if example else           "Group: ____________    Lead 1: ________   Lead 2: ________   Lead 3: ________    Version / date: ________"
    ops.append(text(28, 250, grp, 26, "bold" if example else "normal", "#1F4E78" if example else MUTED))

    # legend (top right)
    lx, ly = 4300, 40
    ops.append(text(lx, ly + 28, "COLOUR BY FACTOR", 22, "bold", MUTED))
    for i, (k, c) in enumerate(FACTORS.items()):
        xx = lx + i * 330
        ops.append(rect(xx, ly + 46, 60, 34, c, rx=6))
        ops.append(text(xx + 72, ly + 72, k, 24))
    ly2 = ly + 120
    ops.append(text(lx, ly2 + 28, "SHAPES", 22, "bold", MUTED))
    ops.append(rect(lx, ly2 + 46, 110, 34, "#DDE3EA", INK, 2, rx=6))
    ops.append(text(lx + 122, ly2 + 72, "bar = date range", 22))
    ops.append(diamond(lx + 420, ly2 + 63, 20, "#DDE3EA"))
    ops.append(text(lx + 450, ly2 + 72, "milestone = one date", 22))
    ops.append(rect(lx + 720, ly2 + 50, 110, 26, "none", BASELINE, 4, rx=4, dash="10 6"))
    ops.append(text(lx + 842, ly2 + 72, "baseline (planned)", 22))
    ops.append(rect(lx + 1080, ly2 + 46, 60, 34, "#FFFFFF", INK, 3, rx=6, dash="10 6"))
    ops.append(text(lx + 1152, ly2 + 72, "dashed = [A] assumption", 22))
    ops.append(star(lx + 1470, ly2 + 63, 20))
    ops.append(text(lx + 1500, ly2 + 72, "required form / scenario", 22))
    ops.append(line(lx + 1800, ly2 + 44, lx + 1800, ly2 + 84, MARKER, 5))
    ops.append(text(lx + 1815, ly2 + 72, "scenario marker", 22))
    ops.append(gate(lx + 2040, ly2 + 63, 13, "#DDE3EA"))
    ops.append(text(lx + 2066, ly2 + 72, "CAA approval gate", 22))

    # phase header + tinted phase columns
    for name, a, b, col in PHASES:
        ops.append(rect(x(a), grid_top, x(b) - x(a), body_bottom - grid_top, col))
    ops.extend(lane_ops_tinted(lane_ops))
    for name, a, b, col in PHASES:
        ops.append(rect(x(a), TOP, x(b) - x(a), PHASE_H - 8, col, INK, 2))
        label = name if (x(b) - x(a)) > 700 else name.split("  ")[0]
        ops.append(text(x(a) + 16, TOP + 42, label, 28, "bold"))
        if (x(b) - x(a)) <= 700:
            rest = name.split("  ", 1)[1].strip() if "  " in name else ""
            for j, part in enumerate(rest.split("->")):
                ops.append(text(x(a) + 16, TOP + 72 + j * 26, part.strip() + (" ->" if j == 0 and "->" in rest else ""), 20, "normal", MUTED))
        else:
            ops.append(text(x(a) + 16, TOP + 80, f"{fmt(a)}  to  {fmt(b)}  (default - adjust)", 20, "normal", MUTED))
    ops.append(text(28, TOP + 48, "PHASES", 26, "bold", MUTED))
    ops.append(text(28, TOP + 80, "the three periods", 20, "normal", MUTED))

    # year axis + gridlines
    ay = TOP + PHASE_H
    ops.append(rect(0, ay, W, AXIS_H, GROUND))
    ops.append(text(28, ay + 42, "YEAR", 24, "bold", MUTED))
    for yr in range(int(Y0), int(Y1) + 1):
        xx = x(yr)
        ops.append(line(xx, ay + AXIS_H, xx, body_bottom, "#D9DEE4", 2 if yr % 5 else 3))
        if yr < Y1:
            ops.append(text(xx + 8, ay + 42, str(yr), 26, "bold" if yr % 5 == 0 else "normal", INK if yr % 5 == 0 else MUTED))
    ops.append(line(LEFT, ay, LEFT, body_bottom, INK, 3))

    # bottom axis repeat
    ops.append(rect(0, body_bottom, W, AXIS_H, GROUND))
    for yr in range(int(Y0), int(Y1)):
        ops.append(text(x(yr) + 8, body_bottom + 42, str(yr), 24, "normal", MUTED))

    if example:
        ops.extend(draw_events(pos))
        sx, slabel = SCENARIO_MARK
        ops.append(line(x(sx), TOP + PHASE_H, x(sx), body_bottom, MARKER, 6))
        ops.append(rect(x(sx) + 8, TOP + PHASE_H + 6, 16 * len(slabel) + 40, 50, MARKER, rx=6))
        ops.append(text(x(sx) + 22, TOP + PHASE_H + 42, slabel, 26, "bold", PAPER))

    # lower panel: card template + workflow + inbox
    panel_y = body_bottom + AXIS_H + 60
    ops.extend(lower_panel(panel_y, example))
    total_h = panel_y + 900

    body = "\n".join(ops)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{total_h}" '
            f'viewBox="0 0 {W} {total_h}">\n{rect(0, 0, W, total_h, PAPER)}\n{body}\n</svg>')


def lane_ops_tinted(lane_ops):
    """Lane backgrounds are drawn semi-transparent so the phase tint shows through."""
    out = []
    for op in lane_ops:
        if op.startswith("<rect") and ('fill="#FFFFFF"' in op or 'fill="#FAFBFB"' in op or 'fill="#F7F8F9"' in op):
            op = op.replace("/>", ' fill-opacity="0.55"/>')
        out.append(op)
    return out


def fmt(yr):
    y = int(yr)
    m = int(round((yr - y) * 12)) + 1
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    return f"{months[min(m, 12) - 1]} {y}"


def gate(cx, cy, r, fill, dash=None):
    """Client written-approval gate (CAA): a square with a heavy outline."""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{cx-r:.1f}" y="{cy-r:.1f}" width="{2*r}" height="{2*r}" fill="{fill}" '
            f'stroke="{INK}" stroke-width="5"{d}/>')


def point_label(cx, yy, label, size=21):
    """Label to the right of a marker, or to the left near the right edge."""
    if cx > W - 900:
        return text(cx - 26, yy + 8, label, size, "normal", INK, "end")
    return text(cx + 26, yy + 8, label, size, "normal", INK)


def draw_events(pos):
    """Marker rows at y+34/+74/+114/+154 (rows 0-3); bar tracks at y+100 (0) and y+144 (1)."""
    ops = []
    slots = {}
    for ev in EVENTS:
        lane, kind, a, b, label = ev["lane"], ev["kind"], ev["a"], ev["b"], ev["label"]
        top, bot = pos[lane]
        dash = "12 7" if ev["tag"] == "A" else None
        col = FACTORS[ev["factor"]]
        if kind == "baseline":
            yy = top + 150
            ops.append(rect(x(a), yy, x(b) - x(a), 24, "none", BASELINE, 4, rx=4, dash="12 7"))
            ops.append(text(x(b) + 10, yy + 19, label, 20, "normal", MUTED))
            continue
        if kind == "bar":
            yy = top + 100 + ev["track"] * 44
            w = max(x(b) - x(a), 12)
            ops.append(rect(x(a), yy, w, 36, col, INK if dash else "none", 3 if dash else 0, rx=8, dash=dash))
            if w >= 12 * len(label):
                ops.append(text(x(a) + 12, yy + 26, label, 21, "bold", PAPER))
            else:  # too short to hold its label: write it to the right
                ops.append(text(x(a) + w + 12, yy + 26, label, 21, "bold", INK))
            if ev["star"]:
                ops.append(star(x(a) - 20, yy + 18, 14))
            continue
        n = slots.get(lane, 0)
        slots[lane] = n + 1
        rrow = ev["row"] if ev["row"] is not None else n % 2
        cx, yy = x(a), top + 34 + rrow * 40
        if kind == "gate":
            ops.append(gate(cx, yy, 13, col, dash))
        else:
            ops.append(diamond(cx, yy, 15, col, INK, dash))
        ops.append(point_label(cx, yy, label))
        if ev["star"]:
            ops.append(star(cx - 34 if cx <= W - 900 else cx + 34, yy, 14))
    return ops


def lower_panel(py0, project=False):
    ops = []
    # ---- event card (like the monday item card); the project board shows the SW-12 card filled in
    cx, cw, ch = 60, 1500, 760
    ops.append(text(cx, py0, "EVENT CARD  (copy one per event - Miro card or sticky)", 30, "bold"))
    ops.append(rect(cx, py0 + 30, cw, ch - 60, PAPER, INK, 3, rx=10))
    ops.append(rect(cx, py0 + 30, 22, ch - 60, FACTORS["Scope"], rx=4))
    if project:
        rows = [
            ("E-ID  |  Date(s)", "S1-03  |  Aug 1961  [A] month (Register: 1961)"),
            ("Event", "Instruction for a Variation - strengthen columns, add piers"),
            ("Timeline  /  lane", "Contract  /  C3 Contract administration"),
            ("Phase", "P3 Construction -> Completion"),
            ("Initiated by  ->  must respond", "Architect (Utzon)  ->  Contractor (Civil & Civic)"),
            ("Factor changed", "Scope   (+ Time 1 month, Cost $5,000)"),
            ("[F] fact / [A] assumption", "[A] month; figures = tutor's worked example"),
            ("Documents + clause", "SW-12 (J1) -> SW-14 (H4/L1) -> SW-11 (H4/J5); CAA D.8"),
            ("Student  (lead / research / check)", "Prani  /  ________  /  Jerry"),
        ]
    else:
        rows = [
            ("E-ID  |  Date(s)", "E11  |  Jun 1961 - Sep 1962"),
            ("Event", "Podium columns inadequate for final roof loads"),
            ("Timeline  /  lane", "Design  /  D3 Consultants"),
            ("Phase", "P3 Construction -> Completion"),
            ("Initiated by  ->  must respond", "Engineer (Arup)  ->  Architect, Client, Contractor"),
            ("Factor changed", "Scope   (+ Time, Cost)"),
            ("[F] fact / [A] assumption", "[F]  source: SOH Project Info p._  [verify]"),
            ("Documents + clause", "SW-12 (J1), SW-14 (H4/L1), SW-11 (H4/J5); CAA D.8"),
            ("Student  (lead / research / check)", "________ / ________ / ________"),
        ]
    for i, (k, v) in enumerate(rows):
        yy = py0 + 100 + i * 70
        ops.append(text(cx + 50, yy, k, 22, "bold", MUTED))
        ops.append(text(cx + 560, yy, v, 24))
        if i < len(rows) - 1:
            ops.append(line(cx + 40, yy + 26, cx + cw - 30, yy + 26, "#E3E7EB", 2))

    # ---- workflow steps
    wx = 1700
    ops.append(text(wx, py0, "WORKFLOW  (each research session)", 30, "bold"))
    steps = [
        "Research an event -> write ONE card in the Inbox",
        "Classify: Design or Contract timeline -> drop in its lane",
        "Place on the year axis: bar if a range, diamond if one date",
        "Colour by the factor that changed (Scope / Time / Cost / Quality / Resp.)",
        "Tag [F] + source, or [A] + reason (dashed outline)",
        "Draw connectors cause -> consequence between cards",
        "Planned vs actual: grey dashed baseline under the actual bar",
        "Scenario events: red star + copy into the Zoom frame (months)",
        "Card issues a document? -> add the Architects Register row the same day",
        "Weekly: lead checks their lanes; auditor filters by tag for gaps",
    ]
    for i, st in enumerate(steps):
        yy = py0 + 80 + i * 66
        ops.append(f'<circle cx="{wx + 22}" cy="{yy - 8}" r="22" fill="{INK}"/>')
        ops.append(text(wx + 22, yy, str(i + 1), 22, "bold", PAPER, "middle"))
        ops.append(text(wx + 62, yy, st, 25))

    # ---- inbox (template) / task assignment (project)
    ix = 4300
    if project:
        ops.append(text(ix, py0, "TASK ASSIGNMENT  (from the Register)", 30, "bold"))
        ops.append(rect(ix, py0 + 30, 1300, 700, "#F7FAFD", "#1F4E78", 3, rx=10))
        tasks = [
            ("LEAD 1 - FRANK", "lanes D0-D3  |  checker: Prani", [
                "Date the introductory letter (Register has no date)",
                "Build the CAA on the 2024 template (Register says 2019)",
                "Add row: client rep change Cahill -> Askin (CAA C.3)",
                "Add row: CAA D.8 extra-services notice, Jul 1961"]),
            ("LEAD 2 - JERRY", "lanes C1-C2  |  checker: Frank", [
                "Tender dates + contractor selection (Register: years only)",
                "ABIC SW Schedule 1: contract sum, possession, PC date",
                "Cost plan CP-06: name the QS or declare [A]"]),
            ("LEAD 3 - PRANI", "lane C3  |  checker: Jerry", [
                "SW-12 -> SW-14 (+1 month) -> SW-11 (+$5,000) -> SW-31",
                "Optional: SW-42 claim + SW-13 instruction to proceed"]),
            ("ALL THREE", "before the Week 12 presentation", [
                "Agree the [A] months (dashed outlines on this board)",
                "Premier in 1961: tutor's Askin or historical Heffron?",
                "Architect on SW-31 (1974): Utzon, or Hall/Todd/Littlemore?"]),
        ]
        yy = py0 + 80
        for head, sub, items in tasks:
            ops.append(text(ix + 30, yy, head, 25, "bold", "#1F4E78"))
            ops.append(text(ix + 330, yy, sub, 20, "normal", MUTED))
            yy += 34
            for it in items:
                ops.append(rect(ix + 36, yy - 16, 16, 16, PAPER, INK, 2, rx=2))
                ops.append(text(ix + 64, yy, it, 21))
                yy += 30
            yy += 14
    else:
        ops.append(text(ix, py0, "INBOX  (unsorted cards)", 30, "bold"))
        ops.append(rect(ix, py0 + 30, 1300, 700, "#FBFBF7", MUTED, 3, rx=10, dash="16 10"))
        ops.append(text(ix + 40, py0 + 90, "new research lands here first - sort weekly", 24, "normal", MUTED))

    # ---- zoom frame: ABIC SW clock + month grid
    zx = 5700
    ops.append(text(zx, py0, "ZOOM FRAME  (scenario by month + ABIC SW clock)", 30, "bold"))
    ops.append(rect(zx, py0 + 30, 1640, 700, "#FFF7F6", MARKER, 3, rx=10))
    clock = [
        ("SW-12", "Variation", "J1", "before PC", True),
        ("notice", "Effect", "J2.3", "20 WD", False),
        ("SW-13", "Proceed?", "J3", "5 WD", False),
        ("SW-42", "Claim", "H1-H2", "20 WD", False),
        ("SW-14 / 11", "Decision", "H4", "20 WD", True),
        ("cert.", "Progress", "J5 / N4", "10 BD", False),
        ("PC", "Notice", "M4", "5 WD", False),
        ("DLP", "Defects", "M13", "12 mo", False),
        ("SW-49", "Final claim", "N10", "20 WD", False),
        ("SW-31", "Final cert.", "N11", "10 BD", True),
    ]
    bw, bh, gap = 300, (70 if project else 108), 24
    for i, (form, name, cl, limit, req) in enumerate(clock):
        r, c = divmod(i, 5)
        bx, by = zx + 30 + c * (bw + gap) + 2, py0 + 50 + r * (bh + 12)
        ops.append(rect(bx, by, bw - 20, bh, PAPER, MARKER if req else MUTED, 3 if req else 2, rx=8,
                        dash=None if req else "10 6"))
        ops.append(text(bx + 14, by + 30, form, 22 if project else 24, "bold", MARKER if req else INK))
        if project:
            ops.append(text(bx + 14, by + 58, f"{name} ({cl})  {limit}", 18))
        else:
            ops.append(text(bx + 14, by + 64, f"{name}  ({cl})", 21))
            ops.append(text(bx + 14, by + 94, f"limit: {limit}", 19, "normal", MUTED))
    months = "J F M A M J J A S O N D".split()
    if project:
        gx0, gy0, gw = zx + 40, py0 + 250, 1560
        pm = gw / 24
        for yi, yr in enumerate((1961, 1962)):
            ops.append(text(gx0 + yi * 12 * pm, gy0, str(yr), 24, "bold", MARKER))
            for mi, m in enumerate(months):
                mx = gx0 + (yi * 12 + mi) * pm
                ops.append(text(mx + pm / 2, gy0 + 28, m, 18, "normal", MUTED, "middle"))
                ops.append(line(mx, gy0 + 38, mx, py0 + 715, "#F0D6D3", 1))
        for i, (yr, mo, form, what, who, req) in enumerate(ZOOM):
            mx = gx0 + ((yr - 1961) * 12 + mo - 1) * pm + pm / 2
            yy = gy0 + 64 + i * 51
            ops.append(diamond(mx, yy, 13, MARKER if req else "#FFFFFF", INK))
            lbl = f"{form}  {what}" + (f"   [{who}]" if who else "")
            ops.append(text(mx + 22, yy + 7, lbl, 19, "bold" if req else "normal", INK))
        ops.append(text(gx0, py0 + 718, "months placed inside the Register's years are [A] - agree them as a group; SW-31 (Nov 1974) is off this grid", 18, "normal", MUTED))
    else:
        ops.append(text(zx + 34, py0 + 330, "WD = working days, BD = business days. Red = required by the brief, dashed = optional form or step. Form <-> clause [verify vs template forms]", 18, "normal", MUTED))
        for yi, yr in enumerate(range(1961, 1964)):
            bx = zx + 40 + yi * 525
            ops.append(text(bx, py0 + 380, str(yr), 26, "bold", MARKER))
            for mi, m in enumerate(months):
                ops.append(text(bx + mi * 42, py0 + 412, m, 20, "normal", MUTED))
                ops.append(line(bx + mi * 42 - 4, py0 + 424, bx + mi * 42 - 4, py0 + 700, "#F0D6D3", 1))
        ops.append(text(zx + 40, py0 + 718, "re-date the months to your scenario; place each form card on its issue month", 20, "normal", MUTED))
    return ops


def write(name, svg):
    p = os.path.join(HERE, name)
    with open(p + ".svg", "w", encoding="utf-8") as f:
        f.write(svg)
    doc = pymupdf.open(p + ".svg")
    doc[0].get_pixmap(dpi=72).save(p + ".png")
    print("wrote", p + ".svg / .png")


def phase_of(yr):
    for name, a, b, _ in PHASES:
        if a <= yr < b:
            return name.split("  ")[0]
    return "pre-P1"


def write_csv(name):
    """One row per example event -> paste the 'Card text' column into Miro (one sticky per cell)."""
    import csv
    lane_group = {lid: g for g, _, lanes in GROUPS for lid, _, _ in lanes}
    p = os.path.join(HERE, name)
    with open(p, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Timeline", "Lane", "Phase", "Kind", "Start", "End", "Event", "Factor",
                    "F/A", "Required form / scenario", "Source", "Student", "Card text"])
        for ev in EVENTS:
            lane, kind, a, b, label = ev["lane"], ev["kind"], ev["a"], ev["b"], ev["label"]
            factor, tag, is_star = ev["factor"], ev["tag"], ev["star"]
            when = fmt(a) + (f" - {fmt(b)}" if b else "")
            card = f"{label} | {when} | {factor} | [{tag}]"
            w.writerow([lane_group[lane].title(), lane, phase_of(a), kind, fmt(a), fmt(b) if b else "",
                        label, factor, tag, "yes" if is_star else "", "Register / tutor" if tag == "F" else "[A]",
                        LANE_OWNER[lane], card])
    print("wrote", p)


if __name__ == "__main__":
    write("soh-timeline-template", build(example=False))
    write("soh-timeline-scenario1", build(example=True))
    write_csv("soh-timeline-scenario1-events.csv")
