"""
Stigmergy / space-colonization diagram generator for Assessment 1
(The Disciplinary Matrix of Architecture)

Rhino 8 -- run in the new ScriptEditor (Python 3 / CPython). Click Run to
open a small dark-themed control panel: tune growth/text parameters, hit
Generate, read the status log. Re-running Generate clears the previous
bake first, so you can iterate without manually selecting + deleting.

HOW IT WORKS
------------
Each required topic (REGISTRATION, EDUCATION, EMPLOYMENT...) is a "zone."
A tree of branches grows from that zone's root point toward a cloud of
random attractor points inside the zone, using the classic space-
colonization algorithm (Runions et al., "Modeling Trees with a Space
Colonization Algorithm", 2007) -- the same family of algorithm behind
root/nerve/coral-looking generative diagrams. That's the "stigmergy"
look: branches accrete toward unclaimed space rather than following a
fixed layout.

Main-node headings are placed BEFORE their zone grows and registered as
"obstacles" -- branch growth steers away from them, so the heading text
ends up with stigmergy lines curving around it rather than through it.

Subtopic labels are placed on the longest/farthest branch tips after
growth finishes, offset outward along the tip's own direction so the
label sits past the line end, not on top of it.

Cross-links are separate smooth curves connecting specific points
across zones (dashed, thin, on their own layer) for "related info
across category."

EDIT THE "CONTENT DATA" BLOCK to change zones / subtopics / links --
nothing else needs to change to regenerate.

ANNOTATION-SCALE FIX (2026-08-20)
----------------------------------
First click-test baked headings at ~50x the requested height, overlapping
across zones that are 200mm+ apart. Cause: Rhino's model-space annotation
scale (DimStyle.DimensionScale) multiplies baked TextHeight for on-screen
display -- some mm templates ship with this set to e.g. 1:50, independent
of the literal height value passed to AddText. Millimeters is still the
correct document unit for this diagram (it spans ~330x380mm, proportionate
to an A1 sheet); the fix below forces the current dimstyle's scale to 1:1
before baking, so HEADING_HEIGHT etc. are literal mm. UNVERIFIED against a
live Rhino session -- this is exactly what the next click-test is for.
"""

import random
import math
import traceback
import Rhino
import Rhino.UI
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Eto.Drawing as edrawing
import Eto.Forms as eforms

# =================================================================
# 0. DARK THEME + WIDGET FACTORY -- same palette/pattern as the
#    house Eto style (architectural-python-starter/lib/eto_theme.py).
#    Inlined, not imported: this script must run standalone, pasted
#    straight into the Rhino 8 Script Editor.
# =================================================================
def _ec(r, g, b):
    return edrawing.Color(r / 255.0, g / 255.0, b / 255.0)


