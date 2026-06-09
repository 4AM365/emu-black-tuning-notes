#!/usr/bin/env python3
"""Per-cylinder EGT evenness / health from an EMU Black CSV log.

Detects active EGT channels (CAN EGT 1..8, EGT 1/2), then over warm running
rows where every active probe is firing reports per-cylinder mean / median /
p95 and the mean-to-mean spread — the cylinder-to-cylinder distribution signal.
Also reads back any active per-injector trims (Injector N trim).

A flat, even EGT spread at load is the fingerprint of all cylinders doing the
same thing; a hot cylinder (front-feed manifolds run the rear lean/hot) shows as
a high outlier and usually wants per-cylinder fuel trim.

Usage:
    python egt_analysis.py LOG.csv [--clt 70] [--firing 300] [--state 3]

EMU semicolon-delimited CSV export. Pandas required.
"""
import argparse
import sys

try:
    import pandas as pd
    import numpy as np
except ImportError:
    sys.exit("requires pandas + numpy:  pip install pandas numpy")

EGT_CHANNELS = ["CAN EGT " + str(i) for i in range(1, 9)] + ["EGT 1", "EGT 2"]


def load(path):
    df = pd.read_csv(path, sep=";")
    df.columns = df.columns.str.strip()
    return df


def active_egt(df, min_nonzero=100):
    out = []
    for c in EGT_CHANNELS:
        if c in df.columns and (df[c] != 0).sum() > min_nonzero:
            out.append(c)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("log", help="EMU semicolon-delimited CSV log")
    ap.add_argument("--clt", type=float, default=70, help="warm CLT threshold (C)")
    ap.add_argument("--firing", type=float, default=300, help="EGT 'firing' threshold (C)")
    ap.add_argument("--state", type=int, default=3, help="running ECU State value")
    a = ap.parse_args()

    df = load(a.log)
    n = len(df)
    dur = df["TIME"].iloc[-1] - df["TIME"].iloc[0] if "TIME" in df else float("nan")
    print(f"rows {n}  duration {dur:.1f}s")
    if "ECU State" in df:
        print("ECU State:", dict(df["ECU State"].value_counts()))

    egts = active_egt(df)
    print("\n=== EGT channel activity ===")
    for c in EGT_CHANNELS:
        if c in df.columns:
            v = df[c]
            print(f"  {c}: mean {v.mean():.0f}  max {v.max():.0f}  nonzero {(v != 0).sum()}")
    print("active EGT:", egts or "(none)")
    if not egts:
        return

    run = df.copy()
    if "ECU State" in df:
        run = run[run["ECU State"] == a.state]
    if "CLT" in df:
        run = run[run["CLT"] > a.clt]
    print(f"\n=== warm running rows: {len(run)} ===")

    firing = run[run[egts].gt(a.firing).all(axis=1)]
    print(f"rows with all EGT>{a.firing:.0f}: {len(firing)}")
    if len(firing):
        print("\n=== EGT evenness (warm, all firing) ===")
        means = {}
        for c in egts:
            means[c] = firing[c].mean()
            print(f"  {c}: mean {firing[c].mean():.0f}  median {firing[c].median():.0f}  p95 {firing[c].quantile(.95):.0f}")
        mv = np.array(list(means.values()))
        hot = max(means, key=means.get)
        print(f"  spread mean-to-mean: {mv.max() - mv.min():.0f} C  (min {mv.min():.0f} / max {mv.max():.0f}) — hottest: {hot}")

    print("\n=== per-injector trims (warm running) ===")
    any_trim = False
    for i in range(1, 9):
        c = "Injector %d trim" % i
        if c in run and (run[c] != 0).any():
            any_trim = True
            v = run[c]
            print(f"  {c}: mean {v.mean():.2f}  min {v.min():.2f}  max {v.max():.2f}")
    if not any_trim:
        print("  (no active injector trims)")


if __name__ == "__main__":
    main()
