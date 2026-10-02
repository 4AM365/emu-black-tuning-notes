"""Before/after per-cylinder trim on decoded LogAutosave data (Mar 1 - Sep 29 2026).
Groups are assigned per SAMPLE from logged Injector 6 trim (100 = no trim) and Ethanol content."""
import sys, os, pickle, json, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
SK = r"C:/Code/car-projects/emu-black-tuning-notes/skills"
sys.path.insert(0, SK + "/emu-black-idle-stability/scripts"); sys.path.insert(0, SK + "/emu-black-knock-cov/scripts")
import idle_stability as IS
import knock_chatter_cov as KC

A, F = pickle.load(open(os.path.join(HERE, "..", "data", "eb_all.pkl"), "rb"))
A = A[A.RPM > 500].copy()
GROUPS = ["Before trim (Mar 1 – May 4)", "After trim (May 4 – Sep 29)"]
t6, eth = A["Injector 6 trim"], A["Ethanol content"]
A["g"] = -1
A.loc[t6 == 100, "g"] = 0      # before: no trim (2026-05-04 17:25 and earlier)
A.loc[t6 > 100, "g"] = 1       # after: trim live (2026-05-04 17:38 on)
print(A.groupby("g").agg(min=("RPM", lambda x: round(len(x) / 1500)), files=("file", "nunique"),
                          d0=("day", lambda x: min(x.astype(str))), d1=("day", lambda x: max(x.astype(str)))))
