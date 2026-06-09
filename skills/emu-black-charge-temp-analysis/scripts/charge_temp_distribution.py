#!/usr/bin/env python3
"""Charge-temp / Pre-IC distribution summary from EMU Black CSV logs.

For each log, over running + no-boost samples (RPM > 400, MAP < 100 kPa), print
min / p05 / median / mean / p95 / max for IAT, Pre-IC temperature, Charge temp,
and CLT, plus the Pre-IC sensor dropout rate (<= 2 C) and an idle subset
(RPM < 1500, MAP < 60).

Generalized from the original date-pinned `analyze_apr8.py`: pass any number of
log files as arguments instead of editing a hardcoded list.

Usage:
    python charge_temp_distribution.py LOG.csv [LOG2.csv ...] [--ambient C]

Reads EMU semicolon-delimited CSV exports. Channel names must match the export
(RPM, MAP, IAT, "Pre IC temperature", "Charge temp", CLT). --ambient is used for
the printed label only.
"""
import csv
import os
import argparse

WANT = ["RPM", "MAP", "IAT", "Pre IC temperature", "Charge temp", "CLT"]
OPT = ["IAT", "Pre IC temperature", "Charge temp", "CLT"]


def parse(path):
    rows = []
    with open(path, newline="") as f:
        r = csv.reader(f, delimiter=";")
        hdr = [h.strip() for h in next(r)]
        idx = {n: i for i, n in enumerate(hdr)}
        col = {w: idx.get(w) for w in WANT}
        for line in r:
            try:
                rpm = float(line[col["RPM"]])
                mp = float(line[col["MAP"]])
            except (ValueError, IndexError, TypeError):
                continue
            if rpm <= 400:
                continue
            rec = {"rpm": rpm, "map": mp}
            for w in OPT:
                ci = col[w]
                try:
                    rec[w] = float(line[ci]) if ci is not None else None
                except (ValueError, IndexError):
                    rec[w] = None
            rows.append(rec)
    return rows


def dist(v):
    v = [x for x in v if x is not None]
    if not v:
        return "n/a"
    v = sorted(v)
    n = len(v)
    return (f"min={v[0]:.0f} p05={v[int(.05*(n-1))]:.0f} med={v[n//2]:.0f} "
            f"mean={sum(v)/n:.1f} p95={v[int(.95*(n-1))]:.0f} max={v[-1]:.0f}")


def summarize(label, path, ambient=None):
    rows = parse(path)
    nb = [r for r in rows if r["map"] < 100]
    pre = [r["Pre IC temperature"] for r in nb]
    amb = f"  (ambient {ambient:.0f}C)" if ambient is not None else ""
    print("=" * 78)
    print(f"{label}{amb}")
    print("=" * 78)
    n = len(pre) or 1
    zeros = sum(1 for x in pre if x is not None and x <= 2)
    print(f"  no-boost samples={len(nb)}  Pre-IC<=2C dropouts={zeros} ({100*zeros/n:.1f}%)")
    print(f"  IAT      : {dist([r['IAT'] for r in nb])}")
    print(f"  Pre-IC   : {dist(pre)}   (raw, incl dropouts)")
    print(f"  Pre-IC>2 : {dist([x for x in pre if x and x > 2])}")
    print(f"  Charge   : {dist([r['Charge temp'] for r in nb])}")
    print(f"  CLT      : {dist([r['CLT'] for r in nb])}")
    idle = [r for r in nb if r["rpm"] < 1500 and r["map"] < 60]
    print(f"  -- idle (n={len(idle)}):")
    print(f"     IAT   : {dist([r['IAT'] for r in idle])}")
    print(f"     Pre-IC: {dist([r['Pre IC temperature'] for r in idle if r['Pre IC temperature'] and r['Pre IC temperature'] > 2])}")
    print(f"     Charge: {dist([r['Charge temp'] for r in idle])}")
    print()


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("logs", nargs="+", help="EMU semicolon-delimited CSV log file(s)")
    ap.add_argument("--ambient", type=float, default=None,
                    help="ambient temp (C), for the printed label only")
    a = ap.parse_args()
    for p in a.logs:
        summarize(os.path.basename(p), p, a.ambient)


if __name__ == "__main__":
    main()
