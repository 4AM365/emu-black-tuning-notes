"""Control for baseline/noise changes in the knock-peak definition (Will, 2026-10-02).
For each cylinder, region and period, a peak is counted three ways:
  pooled : V > k x median(cell, both periods pooled)          (the original definition)
  own    : V > k x median(cell, this period only)
  mad    : (V - median(cell, this period)) / MAD(cell, this period) > z   -- scale-free; asks whether the peak
           stands out from that period's own noise spread, so a lower noise floor can't inflate it.
Cell = region x RPM 250 x MAP 10 kPa; cells need >= 200 samples in a period. -> data/peak_norm.json"""
import os, json, pickle, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
A, F = pickle.load(open(os.path.join(HERE, "..", "data", "eb_all.pkl"), "rb"))
A = A[(A.RPM > 500)].copy()
A["g"] = np.where(A["Injector 6 trim"] > 100, 1, 0)
fuel = A["Injectors PW"] > 0.3
A["reg"] = ""
A.loc[fuel & A.MAP.between(105, 175) & A.RPM.between(3500, 6000), "reg"] = "boost"
A.loc[fuel & (A.reg == "") & A.MAP.between(30, 95) & A.RPM.between(1500, 4000), "reg"] = "cruise"
A.loc[fuel & (A.reg == "") & (A.RPM < 1400) & (A["Idle state"] == 2) & (A.CLT >= 80), "reg"] = "idle"
S = A[A.reg != ""].copy(); S["rc"] = (S.RPM // 250).astype(int); S["mc"] = (S.MAP // 10).astype(int)
cnt = S.groupby(["reg", "rc", "mc", "g"]).size().unstack("g")
good = cnt[(cnt[0] >= 200) & (cnt[1] >= 200)].index          # cells both periods visit enough
S = S.set_index(["reg", "rc", "mc"]); S = S[S.index.isin(good)].reset_index()
rows = []
for c in range(1, 7):
    k = f"Knock voltage peak cyl {c}"
    pooled = S.groupby(["reg", "rc", "mc"])[k].transform("median")
    own = S.groupby(["reg", "rc", "mc", "g"])[k].transform("median")
    mad = S.groupby(["reg", "rc", "mc", "g"])[k].transform(lambda x: (x - x.median()).abs().median())
    rp, ro = S[k] / pooled, S[k] / own
    z = (S[k] - own) / mad.where(mad > 0)
    for (rg, g), idx in S.groupby(["reg", "g"]).groups.items():
        rows.append(dict(reg=rg, g=int(g), cyl=c, n=int(len(idx)), med=round(float(S.loc[idx, k].median()), 3), mad=round(float(mad.loc[idx].median()), 4),
                         pooled15=round(100 * float((rp[idx] > 1.5).mean()), 3), pooled20=round(100 * float((rp[idx] > 2).mean()), 3),
                         own15=round(100 * float((ro[idx] > 1.5).mean()), 3), own20=round(100 * float((ro[idx] > 2).mean()), 3),
                         z6=round(100 * float((z[idx] > 6).mean()), 3), z10=round(100 * float((z[idx] > 10).mean()), 3)))
R = pd.DataFrame(rows)
pd.set_option("display.width", 220)
for rg in ("idle", "cruise", "boost"):
    print("==", rg); print(R[R.reg == rg].pivot_table(index="cyl", columns="g", values=["med", "mad", "pooled20", "own20", "z6", "z10"]).round(3).to_string())
json.dump(rows, open(os.path.join(HERE, "..", "data", "peak_norm.json"), "w"))
