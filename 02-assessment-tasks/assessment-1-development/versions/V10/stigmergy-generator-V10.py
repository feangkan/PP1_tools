"""
Assessment 1 stigmergy generator  V10 / v1.3
Development copy -- does not overwrite 05-diagrams/assessment-1/stigmergy-generator.py

Rhino 8 Script Editor (Python 3 / CPython). Run to open the control panel.

Futura catalog text is baked at print pt sizes (GUI). Annotation scale
is forced to 1:1. Hide Diagram::Text / Diagram::Legend if type is too big.

LAYOUT  v1.3 -- mycelial / nerve mesh (fast + animated)
------------------------------------------------------------
Group linkages are dense stigmergy *lines* (bundles of organic strands),
not pipe polysurfaces. Gold REGISTRATION trunk is Victoria's linear gated
pathway. Other colour groups keep their own graphic language.
Legend uses colour circles, not the words Gold / Green / Tan.
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

    def textbox(self, value, width=140):
        tb = eforms.TextBox()
        tb.Text = value
        tb.Width = width
        tb.BackgroundColor = TH["bg_ctrl"]
        tb.TextColor = TH["fg_bright"]
        return tb


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
        self.influence_radius = 17.0
        self.kill_distance = 3.2
        self.segment_length = 2.0
        self.max_iterations = 480
        self.attractors_per_zone = 90
        self.canvas_scale = 1.0
        self.title_y = 72.0
        self.title_keepout = 28.0
        self.grow_bias = 0.50
        self.density_pull = 0.30
        self.tip_dot_radius = 3.0
        self.trunk_dot_radius = 6.0
        self.rel_dot_radius = 3.0
        self.junction_radius = 2.2
        self.highway_line = 1.45
        self.highway_strands = 26
        self.trunk_line = 0.90
        self.branch_line = 0.26
        self.hair_line = 0.08
        self.rel_line = 0.50
        self.mesh_link_dist = 42.0
        self.mesh_sample = 45
        self.capillary_hairs = 24
        self.bridges_per_pair = 7
        self.bridge_range = 150.0
        self.draw_title_ellipse = True
        self.draw_highways = True
        self.draw_highway_filaments = True
        self.draw_mesh_links = True
        self.draw_nerve_bridges = False
        self.draw_capillaries = True
        self.draw_junctions = False
        self.draw_relations = True
        self.draw_loops = True
        self.draw_text = True
        self.draw_legend = True
        self.font_name = "Futura"
        self.title_pt = 2.5
        self.heading_pt = 2.5
        self.subtopic_pt = 1.5
        self.branch_pt = 0.5
        self.legend_pt = 1.0
        self.text_scale = 1.0
        self.fast_mode = True
        self.use_pipes = False
        self.bake_pipes_at_end = False
        self.animate = True
        self.animate_batch = 28
        self.animate_delay = 0.012


class AnimateContext(object):
    """Batch redraws so animation stays smooth and fast."""

    def __init__(self, enabled, batch_size=28, delay=0.012):
        self.enabled = bool(enabled)
        self.batch_size = max(1, int(batch_size))
        self.delay = float(delay)
        self._count = 0

    def tick(self, force=False):
        if not self.enabled and not force:
            return
        if force:
            sc.doc.Views.Redraw()
            self._pump_ui()
            return
        self._count += 1
        if self._count >= self.batch_size:
            self._count = 0
            sc.doc.Views.Redraw()
            if self.delay > 0:
                time.sleep(self.delay)
            self._pump_ui()

    @staticmethod
    def _pump_ui():
        try:
            eforms.Application.Instance.RunIteration()
        except Exception:
            pass


class BakeState(object):
    """Shared bake flags -- skip per-segment pipes during fast/animated draw."""

    skip_pipes = True
    use_pipes = False
    pending_pipes = []
    anim = None

    @classmethod
    def reset(cls, params):
        cls.use_pipes = bool(getattr(params, "use_pipes", False))
        cls.skip_pipes = (not cls.use_pipes) or bool(params.fast_mode)
        cls.pending_pipes = []
        cls.anim = AnimateContext(
            params.animate, params.animate_batch, params.animate_delay,
        )

    @classmethod
    def queue_pipe(cls, curve_id, radius, colour, layer, name, kind="branch"):
        if curve_id and cls.skip_pipes:
            cls.pending_pipes.append((curve_id, radius, colour, layer, name, kind))

    @classmethod
    def flush_pipes(cls, status_cb, trunks_only=False):
        if not cls.pending_pipes:
            if status_cb:
                status_cb("No pipes queued. Generate first, or pipes already baked.")
            return 0
        made = 0
        pipe_layer = ensure_layer("Diagram::Pipes", (120, 120, 120))
        keep = []
        for curve_id, radius, colour, layer, name, kind in cls.pending_pipes:
            if trunks_only and kind not in ("trunk", "highway", "relation"):
                keep.append((curve_id, radius, colour, layer, name, kind))
                continue
            try:
                pipes = rs.AddPipe(curve_id, [0.0, 1.0], [radius, radius], 0, 1)
            except Exception:
                try:
                    pipes = rs.AddPipe(curve_id, 0, radius)
                except Exception:
                    pipes = None
            for p in _as_list(pipes):
                paint(p, colour, pipe_layer, name)
                made += 1
            if cls.anim:
                cls.anim.tick()
        cls.pending_pipes = keep if trunks_only else []
        if status_cb and made:
            scope = "trunks + highways" if trunks_only else "all queued"
            status_cb("Baked {} screen pipes ({}).".format(made, scope))
        return made


PT_MM = 0.352778

FUTURA_CANDIDATES = [
    "Futura",
    "Futura Medium",
    "Futura Std Medium",
    "Futura PT Medium",
    "FuturaBT-Medium",
    "Futura Std",
    "Century Gothic",
    "Arial",
]


def resolve_font(preferred):
    names = []
    try:
        names = list(Rhino.DocObjects.Font.AvailableFontFaceNames())
    except Exception:
        try:
            names = list(rs.FontNames() or [])
        except Exception:
            names = []
    lower = {n.lower(): n for n in names}
    for cand in [preferred] + FUTURA_CANDIDATES:
        if not cand:
            continue
        if cand.lower() in lower:
            return lower[cand.lower()]
        for n in names:
            if cand.lower() in n.lower():
                return n
    return preferred or "Arial"


def pt_to_mm(pt_size, params):
    return max(float(pt_size) * PT_MM * float(params.text_scale), 0.05)


def add_label(pt, text, pt_size, colour, layer, name, params, justify=2):
    """Annotation-scale-safe text. Height is pt converted to mm * text_scale."""
    if not text or not params.draw_text:
        return None
    height = pt_to_mm(pt_size, params)
    font = resolve_font(params.font_name)
    plane = rg.Plane(pt, rg.Vector3d.ZAxis)
    tid = None
    try:
        tid = rs.AddText(str(text), plane, height, font, 0, justify)
    except Exception:
        try:
            tid = rs.AddText(str(text), pt, height, font)
        except Exception:
            tid = rs.AddText(str(text), pt, height)
    if not tid:
        return None
    paint(tid, colour, layer, name)
    try:
        rs.TextObjectFont(tid, font)
        rs.TextObjectHeight(tid, height)
    except Exception:
        pass
    return tid


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
        "logic": "cycle: knowledge → power → public → knowledge",
        "colour": (176, 106, 122),
        "hub": (-165, 38),
        "grow_dir": (-0.85, 0.35),
        "zone_radius": 36,
        "hub_scale": 1.0,
        "legend": "duty past the fee-payer",
        "subs": [
            ("H1", "Knowledge becomes power"),
            ("H2", "Ethics answers that power"),
            ("H3", "Client not in the room"),
            ("H4", "Profession is not a business"),
            ("H5", "Fees do not shrink judgment"),
            ("H6", "No good or bad architects — only degree"),
            ("H7", "Searchlight or lantern"),
            ("H8", "Collective test"),
        ],
    },
    {
        "key": "LEGISLATION",
        "zoom": "The Act and the NCC can be rewritten",
        "logic": "instrument: write / interpret / amend",
        "colour": (91, 124, 153),
        "hub": (-78, 48),
        "grow_dir": (-0.25, 0.95),
        "zone_radius": 40,
        "hub_scale": 1.05,
        "legend": "Act and NCC can be rewritten",
        "subs": [
            ("L1", "Act gives legal form"),
            ("L2", "Who may use the title"),
            ("L3", "Cannot sign undone work"),
            ("L4", "Resign rather than breach"),
            ("L5", "Fire-isolated stair — public over payer"),
            ("L6", "NCC class and type"),
            ("L7", "Professional vs prohibited courts"),
            ("L8", "Written → interpreted → amended"),
            ("L9", "Subject, interpreter, co-author"),
            ("L10", "RIBA was not a licence"),
            ("L11", "Victoria public register 1922/23"),
            ("L12", "London 1666 — same instrument logic"),
        ],
    },
    {
        "key": "RESEARCH",
        "zoom": "Codes change what may be built",
        "logic": "contest: who may rewrite the code",
        "colour": (77, 143, 106),
        "hub": (-52, -52),
        "grow_dir": (-0.35, -0.90),
        "zone_radius": 32,
        "hub_scale": 1.0,
        "legend": "codes change what may be built",
        "subs": [
            ("N1", "Fit for purpose, then performance"),
            ("N2", "Codes are co-authored"),
            ("N3", "Bathrooms into the NCC"),
            ("N4", "Carbon written as a limit"),
            ("N5", "Optional becomes ordinary"),
            ("N6", "One good makes another problem"),
        ],
    },
    {
        "key": "PROCUREMENT",
        "zoom": "Contract can strip design control",
        "logic": "fork: three contracts, authorship optional",
        "colour": (52, 80, 112),
        "hub": (-158, -42),
        "grow_dir": (-0.92, -0.25),
        "zone_radius": 28,
        "hub_scale": 1.0,
        "legend": "contract can strip design control",
        "subs": [
            ("P1", "Traditional AS4000 — keep design"),
            ("P2", "Design and construct AS4902"),
            ("P3", "Novated D and C"),
            ("P4", "Institute survey 2019"),
            ("P5", "Title intact, authorship gone"),
        ],
    },
    {
        "key": "REGISTRATION",
        "zoom": "Victoria's path to architect [linear, gated]",
        "logic": "pathway: gated stages + fail loop + ejection",
        "colour": (201, 162, 39),
        "hub": (28, -28),
        "grow_dir": (0.15, -0.88),
        "zone_radius": 52,
        "hub_scale": 1.35,
        "legend": "the one compulsory gate",
        "subs": [
            ("R1", "TRUST: Autonomy · Discretion · Accountability"),
            ("R2", "RISK: owed to the PUBLIC and the PROFESSION"),
            ("R3", "START"),
            ("R4", "Stage 1: Accredited education (AQF Part 1/2)"),
            ("R5", "Stage 2: Supervised experience — logbook, 3,300 hrs / 35 competencies"),
            ("R6", "Stage 3: APE — National Exam (80 MCQ) + interview (45–60 min, probes gaps)"),
            ("R7", "Fail / re-queue: exam, hours, mutual recognition — sent back, not ejected"),
            ("R8", "Re-attempt"),
            ("R9", "Stage 4: ARBV registration granted"),
            ("R10", "Stage 5: CPD + PI insurance — the ride never fully ends, it loops"),
            ("R11", "causes, on serious breach"),
            ("R12", "Ejected from the park: Tribunal finding, discipline register, loss of title"),
        ],
    },
    {
        "key": "EMPLOYMENT",
        "zoom": "A project is a loop; career hours are a different line",
        "logic": "loop: brief → design → CA, Council/BS fire, findings return",
        "colour": (166, 138, 91),
        "hub": (-92, -68),
        "grow_dir": (-0.55, -0.80),
        "zone_radius": 32,
        "hub_scale": 1.0,
        "legend": "hours in practice; project is a loop",
        "subs": [
            ("W1", "Client + stakeholders write the brief"),
            ("W2", "F → SK → DD"),
            ("W3", "CD → CA"),
            ("W4", "Town Planning (Council)"),
            ("W5", "Building Surveyor"),
            ("W6", "Findings return to the brief"),
            ("W7", "Firm is where logbook hours live"),
            ("W8", "NSCA spans design and CA"),
        ],
    },
    {
        "key": "EDUCATION",
        "zoom": "Judgment trained, then kept alive",
        "logic": "formative cycle — not a one-off stamp",
        "colour": (107, 155, 107),
        "hub": (-8, 52),
        "grow_dir": (0.05, 0.98),
        "zone_radius": 30,
        "hub_scale": 1.0,
        "legend": "judgment trained, then kept alive",
        "subs": [
            ("E1", "University under AQF"),
            ("E2", "Judgment over competency"),
            ("E3", "Integrity: head · heart · hand"),
            ("E4", "CPD is formative"),
            ("E5", "Knowledge should be collective"),
            ("E6", "Classic or neo-profession"),
        ],
    },
    {
        "key": "BODIES",
        "zoom": "Institute advances; Board accounts",
        "logic": "split + network: voluntary / statutory / recognition",
        "colour": (138, 107, 168),
        "hub": (125, 38),
        "grow_dir": (0.90, 0.35),
        "zone_radius": 34,
        "hub_scale": 1.05,
        "legend": "Institute advances; Board accounts",
        "subs": [
            ("B1", "AIA is voluntary"),
            ("B2", "ARBV is statutory"),
            ("B3", "AACA sets the national test"),
            ("B4", "Network filling AIA gaps"),
            ("B5", "Fragmentation is the problem"),
            ("B6", "Awards write 'good'"),
            ("B7", "Outside juries disagree"),
            ("B8", "Six media channels"),
        ],
    },
    {
        "key": "POWER",
        "zoom": "Tight title, loose code and contract",
        "logic": "overlap: smaller hub across the other clusters",
        "colour": (176, 80, 64),
        "hub": (62, 8),
        "grow_dir": (0.65, 0.15),
        "zone_radius": 24,
        "hub_scale": 0.72,
        "legend": "tight title, loose code and contract",
        "subs": [
            ("K1", "Interlocking seats"),
            ("K2", "Influence sits in relations"),
            ("K3", "Tight title, loose instrument"),
            ("K4", "Crisis without revolution"),
            ("K5", "Institution versus the public"),
            ("K6", "Who writes rules / keeps authorship"),
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

# Dotted intra-group rides (fail / re-attempt / loop / ejection analog).
# Same grammar as the gold pathway picture: sent back is not ejected.
INTRA_LOOPS = [
    # Real contingencies on the gold pathway
    ("REGISTRATION", "R6", "R7", "Fail"),
    ("REGISTRATION", "R7", "R8", "Re-queue"),
    ("REGISTRATION", "R8", "R6", "Re-attempt"),
    ("REGISTRATION", "R10", "R11", "causes, on serious breach"),
    ("REGISTRATION", "R12", "R4", "back toward Stage 1"),
    # Tutorial project loop (employment actually has stages)
    ("EMPLOYMENT", "W4", "W6", "Council findings"),
    ("EMPLOYMENT", "W5", "W6", "Surveyor findings"),
    ("EMPLOYMENT", "W6", "W1", "return to brief"),
    # Ethics is a cycle, not a pathway
    ("ETHICS", "H8", "H1", "feeds back"),
    # Education keeps judgment alive after the stamp
    ("EDUCATION", "E4", "E2", "formative"),
    # Research: a new rule answers the last rule
    ("RESEARCH", "N6", "N2", "new rule answers last"),
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


def spine_center(params):
    """Dense core anchor -- REGISTRATION hub."""
    return hub_pt({"hub": (28, -28)}, params.canvas_scale)


def neighbor_hub_pts(cat, scale, n=4):
    mine = hub_pt(cat, scale)
    others = []
    for other in CATEGORIES:
        if other["key"] == cat["key"]:
            continue
        p = hub_pt(other, scale)
        others.append((mine.DistanceTo(p), p))
    others.sort(key=lambda t: t[0])
    return [p for _, p in others[:n]]


def random_point_in_zone(root, grow_dir, zone_radius, scale, params=None, neighbors=None):
    gd = grow_vec({"grow_dir": grow_dir})
    perp = rg.Vector3d(-gd.Y, gd.X, 0)

    # Pull some attractors toward neighbouring hubs so branches reach other groups
    if neighbors and random.random() < 0.42:
        target = neighbors[random.randrange(len(neighbors))]
        t = random.uniform(0.25, 0.82)
        spread = zone_radius * scale * 0.40 * (random.random() - 0.5)
        return rg.Point3d(
            root.X + (target.X - root.X) * t + perp.X * spread,
            root.Y + (target.Y - root.Y) * t + perp.Y * spread,
            0,
        )

    if params and params.density_pull > 0 and random.random() < params.density_pull:
        core = spine_center(params)
        t = random.random() * 0.55 + 0.15
        spread = zone_radius * scale * 0.35 * (random.random() - 0.5)
        return rg.Point3d(
            root.X + (core.X - root.X) * t + perp.X * spread,
            root.Y + (core.Y - root.Y) * t + perp.Y * spread,
            0,
        )

    along = (random.random() - 0.15) * zone_radius * scale * 1.35
    across = (random.random() - 0.5) * zone_radius * scale * 0.85
    return rg.Point3d(
        root.X + gd.X * along + perp.X * across,
        root.Y + gd.Y * along + perp.Y * across,
        0,
    )


def grow_branches(root_pt, grow_dir, zone_radius, n_attractors, params, scale, neighbors=None):
    gd = grow_vec({"grow_dir": grow_dir})
    influence = params.influence_radius * scale
    kill = params.kill_distance * scale
    seg_len = params.segment_length * scale
    node_window = 140

    attractors = []
    for _ in range(n_attractors):
        p = random_point_in_zone(root_pt, grow_dir, zone_radius, scale, params, neighbors)
        p = push_outside_title(p, params)
        attractors.append(p)

    nodes = [root_pt]
    parent_of = {0: -1}

    def nearest_node_index(target):
        best_i, best_d = -1, influence
        n_nodes = len(nodes)
        start = max(0, n_nodes - node_window)
        for i in range(n_nodes - 1, start - 1, -1):
            d = nodes[i].DistanceTo(target)
            if d < best_d:
                best_d, best_i = d, i
        if best_i >= 0:
            return best_i
        for i in range(start - 1, -1, -1):
            d = nodes[i].DistanceTo(target)
            if d < best_d:
                best_d, best_i = d, i
        return best_i

    for _ in range(int(params.max_iterations)):
        if not attractors:
            break

        node_dir_sum = {}
        node_count = {}

        for a in attractors:
            nearest_i = nearest_node_index(a)
            if nearest_i >= 0:
                v = a - nodes[nearest_i]
                if v.Length > 1e-9:
                    v.Unitize()
                    node_dir_sum[nearest_i] = node_dir_sum.get(
                        nearest_i, rg.Vector3d(0, 0, 0),
                    ) + v
                    node_count[nearest_i] = node_count.get(nearest_i, 0) + 1

        if not node_dir_sum:
            break

        for i, vsum in node_dir_sum.items():
            avg = vsum / node_count[i]
            avg = avg + gd * params.grow_bias
            jitter = rg.Vector3d(
                random.uniform(-0.22, 0.22),
                random.uniform(-0.22, 0.22),
                0,
            )
            avg = avg + jitter
            if avg.Length > 1e-9:
                avg.Unitize()
            new_pt = push_outside_title(nodes[i] + avg * seg_len, params)
            nodes.append(new_pt)
            parent_of[len(nodes) - 1] = i

        if kill > 0:
            kd2 = kill * kill
            alive = []
            for a in attractors:
                ax, ay = a.X, a.Y
                ok = True
                for n in nodes[-min(len(nodes), 80):]:
                    dx = n.X - ax
                    dy = n.Y - ay
                    if dx * dx + dy * dy < kd2:
                        ok = False
                        break
                if ok:
                    alive.append(a)
            attractors = alive

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


def ensure_dash_linetype():
    name = "DiagramDash"
    try:
        if rs.IsLinetype(name):
            return name
    except Exception:
        pass
    try:
        rs.AddLinetype(name, [3.5, 1.8])
        return name
    except Exception:
        pass
    for fallback in ("Dashed", "Hidden", "Dash"):
        try:
            if rs.IsLinetype(fallback):
                return fallback
        except Exception:
            continue
    return None


def set_dashed(obj_id):
    if not obj_id:
        return
    lt = ensure_dash_linetype()
    if not lt:
        return
    try:
        rs.ObjectLinetype(obj_id, lt)
    except Exception:
        pass


def tip_point(zone, mid):
    for item_id, _short, pt in zone.get("tips", []):
        if item_id == mid:
            return pt
    return None


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


def thicken_curve(curve_id, radius, colour, layer, name=None, delete_curve=False, pipe_kind="branch"):
    """Stroke a curve. Pipes (polysurfaces) are optional and off by default."""
    if not curve_id:
        return None
    paint(curve_id, colour, layer, name)
    set_print_width(curve_id, max(radius * 2.2, 0.35))
    if not getattr(BakeState, "use_pipes", False):
        return curve_id
    if BakeState.skip_pipes:
        BakeState.queue_pipe(curve_id, radius, colour, layer, name, pipe_kind)
        if delete_curve:
            pass  # keep centerline for vector export
        return curve_id
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
    if not BakeState.skip_pipes:
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


def anim_tick():
    if BakeState.anim:
        BakeState.anim.tick()


def draw_segment(p1, p2, radius, colour, layer, name, pipe_kind="branch"):
    lid = rs.AddLine(p1, p2)
    if not lid:
        return None
    paint(lid, colour, layer, name)
    if radius > 0.04:
        thicken_curve(lid, radius, colour, layer, name, pipe_kind=pipe_kind)
    else:
        set_print_width(lid, max(radius * 2.0, 0.2))
    anim_tick()
    return lid


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
    anim_tick()
    status_cb("Title seat in upper void -- letter DISCIPLINARY MATRIX here.")


def sample_curve_points(p1, p2, n_samples, bulge=0.18, scale=1.0):
    pts = curve_between(p1, p2, bulge_factor=bulge, scale=scale)
    if len(pts) == 3:
        # quadratic bezier samples
        a, c, b = pts[0], pts[1], pts[2]
        out = []
        for i in range(n_samples):
            t = i / float(max(n_samples - 1, 1))
            u = 1.0 - t
            x = u * u * a.X + 2 * u * t * c.X + t * t * b.X
            y = u * u * a.Y + 2 * u * t * c.Y + t * t * b.Y
            out.append(rg.Point3d(x, y, 0))
        return out
    return [p1, p2]


def bake_highway_filaments(zone_results, params):
    if not params.draw_highway_filaments:
        return 0
    layer = ensure_layer("Diagram::Filaments", (110, 110, 110))
    rs.CurrentLayer(layer)
    scale = params.canvas_scale
    count = 0
    for a_key, b_key, weight in HIGHWAYS:
        if a_key not in zone_results or b_key not in zone_results:
            continue
        p1 = zone_results[a_key]["root"]
        p2 = zone_results[b_key]["root"]
        samples = sample_curve_points(p1, p2, 9, bulge=0.18, scale=scale)
        c1 = zone_results[a_key]["colour"]
        c2 = zone_results[b_key]["colour"]
        blend = (
            int((c1[0] + c2[0]) * 0.5),
            int((c1[1] + c2[1]) * 0.5),
            int((c1[2] + c2[2]) * 0.5),
        )
        for sp in samples[1:-1]:
            ang = random.random() * 2.0 * math.pi
            length = random.uniform(3.0, 8.0) * scale
            tip = push_outside_title(
                rg.Point3d(sp.X + math.cos(ang) * length, sp.Y + math.sin(ang) * length, 0),
                params,
            )
            w = params.hair_line * scale * random.uniform(0.6, 1.0)
            draw_segment(sp, tip, w, blend, layer, "filament", "hair")
            count += 1
    return count


def _mesh_sample_indices(zd, max_count):
    cands = [i for i in range(len(zd["nodes"]))
             if i > 0 and zd["depths"].get(i, 0) >= 3]
    if len(cands) <= max_count:
        return cands
    random.shuffle(cands)
    return cands[:max_count]


def organic_walk(p1, p2, steps, params, scale):
    pts = [p1]
    steps = max(4, int(steps))
    for i in range(1, steps):
        t = i / float(steps)
        mx = p1.X + (p2.X - p1.X) * t
        my = p1.Y + (p2.Y - p1.Y) * t
        jitter = 5.5 * scale * (0.35 + math.sin(t * math.pi))
        mx += random.uniform(-jitter, jitter)
        my += random.uniform(-jitter, jitter)
        pts.append(push_outside_title(rg.Point3d(mx, my, 0), params))
    pts.append(p2)
    return pts


def offset_walk(pts, lateral):
    """Pin ends; bow the middle sideways so strands form a dense bundle."""
    n = len(pts)
    if n < 3 or abs(lateral) < 1e-9:
        return pts
    out = []
    for i, p in enumerate(pts):
        if i == 0 or i == n - 1:
            out.append(p)
            continue
        prev = pts[i - 1]
        nxt = pts[min(i + 1, n - 1)]
        tx = nxt.X - prev.X
        ty = nxt.Y - prev.Y
        length = math.hypot(tx, ty) or 1.0
        env = math.sin(i / float(n - 1) * math.pi)
        out.append(rg.Point3d(
            p.X + (-ty / length) * lateral * env,
            p.Y + (tx / length) * lateral * env,
            0,
        ))
    return out


def add_stigmergy_strand(pts, print_w, colour, layer, name):
    if not pts or len(pts) < 2:
        return None
    crv = rs.AddInterpCurve(pts, 3)
    if not crv:
        crv = rs.AddPolyline(pts)
    if not crv:
        return None
    paint(crv, colour, layer, name)
    set_print_width(crv, max(print_w, 0.12))
    return crv


def _mid_branch_indices(zd, min_depth=3):
    return [i for i in range(len(zd["nodes"]))
            if i > 0 and zd["depths"].get(i, 0) >= min_depth]


def bake_nerve_bridges(all_zones, params):
    """Sub-links between groups -- like nerve anastomoses, not isolated islands."""
    if not params.draw_nerve_bridges:
        return 0
    layer = ensure_layer("Diagram::NerveBridges", (110, 110, 110))
    rs.CurrentLayer(layer)
    scale = params.canvas_scale
    max_hub = params.bridge_range * scale
    n_each = max(2, int(params.bridges_per_pair))

    pairs = []
    seen = set()
    for a_key, b_key, _w in HIGHWAYS:
        tag = tuple(sorted((a_key, b_key)))
        if tag not in seen and a_key in all_zones and b_key in all_zones:
            seen.add(tag)
            pairs.append((a_key, b_key))
    keys = list(all_zones.keys())
    for i, ka in enumerate(keys):
        for kb in keys[i + 1:]:
            tag = tuple(sorted((ka, kb)))
            if tag in seen:
                continue
            d = all_zones[ka]["root"].DistanceTo(all_zones[kb]["root"])
            if d <= max_hub:
                seen.add(tag)
                pairs.append((ka, kb))

    count = 0
    for ka, kb in pairs:
        za, zb = all_zones[ka], all_zones[kb]
        ia_list = _mid_branch_indices(za)
        ib_list = _mid_branch_indices(zb)
        if not ia_list or not ib_list:
            continue
        random.shuffle(ia_list)
        random.shuffle(ib_list)
        for k in range(n_each):
            ia = ia_list[k % len(ia_list)]
            ib = ib_list[k % len(ib_list)]
            pa, pb = za["nodes"][ia], zb["nodes"][ib]
            walk = organic_walk(pa, pb, random.randint(5, 8), params, scale)
            for s in range(len(walk) - 1):
                t = s / float(max(len(walk) - 2, 1))
                col = za["colour"] if t < 0.5 else zb["colour"]
                w = (params.branch_line * (1.15 - t * 0.7)) * scale
                draw_segment(walk[s], walk[s + 1], w, col, layer, "{}-{}".format(ka, kb), "branch")
                count += 1
            za["junctions"][ia] = za["junctions"].get(ia, 0) + 1
            zb["junctions"][ib] = zb["junctions"].get(ib, 0) + 1
    return count


def bake_mesh_links(all_zones, params):
    """Cross-link nearby branches -- sampled nodes for speed."""
    if not params.draw_mesh_links:
        return 0
    layer = ensure_layer("Diagram::Mesh", (100, 100, 100))
    rs.CurrentLayer(layer)
    scale = params.canvas_scale
    max_d = params.mesh_link_dist * scale
    max_d2 = max_d * max_d
    min_d2 = (1.5 * scale) ** 2
    sample_n = int(params.mesh_sample)
    links = 0
    keys = list(all_zones.keys())
    sampled = {k: _mesh_sample_indices(all_zones[k], sample_n) for k in keys}
    for i, ka in enumerate(keys):
        za = all_zones[ka]
        for kb in keys[i + 1:]:
            zb = all_zones[kb]
            for ia in sampled[ka]:
                pa = za["nodes"][ia]
                for ib in sampled[kb]:
                    pb = zb["nodes"][ib]
                    dx = pa.X - pb.X
                    dy = pa.Y - pb.Y
                    d2 = dx * dx + dy * dy
                    if d2 > max_d2 or d2 < min_d2:
                        continue
                    if random.random() > 0.55:
                        continue
                    c1, c2 = za["colour"], zb["colour"]
                    blend = (
                        int((c1[0] + c2[0]) * 0.5),
                        int((c1[1] + c2[1]) * 0.5),
                        int((c1[2] + c2[2]) * 0.5),
                    )
                    w = params.hair_line * scale * 1.3
                    draw_segment(pa, pb, w, blend, layer, "mesh", "hair")
                    za["junctions"][ia] = za["junctions"].get(ia, 0) + 1
                    zb["junctions"][ib] = zb["junctions"].get(ib, 0) + 1
                    links += 1
    return links


def bake_capillaries(all_zones, params):
    """Fine reaching hairs from mid-branch and tip nodes (mycelial edge)."""
    if not params.draw_capillaries:
        return 0
    count = 0
    scale = params.canvas_scale
    for key, zd in all_zones.items():
        layer = ensure_layer("Diagram::" + key, zd["colour"])
        rs.CurrentLayer(layer)
        colour = zd["colour"]
        nodes = zd["nodes"]
        n_hairs = int(params.capillary_hairs * max(scale, 0.85))
        candidates = [i for i in range(len(nodes))
                      if zd["depths"].get(i, 0) >= 4]
        if not candidates:
            continue
        random.shuffle(candidates)
        foreign = []
        for other_key, other in all_zones.items():
            if other_key == key:
                continue
            foreign.extend(other["nodes"][1:min(len(other["nodes"]), 40)])
        for idx in candidates[:n_hairs]:
            base = nodes[idx]
            if foreign and random.random() < 0.65:
                target = min(foreign, key=lambda p: base.DistanceTo(p))
                direction = target - base
            else:
                direction = rg.Vector3d(
                    random.uniform(-1, 1),
                    random.uniform(-1, 1),
                    0,
                )
            if direction.Length > 1e-9:
                direction.Unitize()
            steps = random.randint(2, 4)
            prev = base
            for s in range(steps):
                reach = params.segment_length * scale * random.uniform(0.7, 1.2)
                nudge = rg.Vector3d(
                    random.uniform(-0.35, 0.35),
                    random.uniform(-0.35, 0.35),
                    0,
                )
                nxt = push_outside_title(prev + direction * reach + nudge, params)
                w = params.hair_line * scale * (0.5 + s * 0.15)
                draw_segment(prev, nxt, w, colour, layer, key, "hair")
                prev = nxt
                count += 1
    return count


def bake_junction_nodes(all_zones, params):
    """Thickened nodes where multiple filaments meet."""
    if not params.draw_junctions:
        return 0
    layer = ensure_layer("Diagram::Junctions", (120, 120, 120))
    rs.CurrentLayer(layer)
    scale = params.canvas_scale
    count = 0
    for key, zd in all_zones.items():
        colour = zd["colour"]
        parent_of = zd["parent_of"]
        child_count = {}
        for i, p in parent_of.items():
            if p >= 0:
                child_count[p] = child_count.get(p, 0) + 1
        for i, node in enumerate(zd["nodes"]):
            degree = child_count.get(i, 0)
            if i in parent_of and parent_of[i] >= 0:
                degree += 1
            degree += zd["junctions"].get(i, 0)
            if degree >= 3:
                r = params.junction_radius * scale * min(1.0 + degree * 0.12, 2.0)
                add_filled_disk(node, r, colour, layer, "{}_j{}".format(key, i))
                count += 1
                anim_tick()
    return count


def bake_highways(zone_results, params):
    """Dense stigmergy strands between hubs -- curves only, no pipe polysurfaces."""
    if not params.draw_highways:
        return 0
    layer = ensure_layer("Diagram::Highways", (100, 100, 100))
    rs.CurrentLayer(layer)
    scale = params.canvas_scale
    n_base = max(8, int(getattr(params, "highway_strands", 26)))
    count = 0

    for a_key, b_key, weight in HIGHWAYS:
        if a_key not in zone_results or b_key not in zone_results:
            continue
        p1 = zone_results[a_key]["root"]
        p2 = zone_results[b_key]["root"]
        c1 = zone_results[a_key]["colour"]
        c2 = zone_results[b_key]["colour"]
        blend = (
            int((c1[0] + c2[0]) * 0.5),
            int((c1[1] + c2[1]) * 0.5),
            int((c1[2] + c2[2]) * 0.5),
        )
        n = max(10, int(n_base * (0.7 + 0.55 * weight)))
        spread = params.highway_line * 5.2 * scale
        for s in range(n):
            u = s / float(max(n - 1, 1))
            lateral = (u - 0.5) * 2.0 * spread
            walk = organic_walk(p1, p2, random.randint(8, 14), params, scale)
            walk = offset_walk(walk, lateral)
            dist_from_core = abs(u - 0.5)
            if dist_from_core < 0.07:
                pw = params.branch_line * 2.0 * scale
                col = blend
            elif dist_from_core < 0.20:
                pw = params.branch_line * scale
                col = blend
            else:
                pw = params.hair_line * scale * random.uniform(0.65, 1.15)
                col = c1 if u < 0.5 else c2
            if add_stigmergy_strand(walk, pw, col, layer, "{}-{}".format(a_key, b_key)):
                count += 1
            anim_tick()
    return count


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
    chosen = []
    if ranked:
        chosen = ranked[:n_need]
    while len(chosen) < n_need:
        k = len(chosen)
        gd_len = 22.0 * (1.0 if not leaves else 1.0)
        if leaves:
            gd_len = max(root.DistanceTo(nodes[i]) for i in leaves)
        t = (k + 1) / float(n_need + 1)
        along = gd_len * (0.85 + t * 0.45)
        across = (k - n_need * 0.5) * 4.5
        nodes.append(rg.Point3d(
            root.X + gd.X * along + perp.X * across,
            root.Y + gd.Y * along + perp.Y * across,
            0,
        ))
        chosen.append(len(nodes) - 1)
    chosen.sort(key=sort_key)
    return [(subs[k][0], nodes[chosen[k]]) for k in range(len(subs))]


def bake_zone(cat, params):
    colour = cat["colour"]
    layer = ensure_layer("Diagram::" + cat["key"], colour)
    rs.CurrentLayer(layer)
    scale = params.canvas_scale

    root = hub_pt(cat, scale)
    hub_scale = cat.get("hub_scale", 1.0)

    add_text_seat(root, colour, layer, cat["key"], "main", params, hub_scale)
    anim_tick()

    neighbors = neighbor_hub_pts(cat, scale, n=4)
    nodes, parent_of = grow_branches(
        root, cat["grow_dir"], cat["zone_radius"],
        params.attractors_per_zone, params, scale, neighbors,
    )
    depths = {0: 0}
    for i in range(1, len(nodes)):
        if i not in parent_of or parent_of[i] < 0:
            continue
        depth = node_depth(i, parent_of)
        depths[i] = depth
        w = line_weight_for_depth(depth, params) * scale
        kind = "trunk" if depth <= 2 else "branch"
        draw_segment(
            nodes[parent_of[i]], nodes[i], w, colour, layer, cat["key"], kind,
        )

    marker_layer = ensure_layer("Diagram::Markers", colour)
    rs.CurrentLayer(marker_layer)

    leaves = find_leaf_tips(nodes, parent_of)
    tip_assignments = assign_tips_to_subs(root, leaves, nodes, cat["subs"], cat["grow_dir"])

    placed = 0
    tips = []
    short_of = {mid: short for mid, short in cat["subs"]}
    for mid, tip in tip_assignments:
        add_text_seat(tip, colour, marker_layer, mid, "sub", params)
        tips.append((mid, short_of.get(mid, mid), tip))
        placed += 1
        anim_tick()

    return {
        "root": root,
        "colour": colour,
        "placed": placed,
        "hub_scale": hub_scale,
        "nodes": nodes,
        "parent_of": parent_of,
        "depths": depths,
        "junctions": {},
        "grow_dir": cat["grow_dir"],
        "zoom": cat.get("zoom", ""),
        "tips": tips,
    }


def bake_relations(zone_results, params, status_cb):
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
        paint(crv, (100, 100, 100), layer, rel_name)
        set_print_width(crv, max(params.rel_line * scale * 1.6, 0.35))
        mid = pts[len(pts) // 2]
        add_text_seat(mid, (90, 90, 90), layer, rel_name, "rel", params)
        zone_results.setdefault("_rels", []).append((mid, rid, verb))
        anim_tick()


def bake_loops(zone_results, params, status_cb):
    if not getattr(params, "draw_loops", True):
        return
    layer = ensure_layer("Diagram::Loops", (140, 140, 140))
    rs.CurrentLayer(layer)
    scale = params.canvas_scale
    n = 0
    for group, a_id, b_id, label in INTRA_LOOPS:
        zd = zone_results.get(group)
        if not zd:
            continue
        p1 = tip_point(zd, a_id)
        p2 = tip_point(zd, b_id)
        if p1 is None or p2 is None:
            continue
        pts = curve_between(p1, p2, bulge_factor=0.42, scale=scale)
        crv = rs.AddInterpCurve(pts, 3)
        if not crv:
            continue
        paint(crv, (130, 130, 130), layer, "{} {}".format(a_id, label))
        set_print_width(crv, max(params.rel_line * 0.55, 0.18) * scale)
        set_dashed(crv)
        mid = pts[len(pts) // 2]
        add_label(
            rg.Point3d(mid.X, mid.Y + 1.6 * scale, 0),
            label, params.branch_pt, (150, 150, 150), layer,
            "{}-{}".format(a_id, b_id), params,
        )
        n += 1
        anim_tick()
    if n:
        status_cb("Intra-group loops: {} dotted rides (fail / re-attempt / return).".format(n))


def offset_pt(pt, direction, dist):
    v = rg.Vector3d(direction[0], direction[1], 0)
    if v.Length < 1e-9:
        v = rg.Vector3d(1, 0, 0)
    v.Unitize()
    return rg.Point3d(pt.X + v.X * dist, pt.Y + v.Y * dist, 0)


def bake_labels(zone_results, params, status_cb):
    if not params.draw_text:
        return
    layer = ensure_layer("Diagram::Text", (220, 220, 220))
    rs.CurrentLayer(layer)
    font = resolve_font(params.font_name)
    status_cb("Font: {}  (2pt={:.2f} mm at text scale {}).".format(
        font, pt_to_mm(params.heading_pt, params), params.text_scale))

    title_pt = title_center(params)
    add_label(
        rg.Point3d(title_pt.X, title_pt.Y + 4.0 * params.canvas_scale, 0),
        "DISCIPLINARY MATRIX", params.title_pt, (210, 210, 210), layer, "TITLE", params,
    )
    add_label(
        rg.Point3d(title_pt.X, title_pt.Y - 5.0 * params.canvas_scale, 0),
        "Trusted with the title — by whom, for what?",
        params.subtopic_pt, (160, 160, 160), layer, "TITLE_SUB", params,
    )

    for cat in CATEGORIES:
        zd = zone_results.get(cat["key"])
        if not zd:
            continue
        colour = cat["colour"]
        gd = cat["grow_dir"]
        scale = params.canvas_scale
        heading_pt = offset_pt(zd["root"], gd, params.trunk_dot_radius * scale * 2.4)
        add_label(heading_pt, cat["key"], params.heading_pt, colour, layer, cat["key"], params)
        zoom_pt = offset_pt(heading_pt, gd, 3.2 * scale)
        add_label(zoom_pt, cat.get("zoom", ""), params.subtopic_pt, colour, layer, cat["key"] + "_ZOOM", params)
        if cat.get("logic"):
            logic_pt = offset_pt(zoom_pt, gd, 2.6 * scale)
            add_label(logic_pt, cat["logic"], params.branch_pt, colour, layer, cat["key"] + "_LOGIC", params)
        for mid, short, tip in zd.get("tips", []):
            id_pt = offset_pt(tip, gd, params.tip_dot_radius * scale * 1.6)
            add_label(id_pt, mid, params.branch_pt, colour, layer, mid, params)
            sub_pt = offset_pt(id_pt, gd, 2.4 * scale)
            add_label(sub_pt, short, params.subtopic_pt, colour, layer, mid + "_SUB", params)

    for mid, rid, verb in zone_results.get("_rels", []):
        add_label(
            rg.Point3d(mid.X, mid.Y + 2.2 * params.canvas_scale, 0),
            "{}  {}".format(rid, verb),
            params.branch_pt, (140, 140, 140), layer, rid, params,
        )


def bake_legend(zone_results, params, status_cb):
    """Lower-left key: colour *circles* stand in for Gold/Green/Tan words."""
    if not params.draw_legend:
        return
    layer = ensure_layer("Diagram::Legend", (200, 200, 200))
    rs.CurrentLayer(layer)
    scale = params.canvas_scale
    roots = [zd["root"] for zd in zone_results.values() if isinstance(zd, dict) and "root" in zd]
    if roots:
        minx = min(p.X for p in roots)
        miny = min(p.Y for p in roots)
    else:
        minx, miny = -200.0 * scale, -140.0 * scale

    # Airy stack, left-aligned: title, then swatch column + claim.
    title_h = pt_to_mm(params.heading_pt, params)
    row_h = max(pt_to_mm(params.legend_pt, params) * 2.8, 1.8 * scale)
    swatch = max(pt_to_mm(params.legend_pt, params) * 0.95, 0.95 * scale)
    origin = rg.Point3d(minx - 12.0 * scale, miny - 18.0 * scale, 0)

    add_label(
        rg.Point3d(origin.X, origin.Y, 0),
        "LEGEND", params.heading_pt, (220, 220, 220), layer, "LEGEND", params, justify=1,
    )

    order = [
        "REGISTRATION", "EDUCATION", "EMPLOYMENT", "LEGISLATION",
        "BODIES", "ETHICS", "PROCUREMENT", "RESEARCH", "POWER",
    ]
    by_key = {c["key"]: c for c in CATEGORIES}
    text_x = origin.X + swatch * 2.6
    first_y = origin.Y - title_h * 1.8 - row_h * 0.2

    for i, key in enumerate(order):
        cat = by_key.get(key)
        if not cat:
            continue
        y = first_y - i * row_h
        cx = rg.Point3d(origin.X + swatch * 0.55, y + swatch * 0.35, 0)
        add_filled_disk(cx, swatch, cat["colour"], layer, "LEGEND")
        add_halo(cx, swatch * 1.18, cat["colour"], layer, "LEGEND")
        label = "{}  —  {}".format(key, cat.get("legend", cat.get("zoom", "")))
        add_label(
            rg.Point3d(text_x, y, 0),
            label, params.legend_pt, (200, 200, 200), layer, "LEGEND", params, justify=1,
        )

    arc_y = first_y - len(order) * row_h - row_h * 0.35
    add_diamond(
        rg.Point3d(origin.X + swatch * 0.55, arc_y + swatch * 0.35, 0),
        swatch * 0.72, (150, 150, 150), layer, "LEGEND",
    )
    add_label(
        rg.Point3d(text_x, arc_y, 0),
        "enables / limits / depends upon / influences / contrasts",
        params.legend_pt, (175, 175, 175), layer, "LEGEND", params, justify=1,
    )
    status_cb("Legend: colour circles (no Gold/Green words), heading {} pt / rows {} pt.".format(
        params.heading_pt, params.legend_pt))


def generate_diagram(params, status_cb):
    random.seed(params.seed)
    force_annotation_scale_to_one(status_cb)
    clear_diagram_layers(status_cb)

    BakeState.reset(params)
    sc.doc.Views.RedrawEnabled = True
    t0 = time.time()
    try:
        bake_title(params, status_cb)

        zone_results = {}
        for cat in CATEGORIES:
            result = bake_zone(cat, params)
            zone_results[cat["key"]] = result
            status_cb("{} : {} subtopic seats.".format(cat["key"], result["placed"]))

        n_hw = bake_highways(zone_results, params) or 0
        n_fil = bake_highway_filaments(zone_results, params) or 0
        n_bridge = bake_nerve_bridges(zone_results, params) or 0
        n_mesh = bake_mesh_links(zone_results, params) or 0
        n_cap = bake_capillaries(zone_results, params) or 0
        n_junc = bake_junction_nodes(zone_results, params) or 0
        bake_relations(zone_results, params, status_cb)
        bake_loops(zone_results, params, status_cb)
        bake_labels(zone_results, params, status_cb)
        bake_legend(zone_results, params, status_cb)

        if BakeState.anim:
            BakeState.anim.tick(force=True)

        if getattr(params, "use_pipes", False) and params.fast_mode and params.bake_pipes_at_end:
            BakeState.flush_pipes(status_cb, trunks_only=True)

        elapsed = time.time() - t0
        status_cb("Highways: {} stigmergy strands. Mesh: {} local, {} nerve bridges, {} capillaries, {} junctions.".format(
            n_hw, n_mesh, n_bridge, n_cap, n_junc))
        status_cb("Done in {:.1f}s (dense lines{}).".format(
            elapsed,
            " + optional trunk pipes" if params.use_pipes and params.bake_pipes_at_end else "",
        ))
    finally:
        sc.doc.Views.RedrawEnabled = True

    rs.ZoomExtents()
    status_cb(
        "V10: group linkages = dense stigmergy lines (no pipe polysurfaces).\n"
        "Text on Diagram::Text / Diagram::Legend — hide those layers if too big."
    )


# -----------------------------------------------------------------
# GUI
# -----------------------------------------------------------------
class StigmergyForm(eforms.Form):

    def __init__(self):
        eforms.Form.__init__(self)
        self.Title = "A1 Stigmergy  V10  v1.3  (dense line linkages)"
        self.Resizable = True
        self.MinimumSize = edrawing.Size(420, 480)
        self.ClientSize = edrawing.Size(460, 620)
        self.Padding = edrawing.Padding(8)
        self.BackgroundColor = TH["bg_form"]
        self.params = GrowthParams()
        self._build_ui()

    def _build_ui(self):
        w = Widgets()
        settings = w.layout()

        settings.AddRow(w.section("Layout -- mycelial mesh (horizontal hubs)"))
        self._scale = w.num(self.params.canvas_scale, 0.5, 2.0, dec=2, inc=0.05)
        settings.AddRow(w.row("Canvas scale", self._scale))
        self._title_y = w.num(self.params.title_y, 30, 120, dec=1)
        settings.AddRow(w.row("Title Y (upper void)", self._title_y))
        self._keepout = w.num(self.params.title_keepout, 12, 60, dec=1)
        settings.AddRow(w.row("Title keep-out", self._keepout))
        self._grow_bias = w.num(self.params.grow_bias, 0.0, 1.5, dec=2, inc=0.05)
        settings.AddRow(w.row("Branch direction bias", self._grow_bias))
        self._density = w.num(self.params.density_pull, 0.0, 0.8, dec=2, inc=0.05)
        settings.AddRow(w.row("Spine density pull", self._density))
        self._draw_title = w.check("Draw title keep-out ellipse", True)
        settings.AddRow(self._draw_title)
        self._draw_hw = w.check("Dense highway strands (stigmergy lines)", True)
        settings.AddRow(self._draw_hw)
        self._draw_fil = w.check("Highway side filaments", True)
        settings.AddRow(self._draw_fil)
        self._draw_mesh = w.check("Cross-link mesh (voids)", True)
        settings.AddRow(self._draw_mesh)
        self._draw_bridges = w.check("Nerve sub-links (pic 1 density)", False)
        settings.AddRow(self._draw_bridges)
        self._draw_cap = w.check("Reaching capillary hairs", True)
        settings.AddRow(self._draw_cap)
        self._draw_junc = w.check("Thickened junction nodes (pic 1)", False)
        settings.AddRow(self._draw_junc)
        self._draw_rel = w.check("Draw relation paths", True)
        settings.AddRow(self._draw_rel)
        self._draw_loops = w.check("Dotted intra-group links (fail / feedback)", True)
        settings.AddRow(self._draw_loops)

        settings.AddRow(w.section("Speed + animation"))
        self._fast = w.check("Fast mode", True)
        settings.AddRow(self._fast)
        self._use_pipes = w.check("Optional: pipe trunks (polysurface)", False)
        settings.AddRow(self._use_pipes)
        self._pipes_end = w.check("Bake those pipes at end", False)
        settings.AddRow(self._pipes_end)
        self._animate = w.check("Animate while generating", True)
        settings.AddRow(self._animate)
        self._anim_batch = w.num(self.params.animate_batch, 5, 120, dec=0, inc=5)
        settings.AddRow(w.row("Animate batch size", self._anim_batch))
        self._anim_delay = w.num(self.params.animate_delay, 0.0, 0.08, dec=3, inc=0.005)
        settings.AddRow(w.row("Animate delay (sec)", self._anim_delay))

        settings.AddRow(w.section("Growth"))
        self._seed = w.num(self.params.seed, 0, 9999)
        settings.AddRow(w.row("Random seed", self._seed))
        self._influence = w.num(self.params.influence_radius, 4, 60, dec=1)
        settings.AddRow(w.row("Influence radius", self._influence))
        self._kill = w.num(self.params.kill_distance, 1, 20, dec=1)
        settings.AddRow(w.row("Kill distance", self._kill))
        self._segment = w.num(self.params.segment_length, 0.5, 10, dec=1)
        settings.AddRow(w.row("Segment length", self._segment))
        self._iterations = w.num(self.params.max_iterations, 50, 2000, dec=0, inc=10)
        settings.AddRow(w.row("Max iterations", self._iterations))
        self._attractors = w.num(self.params.attractors_per_zone, 20, 400, dec=0, inc=5)
        settings.AddRow(w.row("Attractors / zone", self._attractors))
        self._mesh_dist = w.num(self.params.mesh_link_dist, 3, 80, dec=1)
        settings.AddRow(w.row("Mesh link distance", self._mesh_dist))
        self._cap_hairs = w.num(self.params.capillary_hairs, 0, 120, dec=0, inc=5)
        settings.AddRow(w.row("Capillary hairs / zone", self._cap_hairs))
        self._mesh_sample = w.num(self.params.mesh_sample, 15, 120, dec=0, inc=5)
        settings.AddRow(w.row("Mesh sample nodes", self._mesh_sample))
        self._bridges = w.num(self.params.bridges_per_pair, 0, 20, dec=0, inc=1)
        settings.AddRow(w.row("Sub-links / group pair", self._bridges))
        self._bridge_range = w.num(self.params.bridge_range, 40, 280, dec=0, inc=10)
        settings.AddRow(w.row("Sub-link hub reach", self._bridge_range))

        settings.AddRow(w.section("Line weight -- print width on curves"))
        self._strands = w.num(self.params.highway_strands, 8, 80, dec=0, inc=2)
        settings.AddRow(w.row("Strands / highway", self._strands))
        self._highway = w.num(self.params.highway_line, 0.3, 4.0, dec=2, inc=0.05)
        settings.AddRow(w.row("Highway bundle spread", self._highway))
        self._trunk_line = w.num(self.params.trunk_line, 0.15, 3.0, dec=2, inc=0.05)
        settings.AddRow(w.row("Near-root branches", self._trunk_line))
        self._branch_line = w.num(self.params.branch_line, 0.05, 2.0, dec=2, inc=0.05)
        settings.AddRow(w.row("Mid branches", self._branch_line))
        self._hair_line = w.num(self.params.hair_line, 0.02, 1.5, dec=2, inc=0.05)
        settings.AddRow(w.row("Terminal capillaries", self._hair_line))
        self._rel_line = w.num(self.params.rel_line, 0.10, 2.0, dec=2, inc=0.05)
        settings.AddRow(w.row("Relation paths", self._rel_line))

        settings.AddRow(w.section("Text seats -- filled dots, no letters"))
        self._trunk_r = w.num(self.params.trunk_dot_radius, 2.0, 16, dec=1)
        settings.AddRow(w.row("Main-topic seat", self._trunk_r))
        self._tip_r = w.num(self.params.tip_dot_radius, 1.2, 10, dec=1)
        settings.AddRow(w.row("Subtopic seat", self._tip_r))
        self._rel_r = w.num(self.params.rel_dot_radius, 1.0, 10, dec=1)
        settings.AddRow(w.row("Relation diamond", self._rel_r))
        self._junc_r = w.num(self.params.junction_radius, 0.5, 8, dec=1)
        settings.AddRow(w.row("Junction node", self._junc_r))

        settings.AddRow(w.section("Text -- Futura, sizes in pt (print)"))
        self._draw_text = w.check("Bake catalog text", True)
        settings.AddRow(self._draw_text)
        self._draw_legend = w.check("Legend lower-left (colour circles, no Gold/Green words)", True)
        settings.AddRow(self._draw_legend)
        self._font = w.textbox(self.params.font_name)
        settings.AddRow(w.row("Font", self._font))
        self._title_pt = w.num(self.params.title_pt, 0.2, 24, dec=1, inc=0.5)
        settings.AddRow(w.row("Title pt", self._title_pt))
        self._heading_pt = w.num(self.params.heading_pt, 0.2, 24, dec=1, inc=0.5)
        settings.AddRow(w.row("Heading / title pt", self._heading_pt))
        self._sub_pt = w.num(self.params.subtopic_pt, 0.2, 24, dec=1, inc=0.5)
        settings.AddRow(w.row("Subtopic pt", self._sub_pt))
        self._br_pt = w.num(self.params.branch_pt, 0.1, 24, dec=1, inc=0.1)
        settings.AddRow(w.row("Branch / ID pt", self._br_pt))
        self._leg_pt = w.num(self.params.legend_pt, 0.2, 24, dec=1, inc=0.5)
        settings.AddRow(w.row("Legend pt", self._leg_pt))
        self._text_scale = w.num(self.params.text_scale, 0.5, 20, dec=1, inc=0.5)
        settings.AddRow(w.row("Text scale (if too small)", self._text_scale))

        scroll = eforms.Scrollable()
        scroll.Content = settings
        scroll.ExpandContentWidth = True
        scroll.BackgroundColor = TH["bg_form"]

        self._btn_generate = w.button("Generate", self._on_generate, width=110, primary=True)
        self._btn_clear = w.button("Clear only", self._on_clear, width=110)
        self._btn_vector = w.button("Hide pipes (vector)", self._on_hide_pipes, width=130)
        self._btn_pipes = w.button("Show pipes", self._on_show_pipes, width=100)

        self._log = w.log_area(height=120)
        self.status_cb = make_logger(self._log)

        outer = w.layout()
        outer.Add(scroll, yscale=True)
        outer.AddRow(w.button_row(self._btn_generate, self._btn_clear))
        outer.AddRow(w.button_row(self._btn_vector, self._btn_pipes))
        outer.AddRow(self._log)
        self.Content = outer
        self.status_cb(
            "V10: linkages are dense stigmergy lines, not pipe polysurfaces.\n"
            "Gold path stays the Victoria flowchart. Legend = colour circles."
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
        p.density_pull = float(self._density.Value)
        p.trunk_dot_radius = float(self._trunk_r.Value)
        p.tip_dot_radius = float(self._tip_r.Value)
        p.rel_dot_radius = float(self._rel_r.Value)
        p.junction_radius = float(self._junc_r.Value)
        p.highway_line = float(self._highway.Value)
        p.trunk_line = float(self._trunk_line.Value)
        p.branch_line = float(self._branch_line.Value)
        p.hair_line = float(self._hair_line.Value)
        p.rel_line = float(self._rel_line.Value)
        p.mesh_link_dist = float(self._mesh_dist.Value)
        p.capillary_hairs = int(self._cap_hairs.Value)
        p.mesh_sample = int(self._mesh_sample.Value)
        p.bridges_per_pair = int(self._bridges.Value)
        p.bridge_range = float(self._bridge_range.Value)
        p.fast_mode = bool(self._fast.Checked)
        p.use_pipes = bool(self._use_pipes.Checked)
        p.bake_pipes_at_end = bool(self._pipes_end.Checked)
        p.highway_strands = int(self._strands.Value)
        p.animate = bool(self._animate.Checked)
        p.animate_batch = int(self._anim_batch.Value)
        p.animate_delay = float(self._anim_delay.Value)
        p.draw_title_ellipse = bool(self._draw_title.Checked)
        p.draw_highways = bool(self._draw_hw.Checked)
        p.draw_highway_filaments = bool(self._draw_fil.Checked)
        p.draw_mesh_links = bool(self._draw_mesh.Checked)
        p.draw_nerve_bridges = bool(self._draw_bridges.Checked)
        p.draw_capillaries = bool(self._draw_cap.Checked)
        p.draw_junctions = bool(self._draw_junc.Checked)
        p.draw_relations = bool(self._draw_rel.Checked)
        p.draw_loops = bool(self._draw_loops.Checked)
        p.draw_text = bool(self._draw_text.Checked)
        p.draw_legend = bool(self._draw_legend.Checked)
        p.font_name = (self._font.Text or "Futura").strip()
        p.title_pt = float(self._title_pt.Value)
        p.heading_pt = float(self._heading_pt.Value)
        p.subtopic_pt = float(self._sub_pt.Value)
        p.branch_pt = float(self._br_pt.Value)
        p.legend_pt = float(self._leg_pt.Value)
        p.text_scale = float(self._text_scale.Value)
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
            n = BakeState.flush_pipes(self.status_cb, trunks_only=False)
            if rs.IsLayer("Diagram::Pipes"):
                rs.LayerVisible("Diagram::Pipes", True)
            if n:
                self.status_cb("All queued pipes baked and visible.")
            else:
                self.status_cb("Pipes layer visible (if any from last generate).")
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
