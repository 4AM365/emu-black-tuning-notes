"""T5: cyl6 - cyl3 EGT before vs after, drive-level bootstrap on the difference of means, per band
(MAP held in band 2 s, overrun excluded), plus the same-fuel window Apr 20 - May 10. -> data/egt_tests.json"""
import os, json, pickle, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(11)
A, F = pickle.load(open(os.path.join(HERE, "..", "data", "eb_all.pkl"), "rb"))
A = A[(A.RPM > 500)].copy()
A["g"] = np.where(A["Injector 6 trim"] > 100, 1, 0)
BANDS = [("idle", 0, 45, 0, 1400), ("light", 25, 60, 1400, 9000), ("cruise", 60, 95, 1400, 9000), ("transition", 95, 130, 1400, 9000)]
rows = []
for f, d in A.groupby("file", observed=True):
    d = d.sort_values("TIME")
    ok = (d["Injectors PW"] > 0.3) & (d["EGT 1"] > 250) & (d["EGT 2"] > 250) & (d.CLT > 70)
    for b, m0, m1, r0, r1 in BANDS:
        inb = (d.MAP >= m0) & (d.MAP < m1) & (d.RPM >= r0) & (d.RPM < r1)
        held = inb.rolling(50, min_periods=50).min().fillna(0).astype(bool)
        s = d[held & ok]
        if len(s) >= 250:
            rows.append(dict(f=f, day=f[:8], g=int(s.g.mode()[0]), band=b, n=len(s), dl=float((s["EGT 2"] - s["EGT 1"]).mean())))
D = pd.DataFrame(rows)
out = {}
for label, sel in (("all data", D), ("same fuel Apr 20 - May 10", D[(D.day >= "20260420") & (D.day <= "20260510")])):
    for b in [x[0] for x in BANDS]:
        x = sel[sel.band == b]; b0, b1 = x[x.g == 0], x[x.g == 1]
        if len(b0) < 3 or len(b1) < 3: continue
        diffs = [rng.choice(b1.dl.values, len(b1)).mean() - rng.choice(b0.dl.values, len(b0)).mean() for _ in range(4000)]
        lo, hi = np.percentile(diffs, [2.5, 97.5])
        out[f"{b} ({label})"] = dict(drives_before=int(len(b0)), drives_after=int(len(b1)), before=round(b0.dl.mean(), 1), after=round(b1.dl.mean(), 1),
                                     diff=round(b1.dl.mean() - b0.dl.mean(), 1), ci_lo=round(float(lo), 1), ci_hi=round(float(hi), 1))
pd.set_option("display.width", 200)
print(pd.DataFrame(out).T)
json.dump(out, open(os.path.join(HERE, "..", "data", "egt_tests.json"), "w"), default=float)
