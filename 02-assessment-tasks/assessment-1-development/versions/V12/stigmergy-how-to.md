# How to use the stigmergy (geometry in Rhino + web guide)

**Development only.** Does not replace `05-diagrams/assessment-1/stigmergy-generator.py`.

---

## Split of labour (this is the point)

| Tool | What it does |
|---|---|
| `stigmergy-generator.py` in Rhino | Geometry **and** Futura catalog text. Size unit defaults to **millimetres**. Colour chip per text type; legend defaults to black. Annotation scale is forced to 1:1. |
| `stigmergy-guide.html` | **The picture / web app.** Zoom out for main claims, zoom in for subtopics, click a dot for the sentence. Same hub positions and colours as Rhino. Lower-left legend uses **colour circles**, not the words Gold / Green / Tan. |
| `stigmergy-text-catalog.md` | Full typed catalog if you prefer a printout. |

Hide `Diagram::Text` / `Diagram::Legend` if baked type is too big; you can still letter by hand.

---

## 1. Generate the drawing (Rhino 8)

1. Script Editor → open `stigmergy-generator.py` (or `stigmergy-generator-V12.py`) → Run.  
2. Leave defaults (V12 — millimetre sizes, black legend, colour chips). Click **Generate**.  
3. Branches draw in **animated batches**. Group-to-group links are **dense stigmergy strands** (curves with print width), not pipe polysurfaces. Optional trunk pipes stay off unless you tick them.  
4. **Where the words sit (on the circle, middle-center)**
   - Title disc = DISCIPLINARY MATRIX (subtitle just under the same centre)  
   - Large filled disc = group name; zoom-out claim on the same disc, one line down  
   - Small filled disc = short label on the centre; tiny ID just above  
   - Grey diamond = relation verb on the diamond  
   - Lower-left **LEGEND**: colour circles, then group key — claim (left-aligned, not on a node)  
5. Gold (lower-centre, **largest hub**) = Victoria’s linear gated registration spine. Terracotta (overlap hub, **smaller**) = Power — not a pathway. Other colours are not fake stages: Education = formative cycle, Employment = project loop, Legislation = instrument, Ethics = duty cycle, Bodies = split + network, Procurement = contract fork, Research = code contest.  
6. If you lose an ID: select the seat → **Properties → Name**.

Font panel: Font **Futura** · **Size unit = millimetres** · Title **2.5** · Heading **2.5** · Subtopic **1.5** · Branch / ID **0.5** · Legend **1.0** · Text scale **1.0**. Legend colour defaults to **black**. Each type has a colour chip.

**Why older generates looked like 0.5–1 mm:** the GUI said “pt” and the script multiplied by 0.353 (1 print point = 0.353 mm). Title 2.0 pt became **0.71 mm** in Rhino Properties. The stepper itself was never limited to 0.5–1 (range was 0.2–24). V12 defaults to millimetres so 2.0 means 2.0 mm. Switch **Size unit** back to print points if you want the old conversion. The log after Generate lists the actual millimetre heights.

---

## 2. Open the guide (browser)

Open `stigmergy-guide.html` in Chrome / Edge / Safari (double-click the file).

| Control | Use |
|---|---|
| **Zoom out** | Only main topics — what to write large on each trunk |
| **Zoom in** | All subtopic IDs and short labels |
| **Relations** | Grey curved paths between hubs with *enables / limits / depends upon / influences / contrasts* |
| Click a dot | Side panel shows the **typed sentence** to letter |
| Print / PDF | Save a still picture if you want the guide on paper beside Rhino |

Scroll to zoom, drag to pan.

---

## 3. Allocate (your hand)

1. Upper void → *DISCIPLINARY MATRIX* / *Trusted with the title — by whom, for what?*  
2. Each large coloured dot → that group’s **zoom-out claim** (from the panel).  
3. Small dots of the same colour → catalog order along each zone (R1… R12 on gold, L1… on blue, and so on). Tips sit on organic branches, not straight fan spokes.  
4. Grey path mid-dots → one verb (X3 *enables*, X7 *limits*…). Paths run **between hubs**, not around a central ring.  
5. Power stays visually smaller than Registration.

---

## Hub map (same in both tools — nerve layout, not a clock)

Horizontal spread (~2:1). West → east:

