"""Running dataset: oil pressure vs DBW output duty (and airflow/TPS) at ~1000 rpm hot idle,
ignition held near the idle target (17-19 deg), across every EMU log that carries the channels.

Re-run any time. Every log found in SOURCES that has the required channels is (re)scanned, so a
new log just needs to land in one of those folders. Outputs beside this script:
  samples.csv   one row per gated log sample (all logs, tagged by log name + file mtime)
  table.md      the big table: oil-pressure bins x {DBW Out. DC, Idle air %, TPS, MAP, RPM, n}
  scatter.png   OP vs DBW Out. DC, coloured by log date
Gate (all must hold): Idle state == 2, |RPM-1000| <= RPM_TOL, 17 <= Ignition Angle <= 19,
  Engine oil pressure status == 1 (when present), OP >= 0.5 bar, MAP < 60, AC Clutch == 0 (when present).
"""
import os, sys, glob, io, datetime as dt
import numpy as np, pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EMU  = r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra"
SOURCES = [EMU, os.path.join(EMU, "misc log csv"), os.path.join(EMU, "LogAutosave"),
           os.path.join(REPO, "supra", "logs"), os.path.join(REPO, "supra", "tunes")]
RPM_C, RPM_TOL = 1000, 50
IGN_LO, IGN_HI = 17.0, 19.0
NEED = ["TIME","RPM","Engine oil pressure","DBW Out. DC","Ignition Angle","Idle state","Idle air %","TPS","MAP","CLT"]
OPT  = ["Engine oil pressure status","AC Clutch","Coolant fan","Idle PID air % correction","Idle target",
        "DBW target","Battery voltage","IAT","Idle ignition correction","Estimated airflow"]
OP_EDGES = np.arange(1.0, 8.01, 0.25)
# Logs that duplicate another log's samples: keep only the TIME window that is unique to them.
# fullchannels.csv (2026-09-19) = whencold.csv verbatim for t 0-602 s, then the post-TB-clean afternoon.
TRIM = {"fullchannels.csv": (611.0, None)}

