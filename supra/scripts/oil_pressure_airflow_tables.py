"""Oil-pressure-sliced idle-airflow-requirement tables from EMU Black CSV logs.

For each of 5 oil-pressure bins (2/3/4/5/6 bar, nearest-bin assignment), builds
an idleActiveAirflow-shaped table: rows = idle target RPM axis
(1000/1100/1200/1375/1500), cols = CLT axis (0/15/30/45/60/75/96/105), cell =
median TOTAL commanded idle airflow (%) -- i.e. `Idle air %`, the sum of base
+ custom corr. + coolant-fan corr. + PID -- from held-idle samples whose oil
pressure lands in that bin. This is the requirement surface Result 8's
warmup-locus back-calc used, sliced a new way: fix oil pressure, read off
airflow vs (RPM, CLT) directly, instead of fixing CLT and reading off airflow
vs (RPM, pressure).

Two gating modes, chosen per-log by which channels are present. In BOTH modes
the RPM axis value binned into the table is ACTUAL RPM, never Idle target --
Idle target is used only as a gating/confirmation signal. This matches this
project's established convention (oil_viscosity_idle_airflow.md Results 5-6):
oil pressure is generated at the live RPM (P ~ mu*N), so pairing a pressure
reading with anything but the actual instantaneous RPM decouples the cell
from the physical quantity actually driving it.
  - "target"  (Idle state + Idle target both logged): the canonical stable-
    idle mask -- Idle state==2, |RPM-target|<50, TPS<15, PPS<3, driven-axle
    speed<2 (each condition applied only if its channel exists in this log),
    plus a rolling-window (2 s) RPM std < RPM_STD_MAX.
  - "proxy"   (no Idle state/target -- reduced-channel exports): RPM in
    [700,1700], MAP in [20,55] kPa (idle-load confirmation, used in place of
    the missing TPS/PPS gates), tighter rolling RPM std < PROXY_RPM_STD_MAX
    (no state confirmation, so lean stricter).

  The stability statistic is raw RPM std over a rolling ~2 s window, NOT
  d(RPM)/dt -- at this ECU's 25 Hz log rate the derivative is dominated by
  single-sample RPM quantization (a 4-8 RPM step over 0.04 s already reads as
  ~100-200 RPM/s), so a d/dt-based threshold rejects nearly all real held
  idle. Calibrated empirically against confirmed Idle-state==2 samples in
  20260613_1141.csv: rolling RPM std runs a 16.4 median / 31.7 p75 RPM there,
  so RPM_STD_MAX=25 keeps the bulk of genuine holds without a d/dt rescale.

Oil pressure status (1=OK) is gated when the channel is present; otherwise a
plausibility floor (>0.3 bar, drops cranking/prime transients) substitutes,
consistent with the sensor's fleet-wide reliability (see notes/oil_pressure.md).

Outputs (under --out-dir):
  oil_press_<N>bar_table.md   -- 5 files, one per oil-pressure bin
  oil_press_<N>bar_n.md       -- matching sample-count grids
  oil_press_points.csv        -- every binned sample, for audit
  oil_press_log_summary.csv   -- per-log row counts, mask mode, oil-pressure range

Usage:
  python oil_pressure_airflow_tables.py --out-dir DIR log1.csv log2.csv ...
"""
import argparse
import sys
import numpy as np
import pandas as pd

RPM_BINS = [1000, 1100, 1200, 1375, 1500]
CLT_BINS = [0, 15, 30, 45, 60, 75, 96, 105]
OP_BINS = [2, 2.5, 3, 4, 5, 6]

MIN_CELL_N = 15
ROLL_SECONDS = 2.0
RPM_STD_MAX = 25.0         # target mode; calibrated vs confirmed Idle-state==2 holds (see module docstring)
PROXY_RPM_STD_MAX = 20.0   # proxy mode: no Idle state to confirm active idle, lean stricter
PROXY_MAP_RANGE = (20, 55) # kPa; idle-load confirmation in place of missing TPS/PPS gates
OP_MIN_PLAUSIBLE = 0.3     # bar; drops oil-pump-prime transients when no status channel

ALL_WANTED = ["TIME", "RPM", "MAP", "CLT", "Engine oil pressure", "Engine oil pressure status",
              "Idle air %", "Idle state", "Idle target", "TPS", "PPS", "Driven axle speed"]


def nearest_bin_idx(values, bins):
    return np.abs(np.subtract.outer(values, np.array(bins, dtype=float))).argmin(axis=1)


def load_log(path):
    hdr = pd.read_csv(path, sep=";", nrows=0).columns.str.strip().tolist()
    required = ["TIME", "RPM", "CLT", "Engine oil pressure", "Idle air %"]
    missing = [c for c in required if c not in hdr]
    if missing:
        return None, f"missing required channels: {missing}"
    use_orig = [c for c in hdr if c.strip() in ALL_WANTED]
    df = pd.read_csv(path, sep=";", usecols=use_orig)
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=required)
    if df.empty:
        return None, "no data rows"
    return df, None


