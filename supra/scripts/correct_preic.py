import csv, bisect
SUP=r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra"; LA=SUP+r"\LogAutosave"

# WRONG curve currently applied to Pre-IC ("Custom temp cal 1") : V -> T
WRONG_V=[0.00,0.55,0.57,1.67,2.22,2.76,3.31,3.88,4.43,4.98]
WRONG_T=[92,  55,  54,  15,  3,   -5,  -15, -24, -33, -40]
# CORRECT curve (real IAT calibration) : V -> T
RIGHT_V=[0.00,0.24,0.31,0.45,0.78,1.00,1.45,1.73,2.47,2.96,3.63,4.10,4.63,4.98]
RIGHT_T=[121, 115, 104, 91,  71,  62,  49,  42,  27,  18,  6,   -5,  -22, -39]

def interp(x, xs, ys):
    if x<=xs[0]: return ys[0]
    if x>=xs[-1]: return ys[-1]
    i=bisect.bisect_right(xs,x)-1
    f=(x-xs[i])/(xs[i+1]-xs[i]); return ys[i]+f*(ys[i+1]-ys[i])

def temp_to_V_wrong(t):           # invert wrong curve (T decreasing) -> V
    Td=list(reversed(WRONG_T)); Vd=list(reversed(WRONG_V))  # now T ascending
    return interp(t, Td, Vd)
def V_to_temp_right(v): return interp(v, RIGHT_V, RIGHT_T)
def correct(t_wrong): return V_to_temp_right(temp_to_V_wrong(t_wrong))

# sanity
for tw in [3,15,17,24,31,41,54]:
    print(f"  Pre-IC logged {tw:4.0f}C -> V {temp_to_V_wrong(tw):.3f} -> corrected {correct(tw):5.1f}C")
print()

# ---- validate recovered V against raw Analog channels (full-channel log) ----
def find_analog(path, n=8):
    with open(path,newline="") as f:
        r=csv.reader(f,delimiter=";"); hdr=[h.strip() for h in next(r)]
        idx={h:i for i,h in enumerate(hdr)}
        acols=[f"Analog {k}" for k in range(1,7) if f"Analog {k}" in idx]
        pic=idx["Pre IC temperature"]
        print(f"VALIDATION on {path.split(chr(92))[-1]} (Pre-IC logged, recovered V, raw analogs):")
        cnt=0
        for line in r:
            try: t=float(line[pic])
            except (ValueError,IndexError): continue
            if cnt%4000==0 and cnt<24000:
                vs={a: line[idx[a]] for a in acols}
                print(f"   PreIC={t:5.1f}C recV={temp_to_V_wrong(t):.3f}  "+" ".join(f"{a}={vs[a]}" for a in acols))
            cnt+=1
            if cnt>=24000: break

find_analog(LA+r"\drive_home_today.csv")
print()

# ---- reprocess hood logs with corrected Pre-IC ----
LOGS=[("0509 ON 104F","ON",LA+r"\hood on 0509 terrible day.csv"),
      ("0514 ON  99F","ON",LA+r"\hood on 0514.csv"),
      ("hood-OFF 97F","OFF",SUP+r"\hood-removed.csv")]
def proc(path):
    out={"all":[], "idle":[]}
    with open(path,newline="") as f:
        r=csv.reader(f,delimiter=";"); hdr=[h.strip() for h in next(r)]
        idx={h:i for i,h in enumerate(hdr)}
        ri,mi,pi,ci=idx["RPM"],idx["MAP"],idx["Pre IC temperature"],idx["Charge temp"]
        for line in r:
            try: rpm=float(line[ri]); mp=float(line[mi]); pre=float(line[pi]); chg=float(line[ci])
            except (ValueError,IndexError): continue
            if rpm<=400 or mp>=100 or pre<=2: continue
            rec=(correct(pre),chg)
            out["all"].append(rec)
            if rpm<1500 and mp<60: out["idle"].append(rec)
    return out
def mean(v): return sum(v)/len(v) if v else float('nan')
def F(c): return c*9/5+32

cache={lbl:proc(p) for lbl,h,p in LOGS}
for grp in ("all","idle"):
    print("="*72); print(f"CORRECTED Pre-IC  [{grp} , MAP<100]"); print("="*72)
    print(f"{'log':14s}{'PreIC_corr':>12s}{'Charge':>10s}{'PreIC-Charge':>14s}")
    for lbl,h,p in LOGS:
        d=cache[lbl][grp]; pc=mean([x[0] for x in d]); cg=mean([x[1] for x in d])
        print(f"{lbl:14s}{pc:8.1f}C{F(pc):4.0f}F{cg:7.1f}C{pc-cg:>+11.1f}C")
    print()
