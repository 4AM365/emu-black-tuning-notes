import csv, bisect
SUP=r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra"; LA=SUP+r"\LogAutosave"

# Pre-IC correction (invert wrong curve -> V -> apply correct IAT curve)
WV=[0.00,0.55,0.57,1.67,2.22,2.76,3.31,3.88,4.43,4.98]; WT=[92,55,54,15,3,-5,-15,-24,-33,-40]
RV=[0.00,0.24,0.31,0.45,0.78,1.00,1.45,1.73,2.47,2.96,3.63,4.10,4.63,4.98]
RT=[121,115,104,91,71,62,49,42,27,18,6,-5,-22,-39]
def interp(x,xs,ys):
    if x<=xs[0]:return ys[0]
    if x>=xs[-1]:return ys[-1]
    i=bisect.bisect_right(xs,x)-1; f=(x-xs[i])/(xs[i+1]-xs[i]); return ys[i]+f*(ys[i+1]-ys[i])
def correct(t):
    Td=list(reversed(WT)); Vd=list(reversed(WV)); v=interp(t,Td,Vd); return interp(v,RV,RT)

# log, hood, local ambient F, ambient-confidence, path
LOGS=[
 ("drive_home","ON", 85,"exact 22:00 Gilbert", LA+r"\drive_home_today.csv"),
 ("more_tip_in","ON",85,"exact 22:00 Gilbert", LA+r"\more_tip_in.csv"),
 ("0506","ON", 80,"Wed Phx, time unk (high 84)", SUP+r"\hood on 0506 terrible day.csv"),
 ("0514","ON", 99,"Thu Phx, time unk (high 99)", LA+r"\hood on 0514.csv"),
 ("0509","ON",103,"Sat Gilbert, time unk (high 103)", LA+r"\hood on 0509 terrible day.csv"),
 ("hood-OFF","OFF",97,"given (now)", SUP+r"\hood-removed.csv"),
]
def proc(path):
    pre=[]; chg=[]
    with open(path,newline="") as f:
        r=csv.reader(f,delimiter=";"); h=[x.strip() for x in next(r)]; ix={n:i for i,n in enumerate(h)}
        ri,mi,pi,ci=ix["RPM"],ix["MAP"],ix["Pre IC temperature"],ix["Charge temp"]
        for ln in r:
            try: rpm=float(ln[ri]); mp=float(ln[mi]); p=float(ln[pi]); c=float(ln[ci])
            except (ValueError,IndexError): continue
            if rpm<=400 or mp>=60 or rpm>=1500 or p<=2: continue   # IDLE, no-boost
            pre.append(correct(p)); chg.append(c)
    return (sum(pre)/len(pre) if pre else float('nan'),
            sum(chg)/len(chg) if chg else float('nan'), len(pre))
def F(c): return c*9/5+32

print("IDLE (rpm<1500, MAP<60). Pre-IC = CORRECTED. Charge = IAT @ throttle body.\n")
print(f"{'log':12s}{'hood':5s}{'localF':>7s}{'PreIC_corr':>16s}{'Charge(preTB)':>16s}{'PreIC-Chg':>10s}  ambient note")
print("-"*92)
for lbl,hood,af,note,path in LOGS:
    pc,cg,n=proc(path)
    print(f"{lbl:12s}{hood:5s}{af:>6d}F{pc:>11.1f}C{F(pc):4.0f}F{cg:>10.1f}C{F(cg):4.0f}F{pc-cg:>+8.1f}C  {note}")

print("\nMATCHED-AMBIENT PAIR (hottest, ~2F apart):")
print("  0514 hood-ON @99F vs hood-OFF @97F  -> read the deltas directly (no normalization).")
