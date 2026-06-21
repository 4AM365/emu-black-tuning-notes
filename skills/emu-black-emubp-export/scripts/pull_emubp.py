#!/usr/bin/env python3
"""
pull_emubp.py — pull scalar parameters from an EMU Black XML tune into an
importable .emubp parameters file (a <variables> block of scalar symbols).

Three ways to choose which symbols to pull:

  --template <example.emubp>   Use an example .emubp as the symbol list AND order.
                               Pulls each symbol's CURRENT value from --source.
                               (Preferred: EMU itself defines these groups; the
                               'example ... .emubp' files in a vehicle folder are
                               exactly those group exports.)

  --prefix vvtCam1             Pull every SCALAR symbol whose name starts with the
                               prefix, in source-file order.

  --symbols "a b c"            Pull exactly these named symbols, in this order.

--source accepts a vehicle name (resolved via the EMU source index below), a
folder (newest *.xml.emub3 is used), or a direct .xml.emub3 path.

Scalars only: symbols carrying a `data=`/`width=` table payload are skipped with a
warning — tables belong in a .emubt (use emu-black-emubt-export), never a .emubp.

Examples
--------
  # pull bradley's cam-1 PID values shaped like the example, write into bradley
  python pull_emubp.py --source bradley \
    --template ".../bradley/example CAM 1 - CAM 1 PID.emubp" \
    --out ".../bradley/bradley CAM 1 - CAM 1 PID.emubp"

  # "pull the cam settings from land cruiser to emubp"
  python pull_emubp.py --source "land cruiser" --prefix vvtCam1 \
    --out "land cruiser CAM 1 settings.emubp"
"""
import argparse, os, re, sys, glob

# --- EMU source-folder index (mirror of repo EMU_SOURCE_INDEX.md) -------------
BASE = r"C:\Users\WTCra\OneDrive\Documents"
V3   = os.path.join(BASE, "EMU_BLACK_V3")
V1   = os.path.join(BASE, "EMU_BLACK")
VEHICLE_FOLDERS = {
    "supra":        os.path.join(V3, "Supra"),
    "bradley":      os.path.join(V3, "bradley"),
    "land cruiser": os.path.join(V3, "Land Cruiser"),
    "landcruiser":  os.path.join(V3, "Land Cruiser"),
    "fj80":         os.path.join(V3, "Land Cruiser"),
    "napier":       os.path.join(V1, "Napier_GS300"),   # V1 only
    "gs300":        os.path.join(V1, "Napier_GS300"),
    "base maps":    os.path.join(V3, "Base maps"),
    "default":      os.path.join(V3, "DEFAULT"),
}

SYMBOL_RE = re.compile(r"<symbol\b[^>]*/>")
ATTR_RE   = re.compile(r'(\w+)\s*=\s*"([^"]*)"')


def parse_symbols(xml_text):
    """Return {name: {attr: val}} for every <symbol .../> in the text."""
    out = {}
    order = []
    for tag in SYMBOL_RE.findall(xml_text):
        attrs = dict(ATTR_RE.findall(tag))
        name = attrs.get("name")
        if not name:
            continue
        out[name] = attrs
        order.append(name)
    return out, order


def resolve_source(source):
    """Resolve a vehicle name / folder / file to a concrete .xml.emub3 path."""
    if os.path.isfile(source):
        return source
    # Known vehicle names win over a same-named local dir (the repo has a `supra/`).
    folder = VEHICLE_FOLDERS.get(source.strip().lower())
    if folder is None:
        if os.path.isdir(source):
            folder = source
        else:
            sys.exit(f"error: unknown source '{source}'. Known vehicles: "
                     f"{', '.join(sorted(VEHICLE_FOLDERS))}; or pass a folder/file path.")
    if not os.path.isdir(folder):
        sys.exit(f"error: source folder does not exist: {folder}")
    cands = glob.glob(os.path.join(folder, "*.xml.emub3"))
    if not cands:
        sys.exit(f"error: no *.xml.emub3 tune found in {folder} "
                 f"(only XML exports are readable; binary .emub3 starts with PK).")
    newest = max(cands, key=os.path.getmtime)
    return newest


def is_scalar(attrs):
    """A parameter scalar carries `value`; a table carries `data`/`width`."""
    return "value" in attrs and "data" not in attrs and "width" not in attrs


def build_variables(symtab, wanted):
    """Return (rows, missing, skipped_tables) for the wanted symbol names."""
    rows, missing, skipped = [], [], []
    for name in wanted:
        attrs = symtab.get(name)
        if attrs is None:
            missing.append(name)
            continue
        if not is_scalar(attrs):
            skipped.append(name)
            continue
        rows.append(attrs)
    return rows, missing, skipped


def emit_emubp(rows):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<project version="1.0">', '  <variables>']
    for a in rows:
        storage = a.get("storage", "ubyte")
        typ     = a.get("type", "value")
        lines.append(f'    <symbol name="{a["name"]}" value="{a["value"]}" '
                     f'storage="{storage}" type="{typ}"/>')
    lines += ['  </variables>', '</project>', '']
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True,
                    help="vehicle name, folder, or .xml.emub3 path")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--template", help="example .emubp; defines symbol list + order")
    g.add_argument("--prefix",   help="pull scalar symbols whose name starts with this")
    g.add_argument("--symbols",  help="explicit space-separated symbol names")
    ap.add_argument("--out", required=True, help="output .emubp path")
    args = ap.parse_args()

    src = resolve_source(args.source)
    with open(src, "r", encoding="utf-8", errors="replace") as f:
        symtab, src_order = parse_symbols(f.read())
    print(f"source tune : {src}")

    template_vals = {}
    if args.template:
        with open(args.template, "r", encoding="utf-8", errors="replace") as f:
            tpl, wanted = parse_symbols(f.read())
        template_vals = {n: a.get("value") for n, a in tpl.items()}
        print(f"template    : {args.template}  ({len(wanted)} symbols)")
    elif args.prefix:
        wanted = [n for n in src_order if n.startswith(args.prefix) and is_scalar(symtab[n])]
        print(f"prefix      : {args.prefix}*  ({len(wanted)} scalar matches)")
    else:
        wanted = args.symbols.split()

    rows, missing, skipped = build_variables(symtab, wanted)

    out_text = emit_emubp(rows)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(out_text)
    print(f"wrote       : {args.out}  ({len(rows)} parameters)\n")

    # comparison report
    w = max((len(a["name"]) for a in rows), default=10)
    if args.template:
        print(f"{'symbol'.ljust(w)}  {'template':>10}  {'pulled':>10}")
        for a in rows:
            tv = template_vals.get(a["name"], "")
            flag = "" if str(tv) == str(a["value"]) else "  <- differs"
            print(f"{a['name'].ljust(w)}  {str(tv):>10}  {str(a['value']):>10}{flag}")
    else:
        print(f"{'symbol'.ljust(w)}  {'value':>10}")
        for a in rows:
            print(f"{a['name'].ljust(w)}  {str(a['value']):>10}")

    if skipped:
        print("\nSKIPPED (tables, not scalars — use emu-black-emubt-export):")
        for n in skipped:
            print(f"  - {n}")
    if missing:
        print("\nMISSING from source (not written):")
        for n in missing:
            print(f"  - {n}")


if __name__ == "__main__":
    main()
