#!/usr/bin/env python3
"""Convert an injector manufacturer dead-time (offset) table into EMU Black's
`injOpeningTimeTbl` ("Injectors - Injectors cal. [ms]") grid.

Manufacturers (Injector Dynamics, etc.) publish dead time / latency / "offset"
as a 2D grid of **offset (microseconds) vs fuel pressure (psid) x supply
voltage**. EMU Black's table wants the same thing on its own axes:

  X = Battery Voltage (V)        : 6..17  (12 cols), col 0 = 6 V (lowest)
  Y = Effective fuel pressure    : 200/300/400/500 kPa g (4 rows),
                                   row 0 = 200 (lowest)  [low->high, per
                                   emu-black-emubt-export row-major convention]
  cell  = dead time in ms, ubyte, SCALE 0.03125 ms/count (1/32)
          (verified: 0x43=67 -> 2.09 ms, 0x1F=31 -> 0.97 ms)

This instance is populated with the **ID1050x Dynamic Flow Data** offset table.
Swap `OFFSET_US` / `PSI` / `VID` for a different injector and re-run.

Physics: dead time RISES with fuel pressure (more hydraulic force holds the
pintle shut) and FALLS with supply voltage (faster solenoid pull-in).

Run:  python injector_deadtime_to_emubt.py
Then feed the printed --values line to export_emubt.py (or it is identical to
the committed `supra/exports/Injectors - Injectors cal. [ms].emubt`).
"""

KPA_PER_PSI = 6.894757
SCALE = 0.03125  # ms per ubyte count (1/32)

# --- Injector source data: ID1050x Dynamic Flow Data, Offset (microseconds) ---
PSI = [40.0, 43.5, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0]
VID = [8, 10, 12, 14, 16]
OFFSET_US = {
    40.0:  [1920, 1410, 1115,  920, 790],
    43.5:  [1955, 1425, 1125,  925, 795],
    45.0:  [1970, 1435, 1130,  930, 800],
    50.0:  [2025, 1475, 1160,  955, 825],
    55.0:  [2080, 1515, 1190,  980, 845],
    60.0:  [2140, 1540, 1215, 1000, 860],
    65.0:  [2195, 1560, 1225, 1010, 855],
    70.0:  [2255, 1575, 1235, 1015, 850],
    75.0:  [2340, 1610, 1250, 1020, 850],
    80.0:  [2440, 1655, 1265, 1020, 850],
    85.0:  [2555, 1705, 1280, 1030, 855],
    90.0:  [2680, 1765, 1315, 1045, 865],
    95.0:  [2815, 1825, 1355, 1075, 880],
    100.0: [2960, 1890, 1405, 1110, 900],
}

# --- EMU target axes ---
KPA_ROWS = [200, 300, 400, 500]      # Y, low -> high (row 0 first)
V_COLS = list(range(6, 18))          # X, 6..17 V


def _lin(x, x0, x1, y0, y1):
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def interp(xt, xs, ys):
    """Linear interp; edges linear-extrapolate off the nearest segment."""
    if xt <= xs[0]:
        return _lin(xt, xs[0], xs[1], ys[0], ys[1])
    if xt >= xs[-1]:
        return _lin(xt, xs[-2], xs[-1], ys[-2], ys[-1])
    for i in range(len(xs) - 1):
        if xs[i] <= xt <= xs[i + 1]:
            return _lin(xt, xs[i], xs[i + 1], ys[i], ys[i + 1])


def build():
    # 1) offset (us) at each manufacturer voltage for the 4 target pressures
    psi_targets = [k / KPA_PER_PSI for k in KPA_ROWS]
    at_vid = []
    for pt in psi_targets:
        at_vid.append([interp(pt, PSI, [OFFSET_US[p][vi] for p in PSI])
                       for vi in range(len(VID))])
    # 2) interpolate/extrapolate across voltage to the full 6..17 axis
    raw_rows = []
    ms_rows = []
    for r in range(len(KPA_ROWS)):
        ms = [interp(v, VID, at_vid[r]) / 1000.0 for v in V_COLS]
        ms_rows.append(ms)
        raw_rows.append([round(m / SCALE) for m in ms])
    return ms_rows, raw_rows


if __name__ == "__main__":
    ms_rows, raw_rows = build()
    print("Display ms grid (rows 200->500 kPa g, cols 6->17 V):")
    print("kPa  " + " ".join(f"{v:>5}" for v in V_COLS))
    for k, ms in zip(KPA_ROWS, ms_rows):
        print(f"{k:<4} " + " ".join(f"{m:5.2f}" for m in ms))
    flat = [c for row in raw_rows for c in row]
    assert max(flat) <= 255, "ubyte overflow"
    print("\n--values for export_emubt.py:")
    print('"' + " ".join(str(c) for c in flat) + '"')
    print("\nhex:", " ".join(f"{c:02X}" for c in flat))
