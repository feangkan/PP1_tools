# 23 — Submission audit (Week 12, 2026-11-04)

**Checked:** the two group files in `D:\RMIT_SEM2 26_PROPRAC 1\Week 12\`:
- `PP MARKUP_…caa2024_fullservices_digital.pdf`: the CAA 2024. This is our draft v2 with the group's edits and **12 reviewer sticky notes**.
- `construction contract ABIC Simple Works Contract 2018.pdf`: the ABIC SW 2018, Schedules 1 to 8 filled. It is flattened (exported from Illustrator), so its fields can't be edited.

**Checked against:** the official submission tab (`12-official-tabs-confirmed.md`), the rubric (`../../02-assessment-tasks/assessment-3-brief.md`), Register v3 (`20-document-register-v3.md`), the GL1 letter (`letters/`), the Timeline workbook (`programme/`) and the example submission (`Example assessment 3/Assessment Task 3_Skilbeck_Brigit_Howard_Matte.pdf`).

**Due:** Fri 6 Nov 2026, 23:59. That is two days away.

---

## 1. Does the submission meet the requirements?

The required format is **one compiled PDF**, in this order:

| # | Required item | Where it is | Status |
|---|---|---|---|
| 1 | Contents page | none | ❌ **Missing.** Easy to make |
| 2 | **Letter to the ARBV (Part B, 1,000 words)** | none | ❌ **Missing.** Worth 1 of the 5 rubric criteria (C3), and it ties C4 together |
| 3a | Architect's Register | `document-register-v3.docx` | ⚠ Exists, but has the date and money problems below. "(suggested)" contributions are still unconfirmed |
| 3b | Introductory letter | `letters/GL1 Introductory letter - draft v1.docx` | ⚠ Exists, but still has **14 yellow assumption highlights** and is marked "draft v1" |
| 3c | Client Architect Agreement | Week 12 CAA | ⚠ Exists. It has 12 open sticky-note questions and empty signature boxes |
| 3d | ABIC SW 2018 reference copy | Week 12 ABIC | ⚠ Exists. It has 2 value errors and conflicts with the CAA and the Register (below) |
| 3e | ABIC template forms SW-12, SW-14, SW-11, SW-31 | none | ❌ **Missing.** The Word template forms aren't in any folder either |
| (A1) | Timeline of significant project events | `programme/Timeline of significant project events.xlsx` | ✅ Exists. It isn't in the tab's list, but it is a brief deliverable (A1). Put it in Appendix a, after the Register |
| — | File name `Assessment Task 3_Last name, First name` | — | `[gap]` Still not answered for a group. The example used both surnames: `Assessment Task 3_Skilbeck_Brigit_Howard_Matte` |

**Verdict: not ready to submit.** Three required parts don't exist yet (Contents, ARBV letter, the four SW forms). The parts that do exist have the coherence faults below. In the rubric, C4 (integration) and C5 (consistency) are lost through exactly these faults.

---

## 2. Are the files coherent with each other?

### A. Critical: the contract story contradicts itself

| # | Problem | Where | Why it matters |
|---|---|---|---|
| **A1** | **The ABIC covers Stage I only, but the Register closes it in 1975.** ABIC Schedule 2a special condition 1 says *"Stage I podium and substructure works only… Stage II and III excluded"*, with Civil & Civic as contractor. The Register then dates **SW-31 Final Certificate 31.05.1975**. That is the Stage III / whole-building completion, a decade after Civil & Civic left the site, and after Utzon resigned | ABIC p.7; Register rows "Practical Completion Certificate 20.10.1973", "End of DLP 20.10.1974", "Final Certificate 31.05.1975" | SW-31 must certify **the contract that SW-11 adjusted**: Stage I, Civil & Civic. Stage I reached completion in early 1963, so with the 12-month DLP its final certificate falls in **about 1964, signed by Utzon**. The example submission did the same: its ARBV letter is dated Dec 1964, "Stage 1" |
| **A2** | **"Stage I Completed 03.1963: two years late"** conflicts with the ABIC's own date for practical completion. The ABIC date is **26.01.1963**, adjusted by SW-14 to **26.02.1963**. Read against that date, March 1963 is late, so liquidated damages ($1,000/day, Item 24) apply, and no form deals with them | Register; ABIC Item 22, Item 24 | Source A gives **Feb 1963**. Using Feb 1963 puts practical completion inside the adjusted date and removes the conflict. "Two years late" then refers to the historical original program, not this contract |
| **A3** | **SW-11 +$5,000 doesn't match ABIC Item 18.** Item 18 sets adjustment-of-time costs at **$1,000 per working day**. SW-14 grants **+1 month (about 20 working days)**. Under ABIC L1.1c an architect's instruction is a *delay with costs*, so the time costs alone come to about **$20,000** | ABIC p.8 Item 18; Register SW-42/SW-14/SW-11 | Rubric C1 asks for the "contractual consequences for scope, time and cost". A marker who multiplies 20 × $1,000 sees that the figures don't add up |
| **A4** | **GST basis isn't stated.** The ABIC contract price is **$10,560,000 incl. GST**. The Register says "contract sum $9,600,000" and "SW-11 … $9,605,000", with no GST basis | ABIC Item 4; Register | SW-11 and SW-31 have to state which figure they adjust |

### B. Errors in the ABIC

| # | Problem | Fix |
|---|---|---|
| B1 | Items 13 and 14 read **"10% / 10,560,000"**. That says the cover is 10% *and* $10.56m. 10% of the contract price is **$1,056,000** | Write `$1,056,000 (10% of the contract price)` |
| B2 | The architect's registration number is **N/A** in the ABIC but **0001** in the CAA | Pick one. Recommendation: `N/A [A]` in both. Utzon was not registered in NSW, and that is a useful point for Part B |
| B3 | The owner's ABN is **N/A** in the ABIC but **00 000 000 000** in the CAA | Pick one convention. Recommendation: N/A in both |
| B4 | The cover says **"Civil&Civic Pty Ltd"**; inside it says "Civil & Civic Pty Ltd" | Fix the cover |
| B5 | The owner's representative, **"James Wilson"**, and the other names (Robert Taylor, David Brown, Australia Guarantee Bank, Alex Morgan) are invented and appear nowhere else in the file. The CAA names Premier Cahill, *"or a Minister he nominates in writing"* (Schedule C) | Keep them, but list them on one **Assumptions** page so the marker can see they are deliberate `[A]` |

### C. The CAA: the 12 group comments, answered

| Page | Comment | Answer | Action |
|---|---|---|---|
| 9 (A.1) | "Why won't we get approval from client for this?" (approval to prepare a DA) | It's excluded **because no DA is prepared**: the Minister for Public Works is the constructing authority, and the Crown approves its own works (Sydney Opera House Act 1960, backdated to 1 Jan 1957) | Add a Schedule C condition that says so |
| 9 (A.2) | "same for this?" | Same answer | Same condition |
| 10 (A.3) | "Why is the architect not submitting authority approvals? If not us, who?" | The **Client** (as the Government) obtains its own approvals. The architect still supplies the drawings under A.4 ("prepare drawings… to be submitted for statutory approval": Included) | Same condition names who does it |
| 10 (A.5) | "If the client doesn't pay us to evaluate and select the contractor…?" | They do. **A.5 (1) Tender is Included.** Only (2) *Negotiated offer* is Additional, for later stages (Hornibrook) | Answer only. No change |
| 12 (B.2) | "points 2 and 5 should be included" | Agreed in principle: survey coordination and **record (as-built) documents** matter. Mark them **Additional**, not Included, because the fee table gives B.2 no fee | Tick B.2 lines 2 and 5 as Additional, at time-based rates |
| 12 (B.3) | "Which other registered architect should the client go to?" | None is needed: there is no planning negotiation for a Crown project (see A.1) | Covered by the new Schedule C condition |
| 12 (B.5) | "This is our architectural construction set?" | No. B.5 is **trade-package** documentation for a construction manager. Our construction set is **A.4**, which is Included | Answer only |
| 12 (B.6) | "How can we administer disputes if we won't prep for tribunal?" | Two different things. The **planning**-tribunal lines are Excluded; the **building-contract dispute** lines (B6.5 to B6.9) are Additional, so we *do* act in contract disputes | Answer only |
| 13 (fee A.5) | "We earlier ticked this as excluded?" | No. Tender is Included, so A.5 = 0.300% is right | Answer only |
| 13 (fee B.5) | "Construction package ticked as excluded?" | Yes. B.5 is excluded, so its fee is blank, which is correct | Answer only |
| 13 (B.4) | "Specify the cost if the client chooses illustration" | Already priced: the **time-based** box is ticked, so Item 2's hourly rates apply | Answer only; add "time-based, Item 2" to Schedule C |
| 15 (Item 4) | "Ticked land surveyor: we need someone to draw up the site" | Agreed | Add the note "To be appointed" |

**Other CAA points:**
- **Signatures:** the CAA signature boxes are empty, while the ABIC says "Signature omitted — academic simulation". Use the same convention in both.
- **Architect's signing date:** it was removed in the group's edit. Restore **21/02/1957**.
- **Project name:** the CAA now says "The Sydney Opera House", while the 1957 letter says "National Opera House". Use **"National Opera House (now the Sydney Opera House)"** in the CAA so the two match.

### D. Letter and Register housekeeping
- **GL1 letter:** remove the 14 yellow highlights; remove "draft v1" from the file name. Its figures match the CAA: $9.6m, 6% = $576,000, $10,000 mobilisation fee, 11.02.1957, Cahill.
- **Register:** the "(suggested)" contributions must be confirmed by each person. The brief marks this column ("each student's contribution").
- **Register:** add the Stage I close-out rows (practical completion, end of DLP, final claim, SW-31) and keep 1973/1975 as grey milestones for Stage III.

### E. What is already coherent ✅
- **Dates:** letter 11.02.1957, then CAA 21.02.1957, then tender 12.1958 to 01.1959, then ABIC 19.02.1959, then possession 02.03.1959. Consistent across the letter, CAA, ABIC, Register and Timeline.
- **Cost of Works:** $9.6m, 6% fee, mobilisation fee $10,000, the same consultants (Arup, Steensen & Varming, Rider Hunt). Consistent between the letter and the CAA.
- **CAA Schedule C:** its conditions pre-set the Scenario 1 story (early start warning, D.8 redesign, B.2 instructions only through the architect, C.3 representative changes). The ABIC's special condition 3 points the same way. This is the strongest thread in the file.
- **ABIC security:** the guarantee of $264,000 = 2.5% × $10,560,000 is correct. Owner occupation and cash retention are struck out correctly.

---

## 3. Five fixes (what gets remade)

| # | Fix | Files touched | Rubric |
|---|---|---|---|
| **1** | **CAA clean-up:** apply the agreed comment outcomes (B.2 lines 2 and 5 Additional; land surveyor note; new Schedule C conditions on Crown approvals, disputes and illustration rates); restore the architect's signing date; align the ABN and registration number with the ABIC; fix the project name; then export a **flattened submission copy with no sticky notes**. Keep a separate review copy with an answer under each comment | CAA | C2, C4 |
| **2** | **ABIC corrections:** Items 13 and 14 to $1,056,000; cover "Civil & Civic"; Item 18 matched to the agreed time-cost figure (see fix 3) | ABIC | C1, C5 |
| **3** | **Close the Stage I chain:** practical completion 02.1963 (inside the SW-14 date), DLP end 02.1964, SW-31 about 03.1964 signed by Utzon, referring to SW-11; GST basis stated on every money row; SW-11 = varied work + time costs, so it adds up against Item 18 | Register (docx/xlsx/csv), Timeline workbook | C1, C4 |
| **4** | **Assumptions + conventions page:** one page that declares every `[A]` (invented names, placeholder numbers, GST on 1950s work, the $9.6m figure from the tutor, the H Vic edition of the conditions, the signature convention), plus a **form data sheet** with the exact values the SW-12/14/11/31 forms must carry | New page, in the Contents | C4, C5 |
| **5** | **Compiled submission PDF:** Contents, then the ARBV letter slot, then appendices in the official order (Register + Timeline, letter with highlights removed, CAA, ABIC, forms slot), with bookmarks. Group-written pieces drop into the two marked slots | New PDF | C5 |

## 4. What was done (2026-11-04)

Decisions taken by Kankawee:
- **SW-31 stays at 31.05.1975.** It is declared on the assumptions page: the Stage I final account is held over and certified at overall completion by Hall, Todd & Littlemore. Finding A1 is therefore *declared*, not removed. The ARBV letter should explain it.
- **SW-11 stays at +$5,000 excl. GST.** ABIC Item 18 is now **$275 incl. GST ($250 + GST)** per working day, so 20 working days × $275 = $5,500 incl. GST = $5,000 excl. GST.
- **The ARBV letter and the SW forms stay with the group.** They have marked slots in the compiled PDF and a data sheet.

| Fix | Done |
|---|---|
| 1 CAA | B.2 lines 2 and 5 marked Additional, with the time-based box ticked; land surveyor "To be appointed"; Schedule C rows A.3, B.2/B.6, B.4 added; ABN "N/A (1957)", registration no. "N/A [A]"; architect's signing date 21/02/1957 restored; project name "National Opera House (now the Sydney Opera House)"; signature boxes stamped; sticky notes removed; flattened. Separate review copy with an answer beside each note |
| 2 ABIC | Items 13 and 14 changed to $1,056,000 (10%); Item 18 changed to 275 ($250 + GST); cover changed to "Civil & Civic Pty Ltd". Each correction is placed over the original text; the "for tenders" watermark is kept |
| 3 Register + Timeline | GST basis on every money row; SW-11 tied to Item 18; internal "Register said 2019" notes removed from the Register and the Timeline; rebuilt (`programme/`); the date check still passes |
| 4 | Contents page and Conventions-and-assumptions page; `For the group - SW form data sheet.pdf` |
| 5 | Compiled PDF in the official order, with bookmarks. Builder: `submission/build_submission.py`; output: `D:\RMIT_SEM2 26_PROPRAC 1\Week 12\Ready to submit\` |

**Still open:** the H4 timing. SW-14 (11.1961) is more than 20 working days after SW-42 (09.1961), and SW-11 (04.1962) does not land in the next progress certificate (J5). Either move these dates, or explain them in the ARBV letter.

**Not in these fixes, still the group's to do:** write the **ARBV letter** (about 1,000 words); fill the **SW-12, SW-14, SW-11 and SW-31** Word template forms from the data sheet; confirm the contributions; ask the tutor about the file name.