| Region | Colour | Group |
|---|---|---|
| Far west (upper) | ● Rose | Ethics |
| Far west (lower) | ● Navy | Procurement |
| West-centre (upper) | ● Blue | Legislation |
| West-centre (lower) | ● Teal | Research |
| South-west | ● Tan | Employment |
| North-centre | ● Green | Education |
| **Lower-centre (largest)** | ● Gold | **Registration (spine)** |
| Overlap (smaller) | ● Terracotta | Power |
| East | ● Purple | Bodies |

On the sheet legend, print the **circle** and the group name — not the colour word.

Thick **highway strands** (many organic curves, not one fat tube) bundle between hubs. A **mycelial mesh** (cross-links + voids) grows densest near the gold REGISTRATION spine and opens toward the edges. Fine **capillaries** reach outward from branch tips.

---

## What the relations are doing

The relation paths are the argument, not decoration:

- Education and employment **depend upon** / **enable** registration.  
- Legislation **enables** the title and **limits** a project (Council / surveyor).  
- Research **influences** legislation (the code can be rewritten).  
- Procurement **limits** registration (title intact, authorship gone).  
- Power **contrasts** the tight title-gate with the loose code and contract.

If a viewer only reads the gold trunk and the grey verbs, they should still get the critical position.

---

## 4. Export a high-res **vector** file (keep line weight)

Linkages are **dense stigmergy curves** with print width. Optional 3D pipes live on `Diagram::Pipes` only if you tick that box (off by default). Vector export uses the centerlines.

Use **Print → PDF (Vector)** or **Export AI / SVG**. Do not Export PNG/JPG if you want real vectors.

### A. Best: Print to PDF as vector (A1)

1. Viewport: **Top**, **Parallel** projection (not Perspective).  
2. Display: **Wireframe** or **Pen** (not Shaded — shaded print can go raster).  
3. Hide the heavy 3D tubes: `Layers` → turn **off** `Diagram::Pipes`. You should still see coloured curves and filled seats.  
4. `File` → `Print…` (or Ctrl+P).  
5. Destination: **PDF**.  
6. **Output type: Vector** (not Raster). If you pick Raster, “high res” is only pixels.  
7. Size: **A1** (841 × 594 mm) landscape, or your sheet.  
8. Scale: **1:1** if the bake already sits in millimetres, or **Scale to fit** on A1.  
9. Colour: **Print color** or **Display color**.  
10. Print widths: **Use object print widths** (the script set these on every centerline).  
11. Save. Open the PDF in Illustrator or Acrobat and zoom — strokes should stay sharp.

If a stroke looks too thin in the PDF, in Rhino select that curve → Properties → **Print Width** (try 0.7–2.0 mm) and print again. Or raise **Highway trunks** / **Near-root branches** in the GUI and Generate again.

### B. Adobe Illustrator (`.ai`) or SVG

1. Hide `Diagram::Pipes` (same as above).  
2. `File` → `Export Selected` or `Export`.  
3. Format: **Adobe Illustrator (*.ai)** or **SVG (*.svg)**.  
4. View: **Top**.  
5. In the options, export **curves** (not meshes). If there is “Preserve print widths” / “Use linetypes”, turn it on.  
6. Open in Illustrator. If strokes came in at 0.25 pt, select by colour/layer and set stroke: highways ~ **3–5 pt**, near-root branches ~ **2–3 pt**, capillaries ~ **0.5–1 pt**, relation paths ~ **1 pt**. That is still vector.

SVG from Rhino sometimes drops print width. Fix strokes in Illustrator, or use the PDF from method A and `Open` that PDF in Illustrator (usually cleaner).

### C. Make2D if you want the *pipe* thickness as outlines

Only if you want the fat tube look as vector outlines (each line becomes two edges):

1. Show `Diagram::Pipes`. Top view.  
2. `Make2D` → Scene: current view, hidden-line.  
3. Export the Make2D curves to PDF/AI/SVG.

This is vector, but it is **outlines of tubes**, not a single thick stroke. Method A is usually better for the matrix.

### Do not use (if you need vectors)

- `ViewCaptureToFile` / screenshot  
- Print → **Raster** (even at 600 dpi)  
- Export PNG, JPG, TIF  

Those are pictures. Fine for a guide; not for the submission linework.

### After you letter the text

Type in Illustrator or on a printed A1. Keep the PDF/AI as the linework layer; put type on a layer above so you never rasterise the stigmergy.

---

Follow the unit AI-use policy for any wording you copy onto the submitted sheet.
