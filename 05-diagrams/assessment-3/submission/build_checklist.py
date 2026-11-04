"""Assessment 3: fix checklist PDF, one part per lead (+ whole group), from the audit in ../23-submission-audit.md.

Run:  py build_checklist.py
Writes  D:\\RMIT_SEM2 26_PROPRAC 1\\Week 12\\Ready to submit\\Checklist - fixes by lead.pdf

Page numbers ("p.") are pages of the compiled submission PDF (Assessment Task 3_..._DRAFT.pdf), as built on 04.11.2026.
Status DONE = already fixed by build_submission.py, so the lead only checks it. TO DO = the lead still has to act.
"""
import os
import pymupdf

OUT = r"D:\RMIT_SEM2 26_PROPRAC 1\Week 12\Ready to submit\Checklist - fixes by lead.pdf"
TOOLS = r"D:\Claude code\PP1_tools\05-diagrams\assessment-3"

# (priority, status, where, problem, fix)
LEAD1 = [  # Lead 1 reviewed and approved on 04.11.2026
    ("High", "DONE", "Group review copy of the CAA (separate file)",
     "The 12 sticky-note questions on the CAA now have green answers beside them.",
     "APPROVED by Lead 1 as the group's answers (04.11.2026). Other leads: tell Kankawee if you disagree with one."),
    ("High", "DONE", "b Introductory letter, p.9-13",
     "The 14 former highlights (11 Feb 1957, Premier's Department address, 30% contingency, 5% variation report, "
     "6% fee, Rider Hunt & Partners, 18-24 months, early 1958, 4 years, 5-6 and 6-8 years) needed confirming.",
     "ACCEPTED by Lead 1. Checked against Leads 2 and 3: no major issue. The 4-year podium matches the ABIC "
     "(02.03.1959 to 26.01.1963); the design period to tender (22 months) is inside 18-24; the fee, contingency "
     "and QS match the CAA. Two minor points are noted below."),
    ("Low", "NOTE", "b letter p.9 against c CAA p.15 and d ABIC p.36 (addresses)",
     "The letter goes to the 'Premier's Department, Sydney NSW'. The CAA and ABIC give the notice address as "
     "'Parliament House, Macquarie Street'.",
     "Acceptable: a letter can go to the Premier's office while the contracts give a notice address. Optional "
     "one-line fix: use Parliament House in the letter too."),
    ("Low", "NOTE", "b letter p.9-10 and c CAA p.15 against d ABIC p.37 (Item 4)",
     "The letter and CAA give $9.6m as the Cost of Works for the whole project. The ABIC uses the same $9.6m for the "
     "Stage I contract alone.",
     "Acceptable: it is the tutor's figure, declared on p.2. Lead 2 item 6: say so in the ARBV letter."),
    ("Med", "DONE", "c CAA p.15 (CAA page 1)",
     "ABN and registration no. were placeholders (00 000 000 000, 0001), which clashed with 'N/A' in the ABIC. The "
     "architect's signing date was missing. The project name did not match the letter.",
     "APPROVED. Now: ABN 'N/A (1957)', registration no. 'N/A [A]', architect's date 21/02/1957, 'National Opera "
     "House (now the Sydney Opera House)'."),
    ("Med", "DONE", "c CAA p.15",
     "Empty signature boxes, while the ABIC says 'Signature omitted - academic simulation'.",
     "APPROVED. The same wording is now stamped in the CAA's client and architect boxes."),
    ("Med", "DONE", "c CAA p.26 (Schedule A, B.2) and p.27 (Schedule B Item 1)",
     "Group comment: 'points 2 and 5 should be included'.",
     "APPROVED. B.2 lines 2 and 5 are now Additional, at time-based rates (B.2 has no % fee)."),
    ("Med", "DONE", "c CAA p.29 (Schedule B Item 4)",
     "The land surveyor was ticked but had no note.",
     "APPROVED. Note 'To be appointed' added."),
    ("Med", "DONE", "c CAA p.30 (Schedule C)",
     "Comments asked who gets approvals if A.3/B.3 are excluded, how disputes are handled, and what illustration costs.",
     "APPROVED. New rows: A.3 (Crown project: the Minister approves; we supply the drawings), B.2/B.6 (Additional "
     "at Item 2 rates; planning tribunal excluded), B.4 (Item 2 rates)."),
    ("Low", "DONE", "c CAA p.16-31 and d ABIC schedules (initials boxes)",
     "The client initials boxes are blank, in the ABIC too.",
     "DECIDED: leave them blank in both. This is consistent, and matches 'signature omitted'."),
    ("Low", "DONE", "a Register p.5-6 (C.3, D.8, engineer's advice, resignation, replacement rows)",
     "7 contributions were grey '(suggested)' names.",
     "CONFIRMED as Kankawee Maksomboon (now shown in black)."),
    ("Med", "DONE", "a Timeline, p.8",
     "The Timeline page was coloured by factor.",
     "Now the 'Timeline by party' sheet: the same lanes and events, coloured by the party who acts."),
    ("Info", "NOTE", "How to edit the CAA",
     "The CAA in the submission is rebuilt by a script from the Week 12 file. Hand edits to the output are lost.",
     "Edit the Week 12 CAA (or tell Kankawee what to change), then run py build_submission.py."),
]

