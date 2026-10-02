# Oil pressure — sensor, measured RPM×CLT baseline, protection config

**Software page:** Sensors & inputs (sensor + cal) · Engine protection (cut/failsafe).
See [[sensors_and_inputs]], [[engine_protection]].

## Sensor & calibration (from tune `supra xml v3 05292026.xml.emub3`)

- `oilPressureInput = 204` — analog input assigned; sensor **installed and valid**
  (`Engine oil pressure status` reads 1 for all rows across all logs that carry it;
  status polarity per [[log]]: 1 = present/OK).
- 2-point cal: `oilPressureCalBins = 19 E6` (hex → 25, 230), `oilPressureCal = 0 A5`
  (hex → 0, 165). Bins decode as sensor voltage at ~0.02 V/count → **0.50 V → 4.60 V**,
  i.e. a classic 0.5–4.5 V analog pressure sender.
- **Logged `Engine oil pressure` channel is in BAR** (1/16-bar = 0.0625 steps),
  confirmed by magnitude (hot idle ~1.4–3 bar, relief plateau ~6 bar). This is the
  engineering-unit ground truth; use it directly, don't re-derive from the cal.
- **Tap location:** post-oil-filter, on the sandwich plate. Reads pressure delivered
  to the main gallery → also reflects filter restriction (a rising tap-vs-expected
  delta would indicate a clogging filter). No restriction signature observed.

## Measured baseline (2026-07-12)

Source: 4 logs carrying the channel — `20260524_1301`, `drive_wobble`, `drivehome`,
`new_fuel_strategy`. ~45 min running samples, gated `status==1 & RPM>=500 & OP>=0.5`
(the OP>=0.5 gate drops oil-pump-prime transients: every sub-0.5 bar "running" sample
sits within 0.1–1.5 s of the engine first catching — start prime, not a dropout).
CLT span 28→111 °C, RPM to 6500.

**Median oil pressure [bar] (psi):** rows RPM high→low, cols CLT low→high

| RPM ＼ CLT | 28–50 | 50–70 | 70–85 | 85–95 | 95–111 (hot) |
|---|---|---|---|---|---|
| 4500+     | 9.1 (132) | — | — | 7.1 (103) | **6.3 (92)** |
| 3500–4500 | 8.9 (130) | — | 7.9 (115) | 7.1 (103) | **6.1 (88)** |
| 3000–3500 | 8.7 (126) | — | 7.8 (114) | 7.1 (103) | **5.8 (84)** |
| 2500–3000 | 8.1 (118) | 7.3 (106) | 7.3 (106) | 6.9 (101) | **5.3 (76)** |
| 2000–2500 | 7.8 (114) | 7.1 (102) | 7.1 (102) | 6.8 (99) | **4.5 (65)** |
| 1600–2000 | 7.6 (111) | 6.6 (96) | 6.7 (97) | 6.3 (92) | **4.1 (59)** |
| 1200–1600 | 6.7 (97) | 6.5 (94) | 6.4 (93) | 4.8 (70) | **2.4 (35)** |
| 500–1200  | n/a | 6.1 (88) | 6.4 (93) | 4.1 (59) | **2.25 (33)** |

(Cold 500–1200 cell = 2 prime-transient samples; ignore.)

### What the surface means (all normal)
- **Monotonic temp scaling.** At fixed RPM, pressure falls as oil thins with heat
  (2500–3000 RPM: 8.1 bar cold → 5.3 bar hot). Healthy viscosity behavior.
- **Relief valve working, with margin.** Hot, pressure plateaus at **~6.0–6.3 bar
  (88–92 psi) above ~3500 RPM**, flat to redline → pump makes more than the engine
  needs and rides the relief. Cold, thick oil overruns the bleed and the relief lets
  it climb to **~9.1 bar (132 psi)** — relief-limited, not runaway.
- **Hot idle (~950 RPM): ~2.2–2.5 bar (32–36 psi) typical; lowest sustained ~1.4 bar
  (21 psi).** No collapse, no hunt.

### Evaluation — appropriate, on the robust side
- Rule of thumb (10 psi/1000 RPM): need 9.5 psi idle → 60 psi @6000; have 33 → ~90.
  **2–3× over the minimum everywhere.**
- Toyota 2JZ FSM (general knowledge, not repo-backed): idle ≥0.3 bar (have ~7×);
  3000 RPM 2.5–4.9 bar → have 5.3 bar (at/above top of band).
- Only "high" point is ~9 bar cold at RPM — relief-limited, within 2JZ relief
  allowance, and the usual reason to warm oil before high RPM (filter/cooler/line
  stress). No action needed; it's the safe direction.

## Start-up oil fill — revolutions, not seconds (2026-09-29)

Measured per start: first RPM > 50 → `Engine oil pressure` ≥ 1 bar at the sandwich-plate tap
(script: `supra/notes/oil_fill/opfill.py`; logs in `EMU_BLACK_V3\Supra`).

| log | CLT | crank → 1 bar | catch (>800) → 1 bar | crank revs to 1 bar | peak RPM before oil |
|---|---|---|---|---|---|
| allchannels_smoothclt (09-29) | 26 | 3.92 s | 1.52 s | 47 | 1815 |
| fullchannels (09-19, t 715) | 52 | 4.92 s | 0.92 s | 54 | 2071 |
| drivehome | 61 | 3.56 s | 1.40 s | 43 | 1782 |
| 20260524_1301 (t 389, short restart) | 28 | 0.68 s | 0.16 s | 6 | — |
| 20260524_1301 (t 865, hot restart) | 96 | 0.72 s | still cranking | 2 | 246 |

- After a soak the tap needs **~43–54 crank revolutions** whatever the RPM path. That is a
  drained volume (filter/plate/galleries) the pump has to refill; a quick restart with the
  circuit still full shows pressure in 2–6 revs.
- The fill is volume-limited, so it is fixed in **revs**. More RPM shortens the seconds but not
  the number of revolutions turned before oil arrives — the quantity that matters for the
  bearings and cam journals.
- In all three soaked starts the entire afterstart flare (peak 1782–2071) happened **before**
  the tap saw pressure; in 09-29 pressure arrived at the RPM trough (86.9 s, 1155 rpm) and went
  straight to the cold relief (≈7.5 bar at 1400 rpm).
- Consequence: `idleAfterstartRPMincrease` does not prime the oil system on this car. Once
  pressure is up it sits on the relief cold, so extra RPM adds no oil delivery either.

## Protection config — currently DISABLED
- `oilPressureCutEnable = 0`, `minOilPressureToDeliverFuel = 0`, `oilPressureFailSafe = 0`.
- `oilPressureCutTbl` = flat 8 (12 RPM bins), `oilPressureCutDelay = 300`,
  `oilPressureCutRestartTime = 5`, `oilPressureStartDelay = 5`,
  `oilPressCutDisableWhenOilpSensorFails = 0`.
- Sensor is installed and reliable, so a conservative low-OP warning/cut floor
  (below the ~1.4 bar hot minimum the engine never actually dips under) is available
  as cheap insurance. Present as an option — not a standing recommendation.
