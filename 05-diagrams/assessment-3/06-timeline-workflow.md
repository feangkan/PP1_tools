# 06 — Timeline template + Miro workflow (A1 Timeline of significant project events)

- **Date:** 2026-09-26 (**v02**: lanes and zoom frame now built from the supplied CAA 2024 and ABIC SW 2018 — see `../../02-assessment-tasks/assessment-3-resources.md`)
- **Reference:** monday.com *The Timeline Widget* (support article, read 2026-09-26) — shortcut in `D:\RMIT_SEM2 26_PROPRAC 1\Assessment 3 resources\`.
- **Files:** `timeline/` — `soh-timeline-template.png/.svg` (empty board), `soh-timeline-scenario1.png/.svg` (**our project board**: Scenario 1, Register dates, team names per lane, task-assignment panel, month-by-month zoom of the chain), `soh-timeline-scenario1-events.csv`, `build_timeline.py` (regenerates all of them).
- **Categories (as asked):** two timelines × three phases.

| | P1 Client brief → Tender | P2 Tender → Start construction | P3 Construction → Completion |
|--|--|--|--|
| **Design timeline** (architect's services, CAA Schedule A) | A.1 Concept → A.2 Design Development → A.3 DA → A.4 Construction Documentation | A.5 Contractor Selection, A.6 pre-construction (contract docs, signing) | A.6 construction + post-construction, plus on SOH **A.2 still running** (roof unresolved until 1961) |
| **Contract timeline** (procurement + ABIC SW) | procurement route | tender accepted, ABIC SW signed (Sched 1), **F1** site possession | **J1** variation → **H4** time/price → **M4** PC → **M13** DLP → **N10/N11** final claim + certificate |

The **P3 × Design** cell is the SOH story. Normally it's nearly empty. On this project the design lane runs right through construction, which is the cause of scenarios 1 and 2. The board shows it without anyone having to explain it.

## Board anatomy

| Zone | What goes there |
|------|-----------------|
| **Phase header** | P1 / P2 / P3 bands with default boundaries: competition Sep 1955 → Stage I tender ~mid 1958 `[verify]` → site possession 2 Mar 1959 → opening 20 Oct 1973, plus a final-certificate tail |
| **Year axis** | 1954–1974, one column per year, bold every 5 |
| **Design timeline lanes** | **D0 CAA services stage** (A.1–A.6 bars + **client written-approval gates**, the squares) · D1 Client + brief · D2 Architect design output · D3 Consultants (client-engaged, CAA E.1) |
| **Contract timeline lanes** | C1 Procurement + tender · C2 Construction works (Stage I/II/III) · C3 Contract administration (forms) |
| **Architects Register strip** | document-number tags under the event that issued them |
| **Event card** | the card layout, one per event |
| **Workflow** | the 10 steps below, printed on the board |
| **Inbox** | unsorted new cards |
| **Zoom frame** | the **ABIC SW clock**: SW-12 (J1) → notice (J2.3, 20 WD) → SW-13 (J3, 5 WD) → SW-42 (H1–H2, 20 WD) → SW-14/11 (H4, 20 WD) → certificate (N4, 10 BD) → PC (M4, 5 WD) → DLP (M13, 12 mo) → SW-49 (N10, 20 WD) → SW-31 (N11, 10 BD), above a month grid (1961–63 by default) |

## monday.com feature → our Miro board

| Timeline Widget feature | On the Miro board |
|---|---|
| Timeline / Date column | Year axis on the background + the card's **Date(s)** field |
| Items shown as bars | Rectangle stretched from start to end date |
| **Milestones** (diamonds) | Diamond shape. Use for one-date events: engagement, possession, PC, each form issued |
| **Group timeline bars** (group by) | Lanes: Design timeline (D1–D3) / Contract timeline (C1–C3) |
| Collapse / expand groups | Put each timeline in its own Miro frame so you can hide or focus one |
| **Color by** column | **Colour by factor**: Scope red · Time amber · Cost teal · Quality green · Responsibility violet (tutor marked Scope red) |
| Show color legend | Legend, top right |
| **Today indication** | **Scenario marker**, a red vertical line at the scenario event. A historical project has no "today". |
| Timeframe: days → years, zoom | Main board in **years**; **Zoom frame** in **months** for the scenario |
| Click a bar → item card | Miro **card** (title, description, dates, tags, assignee) |
| Filters | Miro tags (`Scope`, `[A]`, `SCENARIO`, `D2`, a student's name), found with board search |
| Dependencies / shift items | **Connectors** from cause to consequence (early start → columns inadequate → SW-12 → SW-14 → SW-11) |
| Gantt **baseline** | Grey dashed bar for the **planned** dates under the actual bar (e.g. planned PC 26 Jan 1963 vs actual 20 Oct 1973). Planned dates come from the **intro letter's "Program of services"** and **ABIC Sched 1 item 22**, so the letter, the contract and the timeline agree |

## Event card fields

`E-ID | Date(s)` · Event · Timeline / lane · Phase · Initiated by → must respond · Factor changed · `[F]` + source / `[A]` + reason · **Documents + clause** (e.g. SW-12 (J1); CAA D.8) · Student (lead / research / check)

**The gate the SOH skipped.** In lane D0, the square before 2 Mar 1959 marks where CAA would require the client's written approval of the developed design before documentation, tender and construction. On SOH the works started while A.2 was still running. Put that on the board first, because scenarios 1 and 2 follow from it.

These fields map straight onto the course's **Architects Register** columns (`Date | Document | Form No. | From/To | Details (cost etc) | Student Contribution`, from `Document Register Sample 2026-1.docx`). A card that issues a document becomes a register row with no retyping.

## Workflow (each research session)

1. Research an event, then write **one card** in the Inbox.
2. Classify it as Design or Contract timeline and drop it in its lane.
3. Place it on the year axis: a **bar** for a date range, a **diamond** for a single date.
4. Colour it by the **factor that changed**.
5. Tag it `[F]` with a source, or `[A]` with a reason. Assumptions get a **dashed outline**.
6. Draw **connectors** from cause to consequence.
7. **Planned vs actual:** put a grey dashed baseline under the actual bar.
8. **Scenario events:** give them a red star and copy them into the **Zoom frame** (months).
9. If the card issues a document, add the **Architects Register** row the same day.
10. **Weekly:** each lead checks their lanes (Lead 1: D1–D2, Lead 2: C1–C2, Lead 3: C3 + Zoom), and the consistency auditor searches by tag for gaps.

## Setting it up in Miro (about 15 minutes, once)

1. In the group's Miro board, **Upload → from device →** `soh-timeline-template.png`. It is 7400 × 2962 px, so the dates line up if you keep it at 100% scale.
2. Right-click → **Lock**, so nobody drags the background.
3. To the right of the board, build a **kit**: one card, one bar and one diamond per factor colour, a dashed version of each, a red star and a red line. Everyone duplicates from the kit (Alt-drag or Ctrl+D) so colours stay exact.
4. Create the **tags** once: the 5 factors, `[F]`, `[A]`, `SCENARIO`, the lane IDs and the three students' names.
5. **Bulk start (optional):** open `soh-timeline-scenario1-events.csv` in Excel or Sheets, copy the *Card text* column and paste it onto the board. Miro should turn each cell into a sticky `[verify this behaviour]`. The *Student* column gives each card its lane owner.
6. Take a photo or export of the board at each weekly meeting. That gives you a version history for the group.

## Rules that keep it consistent (rubric C4)

- **One event, one E-ID** on the timeline card, the register row, the correspondence and the forms.
- Dates on the timeline are the **source of truth**. Change a date here first, then everywhere else.
- **Money:** the course's own register sample uses **historical dates and A$** (e.g. cost plan 1962 A$27.5m; final cost "107M" in 1974). Default to that. `[verify]` The final-cost figure differs from the commonly cited ~A$102m, so check which figure the course uses.
- **Required forms** (SW-12, SW-14, SW-11, SW-31, CAA, ABIC SW, intro letter) get the red star on the board and are **highlighted in a different colour** in the register, as the course sample asks.

## Regenerating the board

Edit `EVENTS`, `PHASES` or `GROUPS` in `timeline/build_timeline.py`, then run it:

```
py build_timeline.py
```

It rewrites the template, the Scenario 1 board and its events CSV. Re-upload the PNG to Miro if the lanes or phases change. Moving cards doesn't need a rebuild.
