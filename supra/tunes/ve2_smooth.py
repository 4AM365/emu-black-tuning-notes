"""
Smooth the EMU autotune VE table 2 (ethanol) using its corrected cells as anchors.
Identical method to ve_smooth.py (VE table 1): delta-overlay (base + blurred
correction), positive corrections extrapolated up the RPM axis to the ~5500 peak,
non-decreasing-to-peak guard. Base shape (residual knee, plateau) preserved off-band.
"""
import re
import numpy as np

BEFORE = r"C:\Code\car-projects\emu-black-tuning-notes\supra\tunes\new-fuel-strategy-before-ve-correction.xml.emub3"

MAP = np.array([20,35,49,64,79,93,108,123,137,152,167,181,196,211,225,240], float)
RPM = np.array([500,842,1184,1526,1868,2211,2553,2895,3237,3579,
                3921,4263,4605,4947,5289,5632,5974,6316,6658,7000], float)

# Transcribed EMU autotune VE2, rows high->low (7000 first).
T_hi2lo = np.array([
 [58.5,62.4,66.1,68.9,70.0,70.6,71.6,72.5,73.3,74.2,75.3,76.2,77.0,77.8,78.7,79.5],
 [58.0,61.9,65.6,68.4,69.6,70.4,71.5,72.4,73.3,74.3,75.3,76.1,76.9,77.8,78.7,79.5],
 [57.5,61.4,65.1,68.0,69.3,70.2,71.3,72.2,73.0,74.1,75.3,76.1,76.9,77.7,78.6,79.5],
 [56.9,60.8,64.5,67.5,69.0,70.0,71.1,72.2,73.0,74.2,75.2,76.0,76.7,77.6,78.4,79.4],
 [56.3,60.3,64.0,67.1,68.6,69.8,71.1,72.1,72.9,73.9,74.9,75.5,76.3,77.0,77.8,78.7],
 [56.0,59.9,63.6,66.7,68.3,69.6,71.1,71.9,72.7,76.8,74.6,75.1,75.6,76.4,77.1,78.0],
 [55.5,59.4,63.1,66.3,68.1,69.6,71.0,71.7,72.5,76.0,76.9,74.5,74.9,75.6,76.4,77.4],
 [54.8,58.7,62.4,65.8,67.8,69.4,70.6,71.3,72.1,74.9,73.3,73.9,74.3,75.1,75.9,76.9],
 [54.1,58.1,61.8,69.2,71.3,69.1,70.2,70.9,71.4,72.1,72.5,73.2,73.6,74.5,75.2,76.1],
 [53.6,57.6,61.4,67.8,69.7,71.5,69.8,70.3,70.7,71.3,71.8,72.2,72.7,73.5,74.4,75.2],
 [51.1,57.7,61.0,67.6,69.1,71.1,71.8,69.5,70.2,70.8,71.4,71.7,72.0,72.7,73.5,74.5],
 [51.3,55.9,59.3,64.2,67.5,70.5,68.4,68.9,69.4,70.2,70.6,71.0,71.3,72.0,72.6,73.6],
 [46.1,51.6,57.7,62.3,66.4,69.4,67.9,68.2,68.8,69.3,69.7,70.1,70.9,70.9,71.9,72.7],
 [44.3,46.4,57.1,59.8,66.8,68.5,67.3,67.3,67.4,67.7,68.1,68.5,69.0,69.9,70.8,71.7],
 [42.2,44.8,56.2,59.6,64.8,66.7,65.8,65.7,65.8,66.2,66.6,67.3,67.8,68.8,69.8,70.6],
 [41.6,43.4,54.6,59.5,62.7,64.5,64.4,64.0,64.2,64.8,65.4,65.9,66.7,67.6,68.8,69.6],
 [42.8,43.4,45.0,57.9,61.4,63.3,63.2,62.6,62.7,63.3,63.8,64.5,65.3,66.4,67.6,68.6],
 [42.6,43.3,44.2,53.3,59.7,61.8,61.3,60.7,60.8,61.4,62.2,63.1,64.0,65.2,66.2,67.5],
 [39.0,43.1,43.5,47.8,56.6,59.4,59.1,58.3,58.4,59.3,60.5,61.4,62.5,63.7,65.0,66.2],
 [39.0,39.0,42.7,46.6,54.1,56.4,56.4,55.9,56.2,57.2,58.6,59.7,60.9,62.3,63.6,65.2],
])
T = T_hi2lo[::-1].copy()
H, W = T.shape

b = open(BEFORE, encoding="utf-8", errors="replace").read()
m = re.search(r'name="veTable2"\s+storage="\w+"\s+width="\d+"\s+height="\d+"\s+data="([^"]*)"', b)
base = np.array([int(x, 16) for x in m.group(1).split()], float).reshape(H, W) * 0.1

delta = T - base

