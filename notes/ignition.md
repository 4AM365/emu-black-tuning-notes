# Ignition — EMU Black settings and the principles behind them

> **Software page:** *Ignition*. Full symbol catalog: [tune_feature_tree.md → Ignition](tune_feature_tree.md). **Knock** is a separate software page → [knock_sensors.md](knock_sensors.md).

The dedicated ignition document, organized like [idle.md](idle.md) and [fueling.md](fueling.md):

- **Part 1 — Settings**: one block per EMU Black ignition table — what it is, how to set it, how
  it fails, where the deep reference + live values live.
- **Part 2 — Principles**: the combustion-timing facts that set what every cell wants.

> **Deep reference.** [timing.md](timing.md) is the full ignition reference — vocabulary, the
> theoretical MBT tables for 238°/264°/272° cam durations (E0 + E100), and the detailed
> cruise/boost/VVT methodology. This hub summarizes the principles and maps them to EMU tables;
> go to `timing.md` for the data tables and step-by-step methodology.

> **Car-specific values live in the build working docs**, not here. For the reference build see
> [`supra/notes/`](../supra/notes/) — esp. [`timing_targets.md`](../supra/notes/timing_targets.md)
> and [`my_car.md`](../supra/notes/my_car.md).

---

# Part 1 — Settings (one block per EMU Black ignition table)

### Base ignition — `ignTable` / `ignTable2`

- **What it is.** Base spark advance, pump (`ignTable`) and ethanol (`ignTable2`), blended by
  ethanol content. Indexed `mapBins` × `rpmBins` (same axes as the VE tables).
- **How to set it.** Target MBT where the fuel allows, KLSA where it doesn't (I1). Shape follows
  the U-shape vs RPM, ~2°/30 kPa down across MAP, +timing up the RPM axis. Find cruise MBT
  **experimentally with an EGT sensor** (lower EGT → closer to MBT; rising MAP at constant pedal
  confirms a torque gain; degrading lambda stability means you've gone too far). Build a shallow
  **cruise plateau** (~1° total across the narrow cruise MAP band) so small MAP wander doesn't
  translate to torque roughness. Walk up boost timing in **1° steps** on per-cylinder knock + EGT.
  Use the theoretical MBT tables in [timing.md](timing.md) for *shape*, not as safe-to-run values —
  subtract knock retard per fuel/CR/charge-temp. Lock VVT before tuning (I5).
- **Failure modes.** Over-advance → torque loss + high EGT + knock/preignition; the knock-band
  baseline walks if cylinders aren't uniform (I4). Cruise timing that varies across the band →
  perceived roughness.
- **Live values / deep reference:** [timing.md](timing.md), [supra/notes/timing_targets.md](../supra/notes/timing_targets.md).

### Flex ignition blend

- **What it is.** The ethanol-content blend between Table 1 (E0, conservative) and Table 2 (E100,
  aggressive). Axis = ethanol %; its shape sets how fast authority shifts to Table 2.
- **How to set it.** Steep transition 0–50% ethanol (knock-resistance gain is front-loaded),
  flatter tail above 50% (e.g. ~14%/86% at E62.5, 0% Table 1 by ~E75). **Do not dial timing by
  reshaping the blend** — when you need more timing, advance Table 2 values; the blend multiplies
  the delta. The blend scalar is **< 1** at any partial ethanol, so a given Table 2 advance
  delivers proportionally less at the wheel — multiply the Table 2 delta by the blend fraction at
  your working ethanol % when stepping values.
- **Failure mode.** Knock margin compresses fast as ethanol content drops (partial fill, supplier
  variation) — a flex sensor **plus a conservative fallback blend** is mandatory insurance.
- **Live values:** build doc (blend curve, per-fuel boost ceiling).

### Knock control → its own Software page

EMU treats **Knock sensors** as a separate top-level page, so knock detection setup and the
knock-as-combustion-quality reading method now live in **[knock_sensors.md](knock_sensors.md)**.
Timing tuning leans on it directly: walk boost timing up in 1° steps while watching per-cylinder
knock + EGT, and remember knock voltage is a **boost-region** tool (use RPM CoV at idle,
[idle.md → P4](idle.md)).

### Idle ignition

- **What it is.** The fast idle lever — `idleIgnitionTargetTbl` + Min/Max torque-angle swing, on
  top of base `ignTable`/`ignTable2`.
- **How to set it.** Set base idle advance **below MBT** for recovery reserve, keep it flat, keep
  the PID window narrow; knock down a high hot idle with ignition retard (reversible), not air.
  This is an idle-system block — full treatment: **[idle.md → Idle ignition](idle.md)** and the
  fuel×cam range table in [engine_start.md](engine_start.md).
- **Live values:** build doc.

### Decel / overrun ignition retard

- **What it is.** Timing retard during overrun / the power-off transition.
- **How to set it.** Use **asymmetric** transition rates on overrun exit — fast enter (cut fast),
  **slow exit** (restore advance slowly) so the advance step doesn't stack with the re-fuel event
  and force the airflow PID to chase it. Decel retard can also soften the off-throttle "parachute"
  as a secondary tool. See [idle.md → Armed state / overrun](idle.md), [throttle_feel.md](throttle_feel.md).
- **Live values:** build doc.

---

# Part 2 — Principles

## I1. MBT, CA50, KLSA — the goal of timing

The goal is to place **CA50** (where 50% of fuel has burned, the point of greatest charge-gas
expansion) at the crank angle of maximum mechanical advantage — that's **MBT** (Maximum Brake
Torque). A good MBT indicator is **CA50 at ~8° ATDC**. Too advanced and peak pressure arrives so
early the piston fights the crank — torque falls, EGT rises (the inefficiency shows up as heat).
On a stable fuel you can run MBT everywhere; on a knock-limited fuel the mixture transitions to
detonation before MBT, so you retard to the **Knock-Limited Spark Advance (KLSA)**. Two fuel
properties to keep separate: **octane** sets resistance to detonation (end-gas autoignition);
**burn rate** sets how much advance reaches MBT (ethanol burns such that it needs ~3–8° *more*
timing to reach MBT). On ethanol the problem inverts — it barely knocks, so the limit becomes how
much torque the engine can physically take. Full vocabulary + theory: [timing.md](timing.md).

