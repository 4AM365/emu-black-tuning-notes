"""Post-cleaning regime (t >= 1040, window 1.5-6.5 live): oil pressure vs Idle air % at Ignition Angle == 18, 1025 +/- 20 rpm."""
import os, sys, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__)); from loadf import load
OUT = r"C:\Code\car-projects\emu-black-tuning-notes\supra\notes\tb_clean_2026-09-19"
BLUE, INK, INK2, SURF, GRAY = "#2a78d6", "#0b0b0b", "#52514e", "#fcfcfb", "#9a9891"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": "#c9c8c2", "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.spines.top": False, "axes.spines.right": False, "grid.color": "#e6e5e0", "grid.linewidth": 0.6,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "text.color": INK})
df = load()
st = df["Idle state"].values; t = df["TIME"].values; last = -1e9; ent = np.full(len(df), np.nan)
for i in range(len(df)):
    if st[i] == 2 and (i == 0 or st[i-1] != 2): last = t[i]
    if st[i] == 2: ent[i] = t[i] - last
df["t_in"] = ent
g = df[(df.TIME >= 1050) & (df["Idle state"] == 2) & (df.t_in > 3) & (df["Ignition Angle"] == 18.0) & df.RPM.between(1005, 1045)
       & (df["Idle target"] == 1025) & (df.CLT >= 95) & (df["Engine oil pressure status"] == 1)].copy()
g["op_bin"] = (g["Engine oil pressure"] * 4).round() / 4
tab = g.groupby("op_bin").agg(n=("RPM", "size"), air_med=("Idle air %", "median"), air_p10=("Idle air %", lambda s: s.quantile(.1)), air_p90=("Idle air %", lambda s: s.quantile(.9)),
                              pid_med=("Idle PID air % correction", "median"), tps_med=("TPS", "median"), map_med=("MAP", "median"), iat=("IAT", "median"),
                              t0=("TIME", "min"), t1=("TIME", "max"))
tab = tab[tab.n >= 25]
print(f"n = {len(g)} samples, t {g.TIME.min():.0f}-{g.TIME.max():.0f} s, OP {g['Engine oil pressure'].min():.2f}-{g['Engine oil pressure'].max():.2f} bar")
print(tab.round(2).to_string())
k, b = np.polyfit(g["Engine oil pressure"], g["Idle air %"], 1); r = g["Idle air %"] - (k * g["Engine oil pressure"] + b)
print(f"fit: Idle air % = {b:.1f} + {k:.1f} × OP   (resid sd {r.std():.1f});  base (air − PID) median {(g['Idle air %'] - g['Idle PID air % correction']).median():.1f}")
fig, ax = plt.subplots(figsize=(10.5, 6))
ax.scatter(g["Engine oil pressure"], g["Idle air %"], s=9, alpha=.18, color=BLUE, edgecolor="none")
ax.vlines(tab.index, tab.air_p10, tab.air_p90, color=BLUE, lw=1.2, alpha=.7)
ax.plot(tab.index, tab.air_med, color=BLUE, lw=2, marker="o", ms=6, markeredgecolor=SURF, zorder=3)
for op, r_ in tab.iterrows():
    ax.annotate(f"{r_.air_med:.1f}", (op, r_.air_med), textcoords="offset points", xytext=(0, 10), ha="center", fontsize=9, color=INK)
    ax.annotate(f"n={int(r_.n)}", (op, r_.air_p10), textcoords="offset points", xytext=(0, -12), ha="center", fontsize=7.5, color=INK2)
xs = np.linspace(1.5, 3.4, 20); ax.plot(xs, k * xs + b, color=GRAY, lw=1, ls="--")
ax.text(xs[-1], k * xs[-1] + b + 0.8, f"fit: {k:.1f} airflow-% per bar", fontsize=8.5, color=INK2, ha="right")
base = (g["Idle air %"] - g["Idle PID air % correction"]).median()
ax.axhline(base, color=GRAY, lw=.8, ls=":"); ax.text(1.55, base + 0.5, f"idleActiveAirflow hot cell in force ≈ {base:.0f} % (Idle air % − PID)", fontsize=8.5, color=INK2)
ax.set_xlabel("engine oil pressure [bar]"); ax.set_ylabel("Idle air %  (airflow %, window 1.5–6.5)")
ax.set_xlim(1.5, 3.4); ax.set_ylim(8, 36); ax.grid(alpha=.6)
ax.set_title("Post-cleaning: airflow % the idle strategy needed vs oil pressure — 1025 ± 20 rpm, Ignition Angle = 18°, CLT ≥ 95", loc="left", fontsize=11.5)
ax.text(0.01, 0.97, f"fullchannels.csv t ≥ 1050 s (1.5–6.5 window live; the 1042–1049 s edit transient excluded) · settled ACTIVE, ≥ 3 s after entry · n = {len(g)} samples\n"
        "dot = median per 0.25-bar bin, whisker = p10–p90 · Idle air % = commanded position through the window (PID included)", transform=ax.transAxes, va="top", fontsize=8.3, color=INK2)
fig.tight_layout(); fig.savefig(OUT + "/op_vs_idle_air_post_clean.png", dpi=130); plt.close(fig)
tab.round(2).to_csv(OUT + "/op_vs_idle_air_post_clean.csv")
