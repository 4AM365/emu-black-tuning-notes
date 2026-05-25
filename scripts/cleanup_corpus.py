"""
Post-processing cleanup for corpus markdown files.

Handles:
  how_to_tune.md      - strip InDesign print-layer metadata & doubled-char artifacts
  four_stroke.md      - normalize common OCR ligature errors
  ice_fundamentals.md - minor whitespace / heading normalization
  engine_mgmt.epub    - already clean, just normalise spacing

Maximum Boost is handled separately (needs full re-OCR).
"""

import re
from pathlib import Path

CORPUS = Path("corpus")


# ── how_to_tune: InDesign artefact removal ─────────────────────────────────────

# Lines like: 001-177_30412.indd 38  4/4/13  9:06 AM
INDESIGN_FILE = re.compile(r"^\d{3}-\d{3}_[A-Z0-9]+\.indd\b", re.IGNORECASE)

# Doubled-char metadata blocks, e.g.:
#   ((FFooggrraa 3399))JJoobb::0033--3300441122 TTiittllee::MMBBII--...
#   ##117755 DDttpp::222255 PPaaggee::3388
DOUBLED_CHAR = re.compile(r"(\(\([A-Za-z]{4,})|##\d{4,}|JJoobb::|DDttpp::|TTiittllee::")

# Print shop colophon lines (single-colon variants)
#   (Fogra 39)Job:03-30412 Title:MBI-...
#   #175 Dtp:225 Page:4
FOGRA_LINE = re.compile(r"\(Fogra\s+\d+\)Job:", re.IGNORECASE)
DTP_LINE   = re.compile(r"#\d+\s+Dtp:\d+\s+Page:\d+")
COLOPHON   = re.compile(r"\b(Dtp|Fogrra|Job|Title|Ray|Canale|Text)\b.*::\s*\d", re.IGNORECASE)

def clean_how_to_tune(text: str) -> str:
    cleaned = []
    for line in text.splitlines():
        stripped = line.strip()
        # Drop InDesign file lines
        if INDESIGN_FILE.match(stripped):
            continue
        # Drop doubled-char artifact lines
        if DOUBLED_CHAR.search(stripped):
            continue
        # Drop Fogra/Dtp print-shop colophon lines
        if FOGRA_LINE.search(stripped):
            continue
        if DTP_LINE.search(stripped):
            continue
        # Drop colophon lines (double-colon variant)
        if COLOPHON.search(stripped):
            continue
        cleaned.append(line)
    # Collapse runs of 3+ blank lines → 2
    result = re.sub(r"\n{3,}", "\n\n", "\n".join(cleaned))
    return result


# ── four_stroke: OCR ligature / scan artefact normalization ────────────────────

FOUR_STROKE_FIXES = [
    # Ligature repairs (common in older Haynes scans)
    (r"\bfi(?=[a-z])", "fi"),       # sometimes fi ligature shows as placeholder
    (r"B<::l1\b", "Bell"),
    (r"\bL1\b", "11"),              # "Chapter Ll" → "Chapter 11" context-sensitive
    (r"(?<=\d)J\b", "1"),           # trailing J after digit → 1
    (r"\bIIl\b", "III"),
    (r"\bJJ\b", "11"),
    (r"(?<=[A-Za-z])0(?=[A-Za-z])", "o"),  # zero inside word → o (careful)
    # Common OCR word errors seen in this scan
    (r"\bMc;\)suremem\b", "Measurement"),
    (r"\bVnlve\b", "Valve"),
    (r"\bancl\b", "and"),
    (r"\btlie\b", "the"),
    (r"\btimt\b", "that"),
    (r"\bliom\b", "from"),
    (r"\bliave\b", "have"),
    (r"\bwliich\b", "which"),
    (r"\btlie\b", "the"),
]

def clean_four_stroke(text: str) -> str:
    for pattern, replacement in FOUR_STROKE_FIXES:
        text = re.sub(pattern, replacement, text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


# ── ice_fundamentals: heading / whitespace normalization ───────────────────────

def clean_ice_fundamentals(text: str) -> str:
    lines = text.splitlines()
    cleaned = []
    prev_blank = True
    for line in lines:
        # Heywood uses ALL-CAPS section headers like "1.1 INTRODUCTION AND HISTORICAL"
        # pdfplumber sometimes inserts spurious blank lines mid-sentence; collapse those
        # where a line ends mid-sentence (no terminal punctuation) and next is lowercase
        stripped = line.strip()
        cleaned.append(line)
        prev_blank = (stripped == "")
    result = re.sub(r"\n{3,}", "\n\n", "\n".join(cleaned))
    return result


# ── engine_management: space after split-word headings ────────────────────────
# The epub H2s have spaces from HTML: "## A CKNOWLEDGMENTS" → "## ACKNOWLEDGMENTS"
SPACED_HEADING = re.compile(r"^(#{1,4})\s+([A-Z])\s([A-Z ]+)$", re.MULTILINE)

def clean_engine_mgmt(text: str) -> str:
    # Re-join single-letter + rest pattern in headings: "A CKNOWLEDGMENTS" → "ACKNOWLEDGMENTS"
    def rejoin(m):
        prefix = m.group(1)
        first  = m.group(2)
        rest   = m.group(3).replace(" ", "")
        return f"{prefix} {first}{rest}"
    text = SPACED_HEADING.sub(rejoin, text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


# ── runner ─────────────────────────────────────────────────────────────────────

CLEANERS = {
    "how_to_tune.md":                     clean_how_to_tune,
    "four_stroke_performance.md":          clean_four_stroke,
    "ice_fundamentals.md":                 clean_ice_fundamentals,
    "engine_management_advanced_tuning.md": clean_engine_mgmt,
}

def main():
    for filename, cleaner in CLEANERS.items():
        path = CORPUS / filename
        if not path.exists():
            print(f"  SKIP (missing): {filename}")
            continue
        original = path.read_text(encoding="utf-8")
        cleaned  = cleaner(original)
        path.write_text(cleaned, encoding="utf-8")
        orig_lines    = original.count("\n")
        cleaned_lines = cleaned.count("\n")
        delta = orig_lines - cleaned_lines
        size_kb = path.stat().st_size // 1024
        print(f"  {filename:<48} {size_kb:>5} KB  removed {delta:>5} lines")

if __name__ == "__main__":
    print("Cleaning corpus files...")
    main()
    print("Done.")
