"""Fill the CAA 2024 (Assessment 3, file 4) from the course's fillable PDF.

Source: D:\\RMIT_SEM2 26_PROPRAC 1\\Assessment 3 resources\\
        (4.Complete a Client Architect Agreement 2024 with the client) caa2024_fullservices_digital.pdf
Every figure (including the $10,000 Mobilisation Fee and the two program options) matches the GL1 letter (letters/build_intro_letter.py), the Register and the timeline.
Assumptions are listed in ../22-caa-2024-notes.md.

Run:  py build_caa.py   (writes "CAA 2024 - Sydney Opera House - draft v1.pdf" next to this file)
Signature boxes and client initials are left for the signers (add with Acrobat Fill & Sign).
"""
import re
import sys
import textwrap
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
SRC = Path(r"D:\RMIT_SEM2 26_PROPRAC 1\Assessment 3 resources"
           r"\(4.Complete a Client Architect Agreement 2024 with the client) caa2024_fullservices_digital.pdf")
OUT = HERE / (sys.argv[1] if len(sys.argv) > 1 else "CAA 2024 - Sydney Opera House - draft v1.pdf")

COST_OF_WORKS = 9_600_000
FEE_PCT = 6.0
SPLIT = {"A.1": 15, "A.2": 15, "A.3": 0, "A.4": 35, "A.5": 5, "A.6": 30}   # share of the fee, as in the letter

# ---- page 1 -------------------------------------------------------------------------------------
TEXT = {
    "Agreement made on date": "21", "Agreement made on month": "02", "Agreement made on year": "1957",
    "Client name": "The Government of New South Wales",
    "Client ABN": "00 000 000 000",
    "Client representative": "The Hon. J. J. Cahill MLA, Premier of NSW",
    "Client address": "Parliament House, Macquarie Street, Sydney NSW 2000",
    "Client mobile": "(02) 5550 0100", "Client email": "premier@placeholder.example",
    "Architect name": "Jørn Utzon, Architect",
    "Architect reg no": "0001",
    "Architect ABN": "00 000 000 001",
    "Architect representative": "Jørn Utzon",
    "Architect address": "Hellebæk, Denmark (office); c/o Sydney agent [A]",
    "Architect mobile": "+45 5550 0100", "Architect email": "utzon@placeholder.example",
    # the Government signs as a corporation (two signatories); Utzon signs as an individual
    "corp client signature date": "21/02/1957", "corp client signature date 2": "21/02/1957",
    "Individual architect signature date": "21/02/1957",
    "the project": ("National Opera House (now the Sydney Opera House): a large hall (about 3,000 seats) and a small "
                    "hall (about 1,200 seats) for opera, concerts, ballet, drama and public meetings, with rehearsal, "
                    "restaurant and back-of-house areas, on a raised podium under a roof of shell vaults. Built in "
                    "stages: I podium, II roof, III interiors."),
    "Located site": "Bennelong Point, Sydney Harbour, Sydney NSW (site of the Fort Macquarie tram depot)",
    "Cost of Works forecast": f"{COST_OF_WORKS:,.0f}",
}

# ---- Schedule A: Included / Excluded / Additional per line ----------------------------------------
INC, EXC, ADD = "Included", "Excluded", "Additional"
COLUMN_X = {INC: 451, EXC: 493, ADD: 536}       # x of each tick column in Schedule A


def schedule_a(code):
    """Default choice for a Schedule A line (field name like 'A4.5' or 'B6.5')."""
    stage, n = code[:2], int(code.split(".")[1])
    if code in ("A1.16", "A2.9"):          # approvals for a planning application: A.3 is excluded
        return EXC
    if stage in ("A1", "A2", "A4", "A6"):
        return INC
    if stage == "A3":                      # Crown project: no planning application (letter, Fees table)
        return EXC
    if stage == "A5":                      # Stage I by tender; later stages may be negotiated
        return INC if n <= 7 or n == 13 else ADD
    if stage == "B4":                      # illustration: drawings and models, time-based (letter)
        return ADD if n <= 2 else EXC
    if stage == "B6":                      # disputes under the building contract, if they arise
        return ADD if n >= 5 else EXC
    return EXC                             # B.1 feasibility (the competition did this), B.2, B.3, B.5


