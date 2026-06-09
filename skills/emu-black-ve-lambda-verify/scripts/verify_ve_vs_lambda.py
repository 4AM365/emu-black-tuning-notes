#!/usr/bin/env python3
"""Verify VE-table shape against lambda targets via the veTable x lambda_target product test.

In an EMU fuel model where lambdaTable is a reference / closed-loop target only (NOT
applied as a fuel multiplier), the veTable IS the dose and must carry the lambda
enrichment by hand. Test:

    air_VE_proxy(map, rpm) = veTable(map, rpm) * lambda_target(map, rpm)

A correct VE shape makes this a SMOOTH surface across MAP at each RPM: rises out of the
idle/vacuum region, peaks near the torque-MAP band, then tapers gently into boost. A
DIP or step at the boost-enrichment knee (where lambda_target starts dropping) means the
veTable did NOT get the extra fuel the lambda targets demand -- a shape mismatch.

Reads the tables from a tune XML export (.xml.emub3). Run once per fuel table (pump:
veTable x lambdaTable; ethanol: veTable2 x lambdaTable2).

Usage:
  python verify_ve_vs_lambda.py TUNE.xml.emub3
      [--ve veTable] [--lambda lambdaTable]
      [--map-bins mapBins] [--rpm-bins rpmBins]
      [--lambda-map-bins mapBinsL8] [--lambda-rpm-bins rpmBins10]
      [--ve-scale 0.1] [--lambda-scale 0.01]
"""
import re
import sys
import argparse


def h2i(s):
    return [int(t, 16) for t in s.split()]


def sym(txt, name):
    m = re.search(rf'name="{re.escape(name)}"[^>]*data="([^"]+)"', txt)
    if not m:
        sys.exit(f"symbol {name} not found in tune")
    return h2i(m.group(1))


def grid(flat, w):
    return [flat[i * w:(i + 1) * w] for i in range(len(flat) // w)]


def interp1(x, xs, ys):
    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            t = (x - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + t * (ys[i + 1] - ys[i])
    return ys[-1]


def lam_at(LAM, mapv, rpmv, lmap, lrpm, scale):
    row_vals = [interp1(mapv, lmap, LAM[r]) for r in range(len(lrpm))]
    return interp1(rpmv, lrpm, row_vals) * scale


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("tune", help="tune XML export (.xml.emub3)")
    ap.add_argument("--ve", default="veTable")
    ap.add_argument("--lambda", dest="lam", default="lambdaTable")
    ap.add_argument("--map-bins", dest="mapb", default="mapBins")
    ap.add_argument("--rpm-bins", dest="rpmb", default="rpmBins")
    ap.add_argument("--lambda-map-bins", dest="lmapb", default="mapBinsL8")
    ap.add_argument("--lambda-rpm-bins", dest="lrpmb", default="rpmBins10")
    ap.add_argument("--ve-scale", type=float, default=0.1)
    ap.add_argument("--lambda-scale", type=float, default=0.01)
    a = ap.parse_args()

    txt = open(a.tune, "r", encoding="utf-8", errors="replace").read()
    mapBins = sym(txt, a.mapb)
    rpmBins = sym(txt, a.rpmb)
    lmap = sym(txt, a.lmapb)
    lrpm = sym(txt, a.lrpmb)
    VE = grid(sym(txt, a.ve), len(mapBins))
    LAM = grid(sym(txt, a.lam), len(lmap))

    print(f"=== Product test: {a.ve} x {a.lam} (air-VE proxy) across MAP at each RPM ===")
    print("Smooth monotonic rise then plateau is healthy; a DIP at the boost knee = mismatch.\n")
    print("RPM   " + " ".join(f"{m:>4}" for m in mapBins) + "   (MAP kPa)")
    step = max(1, len(rpmBins) // 7)
    for ri in range(0, len(rpmBins), step):
        rpmv = rpmBins[ri]
        prod = [VE[ri][ci] * a.ve_scale * lam_at(LAM, mapv, rpmv, lmap, lrpm, a.lambda_scale)
                for ci, mapv in enumerate(mapBins)]
        print(f"{rpmv:>5} " + " ".join(f"{p:4.0f}" for p in prod))


if __name__ == "__main__":
    main()
