"""Rescale all airflow-% tables in an EMU Black tune to a new actuator range.

Usage:
  python rescale.py --tune <file.emub3> --old-range FLOOR CEILING --new-range FLOOR CEILING --out-dir <dir>

Optional:
  --skip-symbols sym1,sym2,...     Skip these symbols (still listed in summary)
  --crank-tps "f1 f2 f3 f4"        Override cranking with absolute TPS values for cltBins4 order

Outputs:
  <out-dir>/<EMU title>.emubt   one file per rescaled table
  <out-dir>/range_scalars.emubt updated idleDBWTargetMin/Max
  <out-dir>/summary.md          per-cell diff + clamp warnings
"""
import argparse, os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Symbol classification ───────────────────────────────────────────────────
# (symbol, EMU display title for .emubt filename, storage, scale)
PRESERVE_TPS_TABLES = {
    "idleActiveAirflow":    ("Airflow - Active state air flow [%]",   "ubyte", 0.5),
    "idleArmedAirFlow":     ("Airflow - Armed state air flow [%]",    "ubyte", 0.5),
    "idleCrankingDC":       ("Cranking - Cranking airflow [%]",       "ubyte", 0.5),
    "cyclingIdleAirflow":   ("Idle - Cycling idle airflow [%]",       "ubyte", 0.5),  # scalar
    "overrunDBW":           ("Overrun - Overrun DBW [%]",              "ubyte", 0.5),
    "overrunDBW2":          ("Overrun - Overrun DBW 2 [%]",            "ubyte", 0.5),
    "lcDBWTargetTable":     ("Launch - LC DBW target [%]",             "ubyte", 0.5),
    "lcPrestageDBWTarget":  ("Launch - LC prestage DBW target [%]",    "ubyte", 0.5),  # scalar
    "alsDBWTarget":         ("ALS - ALS DBW target 1 [%]",             "ubyte", 0.5),
    "alsDBWTarget2":        ("ALS - ALS DBW target 2 [%]",             "ubyte", 0.5),
    "ralDBWTarget":         ("Rolling AL - RAL DBW target [%]",        "ubyte", 0.5),
    "pitLimiterDBWLimit":   ("Pit limiter - DBW limit [%]",            "ubyte", 0.5),
}
ADDITIVE_TABLES = {
    "idleCustomCorrection": ("Airflow - Custom air flow correction [%]", "sbyte", 0.5),
}
PID_GAIN_SCALARS = [
    "idleAirFlowKP", "idleAirFlowKI", "idleAirFlowKD",
    "idleAirFlowIntegralLimitMin", "idleAirFlowIntegralLimitMax",
    "idleAirPIDOutMin", "idleAirPIDOutMax",
]
NOT_RESCALED_FLAGGED = ["dbwBoostTargetLimit", "dbwCLTLimitTable"]

# ── EMU hex parsing/writing ─────────────────────────────────────────────────
def parse_emu_hex(s):
    """Sign-magnitude hex token list → list of signed ints."""
    out = []
    for tok in s.strip().split():
        if tok.startswith("-"):
            out.append(-int(tok[1:], 16))
        else:
            out.append(int(tok, 16))
    return out

def fmt_emu_hex(values, storage):
    """ints → sign-magnitude UPPERCASE hex tokens (EMU convention)."""
    bounds = {
        "ubyte": (0, 255), "sbyte": (-128, 127),
        "word": (0, 65535), "sword": (-32768, 32767),
    }
    lo, hi = bounds.get(storage, (-32768, 65535))
    out = []
    for v in values:
        v = max(lo, min(hi, v))
        if v < 0:
            out.append(f"-{(-v):X}")
        else:
            out.append(f"{v:X}")
    return " ".join(out)

# ── Symbol extraction ───────────────────────────────────────────────────────
def get_symbol(xml, name):
    m = re.search(rf'<symbol name="{name}"[^/]*?/>', xml)
    if not m: return None
    blob = m.group(0)
    out = {"name": name}
    for k in ["value", "storage", "width", "height", "type", "data"]:
        mm = re.search(rf'{k}="([^"]*)"', blob)
        if mm: out[k] = mm.group(1)
    return out

