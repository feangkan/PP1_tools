"""Assessment 3: two versions of the compiled submission, from Lead 3's SW forms (received 05.11.2026).

  py build_versions.py 1   Ver.1: Lead 3's four forms combined as received (only their review comments removed),
                           with a suggestion fix report. Uses the parts built on 04.11.2026.
  py build_versions.py 2   Ver.2: the forms corrected (content kept, missing items added), Lead 2 and Lead 3 fixes
                           applied to the Register, Timeline and ABIC, every part rebuilt, with a fix report.

Writes  D:\\RMIT_SEM2 26_PROPRAC 1\\Week 12\\Ready to submit\\Ver.1 - Lead 3 forms combined\\
        D:\\RMIT_SEM2 26_PROPRAC 1\\Week 12\\Ready to submit\\Ver.2 - revised\\
Each version folder has an inputs\\ folder. Save the group's "ARBV letter.pdf" there and re-run: the red slot page
goes and the file name loses its "(ARBV letter to insert)" suffix.
"""
import os, re, shutil, sys
import pymupdf

import build_submission as bs

LEAD3 = r"C:\Users\feang\.claude\uploads\f9cb5449-8ffc-4067-bdee-b6137d07aa6c"
FORMS_IN = {"SW-12": "14f7eaf9-SW-12_Architects_instruction_for_a_variation_1.docx.pdf",
            "SW-14": "eaad3261-SW-14_Adjustment_of_time.pdf",
            "SW-11": "07ac7140-SW-11_Contract_Price_Adjustment_1.pdf",
            "SW-31": "47b69c5d-SW-31_Final_certificate.pdf"}
READY = bs.OUT
VER1 = os.path.join(READY, "Ver.1 - Lead 3 forms combined")
VER2 = os.path.join(READY, "Ver.2 - revised")
FONTS = r"C:\Windows\Fonts"
SURNAMES = "_".join(f"{l}_{f}" for f, l in bs.GROUP)
DUE = "Due Fri 6 Nov 2026, 23:59"


# ------------------------------------------------------------------ shared
def strip_comments(doc):
    """Remove review notes and highlights (Lead 3's comments to the group); returns them for the report."""
    notes = []
    kinds = ("Text", "Highlight", "FreeText", "Underline", "StrikeOut")
    for pno, page in enumerate(doc, start=1):
        found = [(a.xref, a.type[1], (a.info.get("content") or "").strip()) for a in page.annots()
                 if a.type[1] in kinds]
        for xref, kind, content in found:
            if content:
                notes.append((pno, kind, content))
            try:
                page.delete_annot(page.load_annot(xref))  # also removes its popup and replies
            except Exception:
                pass                                      # already removed as a reply of an earlier note
    return notes


def compile_version(folder, label, parts):
    """Compile with build_submission's order and front pages, into folder; name keeps the ARBV status visible."""
    inputs = os.path.join(folder, "inputs")
    bs.OUT, bs.INPUTS = folder, inputs
    bs.compile_all(parts)
    built = [f for f in os.listdir(folder) if f.startswith("Assessment Task 3_") and f.endswith(".pdf")][0]
    arbv = os.path.exists(os.path.join(inputs, "ARBV letter.pdf"))
    final = (f"Assessment Task 3_{SURNAMES}_{label}.pdf" if arbv
             else f"Assessment Task 3_{SURNAMES}_{label} (ARBV letter to insert).pdf")
    for old in os.listdir(folder):
        if old.startswith("Assessment Task 3_") and old.endswith(".pdf") and old != built:
            os.remove(os.path.join(folder, old))
    os.replace(os.path.join(folder, built), os.path.join(folder, final))
    doc = pymupdf.open(os.path.join(folder, final))
    print(f"{label}: {final}  ({doc.page_count} pages)")
    return final, doc.page_count, arbv


REPORT_CSS = """
* { font-family: sans-serif; color: #222; }
h1 { font-size: 15px; margin: 0 0 3px 0; } h2 { font-size: 11.5px; margin: 12px 0 4px 0; color: #1a6b35; }
p, td, th, li { font-size: 8.6px; line-height: 1.32; } .sub { font-size: 9.5px; color: #555; margin: 0 0 8px 0; }
table { border-collapse: collapse; width: 100%; margin-bottom: 6px; }
th, td.hd { color: #1a6b35; text-align: left; padding: 3px 4px; font-size: 8.3px; font-weight: bold; border-bottom: 1.2px solid #1a6b35; }
td { border-bottom: 0.5px solid #bbb; padding: 3px 4px; vertical-align: top; }
.H { color: #b00000; font-weight: bold; } .M { color: #b06000; font-weight: bold; } .L { color: #555; font-weight: bold; }
.done { color: #1a6b35; font-weight: bold; } .todo { color: #b00000; font-weight: bold; } .kept { color: #1f4e78; font-weight: bold; }
.box { border: 1.2px solid #b00000; padding: 6px 8px; margin: 6px 0; } .ok { border: 1.2px solid #1a6b35; padding: 6px 8px; margin: 6px 0; }
"""


