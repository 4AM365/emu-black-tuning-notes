"""
Airflow-requirement surface vs oil pressure.

GOAL   For each oil-pressure bin {2,3,4,5,6} bar, a table of the idle airflow %
       that was actually sustaining the engine, indexed RPM (Y) x CLT (X) on the
       EMU `Airflow - Active state air flow [%]` axes.

METHOD  Every sample where the idle controller owns the throttle (Idle state ==
        ACTIVE) and RPM is genuinely being held steady is one observation of
        "this much air sustains this RPM at this CLT and this oil pressure".
        Bin each observation to the nearest axis value; report the median.

Scaling facts verified in `supra/tunes/supra 06132026.xml.emub3`:
  idleCoolantFanCorr = 13 (airflow %), idleDBWTargetMin/Max = 2.4 / 8.0 % TPS.
"""
import os, csv, json, datetime as dt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------- parameters
WINDOW_START = dt.datetime(2026, 6, 5)      # "past two months" from 2026-08-05
WINDOW_END   = dt.datetime(2026, 8, 6)
SEARCH_DIRS = [
    r"C:\Users\WTCra\Desktop",                  # Will's working exports (pointed here 2026-08-05)
    r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra",
    r"C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra\LogAutosave",
    r"C:\Code\car-projects\emu-black-tuning-notes\supra\logs",
    r"C:\Code\car-projects\emu-black-tuning-notes\supra\tunes",
]

OP_BINS  = np.array([2, 3, 4, 5, 6], float)                    # bar
RPM_BINS = np.array([1000, 1100, 1200, 1375, 1500], float)     # EMU idle-target axis
CLT_BINS = np.array([0, 15, 30, 45, 60, 75, 96, 105], float)   # EMU CLT axis

FAN_CORR      = 13.0    # idleCoolantFanCorr, airflow %
STEADY_SEC    = 1.0     # +/- window for the RPM-steadiness test
STEADY_SD     = 25.0    # rpm; max rolling sigma to call RPM "sustained"
ENTRY_AGE_SEC = 15.0    # skip the armed->active handoff transient
MAP_MAX       = 60.0    # kPa; no load
RPM_GUARD_LO  = 950.0   # below half a bin under the axis -> not representable
RPM_GUARD_HI  = 1562.5  # 1500 + (1500-1375)/2

OUT = os.path.dirname(os.path.abspath(__file__))

COLS = ["TIME", "RPM", "MAP", "CLT", "Engine oil pressure", "Engine oil pressure status",
        "Idle air %", "Idle state", "Idle target", "Idle PID air % correction",
        "Idle airflow custom corr.", "Coolant fan", "AC Clutch", "TPS", "PPS"]


# ---------------------------------------------------------------- discovery
def discover():
    found = []
    for d in SEARCH_DIRS:
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.lower().endswith(".csv"):
                continue
            p = os.path.join(d, fn)
            st = os.stat(p)
            m = dt.datetime.fromtimestamp(st.st_mtime)
            if not (WINDOW_START <= m < WINDOW_END):
                continue
            if st.st_size < 20_000:
                found.append((p, m, "skip: file < 20 kB"))
                continue
            with open(p, encoding="utf-8", errors="replace", newline="") as f:
                hdr = [h.strip() for h in next(csv.reader(f, delimiter=";"))]
            if "Engine oil pressure" not in hdr:
                found.append((p, m, "skip: no oil-pressure channel"))
                continue
            missing = [c for c in ("RPM", "CLT", "Idle air %", "Idle state") if c not in hdr]
            if missing:
                found.append((p, m, f"skip: missing {missing}"))
                continue
            found.append((p, m, "read"))
    return found


