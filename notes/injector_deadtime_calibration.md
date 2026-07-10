# Injector dead-time calibration — `injOpeningTimeTbl` (Injectors cal. [ms])

> **Software page:** *Injectors*. Sits downstream of the fuel-pressure model in
> [fueling.md → Fuel rail / base pressure](fueling.md): the Y axis is **effective fuel pressure**,
> the same live differential the regulator/sensor model produces, so this table only indexes
> correctly once base pressure and `injectorsSize` are honest (see [fueling.md](fueling.md) F6).

**What it is.** Injector dead time (a.k.a. latency / offset) — the delay between coil energization
and actual fuel flow. EMU adds it to the computed pulse width. It **rises at lower supply voltage**
(slower solenoid pull-in) and **rises at higher effective fuel pressure** (more hydraulic force
holding the pintle shut). Getting it wrong skews mixture most where pulse width is short — **idle
and light cruise** — and during transients that swing rail pressure (boost, pump sag).

## Table encoding (verified on this build)

| property | value |
|---|---|
| symbol | `injOpeningTimeTbl` |
| EMU title / filename | `Injectors - Injectors cal. [ms]` |
| storage | `ubyte` |
| dims | **width 12 × height 4** (row-major) |
| **scale** | **0.03125 ms/count (1/32)** → `ms = raw / 32`, `raw = round(ms × 32)` |
| X axis | Battery Voltage: 6,7,8,…,17 V — **col 0 = 6 V** (lowest) |
| Y axis | Effective fuel pressure: 200, 300, 400, 500 kPa **g** — **row 0 = 200** (lowest), per the emu-black-emubt-export low→high row convention |

Scale proof against the live table: `0x43`=67 → 67×0.03125 = **2.09 ms** ✓; `0x31`=49 → 1.53 ✓;
`0x1F`=31 → 0.97 ✓. The `.emubt` carries **only the data block** — the axis bins (vbatt, pressure)
live in the project, so the grid just maps row-major onto whatever axes the table already has.

> **Orientation spot-check on import:** the **500 kPa row (top of the EMU grid) must show the
> HIGHEST** dead times and 200 kPa (bottom) the lowest. If it's inverted, the row order is flipped.

## Source data — ID1050X Dynamic Flow Data (Injector Dynamics)

Offset in **microseconds**, by fuel pressure (psi**d** = differential) × supply volts. This is the
authoritative ID1050X characterization; do **not** hand-invent values. (`psid` is the differential,
which equals EMU's *effective* fuel pressure — so a psi row maps straight onto a kPa-g row via
×6.895.)

| psid | 8 V | 10 V | 12 V | 14 V | 16 V |
|---:|---:|---:|---:|---:|---:|
| 40.0 | 1920 | 1410 | 1115 | 920 | 790 |
| 43.5 | 1955 | 1425 | 1125 | 925 | 795 |
| 45.0 | 1970 | 1435 | 1130 | 930 | 800 |
| 50.0 | 2025 | 1475 | 1160 | 955 | 825 |
| 55.0 | 2080 | 1515 | 1190 | 980 | 845 |
| 60.0 | 2140 | 1540 | 1215 | 1000 | 860 |
| 65.0 | 2195 | 1560 | 1225 | 1010 | 855 |
| 70.0 | 2255 | 1575 | 1235 | 1015 | 850 |
| 75.0 | 2340 | 1610 | 1250 | 1020 | 850 |
| 80.0 | 2440 | 1655 | 1265 | 1020 | 850 |
| 85.0 | 2555 | 1705 | 1280 | 1030 | 855 |
| 90.0 | 2680 | 1765 | 1315 | 1045 | 865 |
| 95.0 | 2815 | 1825 | 1355 | 1075 | 880 |
| 100.0 | 2960 | 1890 | 1405 | 1110 | 900 |

