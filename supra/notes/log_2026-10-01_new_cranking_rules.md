# Log `new_cranking_rules.csv` (2026-10-01) — fw 3.071 migration, A/C at idle, cold start

Source: `EMU_BLACK_V3\Supra\new_cranking_rules.csv` (binary twin `LogAutosave\20261001_0821_28.emublog3`).
25 920 samples @ 25 Hz, 1044 s. `Firmware version` channel = 71 (3.071) for the whole log. E14, ambient ≈ 26 °C
(cold soak: CLT 27 / IAT 26 / Pre-IC 26 agree at key-on). Tune: `Supra.xml.emub3` exported 08:51, two minutes after
the log ended — it describes the **end** state. Live edits: `Data changing` 34 spans (65–1023 s), `Making permanent`
14 spans (76.6 … 1026.5 s). Log-derived values below are authoritative for this log; XML values are the 10-01 export's.

---

## 1. Firmware 3.059 → 3.071: what the "Cannot find symbol" warnings mean

The 72 warned symbols/tables are **exactly** the symbols present in the 10-01 export and absent from the 09-19 (3.059)
export. They are new 3.071 features; each sits at its firmware default in the new export. None was ever set in the
old project, so nothing of the tune was dropped. ECU logs fw 71 throughout, so the ECU itself runs 3.071.

Symbols that went the other way (in 3.059, gone in 3.071) — the ones that matter:

| Removed | Replaced by (10-01 export) | Consequence |
|---|---|---|
| `revLimit1CutPercent`, `revLimit2CutPercent` (were 90) | `revLimit1/2CutPattern` (0), `revLimit1/2FuelCorr` (0) | Old 90 % cut setting has no carry-over. Check the limiter cut in the UI. |
| `wboLambdaTable`, `wboIPNormTable` (internal WBO Ip → λ curve) | `wboRcal` (200) | The internal wideband's conversion changed with the update. A λ reading shift across the update is possible independent of any wiring change. Cross-check with the planned CAN lambda module. |

Also changed in the export, checked against the log: `mapAnalogIn` 0 → 14 and `cltSensorCal` 5 → 0. Readings are sane
(CLT/IAT/Pre-IC agree at cold soak; key-on MAP 98 kPa), so treat these as enum renumbering, not a broken input.

New 3.071 symbols with a direct use here: `switch1DebounceTime` / `switch2…` / `switch3…` (default 8, **units not
verified**) — see §2c. `idleArmedAirFlowCLTCorr` / `idleInactiveAirFlowCLTCorr` (all 0 = no effect),
`idleAirPIDDisableFunction` (0 = none), `dbwEnableSafety` (0 = off).

## 2. A/C at idle

Settings in force (log-derived where possible): A/C request = `Switch 1` (`acActivation`), custom airflow correction
activated by the A/C (`idleDCCorrActivationInput` 254), `idleCustomCorrection` row 1025 = +16, `acTimeToEngage`
varied during the log, final 600 ms. **`acMinRPM` ran at ≈ 800 during the log** (no clutch-on sample below 801;
gate drops at 801–820); the 10-01 export reads 1800 again.

### 2a. Measured A/C airflow need (steady state, hot, idle ACTIVE, |RPM − target| < 40, clutch state held > 4 s)

| Era | target | A/C off: air / PID / MAP | A/C on: air / PID / custom / MAP | Δ air |
|---|---|---|---|---|
| custom corr live (t > 860) | 1025 | 20.9 / −7.6 / 35.6 | 35.1 / −9.2 / +16 / 41.1 | **14.2** |
| before custom corr (640–829) | 1025 | 19.9 / −8.4 / 36.1 | 36.1 / +7.9 / 0 / 41.0 | 16.2 |
| whole log, weak off-reference | 1225 | ≈ 32–34 (t 380–430, few samples) | 49.4 / +17.1 / 0 / 40.0 | ≈ 15.5–17 |

ΔMAP ≈ +5.4 kPa at 1025 rpm. Sanity check: 5.1 kPa × 3.0 L × ηv 0.85 / (R·T) → ≈ 0.14 g air/cycle → at idle
indicated efficiency ~0.25 ≈ 9 N·m — an ordinary compressor torque. The +16 cell over-feeds by ~1.8; the PID sits
1.6 lower with A/C on than off.

A/C off, hot idle at 1025: λ 0.892 vs target 0.901, STFT +0.8 % — the 10-01 VE lean-out is on target at this cell.

### 2b. Why idle with A/C cycles: request glitches restart the engage timer

