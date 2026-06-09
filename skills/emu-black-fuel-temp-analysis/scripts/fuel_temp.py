#!/usr/bin/env python3
"""Fuel-temperature summary from EMU Black CSV logs.

Reads the "Fuel Temperature" channel and reports start / min / mean / max / end
for each log. The start-of-log value is the best cold anchor (≈ ambient/tank temp
before the pump and engine bay heat the rail); the rise to the end shows heat-soak.
Useful as an ambient proxy when a log lacks an Ambient channel, and for sizing
fuel-temp density/vapor-pressure compensation.

Usage:
    python fuel_temp.py LOG1.csv [LOG2.csv ...]

Skips sensor-fault rows (<= -30 C). Standard library only.
"""
import csv
import os
import sys


def F(c):
    return c * 9 / 5 + 32


def probe(path):
    ft = []
    first = tfirst = None
    with open(path, newline="") as f:
        r = csv.reader(f, delimiter=";")
        h = [x.strip() for x in next(r)]
        ix = {n: i for i, n in enumerate(h)}
        if "Fuel Temperature" not in ix:
            return None
        fi, ti = ix["Fuel Temperature"], ix.get("TIME")
        for ln in r:
            try:
                v = float(ln[fi])
                t = float(ln[ti]) if ti is not None else 0.0
            except (ValueError, IndexError):
                continue
            if v <= -30:
                continue
            ft.append(v)
            if first is None:
                first, tfirst = v, t
    if not ft:
        return None
    fs = sorted(ft)
    n = len(fs)
    return dict(first=first, min=fs[0], med=fs[n // 2], mean=sum(ft) / n,
                max=fs[-1], end=ft[-1], n=n)


def main():
    logs = sys.argv[1:]
    if not logs:
        sys.exit("usage: python fuel_temp.py LOG1.csv [LOG2.csv ...]")
    print("FUEL TEMPERATURE  (start = best cold anchor; rises with heat-soak)\n")
    print(f"{'log':24s}{'start':>9s}{'min':>7s}{'mean':>7s}{'max':>7s}{'end':>7s}")
    print("-" * 61)
    for path in logs:
        lbl = os.path.basename(path)[:24]
        p = probe(path)
        if p is None:
            print(f"{lbl:24s}  (no Fuel Temperature channel)")
            continue
        print(f"{lbl:24s}{p['first']:6.0f}C{F(p['first']):3.0f}F{p['min']:6.0f}C"
              f"{p['mean']:6.0f}C{p['max']:6.0f}C{p['end']:6.0f}C   (n={p['n']})")


if __name__ == "__main__":
    main()