def header(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.readline().rstrip("\n").split(";")

def scan(path):
    cols = header(path)
    if any(c not in cols for c in NEED): return None
    use = NEED + [c for c in OPT if c in cols]
    df = pd.read_csv(path, sep=";", usecols=use, low_memory=False)
    lo, hi = TRIM.get(os.path.basename(path).lower(), (None, None))
    if lo is not None: df = df[df["TIME"] >= lo]
    if hi is not None: df = df[df["TIME"] <= hi]
    g = (df["Idle state"] == 2) & (df["RPM"].sub(RPM_C).abs() <= RPM_TOL) \
        & df["Ignition Angle"].between(IGN_LO, IGN_HI) & (df["Engine oil pressure"] >= 0.5) & (df["MAP"] < 60)
    if "Engine oil pressure status" in df: g &= df["Engine oil pressure status"] == 1
    if "AC Clutch" in df: g &= df["AC Clutch"] == 0
    out = df[g].copy()
    if out.empty: return out
    out["log"] = os.path.splitext(os.path.basename(path))[0]
    out["log_date"] = dt.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d")
    out["MAPxRPM_k"] = out["MAP"] * out["RPM"] / 1000.0   # engine-side air proxy: throttle is choked at idle, so MAP*RPM ~ mass flow
    out["op_bin"] = OP_EDGES[np.clip(np.searchsorted(OP_EDGES, out["Engine oil pressure"], side="right")-1, 0, len(OP_EDGES)-2)]
    return out

def main():
    parts, seen = [], set()
    for d in SOURCES:
        for p in sorted(glob.glob(os.path.join(d, "*.csv"))):
            key = os.path.basename(p).lower()
            if key in seen or os.path.getsize(p) < 20000: continue
            seen.add(key)
            try: s = scan(p)
            except Exception as e: print(f"  skip {key}: {e}"); continue
            if s is None: continue
            print(f"  {key:60s} n={len(s)}")
            if len(s): parts.append(s)
    allp = pd.concat(parts, ignore_index=True)
    allp.to_csv(os.path.join(HERE, "samples.csv"), index=False)
    write_table(allp); plot(allp)

def q(s, p): return float(np.nanpercentile(s, p)) if len(s) else np.nan

def write_table(a):
    L = [f"# Oil pressure vs DBW output duty at ~{RPM_C} rpm (ign {IGN_LO:g}-{IGN_HI:g} deg)\n",
         f"Generated {dt.datetime.now():%Y-%m-%d %H:%M} by `running_op_vs_dbw.py`. Gate: `Idle state`==2, "
         f"|RPM-{RPM_C}|<={RPM_TOL}, {IGN_LO:g}<=`Ignition Angle`<={IGN_HI:g}, OP status 1, OP>=0.5 bar, MAP<60, A/C off. "
         f"n = {len(a)} samples from {a.log.nunique()} logs.\n",
         "`DBW Out. DC` is motor drive duty (negative = closing force), NOT position. `Idle air %` is the idle "
         "strategy's commanded airflow (= `Idle effective DC` on this build); `TPS` is the plate position it maps to.\n",
         "## All logs pooled, by oil-pressure bin (0.25 bar)\n",
         "| OP bin [bar] | n | logs | DBW DC p10 | **DBW DC med** | DBW DC p90 | Idle air % med | TPS med | MAP med | RPM med | MAP×RPM/k | CLT med |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for b, g in a.groupby("op_bin"):
        L.append(f"| {b:.2f}-{b+0.25:.2f} | {len(g)} | {g.log.nunique()} | {q(g['DBW Out. DC'],10):.0f} | **{q(g['DBW Out. DC'],50):.0f}** | "
                 f"{q(g['DBW Out. DC'],90):.0f} | {q(g['Idle air %'],50):.1f} | {q(g['TPS'],50):.2f} | {q(g['MAP'],50):.0f} | "
                 f"{q(g['RPM'],50):.0f} | {q(g['MAPxRPM_k'],50):.1f} | {q(g['CLT'],50):.0f} |")
    L += ["\n## Per log (chronological), by oil-pressure bin\n",
          "| log | date | OP bin | n | DBW DC p10 | **DBW DC med** | DBW DC p90 | Idle air % med | TPS med | MAP med | RPM med | MAP×RPM/k | CLT med | PID med |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    a = a.sort_values(["log_date","log"])
    for (d, lg), gl in a.groupby(["log_date","log"], sort=False):
        for b, g in gl.groupby("op_bin"):
            pid = q(g["Idle PID air % correction"],50) if "Idle PID air % correction" in g and g["Idle PID air % correction"].notna().any() else np.nan
            L.append(f"| {lg} | {d} | {b:.2f}-{b+0.25:.2f} | {len(g)} | {q(g['DBW Out. DC'],10):.0f} | **{q(g['DBW Out. DC'],50):.0f}** | "
                     f"{q(g['DBW Out. DC'],90):.0f} | {q(g['Idle air %'],50):.1f} | {q(g['TPS'],50):.2f} | {q(g['MAP'],50):.0f} | "
                     f"{q(g['RPM'],50):.0f} | {q(g['MAPxRPM_k'],50):.1f} | {q(g['CLT'],50):.0f} | {pid:.1f} |")
    L += ["\n## DBW DC distribution per OP bin (count of samples per 5-duty column)\n"]
    dc_edges = list(range(-40, 41, 5))
    L.append("| OP bin | " + " | ".join(f"{e}..{e+5}" for e in dc_edges[:-1]) + " |")
    L.append("|---|" + "---|"*(len(dc_edges)-1))
    for b, g in a.groupby("op_bin"):
        h, _ = np.histogram(g["DBW Out. DC"].clip(-40, 39.9), bins=dc_edges)
        L.append(f"| {b:.2f} | " + " | ".join(str(x) if x else "·" for x in h) + " |")
    open(os.path.join(HERE, "table.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

def plot(a):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2, 2, figsize=(14, 11)); ax = axs.ravel()
    dates = sorted(a.log_date.unique()); cm = plt.get_cmap("viridis", max(len(dates), 2))
    for i, d in enumerate(dates):
        g = a[a.log_date == d]
        ax[0].scatter(g["Engine oil pressure"], g["DBW Out. DC"], s=4, alpha=.35, color=cm(i), label=f"{d} ({g.log.nunique()} log)")
        ax[1].scatter(g["Engine oil pressure"], g["Idle air %"], s=4, alpha=.35, color=cm(i))
        ax[2].scatter(g["Engine oil pressure"], g["TPS"], s=4, alpha=.35, color=cm(i))
        ax[3].scatter(g["Engine oil pressure"], g["MAPxRPM_k"], s=4, alpha=.35, color=cm(i))
    ax[0].set_xlabel("Engine oil pressure [bar]"); ax[0].set_ylabel("DBW Out. DC [%]"); ax[0].set_title(f"~{RPM_C} rpm, ign {IGN_LO:g}-{IGN_HI:g}°: OP vs DBW duty")
    ax[1].set_xlabel("Engine oil pressure [bar]"); ax[1].set_ylabel("Idle air % (commanded airflow)"); ax[1].set_title("OP vs Idle air %")
    ax[2].set_xlabel("Engine oil pressure [bar]"); ax[2].set_ylabel("TPS [%] (plate position)"); ax[2].set_title("OP vs plate position")
    ax[3].set_xlabel("Engine oil pressure [bar]"); ax[3].set_ylabel("MAP × RPM / 1000  (engine-side air proxy)"); ax[3].set_title("OP vs air the engine actually took")
    ax[0].legend(fontsize=7, markerscale=3); [x.grid(alpha=.3) for x in ax]
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "scatter.png"), dpi=130)

if __name__ == "__main__": main()