def load(path):
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        hdr = [h.strip() for h in next(csv.reader(f, delimiter=";"))]
    use = [c for c in COLS if c in hdr]
    df = pd.read_csv(path, sep=";", usecols=use, low_memory=False)
    df.columns = df.columns.str.strip()
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def fingerprint(df):
    """Coarse content signature -> detects a reduced-column re-export of the same drive."""
    r = df[df["RPM"] > 400]
    if r.empty:
        return frozenset()
    s = r.iloc[::50]
    return frozenset(zip(s["TIME"].round(2), s["RPM"].round(0),
                         s["Engine oil pressure"].round(2)))


# ---------------------------------------------------------------- masking
TARGET_DEV = 50.0       # rpm; "held at target" envelope (Will, 2026-08-05)


def gate(df, tag, entry_age=ENTRY_AGE_SEC, steady_sd=STEADY_SD, mode="steady"):
    """mode: 'steady'  RPM locally not moving (sigma test) -- physics definition
             'target'  RPM within +/-TARGET_DEV of Idle target -- control definition
             'either'  union of the two (the strictly-widest envelope)"""
    """Return the frame of samples that are a valid observation of sustained idle."""
    d = df.copy()
    dtm = d["TIME"].diff().median()
    win = max(3, int(round(2 * STEADY_SEC / dtm)) | 1)          # odd, centred

    # contiguous-time blocks so the rolling window never spans a recording gap
    blk = (d["TIME"].diff() > 3 * dtm).cumsum()
    d["rpm_sd"] = d.groupby(blk)["RPM"].transform(
        lambda s: s.rolling(win, center=True, min_periods=win).std())

    # age within the current uninterrupted run of Idle state == 2
    run = (d["Idle state"] != d["Idle state"].shift()).cumsum()
    d["entry_age"] = d["TIME"] - d.groupby(run)["TIME"].transform("first")

    cond = {
        "engine running (RPM>400)":        d["RPM"] > 400,
        "idle state == 2 (ACTIVE)":        d["Idle state"] == 2,
        f"MAP < {MAP_MAX:.0f} kPa":        d["MAP"] < MAP_MAX if "MAP" in d else True,
        f"entry age > {entry_age:.0f}s":   d["entry_age"] > entry_age,
        f"RPM envelope [{mode}]":          {
            "steady": d["rpm_sd"] < steady_sd,
            "target": (d["RPM"] - d["Idle target"]).abs() <= TARGET_DEV,
            "either": (d["rpm_sd"] < steady_sd)
                      | ((d["RPM"] - d["Idle target"]).abs() <= TARGET_DEV),
        }[mode],
        "airflow logged (>0)":             d["Idle air %"] > 0,
        "oil pressure present":            d["Engine oil pressure"].notna(),
        "CLT present":                     d["CLT"].notna(),
    }
    if "Engine oil pressure status" in d:
        cond["oil press. status == 1"] = d["Engine oil pressure status"] == 1
    if "AC Clutch" in d:
        cond["A/C clutch off"] = d["AC Clutch"] == 0

    m = pd.Series(True, index=d.index)
    trace = []
    for name, c in cond.items():
        c = pd.Series(c, index=d.index) if not isinstance(c, pd.Series) else c
        c = c.fillna(False)
        before = int(m.sum())
        m &= c
        trace.append((name, before, int(m.sum())))

    d = d[m].copy()
    d["log"] = tag
    if "Coolant fan" not in d:
        d["Coolant fan"] = np.nan
    return d, trace


def nearest(vals, bins):
    return bins[np.abs(vals.to_numpy()[:, None] - bins[None, :]).argmin(axis=1)]


