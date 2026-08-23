"""
Assessment 1 stigmergy generator  v0.4
Development copy -- does not overwrite 05-diagrams/assessment-1/stigmergy-generator.py

Rhino 8 Script Editor (Python 3 / CPython). Run to open the control panel.

NO TEXT IS BAKED
----------------
Rhino annotation scale cannot be trusted for readable type. This script
draws coloured geometry only: keep-out circle, ring wrap, trunks, branches,
tip dots, relation arcs. Object names (Properties panel) hold catalog IDs
so a selected dot can be matched to the web guide -- nothing is drawn as
letters.

Place words by hand using:
  stigmergy-guide.html  (zoomable picture / web app)
  stigmergy-text-catalog.md

LAYOUT
------
Same clock as the web guide: gold REGISTRATION at the bottom, terracotta
POWER on a smaller inner ring, wrap-arcs around the title (not through it).
"""

import math
import random
import traceback

import Rhino
import Rhino.Geometry as rg
import Rhino.UI
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Eto.Drawing as edrawing
import Eto.Forms as eforms


# -----------------------------------------------------------------
# Theme
# -----------------------------------------------------------------
def _ec(r, g, b):
    return edrawing.Color(r / 255.0, g / 255.0, b / 255.0)


TH = {
    "bg_form": _ec(18, 18, 18),
    "bg_ctrl": _ec(36, 36, 36),
    "bg_btn": _ec(50, 50, 50),
    "bg_btn_hi": _ec(65, 65, 65),
    "fg": _ec(175, 175, 175),
    "fg_section": _ec(155, 155, 155),
    "fg_bright": _ec(218, 218, 218),
}


class Widgets(object):
    def lbl(self, text, bold=False, width=None, color=None, size=8.0):
        lb = eforms.Label()
        lb.Text = text
        lb.TextColor = color if color is not None else TH["fg"]
        style = edrawing.FontStyle.Bold if bold else edrawing.FontStyle(0)
        lb.Font = edrawing.Font(lb.Font.FamilyName, size, style)
        if width is not None:
            lb.Width = width
        lb.VerticalAlignment = eforms.VerticalAlignment.Center
        return lb

    def section(self, title):
        return self.lbl(title, bold=True, color=TH["fg_section"])

    def num(self, value, lo, hi, dec=0, inc=1, width=80):
        ns = eforms.NumericStepper()
        ns.Value = value
        ns.MinValue = lo
        ns.MaxValue = hi
        ns.DecimalPlaces = dec
        ns.Increment = inc
        ns.Width = width
        return ns

    def button(self, label, handler=None, width=90, primary=False):
        btn = eforms.Button()
        btn.Text = label
        btn.Width = width
        btn.BackgroundColor = TH["bg_btn_hi"] if primary else TH["bg_btn"]
        btn.TextColor = TH["fg_bright"]
        if handler is not None:
            btn.Click += handler
        return btn

    def row(self, label, ctrl, lbl_w=160):
        tl = eforms.TableLayout()
        tl.Spacing = edrawing.Size(5, 0)
        spacer = eforms.TableCell(eforms.Label())
        spacer.ScaleWidth = True
        tl.Rows.Add(eforms.TableRow(
            eforms.TableCell(self.lbl(label, width=lbl_w)),
            eforms.TableCell(ctrl),
            spacer,
        ))
        return tl

    def button_row(self, *buttons):
        tl = eforms.TableLayout()
        tl.Spacing = edrawing.Size(6, 0)
        spacer = eforms.TableCell(eforms.Label())
        spacer.ScaleWidth = True
        cells = [eforms.TableCell(b) for b in buttons] + [spacer]
        tl.Rows.Add(eforms.TableRow(*cells))
        return tl

    def log_area(self, height=150):
        log = eforms.TextArea()
        log.ReadOnly = True
        log.Height = height
        log.Font = edrawing.Font(edrawing.FontFamilies.Monospace, 8.5)
        log.BackgroundColor = TH["bg_ctrl"]
        log.TextColor = TH["fg_bright"]
        return log

    def layout(self, spacing=4, padding=7):
        lay = eforms.DynamicLayout()
        lay.DefaultSpacing = edrawing.Size(spacing, spacing)
        lay.Padding = edrawing.Padding(padding)
        lay.BackgroundColor = TH["bg_form"]
        return lay

    def combo(self, items, index=0, width=160):
        cb = eforms.ComboBox()
        cb.DataStore = list(items)
        cb.SelectedIndex = index
        cb.Width = width
        return cb

    def check(self, text, on=True):
        c = eforms.CheckBox()
        c.Text = text
        c.Checked = on
        c.TextColor = TH["fg"]
        return c