def html_pdf(html, path, landscape=True):
    """Lay the report out section by section (split at <h2>), continuing down the page. Laying out the whole report
    as one story can loop forever when a block cannot break at a page end, so each section is its own story and
    the page count is capped."""
    rect = pymupdf.paper_rect("a4-l" if landscape else "a4")
    body = rect + (36, 36, -36, -40)
    chunks = [c for c in re.split(r"(?=<h2>)", html) if c.strip()]
    writer = pymupdf.DocumentWriter(path)
    dev, y, n = writer.begin_page(rect), body.y0, 1
    for chunk in chunks:
        story = pymupdf.Story(html=chunk, user_css=REPORT_CSS)
        more = 1
        while more:
            if body.y1 - y < 60:                                   # too little room left: next page
                writer.end_page(); dev, y, n = writer.begin_page(rect), body.y0, n + 1
            more, filled = story.place(pymupdf.Rect(body.x0, y, body.x1, body.y1))
            story.draw(dev)
            y = filled[3] + 18
            if more:
                writer.end_page(); dev, y, n = writer.begin_page(rect), body.y0, n + 1
            assert n < 40, "report layout runaway"
    writer.end_page()
    writer.close()
    doc = pymupdf.open(path)
    for i, page in enumerate(doc, start=1):
        page.insert_text((36, rect.height - 18), f"{os.path.basename(path)[:-4]}  ·  page {i} of {doc.page_count}",
                         fontsize=7, color=(0.4, 0.4, 0.4))
    doc.saveIncr()
    print("wrote", os.path.basename(path), f"({doc.page_count} pages)")


def table(rows, heads):
    th = "".join(f"<td class='hd'>{h}</td>" for h in heads)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><tr>{th}</tr>{tr}</table>"