Edge-level result (all clutch drops in Idle ACTIVE): request glitch visible in log (1–2 samples low) 9, invisible
blip (clutch off exactly `acTimeToEngage` with `Switch 1` steady and no other gate moving) ~8, RPM gate ~9, real
request-off 7.

Sequence, repeated dozens of times (e.g. t 945.0, 959.2, 962.2):
1. `Switch 1` drops for ≤ 40 ms → clutch off, engage timer restarts. The custom correction **stays on** (it follows
   the A/C gate, which re-arms immediately — it switches on ~`acTimeToEngage` *before* the clutch on a fresh request).
2. +16 air with no compressor load → RPM 1030 → 1260 in 0.4 s → idle ignition hits −7 → the airflow PID (slaved to
   ignition error, mostly P) dumps ~10 air-% in 0.6 s (−7.7 → −18.8).
3. Clutch re-engages into that air deficit → RPM 1260 → 800 → ignition +11.5, PID recovers.
4. If the dip reaches ≈ 800 the `acMinRPM` gate drops the clutch (no hysteresis), and the loop restarts at step 2.

Fresh engagements (no preceding glitch) are fine: custom-corr era dips ~75 rpm (914.3, 930.4 → 946–950);
pre-custom-corr fresh engagements dipped ~230 (to 786–804). The feed-forward works; the glitches defeat it.

### 2c. Why the request line is noisy

Glitch rate with the request on: **2.4 /min clutch pedal released, 68.6 /min pressed** (28×). The pressed bias from
`ac_request_input_noise.md` survives the 08-29 sensor-ground fix at a lower level. Mechanism (pre-"P" rev F switch
inputs, `docs/emu-black-help/Sensorsandinputs.md`): these inputs accept **sensor ground only**. The A/C amplifier's
request output pulls the pin to the amplifier's own ground (body side), so `Switch 1` itself is the input fed by a
non-sensor-ground source. Ground offsets between body and EMU sensor ground, plus the shared measurement path
disturbed by the clutch switch, flip a marginal reading for one sample.

The OEM ECU's input (`AC1`, DI-314) reads ON 0–1.5 V and OFF 7.5–14 V: a battery-level pull-up with a ~6 V dead band.
An OEM input of that kind normally also has RC filtering and software debounce (model knowledge; no OEM ECU input
schematic in the repo). The EMU switch input has none of that margin and no configured pull-up.

Levers: `switch1DebounceTime` (new in 3.071; confirm units in the UI) sized above the observed glitches (≤ 80 ms
visible, plus shorter invisible ones) — real request changes come seconds apart, so a debounce of a few hundred ms costs
nothing. Hardware: a relay or opto driven by the amplifier output whose contact switches **EMU sensor ground** onto
`Switch 1` satisfies the rev-F rule and isolates the grounds.

**Clutch switch (`Switch 3`) chatter, for sizing `switch3DebounceTime`** (Will, 2026-10-02, plans to debounce it).
Run lengths across `new_cranking_rules.csv`, `allchannels_smoothclt.csv` (09-29) and `fullchannels.csv` (09-19):
chatter = 0.04–0.20 s, almost all brief *opens* during a held press (09-29: 15 of 18); shortest genuine presses
0.40–0.48 s (quick shifts; 09-19 has four 0.24–0.28 s presses of unclear origin); shortest genuine release 0.72 s.
Window that separates them: ~0.25 s. Debouncing `Switch 3` cleans the clutch *logic* only — the `Switch 1` glitches
it induces are electrical (rev-F shared input path) and are untouched by it.

**Brake (`Switch 2` → Fn 2 "Brakeinv" → `brakePedalInput` 21) is clean:** one 40 ms glitch in 09-19's 1943 s, none in
09-29 or 10-01; shortest real press 0.32 s. Its main consumer, stuck-throttle protection, needs the condition for
1500 ms, so a one-sample glitch can't act. No debounce needed.

### 2c′. Release side: off-delay the clutch behind the air (proposal, 2026-10-01)

On a real request-off the clutch and the custom correction drop on the same sample. The load leaves at once; the
air cut takes the air-path lag to reach the cylinders → flare (858.44: +156 rpm at 0.44 s, airflow PID to −12.6).
The fix is to make release the mirror of engage: drop the air first, drop the clutch one air-lag later.

`userFunctions` in the 10-01 export uses Fn 1–6 (fp2, Brakeinv, rpadlnch, rpadroll, both_pad, lpad+psi); Fn 7–12 are
free. Functions run at 25 Hz in order F1 → F12, so a later function sees an earlier one's value from the same cycle.