LEAD2 = [
    ("High", "DONE", "d ABIC p.38 (Item 13) and p.39 (Item 14)",
     "Read '10% / 10,560,000', which says the insured amount is $10.56m. 10% of the contract price is $1,056,000.",
     "Now '$1,056,000 (10%)'. Check."),
    ("High", "DONE", "d ABIC p.39 (Item 18, adjustment of time costs)",
     "$1,000 per working day x 20 days = $20,000, but SW-11 is +$5,000.",
     "Now '275 ($250 + GST)' per working day: 20 x $275 = $5,500 incl. GST = $5,000 excl. GST, which matches SW-11. "
     "Check."),
    ("Med", "DONE", "d ABIC p.32 (cover)",
     "Typo 'Civil&Civic Pty Ltd'.",
     "Now 'Civil & Civic Pty Ltd'."),
    ("High", "TO DO", "a Register p.6 ('Stage I Completed 03.1963') against d ABIC p.40 (Item 22, Item 24)",
     "The date for practical completion is 26.01.1963, adjusted by SW-14 to 26.02.1963. March 1963 is therefore late, "
     "so liquidated damages of $1,000 per day (Item 24) apply, and no form deals with them.",
     "Recommended: date Stage I completion 02.1963 (source A says Feb 1963) in the Register and Timeline. It then falls "
     "inside the adjusted date and no damages are due. Otherwise Lead 3 must deduct the damages in SW-31."),
    ("Med", "TO DO", "d ABIC p.36 (Item 1, owner's representative), p.47 (guarantee)",
     "James Wilson, Robert Taylor, David Brown, Australia Guarantee Bank and Alex Morgan are invented and appear nowhere "
     "else in the file.",
     "Already declared on the 'Conventions and assumptions' page (p.2). Keep them, or replace James Wilson with 'The "
     "Minister for Public Works (constructing authority)', which matches CAA Schedule C (C.2)."),
    ("Med", "TO DO", "d ABIC p.37 (Item 4) against CAA p.15 (Cost of Works)",
     "The Stage I contract price ($9.6m) equals the whole-project Cost of Works forecast. That is the tutor's figure, "
     "but a reader will notice.",
     "Already declared on p.2. Make sure the ARBV letter states it as a deliberate assumption."),
    ("Low", "TO DO", "d ABIC p.45 (Schedule 3, item 6 'All other documents')",
     "Blank, although the Register says the Stage I tender included bills of quantities (12.1958).",
     "Optional: add 'Bills of quantities, Rider Hunt & Partners, Dec 1958'. The ABIC is flattened, so edit your "
     "original file and re-export it to the Week 12 folder, or ask Kankawee to place the text."),
    ("Low", "TO DO", "a Register p.4 (tender rows)",
     "Contributions are grey '(suggested)' names.",
     "Confirm or correct them in programme/register_v3.py."),
    ("Info", "TO DO", "How to edit the ABIC",
     "The ABIC was exported from Illustrator, so its fields are not editable. The fixes above are placed over the "
     "original text by build_submission.py.",
     "If you re-export the ABIC to the Week 12 folder, it must keep the same text in Items 13, 14 and 18. Otherwise "
     "the build stops, and you should tell Kankawee."),
]

