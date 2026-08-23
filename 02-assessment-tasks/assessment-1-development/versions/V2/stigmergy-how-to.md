# How to use the stigmergy (geometry in Rhino + web guide)

**Development only.** Does not replace `05-diagrams/assessment-1/stigmergy-generator.py`.

---

## Split of labour (this is the point)

| Tool | What it does |
|---|---|
| `stigmergy-generator.py` in Rhino | **Lines and coloured dots only.** No letters. Annotation scale cannot be trusted. |
| `stigmergy-guide.html` | **The picture / web app.** Zoom out for main claims, zoom in for subtopics, click a dot for the sentence to type. Same hub positions and colours as Rhino. |
| `stigmergy-text-catalog.md` | Full typed catalog if you prefer a printout. |

You type every word by hand on the Rhino bake (or on a print of it).

---

## 1. Generate the drawing (Rhino 8)

1. Script Editor → open `stigmergy-generator.py` → Run.  
2. Leave defaults (v0.6 nerve layout). Click **Generate**. Optional: tick **Animate while generating**.  
3. You should see **thick highway trunks**, **organic capillary branches**, and **filled seats** at every place you type. Zoom out: weight and seats stay visible.  
4. **Where to letter**
   - Upper void disc + crosshair = title  
   - Large filled disc + halo = main claim (that colour)  
   - Smaller filled disc on an **organic branch tip** = subtopic (catalog order left-to-right along each zone)  
   - Grey **diamond** on a curved relation path = relation verb  
5. Gold (lower-centre, **largest hub**) = Registration spine. Terracotta (overlap hub, **smaller**) = Power.  
6. If you lose an ID: select the seat → **Properties → Name**. No letters are drawn.

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
| Far west (upper) | Rose | Ethics |
| Far west (lower) | Navy | Procurement |
| West-centre (upper) | Blue | Legislation |
| West-centre (lower) | Teal | Research |
| South-west | Tan | Employment |
| North-centre | Green | Education |
| **Lower-centre (largest)** | Gold | **Registration (spine)** |
| Overlap (smaller) | Terracotta | Power |
| East | Purple | Bodies |

Thick **highways** bundle between these hubs. Fine **capillaries** grow outward from each hub into its zone.

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

Pipes are 3D solids. They look thick in Rhino, but a clean vector file needs the **centerline curves** plus a **stroke width**. The generator now keeps both: curves on the colour layers (with print width set), pipes on `Diagram::Pipes`.

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
