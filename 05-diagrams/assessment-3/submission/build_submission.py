"""Assessment 3: build the ready-to-submit files from the group's Week 12 files (audit: ../23-submission-audit.md).

Run:  py build_submission.py
Reads   D:\\RMIT_SEM2 26_PROPRAC 1\\Week 12\\  (the group's CAA + ABIC; never modified)
        ../letters, ../document-register-v3.docx, ../programme/Timeline of significant project events.xlsx
Writes  D:\\RMIT_SEM2 26_PROPRAC 1\\Week 12\\Ready to submit\\

Group pieces still to come go in  Ready to submit\\inputs\\  with these exact names, then re-run:
    ARBV letter.pdf   SW-12.pdf   SW-14.pdf   SW-11.pdf   SW-31.pdf   (optional: SW-42.pdf, SW-13.pdf)
Until they are there, the compiled PDF carries a red slot page for each, and its name ends in "DRAFT".
"""
import os, shutil, subprocess, sys
import pymupdf
from docx import Document

HERE = os.path.dirname(os.path.abspath(__file__))
A3 = os.path.dirname(HERE)
WEEK12 = r"D:\RMIT_SEM2 26_PROPRAC 1\Week 12"
SRC_CAA = os.path.join(WEEK12, "PP MARKUP_Complete a Client Architect Agreement 2024 with the client) caa2024_fullservices_digital.pdf")
SRC_ABIC = os.path.join(WEEK12, "construction contract ABIC Simple Works Contract 2018.pdf")
SRC_LETTER = os.path.join(A3, "letters", "GL1 Introductory letter - draft v1.docx")
SRC_REGISTER = os.path.join(A3, "document-register-v3.docx")
SRC_TIMELINE = os.path.join(A3, "programme", "Timeline of significant project events.xlsx")
OUT = os.path.join(WEEK12, "Ready to submit")
PARTS = os.path.join(OUT, "parts")
INPUTS = os.path.join(OUT, "inputs")
PS1 = os.path.join(HERE, "office_to_pdf.ps1")

GROUP = [("Kankawee", "Maksomboon"), ("Prani", "Patton"), ("Yu-Chun", "Ho")]
ARIAL = r"C:\Windows\Fonts\arial.ttf"
SIG = "Signature omitted \u2014 academic simulation"


def office(*args):
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", PS1, *args], check=True)


# ------------------------------------------------------------------ 1. CAA
CAA_TEXT = {
    # B2/B3: same N/A convention as the ABIC
    "Client ABN": "N/A (1957)",
    "Architect ABN": "N/A (1957)",
    "Architect reg no": "N/A [A]",
    "Individual architect signature date": "21/02/1957",
    "the project": ("National Opera House (now the Sydney Opera House): a large hall (about 3,000 seats) and a small hall "
                    "(about 1,200 seats) for opera, concerts, ballet, drama and public meetings, with rehearsal, restaurant "
                    "and back-of-house areas, on a raised podium under a roof of shell vaults. Built in stages: I podium, "
                    "II roof, III interiors."),
    "blank 51": "To be appointed",                       # Item 4 land surveyor (group comment p.15)
    # Schedule C: answers to the group comments, written into the agreement
    "Clause no. 19": "A.3",
    "Details line 19": "No Planning/Development Application is prepared. The Minister for Public Works is the constructing",
    "Details line 20": "authority, and the Client obtains its own statutory approvals. The Architect supplies drawings for them (A.4).",
    "Clause no. 21": "B.2, B.6",
    "Details line 21": "Record documents (B.2 survey coordination; as-built record documents) and disputes under the building",
    "Details line 22": "contract (B6.5-B6.9) are Additional Services at the Item 2 rates. Planning tribunal work is excluded.",
    "Clause no. 23": "B.4",
    "Details line 23": "Illustration (2D marketing drawings and 3D illustrations) is an Additional Service at the Item 2 rates.",
}
CAA_RADIO = {"Group 100": "Choice3", "Group 103": "Choice3"}   # B.2 lines 2 and 5: Additional
CAA_CHECK = {"Check Box 8": True}                              # B.2 lump sum: time-based rates apply
CAA_SIGS = ["corp client signature", "corp client signature 2", "Individual architect signature"]

