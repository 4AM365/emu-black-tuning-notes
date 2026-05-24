"""Local analysis of 20260524_1301.csv — idle quality scan.
Reads only relevant channels to keep memory + token cost low."""
import pandas as pd
import numpy as np
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import os
CSV = os.path.join(os.path.dirname(__file__), "..", "logs", "20260524_1301.csv")

KEEP = [
    "TIME","RPM","MAP","TPS","PPS","CLT","IAT","Charge temp","Ethanol content",
    "Idle target","Idle air %","Idle PID air % correction","Idle ignition correction",
    "I.Idle","Idle state","Idle effective DC","Idle force open loop","Idle control active",
    "Idle airflow custom corr.","Idle airflow custom corr. active","Idle ramp down offset",
    "Idle ignition target","Idle motor step",
    "ECU State","Ignition Angle","Ignition From Table",
    "Lambda 1","Lambda 2","Lambda target","Lambda target from table","Lambda is valid",
    "Short term trim","AFR","VE","Injectors PW",
    "Knock count","Knock Level Peak","Knock Engine Noise","Knocking cylinders","Knock ign corection",
    "Knock ign retard cyl 1","Knock ign retard cyl 2","Knock ign retard cyl 3",
    "Knock ign retard cyl 4","Knock ign retard cyl 5","Knock ign retard cyl 6",
    "Trigger error","Trigger error count","Trigger sync status",
    "Vehicle Speed","Gear","Acc. enrichment %","Afterstart Enrichment","Warmup enrichment",
    "DBW Out. DC","DBW target","Battery voltage","Baro","Fuel Cut","Fuel cut percent",
    "Overrun status","Spark cut percent","VVT CAM1 angle","VVT CAM1 angle target",
    "VVT CAM1 status","Boost","CAM sync trigger tooth",
]

print("Loading header...")
header = pd.read_csv(CSV, sep=";", nrows=0).columns.str.strip().tolist()
keep_present = [c for c in KEEP if c in header]
missing = [c for c in KEEP if c not in header]
print(f"  {len(keep_present)} channels kept, {len(missing)} missing: {missing[:5]}{'...' if len(missing)>5 else ''}")

print("Loading data (chunked)...")
df = pd.read_csv(CSV, sep=";", usecols=keep_present, low_memory=False)
df.columns = df.columns.str.strip()
print(f"  Rows: {len(df):,}  Duration: {df['TIME'].iloc[-1]-df['TIME'].iloc[0]:.1f}s")
print(f"  CLT range: {df['CLT'].min():.0f}..{df['CLT'].max():.0f}°C")
print(f"  RPM range: {df['RPM'].min():.0f}..{df['RPM'].max():.0f}")
print(f"  VSS max: {df['Vehicle Speed'].max():.1f}")
print(f"  Ethanol: {df['Ethanol content'].median():.1f}% (median)")

# Define idle stretches: RPM 600-1700, PPS <= 1%, VSS <= 2, warm engine (CLT > 60)
# At least 3 seconds continuous (this log has little stopped idle time)
idle_mask = (
    (df["RPM"] > 600) & (df["RPM"] < 1700)
    & (df["PPS"] <= 1.0)
    & (df["Vehicle Speed"] <= 2)
    & (df["CLT"] > 60)
    & (df["ECU State"] == 3)
)
print(f"\nIdle samples (warm, foot-off, stopped): {idle_mask.sum():,} ({100*idle_mask.sum()/len(df):.1f}%)")

# Also: foot-off coast (PPS=0, VSS>2) — for overrun handoff issues
coast_mask = (
    (df["PPS"] <= 1.0)
    & (df["Vehicle Speed"] > 2)
    & (df["CLT"] > 60)
    & (df["ECU State"] == 3)
    & (df["RPM"] < 3500)
)
print(f"Foot-off coast samples: {coast_mask.sum():,} ({100*coast_mask.sum()/len(df):.1f}%)")
print(f"Idle state distribution (warm): {df.loc[df['CLT']>60,'Idle state'].value_counts().to_dict()}")

# Find contiguous idle stretches
diff = idle_mask.astype(int).diff().fillna(0)
starts = df.index[diff == 1].tolist()
ends = df.index[diff == -1].tolist()
if idle_mask.iloc[0]: starts = [0] + starts
if idle_mask.iloc[-1]: ends = ends + [len(df)-1]
stretches = [(s,e) for s,e in zip(starts,ends) if (df["TIME"].iloc[e]-df["TIME"].iloc[s]) >= 3]
print(f"Contiguous idle stretches >=3s: {len(stretches)}")
for i,(s,e) in enumerate(stretches[:30]):
    dur = df["TIME"].iloc[e]-df["TIME"].iloc[s]
    sub = df.iloc[s:e+1]
    rpm_mean = sub["RPM"].mean()
    rpm_std = sub["RPM"].std()
    rpm_min = sub["RPM"].min()
    rpm_max = sub["RPM"].max()
    tgt = sub["Idle target"].mean()
    pid = sub["Idle PID air % correction"]
    pid_min, pid_max, pid_mean = pid.min(), pid.max(), pid.mean()
    air = sub["Idle air %"].mean()
    iidle_min = sub["I.Idle"].min()
    iidle_max = sub["I.Idle"].max()
    clt = sub["CLT"].mean()
    lamb = sub["Lambda 1"].mean() if "Lambda 1" in sub.columns else np.nan
    stft = sub["Short term trim"].mean() if "Short term trim" in sub.columns else np.nan
    knock_cyl_max = max([sub[f"Knock ign retard cyl {n}"].max() for n in range(1,7)])
    print(f"  #{i+1:2d} t={df['TIME'].iloc[s]:7.1f}-{df['TIME'].iloc[e]:7.1f}s ({dur:5.1f}s) "
          f"CLT={clt:4.0f} RPM={rpm_mean:4.0f}±{rpm_std:3.0f} [{rpm_min:.0f}..{rpm_max:.0f}] "
          f"tgt={tgt:.0f} air={air:4.1f}% PID=[{pid_min:5.1f}..{pid_max:5.1f}] "
          f"I.idle=[{iidle_min:.1f}..{iidle_max:.1f}] lam={lamb:.2f} STFT={stft:+.1f}% "
          f"knockMax={knock_cyl_max:.1f}")

