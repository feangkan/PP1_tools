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

## Composite layering — zones, types, and cross-links (formalized Week 3)

The diagram is not one layout — it's a **network of zones**, where each zone freely uses whichever layout type actually fits its content, and zones connect to each other by cross-link regardless of their internal type. This is how the hybrid diagrams have worked from Week 1 onward; naming it explicitly makes it easier to apply on purpose rather than by accident.

**Layout types available per zone** (pick per-cluster, not once for the whole diagram):

| Type | Use for |
|------|---------|
| Circular / loop | A process that feeds back into itself (e.g. a professional-identity → duties → culture → outcomes cycle) |
| Process / linear | A sequence with a clear start and end (e.g. an exam pathway, a compliance procedure) |
| Left→right timeline | Dated events, a historical sequence |
| Top-down | Hierarchy, governance, power |
| Radial / mindmap | One core idea with satellite detail |

**Two zoning axes, often both active at once:**

- **Content zoning** — within a single week's diagram, each subgraph/cluster is its own zone with its own layout type (e.g. a HISTORY cluster drawn as a left→right timeline, sitting beside a REGISTRATION cluster drawn as a linear process, sitting beside a COMPLIANCE cluster drawn as a circular loop).
- **Temporal zoning** — across weeks, each week is its own zone (see the synthesis layer, `05-diagrams/synthesis/`) — Week 1's core loop, Week 2's radial six-lens core, Week 3's linear history-to-mechanism spine, each kept in their own native shape rather than forced into one uniform layout.

**Cross-links are what make it a network, not a set of disconnected diagrams.** A dashed/dotted link between two zones is a relationship claim (this circular loop feeds that linear spine), not a directional flow — direction (`→`) only governs movement *inside* a zone. When documenting a diagram's clusters (in `04-topics-context.md` or a similar note), it's worth naming each zone's layout type once, so the composite reads as a deliberate choice rather than an accident of how Mermaid laid it out.

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

## The 3 D's — Depth, Detail, Direction (tutor booster, added Week 3)

Source: Jack Stirling's Week 3 pre-Monday email. Kept because it sharpens the existing method rather than fighting it — it describes how to **fill the page before pruning**, not a licence to leave clutter in the final pack. The two-pass workflow below is how it slots into the existing build sequence.

**Depth** — read every cluster on more than one level: expert-to-expert *and* explain-it-to-an-outsider. Cut each claim through three lenses where relevant — **ethical**, **professional/regulatory** (the repo's default lens), **historical** (what changed over time). Don't add a 6th legend colour for this — tag the lens inline in the node label or in `02-explanation.md`, e.g. "(historical)" / "(ethical)".

**Detail** — when stuck, list *everyone and everything* that actually touches the profession, the architect, or the building: consultants, the client, the public, council/planning authority, the NCC/BCA, accreditation bodies (AACA), the regulator (ARBV), the institute (AIA), insurers, and the legal right to the term "architect" itself. Pull this from the week's actual sources — this is a call to **use more of what's already in the transcript/slides**, not to invent unsourced detail (Hard rule 1 still applies).

**Direction** — the diagram needs a position, not just a map. End `02-explanation.md` with a "critical point" / "so what" the student is willing to argue, and let the diagram's primary spine visibly carry that argument rather than reading as an even, undirected bubble-and-arrow list.

### Two-pass workflow: dump → refine

1. **Pass 1 (dump, this week's draft stage):** apply Detail hard — pull in every interfacing party and mechanism the sources support, even if the diagram gets dense. This is what goes to a Monday in-class draft review.
2. **Pass 2 (refine, before the diagram is called final):** apply the existing **Density rules** below — merge, cut, or move overflow into `02-explanation.md`. The saved `01-diagram.md` in this repo should normally already reflect a refined pass; note in "Redraw notes" if a version is still mid-dump.

### Cross-week continuity lives in synthesis, not here

Don't draw links to a previous week's nodes inside a weekly `01-diagram.md` — each weekly pack stays scoped to that week's own sources only (see `.cursor/rules/weekly-diagram-pack.mdc`). The growing, stacked, cross-week map is a separate deliverable: `05-diagrams/synthesis/` (rule: `.cursor/rules/synthesis-map.mdc`). Run the synthesis update after finishing each week's pack so continuity still gets captured — just in the right file.

## Mermaid translation (for repo drafts)

When drafting in Markdown before hand-drawing / Illustrator:

- Main flow → `flowchart` solid links  
- Feedback → dotted links (`-.->`)  
- Clusters → `subgraph`  
- Keep node labels short  

Final class presentation diagram may be redrawn in your Proprac visual language; Mermaid is the **thinking draft** stored in git.