ANSWERS = {  # page (1-based) -> answers, in the order of the group's notes on that page
    10: ["No DA is prepared: the Minister for Public Works is the constructing authority and the Crown approves its own "
         "works (Sydney Opera House Act 1960). Now stated in Schedule C (A.3).",
         "Same answer as above: see Schedule C (A.3)."],
    11: ["The Client obtains its own approvals as the Government; we still supply the drawings under A.4 (Included). "
         "Schedule C (A.3) now says who does it.",
         "We do select the contractor: A.5 (1) Tender is Included. Only (2) Negotiated offer is Additional, for later "
         "stages (Hornibrook, Stage II/III)."],
    13: ["Agreed: B.2 lines 2 and 5 now ticked Additional (no % fee for B.2, so time-based at Item 2 rates; see Schedule C).",
         "None needed: no planning negotiation on a Crown project. See Schedule C (A.3).",
         "No. B.5 is trade-package documentation for a construction manager. Our construction set is A.4, which is Included.",
         "Two different things: planning-tribunal lines are excluded; building-contract dispute lines B6.5-B6.9 are "
         "Additional, so we do act in contract disputes. Stated in Schedule C."],
    14: ["Not excluded: A.5 (1) Tender is Included, so 0.300% is right.",
         "Correct: B.5 is excluded, so its fee stays blank.",
         "Priced already: the time-based box is ticked, so Item 2 hourly rates apply. Added to Schedule C (B.4)."],
    16: ["Agreed: land surveyor kept, client to engage, note 'To be appointed' added."],
}


def set_caa_fields(doc):
    for page in doc:
        for w in page.widgets():
            n = w.field_name
            if n in CAA_TEXT and "/RV" in doc.xref_object(w.xref):
                # rich-text field: its /RV value overrides the new text, so make it a plain field first
                doc.xref_set_key(w.xref, "RV", "null")
                ff = int(doc.xref_get_key(w.xref, "Ff")[1] or 0)
                doc.xref_set_key(w.xref, "Ff", str(ff & ~(1 << 25)))
            if n in CAA_TEXT:
                w.field_value = CAA_TEXT[n]; w.update()
            elif n in CAA_RADIO or n in CAA_CHECK:
                # set the state only, so the form's own tick appearance is kept (w.update() redraws it)
                on = CAA_RADIO[n] if n in CAA_RADIO else w.on_state()
                doc.xref_set_key(w.xref, "AS", "/" + on if w.on_state() == on else "/Off")
                kind, parent = doc.xref_get_key(w.xref, "Parent")
                doc.xref_set_key(int(parent.split()[0]) if kind == "xref" else w.xref, "V", "/" + on)


def build_caa():
    doc = pymupdf.open(SRC_CAA)
    set_caa_fields(doc)
    # review copy: the group's notes stay, an answer note sits beside each
    rev = pymupdf.open(); rev.insert_pdf(doc)
    for pno, answers in ANSWERS.items():
        page = rev[pno - 1]
        notes = sorted([a for a in page.annots() if a.type[1] == "Text"], key=lambda a: a.rect.y0)
        for a, text in zip(notes, answers):
            ans = page.add_text_annot(pymupdf.Point(a.rect.x1 + 4, a.rect.y0), text, icon="Comment")
            ans.set_info(title="Answer (audit 04.11.2026)", content=text)
            ans.set_colors(stroke=(0.1, 0.6, 0.2)); ans.update()
    rev.save(os.path.join(OUT, "Group review - CAA 2024 with answers to comments.pdf"), garbage=3, deflate=True)
    # submission copy: no notes, signature convention as the ABIC, flattened
    for page in doc:
        for a in list(page.annots()):
            if a.type[1] in ("Text", "Popup", "Highlight"):
                page.delete_annot(a)
    for page in doc:
        for w in page.widgets():
            if w.field_name in CAA_SIGS:
                page.insert_textbox(w.rect + (2, 6, 0, 4), SIG, fontsize=7, fontname="arial", fontfile=ARIAL,
                                    color=(0.2, 0.2, 0.2))
    doc.bake()
    path = os.path.join(PARTS, "c CAA 2024.pdf"); doc.save(path, garbage=3, deflate=True)
    return path


