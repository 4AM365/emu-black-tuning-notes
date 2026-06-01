"""
Stage 1: OCR all pages of Maximum Boost at 200 DPI using Tesseract.
Saves raw text per page to _raw_ocr/page_NNN.txt.
Skips pages already done (resumable).
"""

import fitz
import pytesseract
from PIL import Image
import io
import os
import sys
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

PDF_PATH = r'C:\Users\WTCra\OneDrive\Reference Library\maximum_boost-corky_bell.pdf'
RAW_DIR = os.path.join(os.path.dirname(__file__), '_raw_ocr')
DPI = 200

os.makedirs(RAW_DIR, exist_ok=True)

doc = fitz.open(PDF_PATH)
total = len(doc)
mat = fitz.Matrix(DPI / 72, DPI / 72)

print(f"OCR: {total} pages at {DPI} DPI -> {RAW_DIR}", flush=True)
start = time.time()

for i in range(total):
    out = os.path.join(RAW_DIR, f'page_{i+1:03d}.txt')
    if os.path.exists(out):
        if i % 20 == 0:
            print(f"  [{i+1}/{total}] cached", flush=True)
        continue

    page = doc[i]
    pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
    img = Image.open(io.BytesIO(pix.tobytes("png")))

    # PSM 3 = fully automatic page segmentation (default, no OSD)
    text = pytesseract.image_to_string(img, lang='eng', config='--psm 3 --oem 3')

    with open(out, 'w', encoding='utf-8') as f:
        f.write(text)

    elapsed = time.time() - start
    rate = (i + 1) / elapsed
    eta = (total - i - 1) / rate if rate > 0 else 0
    print(f"  [{i+1}/{total}] {len(text):4d} chars  ETA {eta/60:.1f}min", flush=True)

doc.close()
print(f"Done in {(time.time()-start)/60:.1f} min", flush=True)