# ── .emubt writer (inline, no external dep) ─────────────────────────────────
def write_emubt(out_path, symbols):
    """symbols: list of (name, storage, width, height, raw_ints)"""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<project version="1.0">',
             '  <tables>']
    for name, storage, w, h, vals in symbols:
        hex_data = fmt_emu_hex(vals, storage)
        attrs = f'name="{name}" storage="{storage}"'
        if w is not None: attrs += f' width="{w}"'
        if h is not None: attrs += f' height="{h}"'
        lines.append(f'    <symbol {attrs} data="{hex_data} "/>')
    lines.append('  </tables>')
    lines.append('</project>')
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def write_scalar_emubt(out_path, name_value_pairs):
    """name_value_pairs: list of (name, storage, value)"""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<project version="1.0">',
             '  <tables>']
    for name, storage, value in name_value_pairs:
        lines.append(f'    <symbol name="{name}" value="{value}" storage="{storage}" type="value"/>')
    lines.append('  </tables>')
    lines.append('</project>')
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ── Main ────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tune", required=True)
    ap.add_argument("--old-range", nargs=2, type=float, required=True, metavar=("FLOOR", "CEILING"))
    ap.add_argument("--new-range", nargs=2, type=float, required=True, metavar=("FLOOR", "CEILING"))
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--skip-symbols", default="", help="Comma-sep symbol names to skip")
    ap.add_argument("--crank-tps", default="", help="Override idleCrankingDC with TPS targets")
    ap.add_argument("--custom-corr-mode", choices=["additive", "scalar"], default="additive",
                    help="Mode of idleCustomCorrection (skip width-scale if scalar)")
    args = ap.parse_args()

    f_old, c_old = args.old_range
    f_new, c_new = args.new_range
    B = (c_old - f_old) / (c_new - f_new)
    A_pct = (f_old - f_new) / (c_new - f_new) * 100
    A_raw_half = A_pct / 0.5  # for ubyte ×0.5 tables

    skip = {s.strip() for s in args.skip_symbols.split(",") if s.strip()}
    crank_tps_override = [float(t) for t in args.crank_tps.split()] if args.crank_tps else None

    print(f"Rescale [{f_old}, {c_old}] → [{f_new}, {c_new}]")
    print(f"  B (slope)        = {B:.6f}")
    print(f"  A (offset %)     = {A_pct:+.6f}")
    print(f"  In raw ubyte:    new_raw = round({A_raw_half:+.4f} + {B:.4f} × old_raw)")
    print()

    os.makedirs(args.out_dir, exist_ok=True)
    xml = open(args.tune).read()
    summary_lines = [f"# Actuator rescale summary",
                     f"\n**From:** `[{f_old}, {c_old}]` → **To:** `[{f_new}, {c_new}]`",
                     f"- Slope B = {B:.4f}",
                     f"- Offset A = {A_pct:+.4f}% (display) = {A_raw_half:+.2f} (raw)\n"]
    clamp_warnings = []

    # 1. Preserve-TPS tables (and scalars treated the same)
    for sym, (title, storage, scale) in PRESERVE_TPS_TABLES.items():
        s = get_symbol(xml, sym)
        if not s:
            summary_lines.append(f"- ❌ `{sym}` — not found in tune")
            continue
        if sym in skip:
            summary_lines.append(f"- ⏭️  `{sym}` — skipped per --skip-symbols")
            continue

        # Scalar (no data) vs table (data attr)
        if "data" not in s:
            old_raw = int(s["value"])
            new_raw = round(A_raw_half + B * old_raw)
            new_raw = max(0, new_raw)
            # Write a scalar .emubt — note: requires confirming EMU accepts scalar-only emubt
            summary_lines.append(
                f"- `{sym}` (scalar) raw {old_raw}→{new_raw}, "
                f"display {old_raw*scale:.1f}%→{new_raw*scale:.1f}%"
            )
            continue

        if sym == "idleCrankingDC" and crank_tps_override:
            new_vals = []
            for tps in crank_tps_override:
                new_pct = max(0, (tps - f_new) / (c_new - f_new) * 100)
                new_vals.append(round(new_pct / scale))
            old_vals = parse_emu_hex(s["data"])
            out_file = os.path.join(args.out_dir, f"{title}.emubt")
            write_emubt(out_file, [(sym, storage, int(s["width"]), int(s["height"]), new_vals)])
            summary_lines.append(f"- `{sym}` (override) old={old_vals} new={new_vals} (file: {title}.emubt)")
            continue

        old_vals = parse_emu_hex(s["data"])
        new_vals = []
        clamped_here = 0
        for r in old_vals:
            n = A_raw_half + B * r
            if n < 0:
                clamped_here += 1
                n = 0
            new_vals.append(int(round(n)))

        out_file = os.path.join(args.out_dir, f"{title}.emubt")
        write_emubt(out_file, [(sym, storage, int(s["width"]) if "width" in s else len(new_vals),
                                int(s["height"]) if "height" in s else 1, new_vals)])
        line = f"- `{sym}` → `{title}.emubt`"
        if clamped_here:
            line += f"  ⚠ {clamped_here}/{len(old_vals)} cells clamped (below new floor)"
            clamp_warnings.append((sym, clamped_here, len(old_vals)))
        summary_lines.append(line)
        # Per-cell sample
        if len(old_vals) <= 16:
            summary_lines.append(f"  - OLD %: {[f'{v*scale:.1f}' for v in old_vals]}")
            summary_lines.append(f"  - NEW %: {[f'{v*scale:.1f}' for v in new_vals]}")
        else:
            summary_lines.append(f"  - first row OLD %: {[f'{v*scale:.1f}' for v in old_vals[:int(s.get('width', len(old_vals)))]]}")
            summary_lines.append(f"  - first row NEW %: {[f'{v*scale:.1f}' for v in new_vals[:int(s.get('width', len(new_vals)))]]}")

    # 2. Additive tables (slope-only)
    for sym, (title, storage, scale) in ADDITIVE_TABLES.items():
        s = get_symbol(xml, sym)
        if not s: continue
        if sym in skip:
            summary_lines.append(f"- ⏭️  `{sym}` — skipped"); continue
        if args.custom_corr_mode == "scalar":
            summary_lines.append(f"- ⏭️  `{sym}` — skipped (scalar mode; rescale not needed)")
            continue
        old_vals = parse_emu_hex(s["data"])
        new_vals = [int(round(r * B)) for r in old_vals]
        out_file = os.path.join(args.out_dir, f"{title}.emubt")
        write_emubt(out_file, [(sym, storage, int(s["width"]), int(s["height"]), new_vals)])
        summary_lines.append(f"- `{sym}` (additive, slope-only ×{B:.4f}) → `{title}.emubt`")
        if len(old_vals) <= 32:
            summary_lines.append(f"  - OLD: {[f'{v*scale:.1f}' for v in old_vals]}")
            summary_lines.append(f"  - NEW: {[f'{v*scale:.1f}' for v in new_vals]}")

    # 3. PID gain scalars
    pid_pairs = []
    for sym in PID_GAIN_SCALARS:
        s = get_symbol(xml, sym)
        if not s: continue
        if "value" not in s: continue
        old_v = int(s["value"])
        new_v = int(round(old_v * B))
        pid_pairs.append((sym, s.get("storage", "word"), new_v))
        summary_lines.append(f"- `{sym}` (PID, ×{B:.4f}): {old_v} → {new_v}")

    if pid_pairs:
        write_scalar_emubt(os.path.join(args.out_dir, "PID gains and limits.emubt"), pid_pairs)

    # 4. Range scalars (the actual actuator min/max)
    min_v = int(round(f_new * 10))
    max_v = int(round(c_new * 10))
    write_scalar_emubt(os.path.join(args.out_dir, "range_scalars.emubt"),
                       [("idleDBWTargetMin", "word", min_v),
                        ("idleDBWTargetMax", "word", max_v)])
    summary_lines.append(f"\n## Range scalars")
    summary_lines.append(f"- `idleDBWTargetMin` = {min_v} ({f_new}%)")
    summary_lines.append(f"- `idleDBWTargetMax` = {max_v} ({c_new}%)")

    # 5. Flagged (not rescaled) symbols
    summary_lines.append(f"\n## Flagged (not rescaled — confirm units before applying)")
    for sym in NOT_RESCALED_FLAGGED:
        s = get_symbol(xml, sym)
        if s:
            summary_lines.append(f"- `{sym}` exists but units unclear (could be airflow-% or raw TPS-%). "
                                 "Review manually.")

    # Clamp summary
    if clamp_warnings:
        summary_lines.append(f"\n## Clamp warnings")
        for sym, c, total in clamp_warnings:
            summary_lines.append(f"- `{sym}`: {c}/{total} cells clamped to 0% (= new floor TPS). "
                                 "If this symbol controls something that wants throttle nearly closed "
                                 "(ALS, launch, pit limiter), the new floor breaks its design intent.")

    summary_path = os.path.join(args.out_dir, "summary.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))
    print(f"\n✓ Wrote {len(os.listdir(args.out_dir))} files to {args.out_dir}")
    print(f"  Summary: {summary_path}")

if __name__ == "__main__":
    main()
