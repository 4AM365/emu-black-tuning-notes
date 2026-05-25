"""Analyze a VVT cam-override sweep log: identify cam holds at steady operating
points, compute mean MAP/EGT per hold, rank cam positions.

Usage:
  python analyze_sweep.py --log <file.csv> [--cell-rpm RPM --cell-map MAP] \
                          [--cell-tolerance dRPM dMAP]
                          [--out-json <file.json>]

Without --cell-rpm/--cell-map the script auto-detects all (RPM, MAP) bins
visited at cam holds and reports each separately.
"""
import argparse, sys, io, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("Requires pandas+numpy"); sys.exit(1)

CAM_TARGET_CHANNEL_CANDIDATES = [
    "VVT CAM1 angle target",
    "VVT CAM1 target",
    "VVT CAM1 override",
]
CAM_ACTUAL_CHANNEL_CANDIDATES = [
    "VVT CAM1 angle",
]

def find_channel(df, candidates):
    for c in candidates:
        if c in df.columns: return c
    return None

def find_holds(df, cam_col, min_seconds=8.0, sample_hz=25, tolerance=0.5):
    """Find segments where cam_col was within `tolerance` of a constant value
    for at least min_seconds. Returns list of (start_idx, end_idx, value)."""
    holds = []
    n = len(df)
    i = 0
    min_samples = int(min_seconds * sample_hz)
    while i < n - min_samples:
        v = df[cam_col].iloc[i]
        j = i
        while j < n and abs(df[cam_col].iloc[j] - v) <= tolerance:
            j += 1
        if (j - i) >= min_samples:
            mean_v = df[cam_col].iloc[i:j].mean()
            holds.append((i, j, mean_v))
        i = max(j, i + 1)
    return holds

