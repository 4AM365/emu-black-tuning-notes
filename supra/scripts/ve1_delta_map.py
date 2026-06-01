"""3D delta surface between two EMU Black veTable (u12) .emubt exports.

delta = ve1-053126 (after)  minus  ve1-before-smoothing (before)
Values shown in EMU display units (raw u12 x 0.1).
"""
import re
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SCALE = 0.1  # u12 veTable display scale
BASE = r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra"
BEFORE = rf"{BASE}\ve1-before-smoothing.emubt"
AFTER = rf"{BASE}\ve1-053126.emubt"
# Full tune XML supplies the real axis bins (.emubt exports omit them).
TUNE_XML = r"C:\Code\car-projects\emu-black-tuning-notes\supra\tunes\new-fuel-strategy-after-ve-correction.xml.emub3"
OUT = r"C:\Code\car-projects\emu-black-tuning-notes\supra\tunes\ve1_delta_map.png"


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    m = re.search(r'name="veTable"[^>]*width="(\d+)"[^>]*height="(\d+)"[^>]*data="([^"]+)"', txt)
    if not m:
        sys.exit(f"veTable not found in {path}")
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
mapb = load_bins("mapBins")   # 16 cols
rpmb = load_bins("rpmBins")   # 20 rows, row 0 = lowest RPM
X, Y = np.meshgrid(mapb, rpmb)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")
amax = max(abs(delta.min()), abs(delta.max()))
surf = ax.plot_surface(X, Y, delta, cmap="RdBu_r", vmin=-amax, vmax=amax,
                       edgecolor="k", linewidth=0.2, antialiased=True)
ax.set_xlabel("MAP (kPa) →")
ax.set_ylabel("RPM ↑")
ax.set_zlabel("Δ veTable (display units)")
ax.set_title("VE1 delta: ve1-053126 minus ve1-before-smoothing")
fig.colorbar(surf, shrink=0.6, aspect=12, label="Δ (after - before)")
ax.view_init(elev=28, azim=-125)
fig.tight_layout()
fig.savefig(OUT, dpi=130)
print("wrote", OUT)