def make_logger(text_area, keep_lines=160):
    def log_msg(msg):
        current = text_area.Text or ""
        lines = (current + str(msg) + "\n").split("\n")
        text_area.Text = "\n".join(lines[-keep_lines:])
    return log_msg


# -----------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------
class GrowthParams(object):
    def __init__(self):
        self.seed = 7
        self.influence_radius = 16.0
        self.kill_distance = 3.5
        self.segment_length = 2.6
        self.max_iterations = 550
        self.attractors_per_zone = 110
        self.ring_radius = 95.0
        self.title_keepout = 40.0
        self.outward_bias = 0.45
        self.tip_dot_radius = 3.4
        self.trunk_dot_radius = 6.5
        self.rel_dot_radius = 3.0
        self.trunk_line = 0.90
        self.spoke_line = 0.42
        self.wrap_line = 0.38
        self.hair_line = 0.20
        self.draw_title_circle = True
        self.draw_wrap_arcs = True


ORIGIN = rg.Point3d(0, 0, 0)


def polar(radius, deg):
    a = math.radians(deg)
    return rg.Point3d(radius * math.cos(a), radius * math.sin(a), 0)


# -----------------------------------------------------------------
# Content -- IDs match stigmergy-text-catalog.md
# angle = degrees from +X, CCW (90 = top, 270 = bottom)
# -----------------------------------------------------------------
CATEGORIES = [
    {
        "key": "ETHICS",
        "zoom": "Duty past the fee-payer",
        "colour": (176, 106, 122),
        "angle": 90,
        "ring_scale": 1.0,
        "zone_radius": 30,
        "subs": [
            ("H1", "Knowledge becomes power"),
            ("H2", "Client not in the room"),
            ("H3", "Profession is not a business"),
            ("H4", "Fees do not shrink judgment"),
            ("H5", "No good or bad architects"),
            ("H6", "Architecture, not Architects"),
            ("H7", "Searchlight or lantern"),
            ("H8", "Collective test"),
        ],
    },
    {
        "key": "LEGISLATION",
        "zoom": "Instruments that can be rewritten",
        "colour": (91, 124, 153),
        "angle": 50,
        "ring_scale": 1.0,
        "zone_radius": 34,
        "subs": [
            ("L1", "Act gives legal form"),
            ("L2", "RIBA was not a licence"),
            ("L3", "Victoria public register"),
            ("L4", "Purpose of the Act"),
            ("L5", "Cannot sign undone work"),
            ("L6", "Resign rather than breach"),
            ("L7", "Fire-isolated stair"),
            ("L8", "Professional vs prohibited"),
            ("L9", "NCC class and type"),
            ("L10", "London 1666 same logic"),
            ("L11", "Law is provisional"),
            ("L12", "Subject interpreter co-author"),
        ],
    },
    {
        "key": "RESEARCH",
        "zoom": "Codes change what may be built",
        "colour": (77, 143, 106),
        "angle": 10,
        "ring_scale": 1.0,
        "zone_radius": 26,
        "subs": [
            ("N1", "Fit for purpose, then performance"),
            ("N2", "Codes are co-authored"),
            ("N3", "Bathrooms into the NCC"),
            ("N4", "Carbon written as a limit"),
            ("N5", "Optional becomes ordinary"),
            ("N6", "One good, another problem"),
        ],
    },
    {
        "key": "PROCUREMENT",
        "zoom": "Contract can strip design control",
        "colour": (52, 80, 112),
        "angle": 330,
        "ring_scale": 1.0,
        "zone_radius": 22,
        "subs": [
            ("P1", "Bringing a building into being"),
            ("P2", "Design and construct"),
            ("P3", "Novated D and C"),
            ("P4", "Institute survey 2019"),
            ("P5", "What is lost after novation"),
        ],
    },
    {
        "key": "REGISTRATION",
        "zoom": "The one compulsory gate",
        "colour": (201, 162, 39),
        "angle": 270,
        "ring_scale": 1.0,
        "zone_radius": 40,
        "subs": [
            ("R1", "Accredited education first"),
            ("R2", "Five statutory requirements"),
            ("R3", "Two classes of registration"),
            ("R4", "Three pathways in"),
            ("R5", "Logbook 3300 hours"),
            ("R6", "Four competency groups"),
            ("R7", "Statement of experience"),
            ("R8", "National exam"),
            ("R9", "Interview probes gaps"),
            ("R10", "Pass is not registration"),
            ("R11", "Fail repeats the stage"),
            ("R12", "CPD and insurance loop"),
        ],
    },
    {
        "key": "EMPLOYMENT",
        "zoom": "Hours in practice; project is a loop",
        "colour": (166, 138, 91),
        "angle": 225,
        "ring_scale": 1.0,
        "zone_radius": 26,
        "subs": [
            ("W1", "Firm is where hours live"),
            ("W2", "Project management walked off"),
            ("W3", "ACA and the union"),
            ("W4", "One project, five stages"),
            ("W5", "Two external gates"),
            ("W6", "Competencies span both ends"),
        ],
    },
    {
        "key": "EDUCATION",
        "zoom": "Judgment trained, then kept alive",
        "colour": (107, 155, 107),
        "angle": 185,
        "ring_scale": 1.0,
        "zone_radius": 26,
        "subs": [
            ("E1", "University under AQF"),
            ("E2", "Judgment over competency"),
            ("E3", "Integrity head heart hand"),
            ("E4", "CPD is formative"),
            ("E5", "Knowledge should be collective"),
            ("E6", "Classic or neo-profession"),
        ],
    },
    {
        "key": "BODIES",
        "zoom": "Institute advances; Board accounts",
        "colour": (138, 107, 168),
        "angle": 140,
        "ring_scale": 1.0,
        "zone_radius": 28,
        "subs": [
            ("B1", "AIA is voluntary"),
            ("B2", "ARBV is statutory"),
            ("B3", "AACA sets the national test"),
            ("B4", "Network around the AIA"),
            ("B5", "Fragmentation is the problem"),
            ("B6", "Awards write the value system"),
            ("B7", "Outside juries disagree"),
            ("B8", "Six media channels"),
        ],
    },
    {
        "key": "POWER",
        "zoom": "Tight title, loose code and contract",
        "colour": (176, 80, 64),
        "angle": 305,
        "ring_scale": 0.62,
        "zone_radius": 20,
        "subs": [
            ("K1", "Interlocking seats"),
            ("K2", "Influence sits in relations"),
            ("K3", "Tight title, loose instrument"),
            ("K4", "Crisis without revolution"),
            ("K5", "Institution versus the public"),
            ("K6", "What should change"),
        ],
    },
]

