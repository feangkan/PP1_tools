"""
Manifesto diagram generator -- Assessment 2
("Responsibility without authority" -- the 10-point Practice Manifesto)

Rhino 8 -- run in the new ScriptEditor (Python 3 / CPython). Click Run to
open a dark-themed control panel: tune growth/text parameters, hit Generate,
read the status log. Re-running Generate clears the previous bake first, so
you can iterate without manually selecting + deleting.

LINEAGE
-------
Algorithm reference: ../assessment-1/stigmergy-generator.py -- the same
space-colonization growth (Runions et al., "Modeling Trees with a Space
Colonization Algorithm", 2007) that drew the Assessment 1 disciplinary
matrix. Content is entirely fresh for Assessment 2, and four parts of the
algorithm are re-engineered rather than copied:

  1. SPATIAL GRID for the nearest-node search. A1 scanned every node for
     every attractor every iteration -- O(attractors x nodes), which was
     tolerable at 8 zones and is not at 11. Nodes are now bucketed into a
     uniform grid and only the buckets within the influence radius are
     searched. Same result, far less waiting.

  2. STATELESS PER-ZONE SEEDING. A1 called random.seed() once, so a zone's
     attractor cloud depended on how many zones had already grown -- change
     one zone and every later zone moved. Each zone now derives its own
     RNG from (seed, zone index), so a zone is bit-identical regardless of
     what ran before it. (House rule borrowed from the newer pv_core /
     mo_core work: reproducible from an index, never from a running RNG.)

  3. RECTANGULAR TEXT OBSTACLES. A1 treated every text box as a circle of
     radius max(half_width, half_height), so a wide label pushed branches
     away in a huge disc and a short one barely at all. Obstacles are now
     tested as real rectangles, with the escape along the axis of least
     penetration.

  4. BRANCH WEIGHT FROM SUBTREE SIZE. A1 drew every segment at one weight.
     Each segment's print width now scales with how many tips depend on it
     (Runions' own branch-diameter step), so trunks read heavier than twigs
     -- and in this diagram that means "how much of the point's argument
     runs through here".

  Better tip selection comes with it: subtopic labels are placed on tips
  chosen for ANGULAR SPREAD around the zone, not simply the longest four,
  which in A1 tended to stack all four labels on one side.

WHAT THIS DRAWS, AND WHY IT IS SHAPED THIS WAY
----------------------------------------------
The manifesto's spine is one question asked ten times: *does the person
carrying the responsibility hold the authority to act on it?* The drawing is
built so that question is the thing you see, not a caption:

  - TWO WINGS. Left = the five MAINTAIN/REFINE points, where responsibility
    and authority sit together. Right = the five CHANGE points, where they
    have been separated. The split is the argument, so colour follows the
    half (green / blue), not ten arbitrary per-topic hues.

  - THE RESPONSIBILITY -> AUTHORITY BAR. Every point bakes two small labels
    at its root -- who carries the responsibility, who holds the authority --
    joined by a connector whose STATE carries the claim:
        solid  = joined     (the maintain points)
        dashed = partial    (point 4: evidence without power)
        broken = separated  (the change points -- drawn with a real gap)
    This is the one device that stops the drawing being a bubble map.

  - CROSS-LINKS are the coherence test. Most run maintain <-> change through
    the middle of the sheet, which is the point: registration (1) depends on
    conditions (9) and on authority at site (8); the duty to the public (2)
    is what the novation claim rests on. Ten points that need each other are
    a manifesto; ten that don't are ten interesting issues.

  - THE AI STANCE is deliberately NOT a zone. It bakes as a marginal note,
    because in this manifesto AI is an assistive instrument, not a subject:
    a tool can assist production but cannot be held responsible for the
    work, so the authority to decide stays with the person who is.

EDIT THE "CONTENT DATA" BLOCK to change points / labels / links -- nothing
else needs to change to regenerate.

STATUS
------
NOT YET CLICK-TESTED in a live Rhino session. The growth/bake/Eto skeleton
descends from the click-tested A1 generator, but everything listed under
LINEAGE above is new code. Expect the first run to need layout tuning
(spacing vs zone radius) rather than debugging -- see REDRAW NOTES at the
foot of this file.

ANNOTATION-SCALE FIX -- carried over from Assessment 1
-------------------------------------------------------
Rhino's model-space annotation scale (DimStyle.DimensionScale) multiplies
baked TextHeight for on-screen display, so a 6mm heading can arrive ~50x too
large on templates shipping 1:50. Millimetres remain the correct document
unit (this sheet spans roughly 900 x 620mm including the margin notes,
proportionate to A1). The fix below forces the current dimstyle's scale to
1:1 before baking, so the height values in the panel are literal mm.
"""

import random
import math
import time
import traceback
import Rhino
import Rhino.UI
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Eto.Drawing as edrawing
import Eto.Forms as eforms


# =================================================================
# 0. DARK THEME + WIDGET FACTORY -- same palette/pattern as the house
#    Eto style (architectural-python-starter/lib/eto_theme.py). Inlined,
#    not imported: this script must run standalone, pasted straight into
#    the Rhino 8 Script Editor.
# =================================================================
def _ec(r, g, b):
    return edrawing.Color(r / 255.0, g / 255.0, b / 255.0)


