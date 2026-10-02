"""Challenge the assumptions behind each before/after test (Will, 2026-10-02: scientific method).
Idle conditions, lambda target, closed-loop activity, timing, fuel era, timing of the change. -> data/assumptions.json"""
import os, sys, json, pickle, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "skills", "emu-black-idle-stability", "scripts"))
import idle_stability as IS
A, F = pickle.load(open(os.path.join(HERE, "..", "data", "eb_all.pkl"), "rb"))
A = A.sort_values(["file", "TIME"])
last_stop = A.TIME.where(A.RPM < 200).groupby(A.file, observed=True).ffill()
A["since_start"] = (A.TIME - last_stop).fillna(1e6)
A = A[A.RPM > 500].copy()
A["g"] = np.where(A["Injector 6 trim"] > 100, 1, 0)
A["fuel"] = np.where(A["Ethanol content"] > 45, "E57", np.where(A["Ethanol content"] > 20, "E25", np.where(A["Ethanol content"] > 11, "E14", "E9")))
OUT = {}
pd.set_option("display.width", 220)

def idle_mask(d):
    tdt = d.TIME.diff(IS.RATE_K); slew = (d.RPM.diff(IS.RATE_K) / tdt.where(tdt > 0)).abs()
    tc = np.nanpercentile(d.TPS, IS.TPS_CLOSED_PCT)
    return ((d["Idle state"] == 2) & (d.TPS <= tc + IS.TPS_MARGIN) & d.RPM.between(IS.RPM_LO, IS.RPM_HI)
            & (slew.fillna(0) <= IS.RATE_MAX) & (d.CLT >= IS.WARM_CLT) & (d.since_start >= 120)).fillna(False)

frames = []
for f, d in A.groupby("file", observed=True):
    d = d.reset_index(drop=True)
    m = idle_mask(d)
    if m.sum() < 100: continue
    lam = d["Lambda 1"]; lv = d["Lambda is valid"] > 0.5
    med = lam.rolling(15, center=True, min_periods=1).median()
    d["rich2"] = lv & (lam - med < -0.02)
    d["rich2_start"] = d.rich2 & ~d.rich2.shift(1, fill_value=False)
    tchg = d["Lambda target"].diff().abs() > 1e-4
    d["tgt_change_near"] = tchg.rolling(25, center=True, min_periods=1).max().astype(bool)   # +-0.5 s
    d["stft_step"] = d["Short term trim"].diff().abs()
    frames.append(d[m])
I = pd.concat(frames, ignore_index=True)

# 1. idle conditions before vs after
cond = I.groupby("g").agg(min=("RPM", lambda x: round(len(x) / 1500, 1)), rpm=("RPM", "median"), idle_tgt=("Idle target", "median"),
                          lam_tgt=("Lambda target", "median"), lam_tgt_p10=("Lambda target", lambda x: x.quantile(.1)), lam_tgt_p90=("Lambda target", lambda x: x.quantile(.9)),
                          lam=("Lambda 1", "median"), stft=("Short term trim", "median"), stft_sd=("Short term trim", "std"),
                          stft_nonzero=("Short term trim", lambda x: 100 * (x.abs() > 0.1).mean()),
                          ign=("Ignition Angle", "median"), clt=("CLT", "median"), iat=("IAT", "median"), eth=("Ethanol content", "median"),
                          pw=("Injectors PW", "median"), map=("MAP", "median"), batt=("Battery voltage", "median"))
print("idle conditions\n", cond.round(3).T)
OUT["idle_conditions"] = cond.round(4).reset_index().to_dict("records")

