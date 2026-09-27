"""Build the SOH project-timeline board for Miro (Assessment 3, item A1).

Modelled on the monday.com Timeline Widget: items grouped into lanes,
bars for date ranges, diamonds for milestones, colour by one column
(here: the factor that changed), a vertical marker line, a colour legend,
and a baseline (planned vs actual).

Outputs (next to this script):
  soh-timeline-template.svg / .png   empty board -> upload to Miro, lock as background
  soh-timeline-example.svg / .png    same board filled with the scaffold events (all [verify])

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
    ("P1  Client brief  ->  Tender", ym(1955, 9, 13), ym(1958, 6), "#E6ECF3"),
    ("P2  Tender  ->  Start construction", ym(1958, 6), ym(1959, 3, 2), "#F4EBDD"),
    ("P3  Construction  ->  Completion", ym(1959, 3, 2), ym(1973, 10, 20), "#E4EFE6"),
    ("Final cert.", ym(1973, 10, 20), ym(1975), "#EEEEEE"),
]

GROUPS = [
    ("DESIGN TIMELINE", "architect's services  -  CAA 2024", [
        ("D0", "CAA services stage", "Sched A: A.1 Concept > A.2 DD > A.4 CD > A.5 > A.6 + approval gates"),
        ("D1", "Client + brief", "decisions, approvals, representatives (C.3)"),
        ("D2", "Architect - design output", "competition, Red Book, Yellow Book, redesign"),
        ("D3", "Consultants - engineering", "client-engaged (E.1): architect coordinates"),
    ]),
    ("CONTRACT TIMELINE", "procurement + ABIC Simple Works 2018", [
        ("C1", "Procurement + tender", "CAA A.5 tender / negotiation, contract signed"),
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

# ---------------------------------------------------------------- example events (all [verify])
# kind: bar | milestone | gate | baseline      tag: F (fact) | A (assumption)
# optional 9th field = bar track (0 upper, 1 lower)
EVENTS = [
    # lane, kind, start, end, label, factor, tag, star(required form / scenario)[, track]
    ("D0", "bar", ym(1957, 3), ym(1958, 3), "A.1 Concept (Red Book)", "Scope", "A", False, 0),
    ("D0", "gate", ym(1958, 3), None, "Gate: concept approved", "Scope", "A", False),
    ("D0", "bar", ym(1958, 3), ym(1962, 1), "A.2 Design Development - roof unresolved (Yellow Book 1962)", "Scope", "A", False, 1),
    ("D0", "bar", ym(1958, 5), ym(1959, 2), "A.4 CD Stage I", "Scope", "A", False, 0),
    ("D0", "gate", ym(1959, 2), None, "Gate SKIPPED: DD not approved before works start", "Scope", "A", True),
    ("D0", "bar", ym(1959, 3, 2), ym(1974, 9), "A.6 Contract Administration (construction + post-construction)", "Time", "A", False, 0),
    ("D1", "milestone", ym(1954), None, "E01 Opera House committee", "Scope", "F", False),
    ("D1", "milestone", ym(1955, 9, 13), None, "E02 Competition launched", "Scope", "F", False),
    ("D1", "milestone", ym(1959, 10), None, "E09 Cahill dies - client rep changes", "Responsibility", "F", False),
    ("D1", "milestone", ym(1965, 5), None, "E15 Askin / Hughes", "Responsibility", "F", False),
    ("D1", "milestone", ym(1966, 2, 28), None, "E16 Utzon resigns", "Responsibility", "F", False),
    ("D1", "milestone", ym(1966, 4), None, "E17 Hall/Todd/Littlemore", "Responsibility", "F", False),
    ("D2", "bar", ym(1955, 9, 13), ym(1957, 1, 29), "Competition", "Scope", "F", False),
    ("D2", "milestone", ym(1957, 3), None, "E04 Architect engaged (CAA)", "Scope", "F", False),
    ("D2", "bar", ym(1957, 3), ym(1961, 10), "Roof geometry unresolved", "Scope", "F", False),
    ("D2", "bar", ym(1963), ym(1966, 2, 28), "Stage III design (plywood)", "Quality", "F", False),
    ("D2", "bar", ym(1966, 4), ym(1973, 10), "Team II redesign + documentation", "Scope", "F", False),
    ("D3", "milestone", ym(1957, 6), None, "E06 Arup engaged by client", "Responsibility", "F", False),
    ("D3", "milestone", ym(1961, 10), None, "E10 Spherical solution", "Quality", "F", False),
    ("D3", "bar", ym(1961, 6), ym(1962, 9), "E11 Columns inadequate for roof", "Scope", "F", True),
    ("C1", "milestone", ym(1958, 11), None, "A.5 Stage I tender accepted", "Cost", "A", False),
    ("C1", "milestone", ym(1959, 2), None, "ABIC SW signed (Sched 1)", "Cost", "A", True),
    ("C1", "milestone", ym(1963, 2), None, "Stage II award - Hornibrook", "Cost", "F", False),
    ("C1", "milestone", ym(1967, 1), None, "Stage III award", "Cost", "F", False),
    ("C2", "milestone", ym(1959, 3, 2), None, "F1 Site possession 2 Mar 1959", "Time", "F", False),
    ("C2", "baseline", ym(1959, 3, 2), ym(1963, 1, 26), "Planned: PC 26 Jan 1963 (Sched 1 item 22)", "Time", "F", False),
    ("C2", "bar", ym(1959, 3, 2), ym(1963, 2), "Stage I podium - Civil & Civic", "Time", "F", False, 0),
    ("C2", "bar", ym(1963, 3), ym(1967, 6), "Stage II shells - Hornibrook", "Time", "F", False, 0),
    ("C2", "bar", ym(1967, 6), ym(1973, 10, 20), "Stage III interiors / glass", "Time", "F", False, 0),
    ("C2", "bar", ym(1973, 10, 20), ym(1974, 10, 20), "M13 DLP 12 mo", "Quality", "A", False, 1),
    ("C3", "milestone", ym(1962, 1), None, "SW-12 Variation (J1)", "Scope", "A", True),
    ("C3", "milestone", ym(1962, 7), None, "SW-14 Adj. of time (H4, L1.1c)", "Time", "A", True),
    ("C3", "milestone", ym(1963, 1), None, "SW-11 Price adj. (H4 / J5)", "Cost", "A", True),
    ("C3", "milestone", ym(1973, 10, 20), None, "M4 PC notice", "Time", "F", False),
    ("C3", "milestone", ym(1974, 9), None, "N10 Final claim", "Cost", "A", False),
    ("C3", "milestone", ym(1974, 11), None, "SW-31 Final cert. (N11)", "Cost", "A", True),
]
SCENARIO_MARK = (ym(1961, 6), "OUR SCENARIO  E11: piers + columns")


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
    pos, lane_ops, body_bottom = lane_positions()
    grid_top = TOP + PHASE_H + AXIS_H
    ops = []

    # title band
    ops.append(rect(0, 0, W, TOP - 20, GROUND))
    ops.append(text(28, 90, "SYDNEY OPERA HOUSE  -  PROJECT TIMELINE", 58, "bold"))
    ops.append(text(28, 145, "PP1 Assessment 3  |  A1 Timeline of significant project events  |  historical dates, contemporary instruments", 28, "normal", MUTED))
    sub = ("EXAMPLE - scaffold events, every item [verify] against the SOH Project Information PDF" if example
           else "TEMPLATE - lock this image as the background, then place cards / bars / diamonds on it")
    ops.append(text(28, 200, sub, 28, "bold", MARKER if example else INK))
    ops.append(text(28, 250, "Group: ____________    Lead 1: ________   Lead 2: ________   Lead 3: ________    Version / date: ________", 26, "normal", MUTED))

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
        ops.append(rect(x(sx) + 8, TOP + PHASE_H + 6, 640, 50, MARKER, rx=6))
        ops.append(text(x(sx) + 22, TOP + PHASE_H + 42, slabel, 26, "bold", PAPER))

    # lower panel: card template + workflow + inbox
    panel_y = body_bottom + AXIS_H + 60
    ops.extend(lower_panel(panel_y))
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
    """Lane layout: two marker rows on top (y+34, y+74), two bar tracks below (y+100, y+144)."""
    ops = []
    slots = {}
    for ev in EVENTS:
        lane, kind, a, b, label, factor, tag, is_star = ev[:8]
        track = ev[8] if len(ev) > 8 else 0
        top, bot = pos[lane]
        dash = "12 7" if tag == "A" else None
        col = FACTORS[factor]
        if kind == "baseline":
            yy = top + 150
            ops.append(rect(x(a), yy, x(b) - x(a), 24, "none", BASELINE, 4, rx=4, dash="12 7"))
            ops.append(text(x(b) + 10, yy + 19, label, 20, "normal", MUTED))
            continue
        if kind == "bar":
            yy = top + 100 + track * 44
            ops.append(rect(x(a), yy, max(x(b) - x(a), 12), 36, col, INK if dash else "none",
                            3 if dash else 0, rx=8, dash=dash))
            ops.append(text(x(a) + 12, yy + 26, label, 21, "bold", PAPER))
        else:
            n = slots.get(lane, 0)
            slots[lane] = n + 1
            cx, yy = x(a), top + 34 + (n % 2) * 40
            if kind == "gate":
                ops.append(gate(cx, yy, 13, col, dash))
            else:
                ops.append(diamond(cx, yy, 15, col, INK, dash))
            ops.append(point_label(cx, yy, label))
            if is_star:
                ops.append(star(cx - 34 if cx <= W - 900 else cx + 34, yy, 14))
        if kind == "bar" and is_star:
            ops.append(star(x(a) - 20, yy + 18, 14))
    return ops


def lower_panel(py0):
    ops = []
    # card template (like the monday item card)
    cx, cw, ch = 60, 1500, 760
    ops.append(text(cx, py0, "EVENT CARD  (copy one per event - Miro card or sticky)", 30, "bold"))
    ops.append(rect(cx, py0 + 30, cw, ch - 60, PAPER, INK, 3, rx=10))
    ops.append(rect(cx, py0 + 30, 22, ch - 60, FACTORS["Scope"], rx=4))
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

    # workflow steps
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
    for i, s in enumerate(steps):
        yy = py0 + 80 + i * 66
        ops.append(f'<circle cx="{wx + 22}" cy="{yy - 8}" r="22" fill="{INK}"/>')
        ops.append(text(wx + 22, yy, str(i + 1), 22, "bold", PAPER, "middle"))
        ops.append(text(wx + 62, yy, s, 25))

    # inbox + zoom frame placeholders
    ix = 4300
    ops.append(text(ix, py0, "INBOX  (unsorted cards)", 30, "bold"))
    ops.append(rect(ix, py0 + 30, 1300, 700, "#FBFBF7", MUTED, 3, rx=10, dash="16 10"))
    ops.append(text(ix + 40, py0 + 90, "new research lands here first - sort weekly", 24, "normal", MUTED))
    zx = 5700
    ops.append(text(zx, py0, "ZOOM FRAME  (scenario by month + ABIC SW clock)", 30, "bold"))
    ops.append(rect(zx, py0 + 30, 1640, 700, "#FFF7F6", MARKER, 3, rx=10))
    # the contract clock: each step, its clause, and the time limit to the next
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
    bw, bh, gap = 300, 108, 24
    for i, (form, name, cl, limit, req) in enumerate(clock):
        r, c = divmod(i, 5)
        bx, by = zx + 30 + c * (bw + gap) + 2, py0 + 56 + r * (bh + 26)
        ops.append(rect(bx, by, bw - 20, bh, PAPER, MARKER if req else MUTED, 3 if req else 2, rx=8,
                        dash=None if req else "10 6"))
        ops.append(text(bx + 14, by + 34, form, 24, "bold", MARKER if req else INK))
        ops.append(text(bx + 14, by + 64, f"{name}  ({cl})", 21))
        ops.append(text(bx + 14, by + 94, f"limit: {limit}", 19, "normal", MUTED))
    ops.append(text(zx + 34, py0 + 330, "WD = working days, BD = business days. Red = required by the brief, dashed = optional form or step. Form <-> clause [verify vs template forms]", 18, "normal", MUTED))
    months = "J F M A M J J A S O N D".split()
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
            lane, kind, a, b, label, factor, tag, is_star = ev[:8]
            when = fmt(a) + (f" - {fmt(b)}" if b else "")
            card = f"{label} | {when} | {factor} | [{tag}] [verify]"
            w.writerow([lane_group[lane].title(), lane, phase_of(a), kind, fmt(a), fmt(b) if b else "",
                        label, factor, tag, "yes" if is_star else "", "[verify]", "", card])
    print("wrote", p)


if __name__ == "__main__":
    write("soh-timeline-template", build(example=False))
    write("soh-timeline-example", build(example=True))
    write_csv("soh-timeline-events-starter.csv")