# Pick the worst stretch by RPM std (proxy for roughness)
metrics = []
for s,e in stretches:
    sub = df.iloc[s:e+1]
    metrics.append((s,e,sub["RPM"].std(),sub["Idle PID air % correction"].max()-sub["Idle PID air % correction"].min(),df["TIME"].iloc[e]-df["TIME"].iloc[s]))
metrics.sort(key=lambda x: -x[2])
print("\n=== TOP 5 ROUGHEST IDLE STRETCHES (by RPM std) ===")
for s,e,rstd,pidrange,dur in metrics[:5]:
    sub = df.iloc[s:e+1]
    print(f"  t={df['TIME'].iloc[s]:7.1f}s ({dur:.1f}s) RPMstd={rstd:.1f} PIDrange={pidrange:.1f}")

# For each top-5 rough stretch dump the data with downsampling
print("\n=== DETAILED LOOK AT THE 3 WORST STRETCHES ===")
for rank,(s,e,rstd,pidrange,dur) in enumerate(metrics[:3]):
    sub = df.iloc[s:e+1].copy()
    # subsample every Nth row to keep output manageable
    n = max(1, len(sub)//40)
    sample = sub.iloc[::n]
    print(f"\n--- Stretch #{rank+1} @ t={df['TIME'].iloc[s]:.1f}s, dur={dur:.1f}s, RPMstd={rstd:.1f} ---")
    cols_show = ["TIME","RPM","Idle target","Idle air %","Idle PID air % correction",
                 "I.Idle","Ignition Angle","Idle state","Lambda 1","Short term trim","CLT","MAP"]
    cols_show = [c for c in cols_show if c in sample.columns]
    print(sample[cols_show].to_string(index=False,float_format="%.2f"))

# Look at PID floor/ceiling events specifically — PID at min or max for sustained period
print("\n=== PID SATURATION EVENTS (idle PID air % correction at extremes) ===")
pid = df["Idle PID air % correction"]
# Find extreme values
pid_lo_thresh = pid.quantile(0.01)
pid_hi_thresh = pid.quantile(0.99)
print(f"  PID 1st pct: {pid_lo_thresh:.1f}  99th pct: {pid_hi_thresh:.1f}")
print(f"  Absolute min/max: {pid.min():.1f} / {pid.max():.1f}")
saturated_lo = idle_mask & (pid <= pid_lo_thresh + 0.5)
saturated_hi = idle_mask & (pid >= pid_hi_thresh - 0.5)
print(f"  Samples at PID floor (during idle): {saturated_lo.sum()}")
print(f"  Samples at PID ceiling (during idle): {saturated_hi.sum()}")

# Knock count progression
print("\n=== KNOCK ACTIVITY ===")
if "Knock count" in df.columns:
    kc = df["Knock count"]
    kc_idle = df.loc[idle_mask,"Knock count"]
    print(f"  Knock count: start={kc.iloc[0]:.0f} end={kc.iloc[-1]:.0f} during-idle delta={kc_idle.iloc[-1]-kc_idle.iloc[0] if len(kc_idle)>0 else 0:.0f}")
for n in range(1,7):
    col=f"Knock ign retard cyl {n}"
    if col in df.columns:
        mx = df.loc[idle_mask,col].max() if idle_mask.sum() else 0
        print(f"  Max idle knock retard cyl {n}: {mx:.1f}")

# Trigger errors
print("\n=== TRIGGER / SYNC ===")
if "Trigger error count" in df.columns:
    print(f"  Trigger error count final: {df['Trigger error count'].iloc[-1]:.0f}")
if "Trigger sync status" in df.columns:
    bad_sync = df[df["Trigger sync status"]!=0]
    print(f"  Bad sync samples: {len(bad_sync)}")

# Lambda excursions during idle
if "Lambda 1" in df.columns and idle_mask.sum() > 100:
    lam_idle = df.loc[idle_mask,"Lambda 1"]
    print(f"\n=== LAMBDA (idle) ===")
    print(f"  Mean: {lam_idle.mean():.3f}  Std: {lam_idle.std():.3f}")
    print(f"  5th/95th pct: {lam_idle.quantile(0.05):.3f} / {lam_idle.quantile(0.95):.3f}")
    print(f"  Min/Max: {lam_idle.min():.3f} / {lam_idle.max():.3f}")

# RPM dip events — sudden drops below target
print("\n=== RPM DIPS (drop > 200 below target while idle) ===")
dip_mask = idle_mask & ((df["Idle target"]-df["RPM"]) > 200)
dip_runs = dip_mask.astype(int).diff().fillna(0)
dip_starts = df.index[dip_runs==1].tolist()
print(f"  Discrete dips: {len(dip_starts)}")
for i,ds in enumerate(dip_starts[:10]):
    t = df["TIME"].iloc[ds]
    rpm_at = df["RPM"].iloc[ds]
    tgt_at = df["Idle target"].iloc[ds]
    print(f"    {i+1}: t={t:.1f}s RPM={rpm_at:.0f} vs target={tgt_at:.0f}")
