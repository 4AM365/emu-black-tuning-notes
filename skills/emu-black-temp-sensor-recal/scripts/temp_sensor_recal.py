#!/usr/bin/env python3
"""Re-calibrate an EMU Black custom temperature sensor by copying a known-good
sensor's curve onto it, and emit the corrected cal as an importable .emubt.

Common case: a custom-temp input (e.g. Pre-IC on Custom temp cal 1) is running the
WRONG voltage->temperature curve, so it reads systematically off. If that sensor is
the *same type* as one already calibrated correctly in the tune (e.g. the IAT
sensor), the fix is to resample the correct curve onto the custom sensor's N cal
nodes. Error is zero at the chosen nodes and tiny in between across the operating
band.

Inputs:
  --ref FILE        reference (correct) curve: CSV rows "voltage_raw,temp_C"
                    (voltage_raw is the ubyte node, display V = raw*5/255)
  --bins N          number of output cal nodes (default 10)
  --keep "i,j,..."  optional: explicit indices of --ref nodes to keep (else auto:
                    drop extreme/low-curvature ends, keep band-dense middle)
  --symbol NAME     cal symbol (default customTemp1Cal)
  --bins-symbol NAME  cal-bins symbol (default customTemp1CalBins)
  --out FILE        output .emubt path
  --wrong FILE      optional: the WRONG curve currently applied (same CSV format);
                    prints old-vs-new and the logged-value correction it implies

Usage:
  python temp_sensor_recal.py --ref iat_curve.csv --out "Custom temp cal 1.emubt"

Standard library only. .emubt temps are ubyte sign-magnitude hex (handles negatives).
"""
import argparse
import csv
import sys

VSCALE = 5 / 255


def read_curve(path):
    vr, t = [], []
    with open(path, newline="") as f:
        for row in csv.reader(f):
            row = [c.strip() for c in row if c.strip() != ""]
            if not row or row[0].lower().startswith("volt"):
                continue
            vr.append(int(float(row[0])))
            t.append(float(row[1]))
    pairs = sorted(zip(vr, t))
    return [p[0] for p in pairs], [p[1] for p in pairs]


def interp(vraw, xs, ys):
    if vraw <= xs[0]:
        return ys[0]
    if vraw >= xs[-1]:
        return ys[-1]
    for i in range(len(xs) - 1):
        if xs[i] <= vraw <= xs[i + 1]:
            f = (vraw - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + f * (ys[i + 1] - ys[i])


def fhex(v):
    """EMU ubyte sign-magnitude hex: negatives set the high bit (|v| | 0x80)."""
    v = int(round(v))
    if v < 0:
        v = (abs(v) & 0x7F) | 0x80
    return format(v & 0xFF, "X")


def pick_nodes(vr, n):
    if n >= len(vr):
        return list(range(len(vr)))
    # keep endpoints, spread the rest evenly by index
    idx = [round(i * (len(vr) - 1) / (n - 1)) for i in range(n)]
    return sorted(set(idx))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ref", required=True, help="correct curve CSV: voltage_raw,temp_C")
    ap.add_argument("--bins", type=int, default=10)
    ap.add_argument("--keep", default=None, help="comma indices of --ref nodes to keep")
    ap.add_argument("--symbol", default="customTemp1Cal")
    ap.add_argument("--bins-symbol", dest="bins_symbol", default="customTemp1CalBins")
    ap.add_argument("--out", required=True)
    ap.add_argument("--wrong", default=None, help="wrong curve CSV (optional report)")
    a = ap.parse_args()

    vr, t = read_curve(a.ref)
    if a.keep:
        idx = [int(x) for x in a.keep.split(",")]
    else:
        idx = pick_nodes(vr, a.bins)
    bins_raw = [vr[i] for i in idx]
    temps = [t[i] for i in idx]

    print(f"Resampled {a.symbol} from the reference curve ({len(idx)} of {len(vr)} nodes)\n")
    wr = read_curve(a.wrong) if a.wrong else None
    hdr = f"{'V':>6} | {'NEW C':>7} | {'true@V':>7}" + ("  | OLD wrong C" if wr else "")
    print(hdr)
    print("-" * len(hdr))
    for raw, tn in zip(bins_raw, temps):
        V = raw * VSCALE
        true = interp(raw, vr, t)
        line = f"{V:6.2f} | {tn:7.1f} | {true:7.1f}"
        if wr:
            line += f"  | {interp(raw, wr[0], wr[1]):8.1f}"
        print(line)

    # operating-band error (0.4-1.8 V ~ 40-90 C for typical NTC IAT)
    maxerr = 0.0
    V = 0.4
    while V <= 1.8:
        raw = V / VSCALE
        maxerr = max(maxerr, abs(interp(raw, bins_raw, temps) - interp(raw, vr, t)))
        V += 0.02
    print(f"\nMax error vs reference across 0.4-1.8 V: {maxerr:.2f} C")

    bins_hex = " ".join(fhex(v) for v in bins_raw) + " "
    temps_hex = " ".join(fhex(v) for v in temps) + " "
    body = (f'    <symbol name="{a.bins_symbol}" storage="ubyte" width="{len(idx)}" height="1" data="{bins_hex}"/>\n'
            f'    <symbol name="{a.symbol}" storage="ubyte" width="{len(idx)}" height="1" data="{temps_hex}"/>')
    text = ('<?xml version="1.0" encoding="UTF-8"?>\n<project version="1.0">\n'
            '  <tables>\n' + body + '\n  </tables>\n</project>\n')
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"\n[SAVED] {a.out}")
    print(f"  {a.bins_symbol} data = {bins_hex}")
    print(f"  {a.symbol} data = {temps_hex}")
    if wr:
        print("\nTo correct values already logged on the wrong curve: invert wrong (T->V),"
              "\nthen apply the reference (V->T).")


if __name__ == "__main__":
    main()
