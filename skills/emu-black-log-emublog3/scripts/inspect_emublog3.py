"""Inspect a .emublog3 file: decompress, dump leading bytes, search for record period.

Usage: python inspect.py <file.emublog3>
"""
import sys, zlib, struct, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def main(path):
    with open(path, "rb") as f:
        raw = f.read()
    print(f"File: {path}")
    print(f"Compressed size: {len(raw):,} bytes")
    if raw[:3] != b"\x1f\x8b\x08":
        print("  ⚠ Not a gzip envelope (no 1F 8B 08 header).")
        return
    d = zlib.decompressobj(16 + zlib.MAX_WBITS)
    out = d.decompress(raw)
    # Drain any trailing data
    while not d.eof:
        try:
            chunk = d.decompress(d.unconsumed_tail) if d.unconsumed_tail else b""
            if not chunk: break
            out += chunk
        except Exception:
            break
    print(f"Decompressed: {len(out):,} bytes  (ratio {len(out)/len(raw):.2f}×)")
    print()

    print("First 64 bytes:")
    print(" ".join(f"{b:02X}" for b in out[:64]))
    print()
    print("Bytes 64-128:")
    print(" ".join(f"{b:02X}" for b in out[64:128]))
    print()

    # Try common record sizes and look for monotonic float32 at offset 0
    print("Looking for monotonic float32 at record-aligned offset 0...")
    for size in range(60, 5000, 4):
        n = len(out) // size
        if n < 30: continue
        try:
            vals = [struct.unpack_from("<f", out, i * size)[0] for i in range(20)]
        except Exception:
            continue
        if not all(0 < v < 1e7 for v in vals): continue
        diffs = [vals[i+1] - vals[i] for i in range(len(vals)-1)]
        if not all(0.001 < d < 1.0 for d in diffs): continue
        if max(diffs) - min(diffs) > 0.01: continue
        print(f"  rec_size={size}: float32 head looks like TIME — {n} records,"
              f" Δ={diffs[0]:.4f}s")

    # Look for monotonic uint32 ms timestamp at offset 0
    print()
    print("Looking for monotonic uint32 at offset 0 (ms timestamp)...")
    for size in range(60, 5000, 4):
        n = len(out) // size
        if n < 30: continue
        try:
            vals = [struct.unpack_from("<I", out, i * size)[0] for i in range(20)]
        except Exception:
            continue
        if not all(0 < v < 1e9 for v in vals): continue
        diffs = [vals[i+1] - vals[i] for i in range(len(vals)-1)]
        if not all(20 < d < 200 for d in diffs): continue
        if max(diffs) - min(diffs) > 5: continue
        print(f"  rec_size={size}: uint32 head looks like ms timestamp — {n} records,"
              f" Δ={diffs[0]} ms")

    # Look for an obvious header — possibly a count + magic
    print()
    print("Header field guesses (LE 32-bit):")
    for off in [0, 4, 8, 12, 16]:
        u = struct.unpack_from("<I", out, off)[0]
        i = struct.unpack_from("<i", out, off)[0]
        f = struct.unpack_from("<f", out, off)[0]
        print(f"  offset {off:>2}: u32={u}  i32={i}  f32={f:.6g}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(1)
    main(sys.argv[1])
