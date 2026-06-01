"""HOT idle RPM tracking error on recent (v3 / machine-smoothed) logs, vs OEM benchmark.

HOT = fully heat-soaked: CLT >= HOT_CLT (operating temp ~96 C on this build), so the
warm-up drift is excluded and we see the true hot-idle hold.

Metric: error = RPM - Idle target, on STEADY HOT closed-loop idle:
  - Idle control active == 1, Vehicle Speed < 3 (parked), CLT >= HOT_CLT
  - drop the first SETTLE s of each idle entry (return-to-idle slew is not "hold")
  - idle target stable across a ~1 s window
Report bias (mean), spread (std RPM), idle-speed CoV (%), excursions, % within bands.

OEM-quality reference (Kiencke & Nielsen idle chapter, corpus):
  - well-tuned controller: ~100-150 RPM dip on an A/C load step
  - smooth stock warm idle hold: ~+/-25-50 RPM, idle-speed CoV ~1-3% (but at 650-750 rpm,
    no cam). A cammed 2JZ idles inherently rougher; judge against hold/disturbance numbers.

Run: python supra/scripts/idle_tracking.py  -> writes supra/scripts/idle_tracking_hot.png
"""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

LOGS = {  # purely new_fuel_strategy -- maps differ in idle calibration, so do not pool
    "new_fuel_strategy":"supra/logs/new_fuel_strategy.csv",
}
HOT_CLT = 95.0
SETTLE_S = 2.0
cols = ["TIME", "RPM", "Idle target", "Idle control active", "Vehicle Speed", "CLT"]


def stats(e):
    return dict(n=len(e), bias=e.mean(), std=e.std(),
                p05=e.quantile(.05), p95=e.quantile(.95),
                lo=e.min(), hi=e.max(), w50=(e.abs() <= 50).mean() * 100)


def steady_hot_idle(path):
    df = pd.read_csv(path, sep=";", decimal=".", low_memory=False, usecols=lambda c: c in cols)
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    hz = (len(df) - 1) / (df["TIME"].iloc[-1] - df["TIME"].iloc[0])
    settle = int(SETTLE_S * hz)
    active = (df["Idle control active"] == 1) & (df["Vehicle Speed"] < 3) & (df["CLT"] >= HOT_CLT)
    seg = (active != active.shift()).cumsum()
    keep = active.copy()
    for _, idx in df[active].groupby(seg[active]).groups.items():
        for i in list(idx)[:settle]:
            keep[i] = False
    keep &= df["Idle target"].rolling(int(hz), min_periods=1).std().fillna(0) < 5
    d = df[keep].copy()
    d["err"] = d["RPM"] - d["Idle target"]
    # longest CONTIGUOUS kept run (original index order) for an honest time trace
    runs = (d.index.to_series().diff() != 1).cumsum()
    longest = max((g for _, g in d.groupby(runs)), key=len, default=d)
    return d, hz, longest


parts, hz, traces = [], None, []
print(f"per-log HOT idle (CLT>={HOT_CLT:.0f}):")
for name, path in LOGS.items():
    d, hz, longest = steady_hot_idle(path)
    s = stats(d["err"].dropna())
    print(f"  {name:18s} n={s['n']:5d} ({s['n']/hz:4.0f}s)  bias{s['bias']:+5.0f}  std{s['std']:5.0f}  "
          f"within+/-50 {s['w50']:4.0f}%  worst {s['lo']:+.0f}/{s['hi']:+.0f}")
    d["log"] = name
    parts.append(d); traces.append((name, longest, hz))
D = pd.concat(parts, ignore_index=True)
err = D["err"].dropna()
s = stats(err)

print(f"\nPOOLED hot idle: {s['n']} samples ({s['n']/hz:.0f} s)")
print(f"  bias {s['bias']:+.1f} RPM | std {s['std']:.1f} RPM | "
      f"idle-speed CoV {D['RPM'].std()/D['RPM'].mean()*100:.2f}% | "
      f"within +/-50 {s['w50']:.0f}% | worst {s['lo']:+.0f}/{s['hi']:+.0f}")

# ---- plot ----
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.2))
ax1.hist(err, bins=np.arange(-150, 151, 10), color="#4c72b0", alpha=.85)
ax1.axvline(0, color="k", lw=1)
for x in (-50, 50):
    ax1.axvline(x, color="#2a9d3b", ls="--", lw=1.3)
ax1.axvline(-50, color="#2a9d3b", ls="--", lw=1.3, label="+/-50 (smooth OEM hold)")
ax1.set_xlabel("hot-idle tracking error: RPM - target"); ax1.set_ylabel("samples")
ax1.set_title(f"HOT steady-idle error (CLT>={HOT_CLT:.0f}, recent logs)\n"
              f"std {err.std():.0f} RPM, CoV {D['RPM'].std()/D['RPM'].mean()*100:.1f}%, "
              f"{(err.abs()<=50).mean()*100:.0f}% within +/-50"); ax1.legend(fontsize=8)

name, g, ghz = max(traces, key=lambda x: len(x[1]))
t = (g["TIME"] - g["TIME"].iloc[0]).values
ax2.plot(t, g["RPM"], color="#4c72b0", lw=.9, label="RPM")
ax2.plot(t, g["Idle target"], color="#c44e52", lw=1.4, ls="--", label="target")
ax2.set_xlabel("time in hot-idle stretch (s)"); ax2.set_ylabel("RPM")
ax2.set_title(f"Longest CONTIGUOUS hot-idle stretch ({len(g)/ghz:.0f} s, {name})")
ax2.legend(fontsize=9); ax2.grid(alpha=.3)
fig.suptitle("Supra HOT idle tracking quality (recent / v3 machine-smoothed)", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig("supra/scripts/idle_tracking_hot.png", dpi=130)
print("\nplot -> supra/scripts/idle_tracking_hot.png")
