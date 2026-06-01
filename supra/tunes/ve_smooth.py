"""
Smooth the EMU autotune VE table 1 using its corrected cells as anchors.

Pipeline (per user spec, 'extreme simplicity'):
  1. Anchors = cells where transcribed autotune table T differs from base.
  2. Projection: spread each anchor's delta (T-base) outward along its row and
     column with inverse-distance weighting -> in-the-ballpark surface P = base + dfill.
     (Preserves the RPM-dependence of the correction; decays to base off the band.)
  3. Column fit: each MAP column fit as VE-vs-RPM (poly, cap 4th), snap.
  4. Row fit:    each RPM row    fit as VE-vs-MAP (poly, cap 4th), snap.
Anchors are intentionally snapped onto the smooth surface too.
"""
import re
import numpy as np

BEFORE = r"C:\Code\car-projects\emu-black-tuning-notes\supra\tunes\new-fuel-strategy-before-ve-correction.xml.emub3"

MAP = np.array([20,35,49,64,79,93,108,123,137,152,167,181,196,211,225,240], float)
RPM = np.array([500,842,1184,1526,1868,2211,2553,2895,3237,3579,
                3921,4263,4605,4947,5289,5632,5974,6316,6658,7000], float)  # low->high (storage order)

# Transcribed EMU autotune VE1, rows high->low (7000 first). Flip to storage order below.
T_hi2lo = np.array([
 [58.5,62.4,66.1,69.2,70.8,72.1,73.1,74.1,74.9,75.8,76.9,77.8,78.7,79.5,80.4,81.2],
 [58.0,61.9,65.6,68.7,70.4,71.9,73.0,74.0,74.9,75.9,76.9,77.7,78.6,79.5,80.4,81.2],
 [57.5,61.4,65.1,68.3,70.1,71.7,72.8,73.8,74.6,75.7,76.9,77.7,78.5,79.4,80.3,81.2],
 [56.9,60.8,64.5,67.8,69.8,71.5,72.6,73.7,74.6,75.8,76.8,77.6,78.4,79.3,80.1,81.1],
 [56.3,60.3,64.0,67.4,69.4,71.1,72.4,73.5,74.5,75.6,76.6,77.3,78.2,79.0,79.8,80.7],
 [56.0,59.9,63.6,67.0,69.1,70.8,72.2,73.3,75.2,75.5,77.0,77.8,78.6,79.4,80.3,80.7],
 [55.5,59.4,63.1,66.6,68.8,70.6,72.0,73.1,74.1,74.9,75.9,76.6,77.3,78.1,78.9,79.9],
 [54.8,58.7,62.4,66.0,68.3,70.3,71.6,72.7,73.7,74.6,75.3,76.1,76.7,77.5,78.4,79.4],
 [54.1,58.1,61.8,69.3,71.4,69.9,71.2,72.2,73.1,74.1,74.7,75.5,76.0,76.9,77.7,78.6],
 [53.6,57.6,61.4,67.8,69.8,71.6,70.7,71.6,72.4,73.3,74.0,74.5,75.1,75.9,76.8,77.7],
 [51.1,57.7,61.0,67.6,69.2,71.2,72.1,70.8,71.7,72.4,73.2,73.7,74.3,75.1,75.9,76.9],
 [51.3,55.9,59.3,64.2,67.5,70.6,69.3,70.2,70.9,71.7,72.3,72.9,73.6,74.3,75.0,76.0],
 [46.1,51.6,57.7,62.3,66.4,69.5,68.0,69.0,70.2,70.9,71.6,72.3,73.2,74.2,75.1,75.1],
 [44.3,46.4,57.1,59.8,66.7,68.5,67.1,67.8,68.4,69.0,69.7,70.4,71.2,72.2,73.1,74.0],
 [42.2,44.8,56.2,59.6,64.7,66.7,65.9,66.5,67.0,67.5,68.2,69.1,69.9,71.0,72.1,72.9],
 [41.6,43.4,54.6,59.5,62.7,64.4,64.6,65.0,65.6,66.2,66.9,67.7,68.8,69.8,71.0,71.9],
 [42.8,43.4,45.1,57.9,61.4,62.9,63.1,63.5,64.1,64.7,65.3,66.3,67.4,68.6,69.8,70.8],
 [42.5,43.3,44.2,53.3,59.8,61.6,61.6,61.6,62.1,62.7,63.7,64.8,66.0,67.3,68.4,69.7],
 [38.4,39.0,42.0,47.8,56.7,59.4,59.4,59.3,59.7,60.6,61.9,63.1,64.5,65.8,67.1,68.4],
 [37.3,37.9,40.4,45.5,54.2,56.4,56.7,56.8,57.4,58.5,60.0,61.3,62.8,64.4,65.7,67.3],
])
T = T_hi2lo[::-1].copy()          # storage order: row0 = 500 rpm
H, W = T.shape

# base table (exact)
b = open(BEFORE, encoding="utf-8", errors="replace").read()
m = re.search(r'name="veTable"\s+storage="\w+"\s+width="\d+"\s+height="\d+"\s+data="([^"]*)"', b)
base = np.array([int(x, 16) for x in m.group(1).split()], float).reshape(H, W) * 0.1

# ---- 1. anchors ----
# Restrict to the coherent autotune operating band; off-band T!=base diffs are
# screenshot-transcription noise (no-boost cells the autotune never touches).
REACH = 3                                  # projection reach in grid steps
delta = T - base
band = np.zeros((H, W), bool)
for i in range(H):
    for j in range(W):
        if 1184 <= RPM[i] <= 4263 and j <= 6:   # MAP <= 108 kPa
            band[i, j] = True
