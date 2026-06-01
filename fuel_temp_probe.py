import csv
SUP=r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra"; LA=SUP+r"\LogAutosave"
FULL=[
 ("Apr8 drive_home", LA+r"\drive_home_today.csv"),
 ("Apr8 more_tip_in",LA+r"\more_tip_in.csv"),
 ("0506/0509 dup",   LA+r"\hood on 0509 terrible day.csv"),
 ("all-channel-ref", SUP+r"\all-channel-reference.csv"),
 ("all-ch-idlaircorr",SUP+r"\all-channels-reduced-idlaircorr.csv"),
]
def F(c): return c*9/5+32
def probe(path):
    ft=[]; first=None; tfirst=None
    with open(path,newline="") as f:
        r=csv.reader(f,delimiter=";"); h=[x.strip() for x in next(r)]; ix={n:i for i,n in enumerate(h)}
        if "Fuel Temperature" not in ix: return None
        fi=ix["Fuel Temperature"]; ti=ix["TIME"]
        for ln in r:
            try: v=float(ln[fi]); t=float(ln[ti])
            except (ValueError,IndexError): continue
            if v<=-30: continue   # skip sensor faults
            ft.append(v)
            if first is None: first=v; tfirst=t
    if not ft: return None
    fs=sorted(ft); n=len(fs)
    return dict(first=first, tfirst=tfirst, min=fs[0], p05=fs[int(.05*(n-1))],
                med=fs[n//2], mean=sum(ft)/n, max=fs[-1], end=ft[-1], n=n)

print("FUEL TEMPERATURE as ambient proxy (start-of-log = best cold anchor; rises with heat-soak)\n")
print(f"{'log':18s}{'start':>8s}{'min':>8s}{'mean':>8s}{'max':>8s}{'end':>8s}")
print("-"*58)
for lbl,path in FULL:
    p=probe(path)
    if p is None: print(f"{lbl:18s}  (no Fuel Temperature channel)"); continue
    print(f"{lbl:18s}{p['first']:5.0f}C{F(p['first']):4.0f}F{p['min']:5.0f}C"
          f"{p['mean']:6.0f}C{p['max']:6.0f}C{p['end']:6.0f}C   (n={p['n']})")
