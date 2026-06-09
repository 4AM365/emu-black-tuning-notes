import csv
SUP = r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra"; LA=SUP+r"\LogAutosave"

# Hottest datable logs. ambient = weather daily HIGH (worst-case anchor).
LOGS = [
    ("0509 hot ON",  "ON",  104, LA  + r"\hood on 0509 terrible day.csv"),
    ("0514 hot ON",  "ON",   99, LA  + r"\hood on 0514.csv"),
    ("hood-OFF",     "OFF",  97, SUP + r"\hood-removed.csv"),
]
WANT=["RPM","MAP","IAT","Pre IC temperature","Charge temp","CLT"]

def parse(path):
    out={"all":{w:[] for w in WANT},"idle":{w:[] for w in WANT}}
    with open(path,newline="") as f:
        r=csv.reader(f,delimiter=";"); hdr=[h.strip() for h in next(r)]
        idx={n:i for i,n in enumerate(hdr)}; col={w:idx.get(w) for w in WANT}
        for line in r:
            try: rpm=float(line[col["RPM"]]); mp=float(line[col["MAP"]])
            except (ValueError,IndexError,TypeError): continue
            if rpm<=400 or mp>=100: continue
            idle = rpm<1500 and mp<60
            for w,ci in col.items():
                if ci is None: continue
                try:
                    v=float(line[ci]); out["all"][w].append(v)
                    if idle: out["idle"][w].append(v)
                except (ValueError,IndexError): pass
    return out

def st(v,dz=False):
    if dz: v=[x for x in v if x>2]
    if not v: return None
    v=sorted(v); n=len(v)
    return dict(n=n,mean=sum(v)/n,p05=v[int(.05*(n-1))],med=v[n//2],p95=v[int(.95*(n-1))])
def F(c): return c*9/5+32

for grp in ("all","idle"):
    label = "MAP<100 (all no-boost)" if grp=="all" else "IDLE (rpm<1500, MAP<60)"
    print("="*84); print(f"{label}   [temps C]"); print("="*84)
    print(f"{'log':12s}{'hood':5s}{'ambF':>5s}{'IATmean':>8s}{'PreIC(med/mean/p95)':>22s}{'Charge(med/mean/p95)':>22s}")
    print("-"*84)
    rows={}
    for lbl,hood,amb,path in LOGS:
        d=parse(path)[grp] if False else None
    # parse once, cache
    cache={lbl:parse(path) for lbl,hood,amb,path in LOGS}
    for lbl,hood,amb,path in LOGS:
        d=cache[lbl][grp]
        pi=st(d["Pre IC temperature"],dz=True); ch=st(d["Charge temp"]); ia=st(d["IAT"])
        rows[lbl]=dict(pi=pi,ch=ch,ia=ia,amb=amb,hood=hood)
        iam = f"{ia['mean']:.1f}" if ia and ia['mean']>-30 else "n/a"
        pis = f"{pi['med']:.0f}/{pi['mean']:.1f}/{pi['p95']:.0f}" if pi else "-"
        chs = f"{ch['med']:.0f}/{ch['mean']:.1f}/{ch['p95']:.0f}" if ch else "-"
        print(f"{lbl:12s}{hood:5s}{amb:>5d}{iam:>8s}{pis:>22s}{chs:>22s}")
    print()

# Matched-ambient direct compare: 0514 (99F) vs hood-off (97F)
print("="*84)
print("MATCHED-AMBIENT DIRECT COMPARE  (0514 hood-ON @99F  vs  hood-OFF @97F, ~2F apart)")
print("="*84)
on=cache["0514 hot ON"]; off=cache["hood-OFF"]
for grp in ("all","idle"):
    pio=st(on[grp]["Pre IC temperature"],dz=True); pif=st(off[grp]["Pre IC temperature"],dz=True)
    cho=st(on[grp]["Charge temp"]); chf=st(off[grp]["Charge temp"])
    print(f"\n  [{grp}]")
    print(f"    Pre-IC mean : hood-ON {pio['mean']:5.1f}C ({F(pio['mean']):3.0f}F)   hood-OFF {pif['mean']:5.1f}C ({F(pif['mean']):3.0f}F)   delta {pif['mean']-pio['mean']:+.1f}C")
    print(f"    Charge mean : hood-ON {cho['mean']:5.1f}C ({F(cho['mean']):3.0f}F)   hood-OFF {chf['mean']:5.1f}C ({F(chf['mean']):3.0f}F)   delta {chf['mean']-cho['mean']:+.1f}C")
