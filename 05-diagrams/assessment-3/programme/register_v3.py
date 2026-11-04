"""Document Register v3 — the group's Register, in its original format, matched to the timeline.

Original format (Week 10/DOCUMENT REGISTER_PP1.pdf): Date · Title of Form · Form No. · From · To ·
Action · Contributor · Checker, with the PDF's colour key:
  milestone = grey (no document) · client = blue (client-facing letter / CAA / notice)
  contract = purple (construction contract signing) · sw = green (SW form chain)

Each row: (date, title, form, from, to, action, contributor, checker, kind, assumed, change, sources)
  date      dd.mm.yyyy when the day is known, mm.yyyy when only the month is
  assumed   True when the date is our assumption (the timeline marks it [A])
  change    what changed from Register v2 ("" = unchanged; "NEW" = new row)
  sources   source keys, as on the timeline (A–AF; see event_notes.SOURCES)

Run build_register_v3.py to write the CSV, the markdown and the standalone Excel; the board
workbook's Register sheet reads the same rows.
"""

K, J, P = "Kankawee Maksomboon", "Yu-Chun Ho", "Prani Patton"
S = " (suggested)"

REGISTER = [
    ("13.09.1955", "Competition Design Phase", "", "", "", "", "", "", "milestone", False,
     "Date 1956 to 13.09.1955: the competition was announced on 13 Sep 1955 (entries were submitted in 1956)",
     "D, I"),
    ("29.01.1957", "Competition winner announced (Jørn Utzon)", "", "", "", "", "", "", "milestone", False,
     "NEW: on the timeline (D2)", "D, I"),
    ("11.02.1957", "Introductory letter", "GL1", "Architect", "Client", "Architect to send", K, P, "client", True,
     "Date 'early 1957' to 11.02.1957 [A]; Form No. GL1 added (the guide letter template)", "REG"),
    ("21.02.1957", "Client Architect Agreement", "CAA 2024", "Architect", "Client", "Client to sign", K, P, "client",
     False, "Form No. CAA 2019 to CAA 2024 (the brief requires the 2024 edition)", "REG"),
    ("12.1958", "Tender documents Issued", "", "Architect", "Contractor", "Architect to issue", J + S, K + S, "", False,
     "Date 1958 to 12.1958: conditions of contract + bills of quantities dated Dec 1958", "C"),
    ("01.1959", "Tender Return", "", "Contractor", "Architect", "Architect to review", J + S, K + S, "", True,
     "Date 1959 to 01.1959 [A]", "REG"),
    ("02.1959", "Contractor selection", "", "", "", "", "", "", "milestone", True,
     "Date 1959 to 02.1959 [A] (Civil & Civic)", "REG, D"),
    ("19.02.1959", "Simple Works Contract", "SW 2018", "Architect", "Contractor", "Architect to issue", J, K,
     "contract", False, "", "REG"),
    ("02.03.1959", "Stage I Commences", "", "", "", "", "", "", "milestone", False,
     "Date 1959 to 02.03.1959: site possession / construction ceremony", "A, D"),
    ("22.10.1959", "Client representative change (Cahill to Heffron)", "", "Client", "Architect", "Client to notify",
     K, P + S, "client", False,
     "Was 'Cahill to Askin, 1959': Cahill died 22 Oct 1959 and Heffron became Premier; Askin came in 1965 "
     "(own row below). To = Architect (CAA C.3 notice)", "U, W, D"),
    ("06.1961", "Engineer's advice: final roof loads exceed podium columns", "", "Engineer", "Architect",
     "Architect to review", K, P + S, "", True, "NEW: the trigger for Scenario 1 (timeline D3)", "tutor, AC"),
    ("07.1961", "Change to architectural services (CAA D.8)", "", "Architect", "Client", "Architect to notify", K,
     P + S, "client", True, "Date 1961 to 07.1961 [A]", "—"),
    ("08.1961", "Instruction- for a Variation", "SW-12", "Architect", "Contractor", "Architect to issue", P, J, "sw",
     True, "Date 1961 to 08.1961 [A]", "REG, tutor"),
    ("09.1961", "Contractor's details of claim (optional)", "SW-42", "Contractor", "Architect", "Architect to assess",
     P + S, J + S, "sw", True, "NEW: optional form in the tutor's worked example (1 month, $5,000)", "tutor"),
    ("10.1961", "Instruction to proceed (optional)", "SW-13", "Architect", "Contractor", "Architect to issue", P + S,
     J + S, "sw", True, "NEW: optional form in the tutor's worked example", "tutor"),
    ("11.1961", "Instruction- Adjustment of Time", "SW-14", "Architect", "Contractor", "Architect to issue", P, J,
     "sw", True, "Date 1961 to 11.1961 [A]", "REG, tutor"),
    ("03.1962", "Cost Plan Issued", "CP-06", "QS", "Architect", "Architect to review", J + S, K + S, "", True,
     "Date 1962 to 03.1962 [A]; £13.7m (A$27.4m)", "G"),
    ("04.1962", "Contract Price Adjustment", "SW-11", "Architect", "Contractor", "Architect to Issue", P, J, "sw", True,
     "Date 1962 to 04.1962 [A]", "REG, tutor"),
    ("18.10.1962", "Stage II Contract signed (Minister for Public Works and Hornibrook)", "", "Client", "Contractor",
     "Client to sign", J + S, K + S, "contract", False, "NEW: Stage II agreement", "E, C"),
    ("18.10.1962", "Stage 2 Contract drawings", "", "Architect", "Contractor", "Architect to Issue", J + S, K + S, "",
     False, "Date 1962 to 18.10.1962 (with the Stage II agreement)", "REG, E"),
    ("03.1963", "Stage I Completed", "", "", "", "", "", "", "milestone", False,
     "NEW: podium complete, two years late (A says Feb 1963, D says Mar 1963)", "A, D"),
    ("04.1963", "Stage II Commences", "", "", "", "", "", "", "milestone", False,
     "Date 1962 to 04.1963: 1962 was the agreement (row above); roof works started Apr 1963", "D"),
    ("13.05.1965", "Client representative change (Askin government; Minister Hughes takes over payments)", "",
     "Client", "Architect", "Client to notify", K, P + S, "client", False,
     "NEW: second change of client representative", "D, G, AD"),
    ("28.02.1966", "Architect resigns (Utzon)", "", "Architect", "Client", "Client to acknowledge", K, P + S,
     "client", False, "NEW", "D, G"),
    ("19.04.1966", "Replacement architects appointed (Hall, Todd & Littlemore)", "", "Client", "Architect",
     "Architect to accept", K, P + S, "client", False, "NEW", "D, G"),
    ("11.1966", "Stage III Contract signed (Minister for Public Works and Hornibrook)", "", "Client", "Contractor",
     "Client to sign", J + S, K + S, "contract", False, "NEW: Stage III agreement", "C"),
    ("17.01.1967", "Stage II Completed", "", "", "", "", "", "", "milestone", False,
     "NEW: last (2,194th) shell segment placed", "F"),
    ("17.01.1967", "Stage III Commences", "", "", "", "", "", "", "milestone", False,
     "Date 1967 to 17.01.1967 (interiors start once the shells are finished; site work from 1968)", "F, K"),
    ("07.1968", "Stage 3 Contract drawings", "", "Architect", "Contractor", "Architect to Issue", J + S, K + S, "",
     False, "Date 1968 to 07.1968: Stage III working drawings dated Jul 1968", "I"),
    ("17.01.1973", "Client representative change (Hughes to Punch)", "", "Client", "Architect", "Client to notify",
     K, P + S, "client", False, "NEW: third change of client representative", "AD"),
    ("20.10.1973", "Practical Completion Certificate", "", "Architect", "Contractor", "Architect to Issue", P + S,
     J + S, "", False, "Date 1973 to 20.10.1973: official opening", "J, D"),
    ("20.10.1974", "End of defects liability period", "", "", "", "", "", "", "milestone", True,
     "NEW: 12 months after practical completion (ABIC M13) [A]", "—"),
    ("31.05.1975", "Final Certificate", "SW-31", "Architect", "Contractor", "Architect to Issue", P, J, "sw", False,
     "Date 1974 to 31.05.1975: Architects' Certificate of Completion", "D"),
]

