"""Build VE2 from VE1 using interpolated lambda target deltas.

This is a narrow utility for the 2026-05-29 flex-fuel retune:

    VE2 = VE1 * (1 - (lambdaTable2 - lambdaTable))

The multiplier follows the local rough rule that 0.01 lambda is approximately
1% VE/fuel. It exports a JSON spec for the existing EMU .emubt exporter and a
markdown back-calc report for review.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def symbol(xml: str, name: str) -> dict[str, str]:
    match = re.search(rf'<symbol name="{re.escape(name)}"[^/]*/>', xml)
    if not match:
        raise KeyError(name)
    blob = match.group(0)
    return dict(re.findall(r'(\w+)="([^"]*)"', blob))


def parse_data(attrs: dict[str, str]) -> list[int]:
    out = []
    for token in attrs["data"].strip().split():
        if token.startswith("-"):
            out.append(-int(token[1:], 16))
        else:
            out.append(int(token, 16))
    return out


def interp_axis(axis: list[float], x: float) -> tuple[int, int, float]:
    if x <= axis[0]:
        return 0, 0, 0.0
    if x >= axis[-1]:
        last = len(axis) - 1
        return last, last, 0.0
    for i in range(len(axis) - 1):
        if axis[i] <= x <= axis[i + 1]:
            t = (x - axis[i]) / (axis[i + 1] - axis[i])
            return i, i + 1, t
    raise ValueError(x)


def bilinear(
    values: list[float],
    width: int,
    x_axis: list[float],
    y_axis: list[float],
    x: float,
    y: float,
) -> float:
    x0, x1, tx = interp_axis(x_axis, x)
    y0, y1, ty = interp_axis(y_axis, y)
    v00 = values[y0 * width + x0]
    v10 = values[y0 * width + x1]
    v01 = values[y1 * width + x0]
    v11 = values[y1 * width + x1]
    vx0 = v00 + (v10 - v00) * tx
    vx1 = v01 + (v11 - v01) * tx
    return vx0 + (vx1 - vx0) * ty


def row_major_table(rows: list[list[float]]) -> list[float]:
    return [cell for row in rows for cell in row]


def render_grid(title: str, rows: list[list[float]], y_axis: list[int], x_axis: list[int], fmt: str) -> str:
    lines = [f"### {title}", ""]
    for y, row in zip(reversed(y_axis), reversed(rows)):
        lines.append(f"{y:>5}  " + "  ".join(fmt.format(v) for v in row))
    lines.append("       " + "  ".join(f"{x:>6}" for x in x_axis))
    lines.append("RPM\\MAP " + "  ".join(" " * 4 for _ in x_axis) + " kPa")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Remap a VE table from another via the lambda-target delta.")
    ap.add_argument("--tune", required=True, help="tune XML (.xml.emub3) with the lambda tables + axes")
    ap.add_argument("--ve1", required=True, help="source VE .emubt (table to remap from)")
    ap.add_argument("--out-emubt", dest="out_emubt", required=True, help="output .emubt path (for the exporter spec)")
    ap.add_argument("--out-json", dest="out_json", default="ve_remap_spec.json")
    ap.add_argument("--out-report", dest="out_report", default="ve_remap_backcalc.md")
    ap.add_argument("--src-symbol", dest="src_symbol", default="veTable")
    ap.add_argument("--dst-symbol", dest="dst_symbol", default="veTable2")
    ap.add_argument("--map-bins", dest="map_bins_sym", default="mapBins")
    ap.add_argument("--rpm-bins", dest="rpm_bins_sym", default="rpmBins")
    ap.add_argument("--lambda-map-bins", dest="lmap_sym", default="mapBinsL8")
    ap.add_argument("--lambda-rpm-bins", dest="lrpm_sym", default="rpmBins10")
    args = ap.parse_args()
    TUNE = Path(args.tune)
    VE1_EMUBT = Path(args.ve1)
    OUT_JSON = Path(args.out_json)
    OUT_REPORT = Path(args.out_report)
    OUT_EMUBT = Path(args.out_emubt)

    tune_xml = TUNE.read_text(encoding="utf-8")
    ve_xml = VE1_EMUBT.read_text(encoding="utf-8")

    ve1 = symbol(ve_xml, args.src_symbol)
    ve_w = int(ve1["width"])
    ve_h = int(ve1["height"])
    ve_raw = parse_data(ve1)

    map_bins = parse_data(symbol(tune_xml, args.map_bins_sym))
    rpm_bins = parse_data(symbol(tune_xml, args.rpm_bins_sym))
    lam_map_bins = parse_data(symbol(tune_xml, args.lmap_sym))
    lam_rpm_bins = parse_data(symbol(tune_xml, args.lrpm_sym))

    lambda_1 = [v / 100.0 for v in parse_data(symbol(tune_xml, "lambdaTable"))]
    lambda_2 = [v / 100.0 for v in parse_data(symbol(tune_xml, "lambdaTable2"))]
    lambda_delta = [b - a for a, b in zip(lambda_1, lambda_2)]

    delta_rows: list[list[float]] = []
    mult_rows: list[list[float]] = []
    ve1_rows: list[list[float]] = []
    ve2_rows: list[list[float]] = []
    ve2_raw_rows: list[list[int]] = []

    for r, rpm in enumerate(rpm_bins):
        delta_row = []
        mult_row = []
        ve1_row = []
        ve2_row = []
        ve2_raw_row = []
        for c, map_kpa in enumerate(map_bins):
            idx = r * ve_w + c
            delta = bilinear(lambda_delta, 8, lam_map_bins, lam_rpm_bins, map_kpa, rpm)
            multiplier = 1.0 - delta
            new_raw = round(ve_raw[idx] * multiplier)
            new_raw = max(0, min(0xFFF, new_raw))
            delta_row.append(delta)
            mult_row.append(multiplier)
            ve1_row.append(ve_raw[idx] * 0.1)
            ve2_row.append(new_raw * 0.1)
            ve2_raw_row.append(new_raw)
        delta_rows.append(delta_row)
        mult_rows.append(mult_row)
        ve1_rows.append(ve1_row)
        ve2_rows.append(ve2_row)
        ve2_raw_rows.append(ve2_raw_row)

    spec = {
        "out": str(OUT_EMUBT),
        "symbols": [
            {
                "name": args.dst_symbol,
                "storage": "u12",
                "width": ve_w,
                "height": ve_h,
                "values": row_major_table(ve2_raw_rows),
            }
        ],
    }
    OUT_JSON.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    report = [
        "# VE2 lambda-delta remap back-calc",
        "",
        f"Source VE1: `{VE1_EMUBT.name}`",
        f"Lambda source: `{TUNE.name}`",
        "",
        "Formula:",
        "",
        "```",
        "lambda_delta = lambdaTable2 - lambdaTable",
        "VE2 = VE1 * (1 - lambda_delta)",
        "```",
        "",
        "This follows the rough rule: `+0.01 lambda leaner ~= -1% VE`.",
        "",
        render_grid("Interpolated lambda delta on VE grid", delta_rows, rpm_bins, map_bins, "{:>6.3f}"),
        render_grid("VE multiplier", mult_rows, rpm_bins, map_bins, "{:>6.3f}"),
        render_grid("Source VE1 display values", ve1_rows, rpm_bins, map_bins, "{:>6.1f}"),
        render_grid("Remapped VE2 display values", ve2_rows, rpm_bins, map_bins, "{:>6.1f}"),
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_REPORT}")
    print(f"VE2 raw count: {ve_w * ve_h}")


if __name__ == "__main__":
    main()