# ------------------------------------------------------------------ Ver.1
# The Conventions and assumptions page as it was on 04.11.2026 (before the Ver.2 corrections).
V1_ASSUMPTIONS = [
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

V1_ISSUES = [  # (priority, form, where, problem, suggestion)
    ("H", "SW-31", "Contractor, A to E",
     "Issued to <b>M.R. Hornibrook</b> and certifies the whole project ($102m, all stages as 'adjustments'). Our ABIC "
     "contract is with <b>Civil &amp; Civic, Stage I only</b> (ABIC special condition 1); the Hornibrook Stage II/III "
     "agreements are separate contracts that are not in our file.",
     "Certify the Stage I contract: contractor Civil &amp; Civic Pty Ltd; A $9,600,000; B $5,000 (SW-11); C $9,605,000; "
     "D GST $960,500; E $10,565,500. Keep Hall, Todd &amp; Littlemore issuing it on 31/05/1975 (already declared)."),
    ("H", "SW-31", "whole form",
     "Does not <b>refer to SW-11</b>, which the brief requires.",
     "Add 'Refers to SW-11, Ref No. 03' and take B from SW-11."),
    ("H", "SW-31", "Items 1, 2, notes A, E",
     "5% cash retention ($5,100,000) and $20,000 bank fees. The ABIC strikes out cash retention: the security is an "
     "unconditional guarantee of $264,000 (ABIC, compiled p.47).",
     "Items 1 and 2 = $0.00; notes A and E = $0.00; the guarantee is returned with the final certificate."),
    ("H", "SW-31", "Items 5 to 7",
     "Arithmetic: E-1-2-3-4 = $107,060,000, not $5,100,000. Item 6 says nothing was certified in any earlier "
     "progress certificate.",
     "With the Stage I figures: 5 = $10,545,500. Previous certificates [A] = $10,565,500 (all progress claims paid). "
     "7 = 5-6 = $20,000 due to the <b>owner</b> (the liquidated damages), strike out 'contractor'."),
    ("M", "SW-31", "Project No., owner",
     "Project No. 03 (01 on the other forms); owner line missing ')' and differs from the ABIC.",
     "Project No. 01; owner 'The Government of New South Wales' (ABIC Item 1)."),
    ("H", "SW-14", "Sum recoverable",
     "Time costs $1,000. ABIC Schedule 1 Item 18 is $275 incl. GST per working day: 20 working days = $5,500 incl. GST "
     "($5,000 excl.), the figure SW-11 adds. As drawn, SW-14 and SW-11 don't add up (rubric C1).",
     "$5,500 incl. GST (20 working days x $275, Item 18)."),
    ("M", "SW-14", "Date issued",
     "01/10/1961 is a <b>Sunday</b>.", "02/10/1961 (Monday): still 14 working days after the 12/09/1961 claim, inside "
     "the 20 days of H4 (Lead 3's own aim)."),
    ("M", "SW-14", "Cause of delay",
     "Only L1.1(f) (owner's consultants late with information). The delay comes from the variation itself, an "
     "architect's instruction.", "Keep (f) and add L1.1(c): the architect's instruction SW-12, No. 01 of 01/08/1961."),
    ("L", "SW-14", "Previous adjustment", "'NA'.", "'Nil'."),
    ("H", "SW-11", "Additions / description",
     "+$5,000 is described as the piers' cost 'verified in CP-06'. The agreed chain (Register, assumptions page, "
     "ABIC Item 18) makes the $5,000 the SW-14 time costs; CP-06 is the QS's whole-project cost plan, not a check of "
     "this claim.", "Keep the piers description; state the basis: SW-14 time costs, 20 working days x $250 (Item 18)."),
    ("M", "SW-11", "claim / variation quotation",
     "'claim' is struck out, but the H4 box (claims) is ticked and the form assesses the SW-42 claim.",
     "Strike out 'variation quotation' instead and keep 'claim'."),
    ("M", "SW-11", "Date issued", "01/04/1962 is a <b>Sunday</b>.", "02/04/1962 (Monday), the data-sheet date."),
    ("M", "SW-11", "Page 2", "An almost empty overflow page (signature and distribution repeated).", "Delete page 2."),
    ("M", "SW-12, 14, 11", "Owner",
     "'The Minister for Public Works (NSW Government)'. The ABIC owner is 'The Government of New South Wales'.",
     "Use the ABIC name on every form (rubric C5, consistency)."),
    ("L", "SW-12", "Instruction", "'Ove Arup &amp; Partners’s' (typo). No reason or J2.3 notice request.",
     "'Partners’'; add the reason (roof loads exceed the podium columns) and the 20-working-day notice (J2.3)."),
    ("L", "SW-14, 11, 31", "Signature line", "Three different wordings.",
     "Use the file's convention: 'Signature omitted — academic simulation'."),
    ("H", "Register + Timeline", "SW dates",
     "The forms now say SW-42 claim 12/09/1961 and SW-14 01/10/1961; the Register and Timeline still say 09.1961 and "
     "11.1961. Stage I completion: Lead 3 deducts $20,000 liquidated damages, so Stage I finished 20 days after "
     "26.02.1963, i.e. 18.03.1963, which the Register doesn't say.",
     "Update both to the form dates; Stage I practical completion 18.03.1963 [A], 'LDs $20,000 deducted in SW-31'."),
]
V1_KEPT = [
    "SW-11 dated April 1962, after the J5 period: Lead 3 notes it is 'historically dated' and would be a breach today. "
    "That is a strong ARBV-letter point (keep the date, explain it in Part B).",
    "Liquidated damages $20,000 in SW-31: this answers Lead 2's open item 4 (Stage I finished after 26.02.1963).",
    "SW-14 issued within 20 working days of the claim (H4), and SW-31 issued by Hall, Todd &amp; Littlemore in 1975.",
]
LEAD2_OPEN = [
    ("4", "H", "Stage I completion vs the adjusted date", "Answered by Lead 3's $20,000 LDs if the group accepts it: "
     "set Stage I practical completion 18.03.1963 in the Register and Timeline."),
    ("5", "M", "Invented names in the ABIC (James Wilson etc.)", "Declared on the assumptions page; keep."),
    ("6", "M", "$9.6m used for Stage I and the whole project", "Declared on p.2; the ARBV letter should say so."),
    ("7", "L", "ABIC Schedule 3 item 6 blank", "Add 'Bills of quantities, Rider Hunt &amp; Partners, Dec 1958'."),
    ("8", "L", "Register tender rows: grey (suggested) names", "Confirm (Yu-Chun Ho)."),
]
LEAD3_OPEN = [
    ("2", "H", "SW-31 refers to SW-11", "Not done (see SW-31 above)."),
    ("3", "H", "H4 / J5 timing", "H4 done in SW-14 (within 20 working days). J5: SW-11 kept at 04.1962 on purpose; "
     "explain in the ARBV letter."),
    ("4", "M", "Register row: notice to the contractor of the replacement architects (04.1966)", "Not done."),
    ("5", "M", "Register: the 1973 Practical Completion row is the whole building, not Stage I", "Not done."),
    ("7", "L", "Register: (suggested) names on SW-42, SW-13 and the 1973 certificate", "Confirm (Prani Patton)."),
]


def ver1():
    os.makedirs(os.path.join(VER1, "inputs"), exist_ok=True)
    notes = []
    for k, f in FORMS_IN.items():
        d = pymupdf.open(os.path.join(LEAD3, f))
        notes += [(k, p, t, c) for p, t, c in strip_comments(d)]
        d.save(os.path.join(VER1, "inputs", f"{k}.pdf"), garbage=3, deflate=True)
    parts = {"a1": "a1 Architects Register.pdf", "a2": "a2 Timeline.pdf", "b": "b Introductory letter.pdf",
             "c": "c CAA 2024.pdf", "d": "d ABIC SW 2018.pdf"}
    parts = {k: os.path.join(bs.PARTS, v) for k, v in parts.items()}
    letter = os.path.join(VER2, "inputs", "ARBV letter.pdf")
    if os.path.exists(letter):
        shutil.copy(letter, os.path.join(VER1, "inputs", "ARBV letter.pdf"))
    saved, bs.ASSUMPTIONS = bs.ASSUMPTIONS, V1_ASSUMPTIONS
    name, pages, arbv = compile_version(VER1, "Ver.1", parts)
    bs.ASSUMPTIONS = saved
    order = {"H": 0, "M": 1, "L": 2}
    issues = sorted(V1_ISSUES, key=lambda r: order[r[0]])
    rows = [(f"<span class='{p}'>{ {'H': 'High', 'M': 'Med', 'L': 'Low'}[p] }</span>", f, w, prob, sug)
            for p, f, w, prob, sug in issues]
    html = f"""<h1>Ver.1 — Lead 3's forms combined: suggestion fix report</h1>
<p class="sub">Built 05.11.2026 · {DUE} · File: <b>{name}</b> ({pages} pages) in <i>Ready to submit\\Ver.1 - Lead 3 forms combined</i></p>
<div class="box"><b>Ver.1 = Lead 3's forms as received</b> (only their 11 review comments taken off, listed at the end), with
the ARBV letter draft v1 (pages 3-4). <b>The letter was written for the corrected figures of Ver.2</b>, so in Ver.1 it
contradicts the forms below (for example SW-31 to Hornibrook for $112.2m, SW-14 time costs $1,000). Ver.2 is the
consistent version. The letter the group tried was the example submission's own letter almost word for word:
do not submit that one.</div>
<h2>Suggested fixes to the forms, highest first</h2>
{table(rows, ["Priority", "Form", "Where", "Problem", "Suggestion"])}
<h2>Good decisions in Lead 3's forms (keep them)</h2><ul>{''.join(f'<li>{k}</li>' for k in V1_KEPT)}</ul>
<h2>Still open from the 04.11 checklist</h2>
{table([(n, f"<span class='{p}'>{p}</span>", w, s) for n, p, w, s in LEAD2_OPEN], ["Lead 2 #", "Pri.", "Item", "Status / suggestion"])}
{table([(n, f"<span class='{p}'>{p}</span>", w, s) for n, p, w, s in LEAD3_OPEN], ["Lead 3 #", "Pri.", "Item", "Status / suggestion"])}
<p><b>Whole group:</b> write the ARBV letter (also explain the SW-11 timing, $9.6m for Stage I, and SW-31 in 1975);
confirm the grey (suggested) names in the Register; ask the tutor whether one person submits for the group.</p>
<h2>Lead 3's review comments (removed from the submission copy, kept here)</h2>
{table([(k, p, t, c) for k, p, t, c in notes], ["Form", "Page", "Type", "Comment"])}
<p><b>Ver.2</b> (<i>Ready to submit\\Ver.2 - revised</i>) applies every fix above, keeping Lead 3's content and decisions.</p>"""
    html_pdf(html, os.path.join(VER1, "Ver.1 - Suggestion fix report (not for submission).pdf"))


# ------------------------------------------------------------------ Ver.2: corrected forms
FONT_FILES = {"PalatinoLinotype-Roman": "pala.ttf", "PalatinoLinotype-Bold": "palab.ttf",
              "PalatinoLinotype-Italic": "palai.ttf", "Calibri": "calibri.ttf", "Calibri-Bold": "calibrib.ttf",
              "Calibri-Italic": "calibrii.ttf"}
INK = (0, 0, 0)


class Form:
    """Edits one of Lead 3's PDFs in place: swap a value in its own font, add a line, strike a word."""

    def __init__(self, path):
        self.doc = pymupdf.open(path)
        self.log = []

    def _span(self, page, rect):
        best = None
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for sp in l["spans"]:
                    r = pymupdf.Rect(sp["bbox"])
                    if r.intersects(rect) and sp["text"].strip():
                        if best is None or (r & rect).get_area() > (pymupdf.Rect(best["bbox"]) & rect).get_area():
                            best = sp
        return best

    def _font(self, page, name):
        fname = FONT_FILES.get(name, "pala.ttf")
        alias = "f_" + fname.split(".")[0]
        page.insert_font(fontname=alias, fontfile=os.path.join(FONTS, fname))
        return alias, pymupdf.Font(fontfile=os.path.join(FONTS, fname))

    def hits(self, old, pno=0, clip=None):
        """Matches of old, top to bottom. A match that runs across two text pieces comes back as two touching
        rectangles on one line: those are merged into one."""
        page = self.doc[pno]
        rects = sorted(page.search_for(old, clip=clip), key=lambda r: r.x0)
        merged = []
        for r in rects:
            for i, m in enumerate(merged):
                if abs((m.y0 + m.y1) / 2 - (r.y0 + r.y1) / 2) < 3 and -1 < r.x0 - m.x1 < 1:
                    merged[i] = m | r
                    break
            else:
                merged.append(pymupdf.Rect(r))
        return sorted(merged, key=lambda r: (round(r.y0), r.x0))

    def swap(self, old, new, pno=0, nth=None, clip=None, align="left", fontname=None, size=None, why="",
             remove_lines=False, log=True):
        page = self.doc[pno]
        found = self.hits(old, pno, clip)
        assert found and (nth is not None or len(found) == 1), (old, found)
        r = found[nth or 0]
        sp = self._span(page, r)
        fontname = fontname or (sp["font"] if sp else "PalatinoLinotype-Roman")
        size = size or (sp["size"] if sp else 11)
        base = sp["origin"][1] if sp else r.y1 - 0.24 * size
        page.add_redact_annot(r, fill=False)
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                              graphics=(pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED if remove_lines
                                        else pymupdf.PDF_REDACT_LINE_ART_NONE))
        if new:
            alias, font = self._font(page, fontname)
            x = r.x1 - font.text_length(new, size) if align == "right" else r.x0
            page.insert_text((x, base), new, fontname=alias, fontsize=size, color=INK)
        if log:
            self.log.append((old, new, why))
        return r

    def add(self, rect, text, fontname="PalatinoLinotype-Roman", size=10, pno=0, why="", lineheight=1.3):
        """Wrap text to the rect's width and set each line at size x lineheight spacing."""
        page = self.doc[pno]
        rect = pymupdf.Rect(rect)
        alias, font = self._font(page, fontname)
        lines, cur = [], ""
        for w in text.split():
            trial = (cur + " " + w).strip()
            if font.text_length(trial, size) <= rect.width or not cur:
                cur = trial
            else:
                lines.append(cur); cur = w
        lines.append(cur)
        step = size * lineheight
        assert len(lines) * step <= rect.height + 2, ("text does not fit", text[:40], len(lines))
        for k, line in enumerate(lines):
            page.insert_text((rect.x0, rect.y0 + size + k * step), line, fontname=alias, fontsize=size, color=INK)
        self.log.append(("(added)", text, why))

    def strike(self, text, pno=0, clip=None, why=""):
        page = self.doc[pno]
        r = self.hits(text, pno, clip)[0]
        y = (r.y0 + r.y1) / 2 + 0.5
        page.draw_line((r.x0, y), (r.x1, y), color=INK, width=0.8)
        self.log.append((f"strike out '{text}'", "", why))

    def save(self, path):
        self.doc.save(path, garbage=3, deflate=True)


