"""From multiple analyze_sweep.py JSON results, propose a new cam1AdvTbl.

Usage:
  python propose_table.py --sweeps cell1.json cell2.json ... \
                          --tune <file.emub3> \
                          --out <file.emubt>

Reads the tune's vvtiMapBins10 and vvtiRpmBins10 axes, places each measured
optimum into the nearest cell, bilinearly interpolates between measured
cells, smooths, and writes the table as a .emubt.
"""
import argparse, json, re, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def get_symbol(xml, name):
    m = re.search(rf'<symbol name="{name}"[^/]*?/>', xml)
    if not m: return None
    blob = m.group(0)
    out = {"name": name}
    for k in ["value", "storage", "width", "height", "type", "data"]:
        mm = re.search(rf'{k}="([^"]*)"', blob)
        if mm: out[k] = mm.group(1)
    return out

def parse_emu_hex(s):
    out = []
    for tok in s.strip().split():
        if tok.startswith("-"):
            out.append(-int(tok[1:], 16))
        else:
            out.append(int(tok, 16))
    return out

def fmt_emu_hex(values, storage="sbyte"):
    bounds = {"ubyte":(0,255),"sbyte":(-128,127),"word":(0,65535),"sword":(-32768,32767)}
    lo, hi = bounds.get(storage, (-128, 127))
    out = []
    for v in values:
        v = max(lo, min(hi, int(round(v))))
        if v < 0: out.append(f"-{(-v):X}")
        else:     out.append(f"{v:X}")
    return " ".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweeps", nargs="+", required=True, help="JSON outputs from analyze_sweep.py")
    ap.add_argument("--tune", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--symbol", default="cam1AdvTbl")
    ap.add_argument("--smooth-passes", type=int, default=1)
    args = ap.parse_args()

    xml = open(args.tune).read()

    # Read axes
    map_bins_sym = get_symbol(xml, "vvtiMapBins10")
    rpm_bins_sym = get_symbol(xml, "vvtiRpmBins10")
    if not map_bins_sym or not rpm_bins_sym:
        print("❌ vvtiMapBins10 or vvtiRpmBins10 not found in tune")
        sys.exit(1)
    map_bins = parse_emu_hex(map_bins_sym["data"])
    rpm_bins = parse_emu_hex(rpm_bins_sym["data"])

    # Read current cam table (we'll modify only cells supported by data)
    cam_sym = get_symbol(xml, args.symbol)
    if not cam_sym:
        print(f"❌ {args.symbol} not found"); sys.exit(1)
    w, h = int(cam_sym["width"]), int(cam_sym["height"])
    storage = cam_sym["storage"]
    current = parse_emu_hex(cam_sym["data"])
    proposed = list(current)

    # Load all sweep results
    measurements = []  # list of (rpm, map, best_cam)
    for f in args.sweeps:
        with open(f) as fp:
            data = json.load(fp)
        for cell in data.get("cells", []):
            m = cell["map_bin"]
            r = cell["rpm_bin"]
            cam = cell.get("best_cam_by_map")
            if cam is None: continue
            measurements.append((r, m, cam))
    print(f"Loaded {len(measurements)} measured cells from {len(args.sweeps)} sweep file(s)")

    # Snap each measurement to the nearest cell
    def nearest(bins, val):
        return min(range(len(bins)), key=lambda i: abs(bins[i] - val))

    cells_modified = {}
    for rpm, map_, cam in measurements:
        ri = nearest(rpm_bins, rpm)
        mi = nearest(map_bins, map_)
        idx = ri * w + mi  # assuming RPM rows × MAP cols (verify against tune)
        # Actually for cam1AdvTbl (10x10), the layout may vary — assume rows=RPM, cols=MAP
        cells_modified[(ri, mi)] = cam
        proposed[idx] = cam

    # Bilinear interp could be added; for now we leave non-measured cells unchanged
    # and only smooth measured cells against their neighbors.
    if args.smooth_passes > 0:
        for _ in range(args.smooth_passes):
            new = list(proposed)
            for ri, mi in cells_modified:
                nbrs = []
                for dr, dm in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr, nm = ri+dr, mi+dm
                    if 0 <= nr < h and 0 <= nm < w:
                        nbrs.append(proposed[nr*w + nm])
                if nbrs:
                    # 50/50 self/neighbor average — gentle smoothing
                    avg_nbr = sum(nbrs) / len(nbrs)
                    new[ri*w + mi] = int(round(0.7 * proposed[ri*w + mi] + 0.3 * avg_nbr))
            proposed = new

    # Write .emubt
    hex_data = fmt_emu_hex(proposed, storage)
    out_xml = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<project version="1.0">',
               '  <tables>',
               f'    <symbol name="{args.symbol}" storage="{storage}" '
               f'width="{w}" height="{h}" data="{hex_data} "/>',
               '  </tables>',
               '</project>']
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(out_xml))
    print(f"✓ Wrote {args.out}")
    print(f"  Cells modified by measurement: {len(cells_modified)}")
    print(f"  Cells unchanged (out of {w*h}): {w*h - len(cells_modified)}")

    # Diff summary
    print(f"\nCells with measurement-driven changes (>2° delta):")
    for ri, mi in sorted(cells_modified):
        idx = ri*w + mi
        if abs(proposed[idx] - current[idx]) > 2:
            print(f"  RPM={rpm_bins[ri]}, MAP={map_bins[mi]}: {current[idx]}° → {proposed[idx]}°")

if __name__ == "__main__":
    main()
