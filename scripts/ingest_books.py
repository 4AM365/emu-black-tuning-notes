"""
Book ingestion pipeline → RAG-ready markdown corpus.

Each book is extracted into corpus/<slug>.md with:
  - H1  = book title + author
  - H2  = chapter headings (detected heuristically)
  - H3  = sub-section headings
  - <!-- page N --> markers for provenance
  - Markdown tables where pdfplumber detects table geometry
  - Minimal whitespace cleanup without destroying paragraph breaks

Run:  python ingest_books.py
"""

import re
import os
import textwrap
from pathlib import Path

import pdfplumber
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

BOOKS_DIR = Path("books")
CORPUS_DIR = Path("corpus")
CORPUS_DIR.mkdir(exist_ok=True)

# ── helpers ────────────────────────────────────────────────────────────────────

def clean_line(line: str) -> str:
    """Strip PDF extraction artefacts while preserving meaningful spaces."""
    # remove soft-hyphen line joins that span pages
    line = line.replace("­", "")
    # collapse runs of spaces > 3 into two (keeps column-like spacing readable)
    line = re.sub(r" {4,}", "   ", line)
    return line.rstrip()


def looks_like_heading(line: str, prev_blank: bool) -> tuple[bool, int]:
    """
    Heuristic: short ALL-CAPS or Title-Case lines that follow a blank line
    are probably headings.  Returns (is_heading, level).
    """
    stripped = line.strip()
    if not stripped or len(stripped) > 120:
        return False, 0
    if not prev_blank:
        return False, 0

    # Chapter-level patterns
    chapter_pat = re.match(
        r"^(CHAPTER|Chapter|PART|Part|SECTION|Section)\s+[\dIVXivx]+[:\s]", stripped
    )
    if chapter_pat:
        return True, 2

    # Numbered section  "3.4  Volumetric Efficiency"
    numbered = re.match(r"^\d+[\.\d]*\s{2,}[A-Z]", stripped)
    if numbered:
        return True, 3

    # Short ALL-CAPS line (e.g. "IGNITION TIMING")
    if stripped.isupper() and 4 < len(stripped) < 80:
        return True, 2

    # Title Case short line (≤ 8 words, no terminal punctuation)
    words = stripped.split()
    if (
        3 <= len(words) <= 8
        and not stripped[-1] in ".,:;?!"
        and sum(1 for w in words if w[0].isupper()) >= len(words) * 0.7
    ):
        return True, 3

    return False, 0


def table_to_markdown(table: list[list]) -> str:
    """Convert pdfplumber table (list of rows) to a markdown table string."""
    if not table or not table[0]:
        return ""
    # normalize cells
    rows = [[str(cell).strip() if cell else "" for cell in row] for row in table]
    col_count = max(len(r) for r in rows)
    # pad rows to same width
    rows = [r + [""] * (col_count - len(r)) for r in rows]

    header = rows[0]
    body = rows[1:]

    def fmt_row(r):
        return "| " + " | ".join(r) + " |"

    sep = "| " + " | ".join(["---"] * col_count) + " |"
    lines = [fmt_row(header), sep] + [fmt_row(r) for r in body]
    return "\n".join(lines)


# ── PDF extractor ──────────────────────────────────────────────────────────────

def extract_pdf(pdf_path: Path, title: str, author: str) -> str:
    """Extract a PDF to structured markdown."""
    blocks = [f"# {title}\n\n**Author:** {author}  \n**Source:** {pdf_path.name}\n"]

    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        print(f"  {pdf_path.name}: {total} pages")

        prev_blank = True  # treat start-of-doc as after a blank line

        for page_num, page in enumerate(pdf.pages, start=1):
            blocks.append(f"\n<!-- page {page_num} -->\n")

            # ── tables first (extract by geometry, then mask their bbox) ──────
            tables = page.extract_tables()
            table_bboxes = []
            table_blocks = []
            for table in tables:
                md = table_to_markdown(table)
                if md:
                    table_blocks.append(md)
                # pdfplumber can give us bbox via find_tables()
            found_tables = page.find_tables()
            for ft, md in zip(found_tables, table_blocks):
                table_bboxes.append(ft.bbox)
                blocks.append("\n" + md + "\n")

            # ── text (crop away table regions to avoid duplication) ───────────
            crop = page
            for bbox in table_bboxes:
                try:
                    crop = crop.outside_bbox(bbox)
                except Exception:
                    pass

            raw_text = crop.extract_text(x_tolerance=3, y_tolerance=3) or ""

            for raw_line in raw_text.splitlines():
                line = clean_line(raw_line)

                is_heading, level = looks_like_heading(line, prev_blank)
                if is_heading:
                    prefix = "#" * level
                    blocks.append(f"\n{prefix} {line.strip()}\n")
                    prev_blank = False
                    continue

                if line == "":
                    if not prev_blank:
                        blocks.append("")
                    prev_blank = True
                else:
                    blocks.append(line)
                    prev_blank = False

    return "\n".join(blocks)