HEADS = ["Date", "Title of Form", "Form No.", "From", "To", "Action", "Contributor", "Checker"]
KIND_FILL = {"milestone": "D9D9D9", "client": "BDD7EE", "contract": "D9C3E9", "sw": "C6E0B4", "": None}
KIND_LABEL = {"milestone": "grey = milestone, no document", "client": "blue = client-facing (letter / CAA / notice)",
              "contract": "purple = construction contract signing", "sw": "green = SW form chain (required forms)"}

# ---------------------------------------------------------------- tutor's format
# Document Register Sample 2026-1.docx: Date · Document · Form No. · From/To · Details (cost etc) ·
# Student Contribution; grey = milestone, green = forms that are part of our assessment, white = other.
TUTOR_HEADS = ["Date", "Document", "Form No.", "From/To", "Details (cost etc)", "Student Contribution"]
ASSESSMENT_FORMS = {"GL1", "CAA 2024", "SW 2018", "SW-12", "SW-42", "SW-13", "SW-14", "SW-11", "SW-31"}
TUTOR_FILL = {"milestone": "D9D9D9", "form": "C5E0B3", "": None}

# title prefix maps to the Details (cost etc) cell. Contract figures are the tutor's worked example
# (contract sum $9,600,000; SW-14 +1 month; SW-11 +$5,000), as in soh_scenario1_timeline.xlsx.
DETAILS = {
    "Competition Design Phase": "Announced by Premier Cahill; 233 entries from 32 countries",
    "Competition winner": "First prize £5,000",
    "Introductory letter": "Cost of Works $9,600,000; fee 6% = $576,000 incl. $10,000 Mobilisation Fee; staged or sequential program",
    "Client Architect Agreement": "Cost of Works $9,600,000; fee 6%; Mobilisation Fee $10,000",
    "Tender documents": "Stage I conditions of contract + bills of quantities",
    "Tender Return": "",
    "Contractor selection": "Civil & Civic Pty Ltd",
    "Simple Works Contract": "Contract price $9,600,000 excl. GST ($10,560,000 incl. GST); Stage I podium; date for practical completion 26.01.1963",
    "Stage I Commences": "Site possession; foundations begin",
    "Client representative change (Cahill": "CAA C.3 notice; Premier Heffron",
    "Engineer's advice": "Ove Arup & Partners",
    "Change to architectural services": "Additional design services and fee (CAA D.8)",
    "Instruction- for a Variation": "Strengthen podium columns, add piers",
    "Contractor's details of claim": "Claims +1 month (20 working days) and +$5,000 excl. GST",
    "Instruction to proceed": "Proceed with the varied work",
    "Instruction- Adjustment of Time": "+1 month (20 working days): date for practical completion 26.02.1963",
    "Cost Plan Issued": "£13.7m (A$27,400,000)",
    "Contract Price Adjustment": "+$5,000 excl. GST (time costs: 20 working days x $275 incl. GST, ABIC Item 18): contract price $9,605,000 excl. GST ($10,565,500 incl.)",
    "Stage II Contract signed": "M.R. Hornibrook (NSW) Pty Ltd: roof shells",
    "Stage 2 Contract drawings": "Roof shells (Yellow Book geometry)",
    "Stage I Completed": "Podium (historically two years behind the original program)",
    "Stage II Commences": "Roof shells, Hornibrook",
    "Client representative change (Askin": "CAA C.3 notice; Minister Davis Hughes",
    "Architect resigns": "Fee dispute with Minister Hughes",
    "Replacement architects": "Hall (design), Todd (documents), Littlemore (supervision), Farmer",
    "Stage III Contract signed": "Hornibrook: interiors + glass walls",
    "Stage II Completed": "Last (2,194th) shell segment placed",
    "Stage III Commences": "Interiors",
    "Stage 3 Contract drawings": "Stage III working drawings",
    "Client representative change (Hughes": "CAA C.3 notice; Minister Leon Punch",
    "Practical Completion Certificate": "Official opening by the Queen",
    "End of defects liability period": "12 months (ABIC M13)",
    "Final Certificate": "Refers to SW-11: final contract price $9,605,000 excl. GST ($10,565,500 incl.). Project final cost $102m (May 1974)",
}


def tutor_rows():
    """REGISTER in the tutor's 6 columns: (values, fill kind, contribution is a suggestion, date assumed)."""
    out = []
    for row in REGISTER:
        date, title, form, frm, to, action, contrib, checker, kind, assumed = row[:10]
        detail = next((v for k, v in DETAILS.items() if title.startswith(k)), "")
        frm_to = f"{frm} to {to}" if frm and to else (frm or to)
        suggested = "(suggested)" in contrib
        student = contrib.replace(" (suggested)", "")
        fill_kind = "form" if form in ASSESSMENT_FORMS else ("milestone" if kind == "milestone" else "")
        out.append(([date, title, form, frm_to, detail, student], fill_kind, suggested, assumed))
    return out