| Fn | Operator | True delay | False delay | Drives |
|---|---|---|---|---|
| Fn 7 `ACreq` | Is True `Switch 1` | debounce (≥ ~0.1–0.2 s) | debounce | `idleDCCorrActivationInput` |
| Fn 8 `ACclt` | Is True `Fn 7` | 0 | D ≈ 0.5–0.6 s | `acActivation` |

- Engage: Fn 7 and Fn 8 rise together; the correction leads the clutch by `acTimeToEngage`, as now.
- Release: the correction drops at Fn 7; the clutch holds for D, then drops as the reduced air arrives.
- Glitch shorter than the debounce: nothing moves. Fn 7's delays replace `switch1DebounceTime` if that one's units or
  range fall short.
- D start value: the engage data put the effective lag a little under 0.6 s (0.52 s lead flared +57 before the clutch
  closed). Tune from release events: flare → raise D; dip before the clutch drops → lower D.
- Unverified: that `acActivation` and `idleDCCorrActivationInput` list Fn 7/8 (EMU help says function results can
  activate strategies). Holding the compressor D after the amplifier withdraws is negligible against its protections,
  which act on seconds (3 s lock test, pressure hysteresis).
- RPM/TPS gate drops still cut the clutch instantly with the correction on; with the request debounced and
  `acMinRPM` ≈ 800 they should be rare.

### 2d. Physics of the A/C airflow correction

- Compressor (fixed displacement assumed, unverified) torque at fixed speed ∝ η_v·[(P_d/P_s)^((n−1)/n) − 1],
  R134a assumed, P_s at 0 °C evaporating, P_d = saturation at ambient + 20 K condenser approach, n = 1.1, 4 %
  clearance. Ratio vs 26 °C ambient: 10 °C 0.71 · 20 °C 0.90 · 30 °C 1.06 · 40 °C 1.19 · 50 °C 1.29 (insensitive to
  approach 15–25 K and n 1.05–1.15 to ±5 %). Model knowledge, not corpus-backed.
- Throttle is choked at idle (MAP/baro ≈ 0.37–0.41 < 0.528), so mass flow ∝ plate area ∝ `Idle air %` above
  break-away. Constant compressor torque needs constant extra air per cycle → Δ air-% ∝ RPM. The 1225 point
  (≈ 15.5–17 measured vs 17.0 predicted) is consistent but weak (its A/C-off reference is from earlier, IAT 23–28).
  What scales is the *airflow*, not the load: compressor torque is roughly speed-independent (OEM torque-based ETC
  books the A/C as a fixed torque request — Banish, `corpus/engine_management_advanced_tuning.md` ~l.2597, "15 ft-lbs").
  Two effects pull the RPM ratio below ∝N (model knowledge): suction pressure falls as compressor speed rises, and the
  plate's flow gain per air-% rises as it opens (log bins: 0.72 → 0.47 air-%/unit ṁ). Expect ×1.0–1.2 from 1025 to
  1250; +17 is the top (over-air-safe) end. Rows ≥ 1500 are unvalidated extrapolation.
- Ambient sensitivity ≈ +1.6 %/K of the A/C term near 26 °C → ≈ 0.23 air-%/K at 1025 (≈ 10 on a 10 °C day, ≈ 17 at
  40 °C). Likely an underestimate on hot days: the model holds suction pressure fixed, but a hotter cabin load raises
  it (denser suction gas, more mass per rev), and idle condenser approach widens with recirculated hot air.
- **IAT is not an ambient proxy at idle on this car.** In this log IAT climbed 22 → 46 °C (Pre-IC 25 → 54) at constant
  ambient ≈ 26 °C, and the measured need did **not** follow IAT (16.2 at IAT ~35, 14.2 at IAT ~43). An IAT slope
  derived from the head-pressure model would have mis-predicted by ~4 points in the wrong direction here.
  `Ambient temperature` channel reads −40 (no sensor), `AC Pressure` / `AC EVAP temp.` not configured. Head pressure
  (an A/C high-side transducer) is the physically correct axis; a real ambient sensor is second best.

## 3. Cold start (CLT 27)

**Attempt 1 (t ≈ 4.6–10.4)** cranked 170–210 rpm, fired to 300–480 rpm and hovered there 4.5 s without reaching
`crankingThreshold` 750. Pedal at 9.48 s (`DBW Target source` 2 → 0) is deliberate — masked. Engine stopped at 10.4.

**Attempt 2 (t 98.4)**: first rev → Cranking exit in **0.4 s** (180 → 561 → 731 → exit at 98.96).