(The ID sheet's **Slope cc/min** column is the pressure-flow curve, **not** used here — that belongs
to `injectorsSize`, entered at base pressure: 1065 @ 3 bar → **1230 @ 4 bar**, see [fueling.md](fueling.md).)

## Conversion recipe

1. **Pressure axis:** kPa g → psi (÷6.894757): 200→29.0, 300→43.5, 400→58.0, 500→72.5. Interpolate
   ID offset onto those. 300 kPa lands on the 43.5 psi row exactly; **200 kPa (29 psi) is below the
   sheet's 40 psi floor** → linear-extrapolate off the 40→45 psi slope.
2. **Voltage axis:** the ID grid is 8–16 V; interpolate to fill 6…17 V. **6, 7, and 17 V are off the
   sheet** → linear-extrapolate off the nearest segment (8–10 V down, 14–16 V up). This is the only
   real change from the old flat table, which just **clamped** the edges (held the 8 V value at 6–7 V,
   the 16 V value at 17 V) — i.e. under-stated dead time at low cranking voltage.
3. **µs → ms** (÷1000), then **raw = round(ms × 32)**, clamp to ubyte. Max here = 96 (well under 255).

## Result (this build)

Display ms (rows 200→500 kPa g, cols 6→17 V):

```
kPa     6    7    8    9   10   11   12   13   14   15   16   17
200  2.25 2.03 1.81 1.59 1.38 1.22 1.09 1.00 0.91 0.84 0.78 0.72
300  2.50 2.22 1.97 1.69 1.44 1.28 1.12 1.03 0.94 0.88 0.78 0.72
400  2.69 2.41 2.12 1.81 1.53 1.38 1.22 1.09 1.00 0.94 0.84 0.78
500  3.00 2.66 2.31 1.94 1.59 1.41 1.25 1.12 1.03 0.94 0.84 0.78
```

Sanity vs the old flat table (which was ID1050X data at ~400 kPa only): the **400 row matches** it
(10 V 1.53, 12 V ~1.21, 14 V ~0.99, 16 V ~0.85). The new content is the **pressure slope** (14 V:
0.91 ms @200 → 1.03 ms @500) and the **low-voltage rise** at 6–7 V.

`.emubt`: [`supra/exports/Injectors - Injectors cal. [ms].emubt`](../supra/exports/Injectors%20-%20Injectors%20cal.%20[ms].emubt)
(raw hex `48 41 3A 33 2C 27 23 20 1D 1B 19 17  50 47 3F 36 2E 29 24 21 1E 1C 19 17  56 4D 44 3A 31 2C 27 23 20 1E 1B 19  60 55 4A 3E 33 2D 28 24 21 1E 1B 19`).

## How to regenerate

`skills/emu-black-emubt-export/scripts/injector_deadtime_to_emubt.py` holds the ID1050X offset data
and the interp/extrap logic. Run it to print the `--values` line, then:

```bash
python skills/emu-black-emubt-export/scripts/injector_deadtime_to_emubt.py
python skills/emu-black-emubt-export/scripts/export_emubt.py \
  --name injOpeningTimeTbl --storage ubyte --width 12 --height 4 \
  --values "<paste>" --out "supra/exports/Injectors - Injectors cal. [ms].emubt"
```

For a **different injector**, swap `OFFSET_US`/`PSI`/`VID` in the generator. For a **different
pressure/voltage axis**, edit `KPA_ROWS`/`V_COLS` — but re-confirm the scale and row order against a
fresh decode first (never assume). EMU's **Injectors wizard** can also auto-populate dead time for
recognized injector models — try it before hand-entering, and use this method when the model isn't
listed or you want it on the repo record.

## Verify after import

- Spot-check 3 cells against the ms grid above (e.g. 400 kPa / 14 V ≈ **1.00 ms**).
- Confirm the orientation spot-check (500 row highest).
- Idle quality and short-PW mixture are the payoff — re-check idle lambda/STFT after import,
  since dead time is a large fraction of the idle pulse.