LEAD3 = [
    ("High", "TO DO", "e SW forms p.95-98 (red INSERT pages)",
     "SW-12, SW-14, SW-11 and SW-31 do not exist yet. They are required.",
     "Fill the ABIC SW 2018 Word template forms from 'For the group - SW form data sheet.pdf'. Save them as SW-12.pdf, "
     "SW-14.pdf, SW-11.pdf and SW-31.pdf in Ready to submit\\inputs\\, then run py build_submission.py. Optional: "
     "SW-42.pdf and SW-13.pdf."),
    ("High", "TO DO", "SW-31 (p.98) against SW-11 (p.97)",
     "The brief says the final certificate must refer to SW-11.",
     "SW-31: 'Refers to SW-11 dated 02.04.1962'. Final contract price $10,565,500 incl. GST ($9,605,000 excl.)."),
    ("High", "TO DO", "a Register p.5 (SW-42 09.1961, SW-14 11.1961, SW-11 04.1962)",
     "ABIC H4: the architect decides a claim within 20 working days, so SW-14 is late. J5: the price adjustment goes "
     "into the next progress certificate, so SW-11 in April 1962 is late.",
     "Option A (better for rubric C1): SW-14 on 29.09.1961, and SW-11 with the next progress certificate (claim mid-Oct 1961, certificate within 10 business days, about 30.10.1961). "
     "Change the Register, Timeline and forms together. Option B: keep the dates and explain the delay in the ARBV "
     "letter."),
    ("Med", "TO DO", "a Register p.6-7 (Utzon resigns 28.02.1966; SW-31 31.05.1975)",
     "SW-31 in 1975 is signed by the replacement architects, but no row shows the contractor being told that the "
     "architect changed.",
     "Add a Register row: 04.1966, 'Notice of replacement architect (Hall, Todd & Littlemore)', Owner to Contractor. "
     "Sign SW-31 as Hall, Todd & Littlemore."),
    ("Med", "TO DO", "a Register p.7 ('Practical Completion Certificate 20.10.1973')",
     "Reads as if it certifies our Stage I contract, but it is the whole building (Stage III, Hornibrook).",
     "Change the Details to 'Whole building (Stage III, Hornibrook); official opening by the Queen'."),
    ("Med", "TO DO", "SW-31 against Lead 2's liquidated-damages item",
     "If Stage I stays at 03.1963, it finished after 26.02.1963.",
     "Either Lead 2 moves completion to 02.1963, or SW-31 deducts liquidated damages at $1,000 per day (ABIC M9/M10). "
     "Agree which one with Lead 2."),
    ("Low", "TO DO", "a Register p.5 and p.7 (SW rows)",
     "Contributions on SW-42, SW-13 and the 1973 certificate are grey '(suggested)' names.",
     "Confirm or correct them in programme/register_v3.py."),
]

GROUP = [
    ("High", "TO DO", "1 Letter to the ARBV, p.3 (red INSERT page)",
     "Missing. Part B, about 1,000 words, rubric C3.",
     "Write it to the ARBV around reg 5.2(a)(b)(c), citing the documents by appendix and page. Explain the declared "
     "assumptions: SW-31 in 1975, $9.6m for Stage I, Utzon not registered in NSW. Save it as inputs\\ARBV letter.pdf."),
    ("High", "TO DO", "Whole file",
     "Final consistency read-through (rubric C4/C5).",
     "One person reads it all with p.2 'Conventions and assumptions' open: dates, parties, money (GST basis) and form "
     "numbers must match everywhere."),
    ("High", "TO DO", "File name / who submits",
     "'Assessment Task 3_Last name, First name' is written for one student.",
     "Ask the tutor. The draft is named with all three surnames, as in the example submission."),
    ("Med", "TO DO", "Gen AI declaration",
     "Parts of this file were prepared with AI help.",
     "Check the subject's USE OF GEN AI page (Canvas > Course Guide) and add any required statement."),
    ("Med", "TO DO", "Final build",
     "The red INSERT pages must be gone.",
     "Run py build_submission.py. The file name must lose ' - DRAFT (slots to fill)'. Open it and check the "
     "bookmarks. Submit by Fri 6 Nov, 23:59."),
]

LEADS = [
    ("Lead 1 - Design + Client framework", "Kankawee Maksomboon", "Prani Patton",
     "GL1 introductory letter, CAA 2024, client correspondence, Register client rows", LEAD1),
    ("Lead 2 - Procurement + Contract", "Yu-Chun Ho", "Kankawee Maksomboon",
     "ABIC SW 2018 contract (Stage I, Civil & Civic), tender rows, Stage I completion", LEAD2),
    ("Lead 3 - Contract administration", "Prani Patton", "Yu-Chun Ho",
     "SW-12, SW-14, SW-11, SW-31 (+ optional SW-42, SW-13), their Register rows and timing", LEAD3),
    ("Whole group", "All three", "-", "ARBV letter, final read-through, submission", GROUP),
]

CSS = """
* { font-family: sans-serif; }
body { font-size: 8.5pt; color: #222; }
h1 { font-size: 16pt; margin: 0 0 2pt 0; } h2 { font-size: 13pt; color: #1a6b35; margin: 0 0 2pt 0; }
p { margin: 2pt 0 4pt 0; } .sub { color: #555; font-size: 9pt; }
table { border-collapse: collapse; width: 100%; margin-top: 4pt; }
th { color: #1a6b35; text-align: left; padding: 3pt; font-size: 8.5pt; border-bottom: 1.2pt solid #1a6b35; }
td { border-bottom: 0.5pt solid #bbb; padding: 3pt; vertical-align: top; }
.done { color: #1a6b35; font-weight: bold; } .note { color: #8a6d00; font-weight: bold; } .todo { color: #c00; font-weight: bold; }
.box { font-family: monospace; font-size: 10pt; }
.w { width: 135pt; } .p { width: 205pt; } .f { width: 240pt; }
tr { page-break-inside: avoid; }
"""


