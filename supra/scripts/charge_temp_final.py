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
 ("Apr8 drive","ON", 85, LA+r"\drive_home_today.csv"),
 ("Apr8 tip-in","ON",85, LA+r"\more_tip_in.csv"),
 ("0506 cool","ON", 82, SUP+r"\hood on 0506 terrible day.csv"),
 ("0514 hot","ON", 99, LA+r"\hood on 0514.csv"),
 ("hood-OFF","OFF",97, SUP+r"\hood-removed.csv"),
]
# region -> (filter, aggregator). idle=PEAK (soak ramp); cruise/boost=MEAN (steady)
REGIONS={
 "IDLE (rpm<1500, MAP<60)  [PEAK]":      (lambda rpm,mp: rpm>400 and rpm<1500 and mp<60, "peak"),
 "CRUISE (2000-3000 rpm, MAP<100) [mean]":(lambda rpm,mp: 2000<=rpm<=3000 and mp<100, "mean"),
 "IN-BOOST (MAP>100 kPa) [mean]":         (lambda rpm,mp: rpm>400 and mp>100, "mean"),
}
def proc(path,filt,agg):
    post=[]; preTB=[]
    with open(path,newline="") as f:
        r=csv.reader(f,delimiter=";"); h=[x.strip() for x in next(r)]; ix={n:i for i,n in enumerate(h)}
        ri,mi,pi,ci=ix["RPM"],ix["MAP"],ix["Pre IC temperature"],ix["Charge temp"]
        for ln in r:
            try: rpm=float(ln[ri]);mp=float(ln[mi]);p=float(ln[pi]);c=float(ln[ci])
            except (ValueError,IndexError): continue
            if p<=2 or not filt(rpm,mp): continue
            post.append(correct(p)); preTB.append(c)
    n=len(post)
    if n==0: return None
    def reduce(v):
        if agg=="mean": return sum(v)/len(v)
        vs=sorted(v); return vs[int(0.99*(len(vs)-1))]   # robust peak (p99)
    return reduce(post), reduce(preTB), n
def F(c): return c*9/5+32

for rname,(filt,agg) in REGIONS.items():
    print("="*104); print(rname); print("="*104)
    print(f"{'log':12s}{'hood':5s}{'localF':>7s}{'n':>7s}{'post-turbo':>15s}{'pre-TB':>15s}{'drop across FMIC':>18s}")
    print("-"*104)
    for lbl,hood,af,path in LOGS:
        res=proc(path,filt,agg)
        if res is None:
            print(f"{lbl:12s}{hood:5s}{af:>6d}F{0:>7d}{'  --':>15s}{'  --':>15s}{'  --':>18s}"); continue
        post,pre,n=res; drop=F(post)-F(pre)
        print(f"{lbl:12s}{hood:5s}{af:>6d}F{n:>7d}{post:>9.1f}C{F(post):4.0f}F{pre:>9.1f}C{F(pre):4.0f}F"
              f"{drop:>+14.0f}F")
    print()
print("post-turbo = corrected Pre-IC (compressor outlet) | pre-TB = Charge/IAT at throttle body")
print("drop across FMIC = post-turbo - pre-TB (real intercooling only under boost; <=0 at idle/cruise = manifold soak)")
print("IDLE values are PEAK (p99) after soak; CRUISE/BOOST are mean.")