# ------------------------------------------------------------------ 2. ABIC
ABIC_FIX = [  # (page 1-based, old span text, clip rect, new text, font size)
    (1, "Civil&Civic Pty Ltd", (230, 618, 300, 633), "Civil & Civic Pty Ltd", 8),
    (7, "10% / 10,560,000", (420, 692, 495, 707), "$1,056,000 (10%)", 9),        # Item 13
    (8, "10% / 10,560,000", (368, 100, 442, 115), "$1,056,000 (10%)", 9),        # Item 14
    (8, "1,000", (330, 406, 358, 420), "275 ($250 + GST)", 9),                   # Item 18
]


def build_abic():
    doc = pymupdf.open(SRC_ABIC)
    for pno, old, clip, new, size in ABIC_FIX:
        page = doc[pno - 1]
        hits = page.search_for(old, clip=pymupdf.Rect(clip))
        assert len(hits) == 1, (pno, old, hits)
        r = hits[0]
        page.add_redact_annot(r, fill=False)
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
        page.insert_font(fontname="arial", fontfile=ARIAL)
        page.insert_text((r.x0, r.y1 - 2.2), new, fontname="arial", fontsize=size, color=(0.137, 0.122, 0.125))
    path = os.path.join(PARTS, "d ABIC SW 2018.pdf"); doc.save(path, garbage=3, deflate=True)
    return path


# ------------------------------------------------------------------ 3. Letter, Register, Timeline
def build_letter():
    d = Document(SRC_LETTER)
    runs = [r for p in d.paragraphs for r in p.runs]
    runs += [r for t in d.tables for row in t.rows for c in row.cells for p in c.paragraphs for r in p.runs]
    n = 0
    for r in runs:
        if r.font.highlight_color is not None:
            r.font.highlight_color = None; n += 1
    docx = os.path.join(OUT, "b Introductory letter (GL1) 11.02.1957.docx"); d.save(docx)
    pdf = os.path.join(PARTS, "b Introductory letter.pdf"); office("-Docx", docx, "-Out", pdf)
    print(f"letter: {n} highlights removed")
    return pdf


def build_register():
    pdf = os.path.join(PARTS, "a1 Architects Register.pdf"); office("-Docx", SRC_REGISTER, "-Out", pdf)
    shutil.copy(SRC_REGISTER, os.path.join(OUT, "a Architects Register v3.docx"))
    return pdf


def build_timeline():
    pdf = os.path.join(PARTS, "a2 Timeline.pdf")
    office("-Xlsx", SRC_TIMELINE, "-Sheet", "Timeline by party", "-Out", pdf)
    return pdf


# ------------------------------------------------------------------ 4. Contents + notes, slots
CSS = """
* { font-family: sans-serif; color: #222; }
h1 { font-size: 17px; margin: 0 0 2px 0; } h2 { font-size: 12px; margin: 14px 0 4px 0; color: #1a6b35; }
p, td, li { font-size: 9.5px; line-height: 1.35; } .sub { font-size: 10.5px; color: #555; margin: 0 0 10px 0; }
table { border-collapse: collapse; width: 100%; } td { border-bottom: 0.5px solid #bbb; padding: 3px 4px; vertical-align: top; }
td.n { width: 30px; text-align: right; color: #555; } td.k { width: 120px; font-weight: bold; }
.ind { padding-left: 18px; }
"""


