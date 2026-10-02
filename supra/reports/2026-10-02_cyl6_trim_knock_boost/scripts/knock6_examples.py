"""All-six knock-voltage traces for matched full-pedal boost pulls, before vs after the 2026-05-04 per-cylinder trim.
Pairs are pulls (Boost > 20 kPa, >= 1.5 s) from the same E56-58 tank, matched on peak boost and RPM span. -> knock6_examples.png"""
import os, pickle, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
A, F = pickle.load(open(os.path.join(HERE, "..", "data", "eb_all.pkl"), "rb"))
A = A[A.RPM > 500]
A = A[A["Injector 6 trim"] >= 100].copy(); A["g"] = (A["Injector 6 trim"] > 100).astype(int)
K = [f"Knock voltage peak cyl {c}" for c in range(1, 7)]
P = []
for f, d in A.groupby("file", observed=True):
    d = d.sort_values("TIME").reset_index(drop=True)
    ev = (d.Boost.fillna(0) > 20).astype(int).values; ed = np.flatnonzero(np.diff(np.r_[0, ev, 0]))
    for a, b in zip(ed[::2], ed[1::2]):
        s = d.iloc[a:b]
        if (b - a) * 0.04 < 1.5: continue
        P.append(dict(f=f, a=a, b=b, g=int(s.g.mode()[0]), peak=float(s.Boost.max()), r0=int(s.RPM.iloc[0]), r1=int(s.RPM.max()),
                      eth=float(s["Ethanol content"].median()), clt=float(s.CLT.median()), iat=float(s.IAT.median()) if "IAT" in s else np.nan))
P = pd.DataFrame(P); print(P.groupby("g").peak.describe())
# Hand-picked from the >=1.5 s pull list: same E56-58 tank, nearest peak boost and RPM span (2026-10-02).
import sys
LOW = "low" in sys.argv[1:]   # low-ethanol set: pump E8-9 (Mar) vs E14-25 (May 30 - Sep)
PICK = ([(("20260328", 57), ("20260908", 57)), (("20260329", 64), ("20260530", 64)), (("20260303", 75), ("20260530", 75))] if LOW else
        [(("20260407", 64), ("20260506", 64)), (("20260420", 73), ("20260510", 73)), (("20260501", 86), ("20260506", 89))])
P["day"] = P.f.str[:8]; P["pk"] = P.peak.round().astype(int)
one = lambda day, pk: P[(P.day == day) & (P.pk == pk)].iloc[0]
ONLY = [a for a in sys.argv[1:] if a.isdigit()]   # e.g. "low 75": keep only the pair whose before peak is 75 kPa
if ONLY: PICK = [pr for pr in PICK if str(pr[0][1]) in ONLY]
rows = [(one(*b), one(*a)) for b, a in PICK]
fig, ax = plt.subplots(len(rows), 2, figsize=(14, 4.2 * len(rows)), sharey=True, squeeze=False)
col = plt.cm.tab10.colors
for i, pr in enumerate(rows):
    for j, r in enumerate(pr):
        d = A[A.file == r.f].sort_values("TIME").reset_index(drop=True).iloc[max(0, r.a - 25):r.b + 12]
        t = d.TIME - d.TIME.iloc[0]; x = ax[i, j]
        for k in range(6): x.plot(t, d[K[k]], lw=1.6 if k == 5 else 0.9, color=col[k], label=f"cyl {k+1}")
        x2 = x.twinx(); x2.plot(t, d.Boost, "k--", lw=1); x2.plot(t, d.RPM / 100, ":", color="gray", lw=1); x2.set_ylim(0, 100)
        if j == 1: x2.set_ylabel("Boost kPa (--) / RPM÷100 (··)")
        else: x2.set_yticklabels([])
        x.set_title(f"{'BEFORE' if r.g == 0 else 'AFTER'} trim · {r.f[:8]} · peak {r.peak:.0f} kPa · {r.r0}–{r.r1} rpm · E{r.eth:.0f} · CLT {r.clt:.0f}", fontsize=9)
        x.set_xlabel("s"); x.grid(alpha=.3)
        if j == 0: x.set_ylabel("Knock voltage peak (V)")
ax[0, 0].legend(ncol=6, fontsize=8, loc="upper left")
fig.tight_layout(); fig.savefig(os.path.join(HERE, "..", ("knock6_examples_low_eth" if LOW else "knock6_examples") + ("_" + "_".join(ONLY) if ONLY else "") + ".png"), dpi=110)
for b0, c in rows:
    for r in (b0, c):
        d = A[A.file == r.f].sort_values("TIME").reset_index(drop=True).iloc[r.a:r.b]
        print(r.g, r.f[:8], f"{r.peak:.0f}kPa {r.r0}-{r.r1} E{r.eth:.0f}", " ".join(f"c{k+1} med {d[K[k]].median():.2f}/max {d[K[k]].max():.2f}" for k in range(6)))
