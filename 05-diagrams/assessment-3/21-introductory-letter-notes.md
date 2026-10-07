# 21 — Introductory letter (GL1), draft v1: notes and assumptions

- **Date:** 2026-10-04. **Owner:** Kankawee Maksomboon (Lead 1, Design and Client Framework). **Checker:** Prani Patton (as in the Register).
- **Files:**
  - `letters/GL1 Introductory letter - draft v1.docx`: the letter, editable in Word. **Yellow highlight = an assumed or unconfirmed value.** Check each one, then remove all highlighting before submission (Ctrl+A, then Highlight > No Color).
  - `letters/GL1 Introductory letter - draft v1 (preview).pdf`: a preview only.
  - `letters/build_intro_letter.py`: rebuilds the .docx from the template. Edit the text in the script and re-run `py build_intro_letter.py`, or simply edit the .docx in Word. If you edit in Word, stop using the script.
  - `letters/source/GL1 template CAA2019 (converted from .doc).docx`: the course template, saved as .docx.
- **Template edition:** the course folder only has the **CAA 2019** GL1. The letter uses the **CAA 2024 wording** from the Week 10 lecture (slide 30, "GL1. Introductory letter for CAA2024"), because the brief requires CAA 2024. If the tutor gives you the 2024 .doc from Acumen, compare it against this draft.
- **Helen's instruction (slide 30):** *"CAA Letter: justify how your fee, services, variations and communications will work."* The draft therefore adds a section the template doesn't have, **"Communication, changes and variations"**, which covers CAA C.2/C.3, H.1, H.8, A.1.4, D.8 and B.2.

> Gen AI check: the subject has its own USE OF GEN AI page (Canvas > Course Guide > Quick Links). Read it before submitting. This draft is a filled template for the group to check, rewrite in your own words and own. It is not a final submission.

## How the letter sets up the rest of the file

