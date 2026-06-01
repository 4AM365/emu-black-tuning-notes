---
name: emu-black-ve-smooth
description: >-
  Smooths an EMU Black VE / fuel-dose table (veTable, veTable2) while pinning
  trusted autotune cells in place. Use this whenever the user wants to "smooth
  my VE map", "clean up the autotune table", "remove the steps in my fuel map",
  "fit a smooth surface through the corrected cells", or has a patchy VE table
  where only some cells were corrected by a log-based autotune and the rest are
  ragged. Performs an anchor-weighted polynomial smooth: trusted cells keep their
  exact value, untouched neighbours are pulled onto a low-order curve, and cells
  far from any data are left alone. Pairs with emu-black-tune (decode/encode the
  table) and emu-black-emubt-export (write the result back as .emubt).
---

# EMU Black VE table smoother

A log-based autotune (STFT-driven VE correction) typically only touches the cells
the car actually visited, leaving the VE / fuel-dose table with sharp steps
between corrected and uncorrected cells. This skill smooths those steps **without
disturbing the cells you trust** — the corrected ("anchor") cells keep their exact
value and everything else is fit onto a low-order polynomial surface bounded to the
region around the anchors.

For decoding/encoding the table itself use **emu-black-tune**; to write the
smoothed result back as an importable file use **emu-black-emubt-export**. On this
build the EMU "VE" table is a **fuel-dose proxy, not pure air VE** — see the build
notes — so smoothing operates on the dose values as displayed, no unit conversion.

## Method (`scripts/smooth_ve.py`)

The smoother is a NumPy module. Core call:

```python
from smooth_ve import smooth_table, print_table, print_delta, write_csv
import numpy as np

smoothed = smooth_table(
    original,          # (n_rpm, n_load) float array, ROW 0 = HIGHEST RPM
    anchors,           # {(row, col), ...} cells that must keep their exact value
    degree=3,          # polynomial degree (3 default; 4 for a tighter fit)
    n_passes=3,        # column+row sweep iterations
    extend=0,          # cells beyond the anchor span allowed to move
    anchor_w=100.0,    # weight of anchor vs non-anchor cells in the fit
)
```

What it does, per pass, for every column (RPM axis) then every row (load axis):

1. Find the anchor span `[lo, hi]` on that line; extend it by `extend` cells each side.
2. Weighted `polyfit` of degree `degree` over that segment — anchors weight 100,
   others weight 1 — then replace **only the non-anchor cells** with the curve.
3. Re-snap every anchor back to its exact original value.

Cells outside the extended anchor zone are never moved, which prevents wild
polynomial extrapolation into regions the autotune never saw. Output is rounded to
0.1.

In plain terms: *reduce the step size between adjacent cells, fit a 3rd-order line
through the trusted cells, and pull the in-between cells onto that line within a
couple percent.*

## Workflow

1. **Decode** the current `veTable` (and `veTable2` if flex) with emu-black-tune —
   get a 2D array in display units and confirm orientation (row 0 = highest RPM, as
   the smoother expects; flip if your decode came out low-RPM-first).
2. **Identify anchors** — the cells the autotune actually corrected and you trust.
   These are the `(row, col)` set. Everything else is fair game to move.
3. **Smooth**: `smooth_table(original, anchors)`. Inspect with `print_table(...,
   anchor_mask)` and the move report from `print_delta(original, smoothed, ...)`.
4. **Review the delta** — max move and mean abs move are printed. A smoothing pass
   should make small moves (typically < a few %); a large max move means an anchor
   set that's too sparse or a degree that's too high for the data.
5. **Write back** as `.emubt` via emu-black-emubt-export (`write_csv` also dumps a
   spreadsheet-friendly grid for eyeballing first).

## Tuning the parameters

- **degree 3** is the safe default. Bump to 4 only when the real surface has a
  genuine inflection the cubic can't follow and you have enough anchors to support it.
- **n_passes 3** converges the row/column alternation. More passes ≈ smoother but
  flatter; watch the delta report so you don't sand off real structure.
- **extend 0** keeps movement strictly inside the anchor span. Raise to 1–3 only if
  you deliberately want the smooth curve to bleed a few cells past the last anchor.
- **anchor_w 100** makes the fit honor trusted cells strongly while still letting
  them inform the curve. Lower it if anchors are noisy and you want the polynomial
  to average through them instead of nailing them.

## Safety

- **Anchors are sacred.** The whole point is that trusted (logged-and-corrected)
  cells survive untouched. If a corrected cell moved in the output, the anchor set
  was wrong — fix it before importing.
- **Confirm orientation before smoothing.** The smoother assumes row 0 = highest
  RPM. A flipped array smooths along the wrong gradient and quietly ruins the table.
- **This is fuel.** A smoothed VE/dose table changes mixture in the cells between
  anchors. Re-verify a few representative cells against the original in EMU after
  import, and re-log before leaning on it.

## Related skills

- **emu-black-tune** — decode the table to an array and encode the result.
- **emu-black-emubt-export** — write the smoothed table as an importable `.emubt`.
- **emu-black-log** — produce the STFT-based VE corrections that become the anchors.
