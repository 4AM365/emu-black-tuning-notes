import csv
LA = r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra\LogAutosave"
LOGS = [("drive_home (Apr8 22:00 Gilbert)", LA+r"\drive_home_today.csv"),
        ("more_tipin (Apr8 22:00 Gilbert)", LA+r"\more_tip_in.csv")]
AMB_C = 29.3  # 84.7F
WANT=["RPM","MAP","IAT","Pre IC temperature","Charge temp","CLT","Boost"]

def parse(path):
    rows=[]
    with open(path,newline="") as f:
        r=csv.reader(f,delimiter=";"); hdr=[h.strip() for h in next(r)]
        idx={n:i for i,n in enumerate(hdr)}; col={w:idx.get(w) for w in WANT}
        for line in r:
            try: rpm=float(line[col["RPM"]]); mp=float(line[col["MAP"]])
            except (ValueError,IndexError,TypeError): continue
            if rpm<=400: continue
            rec={"rpm":rpm,"map":mp}
            for w in ["IAT","Pre IC temperature","Charge temp","CLT","Boost"]:
                ci=col[w]
                try: rec[w]=float(line[ci]) if ci is not None else None
                except (ValueError,IndexError): rec[w]=None
            rows.append(rec)
    return rows

def dist(v):
    v=[x for x in v if x is not None];
    if not v: return None
    v=sorted(v); n=len(v)
    return f"min={v[0]:.0f} p05={v[int(.05*(n-1))]:.0f} med={v[n//2]:.0f} mean={sum(v)/n:.1f} p95={v[int(.95*(n-1))]:.0f} max={v[-1]:.0f}"

for label,path in LOGS:
    rows=parse(path)
    nb=[r for r in rows if r["map"]<100]
    pre=[r["Pre IC temperature"] for r in nb]
    print("="*78); print(label, f"  (ambient {AMB_C:.0f}C / 85F)"); print("="*78)
    n=len(pre); zeros=sum(1 for x in pre if x is not None and x<=2)
    print(f"  no-boost samples={n}  Pre-IC<=2C dropouts={zeros} ({100*zeros/n:.1f}%)")
    print(f"  IAT      : {dist([r['IAT'] for r in nb])}")
    print(f"  Pre-IC   : {dist(pre)}   (raw, incl dropouts)")
    print(f"  Pre-IC>2 : {dist([x for x in pre if x and x>2])}")
    print(f"  Charge   : {dist([r['Charge temp'] for r in nb])}")
    print(f"  CLT      : {dist([r['CLT'] for r in nb])}")
    # idle subset
    idle=[r for r in nb if r['rpm']<1500 and r['map']<60]
    print(f"  -- idle (n={len(idle)}):")
    print(f"     IAT   : {dist([r['IAT'] for r in idle])}")
    print(f"     Pre-IC: {dist([r['Pre IC temperature'] for r in idle if r['Pre IC temperature'] and r['Pre IC temperature']>2])}")
    print(f"     Charge: {dist([r['Charge temp'] for r in idle])}")
    print()
