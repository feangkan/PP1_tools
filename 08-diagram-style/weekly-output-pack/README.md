# Weekly output pack (5 files)

Every week, after feeding resources into `03-weekly-resources/week-XX/`, produce this pack under `05-diagrams/week-XX/`.

| # | File | For you |
|---|------|---------|
| 1 | `01-diagram.md` | Hybrid diagram linking key features |
| 2 | `02-explanation.md` | Plain explanation so you can read and explain the diagram |
| 3 | `03-presentation-script.md` | Spoken script for class (~2–4 minutes) |
| 4 | `04-topics-context.md` | Where each idea came from (file / page / slide) |
| 5 | `05-references.md` | Chicago notes-bibliography list for that week |

Templates: [`../../templates/weekly-diagram-pack/`](../../templates/weekly-diagram-pack/)

## Agent prompt (copy)

> Produce a **weekly diagram pack** for week N using only `03-weekly-resources/week-0N/`.  
> Follow `08-diagram-style/STYLE_GUIDE.md` and `legend.md`.  
> Save all 5 files to `05-diagrams/week-0N/` using the templates in `templates/weekly-diagram-pack/`.  
> Keep diagram labels short-form. Put longer prose in explanation + script.  
> Every claim in the diagram must appear in topics-context with a source path.

## Quality checks

- [ ] Legend present  
- [ ] Primary spine/loop readable in 10 seconds  
- [ ] At least one feedback or tension link  
- [ ] Explanation lets you teach the diagram without guessing  
- [ ] Script is speakable aloud (short sentences)  
- [ ] Context cites repo files (not invented sources)  
- [ ] References in Chicago format  
