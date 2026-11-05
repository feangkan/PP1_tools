"""Part B: letter to the ARBV (practice review statement), draft v1 for the group to review and own.

Writes  ARBV letter - draft v1.docx  (editable)  and  ...\\Ready to submit\\Ver.2 - revised\\inputs\\ARBV letter.pdf
Every fact points to a document in the appendices (Register, Timeline, letter, CAA, ABIC, SW forms);
Code clauses checked on the ARBV site 05.11.2026 (2026 Code, Schedule 1; cl 10 = 2015 Code cl 5).

Run:  py build_arbv_letter.py
"""
import os
import re
import subprocess

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
DOCX = os.path.join(HERE, "ARBV letter - draft v1.docx")
PDF = r"D:\RMIT_SEM2 26_PROPRAC 1\Week 12\Ready to submit\Ver.2 - revised\inputs\ARBV letter.pdf"
PS1 = os.path.join(os.path.dirname(HERE), "submission", "office_to_pdf.ps1")

HEAD = [
    "6 November 2026",
    "",
    "The Registrar",
    "Architects Registration Board of Victoria",
    "Level 10, 533 Little Lonsdale Street",
    "Melbourne VIC 3000",
]
RE = ("Practice review statement: Stage I podium contract, National Opera House (now the Sydney Opera House), "
      "ABIC Simple Works contract of 19 February 1959")

# (heading or None, paragraph). ^n = note marker.
BODY = [
    (None, "Dear Registrar,"),
    (None, "This statement responds to the Board's review of how we, as the architect, administered the Stage I "
           "contract for the National Opera House at Bennelong Point. It does not retell the history of the "
           "building or defend every outcome. It explains the decisions we made each time the contract changed, the "
           "obligations behind each decision, and where our practice fell short. The evidence is in the appendices: "
           "the Architect's Register and Timeline (a), the introductory letter (b), the Client Architect Agreement "
           "(c), the ABIC Simple Works contract (d) and the variation forms (e). We refer to the Victorian Architects "
           "Code of Professional Conduct,^1 in particular the duty to administer a building contract fairly, "
           "impartially, diligently and promptly, and to keep both parties informed.^2"),
    ("1. Setting the terms before work began",
     "Our introductory letter of 11 February 1957 set out the services, a fee of 6% and two ways to program the "
     "project: build the podium while the roof was still being designed, or complete the design first. It warned in "
     "writing that an early start risked the roof loads changing the podium (b). The Client Architect Agreement was "
     "signed on 21 February 1957, eight business days later, so the client had the terms before signing.^3 Its "
     "Schedule C recorded the early-start warning and said in advance how a redesign would be handled: as "
     "additional services under clause D.8, priced and agreed in writing before the work (c). Fixing the mechanism "
     "for change at the outset is what later allowed the change to be managed without dispute."),
    (None, "One gap in our engagement must be declared. The Code requires the client agreement to state the "
           "architect's registration number.^4 None is recorded for the architect in 1957, and the agreement shows "
           "'N/A'. Today an unregistered person could not offer these services, and the client should have been "
           "told so plainly."),
    ("2. When the risk materialised",
     "The client chose the early start, and Stage I began on 2 March 1959. In June 1961 Ove Arup & Partners advised "
     "that the final roof loads would exceed what the podium columns had been designed to carry. We acted on two "
     "fronts. To the client, we gave written notice in July 1961 that redesigning the podium was additional work, "
     "and how it would affect our fee, before carrying it out (a).^5 To the contractor, we issued SW-12 on "
     "1 August 1961, instructing additional piers, giving the reason and asking for the effect on price and time "
     "within 20 working days, with a copy to the owner (e). The client learned of the problem, its cause and its "
     "cost within weeks, as the Code expects.^6"),
    ("3. Assessing the claim fairly",
     "Civil & Civic claimed one month and $5,000 on 12 September 1961. We assessed the claim in SW-14 on "
     "2 October 1961, fourteen working days later and inside the twenty allowed by clause H4. The delay came from "
     "our own instruction and from late information from the owner's engineer, both causes that entitle the "
     "contractor to time and costs under clause L1.1. Refusing or discounting the claim would have pushed the "
     "client's design risk onto the builder. We extended the date for practical completion from 26 January to "
     "26 February 1963, and valued the time costs at the rate in Schedule 1 Item 18: 20 working days at $275, or "
     "$5,500 including GST. Using a rate both parties had agreed at tender, not a figure negotiated afterwards, kept "
     "the assessment impartial."),
    ("4. Where we were not prompt",
     "The matching price adjustment, SW-11, was not issued until 2 April 1962. Under clause J5 it belonged in the "
     "next progress certificate, around the end of October 1961, so the contractor waited six months for money we "
     "had already accepted was owed. The Board's guidance asks architects to issue certificates strictly within the "
     "contract's timeframes.^7 We did not, and we accept that this falls short of the duty to act diligently and "
     "promptly. The cause was the workload of the roof redesign; that explains the delay but does not excuse it. A "
     "diary of contract time limits for every claim would have prevented it. SW-11 raised the contract price to "
     "$9,605,000 excluding GST ($10,565,500 including GST), and it states its basis and its links to SW-12, SW-42 "
     "and SW-14, so the figure can be traced (e)."),
    ("5. Impartiality in both directions",
     "Stage I reached practical completion on 18 March 1963, twenty days after the adjusted date. The extension we "
     "granted protected the contractor for the delay our instruction caused; it did not cover delay of the "
     "contractor's own making. Liquidated damages of $1,000 a day (Item 24) therefore applied: $20,000. Applying "
     "the contract for the contractor in 1961 and for the owner in 1963 is one principle, applied consistently."),
    ("6. Continuity after the change of architect",
     "The architect withdrew on 28 February 1966. An administrator who leaves without a handover leaves the client "
     "and the contractor exposed. The client told Civil & Civic on 20 April 1966 that Hall, Todd & Littlemore now "
     "administered the contract, and the Register gave them a complete record of every instruction, claim and "
     "certificate (a).^8 That record allowed the final certificate, SW-31, to be issued on 31 May 1975. It refers to "
     "SW-11, certifies $10,565,500 including GST, deducts the $20,000 of damages and finds that sum due to the owner "
     "(e). Holding a 1963 final account open until 1975 was far too long: the certificate should have followed the "
     "defects period, in 1964."),
    ("7. Mechanisms that protected integrity",
     "Three mechanisms held the contract together. The first was standard instruments with clear rules for change: "
     "the CAA for our services and the ABIC contract for the works. The second was one written record: every "
     "document is in the Register with its date, sender, recipient and form number.^9 The third was consistent "
     "figures: the $9,600,000 contract sum, the $5,000 adjustment and the dates agree across the letter, agreement, "
     "contract, forms and Timeline."),
    ("8. Conclusion",
     "We believe the variation was handled fairly. The client was warned before the risk arose and told promptly "
     "when it did, and the contractor's claim was assessed on agreed rates within time. Our two failures, the late "
     "SW-11 and the delayed final certificate, were failures of promptness rather than fairness, and we have set "
     "out how we would prevent them. We will gladly provide anything further the Board requires."),
]
SIGN = ["Yours faithfully,", "", "Kankawee Maksomboon · Yu-Chun Ho · Prani Patton",
        "For the architect administering the Stage I contract", "Signature omitted — academic simulation"]
