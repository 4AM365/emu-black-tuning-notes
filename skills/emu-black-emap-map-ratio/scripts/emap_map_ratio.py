"""EMAP/MAP ratio table from EMU Black CSV logs, binned into the VE-table grid.

Pipeline per log:
  1. Load TIME, RPM, MAP, Back pressure, Baro (+ status channels).
  2. Liveness gate — an EMAP channel that never moves is a dead sensor, not data.
  3. Gauge/absolute autodetect from engine-off or idle rows.
  4. Despike (rolling median) + zero-phase Savitzky-Golay low-pass, window sized
     from the measured high-frequency noise. EMAP pulsates at firing frequency
     (3x RPM/60 on an I6 = 50-350 Hz), far above the 12.5 Hz log Nyquist, so the
     pulsation aliases to broadband noise; the only recoverable quantity is the
     cycle-mean, which is exactly what the ratio needs.
  5. r = EMAP_abs / MAP_abs per sample (MAP is absolute in EMU logs).
  6. Nearest-bin into the tune's veTable axes (mapBins x rpmBins); per-cell
     median, IQR, n.

Outputs: <out>_points.csv (all samples), <out>_table.md + <out>_table.csv
(ratio grid, RPM increasing upward, MAP left->right), noise report to stdout.

Usage:
  python emap_map_ratio.py --tune tune.xml.emub3 --out exports/emap_ratio log1.csv log2.csv ...
  python emap_map_ratio.py --self-test ...   # uses MAP as EMAP; every cell must read 1.000
"""
import argparse, re, sys
import numpy as np
import pandas as pd

RUNNING_RPM = 400          # gate: engine actually turning
LIVE_RANGE_KPA = 8.0       # liveness: channel must span at least this (post unit conversion)
LIVE_LEVELS = 4            # ...across at least this many distinct quantization levels
MIN_CELL_N = 20            # cells with fewer samples are left blank
DEFAULT_BARO = 100.0       # kPa, used when the log has no Baro channel


def read_bins(tune_path):
    txt = open(tune_path, encoding="utf-8", errors="replace").read()
    def grab(name):
        m = re.search(rf'name="{name}" storage="word" width="\d+" height="1" data="([0-9A-Fa-f\- ]+)"', txt)
        if not m:
            sys.exit(f"axis symbol {name} not found in {tune_path}")
        return [int(h, 16) for h in m.group(1).split()]
    return grab("mapBins"), grab("rpmBins")  # both scale 1 (kPa, RPM)


def load_log(path):
    hdr = pd.read_csv(path, sep=";", nrows=0).columns
    strip = hdr.str.strip()
    need = ["TIME", "RPM", "MAP", "Back pressure"]
    missing = [c for c in need if c not in strip.tolist()]
    if missing:
        return None, f"missing channels: {missing}"
    want = need + (["Baro"] if "Baro" in strip.tolist() else [])
    use = [hdr[strip.tolist().index(c)] for c in want]
    df = pd.read_csv(path, sep=";", usecols=use)
    df.columns = df.columns.str.strip()
    if "Baro" not in df:
        df["Baro"] = DEFAULT_BARO
    return df.dropna(), None


def hf_noise_sigma(x):
    """Robust high-frequency noise sigma via MAD of successive differences."""
    d = np.diff(x)
    mad = np.median(np.abs(d - np.median(d)))
    return 1.4826 * mad / np.sqrt(2)


def savgol(x, window, poly=2):
    """Zero-phase Savitzky-Golay; scipy if present, else moving-average fallback."""
    try:
        from scipy.signal import savgol_filter
        return savgol_filter(x, window, poly)
    except ImportError:
        return pd.Series(x).rolling(window, center=True, min_periods=1).mean().to_numpy()