def contents_html(pages):
    names = ", ".join(f"{f} {l}" for f, l in GROUP)
    rows = [("1", "Letter to the ARBV (Part B)", pages["arbv"]),
            ("2", "Appendices", None),
            ("a", "Architect's Register, with the Timeline of significant project events", pages["a"]),
            ("b", "Introductory letter to the client (GL1), 11.02.1957", pages["b"]),
            ("c", "Client Architect Agreement 2024, 21.02.1957", pages["c"]),
            ("d", "ABIC Simple Works Contract 2018, Stage I, 19.02.1959", pages["d"]),
            ("e", "ABIC SW 2018 template forms", pages["e"])]
    for code, label in [("SW-12", "Architect's instruction for a variation"), ("SW-14", "Adjustment of time"),
                        ("SW-11", "Contract price adjustment"), ("SW-31", "Final certificate (refers to SW-11)")]:
        rows.append(("", f"{code} {label}", pages[code]))
    tr = []
    for code, label, pg in rows:
        cls = ' class="ind"' if code in "abcde" and code else ""
        cls = ' class="ind"' if code == "" else cls
        tr.append(f"<tr><td class='n'>{code}</td><td{cls}>{label}</td><td class='n'>{'' if pg is None else pg}</td></tr>")
    return f"""<h1>Professional Practice 1 &middot; Assessment Task 3: Portfolio of Practice File Notes</h1>
<p class="sub">Sydney Opera House, run through contemporary instruments &middot; Scenario 1: additional piers to the Stage I podium<br>
Group: {names}</p>
<h2>Contents</h2><table>{''.join(tr)}</table>
<h2>Reading this file</h2>
<p>Every event is traced through the same dates, parties and figures in the Register, the Timeline, the letter, the
CAA, the ABIC contract and the forms. The historical project did not use these contracts, so facts and our assumptions
are kept apart: facts carry a source in the Register and Timeline, and every assumption is listed overleaf.</p>"""


ASSUMPTIONS = [
    ("Instruments", "Today's documents (GL1 letter, CAA 2024, ABIC SW 2018 and its forms) are applied to the historical "
                    "events, as the brief requires. The general conditions bound into Appendix d are the copy supplied "
                    "by the course (SW 2018 H Vic edition)."),
    ("Money", "Australian dollars throughout. Figures are stated excl. GST with GST shown alongside, although GST did not "
              "exist in 1957-75. Cost of Works forecast $9,600,000 (the tutor's original-budget figure), used also as "
              "the Stage I contract price, $9,600,000 + GST = $10,560,000."),
    ("Variation chain", "SW-12 (08.1961) strengthen podium columns and add piers; SW-14 (11.1961) +1 month (20 working "
                        "days), practical completion 26.01.1963 to 26.02.1963; SW-11 (04.1962) +$5,000 excl. GST = "
                        "20 working days x $275 incl. GST (ABIC Item 18); SW-31 (31.05.1975) refers to SW-11: "
                        "$9,605,000 excl. GST ($10,565,500 incl.)."),
    ("Final certificate", "The Stage I final account is held over and certified at overall completion, 31.05.1975, by "
                          "the replacement architects (Hall, Todd & Littlemore), who took over contract administration "
                          "after 28.02.1966 [A]."),
    ("Parties", "Client: the Government of New South Wales; representative under CAA C.2, the Premier or a Minister he "
                "nominates (Cahill, then Heffron, Askin/Hughes, Punch: each change a C.3 notice). Contractor for Stage I: "
                "Civil & Civic Pty Ltd. Named individuals in the ABIC who are not in the historical record (owner's "
                "and contractor's representatives, witness, guarantor bank and attorney) are invented [A]."),
    ("Identifiers", "ABNs and registration numbers are 'N/A': they did not exist, or are not known, for 1957-59. "
                    "Utzon was not registered in NSW (a point taken up in the ARBV letter)."),
    ("Signatures", "No signature is reproduced. Signature boxes read 'Signature omitted - academic simulation'; "
                   "signing dates are those of the Register."),
    ("Dates", "Dates in italics in the Register are months we placed inside a year the sources give [A]. "
              "Sources for every fact are keyed in the Register and in the Timeline workbook's Sources sheet."),
]


def notes_html():
    tr = "".join(f"<tr><td class='k'>{k}</td><td>{v}</td></tr>" for k, v in ASSUMPTIONS)
    return f"<h1>Conventions and assumptions</h1><p class='sub'>Applied in the same way in every document of this file. [A] = our assumption.</p><table>{tr}</table>"