# 2. are rich blips tied to lambda-target changes or closed-loop corrections?
starts = I[I.rich2_start]
tie = I.groupby("g").apply(lambda d: pd.Series(dict(
    blips=int(d.rich2_start.sum()), per_min=round(d.rich2_start.sum() / (len(d) / 1500), 3),
    pct_near_target_change=round(100 * float(d.loc[d.rich2_start, "tgt_change_near"].mean()), 1) if d.rich2_start.sum() else None,
    base_near_target_change=round(100 * float(d.tgt_change_near.mean()), 1),
    stft_step_at_blip=round(float(d.loc[d.rich2_start, "stft_step"].mean()), 3) if d.rich2_start.sum() else None,
    stft_step_base=round(float(d.stft_step.mean()), 3))))
print("rich blips vs target changes / STFT\n", tie)
OUT["blip_ties"] = tie.reset_index().to_dict("records")

# 3. blip rate by fuel era and by date window (is it the switch, or a drift?)
I["era"] = np.where(I.g == 0, "before ", "after ") + I.fuel
era = I.groupby("era").agg(min=("RPM", lambda x: round(len(x) / 1500, 1)), per_min=("rich2_start", lambda x: round(x.sum() / (len(x) / 1500), 3)))
print("rich blips by fuel era\n", era)
OUT["blip_era"] = era.reset_index().to_dict("records")
I["day"] = I.file.astype(str).str[:8]
win = [("Mar 1-28", "20260301", "20260328"), ("Mar 29-Apr 19", "20260329", "20260419"), ("Apr 20-May 4", "20260420", "20260504"),
       ("May 4-10", "20260504", "20260510"), ("May 11-Aug 21", "20260511", "20260821"), ("Aug 22-Sep 29", "20260822", "20260929")]
wr = []
for lab, a, b in win:
    x = I[(I.day >= a) & (I.day <= b)]
    for g in (0, 1):
        y = x[x.g == g]
        if len(y) > 1500: wr.append(dict(window=lab, g=g, min=round(len(y) / 1500, 1), per_min=round(float(y.rich2_start.sum() / (len(y) / 1500)), 3), lam_tgt=round(float(y["Lambda target"].median()), 3), stft_sd=round(float(y["Short term trim"].std()), 2)))
print("rich blips by date window\n", pd.DataFrame(wr))
OUT["blip_windows"] = wr

# 4. knock tests: idle ignition and knock-config proxies by group (sensor/gain unverified before 05-22 exports)
OUT["idle_ign"] = I.groupby("g")["Ignition Angle"].describe()[["25%", "50%", "75%"]].round(2).reset_index().to_dict("records")
print("idle ignition angle\n", I.groupby("g")["Ignition Angle"].describe()[["25%", "50%", "75%"]])

# 5. lambda target in each region, before vs after (Will's question)
fuel_on = A["Injectors PW"] > 0.3
A["reg"] = ""
A.loc[fuel_on & A.MAP.between(105, 175) & A.RPM.between(3500, 6000), "reg"] = "boost"
A.loc[fuel_on & (A.reg == "") & A.MAP.between(30, 95) & A.RPM.between(1500, 4000), "reg"] = "cruise"
A["rc"] = (A.RPM // 250).astype(int); A["mc"] = (A.MAP // 10).astype(int)
lt = []
for rg in ("cruise", "boost"):
    c = A[A.reg == rg]
    m = c.groupby(["rc", "mc", "g"])["Lambda target"].mean().unstack("g"); n = c.groupby(["rc", "mc", "g"]).size().unstack("g").min(axis=1)
    ok = m.notna().all(axis=1) & (n > 200)
    lt.append(dict(reg=rg, before=round(float(np.average(m.loc[ok, 0], weights=n[ok])), 3), after=round(float(np.average(m.loc[ok, 1], weights=n[ok])), 3)))
lt.append(dict(reg="idle", before=round(float(I[I.g == 0]["Lambda target"].median()), 3), after=round(float(I[I.g == 1]["Lambda target"].median()), 3)))
print("lambda target, same cells\n", pd.DataFrame(lt))
OUT["lambda_target"] = lt
json.dump(OUT, open(os.path.join(HERE, "..", "data", "assumptions.json"), "w"), default=float)
