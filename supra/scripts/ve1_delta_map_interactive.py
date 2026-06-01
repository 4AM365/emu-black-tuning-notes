"""Interactive 3D delta surface (plotly) between two EMU Black veTable .emubt exports.

delta = ve1-053126 (after) minus ve1-before-smoothing (before), EMU display units (raw u12 x 0.1).
Writes a standalone HTML you can open in any browser and rotate/zoom/hover.
"""
import re
import sys
import numpy as np
import plotly.graph_objects as go

SCALE = 0.1
BASE = r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra"
BEFORE = rf"{BASE}\ve1-before-smoothing.emubt"
AFTER = rf"{BASE}\ve1-053126.emubt"
# Full tune XML supplies the real axis bins (.emubt exports omit them).
TUNE_XML = r"C:\Code\car-projects\emu-black-tuning-notes\supra\tunes\new-fuel-strategy-after-ve-correction.xml.emub3"
OUT = r"C:\Code\car-projects\emu-black-tuning-notes\supra\tunes\ve1_delta_map.html"


def load(path):
    txt = open(path, "r", encoding="utf-8").read()
    m = re.search(r'name="veTable"[^>]*width="(\d+)"[^>]*height="(\d+)"[^>]*data="([^"]+)"', txt)
    if not m:
        sys.exit(f"veTable not found in {path}")
    w, h = int(m.group(1)), int(m.group(2))
    vals = [int(x, 16) for x in m.group(3).split()]
    return np.array(vals, dtype=float).reshape(h, w) * SCALE, w, h


def load_bins(name):
    txt = open(TUNE_XML, "r", encoding="utf-8").read()
    m = re.search(rf'name="{name}"[^>]*data="([^"]+)"', txt)
    return np.array([int(v, 16) for v in m.group(1).split()], dtype=float)


before, w, h = load(BEFORE)
after, w2, h2 = load(AFTER)
assert (w, h) == (w2, h2)
delta = after - before
amax = max(abs(delta.min()), abs(delta.max()))

# Convention: X = MAP (kPa) low->high left->right; Y = RPM low->high bottom->top.
x = load_bins("mapBins")   # 16 cols
y = load_bins("rpmBins")   # 20 rows, row 0 = lowest RPM (bottom)

fig = go.Figure(go.Surface(
    x=x, y=y, z=delta,
    colorscale="RdBu_r", cmid=0, cmin=-amax, cmax=amax,
    colorbar=dict(title="Δ (after-before)"),
    hovertemplate="MAP %{x:.0f} kPa<br>RPM %{y:.0f}<br>Δ %{z:.2f}<extra></extra>",
))
fig.update_layout(
    title="VE1 delta: ve1-053126 minus ve1-before-smoothing",
    scene=dict(
        xaxis_title="MAP (kPa) →",
        yaxis_title="RPM ↑",
        zaxis_title="Δ veTable (display units)",
    ),
    width=1100, height=800,
)
fig.write_html(OUT, include_plotlyjs=True)
print(f"delta min {delta.min():+.2f} max {delta.max():+.2f} rms {np.sqrt((delta**2).mean()):.2f}")
print("wrote", OUT)
