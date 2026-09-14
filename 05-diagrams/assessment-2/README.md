# Assessment 2 — Practice Manifesto (working folder)

Brief: `../../02-assessment-tasks/assessment-2-brief.md` · Due **Sun 20 Sep 2026**, WIP presentation Week 8 Mon.

This folder develops the manifesto the way the weekly packs develop a diagram: iteratively, sourced, with the diagram as the thinking tool. It is **study scaffolding, not submittable text** — the 2,000 words are the student's to write.

## Files

| File | What it is | Status |
|------|-----------|--------|
| `00-reengineering-from-a1.md` | Answer to "can we re-engineer Assessment 1?" + a cluster-by-cluster map of what A1 material carries into A2 and how | **v03, 2026-09-15** |
| `01-diagram.md` | Manifesto **structure** diagram — the overarching position, the 2 halves (maintain/refine ↔ change), the 10 points as nodes, the CURRENT CONDITION→…→CONSEQUENCE method spine, cross-links to actors/instruments | **v03, 2026-09-15** |
| `02-manifesto-skeleton.md` | The 10 points as a working table — each with position, mechanism, actor, action, consequence, sources, and open gaps. **Points are drafted as prompts to argue, not final wording.** | **v03, 2026-09-15** — needs the student's position decisions |
| `03-presentation-script.md` | (to add for the Week 8 WIP) | not started |
| `04-topics-context.md` | (to add) provenance table once points are locked | not started |
| `05-references.md` | (to add) Chicago bibliography for the manifesto — start from `../../06-references/week-07-bibliography.md`, which lists the Week 7 claims needing verification | not started |

## Version history — read before editing

- **v01 (2026-09-06)** — built on Week 6. AI-heavy: 6 of 10 points touched it.
- **v02 (2026-09-11)** — rewrote every point around "responsibility without authority" as the spine for all ten. **Reverted** 2026-09-14 (`310643f`) — too abstract for several points, and individual judgement read as less valued than intended.
- **v03 (2026-09-15, current)** — restores v01's simpler master position (*collective mechanisms work; the decision over who captures the value of knowledge, innovation and labour is being privatised/individualised*). "Responsibility without authority" survives, but only by name inside **Points 8 and 9**, where it's the actual explanation, not the frame for the whole manifesto. AI is down to three single-line mentions (Points 3, 6, 10) from six-plus points. Points 9 and 10 are now built on Week 7 (conditions; fee/labour value) instead of AI. **This version is committed to git**, unlike v02's scaffold work, which was made across several uncommitted edits before finally being committed and then reverted — commit early when a version is worth keeping.

## How the diagram gets made ("the recent code we have")

The Assessment 1 diagram was baked in Rhino 8 with `../assessment-1/stigmergy-generator.py` (space-colonization growth around zone headings, cross-link curves). The same script is the tool for the A2 diagram — **edit only its `CONTENT DATA` block**: replace the A1 zones (Registration Pathway, Education, …) with the A2 structure (Overarching Position at the hub; MAINTAIN/REFINE and CHANGE as the two halves; the 10 points as sub-nodes; Actors/Instruments as a cross-linked zone). `01-diagram.md`'s Mermaid version is the thinking draft that feeds that block.

## Working method (matches the brief's 4-week method)

1. **Week 6 (now):** watch the lectures, identify issues + responsible bodies/mechanisms. Per the brief, Week 6 covers both halves — pull A1 tensions where *problems* exist (→ the 5 CHANGE points) **and** where *functional/successful* mechanisms exist (→ the 5 MAINTAIN/REFINE points); draft all 10 as propositions; build the structure diagram. (`00-reengineering-from-a1.md`, `01-diagram.md`, `02-manifesto-skeleton.md`) Student decides the overarching position.
2. **Week 7 (not yet happened):** continue developing — lock the position, tighten wording, resolve open gaps, start the presentation script.
3. **Week 8:** refine to one coherent position; WIP presentation Monday; assemble combined PDF (manifesto + descriptions + draft diagrams + appendix + references); submit Sunday.

## Rules carried over

- Chicago notes-bibliography, footnotes + bibliography (rubric assesses footnoting).
- No invented citations or lecture content; independent research tagged as such (`ai-technology-research-note.md` pattern).
- Diagram style: `../../08-diagram-style/STYLE_GUIDE.md` (short nodes, networked links, legend, composite layering).
