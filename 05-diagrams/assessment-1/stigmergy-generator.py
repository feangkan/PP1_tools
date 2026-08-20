"""
Stigmergy / space-colonization diagram generator for Assessment 1
(The Disciplinary Matrix of Architecture)

Rhino 8 — run in the new ScriptEditor (Python 3 / CPython).
Click Run. It bakes curves + text straight into the active document.

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
"""

import random
import math
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import scriptcontext as sc

# =================================================================
# 0. RANDOM SEED -- change this integer to get a different organic
#    shape from the same data. Keep it fixed once you like a result.
# =================================================================
random.seed(7)

# =================================================================
# 1. CONTENT DATA -- edit this to match your actual brief content.
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
# 2. SPACE-COLONIZATION PARAMETERS -- tune these, not the algorithm,
#    if a zone looks too sparse / too tangled.
# =================================================================
INFLUENCE_RADIUS = 18.0
KILL_DISTANCE = 4.0
SEGMENT_LENGTH = 3.0
MAX_ITERATIONS = 500
ATTRACTORS_PER_ZONE = 90

HEADING_HEIGHT = 6.0
SUBTOPIC_HEIGHT = 2.4
LINK_LABEL_HEIGHT = 1.8
TEXT_OBSTACLE_MARGIN = 6.0   # clearance branches keep from heading text

# =================================================================
# 3. TEXT OBSTACLES -- headings register themselves here BEFORE
#    their zone grows, so branch direction steers away from them.
# =================================================================
_text_obstacles = []  # list of (center Point3d, half_width, half_height)


def register_text_obstacle(pt, text, height):
    half_w = 0.6 * height * max(len(text), 1) / 2.0
    half_h = height / 2.0
    _text_obstacles.append((pt, half_w + TEXT_OBSTACLE_MARGIN, half_h + TEXT_OBSTACLE_MARGIN))


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


def grow_branches(root_pt, zone_center, zone_radius, n_attractors):
    attractors = [random_point_in_disc(zone_center, zone_radius) for _ in range(n_attractors)]
    nodes = [root_pt]
    parent_of = {0: -1}

    for _ in range(MAX_ITERATIONS):
        if not attractors:
            break

        node_dir_sum = {}
        node_count = {}

        for a in attractors:
            nearest_i, nearest_d = -1, INFLUENCE_RADIUS
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
            new_pt = nodes[i] + avg * SEGMENT_LENGTH
            nodes.append(new_pt)
            parent_of[len(nodes) - 1] = i

        attractors = [a for a in attractors
                      if all(n.DistanceTo(a) >= KILL_DISTANCE for n in nodes)]

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


def bake_zone(zone_name, data):
    colour = data["colour"]
    layer = ensure_layer("Diagram::" + zone_name, colour)
    rs.CurrentLayer(layer)

    # heading goes down first so growth can steer around it
    register_text_obstacle(data["root"], zone_name.replace("_", " "), HEADING_HEIGHT)
    heading_id = rs.AddText(zone_name.replace("_", " "), data["root"],
                             HEADING_HEIGHT, None, 1, 1)  # bold, centered
    rs.ObjectLayer(heading_id, layer)
    rs.ObjectColor(heading_id, colour)

    nodes, parent_of = grow_branches(data["root"], data["zone_center"],
                                      data["zone_radius"], ATTRACTORS_PER_ZONE)

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
        label_pt = tip + direction * (SUBTOPIC_HEIGHT * 0.8 + 2.0)
        label_id = rs.AddText(label, label_pt, SUBTOPIC_HEIGHT, None, 0, 0)
        rs.ObjectLayer(label_id, label_layer)
        rs.ObjectColor(label_id, colour)
        tip_lookup[label] = tip

    return {"root": data["root"], "tips": tip_lookup, "colour": colour}


def bake_cross_links(zone_results):
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
        label_id = rs.AddText(label, label_pt, LINK_LABEL_HEIGHT, None, 2, 0)  # italic
        rs.ObjectColor(label_id, (120, 120, 120))


# =================================================================
# 6. RUN
# =================================================================
def main():
    sc.doc.Views.RedrawEnabled = False
    zone_results = {}
    for name, data in CATEGORIES.items():
        zone_results[name] = bake_zone(name, data)
    bake_cross_links(zone_results)
    sc.doc.Views.RedrawEnabled = True
    rs.ZoomExtents()
    print("Stigmergy diagram generated: {} zones, {} cross-links.".format(
        len(CATEGORIES), len(CROSS_LINKS)))


if __name__ == "__main__":
    main()
