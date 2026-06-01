"""Lambda tracking quality: measured Lambda 1 vs Lambda target, hand-made map vs
machine-smoothed map. Companion to knock_chatter_cov.py.

Metric: tracking error as PERCENT off target,
    err% = (Lambda1 / Lambda_target - 1) * 100
(percent, not raw lambda, so an error at rich target 0.80 is comparable to one at
0.98). We report bias (mean err%) and spread (RMS err%) overall and by MAP load bin.

Why this is a fair old-vs-new comparison: err% is commanded-vs-measured, so it's
fuel-agnostic — flex-fuel ethanol variation between logs (which confounds absolute VE)
does NOT confound tracking. lambdaDelay is active and the logged Lambda is already
time-aligned to its cell (see notes), so same-row measured-vs-target is valid.

Where map quality shows: in boost / higher load, closed-loop STFT is typically off, so
tracking error there is pure feedforward (map) quality. Steady low-load cruise is
closed-loop and will track tightly regardless of map smoothness — watch the high-MAP bins.

Run: python supra/scripts/lambda_tracking.py
Output: prints tables + writes supra/scripts/lambda_tracking_old_vs_new.png
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MEAS, TGT = "Lambda 1", "Lambda target"
OD = r"C:/Users/WTCra/OneDrive/Documents/EMU_BLACK_V3/Supra"
ODL = OD + "/LogAutosave"

GROUPS = {
    "hand-made": [   # handmade and hand-smoothed are the SAME map
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
# Known global mixture offset: the whole map was NOT re-scaled after per-cylinder trims,
# so the machine-smoothed map reads ~3% lean of target uniformly. Remove that constant
# bias to compare the SHAPE (spread) of tracking, which is what map smoothness changes.
# A constant shift does not change std, so panel B (spread) is unaffected by this.
SHIFT = {"hand-made": 0.0, "machine-smoothed": -3.0}
# valid windows (drop DFCO/fuel-cut sentinels and railed sensor)
TGT_LO, TGT_HI = 0.70, 1.02
MEAS_LO, MEAS_HI = 0.60, 1.30
RPM_MIN = 1200
MAP_BINS = [40, 80, 110, 140, 185]
MAP_LBL = ["40-80\n(vac/cruise)", "80-110", "110-140\n(low boost)", "140-185\n(boost)"]


def load(path):
    cols = [MEAS, TGT, "RPM", "MAP"]
    df = pd.read_csv(path, sep=";", decimal=".", low_memory=False,
                     usecols=lambda c: c in cols)
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def collect(logs):
    frames = []
    for label, path in logs:
        try:
            df = load(path)
        except Exception as e:
            print(f"  {label}: load failed: {e}"); continue
        if MEAS not in df.columns or TGT not in df.columns:
            print(f"  {label}: missing lambda channels"); continue
        m = (df[TGT].between(TGT_LO, TGT_HI) & df[MEAS].between(MEAS_LO, MEAS_HI)
             & (df["RPM"] > RPM_MIN) & (df["MAP"] >= MAP_BINS[0]))  # drop decel/overrun
        s = df[m][[MEAS, TGT, "RPM", "MAP"]].dropna().copy()
        s["err"] = (s[MEAS] / s[TGT] - 1.0) * 100.0
        frames.append(s)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def rms(x):
    x = x.dropna()
    return float(np.sqrt(np.mean(x ** 2))) if len(x) else np.nan


def main():
    pooled = {}
    for g, logs in GROUPS.items():
        print(f"=== {g} ===")
        pooled[g] = collect(logs)
        if SHIFT.get(g):
            pooled[g]["err"] += SHIFT[g]  # remove known global mixture offset
            print(f"  applied {SHIFT[g]:+.1f}% bias correction (un-rescaled map after cyl trims)")

    print(f"\n{'group':18s}{'n':>8s}{'bias%':>8s}{'median%':>9s}{'std%':>8s}{'RMS%':>8s}")
    for g in GROUPS:
        e = pooled[g]["err"]
        print(f"{g:18s}{len(e):8d}{e.mean():8.2f}{e.median():9.2f}{e.std():8.2f}{rms(e):8.2f}")

    # bias & spread (std) by MAP bin -- std is the smoothness-sensitive tracking metric
    print(f"\nbias% / std%  by MAP bin:")
    print(f"{'bin':16s}" + "".join(f"{g:>22s}" for g in GROUPS))
    binstd = {g: [] for g in GROUPS}; binbias = {g: [] for g in GROUPS}; binn = {g: [] for g in GROUPS}
    for i in range(len(MAP_LBL)):
        lo, hi = MAP_BINS[i], MAP_BINS[i + 1]
        row = f"{MAP_LBL[i].splitlines()[0]:16s}"
        for g in GROUPS:
            d = pooled[g]
            e = d[(d["MAP"] >= lo) & (d["MAP"] < hi)]["err"]
            ok = len(e) >= 20
            b = e.mean() if ok else np.nan
            s = e.std() if ok else np.nan
            binbias[g].append(b); binstd[g].append(s); binn[g].append(len(e))
            cell = f"{b:+.1f}/{s:.1f}(n{len(e)})" if ok else f"--(n{len(e)})"
            row += f"{cell:>22s}"
        print(row)

    # ---- plot: (A) error distribution, (B) RMS by MAP bin ----
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(15, 5.6))
    bins = np.linspace(-15, 15, 61)
    for g in GROUPS:
        e = pooled[g]["err"]
        sh = f", shifted {SHIFT[g]:+.0f}%" if SHIFT.get(g) else ""
        axA.hist(e, bins=bins, density=True, alpha=.5, color=COLORS[g],
                 label=f"{g}  (std {e.std():.1f}%{sh})")
    axA.axvline(0, color="k", lw=1, ls="--")
    axA.set_xlabel("lambda tracking error  (measured/target − 1, %)")
    axA.set_ylabel("density"); axA.legend(fontsize=9)
    axA.set_title("Tracking-error distribution (all valid, RPM>1200)\n"
                  "machine bias-corrected −3% (un-rescaled map after cyl trims) — compare SHAPE/width")

    x = np.arange(len(MAP_LBL)); w = 0.4
    for j, g in enumerate(GROUPS):
        vals = [0 if np.isnan(r) else r for r in binstd[g]]
        bars = axB.bar(x + (j - 0.5) * w, vals, w, label=g, color=COLORS[g], alpha=.9)
        for k, b in enumerate(bars):
            s, n = binstd[g][k], binn[g][k]
            t = f"{s:.2f}%\nn={n}" if not np.isnan(s) else (f"n={n}" if n else "")
            axB.text(b.get_x() + b.get_width() / 2, (0 if np.isnan(s) else s) + 0.05,
                     t, ha="center", va="bottom", fontsize=8)
    axB.set_xticks(x); axB.set_xticklabels(MAP_LBL, fontsize=8)
    axB.set_xlabel("MAP load bin (kPa)"); axB.set_ylabel("tracking-error spread, std (%)")
    axB.legend(); axB.grid(axis="y", alpha=.3); axB.margins(y=.15)
    axB.set_title("Tracking-error SPREAD by load (bias removed)\nmap smoothness shows in the high-MAP/open-loop bins")

    fig.suptitle("Lambda tracking: measured vs target, hand-made vs machine-smoothed map",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    out = "supra/scripts/lambda_tracking_old_vs_new.png"
    fig.savefig(out, dpi=130)
    print(f"\nplot -> {out}")


if __name__ == "__main__":
    main()
