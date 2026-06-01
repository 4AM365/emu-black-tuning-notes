"""
Stage 2: Convert raw OCR text files into RAG-ready markdown notes.
Reads _raw_ocr/page_NNN.txt, detects chapter boundaries from running headers,
cleans text, and writes one markdown file per chapter.

Run AFTER ocr_extract.py finishes.
"""

import os
import re
from pathlib import Path
from datetime import date

RAW_DIR = Path(__file__).parent / '_raw_ocr'
OUT_DIR = Path(__file__).parent

# ── Chapter topic hints (for frontmatter enrichment) ──────────────────────────

CHAPTER_TOPICS_HINTS = {
    1:  ["turbocharger", "power calculation", "volumetric efficiency", "thermodynamics",
         "pressure ratio", "inertial load", "detonation", "thermal management"],
    2:  ["OEM turbo", "aftermarket kit", "system evaluation", "boost pressure", "air/fuel ratio"],
    3:  ["compressor", "compressor map", "surge line", "choke", "pressure ratio",
         "mass flow", "efficiency island", "compressor selection"],
    4:  ["turbine", "turbine housing", "A/R ratio", "backpressure", "turbine wheel",
         "exhaust energy", "turbine selection"],
    5:  ["intercooler", "charge cooling", "heat exchanger", "pressure drop",
         "air-to-air", "air-to-water", "intake temperature", "intercooler sizing"],
    6:  ["lubrication", "oil supply", "oil drain", "bearing", "turbo oil pressure",
         "oil return", "drain back", "oil feed line"],
    7:  ["fuel", "fuel injector", "EFI", "carburetor", "ignition timing",
         "detonation", "knock", "fuel enrichment", "fuel map", "stoichiometric"],
    8:  ["exhaust manifold", "exhaust backpressure", "downpipe", "collector",
         "merge", "header design", "turbine inlet"],
    9:  ["boost control", "wastegate", "boost solenoid", "boost creep", "overboost",
         "internal wastegate", "external wastegate", "boost target", "boost controller"],
    10: ["installation", "plumbing", "intercooler piping", "blow-off valve",
         "recirculation", "bypass valve", "mounting"],
    11: ["tuning", "dyno", "boost curve", "AFR", "air fuel ratio",
         "ignition advance", "base map", "data logging"],
    12: ["troubleshooting", "surging", "compressor surge", "oil leak",
         "bearing failure", "boost leak", "detonation diagnosis"],
    13: ["diesel", "marine", "aircraft", "high altitude", "special applications",
         "twin turbo", "sequential turbo"],
    14: ["testing", "system test", "pressure measurement", "temperature measurement",
         "boost gauge", "EGT", "data acquisition"],
}

# ── Running-header patterns ────────────────────────────────────────────────────

# Left-page running header: "page_num CHAPTER N: TITLE" (colon sometimes OCR'd as L or I)
# Handles: "2 CHAPTER 1: TITLE", "6 CHAPTER 1L: TITLE", "26 CHAPTER 2: TITLE"
HEADER_LEFT_RE = re.compile(
    r'^\s*\d+\s+CHAPTER\s+(\d+)\w*\s*[:.]\s*(.+)',
    re.IGNORECASE
)
# Also catch bare "CHAPTER N:" anywhere on a page (chapter opener pages)
CHAPTER_ANY_RE = re.compile(
    r'\bCHAPTER\s+(\d+)[LI]?\b',
    re.IGNORECASE
)


def detect_chapter_and_title(text: str) -> tuple[int | None, str | None]:
    """
    Return (chapter_num, chapter_title) if this page contains a running header
    that identifies a chapter, else (None, None).
    Priority: left-page header (most reliable) > any CHAPTER N mention.
    """
    for line in text.splitlines()[:6]:  # headers are always near the top
        m = HEADER_LEFT_RE.match(line)
        if m:
            n = int(m.group(1))
            title = m.group(2).strip().title()
            if 1 <= n <= 20:
                return n, title

    # Fallback: any CHAPTER N mention in first few lines
    for line in text.splitlines()[:4]:
        m = CHAPTER_ANY_RE.search(line)
        if m:
            n = int(m.group(1))
            if 1 <= n <= 20:
                return n, None

    return None, None


