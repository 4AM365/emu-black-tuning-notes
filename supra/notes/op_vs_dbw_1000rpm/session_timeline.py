"""Timeline figure for one EMU log: plate position vs DBW target vs duty, RPM vs target, Idle air % vs PID.
usage: python session_timeline.py <log.csv> <out.png> [t0 t1]"""
import sys, pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
p, out = sys.argv[1], sys.argv[2]
t0, t1 = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (None, None)
d = pd.read_csv(p, sep=";", usecols=["TIME","RPM","Idle target","Idle state","TPS","DBW target","DBW Out. DC","Idle air %","Idle PID air % correction","Ignition Angle","Engine oil pressure","CLT","MAP","PPS","Data changing"], low_memory=False)
if t0 is not None: d = d[(d.TIME >= t0) & (d.TIME <= t1)]
fig, ax = plt.subplots(4, 1, figsize=(16, 13), sharex=True)
ax[0].plot(d.TIME, d.RPM, lw=.7, label="RPM"); ax[0].plot(d.TIME, d["Idle target"], lw=.7, label="Idle target"); ax[0].set_ylim(0, 3200); ax[0].set_ylabel("rpm")
a0 = ax[0].twinx(); a0.fill_between(d.TIME, 0, d["Idle state"], step="mid", alpha=.12, color="k", label="Idle state (0/1 armed/2 active/4 ramp)"); a0.set_ylim(0, 8); a0.set_ylabel("Idle state")
ax[1].plot(d.TIME, d.TPS, lw=.8, label="TPS (plate)"); ax[1].plot(d.TIME, d["DBW target"], lw=.8, label="DBW target (commanded)"); ax[1].set_ylim(0, 14); ax[1].set_ylabel("% TPS")
a1 = ax[1].twinx(); a1.plot(d.TIME, d["DBW Out. DC"], lw=.6, color="C3", alpha=.7, label="DBW Out. DC"); a1.set_ylim(-45, 45); a1.set_ylabel("duty %"); a1.axhline(0, color="C3", lw=.3)
ax[2].plot(d.TIME, d["Idle air %"], lw=.8, label="Idle air % (command)"); ax[2].plot(d.TIME, d["Idle PID air % correction"], lw=.8, label="Idle PID air % correction"); ax[2].set_ylim(-30, 100); ax[2].set_ylabel("airflow %")
a2 = ax[2].twinx(); a2.plot(d.TIME, d["Ignition Angle"], lw=.6, color="C2", alpha=.7, label="Ignition Angle"); a2.set_ylim(0, 40); a2.set_ylabel("deg")
ax[3].plot(d.TIME, d["Engine oil pressure"], lw=.8, label="Oil pressure [bar]"); ax[3].plot(d.TIME, d.MAP/10, lw=.6, label="MAP/10 [kPa]"); ax[3].plot(d.TIME, d.CLT/20, lw=.6, label="CLT/20 [°C]"); ax[3].plot(d.TIME, d.PPS/10, lw=.5, label="PPS/10"); ax[3].set_ylabel("bar / scaled"); ax[3].set_xlabel("TIME [s]")
chg = d.TIME[d["Data changing"] > 0]
for x in ax: 
    x.grid(alpha=.3)
    for t in chg: x.axvline(t, color="orange", lw=.4, alpha=.5)
for x, a in [(ax[0], a0), (ax[1], a1), (ax[2], a2)]:
    h1, l1 = x.get_legend_handles_labels(); h2, l2 = a.get_legend_handles_labels(); x.legend(h1+h2, l1+l2, fontsize=8, loc="upper right")
ax[3].legend(fontsize=8, loc="upper right")
fig.suptitle(f"{p.split(chr(92))[-1]}  — orange ticks = live tune edits (Data changing)"); fig.tight_layout(); fig.savefig(out, dpi=110)
