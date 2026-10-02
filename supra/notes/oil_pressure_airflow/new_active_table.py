"""Candidate `idleActiveAirflow` built from what was ACTUALLY DELIVERED.

    delivered = base + 13*fan + custom + PID          (identity, verified to 0.0000)

The engine held its target on `delivered`, so `delivered` is the requirement. The ECU will
still add the fan term itself, so the table cell is

    base_new = delivered - 13*fan

...which also assumes the custom correction is ZERO in the new regime (the old IAT-indexed
`idleCustomCorrection` is being replaced) and that the PID is left to centre on ~0 rather than
carrying a standing trim.

Axes are the real table's: X = CLT, Y = idle TARGET (not actual rpm).
Envelope: |RPM - Idle target| <= 50.
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CLT_BINS = [0, 15, 30, 45, 60, 75, 96, 105]
TGT_BINS = [1500, 1375, 1200, 1100, 1000]          # high at top
FAN = 13.0

p = pd.read_csv(os.path.join(HERE, "pooled_samples.csv"))
p["need"] = p["Idle air %"] - FAN * p["fan_used"]   # NaN where fan state unknown
p = p.dropna(subset=["need"]).copy()
p["tgt_bin"] = p["tgt_bin"].astype(float)

q25 = lambda s: s.quantile(.25)
q75 = lambda s: s.quantile(.75)
cell = p.groupby(["tgt_bin", "clt_bin"]).agg(
    need=("need", "median"), lo=("need", q25), hi=("need", q75),
    delivered=("Idle air %", "median"), fan=("fan_used", "mean"),
    custom=("Idle airflow custom corr.", "median"),
    pid=("Idle PID air % correction", "median"),
    op=("Engine oil pressure", "median"),
    op_lo=("Engine oil pressure", "min"), op_hi=("Engine oil pressure", "max"),
    n=("need", "size"), n_ep=("episode", "nunique"), logs=("log", "nunique"),
    rail=("railed", "mean"))
cell.round(2).to_csv(os.path.join(HERE, "new_active_table_cells.csv"))


def grid(field, fmt, title, note="", flags=True):
    out = [f"\n### {title}"]
    if note:
        out.append(note)
    out.append("\n| tgt ＼ CLT | " + " | ".join(str(c) for c in CLT_BINS) + " |")
    out.append("|" + "---|" * (len(CLT_BINS) + 1))
    for t in TGT_BINS:
        row = [f"| **{t}** "]
        for c in CLT_BINS:
            k = (float(t), float(c))
            if k in cell.index and pd.notna(cell.loc[k, field]):
                v = fmt(cell.loc[k, field])
                if flags:
                    if cell.loc[k, "rail"] > 0.2:
                        v += "†"
                    if cell.loc[k, "n"] < 25:
                        v += "⚠"
                row.append(f"| {v} ")
            else:
                row.append("| — ")
        out.append("".join(row) + "|")
    return "\n".join(out)


md = ["# Candidate `idleActiveAirflow` from delivered airflow",
      "\n`base_new = delivered − 13·fan`, median per cell. Axes = CLT (X) × idle target (Y), "
      "the table's own indexing. Envelope |RPM − target| ≤ 50.",
      "\n**†** = PID on its −10 rail > 20 % of the cell → delivered was more than the engine "
      "needed, so the cell is an **upper bound**. **⚠** = n < 25.",
      grid("need", lambda v: f"{v:.1f}", "Table candidate — airflow % (fan removed)"),
      grid("n", lambda v: f"{int(v)}", "n", flags=False),
      grid("delivered", lambda v: f"{v:.1f}", "Delivered `Idle air %` it came from"),
      grid("fan", lambda v: f"{v:.2f}", "Fan-on fraction (the 13 is scaled by this)", flags=False),
      grid("op", lambda v: f"{v:.2f}", "Median oil pressure in the cell (bar)", flags=False),
      grid("custom", lambda v: f"{v:+.1f}", "Old IAT custom correction still live in the data",
           "\nThese are NOT subtracted — the new table assumes custom goes to zero. Where this "
           "is non-zero the engine was getting that much less (or more) than the table alone "
           "would give, and the candidate value already reflects the total that worked.",
           flags=False),
      grid("pid", lambda v: f"{v:+.1f}", "PID output in the cell", flags=False),
      ]
spread = grid("hi", lambda v: f"{v:.1f}", "q75 of the candidate (spread from mixed oil states)")
md.append(spread)
open(os.path.join(HERE, "new_active_table.md"), "w", encoding="utf-8").write("\n".join(md))
print("\n".join(md[3:]))

print("\n\n### cells where one CLT/target cell spans a wide oil-pressure range")
w = cell[(cell.n >= 25) & (cell.op_hi - cell.op_lo > 1.5)]
print(w[["n", "need", "lo", "hi", "op", "op_lo", "op_hi", "logs", "rail"]].round(2).to_string())
