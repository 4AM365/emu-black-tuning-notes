# Per start: time and crank revolutions from first RPM>50 to Engine oil pressure >= 1 bar.
# Usage: python opfill.py <log.csv> [...]
import csv,sys,glob,os
files=sys.argv[1:]
for fn in files:
    try:
        f=open(fn,newline='',errors='ignore'); r=csv.reader(f,delimiter=';'); h=[c.strip() for c in next(r)]
    except Exception as e: continue
    if 'Engine oil pressure' not in h or 'RPM' not in h: continue
    it,ir,io,ic=h.index('TIME'),h.index('RPM'),h.index('Engine oil pressure'),h.index('CLT')
    rows=[]
    for row in r:
        try: rows.append((float(row[it]),float(row[ir]),float(row[io]),float(row[ic])))
        except: pass
    i=0;n=len(rows)
    while i<n:
        # a start: RPM 0 -> >0 with OP<0.3
        if rows[i][1]>50 and (i==0 or rows[i-1][1]<=50) and rows[i][2]<0.3:
            t0=rows[i][0]; revs=0; catch=None; peak=0; j=i
            while j<n-1 and rows[j][2]<1.0 and rows[j][0]-t0<15:
                dt=rows[j+1][0]-rows[j][0]; revs+=rows[j][1]/60*dt
                if catch is None and rows[j][1]>800: catch=rows[j][0]
                peak=max(peak,rows[j][1]); j+=1
            if rows[j][2]>=1.0:
                print(f"{os.path.basename(fn):32s} t0={t0:8.2f} CLT={rows[i][3]:5.1f} crank->OP1bar {rows[j][0]-t0:5.2f}s  catch(>800)->OP1bar {(rows[j][0]-catch) if catch else float('nan'):5.2f}s  revs={revs:5.1f} peakRPM={peak:.0f} RPM@OP={rows[j][1]:.0f}")
            i=j
        i+=1
