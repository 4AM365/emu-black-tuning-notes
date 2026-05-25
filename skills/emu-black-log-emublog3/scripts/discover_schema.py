"""Reverse-engineer the .emublog3 binary schema from a paired CSV export.

Usage:
  python discover_schema.py --emublog3 <file.emublog3> --csv <file.csv> --out-schema <file.json>

Approach:
  1. Decompress the .emublog3.
  2. Read the CSV (same recording session) to know channel names and reference values.
  3. Determine record size by searching for a per-value width that yields a sample count
     close to the CSV row count.
  4. For each CSV channel, search the binary for byte offsets whose decoded value sequence
     correlates highly with the CSV column.
  5. Emit a schema JSON: {records, rec_size, channels: [{name, offset, dtype, scale}, ...]}

This is heuristic — for a brand-new ECU log configuration, expect to inspect intermediate
results and adjust. Once a schema works for one log from a given config, it works for all logs
from that config until the EMU logger setup changes.
"""
import argparse, gzip, json, struct, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("Requires pandas+numpy. Install: pip install pandas numpy"); sys.exit(1)

DTYPES = {
    "u8":  ("B", 1),
    "i8":  ("b", 1),
    "u16": ("<H", 2),
    "i16": ("<h", 2),
    "u32": ("<I", 4),
    "i32": ("<i", 4),
    "f32": ("<f", 4),
}

def decompress(path):
    import zlib
    with open(path, "rb") as f:
        raw = f.read()
    d = zlib.decompressobj(16 + zlib.MAX_WBITS)
    out = bytearray(d.decompress(raw))
    while not d.eof and d.unconsumed_tail:
        try:
            out.extend(d.decompress(d.unconsumed_tail))
        except Exception:
            break
    return bytes(out)

def decode_column(buf, offset, dtype, n_records, rec_size):
    fmt, size = DTYPES[dtype]
    return np.array([struct.unpack_from(fmt, buf, offset + i * rec_size)[0]
                     for i in range(n_records)])

def find_rec_size(buf_len, n_records):
    """Find candidate record sizes that fit n_records into buf_len."""
    candidates = []
    for rec in range(60, 6000):
        if abs(buf_len // rec - n_records) <= 1:
            candidates.append(rec)
    return candidates

def correlate(csv_vals, binary_vals):
    """Return (correlation, scale) best-fitting binary to CSV.
    Tries simple linear scaling.
    """
    if len(csv_vals) != len(binary_vals): return 0.0, 1.0
    if np.std(csv_vals) < 1e-9 or np.std(binary_vals) < 1e-9:
        # Constant column — only matches if all equal after scaling
        if np.all(csv_vals == csv_vals[0]) and np.all(binary_vals == binary_vals[0]):
            scale = csv_vals[0] / binary_vals[0] if binary_vals[0] != 0 else 1.0
            return 1.0, scale
        return 0.0, 1.0
    c = float(np.corrcoef(csv_vals, binary_vals)[0, 1])
    # Linear regression for scale
    slope = np.cov(csv_vals, binary_vals)[0,1] / np.var(binary_vals)
    return c, slope

def search_channel(buf, csv_vals, n_records, rec_size, dtype_hints=None):
    """Find best (offset, dtype) for csv_vals in buf."""
    best = (-1.0, None, None, 1.0)  # (corr, offset, dtype, scale)
    dtypes = dtype_hints or list(DTYPES.keys())
    for dtype in dtypes:
        size = DTYPES[dtype][1]
        for offset in range(0, rec_size - size + 1):
            try:
                vals = decode_column(buf, offset, dtype, n_records, rec_size)
                c, scale = correlate(csv_vals, vals)
                if c > best[0]:
                    best = (c, offset, dtype, scale)
            except Exception:
                continue
    return best

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emublog3", required=True)
    ap.add_argument("--csv",     required=True)
    ap.add_argument("--out-schema", required=True)
    ap.add_argument("--min-corr", type=float, default=0.95,
                    help="Minimum correlation to accept a match (default 0.95)")
    ap.add_argument("--n-samples", type=int, default=300,
                    help="Number of records to use for correlation search (faster on shorter window)")
    args = ap.parse_args()

    buf = decompress(args.emublog3)
    print(f"Decompressed: {len(buf):,} bytes")

    df = pd.read_csv(args.csv, sep=";", low_memory=False)
    df.columns = df.columns.str.strip()
    n_csv = len(df)
    print(f"CSV: {n_csv:,} rows, {len(df.columns)} channels")

    candidates = find_rec_size(len(buf), n_csv)
    if not candidates:
        print(f"⚠ No record size found that fits {n_csv} records into {len(buf)} bytes.")
        return
    print(f"Candidate record sizes: {candidates[:10]}{' ...' if len(candidates)>10 else ''}")

    # Use TIME channel (or first column) as a high-confidence anchor to pick rec_size
    anchor_col = "TIME" if "TIME" in df.columns else df.columns[0]
    csv_anchor = df[anchor_col].values[:args.n_samples]
    print(f"\nAnchor channel: {anchor_col}")

    best_rec_size = None
    best_anchor = (-1.0, None, None, 1.0)
    for rec_size in candidates:
        n_rec = min(args.n_samples, len(buf) // rec_size)
        result = search_channel(buf, csv_anchor[:n_rec], n_rec, rec_size, dtype_hints=["f32", "u32", "i32"])
        if result[0] > best_anchor[0]:
            best_anchor = result
            best_rec_size = rec_size
        print(f"  rec_size={rec_size}: best anchor corr={result[0]:.4f} at offset={result[1]} dtype={result[2]}")
    if best_anchor[0] < args.min_corr:
        print(f"\n⚠ No record size yielded a confident anchor match (best corr={best_anchor[0]:.4f}).")
        print(f"   Consider widening --min-corr or checking that the .emublog3 and CSV are the same session.")
        return
    rec_size = best_rec_size
    n_records = len(buf) // rec_size
    print(f"\nLocked rec_size={rec_size}, n_records={n_records}")
    print(f"  Anchor at offset {best_anchor[1]} as {best_anchor[2]} (scale {best_anchor[3]:.6g})\n")

    # Now match every CSV column
    schema = {"rec_size": rec_size, "n_records": n_records, "channels": []}
    n_match = args.n_samples
    used_offsets = set()
    for col in df.columns:
        csv_vals = df[col].values[:n_match]
        result = search_channel(buf, csv_vals, n_match, rec_size)
        corr, offset, dtype, scale = result
        status = "✓" if corr >= args.min_corr else "?"
        print(f"  {status} {col!s:40s}  off={offset!s:5s} dtype={dtype!s:4s} corr={corr:+.3f} scale={scale:.6g}")
        if corr >= args.min_corr:
            schema["channels"].append({
                "name": col, "offset": offset, "dtype": dtype, "scale": float(scale),
                "correlation": float(corr),
            })
            used_offsets.add((offset, dtype))

    print(f"\nMatched {len(schema['channels'])}/{len(df.columns)} channels.")
    os.makedirs(os.path.dirname(args.out_schema) or ".", exist_ok=True)
    with open(args.out_schema, "w") as f:
        json.dump(schema, f, indent=2)
    print(f"Schema written to {args.out_schema}")

if __name__ == "__main__":
    main()