OWNER_OLD = "Owner: The Minister for Public Works (NSW Government)"
OWNER_NEW = "Owner: The Government of New South Wales"
WHY_OWNER = "Owner as named in the ABIC (Item 1)"


def fix_sw12(f):
    f.swap(OWNER_OLD, OWNER_NEW, why=WHY_OWNER)
    f.swap("Partners’s", "Partners’", why="Typo")
    last = f.hits("latest drawing set issuance")[0]
    f.add((last.x0, last.y1 + 10, 540, last.y1 + 110),
          "Reason: the final roof loads advised by Ove Arup & Partners in June 1961 exceed what the podium columns "
          "built in Stage I were designed to carry. Under clause J2.3, give written notice of the effect of this "
          "variation on the contract price and on the date for practical completion within 20 working days. This "
          "instruction is issued on behalf of the owner.", fontname="Calibri", size=11,
          why="Added: the reason for the variation and the J2.3 notice (data sheet)")
    f.swap("Signature omitted - academic simulation", bs.SIG, why="Signature convention of the file")


def fix_sw14(f):
    f.swap(OWNER_OLD, OWNER_NEW, why=WHY_OWNER)
    f.swap("01/10/1961", "02/10/1961", why="01/10/1961 was a Sunday; still 14 working days after the claim (H4)")
    prev = f.hits("Previous adjustment of time granted")[0]
    f.swap("NA", "Nil", clip=pymupdf.Rect(prev.x1, prev.y0 - 2, 600, prev.y1 + 2), align="right",
           why="'Nil' instead of 'NA'")
    f.swap("1 Calendar Month", "1 month (20 working days)", align="right", why="State the working days used for costs")
    f.swap("$1,000", "$5,500 incl. GST (Item 18)",
           why="ABIC Item 18: 20 working days x $275 incl. GST = $5,500 (the figure SW-11 adds, excl. GST)")
    end = f.hits("reasonable and the adjusted date is accepted.")[0]
    f.add((79, end.y1 + 10, 545, end.y1 + 105),
          "Also under clause L1.1c (an architect's instruction): the variation instructed in SW-12, Instruction "
          "No. 01 dated 01/08/1961 (additional piers to the podium columns). Adjustment of time costs: 20 working "
          "days x $275 incl. GST (Schedule 1, Item 18) = $5,500 incl. GST ($5,000 excl. GST), added to the contract "
          "price by SW-11.", size=10.5, why="Added the L1.1c cause (the variation) beside Lead 3's L1.1f, and the "
          "time-cost basis")
    f.swap("No Signature - Academic Simulation", bs.SIG, why="Signature convention of the file")


