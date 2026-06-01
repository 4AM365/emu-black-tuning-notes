"""
Minor anti-jolt smoothing of the autotune-corrected VE tables.
Goal: remove small cell-to-cell roughness (non-monotonic reversals, isolated kinks)
that cause abrupt fuel-dose steps when crossing cells, WITHOUT touching the real
physical features (residual-gas knee on the load axis, VE hump peaking ~5500).

Strategy (deliberately gentle):
  1. one light separable [1,2,1] blur,
  2. cap per-cell movement to +/-CAP so smooth ramps (the knee) barely move,
  3. enforce load-axis monotonic non-decreasing (VE must rise with MAP),
  4. enforce RPM-axis non-decreasing up to the ~5500 peak.
"""
import re
import numpy as np

RPM = np.array([500,842,1184,1526,1868,2211,2553,2895,3237,3579,
                3921,4263,4605,4947,5289,5632,5974,6316,6658,7000])
MAP = np.array([20,35,49,64,79,93,108,123,137,152,167,181,196,211,225,240])
CAP = 0.6                                  # max % a cell may move (keeps it "minor")
peak_idx = int(np.argmin(np.abs(RPM - 5500)))

def grab(path, sym):
    t = open(path, encoding="utf-8", errors="replace").read()
    d = re.search(r'name="%s".*?data="([^"]*)"' % sym, t, re.S).group(1)
    return np.array([int(x, 16) for x in d.split()], float).reshape(20, 16) * 0.1

def blur(a):
    k = np.array([1.0, 2.0, 1.0]); k /= k.sum()
    p = np.vstack([a[:1], a, a[-1:]])
    o = k[0]*p[:-2] + k[1]*p[1:-1] + k[2]*p[2:]
    p = np.hstack([o[:, :1], o, o[:, -1:]])
    return k[0]*p[:, :-2] + k[1]*p[:, 1:-1] + k[2]*p[:, 2:]

def kinks(T):
    d2m = np.zeros_like(T); d2r = np.zeros_like(T)
    d2m[:, 1:-1] = T[:, 2:] - 2*T[:, 1:-1] + T[:, :-2]
    d2r[1:-1, :] = T[2:, :] - 2*T[1:-1, :] + T[:-2, :]
    return np.abs(d2m).max(), np.abs(d2r).max()

def reversals(T):
    rev = 0
    for i in range(20):
        for j in range(1, 16):
            if T[i, j] < T[i, j-1] - 0.05:
                rev += 1
    return rev

jobs = [("ve1_autotune_corrected.emubt", "veTable",  "ve1_autotune_corrected_smoothed.emubt"),
        ("ve2_autotune_corrected.emubt", "veTable2", "ve2_autotune_corrected_smoothed.emubt")]

OUT = r"C:\Code\car-projects\emu-black-tuning-notes\supra\tunes"
import json, subprocess, sys, os
EXPORT = r"C:\Users\WTCra\.claude\skills\emu-black-emubt-export\scripts\export_emubt.py"

for src, sym, outname in jobs:
    B = grab(src, sym)
    F = blur(B)
    F = np.clip(F, B - CAP, B + CAP)                  # cap movement -> stays minor
    # load-axis monotonic non-decreasing (dose rises with MAP)
    for i in range(20):
        for j in range(1, 16):
            if F[i, j] < F[i, j-1]:
                F[i, j] = F[i, j-1]
    # RPM-axis non-decreasing up to peak
    for j in range(16):
        for i in range(1, peak_idx + 1):
            if F[i, j] < F[i-1, j]:
                F[i, j] = F[i-1, j]
    F = np.round(np.clip(F, 0, 409.5), 1)

    km0, kr0 = kinks(B); km1, kr1 = kinks(F)
    print(f"{sym}: max move {np.abs(F-B).max():.1f}%  mean {np.abs(F-B).mean():.2f}%")
    print(f"   MAP kink {km0:.1f}->{km1:.1f}   RPM kink {kr0:.1f}->{kr1:.1f}   "
          f"reversals {reversals(B)}->{reversals(F)}")
    # knee + hump preserved?
    knee = " ".join(f"{x:+.1f}" for x in np.diff(F[2, :8]))      # 1184 rpm, MAP 20..137
    pk = int(RPM[F[:, 4].argmax()])                              # 79 kPa column peak rpm
    print(f"   1184rpm knee deltas: {knee}   (79kPa column peaks at {pk} rpm)")

    raw = np.clip(np.rint(F / 0.1), 0, 4095).astype(int)
    spec = {"out": os.path.join(OUT, outname),
            "symbols": [{"name": sym, "storage": "u12", "width": 16, "height": 20,
                         "scale": 1.0, "values": raw.flatten().tolist()}]}
    sp = os.path.join(OUT, "_spec.json"); json.dump(spec, open(sp, "w"))
    r = subprocess.run([sys.executable, EXPORT, "--json", sp], capture_output=True, text=True)
    print("   " + (r.stdout.strip() or r.stderr.strip())); os.remove(sp)
    print()
