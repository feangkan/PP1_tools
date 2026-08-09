# Synthesis — cross-week map, updated as weeks stack up

## Why this folder exists

Each `05-diagrams/week-XX/` pack is deliberately scoped to that week's sources only (`weekly-diagram-pack.mdc` rule) — that keeps each week accurate and fast to build. But it also means overlaps between weeks never get caught automatically: Week 1 and Week 2 both quietly redrew the same registration spine before anyone noticed.

This folder is the second layer: it never introduces new claims, it only draws the relationships *between* what the weekly packs already established.

## The two-layer system going forward

| Layer | Files | Updated | Rule |
|-------|-------|---------|------|
| **Weekly (raw)** | `05-diagrams/week-XX/01–05` | Once, when that week is built | Scoped to that week's sources only — never touches other weeks |
| **Synthesis (living)** | `05-diagrams/synthesis/*` | After each new week's pack is finished | Pulls only from what's already in the weekly packs — never adds new source claims |

## The process, each time a new week's pack is built

1. Build the week's normal 5-file pack as usual, scoped to that week only.
2. Skim `02-concept-index.md` — does anything in the new week touch a concept already listed?
3. Update `02-concept-index.md`: add new rows for anything recurring; leave one-off concepts unlisted (they get an "Open" row only if they look likely to recur).
4. Log the update in `03-changelog.md` — one entry, what changed and why.
5. **Rebuild `01-master-map.md` every week, stacking the new week's relationships onto the existing map.** The map is a continuously growing record of Week 1 → 2 → 3 → 4 ... — each week adds its own core-loop cluster and draws links from it back into whatever's already there (reconciled duplicates, threads, and one-off "only" clusters), rather than waiting for a milestone. See the scaling plan below for what to do once this stops being readable as one diagram.

## Scaling plan — what to do once continuous stacking stops being readable

Stacking every week into one diagram is the default. But a map with every week's clusters piled on will eventually fail the "readable at 3 distances" test your tutor flagged for Assessment 1 — likely somewhere around Week 5–6. When that happens (not before):

- **Split the master map by *thread*, not by week.** Instead of one diagram with every week's clusters, build one small diagram per recurring thread — e.g. `power-thread.md` tracing how "who holds power" evolves week by week, `ethics-thread.md` tracing altruism/public trust across weeks. Each thread diagram stays small and readable; `01-master-map.md` becomes a short index pointing to each thread file rather than trying to hold everything itself.
- Until that split happens, `02-concept-index.md` is still the thing to skim first each week — it's what tells you which existing clusters in the stacked map a new week should link into.

## Why this matters for Assessment 1

The disciplinary matrix and your critical position need exactly this kind of cross-week argument — not "here's what Week 1 said, here's what Week 2 said" but "here's how the argument develops." The concept index and thread diagrams are built to be pulled from directly when drafting Assessment 1, rather than you re-deriving the connections from scratch under deadline pressure.
