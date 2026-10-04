"""Build the GL1 introductory letter (Assessment 3, file 3) from the AIA template.

Source: letters/source/GL1 template CAA2019 (converted from .doc).docx — the course's
caa2019_gl1_introductoryletter (R1).doc, saved as .docx by Word. The wording is updated to the
CAA 2024 version of GL1 (Week 10 lecture, slide 30), because the brief requires CAA 2024.

Markup in the text below:
  {{...}}  an assumed or unconfirmed value: highlighted yellow in the draft so the group can
           check it (remove the highlight before submission)
  **...**  bold

Every figure here must match the CAA 2024 (file 4), the Document Register and the timeline.
The assumptions and their sources are listed in ../21-introductory-letter-notes.md.

Run:  py build_intro_letter.py   (writes "GL1 Introductory letter - draft v1.docx" next to this file)
"""
import copy
import re
import sys
from pathlib import Path

import docx
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import RGBColor

HERE = Path(__file__).resolve().parent
SRC = HERE / "source" / "GL1 template CAA2019 (converted from .doc).docx"
OUT = HERE / (sys.argv[1] if len(sys.argv) > 1 else "GL1 Introductory letter - draft v1.docx")

# ---- project facts (keep in step with the CAA and the Register) -------------------------------
COST_OF_WORKS = 9_600_000          # tutor's starting figure (10-tutor-video-notes.md)
FEE_PCT = 6.0                      # assumed: group to confirm
SPLIT = [                          # share of the fee per CAA Schedule B Item 1 (Week 10 fee map)
    ("A.1", "Concept design", 15),
    ("A.2", "Design development", 15),
    ("A.3", "Planning/Development Application", 0),
    ("A.4", "Construction documentation", 35),
    ("A.5", "Contractor selection", 5),
    ("A.6", "Contract administration", 30),
]
CONTINGENCY = "10%"

def money(v):
    return f"${v:,.0f}"

FEE = COST_OF_WORKS * FEE_PCT / 100


# ---- helpers ------------------------------------------------------------------------------------
TOKEN = re.compile(r"(\{\{.*?\}\}|\*\*.*?\*\*)")


def put(p, text, style=None, bold_all=False, plain=False):
    """Replace a paragraph's text, keeping its paragraph format; black, upright runs."""
    for r in list(p.runs):
        r._element.getparent().remove(r._element)
    if style:
        p.style = style
    for chunk in TOKEN.split(text):
        if not chunk:
            continue
        hl = bold = False
        if chunk.startswith("{{"):
            chunk, hl = chunk[2:-2], True
        elif chunk.startswith("**"):
            chunk, bold = chunk[2:-2], True
        run = p.add_run(chunk)
        run.font.color.rgb = RGBColor(0, 0, 0)
        run.italic = False
        run.bold = (bold or bold_all) or None
        if plain:
            run.underline = False
        if hl:
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return p


def drop(p):
    p._element.getparent().remove(p._element)


def clone_after(p, text):
    """Insert a copy of paragraph p (same style/numbering) after p, with new text."""
    new = copy.deepcopy(p._element)
    p._element.addnext(new)
    q = docx.text.paragraph.Paragraph(new, p._parent)
    return put(q, text)


def as_bullet(p, model):
    """Give paragraph p the paragraph properties (bullet numbering, indents) of model."""
    old = p._element.pPr
    if old is not None:
        p._element.remove(old)
    p._element.insert(0, copy.deepcopy(model._element.pPr))
    return p


def fill_table(table, rows):
    """Resize a copied table to len(rows) and fill it; first row is the header."""
    trs = table._tbl.tr_lst
    while len(table._tbl.tr_lst) < len(rows):
        table._tbl.append(copy.deepcopy(trs[-1]))
    while len(table._tbl.tr_lst) > len(rows):
        table._tbl.remove(table._tbl.tr_lst[-1])
    for r, values in enumerate(rows):
        for c, value in enumerate(values):
            cell = table.rows[r].cells[c]
            for extra in cell.paragraphs[1:]:
                drop(extra)
            put(cell.paragraphs[0], f"**{value}**" if r == 0 else value, plain=True)


# ---- build -------------------------------------------------------------------------------------
d = docx.Document(SRC)
P = list(d.paragraphs)          # indices as in the template (see notes file for the map)
body_style = P[26].style        # the template's body text style ("Header")

