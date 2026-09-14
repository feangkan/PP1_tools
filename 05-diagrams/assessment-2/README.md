# Assessment 2 — Practice Manifesto (working folder)

Brief: `../../02-assessment-tasks/assessment-2-brief.md` · Due **Sun 20 Sep 2026**, WIP presentation Week 8 Mon.

This folder develops the manifesto the way the weekly packs develop a diagram: iteratively, sourced, with the diagram as the thinking tool. It is **study scaffolding, not submittable text** — the 2,000 words are the student's to write.

## Files

| File | What it is | Status |
|------|-----------|--------|
| `00-reengineering-from-a1.md` | Answer to "can we re-engineer Assessment 1?" + a cluster-by-cluster map of what A1 material carries into A2 and how | **v02, 2026-09-11** |
| `01-diagram.md` | Manifesto **structure** diagram — the overarching position, the 2 halves (maintain/refine ↔ change), the 10 points as nodes, the CURRENT CONDITION→…→CONSEQUENCE method spine, cross-links to actors/instruments | **v02, 2026-09-11** |
| `02-manifesto-skeleton.md` | The 10 points as a working table — each with position, mechanism, actor, action, consequence, sources, and open gaps. **Points are drafted as prompts to argue, not final wording.** | **v02, 2026-09-11** — needs the student's position decisions |
| `03-presentation-script.md` | **Week 8 WIP presentation** — the slide plan (16 slides, one per point + framing, ~7 min full / ~5 min with the "short on time" cuts) and the speaking script. **Source of truth for the deck**: build slides from this so script, slides and explanation cannot drift apart. No diagram slide | v2, 2026-09-14 — each point got its own slide after v1's combined 5-point slides tested too thin |
| `04-explanation.md` | **The manifesto's content and argument** — the position, the ten points, why they hold together. Mirrors `03` section-for-section (section N = slide N). Not a diagram explanation, and not the submittable accompanying descriptions | v1, 2026-09-14 |
| `05-references.md` | (to add) Chicago bibliography for the manifesto — start from `../../06-references/week-07-bibliography.md`, which already lists the Week 7 claims needing verification | not started |
| `manifesto-generator.py` | **The Rhino 8 bake.** Paste into the ScriptEditor and Run — a dark Eto panel with growth/text/line-weight sliders, Generate and Clear. Space colonization per A1, re-engineered (spatial grid, per-zone stateless seeding, rectangular text obstacles, branch weight from subtree size, angular tip spread). Fresh A2 content throughout | v0.1, 2026-09-11 — **not yet click-tested** |
| `stigmergy-generator.py` | Earlier draft of the same bake from the same session, superseded by `manifesto-generator.py`. Kept only because it was asked to be kept — it has a known bad line in `bake_annotations` and the layout bug below. Delete when you're happy with the newer one | superseded |

## The Rhino bake

`manifesto-generator.py` draws the sheet the skeleton describes: hub at the
top, the two wings as green (joined) and blue (separated) columns, the
actors/instruments band at the bottom, and the cross-links sweeping through
the middle. Each point gets a stigmergy bush grown around its own heading,
with its **responsibility → authority bar** underneath — solid where the two
are joined, dashed for point 4, visibly broken for every CHANGE point, so
the argument is legible at a glance rather than only in the text.

Verified offline before release (Rhino stubbed, growth logic exercised
directly): all 11 zones grow, every subtopic finds a tip to sit on, output
is deterministic for a given seed, and the sheet was rendered to SVG and
looked at. Three real bugs were caught that way and fixed —

1. every point zone grew **zero branches** (roots sat 72mm from their
   attractor discs, influence radius is 18mm);
2. all four labels in a zone landed **within 1 degree of each other**;
3. node counts ran **127 to 1595** across identical zones, purely because
   zones baked later saw more text obstacles than zones baked earlier.

What offline work cannot prove is the Rhino side: text justification,
annotation scale, print widths and the `Dashed` linetype. See REDRAW NOTES
at the foot of the script for what to check on the first click-test.

## What changed at v02 (2026-09-11)

Two decisions by the student, after the Week 7 lectures:

1. **The spine changed to *responsibility without authority*.** Architecture makes individuals responsible — for the public not in the room, for rules they had no route to write, for a design they may no longer control, for conditions they cannot change alone — then lets authority over each of those sit elsewhere. Every point is now sorted by one question: *does the person carrying the responsibility hold the authority to act on it?* Together → MAINTAIN/REFINE. Separated → CHANGE. This grows out of Assessment 1's own finding (where power is mismatched) rather than importing a new subject, and it keeps the individual architect as the protagonist.
2. **AI was demoted from subject to stance.** At v01 Points 9 and 10 were entirely AI-built, with AI clauses in 1, 4, 5 and 6 — half the manifesto resting on an argument that cuts both ways. AI is now a cross-cutting position stated once (`02-manifesto-skeleton.md` §"The AI stance"): a tool assists production but cannot be held responsible for it, so the authority to decide stays with the person who is. It surfaces inside Points 3, 6 and 10 only. Background is retained in `../../02-assessment-tasks/ai-technology-research-note.md`, which now carries a re-scoping header.

Week 7 filled the gap this opened: Point 9 is now the collective instrument for working conditions, Point 10 is authority over where the value of the work goes, Point 4 gains the worker-voice and research bodies, Point 2 gains the duty of care to the people producing the building, and Point 8 gains the argument for *why* novation has resisted twenty years of advocacy.

## How the diagram gets made ("the recent code we have")

The Assessment 1 diagram was baked in Rhino 8 with `../assessment-1/stigmergy-generator.py` (space-colonization growth around zone headings, cross-link curves). **A2 no longer edits that script** — it has its own, `manifesto-generator.py` in this folder, which takes the same algorithm as its reference and re-engineers four parts of it (see the LINEAGE note at the top of the file). A1's script is left untouched so the A1 sheet stays reproducible. `01-diagram.md`'s Mermaid version remains the thinking draft; the Python is the bake.

## Working method (matches the brief's 4-week method)

1. **Week 6 (done):** watched the lectures, identified issues + responsible bodies/mechanisms; drafted all 10 as propositions; built the structure diagram. (`00-reengineering-from-a1.md`, `01-diagram.md`, `02-manifesto-skeleton.md`)
2. **Week 7 (done):** spine chosen and the 5 + 5 reworked around it; Week 7's worker/fee material integrated; AI demoted; Week 7 bibliography started (`../../06-references/week-07-bibliography.md`) and summary written (`../../04-summaries/week-07-summary.md`).
3. **Week 8 (now):** student locks the position wording and the grouping → writes the ~2,000 words → WIP presentation Monday → assemble combined PDF (manifesto + descriptions + draft diagrams + appendix + references) → submit Sunday 20 Sep.

**Immediate next actions for the student**
- Settle the four open decisions at the foot of `02-manifesto-skeleton.md` (position wording · grouping · which points get fuller paragraphs · where the AI stance appears).
- Work the `[verify]` list in `../../06-references/week-07-bibliography.md` — the fee figures, the 1994 fee-scale date and the ACA submissions are the ones most likely to be questioned.
- Draft `03-presentation-script.md` for Monday: the hub question, two wings, and two or three cross-links said aloud is enough for a WIP.

## Rules carried over

- Chicago notes-bibliography, footnotes + bibliography (rubric assesses footnoting).
- No invented citations or lecture content; independent research tagged as such (`ai-technology-research-note.md` pattern).
- Diagram style: `../../08-diagram-style/STYLE_GUIDE.md` (short nodes, networked links, legend, composite layering).
