#!/usr/bin/env python3
"""Build corrected Pre-IC sensor calibration (.emubt) by copying the real IAT
sensor curve onto Custom Temperature 1 (the Pre-IC input).

Pre-IC currently runs the WRONG curve (customTemp1Cal). The correct curve is the
IAT sensor cal already in the tune: iatTbl (14 sbyte temps) over voltage5VIATBin
(14 ubyte voltage nodes). customTemp1Cal/Bins are only 10 points -> we resample
to the 10 IAT nodes that best cover the operating band (zero error at those nodes).
"""

# --- IAT calibration as stored in the tune (decoded, verified vs screenshot) ---
# voltage5VIATBin raw (ubyte, display V = raw * 5/255) and iatTbl temps (C)
IAT_VRAW = [0, 12, 16, 23, 40, 51, 74, 88, 126, 151, 185, 209, 236, 254]
IAT_TEMP = [121,115,104, 91, 71, 62, 49, 42, 27, 18, 6, -5, -22, -39]
VSCALE = 5/255

# --- choose 10 of 14 nodes: keep band-dense (40-90C), drop low-curvature/extreme
# dropped raw nodes: 12(115C),16(104C) [>100C, never seen], 185(6C),236(-22C) [sub-ambient]
KEEP_RAW = [0, 23, 40, 51, 74, 88, 126, 151, 209, 254]
idx = [IAT_VRAW.index(r) for r in KEEP_RAW]
bins_raw  = [IAT_VRAW[i] for i in idx]          # customTemp1CalBins (ubyte)
temps_raw = [IAT_TEMP[i] for i in idx]          # customTemp1Cal     (ubyte, sign-mag)

def fhex(v): return format(int(v), "X")         # EMU sign-magnitude hex
bins_hex  = " ".join(fhex(v) for v in bins_raw)  + " "
temps_hex = " ".join(fhex(v) for v in temps_raw) + " "

# --- OLD (wrong) for the report ---
OLD_BINS_RAW = [0,28,29,85,113,141,169,198,226,254]
OLD_TEMP     = [92,55,54,15,3,-5,-15,-24,-33,-40]

def interp(vraw, xs, ys):
    if vraw<=xs[0]: return ys[0]
    if vraw>=xs[-1]: return ys[-1]
    for i in range(len(xs)-1):
        if xs[i]<=vraw<=xs[i+1]:
            f=(vraw-xs[i])/(xs[i+1]-xs[i]); return ys[i]+f*(ys[i+1]-ys[i])

print("Corrected Custom temp cal 1  (Pre-IC) — 10-pt resample of the IAT curve\n")
print(f"{'V':>6} | {'OLD wrongC':>10} | {'NEW correctC':>12} | {'true IAT@V':>10}")
print("-"*48)
for vr,tn in zip(bins_raw,temps_raw):
    V=vr*VSCALE
    old=interp(vr,OLD_BINS_RAW,OLD_TEMP)
    true=interp(vr,IAT_VRAW,IAT_TEMP)
    print(f"{V:6.2f} | {old:10.1f} | {tn:12d} | {true:10.1f}")

# operating-band error check (sample every 0.05V across 0.4-1.8V => ~40-90C)
maxerr=0
for k in range(8,37):
    vr=k*255/50  # not exact; sample by voltage
for V in [0.4+0.02*i for i in range(71)]:
    vr=V/VSCALE
    new=interp(vr,bins_raw,temps_raw); true=interp(vr,IAT_VRAW,IAT_TEMP)
    maxerr=max(maxerr,abs(new-true))
print(f"\nMax error vs true IAT curve across 0.4-1.8V (~40-90C band): {maxerr:.2f} C")

# --- write .emubt (two symbols: bins + cal), EMU exact format, ubyte sign-mag ---
out = r"supra/exports/Temperature - Custom temp. cal 1 [C].emubt"
body = (
 f'    <symbol name="customTemp1CalBins" storage="ubyte" width="10" height="1" data="{bins_hex}"/>\n'
 f'    <symbol name="customTemp1Cal" storage="ubyte" width="10" height="1" data="{temps_hex}"/>'
)
text = ('<?xml version="1.0" encoding="UTF-8"?>\n<project version="1.0">\n'
        '  <tables>\n'+body+'\n  </tables>\n</project>\n')
with open(out,"w",encoding="utf-8",newline="\n") as f: f.write(text)
print(f"\n[SAVED] {out}")
print(f"  customTemp1CalBins data = {bins_hex}")
print(f"  customTemp1Cal     data = {temps_hex}")
