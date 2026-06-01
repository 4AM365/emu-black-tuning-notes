import csv

SUP = r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra"
LA  = SUP + r"\LogAutosave"

# All hood-ON except hood-removed. Full-channel logs self-report Ambient/IAT/CLT/Post-IC.
LOGS = [
    ("all-ch-ref",  "ON",  SUP + r"\all-channel-reference.csv",          None),
    ("all-ch-idl",  "ON",  SUP + r"\all-channels-reduced-idlaircorr.csv", None),
    ("drive-home",  "ON",  LA  + r"\drive_home_today.csv",                None),
    ("more-tipin",  "ON",  LA  + r"\more_tip_in.csv",                     None),
    ("hood-OFF",    "OFF", SUP + r"\hood-removed.csv",                    36.1),  # reduced; ambient given
]
WANT = ["RPM","MAP","IAT","Pre IC temperature","Post IC temperature","Charge temp",
        "Ambient temperature","CLT"]

def process(path):
    with open(path, newline="") as f:
        r = csv.reader(f, delimiter=";"); hdr=[h.strip() for h in next(r)]
        idx={n:i for i,n in enumerate(hdr)}; col={w:idx.get(w) for w in WANT}
        acc={w:[] for w in WANT}
        for line in r:
            try: rpm=float(line[col["RPM"]]); mp=float(line[col["MAP"]])
            except (ValueError,IndexError,TypeError): continue
            if rpm<=400 or mp>=100: continue
            for w,ci in col.items():
                if ci is None: continue
                try: acc[w].append(float(line[ci]))
                except (ValueError,IndexError): pass
        return acc

def mean(v,drop_zero=False):
    if drop_zero: v=[x for x in v if x>2]
    return sum(v)/len(v) if v else None
def F(c): return None if c is None else c*9/5+32

print("MAP<100 (no boost), engine running. Hood-ON logs self-report ambient.\n")
res=[]
for label,hood,path,amb_given in LOGS:
    a=process(path)
    amb = mean(a["Ambient temperature"]) or amb_given
    iat = mean(a["IAT"]); preic=mean(a["Pre IC temperature"],drop_zero=True)
    post= mean(a["Post IC temperature"]); chg=mean(a["Charge temp"]); clt=mean(a["CLT"])
    res.append(dict(label=label,hood=hood,amb=amb,iat=iat,preic=preic,post=post,chg=chg,clt=clt,
                    n=len([x for x in a["Pre IC temperature"] if x>2])))

# sort hood-ON by ambient to show the temperature sweep, hood-off last
res_on=sorted([r for r in res if r["hood"]=="ON"], key=lambda r:(r["amb"] or 0))
res_off=[r for r in res if r["hood"]=="OFF"]

h=f"{'log':12s}{'hood':5s}{'ambC':>6s}{'IAT':>6s}{'PreIC':>7s}{'PostIC':>7s}{'Charge':>7s}{'CLT':>6s} | {'PreIC-amb':>10s}{'Chg-amb':>9s}{'Chg-PreIC':>10s}"
print(h); print("-"*len(h))
def show(r):
    def g(x): return f"{x:.1f}" if x is not None else "  -"
    pia = (r["preic"]-r["amb"]) if (r["preic"] and r["amb"]) else None
    cma = (r["chg"]-r["amb"]) if (r["chg"] and r["amb"]) else None
    cmp = (r["chg"]-r["preic"]) if (r["chg"] and r["preic"]) else None
    def s(x): return (f"{x:+.1f}" if x is not None else "-")
    print(f"{r['label']:12s}{r['hood']:5s}{g(r['amb']):>6s}{g(r['iat']):>6s}{g(r['preic']):>7s}"
          f"{g(r['post']):>7s}{g(r['chg']):>7s}{g(r['clt']):>6s} | {s(pia):>10s}{s(cma):>9s}{s(cmp):>10s}")
for r in res_on: show(r)
print("-"*len(h))
for r in res_off: show(r)
print("\n(ambC = mean logged ambient during drive; PreIC-amb = compressor-bay air rise above ambient,")
print(" the cleanest hood heat-soak signal at MAP<100. Chg-PreIC = pickup from compressor to throttle body.)")
print("\nPre-IC sensor sample counts (zeros dropped):")
for r in res_on+res_off: print(f"  {r['label']:12s} {r['hood']:4s} n={r['n']}")
