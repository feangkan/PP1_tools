# Assessment 3 — resources map (what each document is for, and where SOH events hit it)

Folder: `D:\RMIT_SEM2 26_PROPRAC 1\Assessment 3 resources\` (read 2026-09-26). Study scaffolding, not submittable text. Clause references are to the documents as supplied; form ↔ clause links marked `[verify]` need checking against the ABIC SW template forms (not yet supplied).

| File | For brief item | What it is | Watch-outs |
|------|----------------|-----------|------------|
| `Document Register Sample 2026-1.docx` | A2 Register | Course's "Architects Register" table: **Date · Document · Form No. · From/To · Details (cost etc) · Student Contribution**. Guide only. | Asks to **highlight the assessment forms in a different colour**. Example rows use **historical dates + A$** (cost plan 1962 A$27.5m; "Final Cost 107M" 1974) |
| `caa2019_gl1_introductoryletter (R1).doc` | A3 Intro letter | AIA guide letter GL1: fee proposal letter enclosing the draft CAA | Written for **CAA2019**. The brief wants **CAA2024**, so update clause/page references. Its **Program of services** para sets the *planned* design + construction durations, which become the timeline **baseline** |
| `caa2024_fullservices_digital.pdf` (18 pp) | A4 CAA | AIA Client Architect Agreement 2024, full services | Conditions A–M; Schedule A services; Schedule B items (fees, consultants, insurance, payment); Schedule C special conditions |
| `SW-2018-ABIC_Contract-1.pdf` (63 pp) | A5 ABIC SW | **Composite.** PDF pp.5–19 = general **ABIC SW 2018** schedules 1–8 (contract information). PDF pp.20–63 = general conditions from the **"Simple Works Contract for Housing in Vic" (SW 2018 H Vic)**, scanned, with partly garbled text | H Vic cites the Domestic Building Contracts Act (s.37, s.38, s.40) — a **housing** contract, applied here to a public building in NSW. Declare as `[A]` or ask the tutor. Clause letters A–S are the same in both |
| `The Timeline Widget – Support.url` | A1 Timeline | monday.com reference for the timeline layout | Done → `05-diagrams/assessment-3/06-timeline-workflow.md` |
| `tutor-video-transcripts/*.txt` (in `03-weekly-resources/week-09/`) | Whole brief | Two auto-transcribed videos where the tutor walks through the assessment, the three example scenarios (fully worked, with dollar/time figures), and where to get every document | **Most authoritative source in the repo for A3** — synthesised in `05-diagrams/assessment-3/10-tutor-video-notes.md`. Flags two conflicts with the written brief (group size, due date) |

Still needed: SOH Project Information & Example Scenarios PDF · ABIC SW 2018 template forms (Word) · SW 2018 User Guide · naming conventions (shown on-screen in the tutor's video, not transcribed) · *Architecture Australia* article on the plywood ribbed structural supports (mentioned in the video, not yet in this folder).

## Where to actually get the documents (from the tutor's video)

Everything above — Guide Letter 1, the CAA + its user guide, the ABIC Simple Works Contract + its user guide + the template forms — comes from the **AIA Acumen website**, reached through the **RMIT Library** login (you'll see "Good afternoon RMIT" once you're through) → **Acumen Practice Notes**, searchable directly. **Check Acumen itself for the current edition of Guide Letter 1** — the tutor notes the copy on the public site was still 2009 at the time of recording, and our supplied copy (above) is CAA2019, not CAA2024. Fill the ABIC Simple Works Contract in **Adobe**, not Word — some of its fields are text boxes rather than fillable form fields.

**Confirmed project facts, from the tutor's video** (replace `[verify]` tags elsewhere in the repo with these):

| Fact | Value |
|------|-------|
| Client representatives — only two needed | **John Cahill**, Premier of NSW, first 2 years → **Robert Askin**, remaining 6 years |
| Engineer | Ove Arup |
| Builders | **Civil and Civic**, then **Hornibrook Limited** — pick one, or use both if re-letting the contract |
| Architect team from Apr 1966 | Peter Hall (design), Lionel Todd (contract documentation), David Littlemore (contract admin) |
| Original budget | **≈$9.6 million** — "just a ballpark figure... okay if you decide to pick a different number" |
| Final cost, after adjustments | **≈$102 million** |

Full detail, including the three fully-worked example scenarios, is in `../05-diagrams/assessment-3/10-tutor-video-notes.md`.

---

## CAA 2024 — Schedule A stages = the Design timeline

| Stage | Key services (short) | Client **written approval** gate at the end | Phase |
|------|---------------------|---------------------------------------------|-------|
| B.1 Feasibility (additional) | objectives, constraints, site, key financial indicators | report accepted | P1 |
| **A.1 Concept Design** | brief, meetings, site, sketches, **preliminary Cost of Works forecast** | approve concept · proceed to DD · prepare DA | P1 |
| **A.2 Design Development** | developed design, coordinate consultants, materials schedule, **updated forecast** | approve DD · submit DA · proceed to CD | P1 |
| **A.3 Planning / DA** | authority requirements, application | — | P1 |
| **A.4 Construction Documentation** | drawings, specifications, **pre-tender forecast**, recommend contractor-selection method | submit for statutory approval · approve documents · proceed to contractor selection | P1 → P2 |
| **A.5 Contractor Selection** | (1) tender **or** (2) negotiated offer, then tender report + recommendation | accept tender | **P2** |
| **A.6 Contract Administration**: pre-construction | draft contract documents, arrange signing | approve contract documents | **P2** |
| A.6: construction | administer contract; report time/cost/progress; site visits; instructions; **assess variations, progress claims, EOT claims**; PC notice | written approval of variations "when required" | **P3** |
| A.6: post-construction | defects liability period instructions; **final certificate** | — | P3 tail |

The SOH problem, stated in CAA terms: **A.6 construction started (Mar 1959) before A.2 Design Development was finished** (roof resolved 1961). Every approval gate between them was skipped or overlapped. `[verify dates]`

## CAA 2024 clauses that map onto SOH events (Part B + rubric C2)

| Clause | Says (paraphrase) | SOH hook `[verify]` |
|--------|-------------------|---------------------|
| A.1.3 | keep accurate records; keep client informed at all stages | the Register itself; reporting on podium redesign |
| **A.1.4** | notify client **promptly** when an instruction changes the scope of Services | roof/podium redesign = scope change to Services |
| A.3 | Cost of Works forecast revised on advice; not guaranteed | £3.5m → A$102–107m |
| A.4 | program of services agreed; revised by mutual agreement | start forced before design complete |
| **A.5** | **protracted services**: notify cause, renegotiate fee + program in good faith | 1957–66 design duration far beyond plan |
| **B.2** | once a builder is appointed, client instructs the builder **only through the architect** | Minister/PWD dealing with contractors directly? |
| B.5 | client gives prompt decisions + approvals | approvals refused 1965–66 (plywood mock-ups) |
| C.3 | either party may replace its representative, with notice | Cahill → Heffron → … → Askin/Hughes |
| **D.3.3 / A.6** | overdue fees let the architect suspend services | fees withheld 1965–66 |
| **D.8** | change to Services: architect notifies fee effect → negotiate → **record in writing** | redesign of piers/columns = additional services |
| **E.1** | client-engaged consultants: **architect coordinates, is not responsible** for their services | Arup engaged directly by client; ceiling conflict (S3) |
| F.1 | architect keeps copyright; licence revocable if invoices overdue | Team II completing Utzon's design |
| K.1 / K.2 / K.4 | termination for client breach / without reason (30 business days) / consequences | Utzon resignation 28 Feb 1966 |

## ABIC SW 2018 — the Contract timeline and its clock

Milestones (Schedule 1 items in brackets):

| Event | Clause | Timing rule |
|-------|--------|-------------|
| Contract signed | Sched 1 item 1 | date of last signature |
| **Site possession** | F1 | → start of P3 |
| Contractor's program | G5 | within **10 working days** after possession |
| Updated program | G6 | when PC date moves **≥ 5 working days** |
| **Variation instruction** | J1 | any time **before PC** |
| Contractor's notice of effect (cost/time/permit) | J2.3 | within **20 working days** |
| Instruction to proceed / not proceed | J3 | within **5 working days** after information |
| Adjustment in next certificate | J5 | next certificate |
| Claim to adjust the contract: notice | H1.1a | **promptly** |
| Claim: details | H1.1b / H2 | within **20 working days** (delay claims: 20 WD after the delay ends) |
| **Architect's decision on price and/or PC date** | H4 | within **20 working days** of the claim, to contractor **and owner** |
| Delay with costs (incl. **architect's instruction**) | L1.1c | contractor notifies within **2 working days** (L3) |
| Delay without costs (weather etc.) | L2 | beyond items 20–21 allowances |
| Progress certificate | N4 | within **10 business days** of each monthly claim (item 26, default 15th) |
| **Practical completion** notice | M1 / M4 | notice within **5 working days** after inspection (item 22 date for PC) |
| Liquidated damages | M9 | item 24 rate per day |
| **Defects liability period** | M13 | item 25, default **12 months** from PC |
| Final claim | N10 | after DLP; within **20 working days** of architect's request |
| **Final certificate** | N11 | within **10 business days** of final claim; must give reasons for any difference |

### Brief forms ↔ clauses `[verify against the template forms]`

| Form | Name (brief) | Clause |
|------|--------------|--------|
| SW-40 | Contractor's RFI / instruction / notice | B1 (discrepancies), J2.3, L3 |
| **SW-12** | Architect's Instruction for a Variation | **J1** |
| SW-42 | Contractor's details of a claim | H1–H2 |
| SW-13 | Instruction to proceed / not proceed with a variation | J3 |
| **SW-14** | Adjustment of time | **H4 + L1/L2** |
| **SW-11** | Contract price adjustment | **H4 / J5** |
| SW-49 | Contractor's final claim summary | N10 |
| **SW-31** | Final certificate | **N11** |

**For Part B (reg 5.2 fairness/impartiality):** under **L1.1c an architect's instruction is a delay with costs**. If the podium redesign comes from the architect's own incomplete design, the architect still has to assess the contractor's time + cost claim fairly (H3–H4) and tell the owner (H4.1 copies the decision to the owner).
