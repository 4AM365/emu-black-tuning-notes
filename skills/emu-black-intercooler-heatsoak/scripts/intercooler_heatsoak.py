#!/usr/bin/env python3
"""Compare charge-temp / intercooler heat-soak ACROSS EMU Black logs, normalized
to ambient.

For each log, over running no-boost samples (RPM>400, MAP<100 kPa), compute mean
IAT, Pre-IC, Post-IC, Charge temp, Ambient and CLT, then the ambient-normalized
deltas that actually compare across different days/conditions:

  PreIC - amb : compressor-bay air rise above ambient (the cleanest heat-soak signal)
  Chg   - amb : total charge-air rise above ambient
  Chg   - PreIC: pickup from compressor outlet to the throttle body

Rows are sorted by ambient so a temperature sweep (cool -> hot day, hood-on vs
hood-off, etc.) reads top to bottom.

Usage:
    python intercooler_heatsoak.py LOG1.csv [LOG2.csv ...] [--ambient C]

Ambient is taken from the logged "Ambient temperature" channel when present;
--ambient supplies a fallback for logs that don't log it (e.g. reduced exports).
"""
import csv
import os
import argparse

WANT = ["RPM", "MAP", "IAT", "Pre IC temperature", "Post IC temperature",
        "Charge temp", "Ambient temperature", "CLT"]


def process(path):
    with open(path, newline="") as f:
        r = csv.reader(f, delimiter=";")
        hdr = [h.strip() for h in next(r)]
        idx = {n: i for i, n in enumerate(hdr)}
        col = {w: idx.get(w) for w in WANT}
        acc = {w: [] for w in WANT}
        for line in r:
            try:
                rpm = float(line[col["RPM"]])
                mp = float(line[col["MAP"]])
            except (ValueError, IndexError, TypeError):
                continue
            if rpm <= 400 or mp >= 100:
                continue
            for w, ci in col.items():
                if ci is None:
                    continue
                try:
                    acc[w].append(float(line[ci]))
                except (ValueError, IndexError):
                    pass
        return acc


def mean(v, drop_zero=False):
    if drop_zero:
        v = [x for x in v if x > 2]
    return sum(v) / len(v) if v else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("logs", nargs="+", help="EMU semicolon-delimited CSV logs")
    ap.add_argument("--ambient", type=float, default=None,
                    help="fallback ambient (C) for logs missing the Ambient channel")
    a = ap.parse_args()

    res = []
    for path in a.logs:
        acc = process(path)
        amb = mean(acc["Ambient temperature"]) or a.ambient
        res.append(dict(
            label=os.path.basename(path), amb=amb,
            iat=mean(acc["IAT"]), preic=mean(acc["Pre IC temperature"], drop_zero=True),
            post=mean(acc["Post IC temperature"]), chg=mean(acc["Charge temp"]),
            clt=mean(acc["CLT"]),
            n=len([x for x in acc["Pre IC temperature"] if x > 2])))

    res.sort(key=lambda r: (r["amb"] is None, r["amb"] or 0))
    print("MAP<100 (no boost), engine running. Ambient = logged channel or --ambient.\n")
    h = (f"{'log':24s}{'ambC':>6s}{'IAT':>6s}{'PreIC':>7s}{'PostIC':>7s}{'Charge':>7s}"
         f"{'CLT':>6s} | {'PreIC-amb':>10s}{'Chg-amb':>9s}{'Chg-PreIC':>10s}")
    print(h)
    print("-" * len(h))

    def g(x):
        return f"{x:.1f}" if x is not None else "  -"

    def s(x):
        return f"{x:+.1f}" if x is not None else "-"

    for r in res:
        pia = (r["preic"] - r["amb"]) if (r["preic"] and r["amb"]) else None
        cma = (r["chg"] - r["amb"]) if (r["chg"] and r["amb"]) else None
        cmp_ = (r["chg"] - r["preic"]) if (r["chg"] and r["preic"]) else None
        print(f"{r['label'][:24]:24s}{g(r['amb']):>6s}{g(r['iat']):>6s}{g(r['preic']):>7s}"
              f"{g(r['post']):>7s}{g(r['chg']):>7s}{g(r['clt']):>6s} | "
              f"{s(pia):>10s}{s(cma):>9s}{s(cmp_):>10s}")
    print("\nPre-IC sample counts (zeros dropped):")
    for r in res:
        print(f"  {r['label'][:24]:24s} n={r['n']}")


if __name__ == "__main__":
    main()
