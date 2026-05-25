#!/usr/bin/env python3
"""Write EMU Black single/multi-table .emubt files from values we generate.

Why this exists: the round-trip tools in emubt_breakout (emubt_to_csv.py /
csv_to_emubt.py) are great for editing EXISTING tables via CSV, but their
fresh-create path infers storage as "u8/u16" (not the "ubyte/sbyte/word/sword"
EMU expects) and cannot tag a signed table. When WE compute a table from
scratch (e.g. a rescaled airflow map), we need to state the storage type
explicitly and emit the exact byte/sign/hex encoding EMU imports cleanly.

Encoding rules (verified against real EMU exports):
  - data is space-separated UPPERCASE hex, no 0x prefix: 108 -> "6C", 0 -> "0".
  - signed types use sign + hex magnitude, NOT two's complement: -13 -> "-D".
  - the XML declaration MUST use double quotes; ElementTree's single-quote
    default is rejected by the ECU, so we template the file as text.

Usage A (single table, raw integer values):
  python export_emubt.py --name idleArmedAirFlow --storage ubyte \
      --width 8 --height 1 --values "48 63 77 87 95 101 107 108" \
      --out "Airflow - Armed state air flow [%].emubt"

Usage B (single table, DISPLAY values + scale -> raw = round(display/scale)):
  python export_emubt.py --name idleActiveAirflow --storage ubyte \
      --width 8 --height 5 --scale 0.5 --values "56.5 50.5 ... 56.5" \
      --out "Airflow - Active state air flow [%].emubt"

Usage C (one or more tables from a JSON spec; values may be 2D rows or flat):
  python export_emubt.py --json spec.json
  spec.json:
  {
    "out": "Airflow - Active state air flow [%].emubt",
    "symbols": [
      {"name": "idleActiveAirflow", "storage": "ubyte",
       "width": 8, "height": 5, "scale": 0.5,
       "values": [[56.5,50.5,37.5,19.5,16,14.5,14.5,14.5], ...]}
    ]
  }
"""
import argparse
import json
import re
import sys
from pathlib import Path

# raw integer range allowed per storage type
RANGES = {
    "ubyte": (0, 255),
    "sbyte": (-128, 127),
    "word": (0, 65535),
    "sword": (-32768, 32767),
    "u12": (0, 4095),
}


def to_raw(value, scale):
    """Convert a (possibly display-scaled) value to the stored raw integer."""
    return int(round(float(value) / scale))


def fmt_hex(v):
    """EMU hex: uppercase magnitude, leading '-' for negatives, no 0x."""
    return format(v, "X")  # format(-13,'X') -> '-D'; format(108,'X') -> '6C'


def flatten(values):
    """Accept a flat list or a list of rows; return a flat list."""
    flat = []
    for item in values:
        if isinstance(item, (list, tuple)):
            flat.extend(item)
        else:
            flat.append(item)
    return flat


def build_symbol(name, storage, width, height, values, scale):
    if storage not in RANGES:
        raise ValueError(f"unknown storage {storage!r}; expected one of {list(RANGES)}")
    flat = flatten(values)
    if len(flat) != width * height:
        raise ValueError(
            f"{name}: got {len(flat)} values but width*height = {width}*{height} = {width*height}"
        )
    raw = [to_raw(v, scale) for v in flat]
    lo, hi = RANGES[storage]
    bad = [(i, r) for i, r in enumerate(raw) if not (lo <= r <= hi)]
    if bad:
        preview = ", ".join(f"idx{i}={r}" for i, r in bad[:5])
        raise ValueError(f"{name}: {len(bad)} value(s) out of {storage} range [{lo},{hi}]: {preview}")
    data = " ".join(fmt_hex(r) for r in raw) + " "  # trailing space matches EMU exports
    return (
        f'    <symbol name="{name}" storage="{storage}" '
        f'width="{width}" height="{height}" data="{data}"/>'
    )


def write_emubt(out_path, symbol_lines):
    body = "\n".join(symbol_lines)
    text = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<project version="1.0">\n'
        "  <tables>\n"
        f"{body}\n"
        "  </tables>\n"
        "</project>\n"
    )
    Path(out_path).write_text(text, encoding="utf-8", newline="\n")
    return out_path


def parse_inline_values(s):
    """Split a CLI --values string on whitespace or commas into floats."""
    return [t for t in re.split(r"[\s,]+", s.strip()) if t]


def main():
    ap = argparse.ArgumentParser(description="Export EMU Black .emubt table files.")
    ap.add_argument("--json", help="JSON spec describing out path and one or more symbols")
    ap.add_argument("--name")
    ap.add_argument("--storage", choices=list(RANGES))
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--values", help="space/comma separated values")
    ap.add_argument("--scale", type=float, default=1.0,
                    help="display->raw divisor (e.g. 0.5 for airflow %% tables). Default 1.0 = raw input.")
    ap.add_argument("--out")
    args = ap.parse_args()

    if args.json:
        spec = json.loads(Path(args.json).read_text(encoding="utf-8"))
        out = spec["out"]
        lines = []
        for sym in spec["symbols"]:
            lines.append(build_symbol(
                sym["name"], sym["storage"], int(sym["width"]), int(sym["height"]),
                sym["values"], float(sym.get("scale", 1.0)),
            ))
        write_emubt(out, lines)
        print(f"[SAVED] {out} ({len(lines)} symbol(s))")
        return

    required = [args.name, args.storage, args.width, args.height, args.values, args.out]
    if any(x is None for x in required):
        ap.error("single-table mode needs --name --storage --width --height --values --out")
    line = build_symbol(
        args.name, args.storage, args.width, args.height,
        parse_inline_values(args.values), args.scale,
    )
    write_emubt(args.out, [line])
    print(f"[SAVED] {args.out} (1 symbol)")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, FileNotFoundError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
