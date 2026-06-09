import csv, bisect
SUP=r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra"; LA=SUP+r"\LogAutosave"

WV=[0.00,0.55,0.57,1.67,2.22,2.76,3.31,3.88,4.43,4.98]; WT=[92,55,54,15,3,-5,-15,-24,-33,-40]
RV=[0.00,0.24,0.31,0.45,0.78,1.00,1.45,1.73,2.47,2.96,3.63,4.10,4.63,4.98]
RT=[121,115,104,91,71,62,49,42,27,18,6,-5,-22,-39]
def interp(x,xs,ys):
    if x<=xs[0]:return ys[0]
    if x>=xs[-1]:return ys[-1]
    i=bisect.bisect_right(xs,x)-1; f=(x-xs[i])/(xs[i+1]-xs[i]); return ys[i]+f*(ys[i+1]-ys[i])
def correct(t):
    Td=list(reversed(WT)); Vd=list(reversed(WV)); v=interp(t,Td,Vd); return interp(v,RV,RT)

LOGS=[
 ("drive_home","ON", 85, LA+r"\drive_home_today.csv"),
 ("more_tip_in","ON",85, LA+r"\more_tip_in.csv"),
 ("0506","ON", 80, SUP+r"\hood on 0506 terrible day.csv"),
 ("0514","ON", 99, LA+r"\hood on 0514.csv"),
 ("0509","ON",103, LA+r"\hood on 0509 terrible day.csv"),
 ("hood-OFF","OFF",97, SUP+r"\hood-removed.csv"),
]
# region filters on (rpm, map)
REGIONS={
 "IN-BOOST (MAP>100 kPa)":      lambda rpm,mp: rpm>400 and mp>100,
 "CRUISE (2000-3000 rpm, MAP<100)": lambda rpm,mp: 2000<=rpm<=3000 and mp<100,
}
def proc(path,filt):
    pre=[];chg=[]
    with open(path,newline="") as f:
        r=csv.reader(f,delimiter=";"); h=[x.strip() for x in next(r)]; ix={n:i for i,n in enumerate(h)}
        ri,mi,pi,ci=ix["RPM"],ix["MAP"],ix["Pre IC temperature"],ix["Charge temp"]
        for ln in r:
            try: rpm=float(ln[ri]);mp=float(ln[mi]);p=float(ln[pi]);c=float(ln[ci])
            except (ValueError,IndexError): continue
            if p<=2 or not filt(rpm,mp): continue
            pre.append(correct(p)); chg.append(c)
    n=len(pre)
    return (sum(pre)/n if n else float('nan'), sum(chg)/n if n else float('nan'), n)
def F(c): return c*9/5+32

for rname,filt in REGIONS.items():
    print("="*100); print(rname); print("="*100)
    print(f"{'log':12s}{'hood':5s}{'localF':>7s}{'n':>7s}{'PreIC_corr':>16s}{'Charge(preTB)':>16s}{'PreIC-Chg':>11s}")
    print("-"*100)
    for lbl,hood,af,path in LOGS:
        pc,cg,n=proc(path,filt)
        if n==0:
            print(f"{lbl:12s}{hood:5s}{af:>6d}F{n:>7d}{'  --':>16s}{'  --':>16s}{'  --':>11s}"); continue
        print(f"{lbl:12s}{hood:5s}{af:>6d}F{n:>7d}{pc:>11.1f}C{F(pc):4.0f}F{cg:>10.1f}C{F(cg):4.0f}F{pc-cg:>+9.1f}C")
    print()