def fix_sw11(f):
    f.swap(OWNER_OLD, OWNER_NEW, why=WHY_OWNER)
    f.swap("01/04/1962", "02/04/1962", why="01/04/1962 was a Sunday (the data-sheet date is 02/04/1962)")
    para = f.hits("You are advised that your")[0]
    clip = pymupdf.Rect(para.x0, para.y0 - 2, 560, para.y1 + 2)
    f.swap("claim", "claim", clip=clip, remove_lines=True, why="Un-strike 'claim': H4 (claims) is ticked and "
           "the form assesses the SW-42 claim")
    f.strike("variation quotation", clip=clip, why="Strike out 'variation quotation' instead")
    cell = None
    for t in ("As described", "in SW-42, and", "verified in", "CP-06"):
        r = f.swap(t, "", log=False)
        cell = r if cell is None else cell | r
    f.log.append(("As described in SW-42, and verified in CP-06", "", "Additions basis restated (next row)"))
    f.add((cell.x0, cell.y0 - 1, cell.x1 + 1, cell.y1 + 8), "SW-14 time costs: 20 working days x $250 (Item 18)",
          size=8.5, lineheight=1.2, why="Additions basis: the SW-14 time costs (Item 18). CP-06 is the QS's whole-project cost plan")
    sub = f.hits("Subtotal")[0]
    f.add((79, sub.y1 + 3, 560, sub.y1 + 28),
          "Claim No. 03 (SW-42, 12/09/1961) · time and costs: SW-14, Ref No. 02 (02/10/1961) · "
          "variation: SW-12, Instruction No. 01 (01/08/1961)", fontname="PalatinoLinotype-Italic", size=8,
          why="Added the references that tie SW-11 to SW-12, SW-42 and SW-14")
    f.swap("No Architect's Signature - Academic Simulation", bs.SIG, why="Signature convention of the file")
    if f.doc.page_count > 1:
        f.doc.delete_page(1)
        f.log.append(("page 2", "(deleted)", "Empty overflow page: signature and distribution repeated"))