# extra lines written into the blank "comment" rows of Schedule A
COMMENTS = {
    "comment 1": ("arrange a geotechnical investigation of Bennelong Point before the foundations are designed", INC),
    "comment 2": ("resolve the roof shell geometry and structure with the structural engineer before the podium "
                  "design is fixed", INC),
    "comment 13": ("administer a separate building contract for each stage (I podium, II roof, III interiors)", INC),
}

# ---- Schedule B -----------------------------------------------------------------------------------
ITEM1 = {k: f"{FEE_PCT * v / 100:.2f}" for k, v in SPLIT.items()}
ITEM1.update({"B.1": "", "B.2": "", "B.3": "", "B.4": "", "B.5": "", "B.6": "",
              "Total % fee": f"{FEE_PCT:.2f}"})
MOBILISATION = 10_000      # A.0: advance on the fee (= the £5,000 first prize at £1 = A$2); inside the 6%
LUMP = {"Lum sum fee A.0": f"{MOBILISATION:,.0f}", "Total lump Sum fee (GST)": f"{MOBILISATION:,.0f}",
        "GST as calculated on the above": f"{MOBILISATION * 0.1:,.0f}",
        "total lump sume fee (inclu. GST)": f"{MOBILISATION * 1.1:,.0f}"}
ITEM1_TIME_BASED = ["Check Box 10", "Check Box 12"]      # B.4 and B.6 rows: time-based rates apply

RATES = [("Principal/director", 350), ("Team leader", 250), ("Senior architect", 200), ("architect", 170),
         ("Graduate of Architecture", 120), ("Technician", 110)]          # $ per hour excl. GST [A]
RATE_FIELDS = {"Principal/director": ("Principal/director excl GST", "Principal/director incl GST"),
               "Team leader": ("Team leader excl GST", "Team leader incl GST"),
               "Senior architect": ("Senior architect excl GST", "Senior architect incl GST"),
               "architect": ("architect exclu GST", "architect incl GST"),
               "Graduate of Architecture": ("Graduate of Architecture exl GST", "Graduate of Architecture incl GST"),
               "Technician": ("Technician exl GST", "Technician incl GST")}

# Item 3 disbursements: (who pays, admin fee 15%, basis). who: "client" = Client to pay, "reimb" = reimburse
DISB = {
    "Disbursement 1": ("client", False, "Paid by the Client direct"),
    "Disbursement 2": ("client", False, "Paid by the Client direct"),
    "Disbursement 3": ("reimb", True, "At cost + 15% (D.7.2)"),
    "Disbursement 4": ("reimb", False, "At cost"),
    "Disbursement 5": ("reimb", False, "At cost"),
    "Disbursement 6": ("reimb", False, "At cost"),
    "Disbursement 7": ("reimb", False, "At cost"),
    "Disbursement 8": ("reimb", False, "At cost"),
    "Disbursement 9": ("reimb", False, "At cost"),
    "Disbursement 10": ("client", False, "Paid by the Client direct"),
    "Disbursement 11": (None, False, "Included in the Fee"),
    "Disbursement 12": ("reimb", False, "At cost (ATO rate per km)"),
    "Disbursement 13": ("reimb", False, "At cost (economy air fares)"),
    "blank 19": ("reimb", False, "At cost"),
}
DISB_EXTRA_NAME = {"blank 19": "International post and telegrams (Denmark to Sydney)"}

