"""Visuals: TB cleaning effect and the fouling history at hot idle (~1000 rpm, ign 17-19).
All TPS shown in ONE frame: the post-relearn (2026-09-19 afternoon) calibration. Pre-relearn TPS -= 1.09
(one TPS calibration Apr..09-19 morning, V@0% = 0.680; post-relearn 0.720 -> 27.6 %/V * 0.040 V = 1.09 %)."""
import os, sys, datetime as dt
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__)); from loadf import load
REPO = r"C:\Code\car-projects\emu-black-tuning-notes"
OUT = REPO + r"\supra\notes\tb_clean_2026-09-19"
S = REPO + r"\supra\notes\op_vs_dbw_1000rpm\samples.csv"
BLUE, ORANGE, AQUA, GRAY, INK, INK2, SURF = "#2a78d6", "#eb6834", "#1baf7a", "#9a9891", "#0b0b0b", "#52514e", "#fcfcfb"
SHIFT = 1.09
plt.rcParams.update({"font.size": 10, "axes.edgecolor": "#c9c8c2", "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.spines.top": False, "axes.spines.right": False, "grid.color": "#e6e5e0", "grid.linewidth": 0.6,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "text.color": INK})

a = pd.read_csv(S)
a["clean"] = a["log"].eq("fullchannels")            # running script already trims fullchannels to the afternoon
a["tps_f"] = np.where(a["clean"], a["TPS"], a["TPS"] - SHIFT)   # one frame
a["date"] = pd.to_datetime(a["log_date"])
a["key"] = a["date"].dt.strftime("%m-%d") + np.where(a["clean"], " clean", "")

# ---------- Figure 1: fouling history ----------
rows = []
for key, g in a.groupby("key"):
    d = g["date"].iloc[0]
    w = g[g["Engine oil pressure"].between(2.0, 3.25)]        # common oil-pressure band where most logs overlap
    band = "OP 2.0–3.25"
    if len(w) < 30: w = g; band = "all OP"
    rows.append(dict(key=key, date=d, clean=g["clean"].iloc[0], n=len(w), tps=w["tps_f"].median(), p10=w["tps_f"].quantile(.1), p90=w["tps_f"].quantile(.9),
                     op=w["Engine oil pressure"].median(), mr=w["MAPxRPM_k"].median(), mr10=w["MAPxRPM_k"].quantile(.1), mr90=w["MAPxRPM_k"].quantile(.9), band=band))
h = pd.DataFrame(rows).sort_values(["date", "clean"])
# 09-19 morning and afternoon: nudge x so both are visible
h["x"] = h["date"] + pd.to_timedelta(np.where(h["clean"], 1.2, 0), unit="D")
print(h[["key", "n", "tps", "p10", "p90", "op", "mr", "band"]].round(2).to_string())

fig, ax = plt.subplots(2, 1, figsize=(12, 8.2), sharex=True, gridspec_kw={"height_ratios": [3, 2], "hspace": 0.12})
dirty = h[~h["clean"]]; clean = h[h["clean"]]
ax[0].plot(dirty["x"], dirty["tps"], color=ORANGE, lw=2, zorder=2)
ax[0].vlines(dirty["x"], dirty["p10"], dirty["p90"], color=ORANGE, lw=1, alpha=.45)
ax[0].scatter(dirty["x"], dirty["tps"], s=46, color=ORANGE, edgecolor=SURF, linewidth=1.5, zorder=3)
ax[0].vlines(clean["x"], clean["p10"], clean["p90"], color=BLUE, lw=1, alpha=.6)
ax[0].scatter(clean["x"], clean["tps"], s=70, color=BLUE, edgecolor=SURF, linewidth=1.5, zorder=4)
for _, r in h.iterrows():
    ax[0].annotate(f"{r.tps:.1f}", (r.x, r.tps), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=9, color=INK)
    ax[0].annotate(f"{r.op:.1f} bar", (r.x, r.p10), textcoords="offset points", xytext=(0, -13), ha="center", fontsize=7.5, color=INK2)