## I2. Knock, preignition, detonation — and the U-shape

- **Knock / detonation**: end-gas igniting from multiple points *after* the spark — the pressure
  shock wave damages crowns, ring lands, rod bearings.
- **Preignition**: a hot chamber lighting the mixture *before* the spark — artificially advancing
  timing, runaway and far more destructive (LSPI is the small-turbo low-RPM-cruise version).
- **MBT timing follows a U-shape** across the rev range for a given MAP; across MAP you lose
  ~2°/30 kPa (peaks near 20 kPa); across RPM you add timing (the piston outruns the flame front).

## I3. How timing demand changes with cam, fuel, and load

The same lever moves with what's in the cylinder:

- **More cam overlap → more idle/low-load timing.** Exhaust reversion dilutes the charge, slowing
  flame-front velocity, so the burn must start earlier to keep CA50 near MBT (idle detail:
  [idle.md → Idle ignition](idle.md), [engine_start.md](engine_start.md)).
- **More boost → less timing.** Higher cylinder pressure raises knock propensity, so KLSA falls;
  each increment of boost demands less advance on a given fuel.
- **Cooler/higher-octane fuel → more timing.** Ethanol carries more advance across boosted cells,
  largest gain in lighter-load VE cells; peak anti-knock by mixture is ~E60.
- The fuel×cam **idle/low-load starting ranges** (10–12° pump/stock up to 19–22° ethanol/big-cam)
  live in [engine_start.md](engine_start.md); cruise can reach the high 30s (pump) to
  low 40s (cammed ethanol); boost MBT for a 4-valve DOHC I6 is generally low-20s° BTDC.

## I4. Knock-band variance is a cylinder-uniformity proxy

A knock sensor is a band-pass piezo accelerometer; the ECU windows each event and measures energy
in the knock band vs a rolling baseline. Two signals live there: **spikes** (true/incipient knock)
and **baseline wander/"grumble"** (the *variance* of the per-event floor). Maldistribution makes
the baseline **walk**: lean cylinders burn faster/hotter (sharper dP/dθ → more HF content) and sit
nearer the autoignition edge (intermittent trace knock that lifts the floor without crossing the
spike threshold), and their higher COV-of-IMEP makes the windowed energy oscillate. So **watch
knock-channel variance, not just spike count** — a flat, smooth baseline at max power is the
acoustic fingerprint of all cylinders doing the same thing every cycle (it went dead-smooth after
per-cylinder fuel trims). Full mechanism: [knock_sensor_baseline_vs_cylinder_uniformity.md](knock_sensor_baseline_vs_cylinder_uniformity.md).

## I5. VVT couples to ignition — re-verify MBT when cam advance changes

VVT cam advance changes both volumetric efficiency (MAP rises at constant pedal → you index a
different VE/timing cell) and MBT itself. On a single-cam VVT-i system advance and overlap move
together, so the direction depends on load: **light load** (EMAP > IMAP) more advance pushes
residuals back into the intake → more dilution → MBT toward **more** advance; **boost**
(IMAP > EMAP) more advance scavenges residuals out → MBT toward **less** advance; and advancing
intake-valve-closing raises low-RPM effective compression → MBT toward less advance. **Lock cam
advance per cell before pulling for MBT** — otherwise timing chases a moving VVT target. Re-verify
ignition at any cell where you change cam advance. Full breakdown: [vvt.md](vvt.md).

---

## Hardware reference

- Coils, dwell tables, and Toyota/Denso COP part numbers are reusable hardware reference (not
  per-car calibration): [denso-coils.md](denso-coils.md). Higher coil voltage charges faster for
  the same energy; the build's specific coil is in [supra/notes/my_car.md](../supra/notes/my_car.md).

## Related documents

- [timing.md](timing.md) — full ignition reference: MBT tables, cruise/boost/VVT methodology (I1–I3, I5)
- [knock_sensor_baseline_vs_cylinder_uniformity.md](knock_sensor_baseline_vs_cylinder_uniformity.md) — knock variance as uniformity proxy (I4)
- [knock_voltage_cov_combustion_stability.md](knock_voltage_cov_combustion_stability.md) — knock-chatter CoV method
- [vvt.md](vvt.md) — VVT mechanism + timing coupling (I5)
- [idle.md](idle.md) — idle/decel ignition (the fast PID lever)
- [fueling.md](fueling.md) — λ targets, charge cooling, per-cyl trim (sets what timing each cell can take)