# ---- diagnostic: full delta grid (validate the band, spot transcription noise) ----
print("delta = transcription - base2 (rows RPM high->low)")
print("  RPM\\MAP " + "".join(f"{int(x):>5}" for x in MAP))
for ii in range(H - 1, -1, -1):
    print(f"{int(RPM[ii]):>6}  " + "".join(
        (f"{delta[ii,j]:>+5.1f}" if abs(delta[ii,j]) > 0.05 else "    .") for j in range(W)))

# ---- 1. anchors (same coherent band as VE1) ----
REACH = 3
band = np.zeros((H, W), bool)
for i in range(H):
    for j in range(W):
        if 1184 <= RPM[i] <= 4263 and j <= 6:
            band[i, j] = True
anchor = band & (np.abs(delta) > 0.15)
# Boost-region airflow correction (152-167 kPa, 4600-5300 rpm): a coherent block in
# VE2's autotune outside the main idle/cruise band. Inject explicitly (same values
# applied to VE1 too, since VE is fuel-independent).
BOOST_ANCHORS = {(4605,152):2.1, (4947,152):2.7, (4947,167):2.8, (5289,152):3.2}
for (rp, mp), d in BOOST_ANCHORS.items():
    bi = int(np.where(RPM == rp)[0][0]); bj = int(np.where(MAP == mp)[0][0])
    delta[bi, bj] = d; anchor[bi, bj] = True
ai, aj = np.where(anchor)
print(f"\nAnchors (band + boost block, |delta|>0.15): {anchor.sum()} cells  "
      f"delta {delta[anchor].min():+.1f}..{delta[anchor].max():+.1f} mean {delta[anchor].mean():+.2f}")

# ---- 2. projection ----
dfill = np.zeros((H, W))
for i in range(H):
    for j in range(W):
        if anchor[i, j]:
            dfill[i, j] = delta[i, j]; continue
        num = den = 0.0
        for (ia, ja) in zip(ai, aj):
            if ia == i and abs(ja - j) <= REACH:
                w = 1.0 / (abs(ja - j) + 1)
            elif ja == j and abs(ia - i) <= REACH:
                w = 1.0 / (abs(ia - i) + 1)
            else:
                continue
            num += w * delta[ia, ja]; den += w
        dfill[i, j] = num / den if den > 0 else 0.0

# ---- 2b. extrapolate positive corrections up the RPM axis ----
PEAK_RPM = 5500
peak_idx = int(np.argmin(np.abs(RPM - PEAK_RPM)))
EXTRAP_MIN = 0.3
for j in range(W):
    rows = [i for i in range(H) if anchor[i, j]]
    if not rows:
        continue
    i_top = max(rows); d_top = dfill[i_top, j]
    if d_top < EXTRAP_MIN or i_top >= peak_idx:
        continue
    for i in range(i_top + 1, peak_idx + 1):
        if not anchor[i, j]:
            dfill[i, j] = d_top
    for i in range(peak_idx + 1, H):
        if not anchor[i, j]:
            dfill[i, j] = d_top * (1 - (i - peak_idx) / (H - 1 - peak_idx))

# ---- 3+4. delta-overlay with blur ----
BLUR_PASSES = 2
def blur(a, passes):
    k = np.array([1.0, 2.0, 1.0]); k /= k.sum()
    out = a.copy()
    for _ in range(passes):
        p = np.vstack([out[:1], out, out[-1:]])
        out = k[0]*p[:-2] + k[1]*p[1:-1] + k[2]*p[2:]
        p = np.hstack([out[:, :1], out, out[:, -1:]])
        out = k[0]*p[:, :-2] + k[1]*p[:, 1:-1] + k[2]*p[:, 2:]
    return out

dsm = blur(dfill, BLUR_PASSES)
F = np.clip(base + dsm, 0, 409.5)

# ---- 5. non-decreasing-to-peak guard ----
fixed = 0
for j in range(W):
    for i in range(1, peak_idx + 1):
        if F[i, j] < F[i - 1, j]:
            F[i, j] = F[i - 1, j]; fixed += 1
print(f"Overlay: max|smoothed delta| {np.abs(dsm).max():.1f}%  "
      f"changed>0.05%: {(np.abs(F-base)>0.05).sum()}  monotonicity fixes: {fixed}")

def show(title, arr):
    print(f"\n{title}")
    print("  RPM\\MAP " + "".join(f"{int(x):>6}" for x in MAP))
    for ii in range(H - 1, -1, -1):
        print(f"{int(RPM[ii]):>6}  " + "".join(f"{arr[ii,j]:>6.1f}" for j in range(W)))

show("FINAL VE table 2 [%] (base2 + smoothed autotune correction)", F)
np.save(r"C:\Code\car-projects\emu-black-tuning-notes\supra\tunes\ve2_smoothed.npy", F)
print("\nSaved ve2_smoothed.npy")