At matched cells (VE 58.5 at the 500 rpm / 93 kPa cell, MAP 94, 10.7 V, inj cal 1.406) cranking PW was 3.23–3.32 ms
in attempt 1 and 3.50–3.63 ms in attempt 2: the edit between them (t 65–77) raised the cold cranking dose ~5–10 %.
The VE lean-out had already cut that cell 63.4 → 58.4 (−7.9 %), which silently cut every cranking cell by the same
7.9 % (cranking dose = VE eq × (1 + cranking %)). Attempt 2 also had attempt 1's fuel film in the ports, so a single
start doesn't separate the two causes.

**Run-up, overshoot, PID wiggle (attempt 2):**

| t | RPM | MAP | Ign | Air % (DBW tgt) | state |
|---|---|---|---|---|---|
| 98.96 | 731 → exit | 77 | 24 lock | 80 (5.5) | Afterstart, delay 0.40 s (`idleControlAfterstartDelay` 4 = 0.1 s/count, confirmed) |
| 99.36 | **1991 peak** | 37 | 24 lock (table 24.5) | 80 | → ACTIVE at the peak |
| 99.36–99.68 | 1991 → 1629 | 33–35 | 24 lock | 67.5 → 65.0 (4.7), PID −8.9 → −11.5 | ACTIVE, ign PID −8.5 |
| 99.64–99.76 | 1666 → 1532 | 33–35 | 24 → 9 in 0.12 s (lock end 0.6 s, restore 48) | | |
| 100.08–100.2 | **1275 trough** | 40 | 27 | 81.5 (5.5), PID +5.8, ign +7.5 | |
| ~100.8 | 1425 settled | 40–41 | 19 | 77–80 | |

- Cranking airflow at CLT 27 (80 %) equals the sustaining airflow at 1425 (76–80 % over the next 10 s). The overshoot
  is manifold discharge (MAP 98 → 37 by the peak) plus the 24° lock (+5.5° over the 18.5° idle target), not excess
  steady air.
- The wiggle is the controller, not the engine: ACTIVE engaged at the RPM peak with MAP already at or below
  equilibrium, the airflow PID cut ~15 air-% and the lock release dropped 15° of ignition within 0.4 s of each
  other, stacking onto a decay that was already happening → −150 rpm undershoot → both PIDs reverse.
- This start broke the rule in `notes/engine_start.md` ("Ignition lock ≤ afterstart delay"): lock 15 × 0.04 =
  0.60 s against delay 0.40 s. For the 0.24 s overlap the idle ignition PID asked for −8.5° that the lock never
  delivered, and the airflow PID (slaved to that ignition error) cut air for it. The lock angle is not the problem:
  `Ignition From Table` ran 18.5–25.5° over the same run-up, so 24° is within ~1° of table from ~1400 rpm up.
- `DBW Target source` = 2 (idle) from 98.56 on; no handoff or blend. The only throttle event is the PID close
  (5.5 → 4.7 % TPS) at ACTIVE entry.

**Holding position longer (Will's proposal, 2026-10-01).** At a choked throttle, charge per cycle ∝ ṁ/N: overspeed
cuts torque per cycle while friction rises, so a held plate is a stable equilibrium at the RPM where plate airflow =
sustaining airflow. With the cranking airflow matched to sustaining, extending `idleControlAfterstartDelay` past the
overspeed decay lands on target without the PID, and ACTIVE engages near zero error. `Ignition From Table` during the
run-up was 18.5–25.5°, so ignition outside ACTIVE stays near the lock angle.

**The hot `idleCrankingDC` bins are correct as they are — do not lower them** (correction from Will, 2026-10-01, after
this note first called the hot bin "too high"). A CLT axis cannot see oil temperature. At CLT ≈ 94 a restart can have
oil anywhere from still warming (needs ~34 %) to fully heat-soaked (needs ~20 %), and the bin is sized to the **upper
envelope** on purpose: over-air during warm-up is acceptable, surprise starvation is not
(`oil_viscosity_idle_airflow.md` §14.6, `notes/oil_temp_vs_coolant_airflow_reference.md`, `notes/idle.md` → "Do not
'fix' this by flattening the hot end"). The ~21 % measured in this log is the hot-oil floor, not the bin's target.

Consequence for a longer hold: on a hot-oil restart the held position is up to ~14 points over-aired, so the engine
sits above target for the whole hold and the PID then trims it down. 14 points is inside the airflow PID's negative
authority (`idleAirPIDOutMin`, 10-01 export), so it is the envelope design's accepted cost, but the hold length sets how
long the high plateau lasts. A cold start is unaffected (cranking airflow ≈ sustaining at CLT 27).