NOTES = [
    "Victorian Architects Code of Professional Conduct, Architects Regulations 2026 (Vic) sch 1, in effect from "
    "25 April 2026 and replacing the Code in the Architects Regulations 2015 (Vic) sch 1. Architects Registration "
    "Board of Victoria, \u201cVictorian Architects Code of Professional Conduct,\u201d "
    "https://www.arbv.vic.gov.au/victorian-architects-code-professional-conduct.",
    "Code cl 10(2)(a)\u2013(c) (cl 5(2) of the 2015 Code): fairness and impartiality; diligence and promptness; "
    "relevant information to the client and the building practitioner in a timely manner.",
    "Code cl 6(1)\u2013(2): a written, signed agreement before services are provided, and the proposed agreement "
    "given at least seven business days before the client is asked to sign.",
    "Code cl 6(4)(c).",
    "Code cl 6(4)(g)(i) and (l); CAA 2024 clause D.8 and Schedule C (Appendix c).",
    "Code cl 9(a)\u2013(c).",
    "Architects Registration Board of Victoria, \u201cClause 10 \u2014 Administer building contracts impartially "
    "and diligently,\u201d Guide to the Victorian Architects Code of Professional Conduct, guidance (updated "
    "8 September 2026).",
    "Code cl 9(f) and cl 10(2)(c).",
    "Code cl 15 (documents and records).",
]


def add_marked(par, text, size):
    for part in re.split(r"(\^\d+)", text):
        if not part:
            continue
        run = par.add_run(part[1:] if part.startswith("^") else part)
        run.font.size = Pt(size)
        if part.startswith("^"):
            run.font.superscript = True


def words():
    text = " ".join(p for _, p in BODY)
    text = re.sub(r"\^\d+", "", text)
    return len(text.split())


def build():
    d = Document()
    sec = d.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.3)
    sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)
    st = d.styles["Normal"]
    st.font.name, st.font.size = "Arial", Pt(10)
    st.paragraph_format.space_after = Pt(5)
    st.paragraph_format.line_spacing = 1.12
    t = d.add_paragraph()
    r = t.add_run("Letter to the ARBV (Part B)")
    r.bold, r.font.size = True, Pt(13)
    for line in HEAD:
        p = d.add_paragraph(line)
        p.paragraph_format.space_after = Pt(0)
    p = d.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    r = p.add_run("Re: " + RE)
    r.bold = True
    for head, text in BODY:
        if head:
            h = d.add_paragraph()
            h.paragraph_format.space_before = Pt(6)
            h.paragraph_format.space_after = Pt(2)
            hr = h.add_run(head)
            hr.bold = True
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if head or text.startswith("This") or text.startswith("One") \
            else WD_ALIGN_PARAGRAPH.LEFT
        add_marked(p, text, 10)
    for line in SIGN:
        p = d.add_paragraph(line)
        p.paragraph_format.space_after = Pt(0)
    d.paragraphs[-1].runs[0].italic = True
    d.paragraphs[-1].runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    n = d.add_paragraph()
    n.paragraph_format.space_before = Pt(12)
    nr = n.add_run("Notes")
    nr.bold, nr.font.size = True, Pt(9)
    for i, note in enumerate(NOTES, start=1):
        p = d.add_paragraph()
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(f"{i}  ")
        r.font.size = Pt(8)
        r.font.superscript = True
        r2 = p.add_run(note)
        r2.font.size = Pt(8)
    d.core_properties.title = "Letter to the ARBV (Part B)"
    d.save(DOCX)
    print("wrote", os.path.basename(DOCX), "-", words(), "words in the body")
    os.makedirs(os.path.dirname(PDF), exist_ok=True)
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", PS1, "-Docx", DOCX,
                    "-Out", PDF], check=True)
    print("wrote", PDF)


if __name__ == "__main__":
    build()