def steady_window(sub, channels, max_std=None):
    """Return (start_idx_within_sub, end_idx_within_sub) for the longest stable window."""
    # Simple heuristic: drop first 2 seconds (~50 samples) to let MAP settle
    drop = min(50, len(sub) // 4)
    return drop, len(sub)

def egt_channel(df):
    """Find a usable EGT channel. Prefer per-bank, then per-cylinder summary, then any cylinder."""
    candidates = ["EGT 1", "EGT 2"]  # bank-level
    for c in candidates:
        if c in df.columns: return c
    # First per-cyl
    for n in range(1, 9):
        c = f"EGT cyl {n}"
        if c in df.columns: return c
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    ap.add_argument("--cell-rpm", type=float, default=None,
                    help="Target operating-point RPM; if omitted, auto-detect all visited cells")
    ap.add_argument("--cell-map", type=float, default=None,
                    help="Target operating-point MAP; if omitted, auto-detect")
    ap.add_argument("--cell-tolerance", type=float, nargs=2, default=(200, 5),
                    metavar=("dRPM", "dMAP"), help="Tolerance for matching cell")
    ap.add_argument("--min-hold-seconds", type=float, default=8.0,
                    help="Minimum cam-hold duration to consider (default 8s)")
    ap.add_argument("--cam-tolerance", type=float, default=0.5,
                    help="Cam angle tolerance to call it a 'hold' (default 0.5°)")
    ap.add_argument("--out-json", help="Write structured result for use by propose_table.py")
    args = ap.parse_args()

    df = pd.read_csv(args.log, sep=";", low_memory=False)
    df.columns = df.columns.str.strip()
    df = df.dropna(axis=1, how="all")
    print(f"Loaded {len(df):,} rows ({df['TIME'].iloc[-1]-df['TIME'].iloc[0]:.1f}s)")

    # WBO valid gate — note for the user, but don't block (most VVT signals don't need lambda)
    if "Lambda is valid" in df.columns:
        valid_mask = df["Lambda is valid"] == 1
        if valid_mask.any():
            t_valid = df.loc[valid_mask, "TIME"].iloc[0]
            print(f"WBO valid from t={t_valid:.1f}s")
        else:
            print("⚠ WBO never validated — STFT-based signals will be unusable downstream.")

    cam_col = find_channel(df, CAM_TARGET_CHANNEL_CANDIDATES)
    if cam_col is None:
        print("❌ No VVT cam target channel found.")
        sys.exit(1)
    print(f"Cam target channel: {cam_col}")

    egt_col = egt_channel(df)
    if egt_col:
        print(f"EGT channel: {egt_col}")

    holds = find_holds(df, cam_col, min_seconds=args.min_hold_seconds, tolerance=args.cam_tolerance)
    if not holds:
        print(f"❌ No cam holds ≥ {args.min_hold_seconds}s found.")
        sys.exit(1)
    print(f"Found {len(holds)} cam-hold segments")

    # For each hold, drop the first ~2s for MAP settle and compute stats
    results = []
    for i, j, cam_val in holds:
        sub = df.iloc[i:j]
        s, e = steady_window(sub, [])
        steady = sub.iloc[s:e]
        if len(steady) < 25: continue
        entry = {
            "t_start": float(sub["TIME"].iloc[0]),
            "t_end":   float(sub["TIME"].iloc[-1]),
            "n_samples": int(len(steady)),
            "cam_target": float(cam_val),
            "cam_actual_mean": float(steady["VVT CAM1 angle"].mean()) if "VVT CAM1 angle" in steady.columns else None,
            "rpm_mean": float(steady["RPM"].mean()),
            "rpm_std":  float(steady["RPM"].std()),
            "map_mean": float(steady["MAP"].mean()),
            "map_std":  float(steady["MAP"].std()),
            "tps_mean": float(steady["TPS"].mean()) if "TPS" in steady.columns else None,
            "egt_mean": float(steady[egt_col].mean()) if egt_col else None,
        }
        results.append(entry)

    # If user specified a target cell, filter
    if args.cell_rpm is not None and args.cell_map is not None:
        dr, dm = args.cell_tolerance
        in_cell = [r for r in results
                   if abs(r["rpm_mean"] - args.cell_rpm) <= dr
                   and abs(r["map_mean"] - args.cell_map) <= dm]
        groups = [((args.cell_rpm, args.cell_map), in_cell)]
    else:
        # Auto-group by rounded RPM and MAP
        from collections import defaultdict
        rmap = defaultdict(list)
        for r in results:
            key = (round(r["rpm_mean"] / 500) * 500, round(r["map_mean"] / 10) * 10)
            rmap[key].append(r)
        groups = [(k, sorted(v, key=lambda x: x["cam_target"])) for k, v in sorted(rmap.items())]

    # Report
    print()
    out_groups = []
    for (rpm_bin, map_bin), holds_in_cell in groups:
        if len(holds_in_cell) < 2:
            print(f"Cell (RPM≈{rpm_bin}, MAP≈{map_bin}): only {len(holds_in_cell)} hold(s), skipping")
            continue
        print(f"Cell (RPM≈{rpm_bin}, MAP≈{map_bin}):")
        # Sort by cam target
        holds_in_cell = sorted(holds_in_cell, key=lambda x: x["cam_target"])
        # Best cam = highest MAP (primary), lowest EGT (corroborating)
        best_map = max(holds_in_cell, key=lambda x: x["map_mean"])
        best_egt = min(holds_in_cell, key=lambda x: x["egt_mean"]) if egt_col else None

        # Drift check: are there multiple holds at the same cam target?
        from collections import defaultdict
        by_cam = defaultdict(list)
        for h in holds_in_cell:
            by_cam[round(h["cam_target"])].append(h)
        drift_warnings = []
        for cam, list_h in by_cam.items():
            if len(list_h) > 1:
                map_range = max(h["map_mean"] for h in list_h) - min(h["map_mean"] for h in list_h)
                if map_range > 2.0:
                    drift_warnings.append(f"cam {cam}°: MAP varied {map_range:.1f} kPa across repeats")

        for h in holds_in_cell:
            label = ""
            if h is best_map: label += " ← MAP peak"
            if best_egt and h is best_egt: label += " ← EGT min"
            egt_str = f"  EGT {h['egt_mean']:6.1f}°C" if h['egt_mean'] is not None else ""
            print(f"  Cam {h['cam_target']:5.1f}°: MAP {h['map_mean']:5.1f} kPa "
                  f"(std {h['map_std']:.2f}){egt_str}  n={h['n_samples']}{label}")
        agree = (best_egt is None) or (abs(best_map["cam_target"] - best_egt["cam_target"]) <= 5)
        print(f"  → Best cam (MAP peak): {best_map['cam_target']:.1f}°")
        if best_egt:
            print(f"  → Best cam (EGT min): {best_egt['cam_target']:.1f}°")
            if agree:
                print(f"  → ✓ MAP and EGT agree within 5° — confidence high")
            else:
                print(f"  → ⚠ MAP and EGT disagree by more than 5° — sweep may be noisy or operating "
                      f"point drifted between holds")
        for w in drift_warnings:
            print(f"  ⚠ Drift check: {w}")
        out_groups.append({
            "rpm_bin": rpm_bin, "map_bin": map_bin,
            "best_cam_by_map": best_map["cam_target"],
            "best_cam_by_egt": best_egt["cam_target"] if best_egt else None,
            "agree_within_5deg": agree,
            "holds": holds_in_cell,
        })

    if args.out_json:
        with open(args.out_json, "w") as f:
            json.dump({"log": args.log, "cells": out_groups}, f, indent=2)
        print(f"\nWrote {args.out_json}")

if __name__ == "__main__":
    main()
