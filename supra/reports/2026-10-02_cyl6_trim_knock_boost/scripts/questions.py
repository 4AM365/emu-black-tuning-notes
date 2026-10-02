"""The two questions, threshold-free: did knock peaks drop, did idle misfire drop?
Reads data/eb_all.pkl (decode_autosaves.py) -> data/questions.json.

Knock peaks: share of samples where Knock voltage peak cyl N exceeds k x its 250 rpm x 10 kPa cell median
(median pooled over the compared periods), swept over k.
Idle misfire proxies (no misfire channel exists): in steady warm idle (Idle state 2, closed TPS, slew < 300 rpm/s,
CLT >= 80, segments >= 4 s), count
  - RPM dips: runs where RPM falls more than d rpm below its centred 0.28 s (7-sample) rolling median, swept over d.
    The short window passes a sharp lost-firing sag but removes the ~1 Hz idle-PID hunt (a 1 s window counted hunt troughs);
  - rich lambda blips: runs where Lambda 1 drops more than x below its centred 0.6 s (15-sample) rolling median (lambda valid).
    A misfire reads RICH on this wideband (Will, 2026-10-02); an earlier version counted lean blips, which was wrong.
  RPM sags are computed but NOT used as a misfire metric: idle RPM is dominated by the throttle-body problems (Will, 2026-10-02).
Rates are events per minute of steady idle."""
import os, sys, json, pickle, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "skills", "emu-black-idle-stability", "scripts"))
import idle_stability as IS

A, F = pickle.load(open(os.path.join(HERE, "..", "data", "eb_all.pkl"), "rb"))
A = A[A.RPM > 500].copy()
t6, eth = A["Injector 6 trim"], A["Ethanol content"]
A["g"] = -1
A.loc[t6 == 100, "g"] = 0      # before trim
A.loc[t6 > 100, "g"] = 1       # after trim (2026-05-04 17:38 on)
A = A[A.g >= 0]
fuel = A["Injectors PW"] > 0.3
K = [f"Knock voltage peak cyl {c}" for c in range(1, 7)]
OUT = {}