TH = {
    "bg_form":    _ec(18, 18, 18),
    "bg_ctrl":    _ec(36, 36, 36),
    "bg_btn":     _ec(50, 50, 50),
    "bg_btn_hi":  _ec(65, 65, 65),
    "fg":         _ec(175, 175, 175),
    "fg_section": _ec(155, 155, 155),
    "fg_bright":  _ec(218, 218, 218),
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

    def check(self, label, value=True):
        cb = eforms.CheckBox()
        cb.Text = label
        cb.Checked = value
        cb.TextColor = TH["fg"]
        return cb

    def button(self, label, handler=None, width=90, primary=False):
        btn = eforms.Button()
        btn.Text = label
        btn.Width = width
        btn.BackgroundColor = TH["bg_btn_hi"] if primary else TH["bg_btn"]
        btn.TextColor = TH["fg_bright"]
        if handler is not None:
            btn.Click += handler
        return btn

    def row(self, label, ctrl, lbl_w=155):
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
# 1. PARAMETERS -- every magic number gets a name and a note saying
#    what goes wrong when it is set badly.
# =================================================================
class GrowthParams(object):
    def __init__(self):
        self.seed = 11               # per-zone RNG derives from (seed, zone index)
        self.influence_radius = 18.0  # attractor only pulls nodes within this
        self.kill_distance = 4.0     # attractor is consumed once a node is this close
        self.segment_length = 3.0    # one growth step; smaller = finer, slower
        self.max_iterations = 500    # safety stop; growth usually ends earlier
        self.attractors_per_zone = 110  # more = denser bush; 75 previewed wispy
        # Text is sized against a ~700x800mm sheet. A1 used 6.0/2.4 on a
        # ~330x380mm sheet; these are scaled to keep the same optical weight.
        self.heading_height = 7.0
        self.subtopic_height = 2.8
        self.pair_height = 2.4       # responsibility / authority labels
        self.link_label_height = 2.2
        self.text_obstacle_margin = 6.0   # clearance branches keep from text
        self.trunk_width = 0.55      # mm print width of the heaviest branches
        self.twig_width = 0.10       # mm print width of single-tip twigs
        self.draw_annotations = True  # hub, wing headers, legend, stance note
        self.draw_weights = True     # scale print width by subtree size


# =================================================================
# 2. CONTENT DATA -- the manifesto, as drawn.
#    Source of truth for wording: 02-manifesto-skeleton.md (v02).
#    Labels stay 3-8 words (08-diagram-style/STYLE_GUIDE.md).
#
#    "joined" drives the responsibility/authority bar:
#       "yes"     -> solid connector   (the two sit together)
#       "partial" -> dashed connector  (evidence without power)
#       "no"      -> broken connector  (they have been separated)
# =================================================================
KEEP_COLOUR   = (63, 110, 63)     # maintain / refine wing
CHANGE_COLOUR = (52, 80, 112)     # change wing
HUB_COLOUR    = (201, 162, 39)
ACTOR_COLOUR  = (122, 59, 40)
NOTE_COLOUR   = (105, 105, 105)
LINK_COLOUR   = (120, 120, 120)

# Wing geometry. Roots sit on a vertical spine per wing; zone centres are
# offset outboard so growth accretes away from the sheet's middle, leaving
# the centre free for the cross-link network.
#
# EACH BUSH SURROUNDS ITS OWN HEADING, as in Assessment 1: the disc is
# centred a little outboard of the root but the root sits well inside it, so
# growth curls around the label group rather than floating away from it.
# Pushing the disc clear of the heading instead (tried, previewed, rejected)
# left a bare 50mm gap between every title and its growth, because a 24-
# character heading's obstacle box is ~100mm wide.
WING_ROOT_X   = 150.0
WING_CENTRE_X = 164.0
ROW_Y = [200.0, 100.0, 0.0, -100.0, -200.0]
ZONE_RADIUS = 46.0

POINTS = {
    "P1": {
        "title": "1 - REGISTRATION",
        "half": "keep",
        "responsibility": "the registered architect",
        "authority": "the Act + ARBV",
        "joined": "yes",
        "subtopics": [
            "APE exam + interview",
            "3300 supervised hours",
            "PI insurance",
            "refine: make supervision real",
        ],
    },
    "P2": {
        "title": "2 - DUTY TO THE PUBLIC",
        "half": "keep",
        "responsibility": "the architect",
        "authority": "standing to refuse (the Act)",
        "joined": "yes",
        "subtopics": [
            "Act s.17-18",
            "duty to withdraw",
            "the client not in the room",
            "standing, not conscience",
        ],
    },
    "P3": {
        "title": "3 - INDEPENDENT REVIEW",
        "half": "keep",
        "responsibility": "the designer",
        "authority": "surveyor + council, by design",
        "joined": "yes",
        "subtopics": [
            "Building Surveyor sign-off",
            "Council planning gate",
            "nobody checks their own work",
            "extends to assisted work",
        ],
    },
    "P4": {
        "title": "4 - SPLIT APPARATUS",
        "half": "keep",
        "responsibility": "workers carry the conditions",
        "authority": "advocacy bodies hold no power",
        "joined": "partial",
        "subtopics": [
            "AIA advances / ARBV regulates",
            "Parlour, ArchiTeam, UAW",
            "wellbeing research",
            "evidence without authority",
        ],
    },
    "P5": {
        "title": "5 - CODES + CPD",
        "half": "keep",
        "responsibility": "the profession complies",
        "authority": "it can amend the instrument",
        "joined": "yes",
        "subtopics": [
            "NCC amendable",
            "Lui: codes as activism",
            "CPD as formative judgement",
            "how a fee is actually built",
        ],
    },
    "P6": {
        "title": "6 - ENCLOSED KNOWLEDGE",
        "half": "change",
        "responsibility": "architect must comply",
        "authority": "a commercial owner gates access",
        "joined": "no",
        "subtopics": [
            "Standards Australia to SAI",
            "paywalled compliance",
            "cladding test data private",
            "restoration, not invention",
        ],
    },
    "P7": {
        "title": "7 - RULE-MAKING",
        "half": "change",
        "responsibility": "bound by the rules",
        "authority": "opaque, overlapping committees",
        "joined": "no",
        "subtopics": [
            "who amends the code",
            "overlapping board seats",
            "publish members + interests",
            "A1's invisible gate",
        ],
    },
    "P8": {
        "title": "8 - PROCUREMENT",
        "half": "change",
        "responsibility": "architect liable for the design",
        "authority": "the contractor controls it",
        "joined": "no",
        "subtopics": [
            "AS4902 + novation",
            "AIA 2019 novation survey",
            "authority lost by contract alone",
            "mandate the Deed in gov work",
        ],
    },
    "P9": {
        "title": "9 - CONDITIONS",
        "half": "change",
        "responsibility": "the individual absorbs it",
        "authority": "no instrument to change it",
        "joined": "no",
        "subtopics": [
            "4 of 5 wellbeing areas",
            "award overtime grey areas",
            "22% Fair Work claim",
            "BLF green bans",
        ],
    },
    "P10": {
        "title": "10 - WHERE THE VALUE GOES",
        "half": "change",
        "responsibility": "responsible for the outcome",
        "authority": "competition sets the price",
        "joined": "no",
        "subtopics": [
            "2% fee on a large job",
            "25% of the billable rate",
            "fee scales ended 1994",
            "transparency, not a price floor",
        ],
    },
}

# Actors / instruments band along the bottom -- every point lands on one of
# these. "The profession should..." is not an action; these are.
ACTORS = {
    "title": "ACTORS + INSTRUMENTS",
    "colour": ACTOR_COLOUR,
    "root": rg.Point3d(0, -320, 0),
    "zone_center": rg.Point3d(0, -334, 0),
    "zone_radius": 78.0,
    "subtopics": [
        "ARBV - registration, code, CPD",
        "AACA - competencies, APE",
        "Architects Act 1991",
        "NCC / Standards Australia",
        "AS4902 + Deed of Novation",
        "Government as procurer",
        "Fair Work + the award",
        "UAW vs ACA - not one interest",
    ],
}

# (point_a, point_b, relationship label) -- the coherence test.
CROSS_LINKS = [
    ("P1", "P9",  "supervision needs conditions"),
    ("P1", "P8",  "no authority on site, no supervision"),
    ("P2", "P8",  "the duty is the test"),
    ("P2", "P9",  "duty of care to the makers"),
    ("P5", "P6",  "open path, paywalled standard"),
    ("P6", "P7",  "the same invisible gate"),
    ("P8", "P9",  "no power to ask"),
    ("P9", "P10", "fees set the conditions"),
    ("P4", "P9",  "evidence base, no authority"),
]

HUB_TITLE = "RESPONSIBILITY WITHOUT AUTHORITY"
HUB_LINES = [
    "Architecture makes individuals responsible -- for the public not in the room,",
    "for rules they had no route to write, for a design they may no longer control,",
    "for conditions they cannot change alone -- then lets authority sit elsewhere.",
    "Defend the mechanisms where the two are joined. Reform belongs where they are not.",
]

KEEP_HEADER   = "MAINTAIN / REFINE -- the two sit together"
CHANGE_HEADER = "CHANGE -- the two have been separated"

STANCE_TITLE = "WHERE AI SITS -- a stance, not a point"
STANCE_LINES = [
    "A tool assists production but cannot be held",
    "responsible for the work, so the authority to",
    "decide stays with the person who is.",
    "Surfaces inside 3 (review), 6 (enclosure)",
    "and 10 (where the gains land).",
]

LEGEND_TITLE = "KEY"
LEGEND_LINES = [
    "green = responsibility and authority sit together",
    "blue  = they have been separated",
    "solid bar  = joined",
    "dashed bar = partial",
    "broken bar = separated",
    "dashed curve = a dependency between points",
    "branch weight = how much runs through it",
]


def build_zones():
    """Expand POINTS into the geometry-bearing dicts the baker consumes, and
    append the actors band. Kept as a function so the layout constants above
    remain the only place the sheet's proportions are set."""
    zones = {}
    keep = [k for k, v in POINTS.items() if v["half"] == "keep"]
    change = [k for k, v in POINTS.items() if v["half"] == "change"]

    for keys, sign, colour in ((keep, -1.0, KEEP_COLOUR),
                               (change, 1.0, CHANGE_COLOUR)):
        for row, key in enumerate(keys):
            data = dict(POINTS[key])
            y = ROW_Y[row % len(ROW_Y)]
            data["colour"] = colour
            data["root"] = rg.Point3d(sign * WING_ROOT_X, y, 0)
            data["zone_center"] = rg.Point3d(sign * WING_CENTRE_X, y, 0)
            data["zone_radius"] = ZONE_RADIUS
            zones[key] = data

    zones["ACTORS"] = dict(ACTORS)
    return zones


# =================================================================
# 3. TEXT OBSTACLES -- rectangles, not circles (LINEAGE note 3).
#    Headings and the responsibility/authority bar register themselves
#    BEFORE their zone grows, so branch direction steers around them.
#    Reset at the start of every generate_diagram() call.
# =================================================================
_obstacles = []   # list of (center_x, center_y, half_width, half_height)


def register_text_obstacle(pt, text, height, margin):
    """Approximate the text's bounding box. 0.6 * height is a serviceable
    average glyph width for the default font -- exact metrics are not worth
    querying here, since `margin` dominates."""
    half_w = 0.6 * height * max(len(text), 1) / 2.0 + margin
    half_h = height / 2.0 + margin
    _obstacles.append((pt.X, pt.Y, half_w, half_h))


def steer_from_obstacles(pt, direction, strength=0.9):
    """Push `direction` out of any rectangle it is inside, along the axis of
    least penetration -- so a wide label pushes mostly vertically and a tall
    one mostly horizontally. A1 used one circle of radius max(half_w,
    half_h), which made wide labels repel in a needlessly large disc."""
    for cx, cy, half_w, half_h in _obstacles:
        dx = pt.X - cx
        dy = pt.Y - cy
        if abs(dx) >= half_w or abs(dy) >= half_h:
            continue
        pen_x = half_w - abs(dx)
        pen_y = half_h - abs(dy)
        if pen_x < pen_y:
            away = rg.Vector3d(1.0 if dx >= 0.0 else -1.0, 0.0, 0.0)
        else:
            away = rg.Vector3d(0.0, 1.0 if dy >= 0.0 else -1.0, 0.0)
        direction = direction + away * strength
    return direction


# =================================================================
# 4. SPATIAL GRID -- bucketed nearest-node search (LINEAGE note 1).
# =================================================================
class NodeGrid(object):
    """Uniform bucket grid over the growing node cloud. Cell size is set to
    the influence radius, so the nearest node within that radius is always
    in the 3x3 block of cells around the query point."""

    def __init__(self, cell_size):
        self.cell = max(float(cell_size), 1e-6)
        self.buckets = {}

    def _key(self, x, y):
        return (int(math.floor(x / self.cell)), int(math.floor(y / self.cell)))

    def add(self, index, pt):
        self.buckets.setdefault(self._key(pt.X, pt.Y), []).append(index)

    def nearest(self, nodes, pt, max_dist):
        """Index of the closest node within max_dist, or -1. Searches the
        3x3 cell block; with cell == max_dist that block provably contains
        any node within range."""
        cx, cy = self._key(pt.X, pt.Y)
        best_i, best_d = -1, max_dist
        for gx in (cx - 1, cx, cx + 1):
            for gy in (cy - 1, cy, cy + 1):
                for i in self.buckets.get((gx, gy), ()):
                    d = nodes[i].DistanceTo(pt)
                    if d < best_d:
                        best_d, best_i = d, i
        return best_i


# =================================================================
# 5. SPACE COLONIZATION GROWTH
# =================================================================
def zone_rng(seed, zone_index):
    """Per-zone RNG (LINEAGE note 2): a zone's attractor cloud depends only
    on (seed, zone index), never on how many zones grew before it."""
    return random.Random(int(seed) * 1000003 + int(zone_index) * 8191)


def random_point_in_disc(rng, center, radius):
    r = radius * math.sqrt(rng.random())
    a = rng.random() * 2.0 * math.pi
    return rg.Point3d(center.X + r * math.cos(a), center.Y + r * math.sin(a), 0)


def seed_stem(origin, zone_center, params, nodes, parent_of, grid):
    """Walk a straight stem from `origin` to the zone centre, chaining each
    step to the last. Space colonization can only grow where an attractor is
    within influence_radius of an existing node; seeding the stem guarantees
    that regardless of how far the disc sits from the heading, so layout and
    influence_radius stop being coupled."""
    v = zone_center - origin
    d = v.Length
    if d <= params.segment_length:
        return
    v.Unitize()
    for s in range(1, int(d / params.segment_length) + 1):
        pt = origin + v * (s * params.segment_length)
        nodes.append(pt)
        parent_of[len(nodes) - 1] = len(nodes) - 2
        grid.add(len(nodes) - 1, pt)


def grow_branches(root_pt, zone_center, zone_radius, rng, params):
    """Classic space colonization: attractors pull the nearest node within
    the influence radius; each influenced node steps once along the average
    direction of its attractors; attractors closer than kill_distance to any
    node are consumed. A stem is seeded from root_pt to the zone centre
    first. Returns (nodes, parent_of)."""
    # Scale the count by AREA so every zone gets the same attractor density.
    # attractors_per_zone is the count for a ZONE_RADIUS disc; the wider
    # actors band needs proportionally more or it grows a sparse stub with
    # too few tips to label.
    n_attractors = max(8, int(params.attractors_per_zone
                              * (zone_radius / ZONE_RADIUS) ** 2))
    attractors = [random_point_in_disc(rng, zone_center, zone_radius)
                  for _ in range(n_attractors)]
    nodes = [root_pt]
    parent_of = {0: -1}

    grid = NodeGrid(params.influence_radius)
    grid.add(0, root_pt)
    seed_stem(root_pt, zone_center, params, nodes, parent_of, grid)

    for _ in range(int(params.max_iterations)):
        if not attractors:
            break

        dir_sum = {}
        counts = {}
        for a in attractors:
            i = grid.nearest(nodes, a, params.influence_radius)
            if i < 0:
                continue
            v = a - nodes[i]
            if v.Length > 1e-9:
                v.Unitize()
                dir_sum[i] = dir_sum.get(i, rg.Vector3d(0, 0, 0)) + v
                counts[i] = counts.get(i, 0) + 1

        if not dir_sum:
            break

        grew = False
        for i, vsum in dir_sum.items():
            avg = vsum / counts[i]
            if avg.Length > 1e-9:
                avg.Unitize()
            avg = steer_from_obstacles(nodes[i], avg)
            if avg.Length > 1e-9:
                avg.Unitize()
            else:
                continue
            new_pt = nodes[i] + avg * params.segment_length
            nodes.append(new_pt)
            parent_of[len(nodes) - 1] = i
            grid.add(len(nodes) - 1, new_pt)
            grew = True

        if grew:
            # New nodes are already in the grid, so one bucketed lookup per
            # attractor replaces A1's full scan against every node.
            attractors = [a for a in attractors
                          if grid.nearest(nodes, a, params.kill_distance) < 0]

    return nodes, parent_of


def subtree_sizes(nodes, parent_of):
    """Tips supported by each node (LINEAGE note 4). Space colonization only
    ever appends a child after its parent, so parent index < child index and
    one reverse pass is enough -- no recursion, no sort."""
    sizes = [1] * len(nodes)
    for i in range(len(nodes) - 1, 0, -1):
        p = parent_of.get(i, -1)
        if p >= 0:
            sizes[p] += sizes[i]
    return sizes


def find_leaf_tips(nodes, parent_of):
    """Leaf indices, farthest from the root first."""
    is_parent = set(parent_of.values())
    leaves = [i for i in range(len(nodes)) if i not in is_parent and i != 0]
    leaves.sort(key=lambda i: nodes[i].DistanceTo(nodes[0]), reverse=True)
    return leaves


def spread_tips(nodes, leaves, center, wanted, pool=160, rim_frac=0.55):
    """Pick `wanted` tips spread around the zone rather than simply the
    longest `wanted`, which in A1 tended to stack every label on one side.

    Candidates are RIM tips -- those at least `rim_frac` of the way from the
    zone centre to its farthest tip. Selecting by distance from the growth
    stem instead (the obvious reading of "longest") picks an outboard arc,
    which is angularly narrow and leaves the spread step nothing to work
    with: measured, all four of one zone's labels landed within 1 degree.
    Distance from the CENTRE picks tips all the way around the disc, and
    they point outward, which is also where a label wants to sit.

    Greedy thereafter: farthest tip first, then whichever candidate is
    angularly farthest from everything already chosen."""
    if wanted <= 0 or not leaves:
        return []

    def radius_of(i):
        return nodes[i].DistanceTo(center)

    def angle_of(i):
        v = nodes[i] - center
        return math.atan2(v.Y, v.X)

    far = max(radius_of(i) for i in leaves)
    rim = [i for i in leaves if radius_of(i) >= rim_frac * far] or list(leaves)
    rim.sort(key=radius_of, reverse=True)
    stride = max(1, len(rim) // pool)
    candidates = rim[::stride][:pool]
    if len(candidates) < wanted:
        candidates = rim[:max(wanted, len(candidates))]

    chosen = [candidates[0]]
    while len(chosen) < wanted and len(chosen) < len(candidates):
        best_i, best_gap = None, -1.0
        for c in candidates:
            if c in chosen:
                continue
            gap = min(abs(math.atan2(math.sin(angle_of(c) - angle_of(s)),
                                     math.cos(angle_of(c) - angle_of(s))))
                      for s in chosen)
            if gap > best_gap:
                best_gap, best_i = gap, c
        if best_i is None:
            break
        chosen.append(best_i)
    return chosen


# =================================================================
# 6. RHINO OUTPUT HELPERS
# =================================================================
LAYER_ROOT = "Manifesto::"


def ensure_layer(name, colour):
    if not rs.IsLayer(name):
        rs.AddLayer(name, colour)
    return name


def clear_diagram_layers(status_cb):
    """Delete objects left over from a previous Generate click, so re-running
    from the GUI doesn't pile up duplicate geometry."""
    removed = 0
    for layer in (rs.LayerNames() or []):
        if layer.startswith(LAYER_ROOT):
            ids = rs.ObjectsByLayer(layer)
            if ids:
                rs.DeleteObjects(ids)
                removed += len(ids)
    if removed:
        status_cb("Cleared {} objects from the previous bake.".format(removed))


def force_annotation_scale_to_one(status_cb):
    """See the ANNOTATION-SCALE FIX note at the top of this file. Best-effort:
    if the RhinoCommon API shape differs from expected this logs the traceback
    rather than killing the whole generate, and the fallback is the manual fix
    (Document Properties > Annotation > Model Space Scale)."""
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
        status_cb("Could not auto-fix annotation scale -- set Document "
                  "Properties > Annotation > Model Space Scale manually:\n"
                  + traceback.format_exc())


def add_text(text, pt, height, colour, layer, style=0, justification=0):
    tid = rs.AddText(text, pt, height, None, style, justification)
    rs.ObjectLayer(tid, layer)
    rs.ObjectColor(tid, colour)
    return tid


def add_text_block(lines, pt, height, colour, layer, style=0, leading=1.8):
    """Stack lines downward from pt. rs.AddText has no multiline mode we can
    rely on across templates, so each line is baked separately."""
    ids = []
    for i, line in enumerate(lines):
        p = rg.Point3d(pt.X, pt.Y - i * height * leading, 0)
        ids.append(add_text(line, p, height, colour, layer, style))
    return ids


def set_print_width(obj_id, width_mm):
    """Per-object print width. Wrapped: not every template/version exposes
    it, and a missing line weight must not fail the bake."""
    try:
        rs.ObjectPrintWidth(obj_id, width_mm)
    except Exception:
        pass


def try_dashed(obj_id):
    try:
        rs.ObjectLinetype(obj_id, "Dashed")
    except Exception:
        pass  # template has no "Dashed" linetype -- leave solid, not fatal


# =================================================================
# 7. THE ARGUMENT: the responsibility -> authority bar
# =================================================================
# All zone text (heading, resp, auth) is baked with the same justification
# value, so the three lines always agree with each other whatever the
# template does with it. The connector bar is drawn relative to the same
# anchor. If the block sits off-centre under the heading on the first
# click-test, this is the one number to change.
BAR_ANCHOR_DX = 0.0
BAR_HALF_LEN = 30.0
ZONE_TEXT_JUSTIFICATION = 1


def bake_responsibility_bar(data, params, layer):
    """The manifesto's core device, as a compact stack under the heading:

        resp: who carries it
        ---------------------   <- solid | dashed | broken
        auth: who holds it

    The connector's state IS the claim -- solid = joined, dashed = partial,
    broken (a real gap) = separated -- so the CHANGE wing reads as a column
    of broken bars at a glance."""
    colour = data["colour"]
    root = data["root"]
    anchor_x = root.X + BAR_ANCHOR_DX

    resp_pt = rg.Point3d(anchor_x, root.Y - params.heading_height * 1.5, 0)
    bar_y = root.Y - params.heading_height * 2.1
    auth_pt = rg.Point3d(anchor_x, root.Y - params.heading_height * 2.9, 0)

    add_text("resp: " + data["responsibility"], resp_pt, params.pair_height,
             colour, layer, justification=ZONE_TEXT_JUSTIFICATION)
    add_text("auth: " + data["authority"], auth_pt, params.pair_height,
             colour, layer, justification=ZONE_TEXT_JUSTIFICATION)
    register_text_obstacle(resp_pt, data["responsibility"], params.pair_height,
                           params.text_obstacle_margin)
    register_text_obstacle(auth_pt, data["authority"], params.pair_height,
                           params.text_obstacle_margin)

    a = rg.Point3d(anchor_x - BAR_HALF_LEN, bar_y, 0)
    b = rg.Point3d(anchor_x + BAR_HALF_LEN, bar_y, 0)
    state = data.get("joined", "yes")

    if state == "yes":
        ids = [rs.AddLine(a, b)]
    elif state == "partial":
        ids = [rs.AddLine(a, b)]
        try_dashed(ids[0])
    else:
        gap = BAR_HALF_LEN * 0.55
        s1 = rg.Point3d(anchor_x - gap, bar_y, 0)
        s2 = rg.Point3d(anchor_x + gap, bar_y, 0)
        ids = [rs.AddLine(a, s1), rs.AddLine(s2, b)]

    for i in ids:
        rs.ObjectLayer(i, layer)
        rs.ObjectColor(i, colour)
        set_print_width(i, params.trunk_width)
    return ids


# =================================================================
# 8. BAKING A ZONE
# =================================================================
def bake_branches(nodes, parent_of, sizes, colour, layer, params):
    """One line per segment, print width interpolated between twig_width and
    trunk_width by how many tips the segment carries."""
    max_size = max(sizes) if sizes else 1
    for i in range(1, len(nodes)):
        line_id = rs.AddLine(nodes[parent_of[i]], nodes[i])
        rs.ObjectLayer(line_id, layer)
        rs.ObjectColor(line_id, colour)
        if params.draw_weights and max_size > 1:
            t = (sizes[i] - 1.0) / float(max_size - 1)
            set_print_width(line_id,
                            params.twig_width
                            + (params.trunk_width - params.twig_width) * t)


def bake_zone_text(key, data, params):
    """PASS 1 -- headings and the responsibility/authority bar for EVERY zone,
    before any zone grows. Growth steers around registered text, so unless
    the whole obstacle field exists up front the zone baked first grows
    freely into space the zone baked last is forbidden, purely by ordering.
    Measured before this split: node counts ran from 127 to 1595 across
    same-sized zones."""
    colour = data["colour"]
    layer = ensure_layer(LAYER_ROOT + key, colour)
    rs.CurrentLayer(layer)

    heading = data.get("title", key)
    register_text_obstacle(data["root"], heading, params.heading_height,
                           params.text_obstacle_margin)
    add_text(heading, data["root"], params.heading_height, colour, layer,
             style=1, justification=1)   # bold, centred

    if "responsibility" in data:
        bake_responsibility_bar(data, params, layer)
    return layer


def bake_zone_growth(key, data, zone_index, params, layer):
    """PASS 2 -- grow the zone and label its tips."""
    colour = data["colour"]
    rs.CurrentLayer(layer)
    rng = zone_rng(params.seed, zone_index)
    nodes, parent_of = grow_branches(data["root"], data["zone_center"],
                                     data["zone_radius"], rng, params)
    sizes = subtree_sizes(nodes, parent_of)
    bake_branches(nodes, parent_of, sizes, colour, layer, params)

    leaves = find_leaf_tips(nodes, parent_of)
    subtopics = data["subtopics"]
    # angles measured from the zone CENTRE, not the root -- from the root
    # every tip of an outboard disc reads as roughly the same bearing
    tips = spread_tips(nodes, leaves, data["zone_center"], len(subtopics))
    label_layer = ensure_layer(LAYER_ROOT + "Labels", (40, 40, 40))

    for label, tip_i in zip(subtopics, tips):
        tip = nodes[tip_i]
        direction = tip - nodes[parent_of[tip_i]]
        if direction.Length > 1e-9:
            direction.Unitize()
        else:
            direction = rg.Vector3d(1, 0, 0)
        label_pt = tip + direction * (params.subtopic_height * 0.8 + 2.0)
        add_text(label, label_pt, params.subtopic_height, colour, label_layer)

    return {"root": data["root"], "colour": colour,
            "labelled": len(tips), "wanted": len(subtopics),
            "nodes": len(nodes)}


def bake_cross_links(results, params):
    layer = ensure_layer(LAYER_ROOT + "CrossLinks", LINK_COLOUR)
    rs.CurrentLayer(layer)

    drawn = 0
    for key_a, key_b, label in CROSS_LINKS:
        if key_a not in results or key_b not in results:
            continue
        pt_a = results[key_a]["root"]
        pt_b = results[key_b]["root"]
        mid = rg.Point3d((pt_a.X + pt_b.X) / 2.0, (pt_a.Y + pt_b.Y) / 2.0, 0)
        perp = rg.Vector3d(-(pt_b.Y - pt_a.Y), pt_b.X - pt_a.X, 0)
        if perp.Length > 1e-9:
            perp.Unitize()
        # bow the midpoint so links read as curves, not straight rules; the
        # per-link offset keeps the nine of them from stacking in the centre
        bow = pt_a.DistanceTo(pt_b) * (0.10 + 0.02 * (drawn % 4))
        mid = mid + perp * bow

        curve_id = rs.AddInterpCurve([pt_a, mid, pt_b])
        rs.ObjectLayer(curve_id, layer)
        rs.ObjectColor(curve_id, LINK_COLOUR)
        set_print_width(curve_id, params.twig_width)
        try_dashed(curve_id)

        add_text(label, mid + perp * 3.0, params.link_label_height,
                 LINK_COLOUR, layer, style=2)   # italic
        drawn += 1
    return drawn


def bake_annotations(params):
    """Hub, wing headers, legend and the AI stance note -- the sheet's
    framing. The style guide asks for a legend on every diagram."""
    layer = ensure_layer(LAYER_ROOT + "Frame", HUB_COLOUR)
    rs.CurrentLayer(layer)

    hub_pt = rg.Point3d(0, 305, 0)
    register_text_obstacle(hub_pt, HUB_TITLE, params.heading_height * 1.5,
                           params.text_obstacle_margin)
    add_text(HUB_TITLE, hub_pt, params.heading_height * 1.5, HUB_COLOUR,
             layer, style=1, justification=ZONE_TEXT_JUSTIFICATION)
    add_text_block(HUB_LINES, rg.Point3d(-190, 288, 0), params.subtopic_height,
                   HUB_COLOUR, layer)

    add_text(KEEP_HEADER, rg.Point3d(-WING_ROOT_X, 262, 0),
             params.subtopic_height * 1.5, KEEP_COLOUR, layer,
             style=1, justification=ZONE_TEXT_JUSTIFICATION)
    add_text(CHANGE_HEADER, rg.Point3d(WING_ROOT_X, 262, 0),
             params.subtopic_height * 1.5, CHANGE_COLOUR, layer,
             style=1, justification=ZONE_TEXT_JUSTIFICATION)

    notes = ensure_layer(LAYER_ROOT + "Notes", NOTE_COLOUR)
    add_text(LEGEND_TITLE, rg.Point3d(-345, 305, 0),
             params.subtopic_height * 1.2, NOTE_COLOUR, notes, style=1)
    add_text_block(LEGEND_LINES, rg.Point3d(-345, 294, 0),
                   params.link_label_height, NOTE_COLOUR, notes)

    add_text(STANCE_TITLE, rg.Point3d(240, 305, 0),
             params.subtopic_height * 1.2, NOTE_COLOUR, notes, style=1)
    add_text_block(STANCE_LINES, rg.Point3d(240, 294, 0),
                   params.link_label_height, NOTE_COLOUR, notes)


# =================================================================
# 9. GENERATE -- one full regenerate cycle from the GUI.
# =================================================================
def generate_diagram(params, status_cb):
    started = time.time()
    del _obstacles[:]

    force_annotation_scale_to_one(status_cb)
    clear_diagram_layers(status_cb)

    zones = build_zones()

    sc.doc.Views.RedrawEnabled = False
    try:
        if params.draw_annotations:
            bake_annotations(params)

        layers = {}
        for key, data in zones.items():
            layers[key] = bake_zone_text(key, data, params)

        results = {}
        for zone_index, (key, data) in enumerate(zones.items()):
            results[key] = bake_zone_growth(key, data, zone_index, params,
                                            layers[key])

        links = bake_cross_links(results, params)
    finally:
        sc.doc.Views.RedrawEnabled = True

    rs.ZoomExtents()

    total_nodes = sum(r["nodes"] for r in results.values())
    status_cb("Generated {} zones, {} branch nodes, {} cross-links in {:.1f}s.".format(
        len(results), total_nodes, links, time.time() - started))

    short = [k for k, r in results.items() if r["labelled"] < r["wanted"]]
    if short:
        status_cb("Too few branch tips to label every subtopic in: "
                  + ", ".join(sorted(short))
                  + " -- raise Attractors/zone, or lower Kill distance.")


# =================================================================
# 10. GUI
# =================================================================
class ManifestoForm(eforms.Form):

    def __init__(self):
        eforms.Form.__init__(self)   # required for Rhino 8 CPython inheritance
        self.Title = "Manifesto Diagram Generator (A2)  v0.1"
        self.Resizable = True
        self.ClientSize = edrawing.Size(440, 660)
        self.Padding = edrawing.Padding(8)
        self.BackgroundColor = TH["bg_form"]

        self.params = GrowthParams()
        self._build_ui()

    def _build_ui(self):
        w = Widgets()
        lay = w.layout()
        p = self.params

        lay.AddRow(w.section("Growth"))
        self._seed = w.num(p.seed, 0, 9999)
        lay.AddRow(w.row("Random seed", self._seed))
        self._influence = w.num(p.influence_radius, 4, 60, dec=1)
        lay.AddRow(w.row("Influence radius", self._influence))
        self._kill = w.num(p.kill_distance, 1, 20, dec=1)
        lay.AddRow(w.row("Kill distance", self._kill))
        self._segment = w.num(p.segment_length, 0.5, 10, dec=1)
        lay.AddRow(w.row("Segment length", self._segment))
        self._iterations = w.num(p.max_iterations, 50, 2000, dec=0, inc=10)
        lay.AddRow(w.row("Max iterations", self._iterations))
        self._attractors = w.num(p.attractors_per_zone, 10, 400, dec=0, inc=5)
        lay.AddRow(w.row("Attractors / zone", self._attractors))

        lay.AddRow(w.section("Text (mm -- annotation scale forced to 1:1 first)"))
        self._heading_h = w.num(p.heading_height, 1, 40, dec=1)
        lay.AddRow(w.row("Heading height", self._heading_h))
        self._subtopic_h = w.num(p.subtopic_height, 0.5, 20, dec=1)
        lay.AddRow(w.row("Subtopic height", self._subtopic_h))
        self._pair_h = w.num(p.pair_height, 0.5, 20, dec=1)
        lay.AddRow(w.row("Resp/auth height", self._pair_h))
        self._link_h = w.num(p.link_label_height, 0.5, 20, dec=1)
        lay.AddRow(w.row("Link label height", self._link_h))

        lay.AddRow(w.section("Line weight (mm)"))
        self._trunk = w.num(p.trunk_width, 0.01, 3.0, dec=2, inc=0.05)
        lay.AddRow(w.row("Trunk width", self._trunk))
        self._twig = w.num(p.twig_width, 0.01, 3.0, dec=2, inc=0.05)
        lay.AddRow(w.row("Twig width", self._twig))

        self._weights = w.check("Scale branch weight by subtree size", p.draw_weights)
        lay.AddRow(self._weights)
        self._annotations = w.check("Draw hub, wing headers, legend + stance note",
                                    p.draw_annotations)
        lay.AddRow(self._annotations)

        self._btn_generate = w.button("Generate", self._on_generate, width=110, primary=True)
        self._btn_clear = w.button("Clear only", self._on_clear, width=110)
        lay.AddRow(w.button_row(self._btn_generate, self._btn_clear))

        self._log = w.log_area(height=180)
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
        p.pair_height = float(self._pair_h.Value)
        p.link_label_height = float(self._link_h.Value)
        p.trunk_width = float(self._trunk.Value)
        p.twig_width = float(self._twig.Value)
        p.draw_weights = bool(self._weights.Checked)
        p.draw_annotations = bool(self._annotations.Checked)
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


# =================================================================
# 11. ENTRY POINT
# =================================================================
def main():
    try:
        form = ManifestoForm()
        form.Owner = Rhino.UI.RhinoEtoApp.MainWindow
        form.Show()
    except Exception:
        print("Manifesto Diagram Generator failed to start:\n"
              + traceback.format_exc())


if __name__ == "__main__":
    main()


# =================================================================
# REDRAW NOTES -- what to look at on the first click-test
# =================================================================
# 1. Vertical crowding. Rows sit 82mm apart with a 33mm zone radius, so a
#    zone's growth reaches roughly halfway to its neighbour. If tip labels
#    from adjacent points collide, drop ZONE_RADIUS before touching any
#    growth parameter.
# 2. The responsibility/authority bar sits on a fixed offset under each
#    heading and registers itself as an obstacle, but only after the heading
#    is placed. If growth still runs through it, raise the obstacle margin.
# 3. Nine cross-links cross the centre. The bow factor is staggered per link
#    (0.10 + 0.02 * n % 4) to stop the labels stacking; expect to nudge one
#    or two by hand anyway.
# 4. Branch weights need "Print display" on in Rhino to be visible on screen
#    (they always show in a PDF print). If everything looks uniform, that is
#    the first thing to check, not the code.
# 5. The sheet spans roughly 900 x 620mm including the margin notes, which
#    sit outboard at x = -430 (legend) and x = +320 (stance).