# (from_key, to_key, rel_id, verb)
RELATIONS = [
    ("EDUCATION", "REGISTRATION", "X1", "depends upon"),
    ("EMPLOYMENT", "REGISTRATION", "X2", "depends upon"),
    ("LEGISLATION", "REGISTRATION", "X3", "enables"),
    ("LEGISLATION", "EMPLOYMENT", "X4", "limits"),
    ("EDUCATION", "REGISTRATION", "X5", "enables"),
    ("RESEARCH", "LEGISLATION", "X6", "influences"),
    ("PROCUREMENT", "REGISTRATION", "X7", "limits"),
    ("ETHICS", "REGISTRATION", "X8", "depends upon"),
    ("BODIES", "ETHICS", "X9", "influences"),
    ("POWER", "REGISTRATION", "X10", "contrasts"),
    ("POWER", "LEGISLATION", "X11", "contrasts"),
    ("POWER", "PROCUREMENT", "X12", "contrasts"),
]


# -----------------------------------------------------------------
# Geometry helpers
# -----------------------------------------------------------------
def ensure_layer(name, colour):
    if not rs.IsLayer(name):
        rs.AddLayer(name, colour)
    return name


def clear_diagram_layers(status_cb):
    removed = 0
    for layer in (rs.LayerNames() or []):
        if layer.startswith("Diagram::"):
            ids = rs.ObjectsByLayer(layer)
            if ids:
                rs.DeleteObjects(ids)
                removed += len(ids)
    if removed:
        status_cb("Cleared {} objects from previous bake.".format(removed))


