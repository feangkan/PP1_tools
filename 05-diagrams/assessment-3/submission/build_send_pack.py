"""Assessment 3: the two files to send to the group (run after build_submission.py and build_checklist.py).

Writes  D:\\RMIT_SEM2 26_PROPRAC 1\\Week 12\\Ready to submit\\To send to group\\
    1. Report - fixes and suggestions by lead.pdf
    2. Draft pre-submission - NOT READY TO SUBMIT.pdf   (the compiled draft, every page stamped)
"""
import glob, os, shutil
import pymupdf

READY = r"D:\RMIT_SEM2 26_PROPRAC 1\Week 12\Ready to submit"
SEND = os.path.join(READY, "To send to group")
STAMP = "DRAFT FOR GROUP REVIEW (04.11.2026)  \u2014  NOT READY TO SUBMIT  \u2014  see the fix report, 1. Report"
ARIAL = r"C:\Windows\Fonts\arialbd.ttf"


def main():
    os.makedirs(SEND, exist_ok=True)
    shutil.copy(os.path.join(READY, "Checklist - fixes by lead.pdf"),
                os.path.join(SEND, "1. Report - fixes and suggestions by lead.pdf"))
    src = [f for f in glob.glob(os.path.join(READY, "Assessment Task 3_*.pdf"))]
    assert len(src) == 1, src
    doc = pymupdf.open(src[0])
    for page in doc:
        w = page.rect.width
        size = 7 * w / 595
        page.insert_font(fontname="arialbd", fontfile=ARIAL)
        tl = pymupdf.Font(fontfile=ARIAL).text_length(STAMP, fontsize=size)
        x = (w - tl) / 2
        page.draw_rect(pymupdf.Rect(x - 6, 3 * w / 595, x + tl + 6, 14 * w / 595),
                       color=(0.8, 0, 0), fill=(1, 1, 1), width=0.6)
        page.insert_text((x, 11 * w / 595), STAMP, fontname="arialbd", fontsize=size, color=(0.8, 0, 0))
    out = os.path.join(SEND, "2. Draft pre-submission - NOT READY TO SUBMIT.pdf")
    doc.save(out, garbage=3, deflate=True)
    print("wrote", SEND, f"(draft {doc.page_count} pages)")


if __name__ == "__main__":
    main()