# ---------------------------------------------------------------- run
def main():
    disc = discover()
    print("LOG DISCOVERY  (mtime window "
          f"{WINDOW_START:%Y-%m-%d} .. {WINDOW_END - dt.timedelta(days=1):%Y-%m-%d})")
    for p, m, why in disc:
        print(f"  {m:%Y-%m-%d}  {os.path.basename(p)[:52]:52} {why}")

    raw, seen = {}, {}
    for p, m, why in disc:
        if why != "read":
            continue
        tag = os.path.splitext(os.path.basename(p))[0]
        df = load(p)
        fp = fingerprint(df)
        dup = next((o for o, ofp in seen.items()
                    if fp and ofp and len(fp & ofp) / min(len(fp), len(ofp)) > 0.95), None)
        if dup:
            print(f"\n  !! {tag}: duplicate content of '{dup}' -> dropped (would double-weight)")
            continue
        seen[tag] = fp
        raw[tag] = df

    def build(entry_age=ENTRY_AGE_SEC, steady_sd=STEADY_SD, verbose=False, mode="steady"):
        frames = []
        for tag, df in raw.items():
            g, tr = gate(df, tag, entry_age, steady_sd, mode)
            if verbose:
                print(f"\n  {tag}: {len(df)} rows -> {len(g)} usable "
                      f"({len(g)/25:.0f}s of sustained idle)")
                for name, b, a in tr:
                    print(f"       {name:34} {b:7d} -> {a:7d}")
            if len(g):
                frames.append(g)
        if not frames:
            return pd.DataFrame()
        t = pd.concat(frames, ignore_index=True)
        keep = (t["RPM"] >= RPM_GUARD_LO) & (t["RPM"] <= RPM_GUARD_HI)
        if verbose:
            print(f"\nPOOLED {len(t)} samples ({len(t)/25/60:.1f} min). "
                  f"Dropped {int((~keep).sum())} outside the RPM axis span "
                  f"[{RPM_GUARD_LO:.0f},{RPM_GUARD_HI:.0f}].")
        t = t[keep].copy()
        t["op_bin"] = nearest(t["Engine oil pressure"], OP_BINS)
        return t

    # ---- sensitivity: does the gate choice move the answer? --------------
    print("\nGATE SENSITIVITY — median airflow % per oil-pressure bin (n)")
    print(f"  {'entry_age / sd':>16} | " + " | ".join(f"{b:.0f} bar" for b in OP_BINS))
    for ea, sd in [(0, 25), (5, 25), (15, 25), (30, 25), (15, 15), (15, 50)]:
        t = build(ea, sd)
        cellstr = []
        for b in OP_BINS:
            sub = t[t["op_bin"] == b]
            cellstr.append(f"{sub['Idle air %'].median():5.1f} ({len(sub):5d})" if len(sub) else "    — (    0)")
        print(f"  {ea:6.0f}s / {sd:4.0f} | " + " | ".join(cellstr))

    print("\nRPM-ENVELOPE COMPARISON — median airflow % per oil-pressure bin (n)")
    for mode in ("steady", "target", "either"):
        t = build(mode=mode)
        cs = []
        for b in OP_BINS:
            sub = t[t["op_bin"] == b]
            cs.append(f"{sub['Idle air %'].median():5.1f} ({len(sub):5d})" if len(sub) else "    — (    0)")
        lo = t[t["RPM"] < 1050]
        print(f"  {mode:>7} | " + " | ".join(cs) + f"   | samples <1050 rpm: {len(lo)}")

    MODE = os.environ.get("ENVELOPE", "target")
    print(f"\n>>> building tables with RPM envelope = '{MODE}'")
    s = build(verbose=True, mode=MODE)

    # ---- axis assignment -------------------------------------------------
    s["op_bin"]  = nearest(s["Engine oil pressure"], OP_BINS)
    s["rpm_bin"] = nearest(s["RPM"], RPM_BINS)
    s["clt_bin"] = nearest(s["CLT"], CLT_BINS)
    s["tgt_bin"] = nearest(s["Idle target"], RPM_BINS) if "Idle target" in s else np.nan
    # Some logs omit `Coolant fan`. Impute it ONLY where the logs that do carry it leave no
    # doubt: measured engage share is 0.000 at CLT <= 75 (n=4326) and 0.999 at CLT >= 95
    # (n=6172); the 75-95 band is genuinely mixed (0.09-0.75) and stays NaN, so those samples
    # drop out of the fan-removed table rather than being guessed.
    # (`coolantFanActTemp`=70 / `coolantFanHyst`=7 in the tune, but the observed switch sits
    #  nearer 80 -- trust the measurement, not the scalar.)
    fan = s["Coolant fan"].copy()
    miss = fan.isna()
    fan[miss & (s["CLT"] >= 95)] = 1.0
    fan[miss & (s["CLT"] <= 75)] = 0.0
    s["fan_used"] = fan
    s["air_nofan"] = s["Idle air %"] - FAN_CORR * fan

    # Rails are the CONFIGURED PID output limits, NOT each log's own minimum. A settled -4 is
    # a FREE output (idleAirPIDOutMin/Max = -6/+15 in the 06/13 tune, floor widened to -10 by
    # August) -- treating it as a clamp is the documented mis-read. A rail must be (a) at least
    # as extreme as the tightest shipped limit and (b) sat on by >=1% of that log's samples.
    #   railed_lo = loop wanted LESS air, none left to remove  -> cell is an UPPER bound
    #   railed_hi = loop wanted MORE air, none left to give    -> cell is a LOWER bound
    s["railed_lo"] = False
    s["railed_hi"] = False
    for tag, g in s.groupby("log"):
        v = g["Idle PID air % correction"]
        lo, hi = v.min(), v.max()
        if lo <= -5.9:
            at = v <= lo + 0.05
            if at.mean() >= 0.01:
                s.loc[g.index[at], "railed_lo"] = True
        if hi >= 14.9:
            at = v >= hi - 0.05
            if at.mean() >= 0.01:
                s.loc[g.index[at], "railed_hi"] = True
    s["railed"] = s["railed_lo"] | s["railed_hi"]
    s["episode"] = s["log"] + "|" + (s["TIME"] // 5).astype(int).astype(str)

    print("\nOIL-PRESSURE BIN OCCUPANCY (nearest-bin lumping, per instruction)")
    for b in OP_BINS:
        sub = s[s["op_bin"] == b]
        if len(sub):
            print(f"  {b:.0f} bar: n={len(sub):6d}  actual OP range "
                  f"{sub['Engine oil pressure'].min():.2f}-{sub['Engine oil pressure'].max():.2f}  "
                  f"median {sub['Engine oil pressure'].median():.2f}")
        else:
            print(f"  {b:.0f} bar: n=0")

    # ---- aggregate -------------------------------------------------------
    def agg(g):
        return pd.Series({
            "air":      g["Idle air %"].median(),
            "air_q25":  g["Idle air %"].quantile(.25),
            "air_q75":  g["Idle air %"].quantile(.75),
            "air_nofan": g["air_nofan"].median(),
            "n":        len(g),
            "n_ep":     g["episode"].nunique(),
            "n_logs":   g["log"].nunique(),
            "op_med":   g["Engine oil pressure"].median(),
            "rpm_med":  g["RPM"].median(),
            "clt_med":  g["CLT"].median(),
            "fan_frac": g["fan_used"].mean(),
            "n_fan_known": int(g["fan_used"].notna().sum()),
            "rail_frac": g["railed_lo"].mean(),
            "rail_hi_frac": g["railed_hi"].mean(),
            "pid_med":  g["Idle PID air % correction"].median() if "Idle PID air % correction" in g else np.nan,
        })

    cells = (s.groupby(["op_bin", "rpm_bin", "clt_bin"], observed=True)
               .apply(agg, include_groups=False).reset_index())
    cells.to_csv(os.path.join(OUT, "cells.csv"), index=False)

    cells_t = (s.groupby(["op_bin", "tgt_bin", "clt_bin"], observed=True)
                 .apply(agg, include_groups=False).reset_index()
                 .rename(columns={"tgt_bin": "rpm_bin"}))
    cells_t.to_csv(os.path.join(OUT, "cells_by_idle_target.csv"), index=False)

    s.to_csv(os.path.join(OUT, "pooled_samples.csv"), index=False)

    # ---- render ----------------------------------------------------------
    def render(cells, field, fmt, title, minn=1):
        out = [f"\n### {title}"]
        for b in OP_BINS:
            sub = cells[cells["op_bin"] == b]
            out.append(f"\n**Oil pressure {b:.0f} bar**  (n={int(sub['n'].sum()) if len(sub) else 0})\n")
            head = "| RPM＼CLT | " + " | ".join(f"{c:.0f}" for c in CLT_BINS) + " |"
            out.append(head)
            out.append("|" + "---|" * (len(CLT_BINS) + 1))
            for r in RPM_BINS[::-1]:
                row = [f"| **{r:.0f}** "]
                for c in CLT_BINS:
                    m = sub[(sub["rpm_bin"] == r) & (sub["clt_bin"] == c)]
                    if len(m) and m.iloc[0]["n"] >= minn and pd.notna(m.iloc[0][field]):
                        mark = "†" if (field.startswith("air") and m.iloc[0]["rail_frac"] > 0.2) else ""
                        row.append(f"| {fmt(m.iloc[0][field])}{mark} ")
                    else:
                        row.append("| — ")
                out.append("".join(row) + "|")
        return "\n".join(out)

    # ---- coverage / operating locus --------------------------------------
    total = len(OP_BINS) * len(RPM_BINS) * len(CLT_BINS)
    print(f"\nCOVERAGE: {len(cells)} of {total} cells hold data "
          f"({len(cells)/total:.0%}); {len(cells[cells['n'] >= 25])} hold >=1 s.")
    print("\nOPERATING LOCUS — the axes are not independent, so most of the cube is unvisitable")
    print(f"  {'CLT bin':>8} | {'n':>6} | oil pressure seen (bar)   | RPM held")
    for c in CLT_BINS:
        sub = s[s["clt_bin"] == c]
        if not len(sub):
            print(f"  {c:8.0f} | {0:6d} | (no samples)")
            continue
        print(f"  {c:8.0f} | {len(sub):6d} | {sub['Engine oil pressure'].min():.2f}"
              f" - {sub['Engine oil pressure'].max():.2f} (med {sub['Engine oil pressure'].median():.2f})"
              f"  | {sub['RPM'].min():.0f}-{sub['RPM'].max():.0f}")

    md = ["# Airflow required to sustain idle — by oil-pressure bin",
          f"\nGenerated {dt.datetime.now():%Y-%m-%d %H:%M} from logs with mtime "
          f"{WINDOW_START:%Y-%m-%d}..{WINDOW_END - dt.timedelta(days=1):%Y-%m-%d} carrying "
          "`Engine oil pressure`.",
          f"\nGate: Idle state==2 (ACTIVE) · MAP<{MAP_MAX:.0f} · A/C off · entry age>"
          f"{ENTRY_AGE_SEC:.0f}s · rolling sigma(RPM) over +/-{STEADY_SEC}s < {STEADY_SD:.0f} rpm."
          f"\nCell = median total commanded `Idle air %` (base + fan {FAN_CORR:.0f} + custom + PID).",
          render(cells, "air", lambda v: f"{v:.1f}", "Airflow % — Y = actual RPM held"),
          render(cells, "n", lambda v: f"{int(v)}", "Sample count (n, 25 Hz)"),
          render(cells, "air_nofan", lambda v: f"{v:.1f}",
                 f"Airflow % with the fan's +{FAN_CORR:.0f} removed (engine-only requirement)"),
          render(cells_t, "air", lambda v: f"{v:.1f}",
                 "Airflow % — Y = Idle TARGET (EMU table indexing)"),
          render(cells_t, "n", lambda v: f"{int(v)}", "Sample count, Y = Idle target"),
          ]
    open(os.path.join(OUT, "tables.md"), "w", encoding="utf-8").write("\n".join(md))
    print("\n" + "\n".join(md[3:]))
    print(f"\nwrote {OUT}\\tables.md, cells.csv, cells_by_idle_target.csv")


if __name__ == "__main__":
    main()