# ── EPUB extractor ─────────────────────────────────────────────────────────────

def extract_epub(epub_path: Path, title: str, author: str) -> str:
    """Extract an epub to structured markdown via HTML → text pipeline."""
    blocks = [f"# {title}\n\n**Author:** {author}  \n**Source:** {epub_path.name}\n"]

    book = epub.read_epub(str(epub_path))

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")

        # remove nav / footnote elements
        for tag in soup.select("nav, .footnote, .endnote, [epub\\:type='footnote']"):
            tag.decompose()

        for elem in soup.body.descendants if soup.body else []:
            if not hasattr(elem, "name"):
                continue  # NavigableString handled via parent

        # walk block elements in document order
        for elem in soup.find_all(
            ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "table", "blockquote"]
        ):
            tag = elem.name
            text = elem.get_text(" ", strip=True)

            if not text:
                continue

            if tag == "h1":
                blocks.append(f"\n## {text}\n")
            elif tag == "h2":
                blocks.append(f"\n### {text}\n")
            elif tag in ("h3", "h4", "h5", "h6"):
                blocks.append(f"\n#### {text}\n")
            elif tag == "table":
                # convert html table rows to markdown
                rows = []
                for tr in elem.find_all("tr"):
                    cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
                    rows.append(cells)
                md = table_to_markdown(rows)
                if md:
                    blocks.append("\n" + md + "\n")
            elif tag == "li":
                blocks.append(f"- {text}")
            elif tag == "blockquote":
                for bline in text.splitlines():
                    blocks.append(f"> {bline}")
            else:  # p
                # wrap long paragraphs at 100 chars for readability
                wrapped = textwrap.fill(text, width=100)
                blocks.append(wrapped)
                blocks.append("")

    return "\n".join(blocks)


# ── book manifest ──────────────────────────────────────────────────────────────

BOOKS = [
    {
        "file": "how to tune.pdf",
        "slug": "how_to_tune",
        "title": "How to Tune and Modify Engine Management Systems",
        "author": "Jeff Hartman",
        "type": "pdf",
    },
    {
        "file": "maximum boost.pdf",
        "slug": "maximum_boost",
        "title": "Maximum Boost: Designing, Testing, and Installing Turbocharger Systems",
        "author": "Corky Bell",
        "type": "pdf",
    },
    {
        "file": "four stroke performance.pdf",
        "slug": "four_stroke_performance",
        "title": "Four-Stroke Performance Tuning",
        "author": "A. Graham Bell",
        "type": "pdf",
    },
    {
        "file": "ice fundamentals.pdf",
        "slug": "ice_fundamentals",
        "title": "Internal Combustion Engine Fundamentals",
        "author": "John B. Heywood",
        "type": "pdf",
    },
    {
        "file": "engine mgmt.epub",
        "slug": "engine_management_advanced_tuning",
        "title": "Engine Management: Advanced Tuning",
        "author": "Greg Banish",
        "type": "epub",
    },
]


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    results = []
    for book in BOOKS:
        path = BOOKS_DIR / book["file"]
        out  = CORPUS_DIR / f"{book['slug']}.md"

        if not path.exists():
            print(f"  SKIP (not found): {path}")
            continue

        print(f"\n>> {book['title']}")

        try:
            if book["type"] == "pdf":
                md = extract_pdf(path, book["title"], book["author"])
            else:
                md = extract_epub(path, book["title"], book["author"])

            out.write_text(md, encoding="utf-8")
            size_kb = out.stat().st_size // 1024
            lines   = md.count("\n")
            print(f"  OK  {out.name}  ({size_kb} KB, {lines:,} lines)")
            results.append((book["slug"], size_kb, lines))

        except Exception as e:
            print(f"  ERR  {book['file']}: {e}")
            import traceback; traceback.print_exc()

    print("\n── Corpus summary ────────────────────────────")
    for slug, kb, lines in results:
        print(f"  {slug:<45} {kb:>6} KB  {lines:>8,} lines")
    print(f"\n  Output dir: {CORPUS_DIR.resolve()}")


if __name__ == "__main__":
    main()
