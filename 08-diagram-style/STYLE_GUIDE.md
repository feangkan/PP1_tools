# Hybrid diagram style guide

Learned from: `examples/Proprac_II_Task_3B-2.pdf` + your BAU / PRL / OFFICE practice-model diagrams.

## Core idea

**Short-form nodes → networked links → full picture.**

Do not start with a polished poster. Build clusters of short labels, then connect them so relationships become visible.

---

## Allowed layouts (mix as needed)

| Layout | Use when… |
|--------|-----------|
| **Circular / loop** | Process that repeats (input → process → output → feedback) |
| **Mindmap / radial** | One core topic with satellite clusters |
| **Timeline / left→right** | Pathway, sequence, registration spine, history |
| **Top→down** | Hierarchy, power, governance |
| **Hybrid** | Circular core + radial branches + small linear strip (your Proprac default) |

Your Proprac pattern:

```
LEFT: Initiation / Input     CENTRE: circular process     RIGHT: Value / Output
TOP/BOTTOM branches: Structure, Labor, Operations, Cost/Revenue
BOTTOM strip (optional): linear process summary
```

---

## Node types (hierarchy)

| Node | Role | Visual (your system) |
|------|------|----------------------|
| **Main / core** | Topic or model name (e.g. BAU, Week theme) | Yellow oval / large centre |
| **Stage node** | Primary categories (3A Initiation, 3B Structure…) | Yellow pill |
| **Expansion** | Short facts, metrics, sub-points | White rounded rectangle |
| **Integrated / theory** | Ideas from Assessment 1 or named theorists | Green node |
| **Transform / shift** | Change from one model/idea to another | Blue “+ …” label |
| **List block** | Dense short-form detail beside a cluster | Text panel (still short lines) |

**Rule:** Prefer **3–8 words per node**. Put longer prose in `02-explanation.md`, not on the diagram.

---

## Line types (relationship language)

Match Assessment 1 relational verbs where useful: *enables / limits / depends upon / influences / causes / prevents*.

| Line | Meaning | Use for |
|------|---------|---------|
| **Solid black →** | Primary connection / main flow | Process steps, spine |
| **Dashed black - - →** | Relationship / secondary link | Indirect influence |
| **Dotted curved** | Feedback loop | Output returns to initiation |
| **Coloured solid (teal/blue)** | Cross-topic or Assignment link | Link Week N idea ↔ Assessment 1 |
| **Pink / special dotted** | Cross-practice transform | Model A → Model B shift |

Always keep a **legend** on the diagram (see `legend.md`).

---

## Colour for grouping

| Colour | Typical grouping |
|--------|------------------|
| Yellow | Core + main stage nodes |
| White / light grey | Expansion detail |
| Green | Assessment 1 / theory integration |
| Blue | Transforms, policy/agency shifts |
| Red / warm accent (sparingly) | Tension, conflict, risk |
| Teal | Links back to Assessment 1 matrix |

Use colour for **category or hierarchy**, not decoration.

---

## Build sequence (how the agent / you should work)

1. **List short-form facts** from the week’s resources (quotes → 3–6 word labels).  
2. **Group** into 4–6 clusters (stages or themes).  
3. **Choose layout** (usually hybrid: spine/loop + branches).  
4. **Draw primary solid links** (the story spine).  
5. **Add relationship + feedback lines**.  
6. **Mark tensions / power** clearly.  
7. **Add legend + title + week label**.  
8. Produce the other 4 pack files so you can explain and present.

---

## Density rules

- Strong diagrams: **fewer nodes, clearer relationships** (same rule as Assessment 1).  
- If a cluster exceeds ~8 expansion nodes, split or move detail to explanation.  
- One diagram = **one job** (one week theme or one comparison).  
- Version as `v01`, `v02`… when you redraw.

---

## Mermaid translation (for repo drafts)

When drafting in Markdown before hand-drawing / Illustrator:

- Main flow → `flowchart` solid links  
- Feedback → dotted links (`-.->`)  
- Clusters → `subgraph`  
- Keep node labels short  

Final class presentation diagram may be redrawn in your Proprac visual language; Mermaid is the **thinking draft** stored in git.