| Letter says | Where it goes next | Consistency |
|---|---|---|
| Cost of Works forecast **$9,600,000** excl. GST | CAA page 1 "Cost of Works forecast"; SW 2018 contract sum | Same figure as the Register (SW 2018 contract sum $9,600,000) and the tutor's starting figure (`10-tutor-video-notes.md`) |
| Fee **6%** = **$576,000** (incl. $10,000 Mobilisation Fee), split A.1 15%, A.2 15%, A.4 35%, A.5 5%, A.6 30%; A.3 excluded | CAA Schedule B Item 1 (percentage fees column: 0.90 / 0.90 / – / 2.10 / 0.30 / 1.80 = 6.00%) | Split follows the Week 10 fee map (concept 15%, DD 15–20%, CD 40–50%, CA 30%); A.4 is 35% to free 5% for A.5 |
| B.4 Illustration, time-based rates | CAA Schedule A Section B (B.4 "Additional") + Schedule B Item 2 rates | Fill Item 2 rates in the CAA |
| Consultants: Ove Arup & Partners, Steensen & Varming, QS, geotechnical, acoustic/stage machinery, **client to engage** (E.1) | CAA Schedule B Item 4 (tick "Client to engage") | Timeline lane D3 "Consultants"; note the sources conflict on who engaged Arup historically. The CAA E.1 model is the client. |
| Disbursements: overseas travel, courier/postage, models | CAA Schedule B Item 3 | |
| Program: podium design and documentation 18–24 months; about 4 years to practical completion of Stage I; early-start risk advice | CAA A.4 program; SW 2018 date for practical completion | Timeline: tender Dec 1958, contract 19 Feb 1959, start 2 Mar 1959, date for practical completion 26 Jan 1963 (≈ 47 months) |
| **Early-start warning:** roof loads will govern the podium design | **Scenario 1** (Jun 1961 engineer's advice, SW-12/14/11) | This is the professional-judgement thread for the ARBV letter: the architect warned, the client chose to start early, and the risk materialised |
| Representatives: Jørn Utzon / client to confirm; changes notified (C.3) | CAA page 1 "Client's representative"; Register rows for the Cahill to Heffron, Askin/Hughes and Punch changes | |
| Contingency 10% | Client's Total Project Cost budget (not in the CAA) | |

## Changes in v1.1 (2026-10-08), after comparing with the example submission

We took only ideas that strengthen our own project, and rebuilt each one on our own evidence:

| Change | Why it makes our project stronger | Our evidence |
|---|---|---|
| **Mobilisation Fee $10,000** (excl. GST), inside the 6%, deducted from A.1 | The CAA's Item 1 has an A.0 lump-sum line and our fee table ignored it. $10,000 is the £5,000 first prize at £1 = A$2 | Sources D, I (prize £5,000); G (£1 = $2) |
| **Contingency 10% to 30%** | A building with no structural precedent and untested ground needs more than a normal allowance; our own record shows the final cost was about ten times the first estimate | Tutor figures ($9.6m to $102m); sources A, G |
| **Two program options** (staged / sequential) with the risk of Option 1 stated | The letter now sets up Scenario 1 directly: the client chose to fast-track, the architect warned in writing, the podium columns later had to change (SW-12, SW-14, SW-11) | Source A (Cahill in a hurry; Stage I finished two years late); timeline D3 |
| **Variation reporting trigger (5% of contract sum)** | Gives the SW-11 price adjustment and the final certificate a visible threshold; our Scenario 1 variation is +$5,000 (about 0.05%), so it stays far below it | Tutor's worked example; CAA A.3.2 |

Not taken from the example: its client (see below), its 8% fee, its Trust-addressed letter, its GST-inclusive Register, and its 66 to 120 month program figures.

### Why our client is the Government of NSW (Premier Cahill)

- The competition was announced by Premier Cahill, who committed the Government in 1957 (timeline sources D, U).
- The tutor names the client representatives as Cahill and then Askin.
- The Sydney Opera House Trust did not exist in 1957: it was created by the Trust Act of 14 March 1961 (source V). A letter or CAA dated 1957 cannot name it as the client.
- Public Works was the client's day-to-day arm. The CAA now says so in Schedule C (C.2: the Premier or a Minister he nominates).

## Assumptions to confirm (all highlighted in the .docx)

| # | Value in the letter | Why this value | Source / status | Who confirms |
|---|---|---|---|---|
| 1 | Letter date **11 Feb 1957** | Must fall after the competition result (29 Jan 1957) and before the CAA (21 Feb 1957, Register) | `[A]`. The Register says 02.1957; if the group accepts this date, change the Register row to 11.02.1957 | Group |
| 2 | Address "Premier's Department, Sydney NSW" | Client = NSW Government, represented by Premier J. J. Cahill (timeline Parties) | `[verify]` the 1957 address | Kankawee Maksomboon |
| 3 | "subsequent correspondence" | Utzon did not visit Sydney until mid-1957 `[verify]`, so a Feb 1957 "meeting" is unlikely | `[A]` | Kankawee Maksomboon |
| 4 | Brief: large hall ≈3,000 seats; small hall ≈1,200; their uses | Competition "Conditions and Programme" (1955, the "Brown Book") | ✅ [Wikipedia: Sydney Opera House](https://en.wikipedia.org/wiki/Sydney_Opera_House); [Dictionary of Sydney](https://dictionaryofsydney.org/entry/sydney_opera_house). Some sources give 3,000–3,500 for the large hall | — |
| 5 | Rehearsal rooms, restaurant, meeting rooms, back-of-house | General reading of the competition programme | `[verify]` against the Brown Book list | Kankawee Maksomboon |
| 6 | Site "at present the Fort Macquarie tram depot" | Bennelong Point site before demolition | `[verify]` (Dictionary of Sydney) | Kankawee Maksomboon |
| 7 | Fee **6%** of Cost of Works | No sourced historical percentage was found. Utzon's actual pay is recorded as **an average of £845 a week, Sep 1957 to Jun 1961** ([City of Sydney Archives](https://archives.cityofsydney.nsw.gov.au/nodes/view/893746)). No fee scale is mandatory today (ACCC, Week 10 slide 13), so the fee must be **justified** | `[A]`: **group decision**. 6% is a placeholder for a large, complex public building; justify it in the letter and the ARBV statement | Group |
| 8 | Stage split 15/15/0/35/5/30 | Week 10 lecture fee map | `[A]` | Group |
| 9 | A.3 excluded ("Crown project: approvals by the Government") | The NSW Government is the client and the approving authority | `[A]` `[verify]`: alternatively tick A.3 as Additional | Group |
| 10 | Contingency **30%**; variation report at **5%** of the contract sum | See the v1.1 table above | `[A]` | Group |
| 11 | QS = Rider Hunt & Partners | Named as the QS in a secondary source (BDSA blog, source AB in `18-miro-board-verified.md`) | `[verify]` | Yu-Chun Ho (cost rows) |
| 12 | Program: 18–24 months; presentation "early 1958"; ≈4 years to Stage I practical completion | Matches the timeline (Red Book Mar 1958 `[verify]`; SW dates) | `[A]` | Kankawee Maksomboon |
| 13 | B.4 estimate "given before starting" | Avoids inventing a figure | `[A]`: or put a lump sum | Group |
| 14 | Option 1: podium design 18–24 months, build about 4 years; Option 2: 5–6 years design + 6–8 years construction | Option 1: matches SW dates (2 Mar 1959 to 26 Jan 1963, about 47 months). Option 2 is our estimate | `[A]` | Group |
| 15 | Mobilisation Fee $10,000 excl. GST | The £5,000 prize at £1 = A$2 | `[A]` conversion; CAA Item 1 A.0 | Group |

## Not highlighted, but check

- **Code of conduct named:** the CAA's definition of Code of Practice gives NSW as the Architects Act 2003 (NSW) / Architects Regulation 2017 (NSW). The letter names the Act; the course teaches the **Victorian** Architects Regulations 2015. Keep NSW (the site's state, CAA H.4), or ask the tutor.
- **Utzon's registration:** the CAA page 1 needs the architect's **registration number**. Whether Utzon was registered in NSW in 1957 is `[verify]`. Either way it is a strong ARBV-letter point (Code of Conduct cl. 4(2)(b)).
- **"Email counts" in 1957:** this is deliberate. The file runs the history through contemporary instruments (brief: "you are not reconstructing the historical contracts").

## Next (file 4: CAA 2024)

Fill `caa2024_fullservices_digital.pdf` with the same values:
- Page 1: parties, representatives, project, site, Cost of Works $9,600,000.
- Schedule A: ticks.
- Schedule B: Item 1 percentages, Item 2 rates, Item 3 disbursements, Item 4 consultants (client to engage), Item 5 attribution, Item 6 insurance, Item 7A/7B.
- Schedule C: special conditions, for example the staged building contracts and the early-start risk.
