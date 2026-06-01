"""smooth_ve.py — VE table polynomial smoother.

Algorithm
---------
For each column (RPM sweep) and each row (load sweep):

  1. Find the span of anchor cells in that axis: [lo_anchor, hi_anchor].
  2. Extend the working segment by EXTEND cells on each side (default 3).
     Cells outside that extended window are left untouched — this prevents
     wild polynomial extrapolation far from autotune data.
  3. Fit a degree-N (default 3) weighted polynomial over the working segment.
     Anchor cells get weight ANCHOR_W (default 100); non-anchors get weight 1.
  4. Replace non-anchor cells in the segment with the polynomial value.
     Anchor cells are always snapped back to their exact original value.
  5. Repeat for N_PASSES (default 3) column+row sweeps.

This is equivalent to: "reduce step size between adjacent cells by addition,
then fit the smoothing line (3rd-order polynomial), then alter cells to sit
on that line within a couple percent."

Usage (standalone)
------------------
  python smooth_ve.py

Or import:
  from smooth_ve import smooth_table, print_table, print_delta, write_csv
"""

from __future__ import annotations

import numpy as np
from pathlib import Path


# ─── Core smoother ───────────────────────────────────────────────────────────

def _poly_smooth_1d(
    values: np.ndarray,
    anchor_mask: np.ndarray,
    degree: int,
    extend: int,
    anchor_w: float,
) -> np.ndarray:
    """Smooth one row or column within the bounded anchor zone."""
    n = len(values)
    anchor_idx = np.where(anchor_mask)[0]

    if len(anchor_idx) == 0:
        return values.copy()   # nothing to anchor to — leave untouched

    lo = max(0, int(anchor_idx[0])  - extend)
    hi = min(n - 1, int(anchor_idx[-1]) + extend)

    seg_len = hi - lo + 1
    if seg_len <= degree:
        return values.copy()   # too short to fit this degree

    # Normalise x to [0, 1] inside the segment for numerical stability
    x = np.linspace(0.0, 1.0, seg_len)
    v = values[lo : hi + 1].copy()
    m = anchor_mask[lo : hi + 1]
    w = np.where(m, anchor_w, 1.0)

    coeffs = np.polyfit(x, v, degree, w=w)
    poly   = np.polyval(coeffs, x)

    result = values.copy()
    for k, abs_idx in enumerate(range(lo, hi + 1)):
        if not anchor_mask[abs_idx]:
            result[abs_idx] = poly[k]

    return result


def smooth_table(
    original: np.ndarray,
    anchors: set[tuple[int, int]],
    degree: int   = 3,
    n_passes: int = 3,
    extend: int   = 0,
    anchor_w: float = 100.0,
) -> np.ndarray:
    """Return smoothed copy of `original`.

    Parameters
    ----------
    original   : shape (n_rpm, n_load) float, row 0 = highest RPM
    anchors    : {(row, col)} cells that must keep their exact original value
    degree     : polynomial degree (3 recommended; 4 for tighter fit)
    n_passes   : number of column+row sweep iterations
    extend     : cells beyond the anchor zone that are allowed to move
    anchor_w   : weight multiplier for anchor vs non-anchor cells
    """
    nrow, ncol = original.shape
    mask = np.zeros((nrow, ncol), dtype=bool)
    for ri, ci in anchors:
        mask[ri, ci] = True

    table = original.astype(float).copy()

    for _ in range(n_passes):
        # ── Column sweep (RPM axis) ──────────────────────────────────────────
        for j in range(ncol):
            table[:, j] = _poly_smooth_1d(
                table[:, j], mask[:, j], degree, extend, anchor_w
            )
        table[mask] = original[mask]

        # ── Row sweep (load axis) ────────────────────────────────────────────
        for i in range(nrow):
            table[i, :] = _poly_smooth_1d(
                table[i, :], mask[i, :], degree, extend, anchor_w
            )
        table[mask] = original[mask]

    return np.round(table, 1)


# ─── Output helpers ──────────────────────────────────────────────────────────

def print_table(
    label: str,
    table: np.ndarray,
    rpm_axis: list[int],
    load_axis: list[int],
    anchor_mask: np.ndarray | None = None,
) -> None:
    print(f"\n=== {label} ===")
    header = "      " + "".join(f"{l:>7}" for l in load_axis)
    print(header)
    for i, rpm in enumerate(rpm_axis):
        row_s = f"{rpm:>5} "
        for j in range(len(load_axis)):
            v = table[i, j]
            mark = "*" if (anchor_mask is not None and anchor_mask[i, j]) else " "
            row_s += f"{v:>5.1f}{mark}"
        print(row_s)
    print(header)


def print_delta(
    original: np.ndarray,
    smoothed: np.ndarray,
    rpm_axis: list[int],
    load_axis: list[int],
) -> None:
    delta = smoothed - original
    print(f"\nMax move: {np.abs(delta).max():.1f}  "
          f"Mean abs move: {np.abs(delta).mean():.2f}")
    header = "      " + "".join(f"{l:>7}" for l in load_axis)
    print("\n=== DELTA ===")
    print(header)
    for i, rpm in enumerate(rpm_axis):
        row_s = f"{rpm:>5} "
        for j in range(len(load_axis)):
            d = delta[i, j]
            row_s += f"{d:>+6.1f} "
        print(row_s)


def write_csv(
    table: np.ndarray,
    rpm_axis: list[int],
    load_axis: list[int],
    path: Path,
) -> None:
    lines = [",".join(["RPM\\MAP"] + [str(l) for l in load_axis])]
    for i, rpm in enumerate(rpm_axis):
        row = [str(rpm)] + [f"{table[i,j]:.1f}" for j in range(len(load_axis))]
        lines.append(",".join(row))
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {path}")
