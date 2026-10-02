"""Fouling history from EVERY log that has TPS/RPM/Idle state/CLT (no oil-pressure or ignition gate), plus the
flow-vs-position figure. One TPS frame: pre-relearn TPS -= 1.09."""
import os, sys, glob, datetime as dt
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__)); from loadf import load
REPO = r"C:\Code\car-projects\emu-black-tuning-notes"; OUT = REPO + r"\supra\notes\tb_clean_2026-09-19"
EMU = r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra"
BLUE, ORANGE, GRAY, INK, INK2, SURF = "#2a78d6", "#eb6834", "#9a9891", "#0b0b0b", "#52514e", "#fcfcfb"
SHIFT = 1.09
plt.rcParams.update({"font.size": 10, "axes.edgecolor": "#c9c8c2", "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.spines.top": False, "axes.spines.right": False, "grid.color": "#e6e5e0", "grid.linewidth": 0.6,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "text.color": INK})
NEED = ["TIME", "RPM", "TPS", "Idle state", "CLT"]; OPT = ["Idle target", "PPS", "Engine oil pressure", "Ignition Angle", "MAP", "Idle air %", "Data changing"]
rows = []; seen = set()
for d in [EMU, EMU + r"\misc log csv", EMU + r"\LogAutosave", REPO + r"\supra\tunes"]:
    for p in sorted(glob.glob(d + r"\*.csv")):
        k = os.path.basename(p).lower()
        if k in seen or os.path.getsize(p) < 20000 or k == "after1720.csv": continue
        seen.add(k)
        hdr = open(p, encoding="utf-8", errors="replace").readline().strip().split(";")
        if any(c not in hdr for c in NEED): continue
        df = pd.read_csv(p, sep=";", usecols=NEED + [c for c in OPT if c in hdr], low_memory=False)
        segs = [("", df)]
        if k == "fullchannels.csv": segs = [(" clean", df[df.TIME > 640])]      # its first 602 s is whencold.csv, already scanned
        for tag, s in segs:
            g = s[(s["Idle state"] == 2) & (s["CLT"] >= 90)]
            if "Idle target" not in g: continue
            g = g[(g["RPM"] - g["Idle target"]).abs() <= 60]
            g["band"] = (g["Idle target"] / 100).round() * 100
            for band, gb in g.groupby("band"):
                if band not in (1000, 1100, 1200) or len(gb) < 30: continue
                clean = tag != ""
                tps = gb["TPS"] - (0 if clean else SHIFT)
                rows.append(dict(log=k + tag, band=int(band), date=dt.datetime.fromtimestamp(os.path.getmtime(p)), clean=clean, n=len(gb), tps=tps.median(), p10=tps.quantile(.1), p90=tps.quantile(.9),
                                 rpm=gb["RPM"].median(), op=gb["Engine oil pressure"].median() if "Engine oil pressure" in gb else np.nan,
                                 ign=gb["Ignition Angle"].median() if "Ignition Angle" in gb else np.nan,
                                 mr=(gb["MAP"] * gb["RPM"] / 1000).median() if "MAP" in gb else np.nan))
h = pd.DataFrame(rows).sort_values("date")
h = h.drop_duplicates(subset=["band", "n", "tps"])           # re-exports of the same recording
pd.set_option("display.width", 250); print(h[["log", "band", "n", "rpm", "tps", "p10", "p90", "op", "ign", "mr"]].round(2).to_string())
h.to_csv(OUT + "/fouling_history_points.csv", index=False)
h["grp"] = np.where(h.band == 1200, "1200", "1000")
fig, ax = plt.subplots(3, 1, figsize=(13.5, 9.6), sharex=True, gridspec_kw={"height_ratios": [3, 3, 1.6], "hspace": 0.08})
for row, grp, ttl in [(0, "1000", "idle target 1000–1100 rpm"), (1, "1200", "idle target 1200 rpm")]:
    for clean, col in [(False, ORANGE), (True, BLUE)]:
        g = h[(h.grp == grp) & (h.clean == clean)]
        if g.empty: continue
        ax[row].vlines(g.date, g.p10, g.p90, color=col, lw=0.9, alpha=.35)
        ax[row].scatter(g.date, g.tps, s=np.clip(g.n / 60, 20, 120), color=col, edgecolor=SURF, linewidth=1.2, zorder=3)
        for _, r in g[g.n >= 1000].iterrows():
            ax[row].annotate(f"{r.tps:.1f}", (r.date, r.tps), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=8, color=INK)
    ax[row].set_ylim(1.4, 5.9); ax[row].grid(axis="y"); ax[row].set_ylabel("% TPS (post-relearn frame)")
    ax[row].text(0.995, 0.04, ttl, transform=ax[row].transAxes, ha="right", va="bottom", fontsize=10, color=INK)
c = h[h.clean & (h.grp == "1000")].iloc[0]
ax[0].annotate("throttle body cleaned + DBW relearn," + chr(10) + "same afternoon: 4.8 / 3.9 → 2.5", (c.date, c.tps), textcoords="offset points", xytext=(-330, 85), fontsize=9, color=BLUE,
               arrowprops=dict(arrowstyle="-", color=BLUE, lw=.8))