TH = {
    "bg_form":   _ec(18, 18, 18),
    "bg_ctrl":   _ec(36, 36, 36),
    "bg_btn":    _ec(50, 50, 50),
    "bg_btn_hi": _ec(65, 65, 65),
    "fg":        _ec(175, 175, 175),
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

    def row(self, label, ctrl, lbl_w=150):
        tl = eforms.TableLayout()
        tl.Spacing = edrawing.Size(5, 0)
        spacer_cell = eforms.TableCell(eforms.Label())
        spacer_cell.ScaleWidth = True
        tl.Rows.Add(eforms.TableRow(
            eforms.TableCell(self.lbl(label, width=lbl_w)),
            eforms.TableCell(ctrl),
            spacer_cell,
        ))
        return tl

    def button_row(self, *buttons):
        tl = eforms.TableLayout()
        tl.Spacing = edrawing.Size(6, 0)
        spacer_cell = eforms.TableCell(eforms.Label())
        spacer_cell.ScaleWidth = True
        cells = [eforms.TableCell(b) for b in buttons] + [spacer_cell]
        tl.Rows.Add(eforms.TableRow(*cells))
        return tl

    def log_area(self, height=180):
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


def make_logger(text_area, keep_lines=150):
    def log_msg(msg):
        current = text_area.Text or ""
        lines = (current + str(msg) + "\n").split("\n")
        text_area.Text = "\n".join(lines[-keep_lines:])
    return log_msg


# =================================================================
# 1. GROWTH PARAMETERS -- defaults for the GUI; tune these, not the
#    algorithm, if a zone looks too sparse / too tangled.
# =================================================================
class GrowthParams(object):
    def __init__(self):
        self.seed = 7
        self.influence_radius = 18.0
        self.kill_distance = 4.0
        self.segment_length = 3.0
        self.max_iterations = 500
        self.attractors_per_zone = 90
        self.heading_height = 6.0
        self.subtopic_height = 2.4
        self.link_label_height = 1.8
        self.text_obstacle_margin = 6.0   # clearance branches keep from heading text


# =================================================================
# 2. CONTENT DATA -- edit this to match your actual brief content.
#    Seeded here from your repo's Assessment 1 required topics.
# =================================================================
CATEGORIES = {
    "REGISTRATION": {
        "colour": (201, 162, 39),
        "root": rg.Point3d(0, 0, 0),
        "zone_center": rg.Point3d(0, 0, 0),
        "zone_radius": 42,
        "subtopics": [
            "Accredited education",
            "Logbook - 3300 hrs",
            "APE exam + interview",
            "ARBV registration",
            "CPD + PI insurance",
        ],
    },
    "EDUCATION": {
        "colour": (107, 155, 107),
        "root": rg.Point3d(-95, 65, 0),
        "zone_center": rg.Point3d(-115, 80, 0),
        "zone_radius": 30,
        "subtopics": [
            "University / AQF",
            "Graduation",
            "CPD mandate since 2022",
            "Molander: formative measure",
        ],
    },
    "EMPLOYMENT": {
        "colour": (166, 138, 91),
        "root": rg.Point3d(-95, -65, 0),
        "zone_center": rg.Point3d(-115, -80, 0),
        "zone_radius": 30,
        "subtopics": [
            "Practice / firm",
            "Project mgmt ceded 1960s-70s",
            "ACA",
            "Professionals Australia",
        ],
    },
    "LEGISLATION": {
        "colour": (91, 124, 153),
        "root": rg.Point3d(95, 65, 0),
        "zone_center": rg.Point3d(115, 80, 0),
        "zone_radius": 30,
        "subtopics": [
            "Architects Act 1991",
            "Building Act / VBA",
            "NCC - amendable",
            "Duty to public s.17-18",
        ],
    },
    "PROFESSIONAL_BODIES": {
        "colour": (138, 107, 168),
        "root": rg.Point3d(95, -65, 0),
        "zone_center": rg.Point3d(115, -80, 0),
        "zone_radius": 30,
        "subtopics": [
            "AIA - voluntary",
            "ARBV - statutory",
            "AACA - standards",
            "Parlour / ArchiTeam",
        ],
    },
    "ETHICS_PUBLIC_VALUE": {
        "colour": (176, 106, 122),
        "root": rg.Point3d(0, 125, 0),
        "zone_center": rg.Point3d(0, 155, 0),
        "zone_radius": 30,
        "subtopics": [
            "Duty beyond paying client",
            "Loos 1910",
            "Architecture not Architects",
            "Stead: searchlight or lantern",
        ],
    },
    "PROCUREMENT": {
        "colour": (52, 80, 112),
        "root": rg.Point3d(-45, -135, 0),
        "zone_center": rg.Point3d(-65, -165, 0),
        "zone_radius": 26,
        "subtopics": [
            "AS4000 vs D&C vs Novated",
            "AIA novation survey 2019",
            "Lost design control",
        ],
    },
    "RESEARCH_INNOVATION": {
        "colour": (77, 143, 106),
        "root": rg.Point3d(45, -135, 0),
        "zone_center": rg.Point3d(65, -165, 0),
        "zone_radius": 26,
        "subtopics": [
            "Lui: codes as co-authorship",
            "Dan Hill: NCC emissions roadmap",
            "Fire, Water, Building exhibition",
        ],
    },
}

# (zone_a, zone_b, relationship label)
CROSS_LINKS = [
    ("REGISTRATION", "EMPLOYMENT", "logged hours"),
    ("LEGISLATION", "PROCUREMENT", "novation clauses"),
    ("LEGISLATION", "RESEARCH_INNOVATION", "NCC amendments"),
    ("REGISTRATION", "LEGISLATION", "tight vs loose gating"),
    ("PROFESSIONAL_BODIES", "ETHICS_PUBLIC_VALUE", "who answers to whom"),
]

# =================================================================
# 3. TEXT OBSTACLES -- headings register themselves here BEFORE
#    their zone grows, so branch direction steers away from them.
#    Reset at the start of every generate_diagram() call.
# =================================================================
_text_obstacles = []  # list of (center Point3d, half_width, half_height)


def register_text_obstacle(pt, text, height, margin):
    half_w = 0.6 * height * max(len(text), 1) / 2.0
    half_h = height / 2.0
    _text_obstacles.append((pt, half_w + margin, half_h + margin))


def steer_from_obstacles(pt, direction):
    for center, half_w, half_h in _text_obstacles:
        d = pt.DistanceTo(center)
        clearance = max(half_w, half_h)
        if 1e-6 < d < clearance:
            away = pt - center
            away.Unitize()
            direction = direction + away * 0.9
    return direction


# =================================================================
# 4. SPACE COLONIZATION GROWTH
# =================================================================
def random_point_in_disc(center, radius):
    r = radius * math.sqrt(random.random())
    a = random.random() * 2.0 * math.pi
    return rg.Point3d(center.X + r * math.cos(a), center.Y + r * math.sin(a), 0)


def grow_branches(root_pt, zone_center, zone_radius, n_attractors, params):
    attractors = [random_point_in_disc(zone_center, zone_radius) for _ in range(n_attractors)]
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
            if avg.Length > 1e-9:
                avg.Unitize()
            avg = steer_from_obstacles(nodes[i], avg)
            if avg.Length > 1e-9:
                avg.Unitize()
            new_pt = nodes[i] + avg * params.segment_length
            nodes.append(new_pt)
            parent_of[len(nodes) - 1] = i

        attractors = [a for a in attractors
                      if all(n.DistanceTo(a) >= params.kill_distance for n in nodes)]

    return nodes, parent_of


def find_leaf_tips(nodes, parent_of):
    is_parent = set(parent_of.values())
    leaves = [i for i in range(len(nodes)) if i not in is_parent and i != 0]
    leaves.sort(key=lambda i: nodes[i].DistanceTo(nodes[0]), reverse=True)
    return leaves


# =================================================================
# 5. RHINO OUTPUT HELPERS
# =================================================================
def ensure_layer(name, colour):
    if not rs.IsLayer(name):
        rs.AddLayer(name, colour)
    return name


def clear_diagram_layers(status_cb):
    """Delete objects left over from a previous Generate click, so
    re-running from the GUI doesn't pile up duplicate geometry."""
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
    """See ANNOTATION-SCALE FIX note at the top of this file. Best-effort:
    if the RhinoCommon API shape differs from expected, this logs the
    traceback instead of crashing the whole generate, and the fallback is
    the manual fix (Document Properties > Annotation > Model Space Scale)."""
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
            status_cb("Annotation scale already 1:1 -- no fix needed.")
    except Exception:
        status_cb(
            "Could not auto-fix annotation scale -- check Document "
            "Properties > Annotation > Model Space Scale manually:\n"
            + traceback.format_exc()
        )


def bake_zone(zone_name, data, params):
    colour = data["colour"]
    layer = ensure_layer("Diagram::" + zone_name, colour)
    rs.CurrentLayer(layer)

    # heading goes down first so growth can steer around it
    heading_text = zone_name.replace("_", " ")
    register_text_obstacle(data["root"], heading_text, params.heading_height,
                            params.text_obstacle_margin)
    heading_id = rs.AddText(heading_text, data["root"],
                             params.heading_height, None, 1, 1)  # bold, centered
    rs.ObjectLayer(heading_id, layer)
    rs.ObjectColor(heading_id, colour)

    nodes, parent_of = grow_branches(data["root"], data["zone_center"],
                                      data["zone_radius"],
                                      params.attractors_per_zone, params)

    for i in range(1, len(nodes)):
        line_id = rs.AddLine(nodes[parent_of[i]], nodes[i])
        rs.ObjectLayer(line_id, layer)
        rs.ObjectColor(line_id, colour)

    leaves = find_leaf_tips(nodes, parent_of)
    subtopics = data["subtopics"]
    label_layer = ensure_layer("Diagram::Labels", (40, 40, 40))

    tip_lookup = {}  # subtopic index -> tip Point3d, for cross-links
    for k, label in enumerate(subtopics):
        if k >= len(leaves):
            break
        tip_i = leaves[k]
        tip = nodes[tip_i]
        parent = nodes[parent_of[tip_i]]
        direction = tip - parent
        if direction.Length > 1e-9:
            direction.Unitize()
        else:
            direction = rg.Vector3d(1, 0, 0)
        label_pt = tip + direction * (params.subtopic_height * 0.8 + 2.0)
        label_id = rs.AddText(label, label_pt, params.subtopic_height, None, 0, 0)
        rs.ObjectLayer(label_id, label_layer)
        rs.ObjectColor(label_id, colour)
        tip_lookup[label] = tip

    return {"root": data["root"], "tips": tip_lookup, "colour": colour}


def bake_cross_links(zone_results, params):
    link_layer = ensure_layer("Diagram::CrossLinks", (120, 120, 120))
    rs.CurrentLayer(link_layer)

    for zone_a, zone_b, label in CROSS_LINKS:
        if zone_a not in zone_results or zone_b not in zone_results:
            continue
        pt_a = zone_results[zone_a]["root"]
        pt_b = zone_results[zone_b]["root"]
        mid = rg.Point3d((pt_a.X + pt_b.X) / 2.0, (pt_a.Y + pt_b.Y) / 2.0, 0)
        # bow the midpoint outward so links read as curves, not straight rules
        perp = rg.Vector3d(-(pt_b.Y - pt_a.Y), pt_b.X - pt_a.X, 0)
        if perp.Length > 1e-9:
            perp.Unitize()
        mid = mid + perp * (pt_a.DistanceTo(pt_b) * 0.12)

        curve_id = rs.AddInterpCurve([pt_a, mid, pt_b])
        rs.ObjectColor(curve_id, (120, 120, 120))
        try:
            rs.ObjectLinetype(curve_id, "Dashed")
        except Exception:
            pass  # template has no "Dashed" linetype -- leave solid, not fatal

        label_pt = mid + perp * 3.0
        label_id = rs.AddText(label, label_pt, params.link_label_height, None, 2, 0)  # italic
        rs.ObjectColor(label_id, (120, 120, 120))


# =================================================================
# 6. GENERATE -- orchestrates one full regenerate cycle from the GUI.
# =================================================================
def generate_diagram(params, status_cb):
    random.seed(params.seed)
    del _text_obstacles[:]

    force_annotation_scale_to_one(status_cb)
    clear_diagram_layers(status_cb)

    sc.doc.Views.RedrawEnabled = False
    try:
        zone_results = {}
        for name, data in CATEGORIES.items():
            zone_results[name] = bake_zone(name, data, params)
        bake_cross_links(zone_results, params)
    finally:
        sc.doc.Views.RedrawEnabled = True

    rs.ZoomExtents()
    status_cb("Stigmergy diagram generated: {} zones, {} cross-links.".format(
        len(CATEGORIES), len(CROSS_LINKS)))


# =================================================================
# 7. GUI
# =================================================================
class StigmergyForm(eforms.Form):

    def __init__(self):
        eforms.Form.__init__(self)  # required for Rhino 8 CPython inheritance
        self.Title = "Stigmergy Diagram Generator  v0.2"
        self.Resizable = True
        self.ClientSize = edrawing.Size(430, 580)
        self.Padding = edrawing.Padding(8)
        self.BackgroundColor = TH["bg_form"]

        self.params = GrowthParams()
        self._build_ui()

    def _build_ui(self):
        w = Widgets()
        lay = w.layout()

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
        self._attractors = w.num(self.params.attractors_per_zone, 10, 400, dec=0, inc=5)
        lay.AddRow(w.row("Attractors / zone", self._attractors))

        lay.AddRow(w.section("Text (mm -- annotation scale forced to 1:1 first)"))
        self._heading_h = w.num(self.params.heading_height, 1, 40, dec=1)
        lay.AddRow(w.row("Heading height", self._heading_h))
        self._subtopic_h = w.num(self.params.subtopic_height, 0.5, 20, dec=1)
        lay.AddRow(w.row("Subtopic height", self._subtopic_h))
        self._link_h = w.num(self.params.link_label_height, 0.5, 20, dec=1)
        lay.AddRow(w.row("Link label height", self._link_h))

        self._btn_generate = w.button("Generate", self._on_generate, width=110, primary=True)
        self._btn_clear = w.button("Clear only", self._on_clear, width=110)
        lay.AddRow(w.button_row(self._btn_generate, self._btn_clear))

        self._log = w.log_area(height=190)
        self.status_cb = make_logger(self._log)
        lay.AddRow(self._log)

        self.Content = lay

    def _read_params(self):
        p = self.params
        p.seed = int(self._seed.Value)
        p.influence_radius = float(self._influence.Value)
        p.kill_distance = float(self._kill.Value)
        p.segment_length = float(self._segment.Value)
        p.max_iterations = int(self._iterations.Value)
        p.attractors_per_zone = int(self._attractors.Value)
        p.heading_height = float(self._heading_h.Value)
        p.subtopic_height = float(self._subtopic_h.Value)
        p.link_label_height = float(self._link_h.Value)
        return p

    def _on_generate(self, sender, e):
        self._btn_generate.Enabled = False
        try:
            params = self._read_params()
            generate_diagram(params, self.status_cb)
        except Exception:
            self.status_cb("ERROR:\n" + traceback.format_exc())
        finally:
            self._btn_generate.Enabled = True

    def _on_clear(self, sender, e):
        try:
            clear_diagram_layers(self.status_cb)
        except Exception:
            self.status_cb("ERROR:\n" + traceback.format_exc())


# =================================================================
# 8. ENTRY POINT
# =================================================================
def main():
    try:
        form = StigmergyForm()
        form.Owner = Rhino.UI.RhinoEtoApp.MainWindow
        form.Show()
    except Exception:
        print("Stigmergy Diagram Generator failed to start:\n" + traceback.format_exc())


if __name__ == "__main__":
    main()