def force_annotation_scale_to_one(status_cb):
    try:
        dimstyles = sc.doc.DimStyles
        current = dimstyles.Current
        if abs(current.DimensionScale - 1.0) > 1e-9:
            was = current.DimensionScale
            fixed = current.Duplicate()
            fixed.DimensionScale = 1.0
            dimstyles.Modify(fixed, current.Index, True)
            status_cb("Annotation scale was {:.3g}:1 -- reset to 1:1.".format(was))
        else:
            status_cb("Annotation scale already 1:1.")
    except Exception:
        status_cb("Could not auto-fix annotation scale:\n" + traceback.format_exc())


def random_point_in_disc(center, radius):
    r = radius * math.sqrt(random.random())
    a = random.random() * 2.0 * math.pi
    return rg.Point3d(center.X + r * math.cos(a), center.Y + r * math.sin(a), 0)


def push_outside_keepout(pt, keepout):
    d = pt.DistanceTo(ORIGIN)
    if d >= keepout:
        return pt
    if d < 1e-9:
        return rg.Point3d(keepout, 0, 0)
    scale = (keepout + 0.8) / d
    return rg.Point3d(pt.X * scale, pt.Y * scale, 0)


def grow_branches(root_pt, zone_center, zone_radius, n_attractors, params):
    attractors = []
    for _ in range(n_attractors):
        p = random_point_in_disc(zone_center, zone_radius)
        p = push_outside_keepout(p, params.title_keepout + 2.0)
        attractors.append(p)

    nodes = [root_pt]
    parent_of = {0: -1}

    for _ in range(int(params.max_iterations)):
        if not attractors:
            break

        node_dir_sum = {}
        node_count = {}

        for a in attractors:
            nearest_i, nearest_d = -1, params.influence_radius
            for i, n in enumerate(nodes):
                d = n.DistanceTo(a)
                if d < nearest_d:
                    nearest_d, nearest_i = d, i
            if nearest_i >= 0:
                v = a - nodes[nearest_i]
                if v.Length > 1e-9:
                    v.Unitize()
                    node_dir_sum[nearest_i] = node_dir_sum.get(nearest_i, rg.Vector3d(0, 0, 0)) + v
                    node_count[nearest_i] = node_count.get(nearest_i, 0) + 1

        if not node_dir_sum:
            break

        for i, vsum in node_dir_sum.items():
            avg = vsum / node_count[i]
            away = nodes[i] - ORIGIN
            if away.Length > 1e-9:
                away.Unitize()
                avg = avg + away * params.outward_bias
            if avg.Length > 1e-9:
                avg.Unitize()
            new_pt = push_outside_keepout(
                nodes[i] + avg * params.segment_length,
                params.title_keepout + 1.0,
            )
            nodes.append(new_pt)
            parent_of[len(nodes) - 1] = i

        attractors = [a for a in attractors
                      if all(n.DistanceTo(a) >= params.kill_distance for n in nodes)]

    return nodes, parent_of


def node_depth(index, parent_of):
    d = 0
    i = index
    seen = set()
    while i in parent_of and parent_of[i] >= 0 and i not in seen:
        seen.add(i)
        i = parent_of[i]
        d += 1
    return d


def find_leaf_tips(nodes, parent_of):
    is_parent = set(parent_of.values())
    leaves = [i for i in range(len(nodes)) if i not in is_parent and i != 0]
    leaves.sort(key=lambda i: nodes[i].DistanceTo(nodes[0]), reverse=True)
    return leaves


def wrap_arc_points(p1, p2, radius):
    a1 = math.atan2(p1.Y, p1.X)
    a2 = math.atan2(p2.Y, p2.X)
    da = a2 - a1
    while da > math.pi:
        da -= 2.0 * math.pi
    while da < -math.pi:
        da += 2.0 * math.pi
    steps = max(10, int(abs(da) / 0.10))
    pts = []
    for i in range(steps + 1):
        t = i / float(steps)
        a = a1 + da * t
        pts.append(rg.Point3d(radius * math.cos(a), radius * math.sin(a), 0))
    return pts