def table(items):
    rows = []
    for i, (pri, status, where, problem, fix) in enumerate(items, 1):
        cls = {"DONE": "done", "NOTE": "note"}.get(status, "todo")
        rows.append(f"<tr><td class='box'>[&nbsp;]</td><td>{i}</td><td>{pri}</td><td class='{cls}'>{status.replace(' ', '&nbsp;')}</td>"
                    f"<td class='w'>{where}</td><td class='p'>{problem}</td><td class='f'>{fix}</td></tr>")
    return ("<table><tr><th>Check</th><th>#</th><th>Priority</th><th>Status</th><th>Where</th>"
            "<th>Problem</th><th>Fix suggestion</th></tr>" + "".join(rows) + "</table>")


def cover():
    rows = "".join(
        f"<tr><td><b>{t}</b></td><td>{owner}</td><td>{chk}</td><td>{scope}</td>"
        f"<td class='todo'>{sum(1 for x in items if x[1] == 'TO DO')}</td>"
        f"<td class='done'>{sum(1 for x in items if x[1] == 'DONE')}</td>"
        f"<td>{sum(1 for x in items if x[0] == 'High' and x[1] == 'TO DO')}</td></tr>"
        for t, owner, chk, scope, items in LEADS)
    return f"""<h1>Assessment 3: fix checklist by lead</h1>
<p class="sub">Sydney Opera House, Scenario 1 (additional piers). Built 04.11.2026 from the submission audit. Due Fri 6 Nov 2026, 23:59.</p>
<p><b>How to read it.</b> Each lead has a section of their own. <span class="done">DONE</span> = already fixed in the compiled PDF; the lead
only checks it and ticks the box. <span class="note">NOTE</span> = minor, accepted as is. <span class="todo">TO DO</span> = the lead still has to act. <b>p.</b> = page of the compiled file
<i>Assessment Task 3_Maksomboon_Kankawee_Patton_Prani_Ho_Yu-Chun - DRAFT (slots to fill).pdf</i>. The checker reviews the lead's section after the fixes.</p>
<table><tr><th>Part</th><th>Owner</th><th>Checker</th><th>Covers</th><th>To do</th><th>Done</th><th>High to do</th></tr>{rows}</table>
<p style="margin-top:8pt"><b>Compiled file map:</b> p.1 Contents &middot; p.2 Conventions and assumptions &middot; p.3 ARBV letter (slot) &middot;
p.4-7 Register &middot; p.8 Timeline by party &middot; p.9-13 Introductory letter &middot; p.14-31 CAA 2024 &middot; p.32-94 ABIC SW 2018 &middot;
p.95-98 SW-12, SW-14, SW-11, SW-31 (slots).</p>
<p><b>Decisions already made</b> (Kankawee, 04.11.2026): SW-31 stays 31.05.1975 (declared on p.2); SW-11 stays +$5,000 excl. GST, with ABIC
Item 18 set to $275 incl. GST to match; the ARBV letter and SW forms are written by the group. Lead 1 part reviewed and approved; Timeline shown by party.</p>
<p><b>Files and tools:</b> Ready to submit\\README.txt &middot; full audit {TOOLS}\\23-submission-audit.md &middot;
rebuild with <i>py build_submission.py</i> in {TOOLS}\\submission.</p>"""


def section(t, owner, chk, scope, items):
    return (f"<h2>{t}</h2><p class='sub'>Owner: <b>{owner}</b> &middot; Checker: <b>{chk}</b> &middot; {scope}</p>"
            + table(items))


def main():
    html = cover() + "".join(
        f"<div style='page-break-before: always'>{section(*lead)}</div>" for lead in LEADS)
    story = pymupdf.Story(html=html, user_css=CSS)
    mediabox = pymupdf.paper_rect("a4-l")
    where = mediabox + (36, 36, -36, -40)
    writer = pymupdf.DocumentWriter(OUT)
    more = 1
    while more:
        dev = writer.begin_page(mediabox)
        more, _ = story.place(where)
        story.draw(dev)
        writer.end_page()
    writer.close()
    doc = pymupdf.open(OUT)
    for i, page in enumerate(doc, 1):
        page.insert_text((36, mediabox.height - 20), f"Assessment 3 fix checklist  \u00b7  page {i} of {doc.page_count}",
                         fontsize=7, color=(0.4, 0.4, 0.4))
    doc.saveIncr()
    print(f"wrote {OUT} ({doc.page_count} pages)")


if __name__ == "__main__":
    main()
