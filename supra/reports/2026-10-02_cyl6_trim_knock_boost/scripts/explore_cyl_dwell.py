"""Follow-up: per-cylinder knock peaks (trim differently vs enrich?) and coil dwell. Binary split at the trim.
Reads data/eb_all.pkl -> data/explore.json and prints the tables."""
import os, json, pickle, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
A, F = pickle.load(open(os.path.join(HERE, "..", "data", "eb_all.pkl"), "rb"))
A = A[A.RPM > 500].copy()
A["g"] = np.where(A["Injector 6 trim"] > 100, 1, 0)
fuel = A["Injectors PW"] > 0.3
K = {c: f"Knock voltage peak cyl {c}" for c in range(1, 7)}
A["reg"] = ""
A.loc[fuel & A.MAP.between(105, 175) & A.RPM.between(3500, 6000), "reg"] = "boost"
A.loc[fuel & (A.reg == "") & A.MAP.between(30, 95) & A.RPM.between(1500, 4000), "reg"] = "cruise"
A.loc[fuel & (A.reg == "") & (A.RPM < 1400) & (A["Idle state"] == 2) & (A.CLT >= 80), "reg"] = "idle"
S = A[A.reg != ""].copy()
S["rc"] = (S.RPM // 250).astype(int); S["mc"] = (S.MAP // 10).astype(int)
for c in K:
    S[f"r{c}"] = S[K[c]] / S.groupby(["reg", "rc", "mc"])[K[c]].transform("median")
    S[f"p{c}"] = S[f"r{c}"] > 2.0
OUT = {}
pd.set_option("display.width", 220)

# 1. per-cylinder baseline level (median V) and peak rate by region, both groups
lvl = S.groupby(["reg", "g"])[[K[c] for c in K]].median().round(3); lvl.columns = [f"cyl{c}" for c in K]
print("median knock V by cylinder\n", lvl)
pk = S.groupby(["reg", "g"])[[f"p{c}" for c in K]].mean().mul(100).round(3); pk.columns = [f"cyl{c}" for c in K]
print("% samples > 2x by cylinder\n", pk)
OUT["level"] = lvl.reset_index().to_dict("records"); OUT["peak"] = pk.reset_index().to_dict("records")

# 2. co-occurrence: given a peak on cyl N, share of the same sample with a peak on each other cylinder, vs base rate
co = []
for rg in ("boost", "cruise", "idle"):
    for g in (0, 1):
        d = S[(S.reg == rg) & (S.g == g)]
        for n in K:
            hit = d[d[f"p{n}"]]
            if len(hit) < 10: continue
            co.append(dict(reg=rg, g=g, cyl=n, n=int(len(hit)), **{f"with{m}": round(float(hit[f"p{m}"].mean() / max(d[f"p{m}"].mean(), 1e-9)), 1) for m in K if m != n},
                           alone=round(100 * float((hit[[f"p{m}" for m in K if m != n]].sum(axis=1) == 0).mean()), 1)))
CO = pd.DataFrame(co); print("co-peak lift (x base rate) and % alone\n", CO.to_string())
OUT["co"] = co

# 3. matched conditions: peak samples vs same-cell non-peak samples (cell = reg x rpm250 x map10)
S["lam_err"] = (S["Lambda 1"] - S["Lambda target"]).where(S["Lambda is valid"] > 0.5)
S = S.sort_values(["file", "TIME"])
S["dmap"] = S.groupby("file", observed=True).MAP.diff(3) / 0.12
VARS = ["lam_err", "Ignition Angle", "IAT", "CLT", "Ethanol content", "Dwell Time", "Battery voltage", "dmap", "Short term trim"]
mc = []
for rg in ("boost", "cruise"):
    for g in (0, 1):
        for c in (1, 3, 4, 6):
            d = S[(S.reg == rg) & (S.g == g)]
            cell = d.groupby(["rc", "mc"])
            row = dict(reg=rg, g=g, cyl=c, n=int(d[f"p{c}"].sum()))
            if row["n"] < 15: continue
            for v in VARS:
                base = cell[v].transform("mean")
                diff = (d[v] - base)[d[f"p{c}"]]
                row[v] = round(float(diff.mean()), 3)
            mc.append(row)
MC = pd.DataFrame(mc); print("peak minus same-cell mean\n", MC.to_string())
OUT["matched"] = mc

# 4. cruise peaks inside the after group: by ethanol era and by RPM
d = S[(S.reg == "cruise")].copy()
d["era"] = np.where(d.g == 0, "before", np.where(d["Ethanol content"] > 45, "after E57", np.where(d["Ethanol content"] > 20, "after E25", "after E14")))
ce = d.groupby("era")[[f"p{c}" for c in K]].mean().mul(100).round(3); ce["min"] = d.groupby("era").size() / 1500
print("cruise % > 2x by fuel era\n", ce)
d["rb"] = (d.RPM // 500 * 500).astype(int)
cr = d.groupby(["g", "rb"])[["p1", "p4", "p6"]].mean().mul(100).round(3); cr["n"] = d.groupby(["g", "rb"]).size()
print("cruise % > 2x by RPM\n", cr)
OUT["cruise_era"] = ce.reset_index().to_dict("records")

# 5. dwell
dw = A[fuel & (A.RPM > 1000)].copy(); dw["rb"] = (dw.RPM // 1000 * 1000).astype(int)
print("dwell ms by RPM, before vs after\n", dw.groupby(["rb", "g"])["Dwell Time"].median().unstack().round(2))
print("battery V by group\n", dw.groupby("g")["Battery voltage"].describe()[["25%", "50%", "75%"]].round(2))
OUT["dwell_rpm"] = dw.groupby(["rb", "g"])["Dwell Time"].median().round(3).reset_index().to_dict("records")
# within-cell: peak rate in dwell terciles after removing cell effects (boost + cruise, cyl 1 and 6)
dt_rows = []
for rg in ("boost", "cruise"):
    d = S[S.reg == rg].copy()
    d["dres"] = d["Dwell Time"] - d.groupby(["rc", "mc"])["Dwell Time"].transform("mean")
    d["dq"] = pd.qcut(d.dres.rank(method="first"), 3, labels=["short", "mid", "long"])
    for (q, g), x in d.groupby(["dq", "g"], observed=True):
        dt_rows.append(dict(reg=rg, dq=str(q), g=int(g), n=int(len(x)), dres=round(float(x.dres.mean()), 3), p1=round(100 * float(x.p1.mean()), 3), p6=round(100 * float(x.p6.mean()), 3)))
DT = pd.DataFrame(dt_rows); print("peak rate by within-cell dwell tercile\n", DT.to_string())
OUT["dwell_terc"] = dt_rows

# 6. cyl6 - cyl3 EGT per trim-table cell (fuelTrimRPM x fuelTrimLoad), MAP held 2 s
RPMB = [1000, 2000, 4000, 6000, 8000]; LOADB = [20, 75, 130, 185, 240]
eg = []
for f, d in A.groupby("file", observed=True):
    d = d.sort_values("TIME")
    ok = fuel[d.index] & (d["EGT 1"] > 250) & (d["EGT 2"] > 250) & (d.CLT > 70)
    ri = np.abs(d.RPM.values[:, None] - np.array(RPMB)[None, :]).argmin(1)
    li = np.abs(d.MAP.values[:, None] - np.array(LOADB)[None, :]).argmin(1)
    cell = pd.Series(ri * 10 + li, index=d.index)
    held = cell.rolling(50, min_periods=50).apply(lambda x: float(np.all(x == x[-1])), raw=True).fillna(0) > 0
    s = d[ok & held]
    if len(s): eg.append(pd.DataFrame({"g": s.g.values, "ri": (cell[s.index] // 10).values, "li": (cell[s.index] % 10).values, "dl": (s["EGT 2"] - s["EGT 1"]).values}))
EG = pd.concat(eg)
T = EG.groupby(["ri", "li", "g"]).dl.agg(["mean", "size"]).reset_index()
T = T[T["size"] >= 50]
T["rpm"] = T.ri.map(dict(enumerate(RPMB))); T["load"] = T.li.map(dict(enumerate(LOADB)))
piv = T.pivot_table(index=["rpm", "load"], columns="g", values=["mean", "size"]).round(1)
print("cyl6-cyl3 EGT per trim cell (nearest cell, held 2 s)\n", piv.to_string())
OUT["egt_cells"] = T.drop(columns=["ri", "li"]).round(2).to_dict("records")

# 7. global lambda tracking after the trim, by region (enrich-everything question)
lt = S[(S["Lambda is valid"] > 0.5)].groupby(["reg", "g"]).agg(lam=("Lambda 1", "median"), tgt=("Lambda target", "median"), err=("lam_err", "median"), err_p90=("lam_err", lambda x: x.quantile(.9)))
print("lambda tracking\n", lt.round(3))
OUT["lambda"] = lt.round(4).reset_index().to_dict("records")
json.dump(OUT, open(os.path.join(HERE, "..", "data", "explore.json"), "w"), default=float)
