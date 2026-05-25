"""Parse a .emublog3 file into a DataFrame (or CSV) using a discovered schema.

Usage:
  python parse_emublog3.py --emublog3 <file.emublog3> --schema <schema.json> [--out-csv <path>]

Or as a library:
  from parse_emublog3 import read_emublog3
  df = read_emublog3('log.emublog3', schema='schemas/supra_v1.json')
"""
import argparse, json, struct, sys, io, zlib

try:
    import pandas as pd
    import numpy as np
except ImportError:
    pd = None
    np = None

DTYPES = {
    "u8": ("B", 1), "i8": ("b", 1),
    "u16": ("<H", 2), "i16": ("<h", 2),
    "u32": ("<I", 4), "i32": ("<i", 4),
    "f32": ("<f", 4),
}

def decompress(path):
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

def read_emublog3(emublog3_path, schema):
    """Parse .emublog3 → pandas DataFrame.

    Args:
        emublog3_path: Path to the binary log.
        schema: Either a path to a JSON schema or a dict.
    """
    if pd is None:
        raise ImportError("pandas required: pip install pandas")
    if isinstance(schema, str):
        with open(schema) as f: schema = json.load(f)
    buf = decompress(emublog3_path)
    rec_size = schema["rec_size"]
    n_records = min(schema["n_records"], len(buf) // rec_size)
    data = {}
    for ch in schema["channels"]:
        fmt, _ = DTYPES[ch["dtype"]]
        vals = np.array([struct.unpack_from(fmt, buf, ch["offset"] + i * rec_size)[0]
                         for i in range(n_records)], dtype=float)
        vals *= ch.get("scale", 1.0)
        data[ch["name"]] = vals
    return pd.DataFrame(data)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emublog3", required=True)
    ap.add_argument("--schema",   required=True)
    ap.add_argument("--out-csv",  help="Write CSV; default = stdout summary")
    args = ap.parse_args()

    df = read_emublog3(args.emublog3, args.schema)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    print(f"Parsed {len(df):,} records × {len(df.columns)} channels")
    if args.out_csv:
        df.to_csv(args.out_csv, sep=";", index=False, float_format="%.4f")
        print(f"Wrote {args.out_csv}")
    else:
        print(df.head().to_string())

if __name__ == "__main__":
    main()