# ---- knock peaks: exceedance curves
A["reg"] = ""
A.loc[fuel & A.MAP.between(105, 175) & A.RPM.between(3500, 6000), "reg"] = "boost"
A.loc[fuel & (A.reg == "") & A.MAP.between(30, 95) & A.RPM.between(1500, 4000), "reg"] = "cruise"
A.loc[fuel & (A.reg == "") & (A.RPM < 1400) & (A["Idle state"] == 2) & (A.CLT >= 80), "reg"] = "idle"
S = A[A.reg != ""].copy()
S["rc"] = (S.RPM // 250).astype(int); S["mc"] = (S.MAP // 10).astype(int)
KS = [round(x, 2) for x in np.arange(1.25, 3.01, 0.25)]
exc = []
for c in range(1, 7):
    r = S[K[c - 1]] / S.groupby(["reg", "rc", "mc"])[K[c - 1]].transform("median")
    for (rg, g), rr in r.groupby([S.reg, S.g]):
        exc.append(dict(reg=rg, g=int(g), cyl=c, n=int(len(rr)), pct=[round(100 * float((rr > k).mean()), 4) for k in KS]))
    if c == 6: S["r6"] = r
OUT["knock"] = dict(ks=KS, rows=exc)
# per drive, cyl 6, idle and boost, share above 2x
pd_rows = []
for (f, rg), d in S.groupby(["file", "reg"], observed=True):
    if (rg == "idle" and len(d) >= 1500) or (rg == "boost" and len(d) >= 250):
        pd_rows.append(dict(f=f, reg=rg, g=int(d.g.mode()[0]), n=int(len(d)), p15=round(100 * float((d.r6 > 1.5).mean()), 3), p20=round(100 * float((d.r6 > 2).mean()), 3)))
OUT["knock_drive"] = pd_rows

# ---- idle misfire proxies
DS = [5, 10, 15, 20, 25, 30, 40, 50]                # RPM dip depth, rpm
XS = [0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.06]   # rich blip size, lambda
def runs_over(mask):
    m = np.asarray(mask, bool)
    return int(np.sum(m[1:] & ~m[:-1]) + (1 if len(m) and m[0] else 0))
tot = {g: dict(min=0.0, dips=np.zeros(len(DS)), lmin=0.0, lean=np.zeros(len(XS))) for g in (0, 1)}
drives = []
for f, d in A.groupby("file", observed=True):
    d = d.sort_values("TIME").reset_index(drop=True)
    dt = 0.04
    tdt = d.TIME.diff(IS.RATE_K); slew = (d.RPM.diff(IS.RATE_K) / tdt.where(tdt > 0)).abs()
    tc = np.nanpercentile(d.TPS, IS.TPS_CLOSED_PCT)
    m = (d["Idle state"] == 2) & (d.TPS <= tc + IS.TPS_MARGIN) & d.RPM.between(IS.RPM_LO, IS.RPM_HI) & (slew.fillna(0) <= IS.RATE_MAX) & (d.CLT >= IS.WARM_CLT)
    tw = max(3, int(round(IS.TREND_S / dt)) | 1)
    fd = dict(min=0.0, dips=np.zeros(len(DS)), lmin=0.0, lean=np.zeros(len(XS)), g=[])
    for a, b in IS.runs(m.fillna(False), dt):
        seg = d.iloc[a:b + 1]
        rpm = seg.RPM.values.astype(float)
        res = rpm - pd.Series(rpm).rolling(7, center=True, min_periods=1).median().values
        lam = seg["Lambda 1"].values.astype(float); lv = seg["Lambda is valid"].values > 0.5
        lres = lam - pd.Series(lam).rolling(15, center=True, min_periods=1).median().values
        mins = len(seg) * dt / 60; g = int(seg.g.mode()[0])
        dips = np.array([runs_over(res < -x) for x in DS], float)
        lean = np.array([runs_over(lv & (lres < -x)) for x in XS], float)   # rich blips (key kept as 'lean' for the page)
        lmin = lv.sum() * dt / 60
        for T in (tot[g], fd):
            T["min"] += mins; T["dips"] += dips; T["lmin"] += lmin; T["lean"] += lean
        fd["g"].append(g)
    if fd["min"] >= 1:
        drives.append(dict(f=f, g=int(pd.Series(fd["g"]).mode()[0]), min=round(fd["min"], 1),
                           dip15=round(fd["dips"][DS.index(15)] / fd["min"], 2), dip25=round(fd["dips"][DS.index(25)] / fd["min"], 3),
                           rich2=round(fd["lean"][XS.index(0.02)] / fd["lmin"], 3) if fd["lmin"] >= 1 else None))
OUT["misfire"] = dict(ds=DS, xs=XS, groups=[dict(g=g, min=round(T["min"], 1), lmin=round(T["lmin"], 1),
                      dips=[round(v / T["min"], 3) for v in T["dips"]], lean=[round(v / T["lmin"], 3) for v in T["lean"]]) for g, T in tot.items()])
OUT["misfire_drive"] = drives
# example idle traces: for each period, the drive whose >50 rpm dip rate is closest to its period's pooled rate; first 30 s of its longest steady segment
D = pd.DataFrame(drives); traces = []
for g in (0, 1):
    target = OUT["misfire"]["groups"][g]["lean"][XS.index(0.02)]
    f = D[(D.g == g) & (D["min"] >= 3) & D.rich2.notna()].assign(dd=lambda x: (x.rich2 - target).abs()).sort_values("dd").f.iloc[0]
    d = A[A.file == f].sort_values("TIME").reset_index(drop=True)
    tdt = d.TIME.diff(IS.RATE_K); slew = (d.RPM.diff(IS.RATE_K) / tdt.where(tdt > 0)).abs()
    tc = np.nanpercentile(d.TPS, IS.TPS_CLOSED_PCT)
    m = (d["Idle state"] == 2) & (d.TPS <= tc + IS.TPS_MARGIN) & d.RPM.between(IS.RPM_LO, IS.RPM_HI) & (slew.fillna(0) <= IS.RATE_MAX) & (d.CLT >= IS.WARM_CLT)
    a0, b0 = max(IS.runs(m.fillna(False), 0.04), key=lambda r: r[1] - r[0])
    mid = (a0 + b0) // 2; s = d.iloc[max(a0, mid - 375):min(b0, mid + 375) + 1]   # middle 30 s
    traces.append(dict(g=g, f=f, rate=float(D[D.f == f].rich2.iloc[0]), t=(s.TIME - s.TIME.iloc[0]).round(2).tolist(), rpm=s.RPM.astype(int).tolist(),
                       tgt=s["Idle target"].astype(int).tolist(), lam=[(round(float(v), 3) if ok > 0.5 else None) for v, ok in zip(s["Lambda 1"], s["Lambda is valid"])], k6=s[K[5]].round(3).tolist()))
OUT["idle_traces"] = traces
json.dump(OUT, open(os.path.join(HERE, "..", "data", "questions.json"), "w"), separators=(",", ":"))

for G in OUT["misfire"]["groups"]:
    print("g", G["g"], "idle min", G["min"], "dips/min", dict(zip(DS, G["dips"])), "\n     lean/min", dict(zip(XS, G["lean"])))
for rg in ("idle", "boost", "cruise"):
    for c in (1, 6):
        print(rg, "cyl", c, {r["g"]: r["pct"][KS.index(2.0)] for r in exc if r["reg"] == rg and r["cyl"] == c}, "(>2x)")
D = pd.DataFrame(drives); print(D.groupby("g")[["dip15", "dip25", "rich2"]].median())
