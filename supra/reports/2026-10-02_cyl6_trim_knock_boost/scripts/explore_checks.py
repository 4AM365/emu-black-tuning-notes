"""Follow-up checks for explore_cyl_dwell.py: fuel era vs peaks, cruise timing shift, dwell vs heat-soak confound."""
import os, pickle, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
A, F = pickle.load(open(os.path.join(HERE, "..", "data", "eb_all.pkl"), "rb"))
A = A[(A.RPM > 500) & (A["Injectors PW"] > 0.3)].copy()
A["g"] = np.where(A["Injector 6 trim"] > 100, 1, 0)
A["fuel"] = np.where(A["Ethanol content"] > 45, "E57", np.where(A["Ethanol content"] > 20, "E25", np.where(A["Ethanol content"] > 11, "E14", "E9")))
A["era"] = np.where(A.g == 0, "before ", "after ") + A.fuel
A["reg"] = ""
A.loc[A.MAP.between(105, 175) & A.RPM.between(3500, 6000), "reg"] = "boost"
A.loc[(A.reg == "") & A.MAP.between(30, 95) & A.RPM.between(1500, 4000), "reg"] = "cruise"
S = A[A.reg != ""].copy(); S["rc"] = (S.RPM // 250).astype(int); S["mc"] = (S.MAP // 10).astype(int)
for c in (1, 3, 4, 6):
    k = f"Knock voltage peak cyl {c}"; S[f"p{c}"] = S[k] / S.groupby(["reg", "rc", "mc"])[k].transform("median") > 2
pd.set_option("display.width", 200)
t = S.groupby(["reg", "era"])[["p1", "p3", "p4", "p6"]].mean().mul(100).round(3); t["min"] = (S.groupby(["reg", "era"]).size() / 1500).round(1)
print("peaks > 2x by fuel era\n", t)
# cruise: ignition angle and table ignition, same cells, before vs after (cell-weighted difference)
c = S[S.reg == "cruise"]
m = c.groupby(["rc", "mc", "g"])[["Ignition Angle", "Ignition From Table", "IAT", "Lambda 1", "Lambda target"]].mean().unstack("g")
n = c.groupby(["rc", "mc", "g"]).size().unstack("g").min(axis=1)
for v in ["Ignition Angle", "Ignition From Table", "IAT", "Lambda 1", "Lambda target"]:
    dlt = (m[(v, 1)] - m[(v, 0)]); ok = dlt.notna() & (n > 200)
    print(f"cruise {v}: after - before, cell-weighted = {np.average(dlt[ok], weights=n[ok]):.3f}")
c2 = c.copy(); c2["rb"] = (c2.RPM // 500 * 500).astype(int)
print("cruise ignition angle by era and RPM\n", c2.groupby(["era", "rb"])["Ignition Angle"].median().unstack().round(1))
# dwell residual vs IAT / battery residual at cruise (is dwell just tracking heat soak and voltage?)
for v in ["Dwell Time", "IAT", "Battery voltage"]:
    c2[v + "_r"] = c2[v] - c2.groupby(["rc", "mc"])[v].transform("mean")
print("cruise within-cell correlations:\n", c2[["Dwell Time_r", "IAT_r", "Battery voltage_r"]].corr().round(2))
