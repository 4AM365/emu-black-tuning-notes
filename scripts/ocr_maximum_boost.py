"""
Full OCR re-extraction for Maximum Boost (Corky Bell).

The PDF is a scanned book — pdfplumber produces garbage text.
Uses PyMuPDF to render each page at 300dpi then Tesseract for OCR.
No poppler dependency.

Runtime: ~10-20 min for 247 pages.
Usage:   python scripts/ocr_maximum_boost.py
"""

import io
import re
import sys
from pathlib import Path

import fitz          # PyMuPDF
import pytesseract
from PIL import Image

# ── config ─────────────────────────────────────────────────────────────────────
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

PDF_PATH = Path("books/maximum boost.pdf")
OUT_PATH = Path("corpus/maximum_boost.md")
DPI      = 300
LANG     = "eng"
TSV_CONFIG = "--oem 1 --psm 3"

TITLE  = "Maximum Boost: Designing, Testing, and Installing Turbocharger Systems"
AUTHOR = "Corky Bell"

# ── heading heuristics ─────────────────────────────────────────────────────────

def looks_like_heading(line: str, prev_blank: bool) -> tuple[bool, int]:
    stripped = line.strip()
    if not stripped or len(stripped) > 120:
        return False, 0
    if not prev_blank:
        return False, 0
    if re.match(r"^(CHAPTER|Chapter|PART|Part|SECTION|Section)\s+[\dIVXivx]+[:\s]", stripped):
        return True, 2
    if re.match(r"^\d+[\.\d]*\s{2,}[A-Z]", stripped):
        return True, 3
    if stripped.isupper() and 4 < len(stripped) < 80:
        return True, 2
    words = stripped.split()
    if (
        3 <= len(words) <= 8
        and not stripped[-1] in ".,:;?!"
        and sum(1 for w in words if w[0].isupper()) >= len(words) * 0.7
    ):
        return True, 3
    return False, 0


def clean_line(line: str) -> str:
    return re.sub(r" {4,}", "   ", line).rstrip()


# ── page renderer ──────────────────────────────────────────────────────────────

SCALE = DPI / 72.0   # 72 = PDF native DPI

def render_page(page: fitz.Page) -> Image.Image:
    mat = fitz.Matrix(SCALE, SCALE)
    pix = page.get_pixmap(matrix=mat)
    return Image.open(io.BytesIO(pix.tobytes("png")))


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    if not PDF_PATH.exists():
        print(f"PDF not found: {PDF_PATH}")
        sys.exit(1)

    doc = fitz.open(str(PDF_PATH))
    total = len(doc)
    print(f"OCR: {PDF_PATH.name}  ({total} pages at {DPI} dpi)")
    print(f"Output: {OUT_PATH}")

    blocks = [f"# {TITLE}\n\n**Author:** {AUTHOR}  \n**Source:** {PDF_PATH.name}\n"]

    for page_num_0, page in enumerate(doc):
        page_num = page_num_0 + 1
        blocks.append(f"\n<!-- page {page_num} -->\n")

        img      = render_page(page)
        raw_text = pytesseract.image_to_string(img, lang=LANG, config=TSV_CONFIG)

        prev_blank = True
        for raw_line in raw_text.splitlines():
            line = clean_line(raw_line)
            is_heading, level = looks_like_heading(line, prev_blank)
            if is_heading:
                blocks.append(f"\n{'#' * level} {line.strip()}\n")
                prev_blank = False
                continue
            if line == "":
                if not prev_blank:
                    blocks.append("")
                prev_blank = True
            else:
                blocks.append(line)
                prev_blank = False

        if page_num % 10 == 0:
            print(f"  ... page {page_num}/{total}", flush=True)

    doc.close()

    md_text = "\n".join(blocks)
    md_text = re.sub(r"\n{3,}", "\n\n", md_text)

    OUT_PATH.write_text(md_text, encoding="utf-8")
    size_kb = OUT_PATH.stat().st_size // 1024
    lines   = md_text.count("\n")
    print(f"\nDone: {OUT_PATH.name}  ({size_kb} KB, {lines:,} lines)")


if __name__ == "__main__":
    main()
