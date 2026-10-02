"""Scientific-method pass (Will, 2026-10-02): for each test, event counts per drive and a drive-level bootstrap
confidence interval on the after/before rate ratio. Resampling whole drives handles clustering (one bad drive
can't carry the result). Also the same-fuel window Apr 20 - May 10 (E57, idle lambda target 0.931 both sides).
-> data/tests.json"""
import os, sys, json, pickle, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "skills", "emu-black-idle-stability", "scripts"))
import idle_stability as IS
rng = np.random.default_rng(7)
A, F = pickle.load(open(os.path.join(HERE, "..", "data", "eb_all.pkl"), "rb"))
A = A.sort_values(["file", "TIME"])
last_stop = A.TIME.where(A.RPM < 200).groupby(A.file, observed=True).ffill()
A["since_start"] = (A.TIME - last_stop).fillna(1e6)
# rich blips: rolling median over the whole file's valid lambda (no segment-edge artefacts), then masked to idle
lam = A["Lambda 1"].where(A["Lambda is valid"] > 0.5)
A["lam_med"] = lam.groupby(A.file, observed=True).transform(lambda x: x.rolling(15, center=True, min_periods=8).median())
A = A[A.RPM > 500].copy()
A["g"] = np.where(A["Injector 6 trim"] > 100, 1, 0)
A["day"] = A.file.astype(str).str[:8]
fuel = A["Injectors PW"] > 0.3

# ---- idle mask (restart-gated)
parts = []
for f, d in A.groupby("file", observed=True):
    tdt = d.TIME.diff(IS.RATE_K); slew = (d.RPM.diff(IS.RATE_K) / tdt.where(tdt > 0)).abs()
    tc = np.nanpercentile(d.TPS, IS.TPS_CLOSED_PCT)
    m = ((d["Idle state"] == 2) & (d.TPS <= tc + IS.TPS_MARGIN) & d.RPM.between(IS.RPM_LO, IS.RPM_HI)
         & (slew.fillna(0) <= IS.RATE_MAX) & (d.CLT >= IS.WARM_CLT) & (d.since_start >= 120)).fillna(False)
    mm = np.zeros(len(d), bool)                     # same >= 4 s steady segments as the idle-stability skill / questions.py
    for a, b in IS.runs(m.reset_index(drop=True), 0.04): mm[a:b + 1] = True
    parts.append(pd.Series(mm, index=d.index))
A["idle"] = pd.concat(parts)
rich = (A["Lambda is valid"] > 0.5) & (A["Lambda 1"] - A.lam_med < -0.02)
A["rich_start"] = rich & ~rich.groupby(A.file, observed=True).shift(1, fill_value=False)

# ---- knock peaks, own-period cell median, shared cells
A["reg"] = ""
A.loc[fuel & A.MAP.between(105, 175) & A.RPM.between(3500, 6000), "reg"] = "boost"
A.loc[fuel & (A.reg == "") & A.MAP.between(30, 95) & A.RPM.between(1500, 4000), "reg"] = "cruise"
A.loc[fuel & (A.reg == "") & (A.RPM < 1400) & (A["Idle state"] == 2) & (A.CLT >= 80), "reg"] = "idle"
S = A[A.reg != ""].copy(); S["rc"] = (S.RPM // 250).astype(int); S["mc"] = (S.MAP // 10).astype(int)
cnt = S.groupby(["reg", "rc", "mc", "g"]).size().unstack("g")
good = cnt[(cnt[0] >= 200) & (cnt[1] >= 200)].index
S = S.set_index(["reg", "rc", "mc"]); S = S[S.index.isin(good)].reset_index()
for c in (1, 4, 6):
    k = f"Knock voltage peak cyl {c}"
    S[f"pk{c}"] = S[k] > 2 * S.groupby(["reg", "rc", "mc", "g"])[k].transform("median")

def drive_table(df, flag):
    t = df.groupby(["file", "g"], observed=True).agg(ev=(flag, "sum"), n=(flag, "size")).reset_index()
    return t[t.n > 0]

def boot(t, B=4000):
    b, a = t[t.g == 0], t[t.g == 1]
    if len(b) < 2 or len(a) < 2 or b.ev.sum() == 0: return None
    r0 = b.ev.sum() / b.n.sum(); r1 = a.ev.sum() / a.n.sum()
    rr = []
    bi, ai = b[["ev", "n"]].values, a[["ev", "n"]].values
    for _ in range(B):
        x = bi[rng.integers(0, len(bi), len(bi))]; y = ai[rng.integers(0, len(ai), len(ai))]
        if x[:, 0].sum() == 0: continue
        rr.append((y[:, 0].sum() / y[:, 1].sum()) / (x[:, 0].sum() / x[:, 1].sum()))
    lo, hi = np.percentile(rr, [2.5, 97.5])
    top = b.sort_values("ev", ascending=False)
    return dict(drives_before=int(len(b)), drives_after=int(len(a)), ev_before=int(b.ev.sum()), ev_after=int(a.ev.sum()),
                min_before=round(b.n.sum() / 1500, 1), min_after=round(a.n.sum() / 1500, 1),
                rate_before_per_hr=round(r0 * 1500 * 60, 2), rate_after_per_hr=round(r1 * 1500 * 60, 2),
                ratio=round(r1 / r0, 3), ci_lo=round(float(lo), 3), ci_hi=round(float(hi), 3),
                top_drive_share_before=round(float(top.ev.iloc[0] / max(b.ev.sum(), 1)), 2),
                drives_with_events_before=int((b.ev > 0).sum()), drives_with_events_after=int((a.ev > 0).sum()))

tests = {}
idle = A[A.idle]
tests["T4 idle rich blips > 0.02 lambda (all data)"] = boot(drive_table(idle, "rich_start"))
win = idle[(idle.day >= "20260420") & (idle.day <= "20260510")]
tests["T4 idle rich blips > 0.02 lambda (same fuel, Apr 20 - May 10)"] = boot(drive_table(win, "rich_start"))
for rg, lab in (("idle", "T1"), ("boost", "T2"), ("cruise", "T3")):
    for c in (6, 4, 1):
        d = S[S.reg == rg]
        tests[f"{lab} {rg} cyl {c} peaks > 2x own normal (all data)"] = boot(drive_table(d, f"pk{c}"))
    d = S[(S.reg == rg) & (S.day >= "20260420") & (S.day <= "20260510")]
    tests[f"{lab} {rg} cyl 6 peaks > 2x own normal (same fuel, Apr 20 - May 10)"] = boot(drive_table(d, "pk6"))
T = pd.DataFrame({k: v for k, v in tests.items() if v}).T
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 20)
print(T.to_string())
json.dump({k: v for k, v in tests.items()}, open(os.path.join(HERE, "..", "data", "tests.json"), "w"), default=float)