def smooth_channel(x, sigma_hf, target_sigma=0.5):
    """Despike then low-pass. Window grows with measured noise so the smoothed
    channel approaches target_sigma kPa; clamped to 0.28-1.24 s at 25 Hz."""
    x = pd.Series(x).rolling(5, center=True, min_periods=1).median().to_numpy()
    n = int(np.ceil((max(sigma_hf, 1e-6) / target_sigma) ** 2))
    n = min(max(n, 7), 31)
    if n % 2 == 0:
        n += 1
    return savgol(x, n), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+")
    ap.add_argument("--tune", required=True)
    ap.add_argument("--out", default="emap_ratio")
    ap.add_argument("--self-test", action="store_true",
                    help="use MAP as EMAP; every populated cell must read 1.000")
    a = ap.parse_args()

    map_bins, rpm_bins = read_bins(a.tune)
    frames = []
    for path in a.logs:
        df, err = load_log(path)
        tag = path.split("\\")[-1].split("/")[-1]
        if err:
            print(f"SKIP {tag}: {err}")
            continue
        if a.self_test:
            emap_abs_raw = df["MAP"].to_numpy(float)
        else:
            bp = df["Back pressure"].astype(float)
            # unit autodetect: EMU logs this channel in BAR (1/32-bar quantization,
            # ~3.1 kPa/count — verified on this build 2026-07-10). A live kPa channel
            # would exceed 6 somewhere in any running log; a bar channel can't.
            unit = "bar" if bp.max() <= 6 else "kPa"
            bp_kpa = bp * 100.0 if unit == "bar" else bp
            rng = bp_kpa.max() - bp_kpa.min()
            levels = bp.nunique()
            if rng < LIVE_RANGE_KPA or levels < LIVE_LEVELS:
                print(f"DEAD {tag}: Back pressure immobile (range {rng:.1f} kPa as {unit}, "
                      f"{levels} levels) over {len(df)} rows, MAP max {df['MAP'].max():.0f} — excluded.")
                continue
            # sanity: where the log spans boost, EMAP must track MAP
            corr = bp_kpa.corr(df["MAP"]) if df["MAP"].max() - df["MAP"].min() > 60 else np.nan
            if np.isfinite(corr) and corr < 0.3:
                print(f"WARN {tag}: corr(EMAP, MAP) = {corr:.2f} — channel moves but does not "
                      f"track load; check sensor/units. Excluded.")
                continue
            off = df[df["RPM"] < 100]
            ref = off["Back pressure"].median() * (100 if unit == "bar" else 1) if len(off) > 10 else \
                bp_kpa[df["RPM"].between(600, 1100)].median()
            gauge = (ref if np.isfinite(ref) else 0) < 50  # off/idle EMAP: ~0 gauge, ~baro absolute
            emap_abs_raw = bp_kpa.to_numpy() + (df["Baro"].to_numpy(float) if gauge else 0.0)
            print(f"{tag}: units={unit}, {'gauge' if gauge else 'absolute'} (ref {ref:.1f} kPa), "
                  f"corr(EMAP,MAP)={corr:.2f}" if np.isfinite(corr) else
                  f"{tag}: units={unit}, {'gauge' if gauge else 'absolute'} (ref {ref:.1f} kPa)")
        s_e = hf_noise_sigma(emap_abs_raw)
        s_m = hf_noise_sigma(df["MAP"].to_numpy(float))
        emap_s, n_e = smooth_channel(emap_abs_raw, s_e)
        map_s, n_m = smooth_channel(df["MAP"].to_numpy(float), s_m)
        print(f"{tag}: hf-noise EMAP {s_e:.2f} kPa (SG window {n_e}), MAP {s_m:.2f} kPa (window {n_m})")
        d = pd.DataFrame({"TIME": df["TIME"], "RPM": df["RPM"], "MAP": df["MAP"],
                          "EMAP_abs": emap_s, "MAP_s": map_s, "log": tag})
        d = d[d["RPM"] > RUNNING_RPM]
        d["ratio"] = d["EMAP_abs"] / d["MAP_s"]
        frames.append(d)

    if not frames:
        print("\nNo logs with live EMAP data — no table produced.")
        sys.exit(1)

    pts = pd.concat(frames, ignore_index=True)
    pts["i_rpm"] = np.abs(np.subtract.outer(pts["RPM"].to_numpy(), np.array(rpm_bins))).argmin(1)
    pts["i_map"] = np.abs(np.subtract.outer(pts["MAP"].to_numpy(), np.array(map_bins))).argmin(1)
    pts.to_csv(f"{a.out}_points.csv", index=False)
    print(f"\n{len(pts)} samples -> {a.out}_points.csv")

    med = np.full((len(rpm_bins), len(map_bins)), np.nan)
    cnt = np.zeros_like(med, dtype=int)
    for (ir, im), g in pts.groupby(["i_rpm", "i_map"]):
        cnt[ir, im] = len(g)
        if len(g) >= MIN_CELL_N:
            med[ir, im] = g["ratio"].median()

    # grid CSV + markdown, RPM increasing upward (top row = highest bin)
    rows_md = ["| RPM \\ MAP | " + " | ".join(str(m) for m in map_bins) + " |",
               "|---" * (len(map_bins) + 1) + "|"]
    for ir in range(len(rpm_bins) - 1, -1, -1):
        cells = ["" if np.isnan(med[ir, im]) else f"{med[ir, im]:.2f}" for im in range(len(map_bins))]
        rows_md.append(f"| **{rpm_bins[ir]}** | " + " | ".join(cells) + " |")
    open(f"{a.out}_table.md", "w").write("\n".join(rows_md) + "\n")
    pd.DataFrame(med[::-1], index=rpm_bins[::-1], columns=map_bins).to_csv(f"{a.out}_table.csv")
    print(f"ratio table -> {a.out}_table.md / .csv   (cells with n<{MIN_CELL_N} blank)")
    print(f"populated cells: {np.isfinite(med).sum()} / {med.size}")


if __name__ == "__main__":
    main()