def html_page(doc, html):
    page = doc.new_page(width=595, height=842)
    page.insert_htmlbox(pymupdf.Rect(56, 56, 539, 800), html, css=CSS)


def slot(title, what):
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    page.draw_rect(pymupdf.Rect(40, 40, 555, 802), color=(0.8, 0, 0), width=2)
    page.insert_htmlbox(pymupdf.Rect(70, 300, 525, 560),
                        f"<p style='font-size:22px;color:#c00;font-weight:bold;text-align:center'>INSERT: {title}</p>"
                        f"<p style='font-size:11px;text-align:center'>{what}</p>"
                        f"<p style='font-size:9px;text-align:center;color:#555'>Save it as a PDF in Ready to submit\\inputs\\ "
                        f"and run build_submission.py again. This page then disappears.</p>")
    return doc


SLOTS = [("arbv", "ARBV letter.pdf", "Letter to the ARBV (Part B)",
          "About 1,000 words, to the ARBV: professional judgement and obligations under the Architects Regulations 2015 "
          "reg 5.2(a)(b)(c), evidenced by the documents in the appendices."),
         ("SW-12", "SW-12.pdf", "SW-12 Architect's instruction for a variation", "Values: see Form data sheet."),
         ("SW-42", "SW-42.pdf", None, None),
         ("SW-13", "SW-13.pdf", None, None),
         ("SW-14", "SW-14.pdf", "SW-14 Adjustment of time", "Values: see Form data sheet."),
         ("SW-11", "SW-11.pdf", "SW-11 Contract price adjustment", "Values: see Form data sheet."),
         ("SW-31", "SW-31.pdf", "SW-31 Final certificate", "Must refer to SW-11. Values: see Form data sheet.")]


def compile_all(parts):
    missing = []
    pieces = {}
    for key, fname, title, what in SLOTS:
        p = os.path.join(INPUTS, fname)
        if os.path.exists(p):
            pieces[key] = pymupdf.open(p)
        elif title:
            pieces[key] = slot(title, what); missing.append(fname)
    order = [("arbv", "1 Letter to the ARBV", pieces["arbv"]),
             ("a", "a Architect's Register", pymupdf.open(parts["a1"])),
             ("a2", "a Timeline of significant project events (by party)", pymupdf.open(parts["a2"])),
             ("b", "b Introductory letter", pymupdf.open(parts["b"])),
             ("c", "c Client Architect Agreement 2024", pymupdf.open(parts["c"])),
             ("d", "d ABIC SW 2018 contract", pymupdf.open(parts["d"]))]
    for k in ["SW-12", "SW-42", "SW-13", "SW-14", "SW-11", "SW-31"]:
        if k in pieces:
            order.append((k, f"e {k}", pieces[k]))
    front_pages = 2
    pages, n = {}, front_pages + 1
    for key, _, d in order:
        pages[key] = n; n += d.page_count
    pages["e"] = pages["SW-12"]
    out = pymupdf.open()
    html_page(out, contents_html(pages)); html_page(out, notes_html())
    toc = [[1, "Contents", 1], [1, "Conventions and assumptions", 2]]
    for key, label, d in order:
        if key == "a2":
            toc.append([2, "Timeline of significant project events (by party)", pages[key]])
        else:
            if key == "a":
                toc.append([1, "2 Appendices", pages[key]])
            toc.append([2 if key != "arbv" else 1, label, pages[key]])
        out.insert_pdf(d)
    out.set_toc(toc)
    surnames = "_".join(f"{l}_{f}" for f, l in GROUP)
    name = f"Assessment Task 3_{surnames}" + (" - DRAFT (slots to fill)" if missing else "") + ".pdf"
    for old in os.listdir(OUT):
        if old.startswith("Assessment Task 3_") and old.endswith(".pdf"):
            os.remove(os.path.join(OUT, old))
    out.save(os.path.join(OUT, name), garbage=3, deflate=True)
    print(f"compiled: {name}  ({out.page_count} pages)")
    print("still to drop into inputs\\:", ", ".join(missing) if missing else "nothing")


