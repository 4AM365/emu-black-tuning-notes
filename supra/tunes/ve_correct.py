"""
One-off VE correction from a closed-loop log.

Reads veTable / veTable2 (u12, 16 MAP cols x 20 RPM rows, scale 0.1) and their
axis bins from the tune XML, computes a per-cell multiplicative correction factor
from a steady-state log, and writes a corrected copy of the tune.

Key modeling choice: VE is volumetric efficiency of AIR (fuel-independent), so the
SAME correction factor is applied to both veTable and veTable2, preserving their
existing relative offset.
"""
import re, sys
import numpy as np
import pandas as pd

TUNE = r"C:\Code\car-projects\emu-black-tuning-notes\supra\tunes\new-fuel-strategy-before-ve-correction.xml.emub3"
LOG  = r"C:\Code\car-projects\emu-black-tuning-notes\supra\logs\new_fuel_strategy.csv"
OUT  = r"C:\Code\car-projects\emu-black-tuning-notes\supra\tunes\new-fuel-strategy-after-ve-correction.xml.emub3"

VE_SCALE = 0.1
WEIGHT_THRESHOLD = 25.0   # min accumulated bilinear weight (~1 s @ 25 Hz) to touch a cell
CLAMP = 0.15              # max +/- correction per pass
ACC_TOL = 1.0            # |Acc. enrichment %| below this = not a tip-in transient

txt = open(TUNE, encoding="utf-8", errors="replace").read()

def get_sym(name):
    m = re.search(
        r'name="%s"\s+storage="(\w+)"\s+width="(\d+)"\s+height="(\d+)"\s+data="([^"]*)"' % re.escape(name),
        txt)
    if not m:
        raise SystemExit("symbol not found: " + name)
    storage, w, h, data = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
    vals = [int(x, 16) for x in data.split()]
    return storage, w, h, vals, data

_, _, _, mapbins, _ = get_sym("mapBins")
_, _, _, rpmbins, _ = get_sym("rpmBins")
st1, w1, h1, ve1, raw1 = get_sym("veTable")
st2, w2, h2, ve2, raw2 = get_sym("veTable2")

mapb = np.array(mapbins, float)               # kPa, scale 1
rpmb = np.array(rpmbins, float)               # rpm, scale 1
ve1g = np.array(ve1, float).reshape(h1, w1)   # [rpm, map] raw u12
ve2g = np.array(ve2, float).reshape(h2, w2)
assert (h1, w1) == (len(rpmb), len(mapb)), (h1, w1, len(rpmb), len(mapb))

print(f"veTable {st1} {w1}x{h1}  veTable2 {st2} {w2}x{h2}")
print(f"MAP bins (kPa): {mapb.astype(int).tolist()}")
print(f"RPM bins:       {rpmb.astype(int).tolist()}")

# ---- log ----
df = pd.read_csv(LOG, sep=";")
df.columns = df.columns.str.strip()

rpm   = df["RPM"].astype(float)
mp    = df["MAP"].astype(float)
stft  = df["Short term trim"].astype(float)
fstft = df["F.Short term trim"].astype(float)
lam   = df["Lambda 1"].astype(float)
ltgt  = df["Lambda target"].astype(float)
lval  = df["Lambda is valid"].astype(float)
fcut  = df["Fuel Cut"].astype(float)
ase   = df["Afterstart Enrichment"].astype(float)
wue   = df["Warmup enrichment"].astype(float)
acc   = df["Acc. enrichment %"].astype(float)
over  = df["Overrun status"].astype(float)
eth   = df["Ethanol content"].astype(float)

# Closed-loop only (F.Short term trim == 1): in this regime STFT is genuinely
# settling the mixture to target, so the correction is bounded by the real fuel
# error. Open-loop samples (decel / light-load, STFT frozen) are transient-
# contaminated and excluded -- they produced spurious -15% corner corrections.
mask = ((lval == 1) & (fstft == 1) & (fcut == 0) & (over < 2)
        & (ase == 0) & (wue == 0)
        & (acc.abs() <= ACC_TOL) & (ltgt > 0) & (lam > 0)
        & (rpm >= rpmb[0]) & (mp >= mapb[0]))