def rolling_rpm_std(df):
    dt = df["TIME"].diff()
    med_dt = dt.median()
    if not np.isfinite(med_dt) or med_dt <= 0:
        med_dt = 0.04
    window = max(5, int(round(ROLL_SECONDS / med_dt)))
    return df["RPM"].rolling(window, center=True, min_periods=max(3, window // 3)).std()


def process_log(path, tag):
    df, err = load_log(path)
    if err:
        print(f"SKIP {tag}: {err}")
        return None, None
    cols = set(df.columns)
    has_state_target = {"Idle state", "Idle target"} <= cols

    stability = rolling_rpm_std(df)

    if has_state_target:
        mode = "target"
        mask = (df["Idle state"] == 2) & ((df["RPM"] - df["Idle target"]).abs() < 50)
        mask &= stability < RPM_STD_MAX
        if "TPS" in cols:
            mask &= df["TPS"] < 15
        if "PPS" in cols:
            mask &= df["PPS"] < 3
        if "Driven axle speed" in cols:
            mask &= df["Driven axle speed"] < 2
        rpm_axis_val = df["RPM"]  # actual RPM, not Idle target -- see module docstring
    else:
        mode = "proxy"
        mask = df["RPM"].between(700, 1700) & (stability < PROXY_RPM_STD_MAX)
        if "MAP" in cols:
            mask &= df["MAP"].between(*PROXY_MAP_RANGE)
        rpm_axis_val = df["RPM"]

    if "Engine oil pressure status" in cols:
        mask &= df["Engine oil pressure status"] == 1
    else:
        mask &= df["Engine oil pressure"] > OP_MIN_PLAUSIBLE

    sub = df.loc[mask, ["CLT", "Engine oil pressure", "Idle air %"]].copy()
    sub["rpm_axis"] = rpm_axis_val[mask]
    sub = sub.dropna()

    summary = {
        "log": tag, "mode": mode, "rows_total": len(df), "rows_kept": len(sub),
        "op_min": df["Engine oil pressure"].min(), "op_max": df["Engine oil pressure"].max(),
    }
    if sub.empty:
        print(f"EMPTY {tag}: mode={mode}, 0/{len(df)} rows survive the mask")
        return None, summary

    sub["log"] = tag
    sub["mode"] = mode
    print(f"{tag}: mode={mode}, {len(sub)}/{len(df)} rows kept, "
          f"OP range {df['Engine oil pressure'].min():.2f}-{df['Engine oil pressure'].max():.2f} bar")
    return sub, summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--subtract", type=float, default=0.0,
                     help="constant subtracted from every displayed cell (e.g. the +13 fan offset)")
    a = ap.parse_args()

    frames, summaries = [], []
    for path in a.logs:
        tag = path.replace("\\", "/").split("/")[-1]
        sub, summ = process_log(path, tag)
        if summ is not None:
            summaries.append(summ)
        if sub is not None:
            frames.append(sub)

    if not frames:
        print("\nNo logs produced usable samples -- no tables written.")
        sys.exit(1)

    pts = pd.concat(frames, ignore_index=True)
    pts["i_rpm"] = nearest_bin_idx(pts["rpm_axis"].to_numpy(), RPM_BINS)
    pts["i_clt"] = nearest_bin_idx(pts["CLT"].to_numpy(), CLT_BINS)
    pts["i_op"] = nearest_bin_idx(pts["Engine oil pressure"].to_numpy(), OP_BINS)

    pts.to_csv(f"{a.out_dir}/oil_press_points.csv", index=False)
    pd.DataFrame(summaries).to_csv(f"{a.out_dir}/oil_press_log_summary.csv", index=False)
    print(f"\n{len(pts)} total samples across {len(frames)} logs -> oil_press_points.csv")

    for i_op, op_val in enumerate(OP_BINS):
        med = np.full((len(RPM_BINS), len(CLT_BINS)), np.nan)
        cnt = np.zeros_like(med, dtype=int)
        bin_pts = pts[pts["i_op"] == i_op]
        for (ir, ic), g in bin_pts.groupby(["i_rpm", "i_clt"]):
            cnt[ir, ic] = len(g)
            if len(g) >= MIN_CELL_N:
                med[ir, ic] = g["Idle air %"].median()

        rows_md = ["| RPM \\ CLT | " + " | ".join(str(c) for c in CLT_BINS) + " |",
                   "|---" * (len(CLT_BINS) + 1) + "|"]
        n_md = list(rows_md)
        for ir in range(len(RPM_BINS) - 1, -1, -1):
            cells = ["" if np.isnan(med[ir, ic]) else f"{med[ir, ic] - a.subtract:.1f} ({cnt[ir, ic]})"
                     for ic in range(len(CLT_BINS))]
            rows_md.append(f"| **{RPM_BINS[ir]}** | " + " | ".join(cells) + " |")
            ncells = [str(cnt[ir, ic]) if cnt[ir, ic] else "" for ic in range(len(CLT_BINS))]
            n_md.append(f"| **{RPM_BINS[ir]}** | " + " | ".join(ncells) + " |")

        open(f"{a.out_dir}/oil_press_{op_val}bar_table.md", "w").write("\n".join(rows_md) + "\n")
        open(f"{a.out_dir}/oil_press_{op_val}bar_n.md", "w").write("\n".join(n_md) + "\n")
        populated = np.isfinite(med).sum()
        print(f"{op_val} bar: {populated}/{med.size} cells populated (n>={MIN_CELL_N}), "
              f"{len(bin_pts)} samples in bin")


if __name__ == "__main__":
    main()
