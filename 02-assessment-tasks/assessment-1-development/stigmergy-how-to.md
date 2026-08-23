# How to use the stigmergy (catalog + Rhino)

**Development only.** Does not replace `05-diagrams/assessment-1/stigmergy-generator.py` or the main thinking diagram.

---

## What you are making

A circular **stigmergy** (root / nerve / coral growth):

1. **Empty centre** — title. Branches must not cross it.  
2. **Ring of main topics** — nine colour trunks around the title. Those trunks *wrap* the title; they do not go through it.  
3. **Subtopic branches** — thinner lines grow *outward* from each trunk. Tips get a small ID (R5, L4…).  
4. **You letter the words by hand** from `stigmergy-text-catalog.md`.

That matches the pictures you gave: a vacant middle, colour groups, thick trunks to thin branches, paths that bundle around rather than cut the centre.

---

## Why the old generator fought you

The first script baked long `AddText` headings. Rhino’s **annotation scale** (often 1:50 on millimetre templates) multiplied those heights, so words sat fifty times too big and ate neighbouring zones.

This version’s default is:

- **No long text in Rhino**  
- **TextDots** with catalog IDs only (R1, E3, X7) — dots stay screen-sized  
- Optional short labels, off unless you tick them  
- Title is a **keep-out circle**, not a huge annotation

You add the real sentences on paper / Illustrator / the printed A1.

---

## Files

| File | Role |
|---|---|
| `stigmergy-text-catalog.md` | Every ID, zoom-out claim, typed sentence, relation |
| `stigmergy-generator.py` | Rhino 8 Script Editor — Python 3 / CPython |
| This file | Order of work |

---

## In Rhino 8

1. New millimetre file (or your A1 template).  
2. **ScriptEditor** → Open `stigmergy-generator.py` → Run.  
3. A dark control panel opens.  
4. Leave **Bake mode** on **Markers only** for the first pass.  
5. Click **Generate**.  
6. You should see: a centre keep-out circle, nine coloured trunks on a ring, outward branches, small dots with IDs, dashed wrap-arcs for relations.  
7. Print or export a viewport. Take the catalog. Letter the zoom-out claims on the ring, then the short labels at the tips.  
8. If a zone is too thin or too hairy: change seed, attractors, or ring radius and Generate again (it clears the last bake first).

### GUI you can turn

| Control | Use |
|---|---|
| Random seed | Different branch shapes, same IDs |
| Influence / kill / segment | Hairier vs calmer growth |
| Attractors / zone | More tips (need enough for every ID) |
| Ring radius / title keep-out | How wide the wrap around the title is |
| Outward bias | How strongly branches flee the centre |
| Bake mode | Markers only · Short labels · Both |
| Draw title circle | On = reminder where to hand-letter the title |
| Draw wrap arcs | On = relation curves (X1–X12) around the title |

**Clear only** deletes `Diagram::` layers without growing a new tree.

---

## Hand-lettering order (do this on the print)

1. **Centre:** DISCIPLINARY MATRIX / *Trusted with the title — by whom, for what?*  
2. **Ring, large, in each colour:** the nine zoom-out claims.  
3. **Arcs:** one verb each (enables, limits, depends upon, influences, contrasts).  
4. **Tips:** short label from the catalog. If space dies, letter the ID only and keep the sentence in your verbal script.  
5. **Power** stays visually smaller than Registration.  
6. **Procurement** can sit on a slightly unfinished connector (dashed into Power).  
7. Legend: copy the colour table from the catalog.

---

## What “stigmergy” is doing as an argument

Branches **accrete toward unclaimed space**. That is the drawing’s claim as well as its look: the profession densely occupies the registration gate, and grows more thinly toward code-writing and novation — unless you *choose* to thicken those trunks. Colour tells the viewer which system they are in. The wrap around the title says the systems are one matrix, not nine posters.

---

## Assessment 1 — do not forget

The brief still wants:

- A legible **Victoria registration pathway** (R1–R12 *in order* along that gold trunk helps)  
- All required topics related with **enables / limits / depends upon / influences / causes / prevents**  
- A **critical position** (terracotta + the 150-word note — still the main file, not this pack)  
- Iteration (keep a v01 print before you letter v02)  
- Chicago references on the sheet or the note  
- Follow the unit AI-use policy for any assessable wording you copy from this catalog

---

## If Rhino is not open today

You can still draw the stigmergy by hand:

1. Circle in the middle (title).  
2. Nine dots on a larger circle.  
3. Gold trunk at the bottom (Registration) drawn thicker.  
4. Organic branches outward; write IDs as you go.  
5. Letter from the catalog.

The Python file is for repeating that geometry cleanly, not for writing the essay onto the screen.