# Guidance text box and the "GL1 ... DELETE BEFORE SENDING" title
for r in list(d.element.body.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r")):
    if r.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pict") is not None:
        r.getparent().remove(r)
drop(P[0])

# Date, addressee, salutation, subject
put(P[3], "{{11 February 1957}}")
put(P[5], "The Honourable J. J. Cahill MLA, Premier of New South Wales")
put(P[6], "for the Government of New South Wales, {{Premier's Department, Sydney NSW}}")
put(P[11], "Dear Mr Cahill,")
put(P[13], "**Re:\tFee proposal to provide Architectural Services**\n"
           "**Project: National Opera House, Bennelong Point, Sydney**")

put(P[15], "It was a great honour to learn that our design was awarded first prize in your Government's "
           "international competition, announced on 29 January 1957, and we thank you for the opportunity "
           "to discuss the next steps for the project.")
put(P[17], "Further to the announcement and our {{subsequent correspondence}}, we include here:")
put(P[18], "a summary of our assessment of the design brief and site assessment;")
put(P[19], "an initial forecast of the Cost of Works for the project, and")
put(P[20], "the method for calculating our fee for our services as your architect,")
put(P[21], "all for your consideration.")
put(P[23], "A draft Client Architect Agreement is attached and provides detailed information on the services "
           "to be provided and contractual conditions of our engagement as your Architect. This agreement is the "
           "Australian Institute of Architects' standard-form Client Architect Agreement 2024 (the CAA). We also "
           "attach the 'Information guide to the client' that helps you understand the CAA, as well as a copy of "
           "the applicable Code of Conduct required under the Architects Act that applies to all architects "
           "(for a site in New South Wales, the code of conduct under the Architects Act 2003 (NSW)).")

# Design brief and site assessment
put(P[28], "Our understanding of the brief is taken from the competition's Conditions and Programme (1955) "
           "and from our winning scheme. The project includes:", "Header")
drop(P[29]); drop(P[30]); drop(P[31]); drop(P[32])
brief = [
    "a large hall seating about 3,000 people, for symphony concerts, opera, ballet, choral concerts and "
    "large public meetings;",
    "a small hall seating about 1,200 people, for drama, smaller-scale opera, chamber music, recitals "
    "and lectures;",
    "{{rehearsal rooms, a restaurant, meeting rooms, and the stage, dressing and back-of-house areas both "
    "halls need}};",
    "a raised platform (the podium) holding the stage machinery, building services and the public approach "
    "and foyers; and",
    "the roof: a series of shell vaults rising over both halls.",
]
for p, text in zip(P[34:39], brief):
    as_bullet(put(p, text), P[18])
drop(P[33])
for p in P[39:43]:
    drop(p)
put(P[44], "**Site:**\tBennelong Point, Sydney Harbour (at present the Fort Macquarie tram depot).", "Header")
put(P[46], "**Site assessment:** the site is prominent and surrounded by water on three sides. We have not yet "
           "seen a survey of the ground conditions. Because the podium and its columns will carry the roof, "
           "the ground must be investigated before the foundations are designed, so we recommend a "
           "geotechnical investigation early in the Concept Design stage (see Specialist Consultants below).",
    "Header")
put(P[48], "Note:\tThe seat numbers and uses outlined above are initial, indicative only and are likely to change "
           "as the design brief and project design evolve. Floor areas will be confirmed at the Concept Design "
           "stage.")

# Cost of Works (2024 wording)
put(P[52], "You will recall our discussion of the Cost of Works and that our fees, among other things, are not "
           "part of calculating the Cost of Works. It is very important that we proceed with a mutual "
           "understanding of what the Cost of Works covers and how it is used during the stages of our services. "
           "We encourage you to read the enclosed 'Information guide to the client' document which also explains "
           "these concepts under the CAA.")
put(P[54], "Clause A.3 and Section M of the CAA (pages 2 and 7) set out the definition of the Cost of Works. If "
           "you are unclear on what parts of your Total Project Cost are included in the Cost of Works and which "
           "parts are not, please ask us or refer to the 'Information guide to the client' document.")
put(P[56], f"On our current understanding of your design brief, and the quality and size of the project, our "
           f"initial Cost of Works forecast is **{money(COST_OF_WORKS)}** (excl. GST).")
put(P[58], "In deriving this initial Cost of Works forecast we have considered the cost of comparable large "
           "public buildings, but indicative costs are not a guarantee of actual costs nor the final cost for "
           "your project. The roof structure in particular has no precedent, and its cost cannot yet be "
           "estimated with confidence.")
put(P[62], "As discussed, we highly recommend you engage a quantity surveyor or professional cost consultant to "
           "assist you in managing your overall budget for the project. A cost consultant can provide "
           "professional and more accurate estimates of the project costs, as the project takes shape.")

# Total Project Cost (2024 wording)
put(P[66], "The Total Project Cost (also defined in Section M) includes the Cost of Works plus all other costs that "
           "relate to the project including (but not limited to) our fees and those of other specialist "
           "consultants and professionals; disbursements; removal and relocation costs; design and construction "
           "contingencies including escalation costs; planning and other authority fees and charges; legal fees; "
           "landscaping; loose or unaffixed furniture, fittings and equipment; borrowing or finance costs; "
           "marketing and promotional costs, etc.")
put(P[68], "As discussed, you are responsible for managing the Total Project Cost budget, because this concept "
           "covers components we are unable to control, manage, or don't have responsibility for. Please also "
           "consider the GST components for costs, because the GST payable on the project costs (including our "
           "fees) should be factored in your budget.")
put(P[70], f"We also recommend that you include in the Total Project Cost budget a contingency sum of say "
           f"{{{{{CONTINGENCY}}}}}, to allow for unforeseen expenses that may eventuate as the project proceeds. "
           f"Given the unresolved roof and the untested ground, we consider this the minimum prudent allowance.")

# Fees
put(P[84], "The scope of these Services is listed in Schedule A: Section A of the draft CAA (page 9). Please note "
           "that specific responsibilities and services not included in our professional services are listed in "
           "clause A.2 (page 2).")
put(P[86], f"We propose a percentage Fee of {{{{{FEE_PCT:g}%}}}} of the Cost of Works (excluding GST as outlined "
           f"above), for which a preliminary estimate is:")
put(P[88], f"{{{{{FEE_PCT:g}%}}}} of {money(COST_OF_WORKS)} (forecast Cost of Works excluding GST) = "
           f"{money(FEE)} (excluding GST)", bold_all=True)
put(P[90], "The breakdown of these fees across the stages of the Core Architectural Services is set out in "
           "Schedule B: Item 1 of the draft CAA (page 13), as follows. No Mobilisation Fee is proposed.")
# fee breakdown table: a copy of the template's table, placed after P[90]
fee_tbl = copy.deepcopy(d.tables[0]._tbl)
P[90]._element.addnext(fee_tbl)
fee_rows = [("Schedule B item", "Service", "Share of fee", "% of Cost of Works / estimate (excl. GST)")]
for code, name, share in SPLIT:
    if share:
        pct = FEE_PCT * share / 100
        fee_rows.append((code, name, f"{share}%", f"{pct:.2f}% = {money(COST_OF_WORKS * pct / 100)}"))
    else:
        fee_rows.append((code, name, "Excluded", "{{Crown project: approvals by the Government}}"))
fee_rows.append(("Total", "Core Architectural Services", "100%", f"{FEE_PCT:.2f}% = {money(FEE)}"))
fill_table(docx.table.Table(fee_tbl, P[90]._parent), fee_rows)

put(P[92], "These Core Services cover the whole path from the competition scheme to a completed building: "
           "developing the scheme with you, documenting it for tender, helping you select the building "
           "contractor, and administering the building contract on your behalf (ABIC Simple Works 2018), "
           "including variations, adjustments of time, progress certificates and the final certificate. We "
           "include contract administration because the building is technically unprecedented, and decisions "
           "on site will need the designer's judgement.")
put(P[95], "As discussed with you, we have identified that the following architectural services are required in "
           "addition to the Core Architectural Services. These services are shown in Schedule A: Section B of "
           "the CAA (page 11) and will attract the fees set out in Schedule B: Item 1 for components B.1 to B.6 "
           "(page 13).")
drop(P[97])
put(P[98], "Individual services in Schedule A which are priced by a different fee method, for the purposes of "
           "Schedule B: Item 1, are set out below:")
fill_table(d.tables[-1], [
    ("Schedule B item:", "Brief description of service:", "Fee method", "Notes"),
    ("B.4", "Illustration: presentation drawings, models and a printed report of the developed scheme, for "
            "your Government and the public", "Time-based rates (Item 2)",
     "{{We will give you an estimate before starting}}"),
])
drop(P[100])

# Specialist consultants
put(P[107], "Item 4 of Schedule B indicates the specialist consultants whose services we recommend are likely to "
            "be needed during the project. As discussed, these specialist consultants are to be engaged by you on "
            "the terms outlined in clause E.1, and their fees will need to be considered in your Total Project "
            "Cost budget. We will coordinate their work, but we are not responsible for the services they "
            "deliver (clause E.1.3).")
put(P[109], "We recommend:")
consultants = [
    "**Structural engineer, Ove Arup & Partners (London):** the roof shells and the podium that carries them are "
    "the central engineering problem of the project;",
    "**Mechanical and electrical engineer, Steensen & Varming (Copenhagen):** air conditioning, electrical "
    "services and lighting for two large halls;",
    "**Quantity surveyor, **{{Rider Hunt & Partners}}**:** cost planning at each stage and the bills of quantities "
    "for tender;",
    "**Geotechnical engineer:** to investigate the ground at Bennelong Point before the foundations are "
    "designed; and",
    "**Acoustic and stage-machinery consultants:** the halls must work for both opera and concerts.",
]
q = P[109]
for text in consultants:
    new = copy.deepcopy(P[18]._element)
    q._element.addnext(new)
    q = put(docx.text.paragraph.Paragraph(new, P[18]._parent), text)

# Disbursements
put(P[118], "Because our office is in Hellebæk, Denmark, the main disbursements will be overseas travel between "
            "Denmark and Sydney, international courier and postage, and presentation models. If these are likely "
            "to be significant, you may wish to consider their likely total amount in your Total Project Cost "
            "budget.")

# Program of services
put(P[121], "We estimate that the design and documentation of the first stage of the works (the podium) can "
            "feasibly be delivered over about {{18 to 24 months}}, with a presentation of the developed scheme "
            "to you in {{early 1958}}.")
put(P[123], "We understand that your Government wishes to start work on site as early as possible. We must advise "
            "that the structure of the roof shells is not yet resolved, and that the roof's loads will govern the "
            "design of the podium and its columns. Starting the podium before the roof design is complete "
            "carries a real risk of later redesign, with extra time and cost. If an early start is required, we "
            "recommend dividing the building work into stages (podium; roof; interiors), each with its own "
            "building contract, and recording this risk in the program and in the contingency above.")
put(P[125], "However, this will depend on several factors critical to the timeframe for delivery of these stages, "
            "such as the time it takes to obtain the necessary Government approvals and to resolve the roof "
            "structure with the engineers. At this point in time, it is not feasible to forecast exactly how long "
            "these will take.")
put(P[127], "In addition, contributing to the indicated timeframe, there are the necessary approvals for building "
            "work to commence and the selection of the contractor. Similarly, we are not in a position to forecast "
            "the time involved before the construction work can begin.")
put(P[129], "Generally, after the building contractor is selected, a building contract signed, and approvals and "
            "finance are secured, construction work can start. We forecast that when construction work starts, "
            "it will take about {{4 years}} to reach practical completion of the first stage (the podium), with "
            "the roof and the interiors following as later stages.")

# New section: communication, changes and variations (Week 10: justify how communications and variations work)
heading = clone_after(P[129], "")
heading.style = P[131].style
put(heading, "Communication, changes and variations")
comms = [
    "Our representative will be Jørn Utzon. Please confirm your Government's representative for the CAA "
    "(clause C.2). If either representative changes, the other party must be told in writing (clause C.3).",
    "All notices, approvals and instructions will be in writing, and email counts (clause H.1). Because our "
    "office is overseas, a posted notice is deemed received 10 business days after posting (clause H.8), so "
    "we will also send every notice by email.",
    "We will report progress at each stage, and ask for your written approval before moving to the next stage "
    "(Schedule A).",
    "If your instructions or the project's needs change the scope of our services, we will promptly tell you in "
    "writing how this affects our fee, and agree the change with you in writing before we carry it out "
    "(clauses A.1.4 and D.8).",
    "Once the building contract is signed, instructions to the builder must be issued only through us (clause "
    "B.2). Changes to the building work will be issued as variations under the building contract, with their "
    "effect on time and cost assessed and recorded.",
]
# each point: a blank spacer, then a body paragraph (copies of the template's own paragraphs)
anchor = heading
for i, text in enumerate(comms):
    para = copy.deepcopy(P[125]._element)
    if i:
        spacer = copy.deepcopy(P[130]._element)
        anchor._element.addnext(spacer)
        spacer.addnext(para)
    else:
        anchor._element.addnext(para)
    anchor = put(docx.text.paragraph.Paragraph(para, P[125]._parent), text)
blank = copy.deepcopy(P[130]._element)
heading._element.addprevious(blank)

# Engaging us (2024 template wording kept; NSW code named)
put(P[136], "Under the Architects Act and the Code of Conduct that applies to our professional services, our "
            "engagement with you must be recorded and confirmed in a written agreement before we start "
            "delivering professional services to you. As discussed and noted above, we propose our engagement is "
            "formalised by signing the Australian Institute of Architects' Client Architect Agreement 2024 that "
            "is enclosed with this letter in draft form. We encourage you to read it carefully, seek legal advice "
            "if you wish and discuss with us any queries you have.")
put(P[138], "We again encourage you to read the 'Information guide to the client' document to assist you in "
            "understanding the CAA and other important elements of our engagement.")
put(P[140], "We look forward to your confirmation. We will then prepare final copies of the CAA and send them to "
            "you to sign and return.")

# Signature
put(P[153], "Jørn Utzon")
put(P[154], "Principal")
put(P[147], "Jørn Utzon, Architect, Hellebæk, Denmark")

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
for section in d.sections:
    for part in (section.header, section.first_page_header, section.even_page_header):
        for r in list(part._element.iter(W + "r")):
            if r.find(W + "pict") is not None and "RMIT Classification" in "".join(r.itertext()):
                r.getparent().remove(r)

d.save(OUT)
print("wrote", OUT)