# ── Text cleaning ──────────────────────────────────────────────────────────────

# Lines that are running headers (already captured for metadata)
HEADER_STRIP_RE = re.compile(
    r'^\s*\d+\s+CHAPTER\s+\d+[LI:]?.{0,60}$|'
    r'^[A-Z\s&\-/:,]{4,60}\s+\d+\s*$',  # right-page header: TITLE page_num
    re.IGNORECASE
)


def clean_ocr(text: str) -> str:
    lines = text.splitlines()
    cleaned = []
    for idx, line in enumerate(lines):
        line = line.rstrip()

        # Strip running headers — only reliable in first 3 lines of a page
        if idx < 3 and HEADER_STRIP_RE.match(line):
            continue

        # Drop lone page numbers
        if re.fullmatch(r'\s*\d{1,3}\s*', line):
            continue

        # Drop lines that are overwhelmingly non-alphanumeric (scan noise)
        stripped = line.strip()
        if len(stripped) > 4:
            alnum = sum(c.isalnum() or c == ' ' for c in stripped)
            if alnum / len(stripped) < 0.40:
                continue

        # Fix common Tesseract errors in technical text
        line = re.sub(r'(?<=\d)L(?=\s)', ':', line)   # "1L " → "1: "
        line = re.sub(r'\bI\.e\b', 'i.e.', line)
        line = re.sub(r'\be\.g\b', 'e.g.', line)

        # Rejoin hyphenated line-breaks
        if cleaned and cleaned[-1].endswith('-'):
            cleaned[-1] = cleaned[-1][:-1] + stripped
            continue

        cleaned.append(line)

    result = re.sub(r'\n{3,}', '\n\n', '\n'.join(cleaned))
    return result.strip()


# ── Section heading detection ──────────────────────────────────────────────────

# Section headings appear as short ALL-CAPS or Title-Case lines preceded by blank line
SECTION_HEADING_RE = re.compile(
    r'\n\n([A-Z][A-Z\s\-/:,\']{4,55})\n\n',
)

# "RULE:" boxes — preserve them
RULE_RE = re.compile(r'(?:©\s*)?RULE[:\.](.+?)(?=\n\n|\Z)', re.DOTALL)


def format_body(text: str) -> str:
    """Convert plain cleaned text into markdown with ## section headers."""
    # Highlight rule boxes
    def rule_repl(m):
        return f"\n> **RULE:** {m.group(1).strip()}\n"
    text = RULE_RE.sub(rule_repl, text)

    # Convert ALL-CAPS section headings to ## headers
    def heading_repl(m):
        heading = m.group(1).strip().title()
        return f"\n\n## {heading}\n\n"
    text = SECTION_HEADING_RE.sub(heading_repl, text)

    # Italicize figure captions
    lines = []
    for line in text.splitlines():
        if re.match(r'\s*Fig\.', line):
            lines.append(f"*{line.strip()}*")
        else:
            lines.append(line)
    return '\n'.join(lines)


# ── Markdown file writer ───────────────────────────────────────────────────────