def fix_sw31(f):
    f.swap("Project No.: 03", "Project No.: 01", why="Same project number as the other forms")
    f.swap("Owner: The Minister for Public Works (NSW Government", OWNER_NEW, why=WHY_OWNER + "; closing ')' missing")
    f.swap("Contractor: M.R. Hornibrook (NSW) Pty Ltd", "Contractor: Civil & Civic Pty Ltd",
           why="The ABIC contract this certificate closes is Civil & Civic's (Stage I)")
    head = f.hits("Hall, Todd & Littlemore")[0]
    f.add((head.x0, head.y1 + 4, 560, head.y1 + 30),
          "Final certificate (N11), ABIC SW 2018 contract of 19/02/1959, Stage I podium works · refers to SW-11, "
          "Ref No. 03 (02/04/1962)",
          fontname="PalatinoLinotype-Italic", size=8.5, why="Added: which contract it closes, and the SW-11 reference "
          "the brief requires")
    bl = f.hits("to date:")[0]
    alias, _ = f._font(f.doc[0], "PalatinoLinotype-Roman")
    f.doc[0].insert_text((bl.x1 + 3, bl.y1 - 3.2), "(SW-11)", fontname=alias, fontsize=11, color=INK)
    f.log.append(("B label", "+ '(SW-11)'", "Item B is the SW-11 adjustment"))
    R = "right"
    f.swap("$9600000", "$9,600,000", align=R, why="Format")
    f.swap("$92395000", "$5,000", align=R, why="B = SW-11 only: the Stage I adjustment (Lead 3 had all stages, $92.4m)")
    f.swap("$102000000", "$9,605,000", align=R, why="C = A + B")
    f.swap("$112200000", "$10,565,500", align=R, why="E = C + D, as in SW-11")
    f.swap("$10200000", "$960,500", align=R, why="D = 10% GST on C")
    f.swap("$$20000", "$0.00", align=R, why="Note E: no cash retention, so no bank fees")
    r51 = f.hits("$5100000")
    assert len(r51) == 4, r51
    f.swap("$5100000", "$0.00", nth=0, align=R, why="Item 1: cash retention is struck out in the ABIC (guarantee)")
    f.swap("$5100000", "$10,545,500", nth=0, align=R, why="Item 5 = E - 1 - 2 - 3 - 4")
    f.swap("$5100000", "$20,000", nth=0, align=R, why="Item 7 = 5 - 6, due to the owner")
    f.swap("$5100000", "$0.00", nth=0, align=R, why="Note A: no cash retention")
    r20 = f.hits("$20000")
    assert len(r20) == 3, r20
    f.swap("$20000", "$0.00", nth=0, align=R, why="Item 2: no cash retention, so no bank fees")
    f.swap("$20000", "$20,000", nth=0, align=R, why="Item 3: Lead 3's liquidated damages kept (format)")
    f.swap("$20000", "$20,000", nth=0, align=R, why="Note B: format")
    z = f.hits("$0.00")
    item6 = f.hits("Total amount certified at")[0]
    k = [i for i, r in enumerate(z) if abs(r.y0 - item6.y0) < 6][0]
    f.swap("$0.00", "$10,565,500", nth=k, align=R, why="Item 6: all progress certificates assumed paid in full [A]")
    f.swap("thousand", "", why="Amount in words (next row)")
    f.swap("Five Million one hundred", "Twenty thousand dollars", why="Amount in words: $20,000")
    item7 = f.hits("Amount certified as due and owing")[0]
    f.strike("contractor", clip=pymupdf.Rect(item7.x0, item7.y0 - 2, 560, item7.y1 + 2),
             why="Item 7: the amount is due to the owner, so 'contractor' is struck out")
    f.swap("No Signature- Academic Simulation", bs.SIG, why="Signature convention of the file")