fuel = A["Injectors PW"] > 0.3
A["reg"] = ""
A.loc[fuel & A.MAP.between(105, 175) & A.RPM.between(3500, 6000), "reg"] = "boost"   # MAP range both sides reach
A.loc[fuel & (A.reg == "") & A.MAP.between(30, 95) & A.RPM.between(1500, 4000), "reg"] = "cruise"
A.loc[fuel & (A.reg == "") & (A.RPM < 1400) & (A["Idle state"] == 2) & (A.CLT >= 80), "reg"] = "idle"
A["rc"] = (A.RPM // 250).astype(int); A["mc"] = (A.MAP // 10).astype(int)
K = [f"Knock voltage peak cyl {c}" for c in range(1, 7)]
OUT = {"groups": GROUPS}

# ---- spikes: knock voltage / pooled cell median (cells RPM 250 x MAP 10, baseline pooled over groups 0-2)
S = A[(A.reg != "") & A.g.isin([0, 1])].copy()
spk = []
for c in K:
    med = S.groupby(["reg", "rc", "mc"])[c].transform("median")
    S["r" + c[-1]] = S[c] / med
for (rg, g), d in S.groupby(["reg", "g"]):
    for c in range(1, 7):
        r = d["r%d" % c]
        spk.append(dict(reg=rg, g=int(g), cyl=c, n=int(len(r)), min=round(len(r) / 1500, 1),
                        p15=round(100 * float((r > 1.5).mean()), 3), p20=round(100 * float((r > 2.0).mean()), 3),
                        per_min15=round(float((r > 1.5).sum()) / (len(r) / 1500), 2)))
OUT["spikes"] = spk
SP = pd.DataFrame(spk)
print(SP.pivot_table(index=["reg", "cyl"], columns="g", values="p15").round(2).to_string())
print(SP.pivot_table(index=["reg", "cyl"], columns="g", values="p20").round(3).to_string())
# per-file cyl6 spike rate (boost, cruise) for the timeline
pf = S.groupby(["file", "reg"], observed=True).agg(g=("g", lambda x: int(x.mode()[0])), n=("r6", "size"),
                                                   p15=("r6", lambda x: 100 * (x > 1.5).mean())).reset_index()
pf2 = S.groupby(["file", "reg"], observed=True).r6.agg(lambda x: 100 * (x > 2).mean()).rename("p20").reset_index()
pf = pf.merge(pf2, on=["file", "reg"]); pf = pf[pf.n >= 1500]   # at least 1 min in the region
OUT["spk_file"] = [dict(f=r.file, day=r.file[:8], reg=r.reg, g=int(r.g), n=int(r.n), p15=round(float(r.p15), 2), p20=round(float(r.p20), 3)) for r in pf.itertuples()]
A["r6"] = np.nan; A.loc[S.index, "r6"] = S["r6"]
# spikes by boost bin (cyl6), to show where in boost they disappear
B = S[(S.reg == "boost")].copy(); B["bb"] = np.clip((B.Boost // 10) * 10, 0, 90).astype(int)
OUT["spk_bins"] = [dict(g=int(g), bin=int(b), n=int(len(d)), p15=round(100 * float((d.r6 > 1.5).mean()), 2))
                   for (g, b), d in B.groupby(["g", "bb"]) if len(d) >= 50]

# ---- knock cyl6 vs boost: binned distribution, RPM 4000-5500
Q = A[A.g.isin([0, 1]) & fuel & A.RPM.between(4000, 5500) & (A.MAP >= 95)].copy()
Q["bb"] = np.clip((Q.Boost // 10) * 10, 0, 90).astype(int)
def q(v): v = np.asarray(v, float); return {k: round(float(np.percentile(v, p)), 3) for k, p in [("p25", 25), ("med", 50), ("p75", 75), ("p95", 95), ("p99", 99)]}
OUT["bins"] = [dict(g=int(g), bin=int(b), n=int(len(d)), **q(d[K[5]])) for (g, b), d in Q.groupby(["g", "bb"]) if len(d) >= 30]
# scatter subsample
rng = np.random.default_rng(1)
sc = A[A.g.isin([0, 1]) & fuel & (A.Boost > 5) & A.RPM.between(3000, 6500)]
pts = []
for g, d in sc.groupby("g"):
    d = d.sample(min(2500, len(d)), random_state=1)
    pts += [[float(b), round(float(k), 3), int(r), int(g), f] for b, k, r, f in zip(d.Boost, d[K[5]], d.RPM, d.file.astype(str))]
OUT["scatter"] = pts
OUT["scatter_n"] = {int(g): int(len(d)) for g, d in sc.groupby("g")}

# ---- ratio cyl6 / mean(cyl1-5) by MAP
R = A[A.g.isin([0, 1]) & fuel & A.RPM.between(2000, 5500) & A.MAP.between(20, 190)].copy()
oth = R[K[:5]].mean(axis=1); R = R[oth > 0.05]; R["ratio"] = R[K[5]] / oth[R.index]
OUT["ratio"] = [dict(g=int(g), map=int(m) * 10, n=int(len(d)), **q(d.ratio)) for (g, m), d in R.groupby(["g", "mc"]) if len(d) >= 50]

# ---- knock CoV, skill method (detrend RPM250 x MAP10, positive transients); no-knock gate unavailable (channels not in binary)
cov = []
for thr in (100, 130):
    for g in (0, 1):
        frames = []
        for f, d in A[A.g == g].groupby("file", observed=True):
            d = d.sort_values("TIME")
            dt = d.TIME.diff(KC.RATE_K)
            trans = (d.RPM.diff(KC.RATE_K) / dt > KC.POS_RPM_RATE) | (d.MAP.diff(KC.RATE_K) / dt > KC.POS_MAP_RATE)
            frames.append(d[(d.MAP > thr) & trans][["RPM", "MAP", K[5]]].rename(columns={K[5]: KC.KCH}))
        dd = KC.detrend(pd.concat(frames, ignore_index=True))
        cov.append(dict(thr=thr, g=g, n=int(len(dd)), cov=round(float(dd.resid_norm.std() * 100), 1)))
OUT["cov"] = cov; print(pd.DataFrame(cov))

# ---- idle quality: skill runs()/pool() with an Idle-state-2 + closed-TPS + slew gate, warm (CLT >= 80)
idle_rows = {0: [], 1: []}; per_file = []
for f, d in A[A.g.isin([0, 1])].groupby("file", observed=True):
    d = d.sort_values("TIME").reset_index(drop=True)
    dt = 0.04
    tdt = d.TIME.diff(IS.RATE_K); slew = (d.RPM.diff(IS.RATE_K) / tdt.where(tdt > 0)).abs()
    tc = np.nanpercentile(d.TPS, IS.TPS_CLOSED_PCT)
    m = (d["Idle state"] == 2) & (d.TPS <= tc + IS.TPS_MARGIN) & d.RPM.between(IS.RPM_LO, IS.RPM_HI) & (slew.fillna(0) <= IS.RATE_MAX) & (d.CLT >= IS.WARM_CLT)
    tw = max(3, int(round(IS.TREND_S / dt)) | 1)
    rows = []
    for a, b in IS.runs(m.fillna(False), dt):
        seg = d.iloc[a:b + 1]
        rpm = seg.RPM.values.astype(float); tgt = seg["Idle target"].values.astype(float)
        trend = pd.Series(rpm).rolling(tw, center=True, min_periods=1).mean().values
        lam = seg["Lambda 1"].values.astype(float); lv = seg["Lambda is valid"].values > 0.5
        lt = pd.Series(lam).rolling(tw, center=True, min_periods=1).mean().values
        g = int(seg.g.mode()[0])
        rows.append(dict(g=g, regime="warm", dur=len(seg) * dt, clt=float(seg.CLT.median()), tgt_band=0, rpm=rpm, tgt=tgt, e=rpm - tgt,
                         resid=rpm - trend, mean_rpm=float(rpm.mean()), lres=(lam - lt)[lv], lam=lam[lv]))
    for r in rows: idle_rows[r["g"]].append(r)
    if rows:
        m2 = IS.pool(rows)
        per_file.append(dict(f=f, day=f[:8], g=int(pd.Series([r["g"] for r in rows]).mode()[0]), dur=round(m2["dur"]), jit=round(m2["jit"], 3),
                             hold=round(m2["cov"], 2), rms=round(m2["rms"], 1), ljit=round(float(np.std(np.concatenate([r["lres"] for r in rows])) * 100), 3) if sum(len(r["lres"]) for r in rows) > 50 else None))
idle = []
for g, rows in idle_rows.items():
    m2 = IS.pool(rows)
    lres = np.concatenate([r["lres"] for r in rows]); lam = np.concatenate([r["lam"] for r in rows])
    idle.append(dict(g=g, segs=len(rows), dur_min=round(m2["dur"] / 60, 1), mean_rpm=round(m2["mean_rpm"]), jit=round(m2["jit"], 3), hold=round(m2["cov"], 2),
                     rms=round(m2["rms"], 1), p50=round(m2["p50"], 1), lam_jit=round(float(np.std(lres)) * 100, 3), lam_mean=round(float(np.mean(lam)), 3)))
OUT["idle"] = idle; OUT["idle_file"] = per_file
print(pd.DataFrame(idle).to_string())
PF = pd.DataFrame(per_file); print(PF.groupby("g")[["jit", "hold", "ljit"]].describe().round(3).T.to_string())

# ---- EGT spread cyl6-cyl3 by band, MAP held in band 2 s
egt = []
BANDS = [("idle", 0, 45, 0, 1400), ("light", 25, 60, 1400, 9000), ("cruise", 60, 95, 1400, 9000), ("transition", 95, 130, 1400, 9000), ("boost", 130, 400, 1400, 9000)]
eg = []
for f, d in A[A.g.isin([0, 1])].groupby("file", observed=True):
    d = d.sort_values("TIME")
    ok = fuel[d.index] & (d["EGT 1"] > 250) & (d["EGT 2"] > 250) & (d.CLT > 70)
    for b, m0, m1, r0, r1 in BANDS:
        inb = (d.MAP >= m0) & (d.MAP < m1) & (d.RPM >= r0) & (d.RPM < r1)
        held = inb.rolling(50, min_periods=50).min().fillna(0).astype(bool)
        s = d[held & ok]
        if len(s): eg.append(pd.DataFrame({"g": s.g.values, "band": b, "f": f, "dl": (s["EGT 2"] - s["EGT 1"]).values}))
EG = pd.concat(eg)
for (g, b), d in EG.groupby(["g", "band"]):
    perf = d.groupby("f").dl.agg(["mean", "size"]); perf = perf[perf["size"] >= 25]
    if len(d) >= 50: egt.append(dict(g=int(g), band=b, mean=round(float(d.dl.mean()), 1), n=int(len(d)), files=int(len(perf)),
                                     lo=round(float(perf["mean"].min()), 1) if len(perf) else None, hi=round(float(perf["mean"].max()), 1) if len(perf) else None))
OUT["egt"] = egt; print(pd.DataFrame(egt).pivot_table(index="band", columns="g", values="mean").to_string())

# ---- boost pulls
pulls = []
for f, d in A.groupby("file", observed=True):
    d = d.sort_values("TIME").reset_index(drop=True)
    ev = (d.Boost.fillna(0) > 20).astype(int).values; ed = np.flatnonzero(np.diff(np.r_[0, ev, 0]))
    for a, b in zip(ed[::2], ed[1::2]):
        if (b - a) * 0.04 < 0.5: continue
        seg = d.iloc[a:b]; w = d.iloc[a:min(len(d), b + 38)]
        pulls.append(dict(f=f, day=f[:8], g=int(seg.g.mode()[0]), dur=round((b - a) * 0.04, 1), peak=float(seg.Boost.max()), tgt=round(float(seg["Boost Target"].max()), 1),
                          pps=round(float(seg.PPS.max()), 0), rpm_hi=int(seg.RPM.max()), d=float(w["EGT 2"].max() - w["EGT 1"].max()),
                          k6max=round(float(seg[K[5]].max()), 2), spk=round(100 * float((seg.r6.dropna() > 1.5).mean()), 1) if seg.r6.notna().sum() else None))
OUT["pulls"] = pulls
P = pd.DataFrame(pulls); print(P.groupby("g").agg(n=("peak", "size"), med=("peak", "median"), mx=("peak", "max"), tmx=("tgt", "max"), d=("d", "median")).to_string())

# ---- matched pull timelines: hardest WOT pull in group 0 vs closest-peak WOT pull in group 1
def tl(row):
    d = A[A.file == row["f"]].sort_values("TIME").reset_index(drop=True)
    i = int(np.flatnonzero((d.Boost > 20).values & (d.Boost == row["peak"]).values)[0])
    a = i;
    while a > 0 and d.Boost.iloc[a] > 20: a -= 1
    s = d.iloc[max(0, a - 75):min(len(d), i + 60)]
    t = (s.TIME - s.TIME.iloc[0]).round(2)
    return dict(log=row["f"], g=int(row["g"]), t=t.tolist(), boost=s.Boost.tolist(), k6=s[K[5]].round(3).tolist(), rpm=s.RPM.astype(int).tolist())
W = P[(P.pps >= 90) & (P.dur >= 1.5)]
pairs = []
for pk in (W[W.g == 0].sort_values("peak", ascending=False).head(1).itertuples(),):
    for r0 in pk:
        cand = W[W.g == 1].sort_values("peak", ascending=False).head(1)
        if len(cand): pairs.append(dict(label=f"Hardest full-pedal pull each side: {r0.peak:.0f} kPa ({r0.f[4:6]}-{r0.f[6:8]}) vs {cand.peak.iloc[0]:.0f} kPa ({cand.f.iloc[0][4:6]}-{cand.f.iloc[0][6:8]})",
                                        before=tl(r0._asdict()), after=tl(cand.iloc[0].to_dict())))
med0 = W[W.g == 0].peak.median()
r0 = W[W.g == 0].assign(dd=(W.peak - 60).abs()).sort_values("dd").iloc[0]; r1 = W[W.g == 1].assign(dd=(W.peak - r0.peak).abs()).sort_values("dd").iloc[0]
pairs.append(dict(label=f"Matched full-pedal pulls near 60–70 kPa: {r0.peak:.0f} kPa ({r0.f[4:6]}-{r0.f[6:8]}) vs {r1.peak:.0f} kPa ({r1.f[4:6]}-{r1.f[6:8]})", before=tl(r0.to_dict()), after=tl(r1.to_dict())))
OUT["pulls_tl"] = pairs

# ---- file table
ft = A.groupby("file", observed=True).agg(g=("g", lambda x: int(x.mode()[0])), min=("RPM", lambda x: round(len(x) / 1500, 1)), eth=("Ethanol content", "median"),
                                          t6=("Injector 6 trim", "median"), t3=("Injector 3 trim", "median"), boost_s=("Boost", lambda x: round(float((x > 20).sum()) * 0.04, 1))).reset_index()
OUT["files"] = [dict(f=r.file, g=int(r.g), min=float(r.min), eth=float(r.eth), t6=float(r.t6), t3=float(r.t3), boost_s=float(r.boost_s)) for r in ft.itertuples()]
json.dump(OUT, open(os.path.join(HERE, "..", "data", "report_data.json"), "w"), separators=(",", ":"))
print("json kB", os.path.getsize(os.path.join(HERE, "..", "data", "report_data.json")) // 1000)
