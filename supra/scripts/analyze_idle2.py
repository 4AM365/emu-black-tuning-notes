"""Deeper dive — overrun handoffs, idle state 4 (recovery) events, sync status."""
import pandas as pd, numpy as np, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import os
CSV = os.path.join(os.path.dirname(__file__), "..", "logs", "20260524_1301.csv")
KEEP = ["TIME","RPM","MAP","TPS","PPS","CLT","Vehicle Speed","ECU State",
        "Idle target","Idle air %","Idle PID air % correction","Idle ignition correction",
        "I.Idle","Idle state","Idle force open loop","Idle control active",
        "Idle airflow custom corr.","Idle ramp down offset","Idle effective DC",
        "Ignition Angle","Ignition From Table","Lambda 1","Lambda is valid","Lambda target",
        "Short term trim","AFR","Acc. enrichment %","Afterstart Enrichment","Warmup enrichment",
        "Trigger error count","Trigger sync status","Overrun status","Fuel Cut",
        "Knock count","Knocking cylinders","Knock ign corection",
        "Gear","CAM sync trigger tooth","DBW Out. DC","DBW target","Spark cut percent",
        "VVT CAM1 angle","VVT CAM1 angle target","VVT CAM1 status",
        "Knock ign retard cyl 1","Knock ign retard cyl 2","Knock ign retard cyl 3",
        "Knock ign retard cyl 4","Knock ign retard cyl 5","Knock ign retard cyl 6"]

df = pd.read_csv(CSV, sep=";", usecols=lambda c: c.strip() in KEEP, low_memory=False)
df.columns = df.columns.str.strip()
print(f"Loaded {len(df):,} rows, {df['TIME'].iloc[-1]-df['TIME'].iloc[0]:.1f}s")

# Lambda validation check
if "Lambda is valid" in df.columns:
    valid_pct = 100*(df["Lambda is valid"]==1).mean()
    print(f"\nLambda valid: {valid_pct:.1f}% of samples")
    print(f"Lambda 1 distribution: min={df['Lambda 1'].min():.3f} mean={df['Lambda 1'].mean():.3f} "
          f"max={df['Lambda 1'].max():.3f} std={df['Lambda 1'].std():.4f}")
    print(f"AFR: min={df['AFR'].min():.2f} mean={df['AFR'].mean():.2f} max={df['AFR'].max():.2f}")
    print(f"Lambda 1 unique vals (top 5): {df['Lambda 1'].value_counts().head().to_dict()}")
    print(f"STFT non-zero samples: {(df['Short term trim']!=0).sum()}")

# Trigger sync status: what does non-zero mean? Look at distribution and when it occurs
if "Trigger sync status" in df.columns:
    print(f"\nTrigger sync status distribution: {df['Trigger sync status'].value_counts().to_dict()}")
    print(f"  When sync != 0, ECU State distribution: {df.loc[df['Trigger sync status']!=0,'ECU State'].value_counts().to_dict()}")
    print(f"  When sync != 0, RPM distribution: min={df.loc[df['Trigger sync status']!=0,'RPM'].min()} max={df.loc[df['Trigger sync status']!=0,'RPM'].max()}")
    # Pretty sure this is "1=synced, 0=not yet" so high count just means key on / cranking
    print(f"  RPM == 0 sync != 0 samples: {((df['Trigger sync status']!=0) & (df['RPM']==0)).sum()}")

# Idle state distribution warm only
warm = df["CLT"] > 60
print(f"\nIdle state (warm, ECU running):")
print(df.loc[warm & (df["ECU State"]==3),"Idle state"].value_counts().sort_index().to_dict())
print(f"  State 4 (recovery) samples: {((df['Idle state']==4) & warm & (df['ECU State']==3)).sum()}")

# Find every idle-state-4 (recovery) entry — group into events
print("\n=== IDLE STATE 4 (RECOVERY) EVENTS ===")
rec_mask = (df["Idle state"]==4) & warm & (df["ECU State"]==3)
rec_diff = rec_mask.astype(int).diff().fillna(0)
rec_starts = df.index[rec_diff==1].tolist()
rec_ends = df.index[rec_diff==-1].tolist()
if rec_mask.iloc[0]: rec_starts = [0]+rec_starts
if rec_mask.iloc[-1]: rec_ends = rec_ends+[len(df)-1]
events = list(zip(rec_starts,rec_ends))
print(f"  Distinct recovery events: {len(events)}")
for i,(s,e) in enumerate(events[:20]):
    t0 = df["TIME"].iloc[s]; t1 = df["TIME"].iloc[e]
    sub = df.iloc[max(0,s-5):min(len(df),e+10)]
    rpm_min = sub["RPM"].min()
    rpm_pre = df["RPM"].iloc[max(0,s-3)]
    pps_pre = df["PPS"].iloc[max(0,s-3)]
    pid_max = sub["Idle PID air % correction"].max()
    pid_min = sub["Idle PID air % correction"].min()
    vss = df["Vehicle Speed"].iloc[s]
    gear = df["Gear"].iloc[s] if "Gear" in df.columns else -1
    print(f"  #{i+1:2d} t={t0:6.1f}-{t1:6.1f}s ({t1-t0:4.1f}s) RPM_pre={rpm_pre:4.0f} RPM_min={rpm_min:4.0f} "
          f"PPS_pre={pps_pre:4.1f}% PID=[{pid_min:5.1f}..{pid_max:5.1f}] VSS={vss:4.1f} gear={gear:.0f}")

