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
5. **Don't rebuild `01-master-map.md` every single week.** See scaling plan below — it gets rebuilt at milestones, not continuously.

## Scaling plan — because a 6-week single diagram won't stay readable

A master map with 2 weeks of overlaps is already a lot of clusters. By Week 5 or 6, cramming every week into one diagram will fail the same "readable at 3 distances" test your tutor flagged for Assessment 1. The plan:

- **Weekly:** only touch `02-concept-index.md` (a table — scales fine, doesn't get visually cluttered).
- **At milestones (roughly every 3 weeks, or before Assessment 1 drafting):** rebuild `01-master-map.md` from scratch using the concept index as the source list — not by bolting new clusters onto the old diagram.
- **Once threads outgrow one diagram (likely by Week 4–5):** split the master map by *thread*, not by week. Instead of one diagram with every week's clusters, build one small diagram per recurring thread — e.g. `power-thread.md` tracing how "who holds power" evolves week by week, `ethics-thread.md` tracing altruism/public trust across weeks. Each thread diagram stays small and readable; `01-master-map.md` becomes a short index pointing to each thread file rather than trying to hold everything itself.

## Why this matters for Assessment 1

The disciplinary matrix and your critical position need exactly this kind of cross-week argument — not "here's what Week 1 said, here's what Week 2 said" but "here's how the argument develops." The concept index and thread diagrams are built to be pulled from directly when drafting Assessment 1, rather than you re-deriving the connections from scratch under deadline pressure.
