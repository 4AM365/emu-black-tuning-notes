"""Knock-sensor chatter as a combustion-stability (CoV) proxy, across three map
generations, in boost (MAP > 130 kPa):

    handmade        - oldest, point-by-point hand-built maps
    hand-smoothed   - smoothed by hand (hand-smoothed-1/2/3 logs)
    machine-smoothed- newest, algorithm/autotune-smoothed (new_fuel_strategy)  <- expected best

METHOD (operating-point-corrected CoV, on table TRANSITIONS only)
-----------------------------------------------------------------
`Knock voltage peak cyl N` = per-event peak of the band-pass-filtered knock signal
in that cylinder's window. We want the CYCLE-TO-CYCLE scatter as a proxy for
combustion CoV (~ CoV-of-IMEP).

The trap (the bug in the first cut): the MEAN of this channel rises steeply and
deterministically with RPM and load (mechanical engine noise). If you take std/mean
over a coarse 1000rpm x 50kPa window, the "spread" is dominated by that deterministic
trend, so a log that simply roams more of the boost map looks noisier — an artifact.
Fix: detrend within fine RPM x MAP cells, then measure residual scatter.

WHERE we measure matters: map smoothness bites while INTERPOLATING ACROSS CELLS, i.e.
during transitions — accelerating through RPM (dRPM/dt > 0) or ramping into boost
(dMAP/dt > 0). At steady state you sit in one cell and the rough-vs-smooth difference
washes out. So we restrict to positive transients before measuring scatter.

    resid_norm = (peak - mean_cell) / mean_cell           (per group, per cell)
    corrected CoV = std(resid_norm) * 100   (%)

This isolates scatter AROUND the local operating point (true cyclic variability) and
removes any absolute-level offset between groups. No-knock cycles only.

Run: python supra/scripts/knock_chatter_cov.py
Output: prints tables + writes supra/scripts/knock_cov_by_map_gen.png
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

KCH = "Knock voltage peak cyl 6"
MAP_MIN = 130.0
RPM_CELL, MAP_CELL = 250, 10      # fine detrend cells
MIN_CELL_N = 6                     # cell must have >= this many samples to detrend
# Transition gate: keep samples accelerating through RPM OR ramping into boost.
RATE_K = 3                         # samples over which to estimate a rate (~0.12 s)
POS_RPM_RATE = 150.0               # rpm/s
POS_MAP_RATE = 5.0                 # kPa/s
OD = r"C:/Users/WTCra/OneDrive/Documents/EMU_BLACK_V3/Supra"
ODL = OD + "/LogAutosave"

GROUPS = {
    "hand-made": [  # handmade and hand-smoothed are the SAME map -> one group
        ("20260524_1301",  r"supra/logs/20260524_1301.csv"),
        ("hood-removed",   OD + r"/hood-removed.csv"),
        ("hood 0506 hot",  OD + r"/hood on 0506 terrible day.csv"),
        ("hand-smoothed-1", ODL + r"/hand-smoothed-1.csv"),
        ("hand-smoothed-2", ODL + r"/hand-smoothed-2.csv"),
        ("hand-smoothed-3", ODL + r"/hand-smoothed-3.csv"),
    ],
    "machine-smoothed": [
        ("machine-smoothed", ODL + r"/machine-smoothed.csv"),
    ],
}
COLORS = {"hand-made": "#c44e52", "machine-smoothed": "#4c72b0"}
RPM_BINS = [3500, 4000, 4500, 5000, 5500]
RPM_LBL = ["3.5-4k", "4-4.5k", "4.5-5k", "5-5.5k"]
NUM = ["TIME", "RPM", "MAP", KCH, "Knocking cylinders", "Knock ign retard cyl 6"]


def load(path):
    df = pd.read_csv(path, sep=";", decimal=".", low_memory=False)
    for c in NUM:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def no_knock(df):
    m = pd.Series(True, index=df.index)
    if "Knocking cylinders" in df:
        m &= df["Knocking cylinders"].fillna(0) == 0
    if "Knock ign retard cyl 6" in df:
        m &= df["Knock ign retard cyl 6"].fillna(0) == 0
    return m


def collect(logs):
    """Pool MAP>130, no-knock, TRANSITIONING (accel or boost-ramp) samples."""
    frames = []
    kept = total = 0
    for label, path in logs:
        try:
            df = load(path)
        except Exception as e:
            print(f"  {label}: load failed: {e}"); continue
        if KCH not in df.columns:
            print(f"  {label}: no knock channel"); continue
        dt = df["TIME"].diff(RATE_K)
        drpm = df["RPM"].diff(RATE_K) / dt.where(dt > 0)
        dmap = df["MAP"].diff(RATE_K) / dt.where(dt > 0)
        trans = (drpm > POS_RPM_RATE) | (dmap > POS_MAP_RATE)
        base = (df["MAP"] > MAP_MIN) & no_knock(df)
        total += int(base.sum())
        m = base & trans.fillna(False)
        kept += int(m.sum())
        frames.append(df[m][["RPM", "MAP", KCH]].dropna())
    print(f"  -> kept {kept}/{total} boost samples on positive transitions")
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def detrend(d):
    """Add resid_norm = (peak - cellmean)/cellmean within RPM x MAP cells."""
    d = d.copy()
    d["rc"] = (d["RPM"] // RPM_CELL) * RPM_CELL
    d["mc"] = (d["MAP"] // MAP_CELL) * MAP_CELL
    g = d.groupby(["rc", "mc"])[KCH]
    d["mu"] = g.transform("mean")
    d["cn"] = g.transform("size")
    d = d[d["cn"] >= MIN_CELL_N]
    d["resid_norm"] = (d[KCH] - d["mu"]) / d["mu"]
    return d


def naive_cov(d):
    v = d[KCH].dropna()
    return v.std() / v.mean() * 100 if len(v) > 1 and v.mean() else np.nan


def main():
    pooled = {}
    for g, logs in GROUPS.items():
        print(f"=== {g} ===")
        pooled[g] = collect(logs)
    det = {g: detrend(pooled[g]) for g in GROUPS}

    print(f"\n{'group':18s}{'n_boost':>9s}{'naiveCoV':>10s}{'corrCoV':>9s}")
    for g in GROUPS:
        print(f"{g:18s}{len(pooled[g]):9d}{naive_cov(pooled[g]):9.1f}%{det[g]['resid_norm'].std()*100:8.1f}%")

    # per-RPM-bin corrected CoV
    print(f"\ncorrected CoV (std of detrended residual, %) by RPM bin:")
    print(f"{'bin':8s}" + "".join(f"{g:>18s}" for g in GROUPS))
    binc = {g: [] for g in GROUPS}; binn = {g: [] for g in GROUPS}
    for i in range(len(RPM_LBL)):
        lo, hi = RPM_BINS[i], RPM_BINS[i + 1]
        row = f"{RPM_LBL[i]:8s}"
        for g in GROUPS:
            d = det[g]
            r = d[(d["RPM"] >= lo) & (d["RPM"] < hi)]["resid_norm"]
            c = r.std() * 100 if len(r) >= 15 else np.nan
            binc[g].append(c); binn[g].append(len(r))
            row += f"  {('%.1f%%(%d)' % (c, len(r))) if not np.isnan(c) else ('--(%d)' % len(r)):>16s}"
        print(row)

    # ---- plot ----
    fig, ax = plt.subplots(figsize=(11, 5.6))
    x = np.arange(len(RPM_LBL)); w = 0.4
    glist = list(GROUPS)
    for j, g in enumerate(glist):
        vals = [0 if np.isnan(c) else c for c in binc[g]]
        bars = ax.bar(x + (j - 0.5) * w, vals, w,
                      label=f"{g}  (overall {det[g]['resid_norm'].std()*100:.1f}%)",
                      color=COLORS[g], alpha=.9)
        for k, b in enumerate(bars):
            c, n = binc[g][k], binn[g][k]
            t = f"{c:.1f}%\nn={n}" if not np.isnan(c) else (f"n={n}" if n else "")
            ax.text(b.get_x() + b.get_width() / 2, (0 if np.isnan(c) else c) + 0.15,
                    t, ha="center", va="bottom", fontsize=7.5)
    ax.set_xticks(x); ax.set_xticklabels(RPM_LBL)
    ax.set_xlabel("RPM bin"); ax.set_ylabel("Operating-point-corrected CoV (%)")
    ax.set_title("Combustion-stability proxy: cyl-6 knock-voltage cyclic scatter by map generation\n"
                 f"(MAP>{MAP_MIN:.0f} kPa, no-knock, detrended within {RPM_CELL}rpm x {MAP_CELL}kPa cells — lower = more stable)")
    ax.legend(); ax.grid(axis="y", alpha=.3); ax.margins(y=.15)
    fig.tight_layout()
    out = "supra/scripts/knock_cov_by_map_gen.png"
    fig.savefig(out, dpi=130)
    print(f"\nplot -> {out}")


if __name__ == "__main__":
    main()