def set_print_width(obj_id, width):
    try:
        rs.ObjectPrintWidth(obj_id, width)
    except Exception:
        pass


def name_obj(obj_id, name):
    """Invisible ID -- shows in Properties, not on the drawing."""
    if not obj_id:
        return
    try:
        rs.ObjectName(obj_id, name)
    except Exception:
        pass
    try:
        rs.SetUserText(obj_id, "catalog", name)
    except Exception:
        pass


def _as_list(val):
    if val is None:
        return []
    if isinstance(val, (list, tuple)):
        return [v for v in val if v]
    return [val]


def paint(obj_id, colour, layer, name=None):
    if not obj_id:
        return
    try:
        rs.ObjectLayer(obj_id, layer)
    except Exception:
        pass
    try:
        rs.ObjectColor(obj_id, colour)
    except Exception:
        pass
    if name:
        name_obj(obj_id, name)


def thicken_curve(curve_id, radius, colour, layer, name=None, delete_curve=True):
    """Real 3D pipe so weight shows on screen when zoomed out.
    Plot-width alone is print-only and disappears in a shaded/zoomed view."""
    if not curve_id:
        return None
    set_print_width(curve_id, max(radius * 6.0, 0.8))
    pipes = None
    try:
        pipes = rs.AddPipe(curve_id, [0.0, 1.0], [radius, radius], 0, 1)
    except Exception:
        try:
            pipes = rs.AddPipe(curve_id, 0, radius)
        except Exception:
            pipes = None
    made = _as_list(pipes)
    if not made:
        paint(curve_id, colour, layer, name)
        return curve_id
    for p in made:
        paint(p, colour, layer, name)
    if delete_curve:
        try:
            rs.DeleteObject(curve_id)
        except Exception:
            pass
    return made


def add_thick_line(p1, p2, radius, colour, layer, name=None):
    lid = rs.AddLine(p1, p2)
    if not lid:
        return None
    paint(lid, colour, layer, name)
    return thicken_curve(lid, radius, colour, layer, name)


def add_filled_disk(pt, radius, colour, layer, name):
    """Solid seat for hand-lettering -- hatch, or a sphere if hatch fails."""
    circ = rs.AddCircle(pt, radius)
    if not circ:
        return None
    paint(circ, colour, layer, name)
    hatches = None
    try:
        hatches = rs.AddHatch(circ)
    except Exception:
        hatches = None
    for h in _as_list(hatches):
        paint(h, colour, layer, name)
        return h
    try:
        sid = rs.AddSphere(pt, radius)
        if sid:
            paint(sid, colour, layer, name)
            try:
                rs.DeleteObject(circ)
            except Exception:
                pass
            return sid
    except Exception:
        pass
    return circ


def add_halo(pt, radius, colour, layer, name):
    cid = rs.AddCircle(pt, radius)
    if not cid:
        return None
    paint(cid, colour, layer, name)
    set_print_width(cid, 0.8)
    thicken_curve(cid, max(radius * 0.06, 0.18), colour, layer, name, delete_curve=True)
    return cid


def add_diamond(pt, size, colour, layer, name):
    pts = [
        rg.Point3d(pt.X, pt.Y + size, 0),
        rg.Point3d(pt.X + size, pt.Y, 0),
        rg.Point3d(pt.X, pt.Y - size, 0),
        rg.Point3d(pt.X - size, pt.Y, 0),
        rg.Point3d(pt.X, pt.Y + size, 0),
    ]
    pl = rs.AddPolyline(pts)
    if not pl:
        return add_filled_disk(pt, size, colour, layer, name)
    paint(pl, colour, layer, name)
    hatches = None
    try:
        hatches = rs.AddHatch(pl)
    except Exception:
        hatches = None
    for h in _as_list(hatches):
        paint(h, colour, layer, name)
        return h
    return pl


