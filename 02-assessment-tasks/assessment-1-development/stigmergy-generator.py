"""
Assessment 1 stigmergy generator  v0.6
Development copy -- does not overwrite 05-diagrams/assessment-1/stigmergy-generator.py

Rhino 8 Script Editor (Python 3 / CPython). Run to open the control panel.

NO TEXT IS BAKED
----------------
Rhino annotation scale cannot be trusted for readable type. This script
draws coloured geometry only: title seat, thick highways, organic branches,
tip dots, relation paths. Object names (Properties panel) hold catalog IDs.

Place words by hand using:
  stigmergy-guide.html  (zoomable picture / web app)
  stigmergy-text-catalog.md

LAYOUT  v0.6 -- nerve style (not radial / galaxy)
-------------------------------------------------
Distributed hubs on a horizontal canvas (~2:1). Thick bundled highways
between regions; fine capillary branches at organic tips. REGISTRATION
is the largest spine hub (lower-centre). POWER is a smaller overlap hub.
Title sits in the upper void -- not a central ring hole.
"""

import math
import random
import time
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
        self.influence_radius = 18.0
        self.kill_distance = 3.8
        self.segment_length = 2.4
        self.max_iterations = 650
        self.attractors_per_zone = 130
        self.canvas_scale = 1.0
        self.title_y = 72.0
        self.title_keepout = 28.0
        self.grow_bias = 0.55
        self.tip_dot_radius = 3.0
        self.trunk_dot_radius = 6.0
        self.rel_dot_radius = 3.0
        self.highway_line = 1.35
        self.trunk_line = 0.85
        self.branch_line = 0.28
        self.hair_line = 0.10
        self.rel_line = 0.55
        self.draw_title_ellipse = True
        self.draw_highways = True
        self.draw_relations = True
        self.animate = False


ORIGIN = rg.Point3d(0, 0, 0)


def hub_pt(cat, scale):
    x, y = cat["hub"]
    return rg.Point3d(x * scale, y * scale, 0)


def grow_vec(cat):
    gx, gy = cat["grow_dir"]
    v = rg.Vector3d(gx, gy, 0)
    if v.Length > 1e-9:
        v.Unitize()
    return v