def write_chapter_md(
    chapter_num: int,
    chapter_title: str,
    pages_text: list[tuple[int, str]],
) -> Path:
    slug_title = re.sub(r'[^a-z0-9]+', '-', chapter_title.lower()).strip('-')[:40]
    slug = f"chapter-{chapter_num:02d}-{slug_title}"

    topics = CHAPTER_TOPICS_HINTS.get(chapter_num, [])
    page_nums = [p for p, _ in pages_text]
    page_range = f"{min(page_nums)}–{max(page_nums)}" if page_nums else "?"

    full_text = '\n\n'.join(clean_ocr(t) for _, t in pages_text)
    body = format_body(full_text)

    out_path = OUT_DIR / f"{slug}.md"

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write(f'title: "Chapter {chapter_num}: {chapter_title}"\n')
        f.write(f'source: "Maximum Boost by Corky Bell (1997)"\n')
        f.write(f'chapter: {chapter_num}\n')
        f.write(f'pages: "{page_range}"\n')
        topics_yaml = "[" + ", ".join(f'"{t}"' for t in topics) + "]"
        f.write(f'topics: {topics_yaml}\n')
        f.write(f'generated: "{date.today()}"\n')
        f.write("---\n\n")
        f.write(f"# Chapter {chapter_num}: {chapter_title}\n\n")
        f.write(f"> *Maximum Boost* — Corky Bell (1997) | pages {page_range}\n\n")
        f.write(body)
        f.write("\n")

    print(f"  OK {out_path.name}  ({len(full_text):,} chars, pages {page_range})")
    return out_path


def write_index(chapters: dict[int, tuple[str, Path]]) -> None:
    idx = OUT_DIR / "index.md"
    with open(idx, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write('title: "Maximum Boost - Knowledge Index"\n')
        f.write('source: "Maximum Boost by Corky Bell (1997)"\n')
        f.write(f'generated: "{date.today()}"\n')
        f.write("---\n\n")
        f.write("# Maximum Boost - Turbocharger RAG Knowledge Index\n\n")
        f.write(
            "Reference guide for turbocharger system design, component selection, "
            "installation, and tuning. Source: *Maximum Boost* by Corky Bell, 1997.\n\n"
        )
        f.write("## Chapters\n\n")
        for n in sorted(chapters):
            title, path = chapters[n]
            topics_str = ", ".join(CHAPTER_TOPICS_HINTS.get(n, [])[:4])
            f.write(f"- **[{path.name}]({path.name})** -- Ch.{n}: {title}  \n")
            f.write(f"  *{topics_str}*\n")
        f.write("\n## Quick-Look Topic Index\n\n")
        f.write("| Topic | Chapter(s) |\n|---|---|\n")
        all_topics: dict[str, list[int]] = {}
        for n, topics in CHAPTER_TOPICS_HINTS.items():
            for t in topics:
                all_topics.setdefault(t, []).append(n)
        for topic in sorted(all_topics):
            chaps = ", ".join(str(c) for c in sorted(all_topics[topic]))
            f.write(f"| {topic} | {chaps} |\n")
    print(f"  OK {idx.name}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    raw_files = sorted(RAW_DIR.glob('page_*.txt'))
    if not raw_files:
        print("No raw OCR files found in _raw_ocr/. Run ocr_extract.py first.")
        return

    print(f"Building notes from {len(raw_files)} pages in {RAW_DIR}...")

    # Scan pages and assign to chapters
    chapter_pages: dict[int, list[tuple[int, str]]] = {}
    chapter_titles: dict[int, str] = {}
    current_chapter = 0

    for f in raw_files:
        m = re.search(r'page_(\d+)', f.stem)
        page_num = int(m.group(1)) if m else 0
        text = f.read_text(encoding='utf-8')

        detected_num, detected_title = detect_chapter_and_title(text)

        if detected_num is not None:
            if detected_num != current_chapter:
                current_chapter = detected_num
                print(f"    Chapter {current_chapter} starts at page {page_num}")
            if detected_title and current_chapter not in chapter_titles:
                chapter_titles[current_chapter] = detected_title

        if current_chapter > 0:
            chapter_pages.setdefault(current_chapter, []).append((page_num, text))

    # Finalize titles (use detected or fallback)
    written: dict[int, tuple[str, Path]] = {}
    for n in sorted(chapter_pages):
        title = chapter_titles.get(n, f"Chapter {n}")
        path = write_chapter_md(n, title, chapter_pages[n])
        written[n] = (title, path)

    write_index(written)
    total_chars = sum(
        sum(len(t) for _, t in pages)
        for pages in chapter_pages.values()
    )
    print(f"\nDone. {len(written)} chapter files, {total_chars:,} total chars -> {OUT_DIR}")


if __name__ == '__main__':
    main()
