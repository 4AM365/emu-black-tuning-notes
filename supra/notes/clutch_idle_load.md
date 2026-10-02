# Clutch load at idle — magnitude, variability, and why it is not a feed-forward candidate

Source: `omg.csv` (2026-08-24, 1022 s, 25 Hz, all channels), tune `omg.xml.emub3`
(2026-08-24 18:42, exported after the log). Companion: [[idle_drive_wobble]],
[[airflow_actuator]], [[oil_viscosity_idle_airflow]].

## Question

Owner asked whether the clutch disturbance at idle is large enough to justify feeding
air forward, given that "clutch drag is so variable."

## The data does not support a statistical answer — say so first

In 539 s of settled ACTIVE idle (idle state 2, pedal closed, VSS < 3):

| clutch state | settled idle time |
|---|---|
| released (pedal up) | **530.4 s** |
| pressed (pedal down) | **1.4 s** |

The pedal is essentially never held down at settled idle in normal use — the car is
either driving or stopped in neutral. **Any matched steady-state comparison is
impossible from this log**, and probably from any normal-driving log. All conclusions
below rest on transients.

Gate note: `PPS` has a non-zero closed-pedal floor in this log (idle p99 ≈ 1.8, with
excursions to ~3 at rest). A `PPS == 0` gate silently drops most idle samples. Gate on
`PPS < 1` and verify against the per-log distribution. Separately, `Vehicle Speed`
carries single-sample glitches (spurious 25–158 km/h at idle RPM — see the driven-axle
glitch in the same log's health sweep), so a `VSS.max() > n` gate over a window will
reject good events. Use a median or a robust statistic.

## Two distinct clutch effects, an order of magnitude apart

**1. Neutral, disc free (the common case).** Pressing the pedal decouples the gearbox
input shaft and its oil churn from the crank. Small unload.

Clean at-idle edges (ACTIVE both sides, pedal closed, stationary, hot, no A/C
transition in window, ±0.8 s):

| t (s) | direction | ΔRPM (0.8 s mean) | peak excursion | airflow-PID response |
|---|---|---|---|---|
| 987.08 | press | +13 | +22 | −0.44 |
| 900.96 | press | +10 | +26 | −0.81 |
| 988.52 | press | +11 | +45 | −0.69 |
| 987.80 | release | −25 | −35 | +0.37 |

Press unloads by **15–45 rpm**, release loads by **25–35 rpm**. The airflow PID answers
with **under 1 point** of a ±25 authority (`idleAirPIDOutMin/Max`, read from the current
tune). Ignition correction moves ~0.5°.

**2. In gear, stationary, pedal down — clutch drag.** The disc is dragged against a
held output shaft; residual friction is a real parasitic torque. One observation only:
t = 184.04 → 191.72 (7.68 s, CLT 63–66, stationary).

| segment | RPM err vs target | `Idle air %` | airflow PID | `Idle ignition correction` | `Ignition Angle` |
|---|---|---|---|---|---|
| before (pedal up) | +11 | 48.96 | −1.68 | −1.21 | 17.25° |
| during (pedal down) | **−50** | **54.42** | **+3.44** | **+2.94** | **21.42°** |
| after (pedal up) | +35 | 52.77 | +1.81 | −1.35 | 16.75° |

≈ **+5.4 airflow points and +4.2° of ignition** spent, and still 50 rpm under target.
**Confounded:** `PPS` ran 0.7–4.0 % through part of the hold, and the target was
oscillating on the ramp-offset re-arm. Treat as an order-of-magnitude indication, not a
calibration number.

## Scale reference

Measured on the same car, same log: the A/C compressor load step is **12–14 airflow
points** and **≈350 rpm** of sag (see the A/C section of [[idle_drive_wobble]] once
merged). The neutral clutch disturbance is roughly **1/15th** of that.

## Conclusion — do not feed the clutch forward

1. **The repeatable component is too small to calibrate.** Under 1 airflow point of PID
   response is inside the loop's own noise; a feed-forward table would be fitting jitter.
2. **The large component is the non-repeatable one.** Clutch drag depends on selected
   gear, clutch and gearbox oil temperature, and wear state. Feed-forward requires a
   disturbance that is predictable from a logged input; drag is not. The owner's own
   instinct ("with the clutch drag being so variable I don't know if it makes sense")
   is correct and is the deciding argument.
3. **The existing mechanism already covers it.** `idleClutchEnablesClosedLoop` is
   enabled, so pressing the pedal forces closed-loop idle and the PID is live for the
   event. That is the right lever and it costs nothing.
4. **`idleClutchTrgtRPMIncrease` would be inert anyway** while `idleTargetBins` floors
   above the commanded hot target — a target bump smaller than the first bin spacing
   buys zero extra base airflow because the lookup clamps to the same row. See the
   axis-clamp analysis in [[idle_drive_wobble]].

**Contrast with A/C, which IS a feed-forward candidate:** binary, ECU-scheduled, and
announced ~900 ms ahead by the compressor engage delay. Spend the effort there.

## Reusable method

- Separate *neutral* from *in-gear* clutch events before pooling. They are different
  physical loads and differ by ~5× in magnitude.
- Report the disturbance in **airflow points of PID response**, not just rpm — that is
  what decides whether a feed-forward is worth building, and it normalises against the
  configured authority.
- Before proposing any idle feed-forward, check the settled-time budget in each state.
  A load the engine never actually sits under does not need a table.
