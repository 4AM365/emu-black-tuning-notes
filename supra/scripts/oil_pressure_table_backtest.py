"""Per-sample backtest of Active airflow + fan + custom correction against logged Idle air %.

Uses bilinear interpolation on both live tables (not nearest-bin snapping) so a
sample at e.g. 5.3 bar gets the correct interpolated correction between the 5
and 6 bar columns, matching how the ECU itself evaluates the table. Compares
predicted = base(RPM,CLT) + fan_term + corr(RPM,OP) against the logged
`Idle air %` sample by sample, gated only on Idle state==2 (no RPM-vs-target
or nearest-bin aggregation) so nothing is lost to coarse binning.

Table values are hardcoded from the 2026-08-05 screenshot (Active state air
flow [%] and Custom air flow correction [%] live tables) -- update BASE_TABLE
/ CORR_TABLE here if the tune changes.

Usage:
  python oil_pressure_table_backtest.py log1.csv [log2.csv ...] [--merge-fan-from PATH]
"""
import argparse
import numpy as np
import pandas as pd
from scipy.interpolate import RegularGridInterpolator

RPM_AXIS = [1000, 1100, 1200, 1375, 1500]
CLT_AXIS = [0, 15, 30, 45, 60, 75, 96, 105]
OP_AXIS = [2, 3, 4, 5, 6]

# rows ordered to match RPM_AXIS (1000..1500), cols ordered to match CLT_AXIS (0..105)
BASE_TABLE = np.array([
    [65.0, 54.0, 40.0, 28.5, 24.5, 20.5, 18.5, 18.5],   # 1000
    [74.5, 62.0, 46.0, 35.5, 30.5, 25.5, 21.0, 21.0],   # 1100
    [81.0, 67.0, 52.5, 42.5, 36.0, 31.0, 24.0, 24.0],   # 1200
    [86.0, 72.0, 59.0, 50.5, 44.0, 39.0, 30.0, 30.0],   # 1375
    [87.5, 75.0, 62.0, 52.0, 47.5, 43.0, 34.5, 34.5],   # 1500
])

# rows ordered to match RPM_AXIS (1000..1500), cols ordered to match OP_AXIS (2..6)
CORR_TABLE = np.array([
    [-6, 0, 16, 39, 51],   # 1000
    [-5, 0, 12, 31, 42],   # 1100
    [-6, 0, 9, 26, 35],    # 1200
    [-6, 0, 2, 10, 16],    # 1375
    [-3, 0, 0, 3, 4],      # 1500
])

base_interp = RegularGridInterpolator((RPM_AXIS, CLT_AXIS), BASE_TABLE,
                                       bounds_error=False, fill_value=None)
corr_interp = RegularGridInterpolator((RPM_AXIS, OP_AXIS), CORR_TABLE,
                                       bounds_error=False, fill_value=None)


def load(path):
    hdr = pd.read_csv(path, sep=";", nrows=0).columns.str.strip().tolist()
    need = ["TIME", "RPM", "CLT", "Engine oil pressure", "Idle air %", "Idle state"]
    missing = [c for c in need if c not in hdr]
    if missing:
        return None, f"missing {missing}"
    want = [c for c in hdr if c.strip() in need + ["Coolant fan"]]
    df = pd.read_csv(path, sep=";", usecols=want)
    df.columns = df.columns.str.strip()
    return df, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+")
    ap.add_argument("--merge-fan-from", help="path to a same-session log carrying Coolant fan, merged on TIME")
    a = ap.parse_args()

    frames = []
    for path in a.logs:
        tag = path.replace("\\", "/").split("/")[-1]
        df, err = load(path)
        if err:
            print(f"SKIP {tag}: {err}")
            continue
        if "Coolant fan" not in df.columns and a.merge_fan_from:
            fan_df, ferr = load(a.merge_fan_from)
            if ferr is None and "Coolant fan" in fan_df.columns:
                df = pd.merge_asof(df.sort_values("TIME"), fan_df[["TIME", "Coolant fan"]].sort_values("TIME"),
                                    on="TIME", direction="nearest", tolerance=0.05)
                print(f"{tag}: merged Coolant fan from {a.merge_fan_from.split(chr(92))[-1]}")
        df = df[df["Idle state"] == 2].dropna(subset=["RPM", "CLT", "Engine oil pressure", "Idle air %"])
        if df.empty:
            print(f"EMPTY {tag}: no Idle state==2 samples")
            continue
        if "Coolant fan" in df.columns:
            fan_term = 13.0 * df["Coolant fan"].fillna(0)
            fan_src = "logged"
        else:
            fan_term = np.where(df["CLT"] >= 70, 13.0, 0.0)
            fan_src = "CLT>=70 assumption"
        rpm_c = df["RPM"].clip(RPM_AXIS[0], RPM_AXIS[-1])
        clt_c = df["CLT"].clip(CLT_AXIS[0], CLT_AXIS[-1])
        op_c = df["Engine oil pressure"].clip(OP_AXIS[0], OP_AXIS[-1])
        base = base_interp(np.column_stack([rpm_c, clt_c]))
        corr = corr_interp(np.column_stack([rpm_c, op_c]))
        predicted = base + fan_term + corr
        resid = df["Idle air %"].to_numpy() - predicted
        print(f"{tag}: n={len(df)}, fan={fan_src}, residual (logged-predicted) "
              f"mean={resid.mean():+.2f} median={np.median(resid):+.2f} std={resid.std():.2f} "
              f"p10={np.percentile(resid,10):+.2f} p90={np.percentile(resid,90):+.2f}")
        d = pd.DataFrame({"log": tag, "TIME": df["TIME"], "RPM": df["RPM"], "CLT": df["CLT"],
                          "OP": df["Engine oil pressure"], "fan_term": fan_term,
                          "logged": df["Idle air %"], "predicted": predicted, "resid": resid})
        frames.append(d)

    if not frames:
        print("no data")
        return
    allpts = pd.concat(frames, ignore_index=True)
    allpts.to_csv("supra/notes/oil_pressure_airflow/backtest_points.csv", index=False)
    r = allpts["resid"]
    print(f"\nALL LOGS COMBINED: n={len(allpts)}, mean={r.mean():+.2f} median={np.median(r):+.2f} "
          f"std={r.std():.2f} p10={np.percentile(r,10):+.2f} p90={np.percentile(r,90):+.2f}")


if __name__ == "__main__":
    main()