# Overrun → idle handoff search: PPS released, RPM falling toward idle target
# Find moments where PPS goes from >5 to 0 while RPM > 2000
pps_release = (df["PPS"].shift(1) > 5) & (df["PPS"] <= 1) & (df["RPM"] > 2000) & warm
release_pts = df.index[pps_release].tolist()
print(f"\n=== OVERRUN/HANDOFF EVENTS (PPS release at RPM>2000) ===")
print(f"  Total: {len(release_pts)}")
for i,p in enumerate(release_pts[:15]):
    window = df.iloc[p:min(len(df),p+200)]  # ~8 sec
    # Find when RPM first crosses below 1500 (entering idle territory)
    handoff_idx = window.index[window["RPM"]<1500]
    if len(handoff_idx)==0: continue
    ho = handoff_idx[0]
    t0 = df["TIME"].iloc[p]
    rpm_init = df["RPM"].iloc[p]
    # Look 2 sec after handoff
    post = df.iloc[ho:min(len(df),ho+50)]
    rpm_min = post["RPM"].min()
    rpm_argmin = post["RPM"].idxmin()
    rpm_undershoot_t = df["TIME"].iloc[rpm_argmin] - df["TIME"].iloc[ho]
    pid_max_post = post["Idle PID air % correction"].max()
    pid_min_post = post["Idle PID air % correction"].min()
    state_seq = post["Idle state"].drop_duplicates().head(4).tolist()
    iidle_max = post["I.Idle"].max() if "I.Idle" in post.columns else np.nan
    iidle_min = post["I.Idle"].min() if "I.Idle" in post.columns else np.nan
    ig_min = post["Ignition Angle"].min()
    print(f"  #{i+1:2d} t={t0:6.1f}s RPM_init={rpm_init:.0f} handoff_RPM_min={rpm_min:.0f} "
          f"undershoot_at +{rpm_undershoot_t:.2f}s PID=[{pid_min_post:.1f}..{pid_max_post:.1f}] "
          f"states={state_seq} ign_min={ig_min:.1f} I.Idle=[{iidle_min:.1f}..{iidle_max:.1f}]")

# Look at the largest RPM dips overall (not just at "idle")
print("\n=== TOP RPM UNDERSHOOTS (RPM dropping below 900 with warm engine and PPS<=2%) ===")
underdrop = (df["RPM"] > 0) & (df["RPM"] < 900) & (df["PPS"]<=2) & warm & (df["Vehicle Speed"]<5) & (df["ECU State"]==3)
under_diff = underdrop.astype(int).diff().fillna(0)
under_starts = df.index[under_diff==1].tolist()
print(f"  Discrete drops below 900: {len(under_starts)}")
for i,s in enumerate(under_starts[:15]):
    # Find local min around this point
    w = df.iloc[max(0,s-10):min(len(df),s+30)]
    rpm_min = w["RPM"].min()
    rpm_min_t = df["TIME"].iloc[w["RPM"].idxmin()]
    pps_seq = w["PPS"].max()
    pid_at = df["Idle PID air % correction"].iloc[s]
    air_at = df["Idle air %"].iloc[s]
    ign_at = df["Ignition Angle"].iloc[s]
    iidle_at = df["I.Idle"].iloc[s] if "I.Idle" in df.columns else np.nan
    pre_rpm = df["RPM"].iloc[max(0,s-5)]
    print(f"  #{i+1:2d} t={rpm_min_t:6.1f}s RPM_min={rpm_min:3.0f} pre_RPM={pre_rpm:4.0f} "
          f"PPS_max_window={pps_seq:4.1f} air%={air_at:.1f} PID={pid_at:5.1f} I.Idle={iidle_at:.1f} ign={ign_at:.1f}")

# Custom correction activity
if "Idle airflow custom corr." in df.columns:
    cc = df["Idle airflow custom corr."]
    print(f"\nIdle airflow custom correction: min={cc.min():.2f} max={cc.max():.2f} non-zero samples={(cc!=0).sum()}")

# Acc.enrichment fires on every PPS bump — check for excessive transient enrichment
if "Acc. enrichment %" in df.columns:
    ae = df["Acc. enrichment %"]
    print(f"Acc. enrichment %: max={ae.max():.1f} non-zero samples={(ae!=0).sum()}")

# Final sanity print: idle state and ignition correlation
warm_idle = (df["RPM"]<2500) & (df["PPS"]<=1) & (df["CLT"]>60) & (df["ECU State"]==3)
print(f"\n=== IGNITION CORRECTION SUMMARY (warm, PPS<=1, RPM<2500) ===")
for st in [0,1,2,3,4,5]:
    sel = warm_idle & (df["Idle state"]==st)
    if sel.sum()==0: continue
    sub = df.loc[sel]
    print(f"  State {st}: n={sel.sum():5d} I.Idle min/mean/max = {sub['I.Idle'].min():.1f}/{sub['I.Idle'].mean():.1f}/{sub['I.Idle'].max():.1f}  "
          f"PID min/mean/max = {sub['Idle PID air % correction'].min():.1f}/{sub['Idle PID air % correction'].mean():.1f}/{sub['Idle PID air % correction'].max():.1f}  "
          f"RPM mean={sub['RPM'].mean():.0f}")