FIXERS = {"SW-12": fix_sw12, "SW-14": fix_sw14, "SW-11": fix_sw11, "SW-31": fix_sw31}

LEAD2_V2 = [
    ("4", "FIXED", "Stage I completion vs the adjusted date",
     "Lead 3's $20,000 liquidated damages adopted: Stage I practical completion 18.03.1963 [A] (20 days after "
     "26.02.1963) in the Register, Timeline and assumptions page; deducted in SW-31."),
    ("5", "KEPT", "Invented names in the ABIC", "Declared on the Conventions and assumptions page (p.2)."),
    ("6", "DECLARED", "$9.6m for Stage I and the whole project", "Declared on p.2. The ARBV letter should mention it."),
    ("7", "FIXED", "ABIC Schedule 3 item 6 blank", "Added 'Bills of quantities (provisional), Rider Hunt &amp; "
     "Partners, December 1958' (ABIC page 14)."),
    ("8", "OPEN", "Register tender rows: grey (suggested) names", "Only Yu-Chun Ho can confirm them."),
    ("9", "INFO", "Editing the flattened ABIC", "All ABIC fixes are placed by build_submission.py."),
]
LEAD3_V2 = [
    ("1", "DONE", "SW-12, SW-14, SW-11, SW-31 exist", "Lead 3's forms, corrected (table above)."),
    ("2", "FIXED", "SW-31 refers to SW-11", "Reference line added; B = SW-11; figures now the Stage I contract."),
    ("3", "FIXED / KEPT", "H4 / J5 timing", "H4: SW-14 02/10/1961, 14 working days after the claim. J5: SW-11 "
     "02/04/1962 kept on purpose (Lead 3's note); declared on p.2, to be explained in the ARBV letter."),
    ("4", "FIXED", "Notice of the replacement architects to the contractor",
     "New Register row and Timeline event: 20.04.1966 [A], Client to Contractor."),
    ("5", "FIXED", "1973 Practical Completion row", "Details now 'Whole building (Stage III, Hornibrook); official "
     "opening by the Queen'."),
    ("6", "FIXED", "Liquidated damages agreed with Lead 2", "See Lead 2 item 4."),
    ("7", "OPEN", "Register: (suggested) names on SW-42, SW-13, 1973 certificate, 1966 notice",
     "Only Prani Patton can confirm them."),
]


ARBV_MISSING = """<div class="box"><b>Still to add before submitting:</b> the <b>ARBV letter</b> (Part B, about 1,000 words;
page 3 is a red slot). Save it as <i>Ver.2 - revised\\inputs\\ARBV letter.pdf</i> and run <i>py build_versions.py 2</i>.</div>"""
ARBV_BOX = """<div class="box"><b>ARBV letter (Part B): draft v1 is in (pages 3-4), 1,016 words.</b> It is a new letter written
from our own file, not from the example submission. The letter the group tried was the example submission's own
ARBV letter almost word for word (Skilbeck and Howard: 'Utzon and Arup Partnership', 1 December 1964, $40,000
provisional sum, $129,000 variation): submitting it would be plagiarism, and it did not fit our project. <b>Read the
draft together, change anything you would say differently, and check the course's Use of Gen AI page before
submitting.</b> Edit <i>letters\\ARBV letter - draft v1.docx</i> in Word, save it as PDF to
<i>Ver.2 - revised\\inputs\\ARBV letter.pdf</i>, then run <i>py build_versions.py 2</i>.</div>"""
ARBV_SECTION = """<h2>5. ARBV letter: what each paragraph rests on</h2>
<table><tr><th>Para.</th><th>Claim</th><th>Evidence in the file</th><th>Code (2026; 2015 cl 5 = cl 10)</th></tr>
<tr><td>1</td><td>Terms set before work: letter 11.02.1957, CAA 21.02.1957 (8 business days later); D.8 set in advance</td><td>b letter; c CAA Schedule C; a Register</td><td>cl 6(1)-(2)</td></tr>
<tr><td>1</td><td>Registration number 'N/A' declared as a gap</td><td>c CAA page 1; p.2 assumptions</td><td>cl 6(4)(c)</td></tr>
<tr><td>2</td><td>Client told in writing of extra services (07.1961) before the work; SW-12 01.08.1961 with reason, J2.3 notice, copy to owner</td><td>a Register (D.8 row); e SW-12</td><td>cl 6(4)(g),(l); cl 9(a)-(c)</td></tr>
<tr><td>3</td><td>Claim 12.09.1961 assessed in 14 working days (H4); causes L1.1(c) and (f); time costs at Item 18</td><td>e SW-14; d ABIC Item 18</td><td>cl 10(2)(a),(b)</td></tr>
<tr><td>4</td><td>SW-11 late against J5 (02.04.1962): accepted as a failure of promptness</td><td>e SW-11; p.2 assumptions</td><td>cl 10(2)(b); ARBV guidance</td></tr>
<tr><td>5</td><td>Liquidated damages $20,000: Stage I 20 days late</td><td>a Register; d ABIC Item 24; e SW-31</td><td>cl 10(2)(a)</td></tr>
<tr><td>6</td><td>Contractor notified of the new architects 20.04.1966; SW-31 refers to SW-11; final account held too long</td><td>a Register; e SW-31</td><td>cl 9(f); cl 10(2)(c)</td></tr>
<tr><td>7</td><td>One record, one set of figures</td><td>a Register and Timeline</td><td>cl 15</td></tr></table>
<p>The 2015 Regulations named in the brief have expired: the ARBV's new Code (Architects Regulations 2026, Schedule 1) took
effect on 25 April 2026, and the contract-administration duty is now clause 10 (clause 5 in 2015). The letter cites the
2026 Code and notes the 2015 number. Ask the tutor if the 2015 numbering is required.</p>"""