def add_text_seat(pt, colour, layer, name, kind, params):
    """Every place you must letter gets a marker you can see zoomed out."""
    if kind == "title":
        add_filled_disk(pt, params.trunk_dot_radius * 0.85, (70, 70, 70), layer, name)
        add_halo(pt, params.trunk_dot_radius * 1.35, (90, 90, 90), layer, name)
        # crosshair so the hole reads as 'write here'
        s = params.trunk_dot_radius * 1.8
        add_thick_line(rg.Point3d(pt.X - s, pt.Y, 0), rg.Point3d(pt.X + s, pt.Y, 0),
                       0.22, (70, 70, 70), layer, name)
        add_thick_line(rg.Point3d(pt.X, pt.Y - s, 0), rg.Point3d(pt.X, pt.Y + s, 0),
                       0.22, (70, 70, 70), layer, name)
        return
    if kind == "main":
        add_filled_disk(pt, params.trunk_dot_radius, colour, layer, name)
        add_halo(pt, params.trunk_dot_radius * 1.55, colour, layer, name)
        return
    if kind == "rel":
        add_diamond(pt, params.rel_dot_radius, (90, 90, 90), layer, name)
        return
    add_filled_disk(pt, params.tip_dot_radius, colour, layer, name)
    add_halo(pt, params.tip_dot_radius * 1.45, colour, layer, name)


# -----------------------------------------------------------------
# Bake
# -----------------------------------------------------------------
def bake_title(params, status_cb):
    layer = ensure_layer("Diagram::Title", (80, 80, 80))
    rs.CurrentLayer(layer)
    add_text_seat(ORIGIN, (70, 70, 70), layer, "TITLE", "title", params)
    if params.draw_title_circle:
        cid = rs.AddCircle(ORIGIN, params.title_keepout)
        paint(cid, (90, 90, 90), layer, "TITLE")
        thicken_curve(cid, params.wrap_line, (90, 90, 90), layer, "TITLE")
    status_cb("Title seat + keep-out ring -- letter in the centre hole.")


def bake_main_wrap(roots_sorted, params):
    layer = ensure_layer("Diagram::MainWrap", (110, 110, 110))
    rs.CurrentLayer(layer)
    if len(roots_sorted) < 3:
        return
    pts = list(roots_sorted) + [roots_sorted[0]]
    crv = rs.AddInterpCurve(pts, 3)
    if crv:
        thicken_curve(crv, params.wrap_line, (110, 110, 110), layer, "MAIN_WRAP")


def bake_zone(cat, params):
    colour = cat["colour"]
    layer = ensure_layer("Diagram::" + cat["key"], colour)
    rs.CurrentLayer(layer)

    root = polar(params.ring_radius * cat["ring_scale"], cat["angle"])
    away = root - ORIGIN
    if away.Length > 1e-9:
        away.Unitize()
    zone_center = root + away * (cat["zone_radius"] * 0.70)

    add_text_seat(root, colour, layer, cat["key"], "main", params)

    nodes, parent_of = grow_branches(
        root, zone_center, cat["zone_radius"],
        params.attractors_per_zone, params,
    )

    for i in range(1, len(nodes)):
        depth = node_depth(i, parent_of)
        lid = rs.AddLine(nodes[parent_of[i]], nodes[i])
        if not lid:
            continue
        paint(lid, colour, layer, cat["key"])
        if depth <= 2:
            thicken_curve(lid, params.trunk_line, colour, layer, cat["key"])
        elif depth <= 5:
            thicken_curve(lid, params.hair_line, colour, layer, cat["key"])
        else:
            set_print_width(lid, 0.35)

    # Content dots sit on a FIXED outward fan (same order as stigmergy-guide.html).
    # Organic growth above is the look only -- it does not pick which sentence
    # goes on which tip. Catalog order = left-to-right across the fan.
    marker_layer = ensure_layer("Diagram::Markers", colour)
    rs.CurrentLayer(marker_layer)
    placed = 0
    n = len(cat["subs"])
    spread = 0.95  # radians -- matches the web guide
    for k, (mid, _short) in enumerate(cat["subs"]):
        t = 0.0 if n == 1 else (k / float(n - 1) - 0.5)
        ang = t * spread
        c, s = math.cos(ang), math.sin(ang)
        ox = away.X * c - away.Y * s
        oy = away.X * s + away.Y * c
        length = cat["zone_radius"] * 1.15 + (k % 3) * 3.0
        tip = rg.Point3d(root.X + ox * length, root.Y + oy * length, 0)
        tip = push_outside_keepout(tip, params.title_keepout + 4.0)
        add_thick_line(root, tip, params.spoke_line, colour, marker_layer, mid)
        add_text_seat(tip, colour, marker_layer, mid, "sub", params)
        placed += 1

    return {
        "root": root,
        "colour": colour,
        "placed": placed,
        "missing": [],
        "angle": cat["angle"],
    }


