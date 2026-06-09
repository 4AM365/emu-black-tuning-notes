"""Attribute the slow hot-idle RPM drift in new_fuel_strategy to a correction term.

The hot-idle stretch enters high (~+110 RPM) and decays to target over ~25-30 s. Is the
driver (a) the airflow PID slowly winding out an excess (response to the high entry), or
(b) charge-temp / IAT compensation drifting torque (an exogenous cause the PID chases)?

Method: take the longest contiguous hot, parked, idle-active stretch (NO settle drop, so
we see the entry). Decompose idle air into PID vs base (= total - PID). Overlay charge
temp, IAT, idle ign correction, lambda. Print per-channel trend (slope over the stretch)
and correlation with RPM so cause (leads, exogenous) is separable from response (PID).

Run: python supra/scripts/idle_drift_attribution.py -> supra/scripts/idle_drift_attribution.png
"""
import sys, os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    sys.exit("usage: python idle_drift_attribution.py LOG.csv [out.png] [hot_clt]")
LOG = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else "idle_drift_attribution.png"
HOT_CLT = float(sys.argv[3]) if len(sys.argv) > 3 else 95.0
chans = ["TIME","RPM","Idle target","Idle control active","Vehicle Speed","CLT","IAT",
         "Charge temp","Idle air %","Idle PID air % correction","Idle ignition correction",
         "Ignition Angle","Lambda 1","Lambda target","IAT user correction","F.IAT user corr."]

df = pd.read_csv(LOG, sep=";", decimal=".", low_memory=False, usecols=lambda c: c in chans)
for c in df.columns:
    df[c] = pd.to_numeric(df[c], errors="coerce")
hz = (len(df) - 1) / (df["TIME"].iloc[-1] - df["TIME"].iloc[0])

active = (df["Idle control active"] == 1) & (df["Vehicle Speed"] < 3) & (df["CLT"] >= HOT_CLT)
runs = (active != active.shift()).cumsum()
g = max((grp for k, grp in df[active].groupby(runs[active])), key=len)
g = g.reset_index(drop=True)
t = (g["TIME"] - g["TIME"].iloc[0]).values
g["base air"] = g["Idle air %"] - g["Idle PID air % correction"]
print(f"longest hot-idle stretch: {len(g)} samples ({t[-1]:.0f} s)\n")

def slope_per_s(y):
    y = y.values.astype(float); m = np.isfinite(y)
    if m.sum() < 5: return np.nan
    return np.polyfit(t[m], y[m], 1)[0]

print(f"{'channel':28s}{'start':>9s}{'end':>9s}{'slope/s':>10s}{'corr(RPM)':>11s}")
rpm = g["RPM"]
for c in ["RPM","Idle target","Charge temp","IAT","Idle air %",
          "Idle PID air % correction","base air","Idle ignition correction",
          "Ignition Angle","Lambda 1","IAT user correction","F.IAT user corr."]:
    if c not in g: continue
    y = g[c]
    cc = y.corr(rpm)
    print(f"{c:28s}{y.iloc[:int(hz)].mean():9.1f}{y.iloc[-int(hz):].mean():9.1f}"
          f"{slope_per_s(y):10.3f}{cc:11.2f}")

# ---- plot ----
fig, axes = plt.subplots(3, 1, figsize=(12, 11), sharex=True)
a = axes[0]
a.plot(t, g["RPM"], color="#4c72b0", lw=1, label="RPM")
a.plot(t, g["Idle target"], color="#c44e52", ls="--", lw=1.4, label="Idle target")
a.set_ylabel("RPM"); a.legend(loc="upper right", fontsize=8)
a2 = a.twinx()
a2.plot(t, g["Charge temp"], color="#dd8452", lw=1.2, label="Charge temp")
a2.plot(t, g["IAT"], color="#8c8c8c", lw=1, ls=":", label="IAT")
a2.set_ylabel("temp (°C)"); a2.legend(loc="lower right", fontsize=8)
a.set_title("A. RPM vs target  +  charge temp / IAT  (does temp rise drive the decay?)")

b = axes[1]
b.plot(t, g["Idle air %"], color="#4c72b0", lw=1.2, label="Idle air % (total)")
b.plot(t, g["base air"], color="#55a868", lw=1.2, label="base air (total - PID)")
b.plot(t, g["Idle PID air % correction"], color="#c44e52", lw=1.2, label="Idle PID air % corr")
b.axhline(0, color="k", lw=.6)
b.set_ylabel("idle air (%)"); b.legend(loc="upper right", fontsize=8)
b2 = b.twinx()
b2.plot(t, g["Idle ignition correction"], color="#dd8452", lw=1, label="Idle ign corr (°)")
b2.set_ylabel("idle ign corr (°)"); b2.legend(loc="lower right", fontsize=8)
b.set_title("B. Airflow split (PID vs base)  +  idle ignition correction")

c = axes[2]
c.plot(t, g["Lambda 1"], color="#4c72b0", lw=1, label="Lambda 1")
c.plot(t, g["Lambda target"], color="#c44e52", ls="--", lw=1.2, label="Lambda target")
c.set_ylabel("lambda"); c.legend(loc="upper right", fontsize=8)
c2 = c.twinx()
for ch, col in [("IAT user correction", "#dd8452"), ("F.IAT user corr.", "#8172b3")]:
    if ch in g: c2.plot(t, g[ch], color=col, lw=1, label=ch)
c2.set_ylabel("IAT/charge fuel corr (%)"); c2.legend(loc="lower right", fontsize=8)
c.set_title("C. Mixture (lambda)  +  charge/IAT fuel correction"); c.set_xlabel("time in hot-idle stretch (s)")

fig.suptitle(f"Hot-idle drift attribution — {os.path.basename(LOG)}", fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.97])
fig.savefig(OUT, dpi=130)
print(f"\nplot -> {OUT}")