# Item 4 consultants: field -> (who engages, notes)
CONSULT = {
    "Consultant 3": ("client", "Rider Hunt & Partners"),
    "Consultant 4": ("client", "Ove Arup & Partners (London)"),
    "Consultant 5": ("client", "Steensen & Varming (Copenhagen)"),
    "Consultant 6": ("client", "Steensen & Varming (Copenhagen)"),
    "Consultant 12": ("client", "To be appointed"),
    "blank 69": ("client", "To be appointed"),
    "blank 70": ("client", "To be appointed"),
}
CONSULT_EXTRA_NAME = {"blank 69": "Acoustic consultant", "blank 70": "Theatre and stage-machinery consultant"}

ITEMS_5_7 = {
    "blank 71": "Jørn Utzon, Architect",
    "blank 72": "Design: Jørn Utzon, Architect, Hellebæk, Denmark",
    "blank 73": "10,000,000",          # PI insurance, not less than $ [A]
    "blank 74": "20,000,000",          # public liability, not less than $ [A]
    "blank 75": "10",                  # 7A business days (the default)
    "blank 76": "15",                  # 7B % per annum (the default)
}

# ---- Schedule C special conditions: (clause, text) — wrapped over the form's lines ------------------
SPECIAL = [
    ("A.4", "Program (the letter's Option 1, staged): the building work is delivered in three stages (Stage I podium; Stage II roof shells; "
            "Stage III interiors), each under its own building contract."),
    ("A.1", "Mobilisation Fee of $10,000 (excl. GST), payable within 5 business days of signing, is an advance on "
            "the Fee and is deducted from the A.1 Concept design component."),
    ("A.3", "The Architect will report in writing when approved variations exceed 5% of the building contract "
            "sum, with their effect on the forecast Cost of Works."),
    ("A.4", "The Client requires Stage I to start on site before the roof design is resolved. The Architect has "
            "advised in writing (letter of 11.02.1957) that this risks redesign of the podium, with extra time "
            "and cost."),
    ("D.8", "Redesign of work already documented or built, caused by a later design decision for another stage, "
            "is a change to the Services under clause D.8 and is notified and agreed in writing."),
    ("A.6", "The building contract for each stage is the ABIC Simple Works Contract 2018. The Architect "
            "administers it as the Client's agent; the Client instructs the contractor only through the "
            "Architect (B.2)."),
    ("C.2", "The Client's representative is the Premier of NSW or a Minister he nominates in writing. Any "
            "change of representative is notified in writing under clause C.3."),
    ("H.8", "The Architect's office is in Denmark. Every notice is also sent by email, so that receipt does not "
            "depend on overseas post."),
    ("E.1", "The structural and services engineers are engaged and paid by the Client. The Architect "
            "coordinates them but is not responsible for their services."),
]
WRAP = 112  # characters per "Details" line


# ---- fill -----------------------------------------------------------------------------------------
def set_text(w, value, size=None):
    w.field_value = value
    if size is not None:
        w.text_fontsize = size
    w.update()


def pick_radio(widgets, x_target=None, state=None):
    """Turn on one button of a radio group (by x position or on-state name); the rest off."""
    def chosen(w):
        return (state is not None and w.on_state() == state) or                (x_target is not None and abs(w.rect.x0 - x_target) < 6)
    for w in widgets:
        if not chosen(w):
            w.field_value = False
            w.update()
    for w in widgets:
        if chosen(w):
            w.field_value = True
            w.update()