ax[0].annotate("throttle body cleaned\n+ DBW relearn", (clean["x"].iloc[0], clean["tps"].iloc[0]), textcoords="offset points", xytext=(-95, -34), fontsize=9, color=BLUE,
               arrowprops=dict(arrowstyle="-", color=BLUE, lw=.8))
ax[0].set_ylabel("plate position holding ~1000 rpm  [% TPS, post-relearn frame]")
ax[0].set_ylim(1.5, 6.2); ax[0].grid(axis="y")
ax[0].set_title("Hot idle at ~1000 rpm, ignition 17–19°: the plate opening climbed all year, then dropped in one step", loc="left", fontsize=12, color=INK)
ax[0].text(0.01, 0.97, "orange = fouled throttle body (pre-relearn TPS shifted −1.09 into today's frame)   ·   blue = clean\n"
           "dot = median, whisker = p10–p90 of settled samples, small label = median oil pressure", transform=ax[0].transAxes, va="top", fontsize=8.5, color=INK2)
ax[1].vlines(dirty["x"], dirty["mr10"], dirty["mr90"], color=ORANGE, lw=1, alpha=.45)
ax[1].scatter(dirty["x"], dirty["mr"], s=46, color=ORANGE, edgecolor=SURF, linewidth=1.5, zorder=3)
ax[1].vlines(clean["x"], clean["mr10"], clean["mr90"], color=BLUE, lw=1, alpha=.6)
ax[1].scatter(clean["x"], clean["mr"], s=70, color=BLUE, edgecolor=SURF, linewidth=1.5, zorder=4)
ax[1].axhspan(35, 39, color=GRAY, alpha=.10, lw=0)
ax[1].set_ylabel("air the engine took\nMAP × RPM / 1000")
ax[1].set_ylim(30, 44); ax[1].grid(axis="y")
ax[1].text(0.01, 0.95, "same engine-side air all year (grey band 35–39 k): the position moved, the air did not", transform=ax[1].transAxes, va="top", fontsize=8.5, color=INK2)
ax[1].xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b %d"))
fig.savefig(OUT + r"\fouling_history.png", dpi=130, bbox_inches="tight"); plt.close(fig)

# ---------- Figure 2: same day, position vs oil pressure and air vs oil pressure ----------
df = load()
st = df["Idle state"].values; t = df["TIME"].values; last = -1e9; ent = np.full(len(df), np.nan)
for i in range(len(df)):
    if st[i] == 2 and (i == 0 or st[i-1] != 2): last = t[i]
    if st[i] == 2: ent[i] = t[i] - last
df["t_in"] = ent
g = df[(df["Idle state"] == 2) & (df["t_in"] > 3) & (df["CLT"] >= 95) & (df["Idle target"] == 1025) & df["RPM"].between(975, 1075) & df["Ignition Angle"].between(17, 19) & (df["MAP"] < 60)].copy()
g["clean"] = g["TIME"] > 640
g["tps_f"] = np.where(g["clean"], g["TPS"], g["TPS"] - SHIFT)
fig, ax = plt.subplots(1, 2, figsize=(13, 5.4))
for flag, col, lab in [(False, ORANGE, "morning — fouled"), (True, BLUE, "afternoon — clean")]:
    s = g[g["clean"] == flag]
    ax[0].scatter(s["Engine oil pressure"], s["tps_f"], s=7, alpha=.25, color=col, label=lab, edgecolor="none")
    ax[1].scatter(s["Engine oil pressure"], s["MR"], s=7, alpha=.25, color=col, label=lab, edgecolor="none")
    # binned medians as the readable layer
    b = (s["Engine oil pressure"] * 4).round() / 4
    m = s.groupby(b).agg(tps=("tps_f", "median"), mr=("MR", "median"), n=("MR", "size")); m = m[m.n >= 25]
    ax[0].plot(m.index, m.tps, color=col, lw=2, marker="o", ms=5, markeredgecolor=SURF)
    ax[1].plot(m.index, m.mr, color=col, lw=2, marker="o", ms=5, markeredgecolor=SURF)