def html_escape(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ver2():
    import subprocess
    prog = os.path.join(bs.A3, "programme")
    for script in ("build_scenario1_timeline.py", "build_board_layout.py", "build_register_v3.py"):
        subprocess.run([sys.executable, script], cwd=prog, check=True)
    inputs = os.path.join(VER2, "inputs")
    os.makedirs(inputs, exist_ok=True)
    form_logs, notes = {}, []
    for k, fname in FORMS_IN.items():
        f = Form(os.path.join(LEAD3, fname))
        notes += [(k, p, t, c) for p, t, c in strip_comments(f.doc)]
        FIXERS[k](f)
        f.save(os.path.join(inputs, f"{k}.pdf"))
        form_logs[k] = f.log
    bs.OUT, bs.PARTS, bs.INPUTS = VER2, os.path.join(VER2, "parts"), inputs
    os.makedirs(bs.PARTS, exist_ok=True)
    parts = {"c": bs.build_caa(), "d": bs.build_abic(), "b": bs.build_letter(), "a1": bs.build_register(),
             "a2": bs.build_timeline()}
    name, pages, arbv = compile_version(VER2, "Ver.2", parts)
    rows = [(k, html_escape(old), html_escape(new) if new else "<i>removed</i>", why)
            for k, log in form_logs.items() for old, new, why in log]
    tl = lambda items: table([(n, f"<span class='{'todo' if s == 'OPEN' else 'done'}'>{s}</span>", w, d)
                              for n, s, w, d in items], ["#", "Status", "Item", "What was done"])
    html = f"""<h1>Ver.2 — revised: fix report</h1>
<p class="sub">Built 05.11.2026 · {DUE} · File: <b>{name}</b> ({pages} pages) in <i>Ready to submit\\Ver.2 - revised</i></p>
{ARBV_BOX if arbv else ARBV_MISSING}
<div class="ok"><b>Approach.</b> Lead 3's forms keep their layout, wording and decisions; values were corrected in their own
fonts and missing items added. Kept as Lead 3 decided: SW-11 in April 1962 (J5 delay, for Part B), liquidated damages
$20,000, SW-14 within 20 working days, SW-31 by Hall, Todd &amp; Littlemore on 31/05/1975, instruction and reference
numbers, the piers description. Lead 3's 11 review comments were removed from the submission copy (listed at the end).</div>
<h2>1. Changes to Lead 3's forms</h2>
{table(rows, ["Form", "Was", "Now", "Why"])}
<h2>2. Register and Timeline, changed to match the forms</h2>
<ul><li>SW-12 01.08.1961 · SW-42 claim No. 03 12.09.1961 · SW-14 02.10.1961 · SW-11 02.04.1962 (exact dates from the forms).</li>
<li>Stage I Completed 18.03.1963 [A]: 20 days after the adjusted date; liquidated damages $20,000 (Item 24).</li>
<li>New row: 20.04.1966 Notice to contractor of replacement architects (Hall, Todd &amp; Littlemore).</li>
<li>Practical Completion Certificate 20.10.1973: 'Whole building (Stage III, Hornibrook)'. Final Certificate: Stage I,
refers to SW-11, less $20,000 liquidated damages, $20,000 due to the owner.</li>
<li>Conventions and assumptions page (p.2): variation chain dates, completion and liquidated damages, final certificate
basis. The date check between Register and Timeline passes.</li></ul>
<h2>3. Lead 2 checklist (Yu-Chun Ho)</h2>{tl(LEAD2_V2)}
<h2>4. Lead 3 checklist (Prani Patton)</h2>{tl(LEAD3_V2)}
{ARBV_SECTION if arbv else ""}
<h2>{6 if arbv else 5}. Still for the group</h2><ul><li>{"Read the ARBV letter together and make it your own (above)." if arbv else "Write the ARBV letter (above)."}</li>
<li>Confirm the grey (suggested) names in the Register (Student Contribution): each person confirms their own.</li>
<li>Ask the tutor whether one person submits for the group.</li></ul>
<h2>Lead 3's review comments (removed from the submission copy)</h2>
{table([(k, p, t, c) for k, p, t, c in notes], ["Form", "Page", "Type", "Comment"])}"""
    html_pdf(html, os.path.join(VER2, "Ver.2 - Fix report (not for submission).pdf"))


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "1"
    if which == "1":
        ver1()
    else:
        ver2()
