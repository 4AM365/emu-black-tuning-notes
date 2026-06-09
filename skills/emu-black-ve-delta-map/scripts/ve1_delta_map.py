"""3D delta surface between two EMU Black veTable (u12) .emubt exports.

delta = ve1-053126 (after)  minus  ve1-before-smoothing (before)
Values shown in EMU display units (raw u12 x 0.1).
"""
import re
import os
import sys
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser(description="3D delta surface between two EMU veTable .emubt exports.")
ap.add_argument("--before", required=True, help=".emubt export (baseline)")
ap.add_argument("--after", required=True, help=".emubt export (corrected)")
ap.add_argument("--tune", required=True, help="tune XML (.xml.emub3) supplying axis bins (.emubt omits them)")
ap.add_argument("--symbol", default="veTable", help="table symbol (default veTable)")
ap.add_argument("--x-bins", dest="xbins", default="mapBins", help="X-axis bin symbol")
ap.add_argument("--y-bins", dest="ybins", default="rpmBins", help="Y-axis bin symbol")
ap.add_argument("--scale", type=float, default=0.1, help="display scale (u12 veTable = 0.1)")
ap.add_argument("--out", default="ve_delta_map.png")
args = ap.parse_args()
SCALE = args.scale
BEFORE, AFTER, TUNE_XML, OUT = args.before, args.after, args.tune, args.out


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    m = re.search(rf'name="{re.escape(args.symbol)}"[^>]*width="(\d+)"[^>]*height="(\d+)"[^>]*data="([^"]+)"', txt)
    if not m:
        sys.exit(f"{args.symbol} not found in {path}")
    w, h = int(m.group(1)), int(m.group(2))
    vals = [int(x, 16) for x in m.group(3).split()]
    arr = np.array(vals, dtype=float).reshape(h, w) * SCALE  # row 0 = lowest Y bin
    return arr, w, h


def load_bins(name):
    txt = open(TUNE_XML, "r", encoding="utf-8").read()
    m = re.search(rf'name="{name}"[^>]*data="([^"]+)"', txt)
    return np.array([int(v, 16) for v in m.group(1).split()], dtype=float)


before, w, h = load(BEFORE)
after, w2, h2 = load(AFTER)
assert (w, h) == (w2, h2), "table dims differ"

delta = after - before

print(f"grid {w} cols x {h} rows")
print(f"delta min {delta.min():+.2f}  max {delta.max():+.2f}  mean {delta.mean():+.2f}  rms {np.sqrt((delta**2).mean()):.2f}")

# Convention: X = MAP (kPa) low->high left->right; Y = RPM low->high bottom->top.
mapb = load_bins(args.xbins)   # X cols
rpmb = load_bins(args.ybins)   # Y rows, row 0 = lowest
X, Y = np.meshgrid(mapb, rpmb)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")
amax = max(abs(delta.min()), abs(delta.max()))
surf = ax.plot_surface(X, Y, delta, cmap="RdBu_r", vmin=-amax, vmax=amax,
                       edgecolor="k", linewidth=0.2, antialiased=True)
ax.set_xlabel("MAP (kPa) →")
ax.set_ylabel("RPM ↑")
ax.set_zlabel("Δ veTable (display units)")
ax.set_title(f"{args.symbol} delta: {os.path.basename(AFTER)} minus {os.path.basename(BEFORE)}")
fig.colorbar(surf, shrink=0.6, aspect=12, label="Δ (after - before)")
ax.view_init(elev=28, azim=-125)
fig.tight_layout()
fig.savefig(OUT, dpi=130)
print("wrote", OUT)