def bake_relations(zone_results, params, status_cb):
    if not params.draw_wrap_arcs:
        return
    layer = ensure_layer("Diagram::Relations", (120, 120, 120))
    rs.CurrentLayer(layer)
    arc_r = params.title_keepout + (params.ring_radius - params.title_keepout) * 0.42

    for a_key, b_key, rid, verb in RELATIONS:
        if a_key not in zone_results or b_key not in zone_results:
            continue
        p1 = zone_results[a_key]["root"]
        p2 = zone_results[b_key]["root"]
        pts = wrap_arc_points(p1, p2, arc_r)
        if len(pts) < 2:
            continue
        crv = rs.AddInterpCurve(pts)
        if not crv:
            continue
        rel_name = "{} {}".format(rid, verb)
        thicken_curve(crv, params.wrap_line * 0.85, (100, 100, 100), layer, rel_name)
        mid = pts[len(pts) // 2]
        add_text_seat(mid, (90, 90, 90), layer, rel_name, "rel", params)
    status_cb("Relation arcs thickened; grey diamonds are verb seats.")


def generate_diagram(params, status_cb):
    random.seed(params.seed)
    force_annotation_scale_to_one(status_cb)
    clear_diagram_layers(status_cb)

    sc.doc.Views.RedrawEnabled = False
    try:
        bake_title(params, status_cb)
        zone_results = {}
        roots_for_wrap = []
        for cat in CATEGORIES:
            result = bake_zone(cat, params)
            zone_results[cat["key"]] = result
            if cat["ring_scale"] >= 0.95:
                roots_for_wrap.append((cat["angle"], result["root"]))
            status_cb("{} : {} content dots on the fan (catalog order).".format(
                cat["key"], result["placed"]))

        roots_for_wrap.sort(key=lambda t: t[0])
        bake_main_wrap([p for _, p in roots_for_wrap], params)
        bake_relations(zone_results, params, status_cb)
    finally:
        sc.doc.Views.RedrawEnabled = True

    rs.ZoomExtents()
    status_cb("Seats are filled. Pipes carry line weight on screen. Letter from stigmergy-guide.html.")


# -----------------------------------------------------------------
# GUI
# -----------------------------------------------------------------
class StigmergyForm(eforms.Form):

    def __init__(self):
        eforms.Form.__init__(self)
        self.Title = "A1 Stigmergy  v0.5  (thick lines + text seats)"
        self.Resizable = True
        self.ClientSize = edrawing.Size(460, 720)
        self.Padding = edrawing.Padding(8)
        self.BackgroundColor = TH["bg_form"]
        self.params = GrowthParams()
        self._build_ui()

    def _build_ui(self):
        w = Widgets()
        lay = w.layout()

        lay.AddRow(w.section("Layout -- title in the hole, mains on a ring"))
        self._ring = w.num(self.params.ring_radius, 40, 220, dec=1)
        lay.AddRow(w.row("Ring radius", self._ring))
        self._keepout = w.num(self.params.title_keepout, 12, 90, dec=1)
        lay.AddRow(w.row("Title keep-out", self._keepout))
        self._outward = w.num(self.params.outward_bias, 0.0, 1.5, dec=2, inc=0.05)
        lay.AddRow(w.row("Outward bias", self._outward))
        self._draw_title = w.check("Draw title keep-out circle", True)
        lay.AddRow(self._draw_title)
        self._draw_arcs = w.check("Draw wrap-around relation arcs", True)
        lay.AddRow(self._draw_arcs)

        lay.AddRow(w.section("Growth"))
        self._seed = w.num(self.params.seed, 0, 9999)
        lay.AddRow(w.row("Random seed", self._seed))
        self._influence = w.num(self.params.influence_radius, 4, 60, dec=1)
        lay.AddRow(w.row("Influence radius", self._influence))
        self._kill = w.num(self.params.kill_distance, 1, 20, dec=1)
        lay.AddRow(w.row("Kill distance", self._kill))
        self._segment = w.num(self.params.segment_length, 0.5, 10, dec=1)
        lay.AddRow(w.row("Segment length", self._segment))
        self._iterations = w.num(self.params.max_iterations, 50, 2000, dec=0, inc=10)
        lay.AddRow(w.row("Max iterations", self._iterations))
        self._attractors = w.num(self.params.attractors_per_zone, 20, 400, dec=0, inc=5)
        lay.AddRow(w.row("Attractors / zone", self._attractors))

        lay.AddRow(w.section("Line weight -- real pipes, visible zoomed out"))
        self._trunk_line = w.num(self.params.trunk_line, 0.15, 3.0, dec=2, inc=0.05)
        lay.AddRow(w.row("Trunk / near-root", self._trunk_line))
        self._spoke_line = w.num(self.params.spoke_line, 0.10, 2.0, dec=2, inc=0.05)
        lay.AddRow(w.row("Fan spokes", self._spoke_line))
        self._wrap_line = w.num(self.params.wrap_line, 0.10, 2.0, dec=2, inc=0.05)
        lay.AddRow(w.row("Wrap + keep-out ring", self._wrap_line))
        self._hair_line = w.num(self.params.hair_line, 0.05, 1.5, dec=2, inc=0.05)
        lay.AddRow(w.row("Organic mid-hair", self._hair_line))

        lay.AddRow(w.section("Text seats -- filled dots, no letters"))
        self._trunk_r = w.num(self.params.trunk_dot_radius, 2.0, 16, dec=1)
        lay.AddRow(w.row("Main-topic seat", self._trunk_r))
        self._tip_r = w.num(self.params.tip_dot_radius, 1.2, 10, dec=1)
        lay.AddRow(w.row("Subtopic seat", self._tip_r))
        self._rel_r = w.num(self.params.rel_dot_radius, 1.0, 10, dec=1)
        lay.AddRow(w.row("Relation diamond", self._rel_r))

        self._btn_generate = w.button("Generate", self._on_generate, width=110, primary=True)
        self._btn_clear = w.button("Clear only", self._on_clear, width=110)
        lay.AddRow(w.button_row(self._btn_generate, self._btn_clear))

        self._log = w.log_area(height=150)
        self.status_cb = make_logger(self._log)
        lay.AddRow(self._log)
        self.Content = lay
        self.status_cb(
            "No letters. Filled seats mark every place to type.\n"
            "Centre + = title. Large discs = main claims.\n"
            "Small discs = subtopics. Grey diamonds = relation verbs.\n"
            "Line weight is a pipe -- it stays visible when you zoom out."
        )

    def _read_params(self):
        p = self.params
        p.seed = int(self._seed.Value)
        p.influence_radius = float(self._influence.Value)
        p.kill_distance = float(self._kill.Value)
        p.segment_length = float(self._segment.Value)
        p.max_iterations = int(self._iterations.Value)
        p.attractors_per_zone = int(self._attractors.Value)
        p.ring_radius = float(self._ring.Value)
        p.title_keepout = float(self._keepout.Value)
        p.outward_bias = float(self._outward.Value)
        p.trunk_dot_radius = float(self._trunk_r.Value)
        p.tip_dot_radius = float(self._tip_r.Value)
        p.rel_dot_radius = float(self._rel_r.Value)
        p.trunk_line = float(self._trunk_line.Value)
        p.spoke_line = float(self._spoke_line.Value)
        p.wrap_line = float(self._wrap_line.Value)
        p.hair_line = float(self._hair_line.Value)
        p.draw_title_circle = bool(self._draw_title.Checked)
        p.draw_wrap_arcs = bool(self._draw_arcs.Checked)
        return p

    def _on_generate(self, sender, e):
        self._btn_generate.Enabled = False
        try:
            generate_diagram(self._read_params(), self.status_cb)
        except Exception:
            self.status_cb("ERROR:\n" + traceback.format_exc())
        finally:
            self._btn_generate.Enabled = True

    def _on_clear(self, sender, e):
        try:
            clear_diagram_layers(self.status_cb)
        except Exception:
            self.status_cb("ERROR:\n" + traceback.format_exc())


def main():
    try:
        form = StigmergyForm()
        form.Owner = Rhino.UI.RhinoEtoApp.MainWindow
        form.Show()
    except Exception:
        print("Stigmergy failed to start:\n" + traceback.format_exc())


if __name__ == "__main__":
    main()
