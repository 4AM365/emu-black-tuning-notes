"""The oil-pressure tables collapsed to the CLT 96 column only.

At fixed coolant temperature the pressure axis IS the oil-viscosity axis, so this is the
2-D view: airflow % vs RPM (rows) vs oil-pressure bin (columns). Reads the pooled sample
set written by build_tables_v2.py (shipped envelope: |RPM - Idle target| <= 50).
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OP_BINS = [2.0, 3.0, 4.0, 5.0, 6.0]
RPM_BINS = [1500.0, 1375.0, 1200.0, 1100.0, 1000.0]      # high at top, EMU order
FAN_CORR = 13.0

CLT_AX = np.array([0, 15, 30, 45, 60, 75, 96, 105], float)
TGT_AX = np.array([1000, 1100, 1200, 1375, 1500], float)
BASE = np.array([                                        # idleActiveAirflow, 06/13 tune
    [65.0, 54.0, 40.0, 28.5, 24.5, 20.0, 16.5, 16.5],
    [74.5, 62.0, 46.0, 35.5, 30.5, 25.5, 21.5, 21.5],
    [81.0, 68.5, 52.5, 42.5, 36.0, 31.0, 26.5, 26.5],
    [86.0, 70.0, 59.0, 50.5, 44.0, 39.0, 35.0, 35.0],
    [87.5, 75.0, 62.0, 52.0, 47.5, 43.5, 40.0, 40.0]])


def lookup(clt, tgt):
    c = np.clip(clt, CLT_AX[0], CLT_AX[-1]); t = np.clip(tgt, TGT_AX[0], TGT_AX[-1])
    j = np.clip(np.searchsorted(CLT_AX, c) - 1, 0, len(CLT_AX) - 2)
    i = np.clip(np.searchsorted(TGT_AX, t) - 1, 0, len(TGT_AX) - 2)
    fc = (c - CLT_AX[j]) / (CLT_AX[j + 1] - CLT_AX[j])
    ft = (t - TGT_AX[i]) / (TGT_AX[i + 1] - TGT_AX[i])
    return ((BASE[i, j] * (1 - fc) + BASE[i, j + 1] * fc) * (1 - ft) +
            (BASE[i + 1, j] * (1 - fc) + BASE[i + 1, j + 1] * fc) * ft)


p = pd.read_csv(os.path.join(HERE, "pooled_samples.csv"))
p = p[p["clt_bin"] == 96].copy()
p["air_nofan"] = p["Idle air %"] - FAN_CORR * p["fan_used"]
p["implied"] = (p["Idle air %"] - FAN_CORR * p["fan_used"]
                - p["Idle airflow custom corr."] - p["Idle PID air % correction"])
p["shipped"] = lookup(p["CLT"].to_numpy(float), p["Idle target"].to_numpy(float))

print(f"CLT 96 bin = nearest-bin span 85.5-100.5 C.  n={len(p)}  "
      f"actual CLT {p.CLT.min():.0f}-{p.CLT.max():.0f} (median {p.CLT.median():.0f})  "
      f"logs={p.log.nunique()}")
print(f"oil pressure spanned: {p['Engine oil pressure'].min():.2f}-"
      f"{p['Engine oil pressure'].max():.2f} bar\n")

cell = (p.groupby(["rpm_bin", "op_bin"])
          .agg(air=("Idle air %", "median"),
               q25=("Idle air %", lambda s: s.quantile(.25)),
               q75=("Idle air %", lambda s: s.quantile(.75)),
               nofan=("air_nofan", "median"),
               implied=("implied", "median"),
               shipped=("shipped", "median"),
               op=("Engine oil pressure", "median"),
               op_lo=("Engine oil pressure", "min"),
               op_hi=("Engine oil pressure", "max"),
               pid=("Idle PID air % correction", "median"),
               rail=("railed", "mean"), fan=("fan_used", "mean"),
               n=("Idle air %", "size"), n_ep=("episode", "nunique"),
               logs=("log", "nunique")))
cell.round(2).to_csv(os.path.join(HERE, "clt96_cells.csv"))


def grid(field, fmt, title, note="", mark_rail=True, minn=1):
    out = [f"\n### {title}", note] if note else [f"\n### {title}"]
    out.append("\n| RPM ＼ oil bar | " + " | ".join(f"**{b:.0f}**" for b in OP_BINS) + " |")
    out.append("|" + "---|" * (len(OP_BINS) + 1))
    for r in RPM_BINS:
        row = [f"| **{r:.0f}** "]
        for b in OP_BINS:
            k = (r, b)
            if k in cell.index and cell.loc[k, "n"] >= minn and pd.notna(cell.loc[k, field]):
                v = fmt(cell.loc[k, field])
                if mark_rail and cell.loc[k, "rail"] > 0.2:
                    v += "†"
                if cell.loc[k, "n"] < 25:
                    v += "⚠"
                row.append(f"| {v} ")
            else:
                row.append("| — ")
        out.append("".join(row) + "|")
    return "\n".join(out)


md = [f"# CLT 96 °C — airflow vs RPM vs oil pressure",
      f"\nAll five oil-pressure tables collapsed to the CLT 96 column "
      f"(nearest-bin span **85.5–100.5 °C**; actual CLT {p.CLT.min():.0f}–{p.CLT.max():.0f}, "
      f"median {p.CLT.median():.0f}). n = {len(p)} samples, {p.log.nunique()} logs, "
      f"envelope |RPM − Idle target| ≤ 50.",
      "\n**†** = airflow PID on its −10 rail > 20 % of the cell (upper bound). "
      "**⚠** = n < 25 (under 1 s).",
      grid("air", lambda v: f"{v:.1f}", "Total commanded `Idle air %` — the requirement"),
      grid("n", lambda v: f"{int(v)}", "Sample count", mark_rail=False),
      grid("nofan", lambda v: f"{v:.1f}",
           "Fan's +13 removed — engine-only airflow",
           "\n(fan is on in 100 % of every cell except 6 bar / 1200 rpm, which is 71 % on — "
           "so that one cell is a mixed median, not total − 13)"),
      grid("op", lambda v: f"{v:.2f}", "Median actual oil pressure in each cell (bar)",
           mark_rail=False),
      grid("pid", lambda v: f"{v:+.1f}", "Median idle-air PID output", mark_rail=False),
      grid("implied", lambda v: f"{v:.1f}",
           "Implied `idleActiveAirflow` cell (air − 13·fan − custom − PID)"),
      ]
open(os.path.join(HERE, "clt96_tables.md"), "w", encoding="utf-8").write("\n".join(md))
print("\n".join(md[3:]))

print("\n\n### Per-cell detail")
print(cell.round(2).to_string())
