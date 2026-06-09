import csv

SRC = r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra"
# ambient anchors (C)
AMB = {"HOOD ON (05/06)": 21.0, "HOOD OFF (now)": 36.1}  # 70F morning May6 vs 97F now
FILES = {
    "HOOD ON (05/06)": SRC + r"\hood on 0506 terrible day.csv",
    "HOOD OFF (now)":  SRC + r"\hood-removed.csv",
}

def load(path):
    rows = []
    with open(path, newline="") as f:
        r = csv.reader(f, delimiter=";")
        hdr = [h.strip() for h in next(r)]
        idx = {name: i for i, name in enumerate(hdr)}
        for line in r:
            if len(line) < len(hdr) - 1: continue
            try:
                rows.append(dict(
                    t=float(line[idx["TIME"]]), rpm=float(line[idx["RPM"]]),
                    map=float(line[idx["MAP"]]), preic=float(line[idx["Pre IC temperature"]]),
                    chg=float(line[idx["Charge temp"]]), egt1=float(line[idx["EGT 1"]])))
            except (ValueError, KeyError): continue
    return rows

def med(v):
    v = sorted(v); n = len(v)
    return v[n//2] if n else float("nan")
def mean(v): return sum(v)/len(v) if v else float("nan")

data = {k: load(p) for k, p in FILES.items()}

# --- Pre-IC dropout check ---
print("PRE-IC SENSOR HEALTH (fraction of running samples reading <=2C = dropout):")
for k, rows in data.items():
    run = [r for r in rows if r["rpm"] > 400]
    drop = sum(1 for r in run if r["preic"] <= 2)
    print(f"  {k:18s}  {drop}/{len(run)} = {100*drop/len(run):.1f}% dropout")
print()

print("="*78)
print("CHARGE-TEMP RISE OVER AMBIENT  (the hood signal; absolute temps confounded by weather)")
print("="*78)
print(f"{'condition':28s}{'HOOD ON':>16s}{'HOOD OFF':>16s}{'delta':>10s}")
print(f"{'ambient (C / F)':28s}{AMB['HOOD ON (05/06)']:6.1f} /{AMB['HOOD ON (05/06)']*9/5+32:5.0f}"
      f"{AMB['HOOD OFF (now)']:8.1f} /{AMB['HOOD OFF (now)']*9/5+32:5.0f}")
print("-"*78)

def grp(rows, cond):
    return [r for r in rows if cond(r)]
conds = {
    "IDLE  (rpm<1500,MAP<60)":  lambda r: r["rpm"]>400 and r["rpm"]<1500 and r["map"]<60,
    "CRUISE(1500-3500,MAP<90)": lambda r: 1500<=r["rpm"]<3500 and r["map"]<90,
    "LIGHT (MAP 60-90)":        lambda r: r["rpm"]>400 and 60<=r["map"]<90,
}
for name, c in conds.items():
    vals = {}
    for k, rows in data.items():
        g = grp(rows, c)
        chg = mean([r["chg"] for r in g])
        vals[k] = chg - AMB[k]
    on, off = vals["HOOD ON (05/06)"], vals["HOOD OFF (now)"]
    print(f"{name:28s}{on:>14.1f}C{off:>14.1f}C{off-on:>+8.1f}C")

print()
print("  (positive delta = hood-off runs HOTTER over ambient; negative = hood-off COOLER)")
print()

# --- MAP-matched charge temp (absolute) ---
print("="*78)
print("MAP-MATCHED ABSOLUTE CHARGE TEMP (C)  — same flow, different ambient")
print("="*78)
print(f"{'MAP bin (kPa)':16s}{'HOOD ON chg':>14s}{'HOOD OFF chg':>14s}{'  n_on/n_off':>16s}")
bins = [(20,40),(40,60),(60,80),(80,100),(100,130),(130,200)]
for lo,hi in bins:
    row=[]
    ns=[]
    for k,rows in data.items():
        g=[r for r in rows if r["rpm"]>400 and lo<=r["map"]<hi]
        row.append(mean([r["chg"] for r in g]) if g else float("nan"))
        ns.append(len(g))
    print(f"{lo:3d}-{hi:<11d}{row[0]:>13.1f}{row[1]:>14.1f}{ns[0]:>9d}/{ns[1]:<6d}")