ax[0].set_xlabel("engine oil pressure [bar]  (falls as the oil heats — the soak clock)"); ax[0].set_ylabel("plate position holding 1025 rpm  [% TPS, one frame]")
ax[0].set_ylim(1.5, 5.5); ax[0].grid(alpha=.6); ax[0].legend(frameon=False, loc="upper left")
ax[0].set_title("Same day, same engine, same coolant (96 °C), same 18° ignition", loc="left", fontsize=11)
ax[0].annotate("≈ −2.0 % TPS where the two\noil-pressure ranges meet (3.2 bar)", xy=(3.25, 3.9), fontsize=9, color=INK2, ha="center")
ax[0].annotate("", xy=(3.25, 2.85), xytext=(3.25, 4.75), arrowprops=dict(arrowstyle="<->", color=INK2, lw=.9))
ax[1].set_xlabel("engine oil pressure [bar]"); ax[1].set_ylabel("air the engine took   MAP × RPM / 1000")
ax[1].set_ylim(30, 44); ax[1].grid(alpha=.6); ax[1].legend(frameon=False, loc="upper left")
ax[1].set_title("…and the air it needed to hold 1025 rpm", loc="left", fontsize=11)
ax[1].text(0.02, 0.06, "only the oil-temperature term separates them: ~5 % more air on thicker oil", transform=ax[1].transAxes, fontsize=8.5, color=INK2)
fig.tight_layout(); fig.savefig(OUT + r"\before_after_vs_oil_pressure.png", dpi=130); plt.close(fig)

# ---------- Figure 3: throttle flow characteristic, fouled vs clean ----------
k = df[(df["Idle state"] == 2) & (df["t_in"] > 3) & (df["CLT"] >= 45) & (df["RPM"] - df["Idle target"]).abs().le(40) & (df["MAP"] < 60) & (df["PPS"] == 0)].copy()
k["clean"] = k["TIME"] > 640
k["tps_f"] = np.where(k["clean"], k["TPS"], k["TPS"] - SHIFT)
fig, ax = plt.subplots(figsize=(10.5, 6.2))
for flag, col, lab in [(False, ORANGE, "fouled (morning)"), (True, BLUE, "clean (afternoon)")]:
    s = k[k["clean"] == flag]
    ax.scatter(s["tps_f"], s["MR"], s=8, alpha=.22, color=col, edgecolor="none", label=lab)
    # fit through binned medians (0.1 % TPS bins with >= 20 samples)
    b = (s["tps_f"] * 10).round() / 10
    m = s.groupby(b)["MR"].median(); n = s.groupby(b).size(); m = m[n >= 20]
    kk, bb = np.polyfit(m.index, m.values, 1)
    xs = np.linspace(0, 6.4, 50); ax.plot(xs, kk * xs + bb, color=col, lw=2)
    x0 = -bb / kk
    ax.annotate(f"{lab}: {kk:.1f} k per % TPS, zero flow at {x0:+.2f} % TPS", (xs[-1], kk * xs[-1] + bb), textcoords="offset points", xytext=(-8, 8 if flag else -14), ha="right", fontsize=9, color=col)
    print(lab, "slope", round(kk, 2), "intercept", round(bb, 2), "zero at", round(x0, 2), "n", len(s))
ax.axvline(0, color=GRAY, lw=.8, ls=":"); ax.text(0.05, 61, "closed stop (0 % after relearn)", fontsize=8, color=INK2, rotation=90, va="top")
ax.set_xlim(-0.2, 6.5); ax.set_ylim(0, 64); ax.grid(alpha=.6)
ax.set_xlabel("plate position  [% TPS, one frame]"); ax.set_ylabel("air the engine took at that position   MAP × RPM / 1000")
ax.set_title("What the throttle body flows per degree of opening — settled idle points, 1025–1500 rpm", loc="left", fontsize=12)
ax.text(0.02, 0.95, "each dot is a settled idle sample; RPM rises left→right within each colour (1025 → 1500 during warm-up)\n"
        "fouled: a ~2.5 %-TPS dead band before any air flows   ·   clean: flow starts at the stop and is proportional to opening", transform=ax.transAxes, va="top", fontsize=8.5, color=INK2)
ax.legend(frameon=False, loc="lower right")
fig.tight_layout(); fig.savefig(OUT + r"\flow_characteristic_fouled_vs_clean.png", dpi=130); plt.close(fig)
print("done")
