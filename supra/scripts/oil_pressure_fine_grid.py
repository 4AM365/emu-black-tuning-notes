"""Fine-resolution oil-pressure x RPM airflow grid, one fixed CLT bin.

Reads the points CSV produced by oil_pressure_airflow_tables.py and re-bins
pressure at a much finer resolution than the 2/2.5/3/4/5/6 table (default
0.125 bar) while keeping the RPM axis at the same 5 idle-target bins. RPM on
Y (high at top), pressure on X, cell = median Idle air %, color = value,
alpha-scaled by sample count so thin cells read as faint. Written to
investigate whether an apparent step in the coarse tables is a real cliff or
a coarse-binning artifact.

Usage:
  python oil_pressure_fine_grid.py --points oil_press_points.csv --clt 96 --res 0.125 --out oil_press_fine_96clt
"""
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RPM_BINS = [1000, 1100, 1200, 1375, 1500]
CLT_BINS = [0, 15, 30, 45, 60, 75, 96, 105]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--points", required=True)
    ap.add_argument("--clt", type=float, required=True, help="which CLT bin (must match a value in CLT_BINS)")
    ap.add_argument("--res", type=float, default=0.125, help="pressure bin width, bar")
    ap.add_argument("--min-n", type=int, default=5)
    ap.add_argument("--stat", choices=["median", "mean"], default="median")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    pts = pd.read_csv(a.points)
    i_clt = CLT_BINS.index(a.clt)
    sub = pts[pts["i_clt"] == i_clt].copy()
    sub["p_bin"] = (sub["Engine oil pressure"] // a.res) * a.res + a.res / 2

    grid = sub.groupby(["i_rpm", "p_bin"]).agg(med=("Idle air %", a.stat), n=("Idle air %", "count")).reset_index()
    grid = grid[grid["n"] >= a.min_n]
    grid.to_csv(f"{a.out}.csv", index=False)

    rows_md = ["| RPM \\ oil bar | " + " | ".join(f"{p:.3f}" for p in np.sort(grid["p_bin"].unique())) + " |"]
    rows_md.append("|---" * (grid["p_bin"].nunique() + 1) + "|")
    p_sorted = np.sort(grid["p_bin"].unique())
    for ir in range(len(RPM_BINS) - 1, -1, -1):
        row = grid[grid["i_rpm"] == ir].set_index("p_bin")
        cells = [f"{row.loc[p, 'med']:.1f} ({int(row.loc[p, 'n'])})" if p in row.index else "" for p in p_sorted]
        rows_md.append(f"| **{RPM_BINS[ir]}** | " + " | ".join(cells) + " |")
    open(f"{a.out}_table.md", "w").write("\n".join(rows_md) + "\n")

    p_vals = np.sort(grid["p_bin"].unique())
    med = np.full((len(RPM_BINS), len(p_vals)), np.nan)
    cnt = np.zeros_like(med)
    for _, row in grid.iterrows():
        ir = int(row["i_rpm"])
        ip = np.searchsorted(p_vals, row["p_bin"])
        med[ir, ip] = row["med"]
        cnt[ir, ip] = row["n"]

    fig, ax = plt.subplots(figsize=(max(8, len(p_vals) * 0.35), 4))
    vmin, vmax = np.nanmin(med), np.nanmax(med)
    masked = np.ma.masked_invalid(med)
    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad("white")
    im = ax.imshow(masked, aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax,
                    extent=[p_vals[0] - a.res / 2, p_vals[-1] + a.res / 2, -0.5, len(RPM_BINS) - 0.5],
                    origin="lower")
    ax.set_yticks(range(len(RPM_BINS)))
    ax.set_yticklabels(RPM_BINS)
    ax.set_xlabel(f"Engine oil pressure (bar), {a.res} bar bins")
    ax.set_ylabel("RPM (actual)")
    ax.set_title(f"Median Idle air % vs oil pressure x RPM, CLT={a.clt} (cells with n<{a.min_n} left blank)")
    fig.colorbar(im, ax=ax, label="Idle air %")
    fig.tight_layout()
    fig.savefig(f"{a.out}.png", dpi=150)
    print(f"-> {a.out}.png / {a.out}.csv, {len(p_vals)} pressure columns, {grid.shape[0]} populated cells")


if __name__ == "__main__":
    main()