anchor = band & (np.abs(delta) > 0.15)
# Boost-region airflow correction from VE2's autotune (152-167 kPa, 4600-5300 rpm).
# VE is volumetric efficiency of AIR (fuel-independent), so the same correction
# belongs in table 1. VE1's own screenshot didn't capture this block; inject it.
BOOST_ANCHORS = {(4605,152):2.1, (4947,152):2.7, (4947,167):2.8, (5289,152):3.2}
for (rp, mp), d in BOOST_ANCHORS.items():
    bi = int(np.where(RPM == rp)[0][0]); bj = int(np.where(MAP == mp)[0][0])
    delta[bi, bj] = d; anchor[bi, bj] = True
ai, aj = np.where(anchor)
print(f"Anchors (band + boost block, |delta|>0.15): {anchor.sum()} cells")
print(f"Anchor delta range: {delta[anchor].min():+.1f} .. {delta[anchor].max():+.1f}  "
      f"mean {delta[anchor].mean():+.2f}")

# ---- 2. projection: inverse-distance spread along rows & columns, reach-capped ----
dfill = np.zeros((H, W))
for i in range(H):
    for j in range(W):
        if anchor[i, j]:
            dfill[i, j] = delta[i, j]
            continue
        num = den = 0.0
        for (ia, ja) in zip(ai, aj):
            if ia == i and abs(ja - j) <= REACH:          # same row, within reach
                w = 1.0 / (abs(ja - j) + 1)
            elif ja == j and abs(ia - i) <= REACH:        # same column, within reach
                w = 1.0 / (abs(ia - i) + 1)
            else:
                continue
            num += w * delta[ia, ja]
            den += w
        dfill[i, j] = num / den if den > 0 else 0.0

# ---- 2b. extrapolate POSITIVE corrections UP the RPM axis toward the peak ----
# Physics: VE rises with RPM to the engine's peak (~5500). If the autotune raises a
# mid-RPM cell but the unvisited cells above it stay at base, the corrected cell can
# poke above them -> a false local peak below 5500. Unaltered cells above an upward
# correction must be lifted too. Hold the top anchor's delta from the band top to the
# peak bin, then taper to 0 by redline -> a single hump that peaks near 5500.
PEAK_RPM = 5500
peak_idx = int(np.argmin(np.abs(RPM - PEAK_RPM)))     # bin nearest 5500 (=5632)
EXTRAP_MIN = 0.3                                       # only meaningful positive corr.
for j in range(W):
    rows = [i for i in range(H) if anchor[i, j]]
    if not rows:
        continue
    i_top = max(rows)
    d_top = dfill[i_top, j]
    if d_top < EXTRAP_MIN or i_top >= peak_idx:
        continue
    for i in range(i_top + 1, peak_idx + 1):           # hold delta up to the peak
        if not anchor[i, j]:
            dfill[i, j] = d_top
    for i in range(peak_idx + 1, H):                   # taper to 0 by redline
        if not anchor[i, j]:
            dfill[i, j] = d_top * (1 - (i - peak_idx) / (H - 1 - peak_idx))

# ---- 3+4. DELTA-OVERLAY: smooth only the correction, keep base shape ----
# Rationale: the base table already encodes the physical residual-gas knee
# (Heywood s6.4) and cam inflection (Banish p.523). Re-fitting absolute VE with a
# polynomial rounds those features off. Instead we smooth the small correction
# surface (dfill) with a light separable [1,2,1] blur and add it back to base.
# The blur decays to ~0 away from the anchor band, so untouched cells stay at base.
BLUR_PASSES = 2

def blur(a, passes):
    k = np.array([1.0, 2.0, 1.0]); k /= k.sum()
    out = a.copy()
    for _ in range(passes):
        p = np.vstack([out[:1], out, out[-1:]])                 # edge-pad RPM axis
        out = k[0]*p[:-2] + k[1]*p[1:-1] + k[2]*p[2:]
        p = np.hstack([out[:, :1], out, out[:, -1:]])           # edge-pad MAP axis
        out = k[0]*p[:, :-2] + k[1]*p[:, 1:-1] + k[2]*p[:, 2:]
    return out

dsm = blur(dfill, BLUR_PASSES)
F = np.clip(base + dsm, 0, 409.5)

# ---- 5. guarantee non-decreasing VE up to the peak (cheap safety net) ----
fixed = 0
for j in range(W):
    for i in range(1, peak_idx + 1):
        if F[i, j] < F[i - 1, j]:
            F[i, j] = F[i - 1, j]
            fixed += 1
print(f"Correction overlay: max |smoothed delta| {np.abs(dsm).max():.1f}%  "
      f"cells changed >0.05%: {(np.abs(F-base)>0.05).sum()}  | monotonicity fixes: {fixed}")

# ---- report ----
def show(title, arr):
    print(f"\n{title}")
    print("  RPM\\MAP " + "".join(f"{int(x):>6}" for x in MAP))
    for ii in range(H - 1, -1, -1):
        print(f"{int(RPM[ii]):>6}  " + "".join(f"{arr[ii,j]:>6.1f}" for j in range(W)))

print(f"\nMethod: delta-overlay (base + blur(correction), {BLUR_PASSES} passes)")
show("FINAL VE table 1 [%]  (base + smoothed autotune correction)", F)

mv = F - T
print(f"\nFinal vs transcription: mean {mv.mean():+.2f}%  max|move| {np.abs(mv).max():.1f}%")
print(f"Anchor cells moved by smoothing: mean {np.abs(mv[anchor]).mean():.2f}%  "
      f"max {np.abs(mv[anchor]).max():.2f}%")

# save final % grid (storage order) for the exporter
np.save(r"C:\Code\car-projects\emu-black-tuning-notes\supra\tunes\ve1_smoothed.npy", F)
print("\nSaved ve1_smoothed.npy (storage order, % units)")