def main():
    doc = pymupdf.open(SRC)
    special_lines = []
    for clause, text in SPECIAL:
        for i, line in enumerate(textwrap.wrap(text, WRAP)):
            special_lines.append((clause if i == 0 else "", line))
    assert len(special_lines) <= 26, "Schedule C overflows"   # rows 27+ share field names

    for page in doc:
        widgets = list(page.widgets())
        by_name = {}
        for w in widgets:
            by_name.setdefault(w.field_name, []).append(w)
        radios = {}
        for w in widgets:
            if w.field_type == pymupdf.PDF_WIDGET_TYPE_RADIOBUTTON:
                radios.setdefault(w.field_name, []).append(w)

        def radio_on_row(y_mid):
            for name, group in radios.items():
                if abs((group[0].rect.y0 + group[0].rect.y1) / 2 - y_mid) < 6:
                    return group
            return None

        for w in widgets:
            name = w.field_name
            ymid = (w.rect.y0 + w.rect.y1) / 2
            if name in TEXT:
                set_text(w, TEXT[name], 8 if name in ("the project", "Located site") else None)
            elif re.match(r"^[AB]\d\.\d+$", name):                      # Schedule A line
                group = radio_on_row(ymid)
                if group:
                    pick_radio(group, x_target=COLUMN_X[schedule_a(name)])
            elif name in COMMENTS:
                text, choice = COMMENTS[name]
                set_text(w, text, 7)
                group = radio_on_row(ymid)
                if group:
                    pick_radio(group, x_target=COLUMN_X[choice])
            elif name in ITEM1 and page.number == 13:
                set_text(w, ITEM1[name])
            elif name in LUMP and page.number == 13:
                set_text(w, LUMP[name])
            elif name in ITEM1_TIME_BASED:
                w.field_value = True
                w.update()
            elif name in DISB or name in DISB_EXTRA_NAME:
                if name in DISB_EXTRA_NAME:
                    set_text(w, DISB_EXTRA_NAME[name], 7)
                who, admin, basis = DISB[name]
                group = radio_on_row(ymid)
                if group and who:
                    pick_radio(group, x_target=366 if who == "client" else 414)
                for o in widgets:                                       # basis column and admin-fee box
                    oy = (o.rect.y0 + o.rect.y1) / 2
                    if abs(oy - ymid) < 6 and o.rect.x0 > 480 and o.field_type == pymupdf.PDF_WIDGET_TYPE_TEXT:
                        set_text(o, basis, 6)
                    if abs(oy - ymid) < 6 and o.field_type == pymupdf.PDF_WIDGET_TYPE_CHECKBOX and admin:
                        o.field_value = True
                        o.update()
            elif name in CONSULT:
                who, notes = CONSULT[name]
                if name in CONSULT_EXTRA_NAME:
                    set_text(w, CONSULT_EXTRA_NAME[name])
                group = radio_on_row(ymid)
                if group:
                    pick_radio(group, x_target=358 if who == "client" else 406)
                for o in widgets:
                    oy = (o.rect.y0 + o.rect.y1) / 2
                    if abs(oy - ymid) < 6 and o.rect.x0 > 430 and o.field_type == pymupdf.PDF_WIDGET_TYPE_TEXT:
                        set_text(o, notes, 7)
            elif name in ITEMS_5_7:
                set_text(w, ITEMS_5_7[name])

        if page.number == 14:                                            # Item 2 rates (printed page 14)
            for role, rate in RATES:
                ex, inc = RATE_FIELDS[role]
                set_text(by_name[ex][0], f"{rate}")
                set_text(by_name[inc][0], f"{rate * 1.1:.0f}")
            for i in range(1, 7):
                w = by_name[f"Time unit {i}"][0]
                w.field_value = "Per Hour"
                w.update()

        if page.number == 16:                                            # Schedule C
            rows = sorted([w for w in widgets if w.field_name.startswith(("Clause no.", "Details line"))],
                          key=lambda w: (round(w.rect.y0 / 4), w.rect.x0))
            rows = [w for w in rows if w.rect.y0 < 580]           # below this the form reuses field names
            clause_cells = [w for w in rows if w.field_name.startswith("Clause no.")]
            detail_cells = [w for w in rows if w.field_name.startswith("Details line")]
            for (clause, line), cw, dw in zip(special_lines, clause_cells, detail_cells):
                set_text(cw, clause, 7)
                set_text(dw, line, 7)

    doc.save(OUT, garbage=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
