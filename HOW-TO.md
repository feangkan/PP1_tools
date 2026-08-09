# How to use PP1 Tools

Feed materials into the folders, then use these prompts with Cursor. The agent is instructed (via `.cursor/rules`) to prefer **your repo resources** over general knowledge when answering.

---

## 1. Add project info

1. Edit `01-project-info/SUBJECT_OVERVIEW.md` (subject code, outcomes, due dates).
2. Optional: add `01-project-info/schedule.md`, `contacts.md`, or the official outline PDF.

**Prompt:**  
> Read `01-project-info/` and give me a one-page study roadmap for PP1.

---

## 2. Assessment tasks — store & recheck

1. Copy each brief/rubric into `02-assessment-tasks/` (e.g. `assessment-1-brief.md`).
2. Put your draft beside it (e.g. `assessment-1-draft.md`).

**Recheck prompt:**  
> Recheck my draft in `02-assessment-tasks/assessment-1-draft.md` against the brief and rubric in the same folder.  
> Output a requirement checklist (Met / Partial / Missing) and concrete fixes. Save to `02-assessment-tasks/assessment-1-requirement-check.md`.

---

## 3. Weekly resources

For each week:

```
03-weekly-resources/week-01/
  README.md          ← topic, learning goals, file index
  lecture-notes.md   ← your notes or transcript
  readings/          ← optional subfolder for PDFs
```

Copy `templates/week-readme.md` into each new week’s `README.md`.

**Prompt:**  
> Using only `03-weekly-resources/week-02/`, summarise key concepts and list open questions. Save to `04-summaries/week-02-summary.md`.

---

## 4. Summarise content

**Prompt:**  
> Summarise [file or week folder]. Use the template in `templates/summary.md`.  
> Save to `04-summaries/<name>-summary.md`.

---

## 5. Weekly diagram pack (your hybrid style)

Style rules live in `08-diagram-style/` (learned from your Proprac II Task 3B-2 diagrams).

Each week produce **5 files** under `05-diagrams/week-XX/`:

1. Diagram (short-form nodes + networked links)  
2. Explanation (for you)  
3. Presentation script  
4. Topics context (where ideas came from)  
5. References (Chicago)

**Prompt:**  
> Using only `03-weekly-resources/week-01/`, produce a weekly diagram pack in my hybrid style (`08-diagram-style/`).  
> Save all 5 files under `05-diagrams/week-01/` using `templates/weekly-diagram-pack/`.

For a single quick Mermaid sketch only, you can still use `templates/diagram.md`.

---

## 5b. Cross-week synthesis (as weeks stack up)

Weekly packs stay scoped to one week each — overlaps between weeks (like a repeated registration spine, or the same "who holds power" question resurfacing) don't get caught automatically. `05-diagrams/synthesis/` is the second layer that catches them.

**Prompt (after finishing a new week's pack):**
> Update the synthesis layer — check `05-diagrams/synthesis/02-concept-index.md` against this week's pack and log any overlaps.

**Prompt (milestone rebuild, e.g. every 3 weeks or before Assessment 1 drafting):**
> Rebuild `05-diagrams/synthesis/01-master-map.md` from the current concept index.

See `05-diagrams/synthesis/README.md` for the full process and how it scales past a few weeks.

---

## 6. Answer questions from resources

**Prompt:**  
> Answer this question using only resources I provided under `03-weekly-resources/` (and cite which files):  
> [your question]  
> Save Q&A to `07-q-and-a/YYYY-MM-DD-topic.md`.

If the answer is not in your materials, the agent should say so instead of inventing content.

---

## 7. Chicago reference lists

1. Collect source details in `06-references/sources-raw.md` (or paste into chat).
2. Ask:

**Prompt:**  
> Format these sources as a Chicago notes-bibliography Reference List.  
> Follow `templates/chicago-reference.md`. Save to `06-references/<topic>-bibliography.md`.

Also available: footnote / endnote examples in the same template.

---

## Tips

- Drop new weeks as `week-07`, `week-08`, … when needed (copy from `templates/week-readme.md`).
- Keep drafts and finals separate (`*-draft.md` vs `*-final.md`).
- For multi-file tasks, point the agent at a folder, not a single file.
- Prefer “use only these resources” when you need citation-faithful answers for assessment work.
- Weekly packs should follow your hybrid style: short-form → network links → full picture.