F = (1.0 + stft / 100.0) * (lam / ltgt)
# drop absurd outliers (sensor glitches) before accumulation
mask = mask & (F > 0.5) & (F < 1.5)

print(f"\nLog rows: {len(df)}  steady-state usable: {int(mask.sum())} "
      f"({100*mask.sum()/len(df):.1f}%)")
print(f"Ethanol content: {eth[mask].mean():.1f}%  (min {eth.min():.1f} max {eth.max():.1f})")
print(f"F over usable samples: mean {F[mask].mean():.4f}  "
      f"p5 {F[mask].quantile(.05):.4f}  p95 {F[mask].quantile(.95):.4f}")

def bracket(bins, v):
    if v <= bins[0]:  return 0, 0, 0.0
    if v >= bins[-1]: return len(bins)-1, len(bins)-1, 0.0
    i = int(np.searchsorted(bins, v) - 1)
    frac = (v - bins[i]) / (bins[i+1] - bins[i])
    return i, i+1, frac

wsum = np.zeros((h1, w1))
fsum = np.zeros((h1, w1))
for r, m_, f in zip(rpm[mask].values, mp[mask].values, F[mask].values):
    ri, ri2, rf = bracket(rpmb, r)
    mi, mi2, mf = bracket(mapb, m_)
    for rr, wr in ((ri, 1-rf), (ri2, rf)):
        for mm, wm in ((mi, 1-mf), (mi2, mf)):
            w = wr * wm
            if w <= 0:
                continue
            wsum[rr, mm] += w
            fsum[rr, mm] += w * f

with np.errstate(invalid="ignore", divide="ignore"):
    Fcell = np.where(wsum >= WEIGHT_THRESHOLD, fsum / np.maximum(wsum, 1e-9), 1.0)
Fcell = np.clip(Fcell, 1-CLAMP, 1+CLAMP)
touched = wsum >= WEIGHT_THRESHOLD

ve1n = np.clip(np.rint(ve1g * Fcell), 0, 4095).astype(int)
ve2n = np.clip(np.rint(ve2g * Fcell), 0, 4095).astype(int)

ncell = int(touched.sum())
print(f"\nCells touched: {ncell}/{h1*w1}")
dev = (Fcell[touched]-1)*100
print(f"Correction on touched cells: mean {dev.mean():+.2f}%  "
      f"min {dev.min():+.2f}%  max {dev.max():+.2f}%")

# ---- report: which rpm/map regions moved ----
print("\nPer-cell correction % (rows=RPM high->low, cols=MAP low->high). '.' = untouched")
hdr = "RPM\\MAP " + " ".join(f"{int(m):>4}" for m in mapb)
print(hdr)
for ri in range(h1-1, -1, -1):
    cells = []
    for mi in range(w1):
        if touched[ri, mi]:
            cells.append(f"{(Fcell[ri,mi]-1)*100:>+4.0f}")
        else:
            cells.append("   .")
    print(f"{int(rpmb[ri]):>6}  " + " ".join(cells))

# ---- before/after VE% on touched cells ----
print("\nBefore -> After VE% (veTable, touched cells only)")
print(hdr)
for ri in range(h1-1, -1, -1):
    cells = []
    for mi in range(w1):
        if touched[ri, mi]:
            cells.append(f"{ve1g[ri,mi]*VE_SCALE:>4.1f}->{ve1n[ri,mi]*VE_SCALE:<4.1f}")
        else:
            cells.append("    .    ")
    print(f"{int(rpmb[ri]):>6}  " + " ".join(cells))

def encode(arr):
    return " ".join(format(int(v), "X") for v in arr.flatten()) + " "

new1 = encode(ve1n)
new2 = encode(ve2n)

# sanity: same token count
assert len(new1.split()) == h1*w1 and len(new2.split()) == h2*w2

out = txt.replace('data="%s"' % raw1, 'data="%s"' % new1, 1)
assert out != txt, "veTable replace failed"
out2 = out.replace('data="%s"' % raw2, 'data="%s"' % new2, 1)
assert out2 != out, "veTable2 replace failed"
open(OUT, "w", encoding="utf-8").write(out2)
print(f"\nWrote {OUT}")
print("NOTE: variablesChecksum/tablesChecksum are now stale; EMU recomputes on import.")
