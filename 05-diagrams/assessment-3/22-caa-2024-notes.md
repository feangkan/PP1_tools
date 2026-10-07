# 22 — Client Architect Agreement 2024, draft v1: notes and assumptions

- **Date:** 2026-10-08. **Owner:** Kankawee Maksomboon (Lead 1). **Checker:** Prani Patton (as in the Register).
- **File:** `caa/CAA 2024 - Sydney Opera House - draft v1.pdf`. This is the course's own fillable `caa2024_fullservices_digital.pdf` with the fields filled in, and **it is still editable**: open it in Adobe Acrobat or Chrome and change any field.
- **Rebuild:** `caa/build_caa.py` (run `py build_caa.py`). If you edit the PDF by hand, stop using the script, or copy your changes into it.
- **Left blank on purpose:**
  - All signatures and the client initials on every schedule page: sign them by hand.
  - The signature dates.
  - Every lump-sum fee field: the fee is a percentage fee.
- **To submit:** the tutor's instruction is to open the PDF in Chrome and choose Print > Save as PDF. That flattens it so it can be combined with the rest of the file.

## Is the GL1 letter written to the client? Yes

The letter (`letters/GL1 Introductory letter - draft v1.docx`) is addressed to **The Hon. J. J. Cahill MLA, Premier of New South Wales, for the Government of New South Wales**. That matches the CAA:

| Field | Value |
|---|---|
| Client | The Government of New South Wales |
| Client's representative | The Hon. J. J. Cahill MLA, Premier of NSW |
| Architect | Jørn Utzon, Architect, Hellebæk, Denmark |
| Date of agreement | 21.02.1957 (Register row "Client Architect Agreement") |

The letter is dated 11.02.1957, which is before the agreement as it should be.

## Values carried over from the letter (they must stay identical)

| CAA field | Value | Letter |
|---|---|---|
| Page 1, Cost of Works forecast | $9,600,000 (excl. GST) | Same |
| Item 1 percentage fees | A.1 0.90%, A.2 0.90%, A.3 0.00% (excluded), A.4 2.10%, A.5 0.30%, A.6 1.80%. **Total 6.00% = $576,000** | Same fee table |
| Item 1 time-based boxes | B.4 Illustration ✓, B.6 Other services ✓ | B.4 named in the letter |
| Item 4 consultants, client to engage | QS Rider Hunt & Partners; structural Ove Arup & Partners; mechanical and electrical Steensen & Varming; geotechnical; acoustic; theatre and stage machinery | Same list |
| Item 3 disbursements | Overseas travel, post and telegrams Denmark to Sydney, models (at cost + 15%) | Same |
| Schedule C | Three stages; the early-start warning; D.8 for redesign; ABIC SW 2018; C.2/C.3 representatives; H.8 overseas notices; E.1 engineers | The letter's "Program" and "Communication, changes and variations" sections |

## Schedule A choices

| Section | Choice | Why |
|---|---|---|
| A.1 Concept, A.2 Design Development, A.4 Construction Documentation, A.6 Contract Administration | **Included** (every line) | Full services, as in the letter |
| Approvals to prepare or submit a Planning/Development Application (A.1, A.2) and all of A.3 | **Excluded** | A Crown project, approved by the Government itself (letter assumption #9) |
| A.5 Contractor selection: tender lines | **Included** | Stage I was tendered (Register: tender issued 12.1958, returned 01.1959) |
| A.5 Contractor selection: negotiation lines | **Additional** | Later stages may be negotiated (Hornibrook, Stage II `[verify]`) |
| B.4 Illustration: 2D and 3D | **Additional** | Letter; animation excluded |
| B.6 Disputes under the building contract (B6.5–B6.9) | **Additional** | If disputes arise |
| B.1, B.2, B.3, B.5, B6.1–B6.4 | **Excluded** | The competition already did the feasibility work; no planning tribunal; no trade packages |

**Three extra lines** were added in the blank rows, all Included:
- A.1 pre-design: arrange a geotechnical investigation of Bennelong Point.
- A.1 design: resolve the roof shells with the structural engineer before the podium design is fixed.
- A.6 construction: administer a separate building contract for each stage.

## New assumptions (not in the letter) to confirm

| # | Value | Status |
|---|---|---|
| 1 | Item 2 hourly rates excl. GST: Principal $350, Team leader $250, Senior architect $200, Architect $170, Graduate $120, Technician $110 | `[A]` today's typical rates. Only used for B.4 and B.6 |
| 2 | Item 6: PI insurance not less than $10,000,000; public liability not less than $20,000,000 | `[A]` |
| 3 | Item 7A 10 business days; 7B 15% per annum | The form's defaults, written in |
| 4 | Item 5 attribution: "Jørn Utzon, Architect" / "Design: Jørn Utzon, Architect, Hellebæk, Denmark" | `[A]`. Matters later: the moral-rights question after 1966 (F.2) |
| 5 | ABN "n/a (1957)", telephone and email "n/a" | Deliberate: ABNs did not exist in 1957 |
| 6 | Architect registration no. "to be confirmed" | `[verify]` whether Utzon was registered in NSW. A good ARBV point either way (Code of Conduct cl. 4(2)(b)) |
| 7 | Building surveyor, cost consultant and the other Item 4 rows left unticked | Group choice |

The letter's assumptions (fee 6%, the stage split, A.3 excluded, contingency, Rider Hunt) are in `21-introductory-letter-notes.md`. **If any of them changes, change it in both files.**

## Links to the rest of the file

- **CAA D.8 row (Jul 1961, Register):** the Schedule C D.8 condition says in advance how the Scenario 1 redesign of the podium is handled.
- **C.3 rows (1959, 1965, 1973):** the Schedule C C.2 condition names the representative as "the Premier or a Minister he nominates", so each change is a C.3 notice.
- **SW 2018 (file 5):** Schedule C says each stage uses the ABIC Simple Works 2018 and the architect administers it (A.6 included). The SW contract sum is $9,600,000, matching the Cost of Works.