ax[0].set_title("The fouling curve — plate opening the Supra needed to hold its hot idle target, April → September 2026", loc="left", fontsize=12)
ax[0].text(0.01, 0.97, "every log with idle channels · settled ACTIVE idle, CLT ≥ 90, |RPM − target| ≤ 60 · orange = fouled throttle body, blue = clean" + chr(10) +
           "dot = median per log (size ∝ samples, value shown when ≥ 1000 samples), whisker = p10–p90 · pre-relearn TPS shifted −1.09 (one TPS calibration all year, V₀ 0.680 → 0.720 at the relearn)",
           transform=ax[0].transAxes, va="top", fontsize=8.2, color=INK2)
have = h[h.op.notna()]
for clean, col in [(False, ORANGE), (True, BLUE)]:
    g = have[have.clean == clean]; ax[2].scatter(g.date, g.op, s=26, color=col, edgecolor=SURF, linewidth=1, zorder=3)
ax[2].set_ylabel("oil pressure" + chr(10) + "[bar]"); ax[2].set_ylim(1, 5); ax[2].grid(axis="y")
ax[2].text(0.01, 0.93, "thicker oil needs a little more opening (≈ 0.4 % TPS per bar): the Sep 19 morning 4.8 was at 4.0 bar, the 3.9 at 1.8 bar — the September step is ~1.5 % TPS beyond that",
           transform=ax[2].transAxes, va="top", fontsize=8.2, color=INK2)
ax[2].xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b %d"))
fig.savefig(OUT + "/fouling_history.png", dpi=130, bbox_inches="tight"); plt.close(fig)

# ---------- Figure 3 (redo): flow vs position, matched-air connectors instead of pooled fits ----------
df = load()
st = df["Idle state"].values; t = df["TIME"].values; last = -1e9; ent = np.full(len(df), np.nan)
for i in range(len(df)):
    if st[i] == 2 and (i == 0 or st[i-1] != 2): last = t[i]
    if st[i] == 2: ent[i] = t[i] - last
df["t_in"] = ent
k = df[(df["Idle state"] == 2) & (df["t_in"] > 3) & (df["CLT"] >= 45) & (df["RPM"] - df["Idle target"]).abs().le(40) & (df["MAP"] < 60) & (df["PPS"] == 0)].copy()
k["clean"] = k["TIME"] > 640; k["tps_f"] = np.where(k["clean"], k["TPS"], k["TPS"] - SHIFT)
fig, ax = plt.subplots(figsize=(11, 6.4))
for flag, col, lab in [(False, ORANGE, "fouled (morning)"), (True, BLUE, "clean (afternoon)")]:
    s = k[k["clean"] == flag]; ax.scatter(s["tps_f"], s["MR"], s=8, alpha=.2, color=col, edgecolor="none", label=lab)
def med(flag, lo, hi):
    s = k[(k["clean"] == flag) & k["MR"].between(lo, hi)]; return s["tps_f"].median(), s["MR"].median(), len(s)
for lo, hi, lab in [(35, 39, "1025 rpm, CLT 96"), (45, 48, "≈1300 rpm, CLT 75"), (50, 53, "≈1460 rpm, CLT 60")]:
    xd, yd, nd = med(False, lo, hi); xc, yc, nc = med(True, lo, hi); y = (yd + yc) / 2
    ax.annotate("", xy=(xc, y), xytext=(xd, y), arrowprops=dict(arrowstyle="<-", color=INK2, lw=1.1))
    ax.text((xc + xd) / 2, y + 0.5, f"{lab}: −{xd - xc:.1f} % TPS for the same air", ha="center", fontsize=8.5, color=INK)
    print(lab, "dirty", round(xd, 2), "clean", round(xc, 2), "delta", round(xd - xc, 2), nd, nc)
p = k[k["clean"] & k["Idle target"].between(1200, 1250) & (k["TIME"] > 1640)]; q = k[k["clean"] & (k["Idle target"] == 1025) & (k["TIME"] > 1640)]
ax.plot([q.tps_f.median(), p.tps_f.median()], [q.MR.median(), p.MR.median()], color=BLUE, lw=1.5, ls="--")
ax.text(p.tps_f.median() + 0.12, p.MR.median() + 1.2, "soaked: 1025 → 1225 rpm\nposition ∝ RPM", fontsize=8.5, color=BLUE, va="bottom")

ax.set_xlim(1.6, 6.4); ax.set_ylim(30, 58); ax.grid(alpha=.6)
ax.set_xlabel("plate position  [% TPS, one frame]"); ax.set_ylabel("air the engine took at that position   MAP × RPM / 1000")
ax.set_title("What cleaning did to airflow: the same air now comes through a plate 1.1–2.3 % TPS further closed", loc="left", fontsize=12)
ax.text(0.02, 0.95, "settled idle samples, both throttle bodies, same day · RPM rises left→right within each colour (1025 hot → 1500 during warm-up)\n"
        "the gap is widest at small openings — a deposit ring eats more of a thin crescent than of a wide one", transform=ax.transAxes, va="top", fontsize=8.5, color=INK2)
ax.legend(frameon=False, loc="lower right")
fig.tight_layout(); fig.savefig(OUT + r"\flow_characteristic_fouled_vs_clean.png", dpi=130); plt.close(fig)
print("done")