FORM_COMMON = ("Contract: ABIC SW 2018 dated 19.02.1959 &middot; Owner: The Government of New South Wales &middot; "
               "Contractor: Civil &amp; Civic Pty Ltd &middot; Architect: J&oslash;rn Utzon &middot; Works: Stage I podium and "
               "substructure works, Bennelong Point, Sydney NSW &middot; Contract price $9,600,000 excl. GST "
               "($10,560,000 incl.) &middot; Date for practical completion 26.01.1963")
FORMS = [
    ("SW-12", "01.08.1961 [A] (Register 08.1961)", "J1",
     "Instruction no. 1. Strengthen the podium columns and add piers to carry the final roof loads advised by Ove Arup "
     "&amp; Partners (06.1961). Cause: the roof design was resolved after Stage I started (CAA Schedule C, A.4 and D.8; "
     "ABIC special condition 3). Contractor to give notice of the effect on price and time within 20 working days (J2.3). "
     "Issued on behalf of the owner; copy to the owner."),
    ("SW-42 (optional)", "01.09.1961 [A]", "H1, H2",
     "Contractor claims +20 working days (1 month) and +$5,000 excl. GST for the varied work."),
    ("SW-13 (optional)", "02.10.1961 [A]", "J3", "Instruction to proceed with the varied work."),
    ("SW-14", "01.11.1961 [A] (Register 11.1961)", "H4, L1.1c",
     "Delay caused by an architect's instruction (a delay with costs). +20 working days: date for practical completion "
     "26.01.1963 becomes 26.02.1963. Adjustment of time costs 20 x $275 incl. GST (Schedule 1 Item 18) = $5,500 incl. GST."),
    ("SW-11", "02.04.1962 [A] (Register 04.1962)", "H4, H5",
     "Refers to SW-14. +$5,000 excl. GST + $500 GST = +$5,500. Contract price $10,560,000 incl. GST becomes "
     "$10,565,500 incl. GST ($9,605,000 excl.)."),
    ("SW-31", "31.05.1975 (Register)", "N11",
     "Must refer to SW-11. Final contract price $10,565,500 incl. GST; less amounts already certified (group to state); "
     "provisional sums (Sched. 6, $150,000) and prime cost sums (Sched. 7, $50,000) assumed spent as allowed, so no "
     "adjustment [A]. Issued by the replacement architects, Hall, Todd &amp; Littlemore [A]; copy to the owner."),
]


def build_form_sheet():
    rows = "".join(f"<tr><td class='k'>{f}</td><td>{d}<br><span style='color:#555'>Clause {c}</span></td><td>{t}</td></tr>"
                   for f, d, c, t in FORMS)
    html = (f"<h1>SW form data sheet (for the group, not for submission)</h1>"
            f"<p class='sub'>Fill the ABIC SW 2018 Word template forms with exactly these values, so they match the Register, "
            f"Timeline, CAA and contract. Dates marked [A] are our assumed days inside the Register's months.</p>"
            f"<p>{FORM_COMMON}</p><table>{rows}</table>"
            f"<h2>Check before you submit</h2><p>ABIC H4: the architect decides a claim within 20 working days. SW-42 on "
            f"01.09.1961 makes SW-14 due by about 29.09.1961, but the Register has 11.1961. J5: the price adjustment goes "
            f"into the next progress certificate, but the Register has SW-11 in 04.1962. Either move these dates (Register, "
            f"Timeline and forms together), or explain the delay in the ARBV letter.</p>")
    doc = pymupdf.open(); html_page(doc, html)
    doc.save(os.path.join(OUT, "For the group - SW form data sheet.pdf"))


def main():
    os.makedirs(PARTS, exist_ok=True); os.makedirs(INPUTS, exist_ok=True)
    build_form_sheet()
    parts = {"c": build_caa(), "d": build_abic(), "b": build_letter(), "a1": build_register(), "a2": build_timeline()}
    compile_all(parts)


if __name__ == "__main__":
    main()