# -----------------------------------------------------------------
# Content -- IDs match stigmergy-text-catalog.md
# hub = (x, y) on nerve canvas; grow_dir = attractor / branch bias
# hub_scale: REGISTRATION largest; POWER smaller overlap hub
# -----------------------------------------------------------------
CATEGORIES = [
    {
        "key": "ETHICS",
        "zoom": "Duty past the fee-payer",
        "colour": (176, 106, 122),
        "hub": (-165, 38),
        "grow_dir": (-0.85, 0.35),
        "zone_radius": 36,
        "hub_scale": 1.0,
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
        "hub": (-78, 48),
        "grow_dir": (-0.25, 0.95),
        "zone_radius": 40,
        "hub_scale": 1.05,
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
        "hub": (-52, -52),
        "grow_dir": (-0.35, -0.90),
        "zone_radius": 32,
        "hub_scale": 1.0,
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
        "hub": (-158, -42),
        "grow_dir": (-0.92, -0.25),
        "zone_radius": 28,
        "hub_scale": 1.0,
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
        "hub": (28, -28),
        "grow_dir": (0.15, -0.88),
        "zone_radius": 52,
        "hub_scale": 1.35,
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
        "hub": (-92, -68),
        "grow_dir": (-0.55, -0.80),
        "zone_radius": 30,
        "hub_scale": 1.0,
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
        "hub": (-8, 52),
        "grow_dir": (0.05, 0.98),
        "zone_radius": 30,
        "hub_scale": 1.0,
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
        "hub": (125, 38),
        "grow_dir": (0.90, 0.35),
        "zone_radius": 34,
        "hub_scale": 1.05,
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
        "hub": (62, 8),
        "grow_dir": (0.65, 0.15),
        "zone_radius": 24,
        "hub_scale": 0.72,
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

# Thick bundled highways between hubs (weight multiplier)
HIGHWAYS = [
    ("ETHICS", "LEGISLATION", 1.0),
    ("LEGISLATION", "EDUCATION", 0.95),
    ("LEGISLATION", "REGISTRATION", 1.0),
    ("EDUCATION", "REGISTRATION", 0.92),
    ("REGISTRATION", "EMPLOYMENT", 0.88),
    ("REGISTRATION", "BODIES", 1.0),
    ("RESEARCH", "LEGISLATION", 0.85),
    ("RESEARCH", "REGISTRATION", 0.80),
    ("PROCUREMENT", "EMPLOYMENT", 0.75),
    ("PROCUREMENT", "REGISTRATION", 0.70),
    ("BODIES", "LEGISLATION", 0.78),
    ("POWER", "REGISTRATION", 0.65),
    ("POWER", "LEGISLATION", 0.60),
    ("POWER", "PROCUREMENT", 0.58),
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


def title_center(params):
    return rg.Point3d(0, params.title_y * params.canvas_scale, 0)


def push_outside_title(pt, params):
    center = title_center(params)
    keep = params.title_keepout * params.canvas_scale
    d = pt.DistanceTo(center)
    if d >= keep:
        return pt
    if d < 1e-9:
        return rg.Point3d(center.X, center.Y - keep - 1.0, 0)
    scale = (keep + 1.2) / d
    dx = pt.X - center.X
    dy = pt.Y - center.Y
    return rg.Point3d(center.X + dx * scale, center.Y + dy * scale, 0)


def random_point_in_disc(center, radius):
    r = radius * math.sqrt(random.random())
    a = random.random() * 2.0 * math.pi
    return rg.Point3d(center.X + r * math.cos(a), center.Y + r * math.sin(a), 0)


def random_point_in_zone(root, grow_dir, zone_radius, scale):
    gd = grow_vec({"grow_dir": grow_dir})
    perp = rg.Vector3d(-gd.Y, gd.X, 0)
    # Elliptical cloud: long along grow_dir, wide perpendicular
    along = (random.random() - 0.15) * zone_radius * scale * 1.35
    across = (random.random() - 0.5) * zone_radius * scale * 0.85
    return rg.Point3d(
        root.X + gd.X * along + perp.X * across,
        root.Y + gd.Y * along + perp.Y * across,
        0,
    )


def grow_branches(root_pt, grow_dir, zone_radius, n_attractors, params, scale):
    gd = grow_vec({"grow_dir": grow_dir})
    zone_center = rg.Point3d(
        root_pt.X + gd.X * zone_radius * scale * 0.55,
        root_pt.Y + gd.Y * zone_radius * scale * 0.55,
        0,
    )

    attractors = []
    for _ in range(n_attractors):
        p = random_point_in_zone(root_pt, grow_dir, zone_radius, scale)
        p = push_outside_title(p, params)
        attractors.append(p)

    nodes = [root_pt]
    parent_of = {0: -1}

    for _ in range(int(params.max_iterations)):
        if not attractors:
            break

        node_dir_sum = {}
        node_count = {}

        for a in attractors:
            nearest_i, nearest_d = -1, params.influence_radius * scale
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
            avg = avg + gd * params.grow_bias
            jitter = rg.Vector3d(
                random.uniform(-0.18, 0.18),
                random.uniform(-0.18, 0.18),
                0,
            )
            avg = avg + jitter
            if avg.Length > 1e-9:
                avg.Unitize()
            new_pt = push_outside_title(
                nodes[i] + avg * params.segment_length * scale,
                params,
            )
            nodes.append(new_pt)
            parent_of[len(nodes) - 1] = i

        attractors = [a for a in attractors
                      if all(n.DistanceTo(a) >= params.kill_distance * scale for n in nodes)]

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
    return leaves


def curve_between(p1, p2, bulge_factor=0.22, scale=1.0):
    mid = rg.Point3d(
        (p1.X + p2.X) * 0.5,
        (p1.Y + p2.Y) * 0.5,
        0,
    )
    dx = p2.X - p1.X
    dy = p2.Y - p1.Y
    dist = math.hypot(dx, dy)
    if dist < 1e-9:
        return [p1, p2]
    perp_x = -dy / dist
    perp_y = dx / dist
    bulge = dist * bulge_factor * scale
    # Alternate bulge direction by hash of endpoints for variety
    sign = 1.0 if (hash((round(p1.X, 1), round(p2.X, 1))) % 2) == 0 else -1.0
    ctrl = rg.Point3d(
        mid.X + perp_x * bulge * sign,
        mid.Y + perp_y * bulge * sign,
        0,
    )
    return [p1, ctrl, p2]


def set_print_width(obj_id, width):
    try:
        rs.ObjectPrintWidth(obj_id, width)
    except Exception:
        pass


def name_obj(obj_id, name):
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


def thicken_curve(curve_id, radius, colour, layer, name=None, delete_curve=False):
    if not curve_id:
        return None
    paint(curve_id, colour, layer, name)
    set_print_width(curve_id, max(radius * 2.2, 0.55))
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
        return curve_id
    pipe_layer = ensure_layer("Diagram::Pipes", colour)
    for p in made:
        paint(p, colour, pipe_layer, name)
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


def add_text_seat(pt, colour, layer, name, kind, params, hub_scale=1.0):
    base = params.trunk_dot_radius * params.canvas_scale * hub_scale
    if kind == "title":
        add_filled_disk(pt, base * 0.85, (70, 70, 70), layer, name)
        add_halo(pt, base * 1.35, (90, 90, 90), layer, name)
        s = base * 1.8
        add_thick_line(rg.Point3d(pt.X - s, pt.Y, 0), rg.Point3d(pt.X + s, pt.Y, 0),
                       0.22, (70, 70, 70), layer, name)
        add_thick_line(rg.Point3d(pt.X, pt.Y - s, 0), rg.Point3d(pt.X, pt.Y + s, 0),
                       0.22, (70, 70, 70), layer, name)
        return
    if kind == "main":
        add_filled_disk(pt, base, colour, layer, name)
        add_halo(pt, base * 1.55, colour, layer, name)
        return
    if kind == "rel":
        add_diamond(pt, params.rel_dot_radius * params.canvas_scale, (90, 90, 90), layer, name)
        return
    tip_r = params.tip_dot_radius * params.canvas_scale
    add_filled_disk(pt, tip_r, colour, layer, name)
    add_halo(pt, tip_r * 1.45, colour, layer, name)


def line_weight_for_depth(depth, params):
    if depth <= 2:
        return params.trunk_line
    if depth <= 6:
        return params.branch_line
    return params.hair_line


def maybe_redraw(animate):
    if animate:
        sc.doc.Views.Redraw()
        time.sleep(0.008)


# -----------------------------------------------------------------
# Bake
# -----------------------------------------------------------------
def bake_title(params, status_cb):
    layer = ensure_layer("Diagram::Title", (80, 80, 80))
    rs.CurrentLayer(layer)
    center = title_center(params)
    add_text_seat(center, (70, 70, 70), layer, "TITLE", "title", params)
    if params.draw_title_ellipse:
        rx = params.title_keepout * params.canvas_scale * 1.55
        ry = params.title_keepout * params.canvas_scale * 0.75
        try:
            plane = rg.Plane(center, rg.Vector3d.ZAxis)
            ell = rg.Ellipse(plane, rx, ry)
            crv = ell.ToNurbsCurve()
            cid = rs.AddCurve(crv)
            if cid:
                thicken_curve(cid, params.hair_line, (90, 90, 90), layer, "TITLE")
        except Exception:
            cid = rs.AddCircle(center, params.title_keepout * params.canvas_scale)
            if cid:
                thicken_curve(cid, params.hair_line, (90, 90, 90), layer, "TITLE")
    status_cb("Title seat in upper void -- letter DISCIPLINARY MATRIX here.")


def bake_highways(zone_results, params, animate=False):
    if not params.draw_highways:
        return
    layer = ensure_layer("Diagram::Highways", (100, 100, 100))
    rs.CurrentLayer(layer)
    scale = params.canvas_scale

    for a_key, b_key, weight in HIGHWAYS:
        if a_key not in zone_results or b_key not in zone_results:
            continue
        p1 = zone_results[a_key]["root"]
        p2 = zone_results[b_key]["root"]
        pts = curve_between(p1, p2, bulge_factor=0.18, scale=scale)
        crv = rs.AddInterpCurve(pts, 3)
        if not crv:
            continue
        # Blend colours of the two zones
        c1 = zone_results[a_key]["colour"]
        c2 = zone_results[b_key]["colour"]
        blend = (
            int((c1[0] + c2[0]) * 0.5),
            int((c1[1] + c2[1]) * 0.5),
            int((c1[2] + c2[2]) * 0.5),
        )
        w = params.highway_line * weight * scale
        thicken_curve(crv, w, blend, layer, "{}-{}".format(a_key, b_key))
        maybe_redraw(animate)


def assign_tips_to_subs(root, leaves, nodes, subs, grow_dir):
    """Map catalog sub IDs to organic leaf tips (angle order for stability)."""
    if not subs:
        return []
    gd = grow_vec({"grow_dir": grow_dir})
    perp = rg.Vector3d(-gd.Y, gd.X, 0)

    def sort_key(i):
        tip = nodes[i]
        rel = tip - root
        along = rel.X * gd.X + rel.Y * gd.Y
        across = rel.X * perp.X + rel.Y * perp.Y
        dist = root.DistanceTo(tip)
        return (round(across, 1), -dist, round(along, 1))

    ranked = sorted(leaves, key=sort_key)
    n_need = len(subs)
    if len(ranked) >= n_need:
        chosen = ranked[:n_need]
    else:
        chosen = list(ranked)
        # Extend with synthetic tips along grow direction if growth was sparse
        gd_len = max(root.DistanceTo(nodes[i]) for i in leaves) if leaves else 20.0
        for k in range(n_need - len(ranked)):
            t = (k + 1) / float(n_need + 1)
            along = gd_len * (0.85 + t * 0.45)
            across = (k - n_need * 0.5) * 4.5
            pt_idx = len(nodes) + k
            chosen.append(pt_idx)
            nodes.append(rg.Point3d(
                root.X + gd.X * along + perp.X * across,
                root.Y + gd.Y * along + perp.Y * across,
                0,
            ))
    chosen.sort(key=lambda i: sort_key(i) if i < len(nodes) else (0, 0, 0))
    return [(subs[k][0], nodes[chosen[k]]) for k in range(len(subs))]


def bake_zone(cat, params, animate=False):
    colour = cat["colour"]
    layer = ensure_layer("Diagram::" + cat["key"], colour)
    rs.CurrentLayer(layer)
    scale = params.canvas_scale

    root = hub_pt(cat, scale)
    hub_scale = cat.get("hub_scale", 1.0)

    add_text_seat(root, colour, layer, cat["key"], "main", params, hub_scale)

    nodes, parent_of = grow_branches(
        root, cat["grow_dir"], cat["zone_radius"],
        params.attractors_per_zone, params, scale,
    )

    for i in range(1, len(nodes)):
        if i not in parent_of or parent_of[i] < 0:
            continue
        depth = node_depth(i, parent_of)
        lid = rs.AddLine(nodes[parent_of[i]], nodes[i])
        if not lid:
            continue
        paint(lid, colour, layer, cat["key"])
        w = line_weight_for_depth(depth, params) * scale
        if depth <= 2:
            thicken_curve(lid, w, colour, layer, cat["key"])
        elif depth <= 6:
            thicken_curve(lid, w, colour, layer, cat["key"])
        else:
            thicken_curve(lid, w * 0.65, colour, layer, cat["key"])
        maybe_redraw(animate)

    marker_layer = ensure_layer("Diagram::Markers", colour)
    rs.CurrentLayer(marker_layer)

    leaves = find_leaf_tips(nodes, parent_of)
    tip_assignments = assign_tips_to_subs(root, leaves, nodes, cat["subs"], cat["grow_dir"])

    placed = 0
    for mid, tip in tip_assignments:
        add_text_seat(tip, colour, marker_layer, mid, "sub", params)
        placed += 1
        maybe_redraw(animate)

    return {
        "root": root,
        "colour": colour,
        "placed": placed,
        "hub_scale": hub_scale,
    }


def bake_relations(zone_results, params, status_cb, animate=False):
    if not params.draw_relations:
        return
    layer = ensure_layer("Diagram::Relations", (120, 120, 120))
    rs.CurrentLayer(layer)
    scale = params.canvas_scale

    for a_key, b_key, rid, verb in RELATIONS:
        if a_key not in zone_results or b_key not in zone_results:
            continue
        p1 = zone_results[a_key]["root"]
        p2 = zone_results[b_key]["root"]
        pts = curve_between(p1, p2, bulge_factor=0.32, scale=scale)
        crv = rs.AddInterpCurve(pts, 3)
        if not crv:
            continue
        rel_name = "{} {}".format(rid, verb)
        thicken_curve(crv, params.rel_line * scale * 0.85, (100, 100, 100), layer, rel_name)
        mid = pts[len(pts) // 2]
        add_text_seat(mid, (90, 90, 90), layer, rel_name, "rel", params)
        maybe_redraw(animate)
    status_cb("Relation paths between hubs; grey diamonds are verb seats.")


def generate_diagram(params, status_cb):
    random.seed(params.seed)
    force_annotation_scale_to_one(status_cb)
    clear_diagram_layers(status_cb)

    animate = params.animate
    sc.doc.Views.RedrawEnabled = not animate
    try:
        bake_title(params, status_cb)

        zone_results = {}
        for cat in CATEGORIES:
            result = bake_zone(cat, params, animate)
            zone_results[cat["key"]] = result
            status_cb("{} : {} subtopic seats on organic tips.".format(
                cat["key"], result["placed"]))

        # Highways on top of zone roots but under relation markers
        bake_highways(zone_results, params, animate)
        bake_relations(zone_results, params, status_cb, animate)
    finally:
        sc.doc.Views.RedrawEnabled = True

    rs.ZoomExtents()
    status_cb(
        "Nerve layout v0.6. No ring. Highways + organic capillaries.\n"
        "Letter from stigmergy-guide.html. Hide pipes before vector export."
    )


# -----------------------------------------------------------------
# GUI
# -----------------------------------------------------------------
class StigmergyForm(eforms.Form):

    def __init__(self):
        eforms.Form.__init__(self)
        self.Title = "A1 Stigmergy  v0.6  (nerve layout)"
        self.Resizable = True
        self.ClientSize = edrawing.Size(460, 760)
        self.Padding = edrawing.Padding(8)
        self.BackgroundColor = TH["bg_form"]
        self.params = GrowthParams()
        self._build_ui()

    def _build_ui(self):
        w = Widgets()
        lay = w.layout()

        lay.AddRow(w.section("Layout -- nerve style (horizontal hubs)"))
        self._scale = w.num(self.params.canvas_scale, 0.5, 2.0, dec=2, inc=0.05)
        lay.AddRow(w.row("Canvas scale", self._scale))
        self._title_y = w.num(self.params.title_y, 30, 120, dec=1)
        lay.AddRow(w.row("Title Y (upper void)", self._title_y))
        self._keepout = w.num(self.params.title_keepout, 12, 60, dec=1)
        lay.AddRow(w.row("Title keep-out", self._keepout))
        self._grow_bias = w.num(self.params.grow_bias, 0.0, 1.5, dec=2, inc=0.05)
        lay.AddRow(w.row("Branch direction bias", self._grow_bias))
        self._draw_title = w.check("Draw title keep-out ellipse", True)
        lay.AddRow(self._draw_title)
        self._draw_hw = w.check("Draw bundled highways", True)
        lay.AddRow(self._draw_hw)
        self._draw_rel = w.check("Draw relation paths", True)
        lay.AddRow(self._draw_rel)
        self._animate = w.check("Animate while generating", False)
        lay.AddRow(self._animate)

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
        self._highway = w.num(self.params.highway_line, 0.3, 4.0, dec=2, inc=0.05)
        lay.AddRow(w.row("Highway trunks", self._highway))
        self._trunk_line = w.num(self.params.trunk_line, 0.15, 3.0, dec=2, inc=0.05)
        lay.AddRow(w.row("Near-root branches", self._trunk_line))
        self._branch_line = w.num(self.params.branch_line, 0.05, 2.0, dec=2, inc=0.05)
        lay.AddRow(w.row("Mid branches", self._branch_line))
        self._hair_line = w.num(self.params.hair_line, 0.02, 1.5, dec=2, inc=0.05)
        lay.AddRow(w.row("Terminal capillaries", self._hair_line))
        self._rel_line = w.num(self.params.rel_line, 0.10, 2.0, dec=2, inc=0.05)
        lay.AddRow(w.row("Relation paths", self._rel_line))

        lay.AddRow(w.section("Text seats -- filled dots, no letters"))
        self._trunk_r = w.num(self.params.trunk_dot_radius, 2.0, 16, dec=1)
        lay.AddRow(w.row("Main-topic seat", self._trunk_r))
        self._tip_r = w.num(self.params.tip_dot_radius, 1.2, 10, dec=1)
        lay.AddRow(w.row("Subtopic seat", self._tip_r))
        self._rel_r = w.num(self.params.rel_dot_radius, 1.0, 10, dec=1)
        lay.AddRow(w.row("Relation diamond", self._rel_r))

        self._btn_generate = w.button("Generate", self._on_generate, width=110, primary=True)
        self._btn_clear = w.button("Clear only", self._on_clear, width=110)
        self._btn_vector = w.button("Hide pipes (vector)", self._on_hide_pipes, width=130)
        self._btn_pipes = w.button("Show pipes", self._on_show_pipes, width=100)
        lay.AddRow(w.button_row(self._btn_generate, self._btn_clear))
        lay.AddRow(w.button_row(self._btn_vector, self._btn_pipes))

        self._log = w.log_area(height=140)
        self.status_cb = make_logger(self._log)
        lay.AddRow(self._log)
        self.Content = lay
        self.status_cb(
            "Nerve layout -- no central ring.\n"
            "Gold REGISTRATION = largest spine hub (lower-centre).\n"
            "Terracotta POWER = smaller overlap hub.\n"
            "Subtopic dots sit on organic branch tips, not fan spokes."
        )

    def _read_params(self):
        p = self.params
        p.seed = int(self._seed.Value)
        p.influence_radius = float(self._influence.Value)
        p.kill_distance = float(self._kill.Value)
        p.segment_length = float(self._segment.Value)
        p.max_iterations = int(self._iterations.Value)
        p.attractors_per_zone = int(self._attractors.Value)
        p.canvas_scale = float(self._scale.Value)
        p.title_y = float(self._title_y.Value)
        p.title_keepout = float(self._keepout.Value)
        p.grow_bias = float(self._grow_bias.Value)
        p.trunk_dot_radius = float(self._trunk_r.Value)
        p.tip_dot_radius = float(self._tip_r.Value)
        p.rel_dot_radius = float(self._rel_r.Value)
        p.highway_line = float(self._highway.Value)
        p.trunk_line = float(self._trunk_line.Value)
        p.branch_line = float(self._branch_line.Value)
        p.hair_line = float(self._hair_line.Value)
        p.rel_line = float(self._rel_line.Value)
        p.draw_title_ellipse = bool(self._draw_title.Checked)
        p.draw_highways = bool(self._draw_hw.Checked)
        p.draw_relations = bool(self._draw_rel.Checked)
        p.animate = bool(self._animate.Checked)
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

    def _on_hide_pipes(self, sender, e):
        try:
            if rs.IsLayer("Diagram::Pipes"):
                rs.LayerVisible("Diagram::Pipes", False)
            self.status_cb("Pipes hidden. Export centreline curves as Vector PDF/AI/SVG.")
        except Exception:
            self.status_cb("ERROR:\n" + traceback.format_exc())

    def _on_show_pipes(self, sender, e):
        try:
            if rs.IsLayer("Diagram::Pipes"):
                rs.LayerVisible("Diagram::Pipes", True)
            self.status_cb("Pipes visible again (screen weight).")
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
