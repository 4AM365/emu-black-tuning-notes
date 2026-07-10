# Fueling — EMU Black settings and the principles behind them

> **Software page:** *Fueling*. Full symbol catalog: [tune_feature_tree.md → Fueling](tune_feature_tree.md). Cold-start enrichment is on [engine_start.md](engine_start.md); overrun fuel cut on [overrun.md](overrun.md); flex blend selectors on [tables_switching.md](tables_switching.md).

The dedicated fueling document, organized like [idle.md](idle.md):

- **Part 1 — Settings**: one block per EMU Black fuel table — what it is, how to set it, how it
  fails, where the live values + full method live.
- **Part 2 — Principles**: the fuel-model facts and combustion physics that make the table
  choices read as consequences. Car-agnostic and stable.

> **Car-specific values live in the build working docs**, not here. For the reference build see
> [`supra/notes/`](../supra/notes/) — esp. [`my_car.md`](../supra/notes/my_car.md),
> [`per_cylinder_trim_results.md`](../supra/notes/per_cylinder_trim_results.md),
> [`lambda_tracking_results.md`](../supra/notes/lambda_tracking_results.md), and
> [`mass_flow_estimator_quirk.md`](../supra/notes/mass_flow_estimator_quirk.md).

> **Deep-dives.** The method notes that derive these procedures in full are linked from each
> block: VE-from-log correction, the dose-proxy model, the idle-knee/smoothing method, VE-vs-MAP
> shaping, lambda-vs-load, the flex blend curve, per-cylinder trim, and lambda tracking.

---

# Part 1 — Settings (one block per EMU Black fuel table)

### Fuel-dose encoding (read this once)

- `veTable` / `veTable2`: **u12**, row-major, **scale 0.1** (raw 444 → 44.4 %). Width (MAP cols)
  × height (RPM rows) match `mapBins` × `rpmBins`. Verify the scale against the log VE channel
  before applying corrections.
- `mapBins` / `rpmBins`: axis values, scale 1 — span/count are build-specific, read from the
  project.
- `fuelTrim1..4Table`: **sbyte 5×5**, % direct, axes `fuelTrimRPM` × `fuelTrimLoad` (kPa).
- Flex blend tables (`tblsVEBlend`, `tblsFFLambdaBlend`): **ubyte**, 0.5% resolution.
- Checksums go stale after editing `data`; EMU recomputes on import. **Never guess conversion** —
  do per-cell math, verify one cell empirically. See the `emu-black-tune` / `emu-black-emubt-export` skills.

---

### Fuel-dose tables — `veTable` / `veTable2`

- **What they are.** The actual injected-fuel dose (F1), pump and ethanol, blended by ethanol
  content through `tblsVEBlend`. Indexed `mapBins` × `rpmBins`.
- **How to set / correct from a log.** Closed-loop steady cells: the wideband tracks target and
  STFT absorbs the error, so **read `Short term trim`, not lambda error**.
  `new_VE = old_VE × (1 + STFT/100) × (λ_actual/λ_target)`; in settled loop this reduces to
  ~`(1+STFT/100)`. Filter to genuine steady closed-loop samples
  (`Lambda is valid==1 & Short term trim==1 & Fuel Cut==0 & Overrun status<2 & ASE==0 & Warmup==0
  & |Acc. enrichment %|≤1`; note `Overrun status` baseline is **1**, not 0). Distribute each
  sample bilinearly, gate on accumulated dwell (~25 ≈ 1 s @ 25 Hz), clamp ±15 %/pass. Open-loop /
  accel cells: read **lambda error directly** (rising-RPM + TPS>10%); the lean region forms a
  diagonal band climbing up-and-right. **Apply the same factor to BOTH tables** to preserve their
  relative offset and keep `veTable2` valid for future ethanol fills.
  Full method: [ve_correction_from_log.md](../ai-analysis-skills/ve_correction_from_log.md), [ve_correctness_from_log_method.md](../ai-analysis-skills/ve_correctness_from_log_method.md).
- **Shaping with no log data.** The cam-resonance VE peak is an **RPM** phenomenon — stamp a
  known-good MAP column's RPM shape onto unmapped high-boost columns rather than interpolating
  *through* the peak. VE at higher MAP (same RPM) trends **flat-to-down** (EMAP backpressure,
  charge heating), so an upward dose offset into boost is the *safe* placeholder direction but not
  physics-derived — back the real offset out of measured lambda. Check the whole table with the
  `veTable × λ_target` air-VE proxy (must be smooth, no kink at the boost knee). Full model:
  [ve_vs_map_at_constant_rpm.md](../ai-analysis-skills/ve_vs_map_at_constant_rpm.md).
- **Smoothing — preserve the idle knee.** The idle/low-MAP corner has a **real nonlinear feature**
  (residual-gas knee on MAP + cam-inflection on RPM). A global low-order polynomial rounds it off
  and invites idle surge / tip-in hesitation. Use **delta-overlay**: smooth the *correction*
  (`final = base + smooth(autotune_delta)`), not absolute VE, so untouched cells stay at base.
  Extrapolate corrections **up** the RPM axis to the VE peak so you don't create a false double
  hump. Full method: [ve_idle_region_nonlinearity.md](../ai-analysis-skills/ve_idle_region_nonlinearity.md).
- **Failure modes.** Single-table autotune leaves `veTable2` stale (logs at low ethanol weight the
  pump table). Over-smoothing kills the idle knee. Don't validate idle VE against the mass-flow
  estimator (it overstates idle airflow ~10× — [idle.md → P1](idle.md)).
- **Live values:** [supra/notes/my_car.md](../supra/notes/my_car.md); machine-smoothed map is the newest/best generation.

### Lambda target — `lambdaTable` / `lambdaTable2`

- **What it is.** Tuning reference + **closed-loop STFT target only** (F1) — never a fuel
  multiplier. Fixed **8-column MAP axis**, pump and ethanol.
- **How to set it.** Spend bins where the curve bends (F2): idle/cruise points where the target is
  flat, a **dense cluster bracketing the MBT→protection knee** (a bin *on* ~130 kPa, bracketed
  100/130/160), ~3 coarse points across the linear rolloff, top bin on the `veTable` MAP boundary.
  Set two **full-boost endpoints** — a richer E0 (pump, no evaporative cooling) and a leaner E100
  (ethanol) — both inside the best-torque/protection band (typical high-boost pump λ ~0.72–0.80);
  let the flex blend interpolate. Don't confuse the full-boost endpoint with the boost-entry ramp;
  shape the 80–130 kPa transition columns for smooth torque, don't jump them to full-boost
  richness. Full derivation + literature basis: [lambda_target_vs_load.md](lambda_target_vs_load.md),
  [flex_fuel_ethanol_compensation_blend.md](flex_fuel_ethanol_compensation_blend.md).
- **Failure modes.** Changing it expecting an open-loop mixture change (it only moves the STFT
  target). A target change baked into VE as a workaround (a planned 0.02 λ ≈ 2% VE, but the
  permanent correction should come from measured lambda error, not a hand-subtraction).
- **Live values:** build doc (WOT endpoints, MAP axis).

### Flex blend curves — `tblsVEBlend` / `tblsFFLambdaBlend`

- **What they are.** The ethanol-content blend weighting between table 1 (E0) and table 2 (E100)
  for VE and for lambda target.
- **How to set it.** When EMU's `ethanolFuelScale` handles the stoichiometric fuel-mass change,
  **derive the blend from the fuel-scale table**, not by intuition:
  `table_1_weight(E) = 1 − ethanolFuelScale(E)/ethanolFuelScale(100)` (works in raw counts; the
  scale cancels). The curve is **nonlinear** (table-1 weight falls faster than ethanol % rises) —
  re-derive it, don't assume a straight line; round to 0.5%, encode ubyte. Use it for
  `tblsFFLambdaBlend` when the λ endpoint should advance with the same ethanol curve; use it for
  `tblsVEBlend` only when VE2 is intentionally tuned away from VE1 (identical VE models → the VE
  blend has no fueling effect). Full method: [flex_fuel_ethanol_compensation_blend.md](flex_fuel_ethanol_compensation_blend.md).
- **Cold-enrichment flex blends** (cranking/ASE/warmup) are **not** stoichiometric compensators —
  they only control how fast the ECU moves from the E0 to the E100 extra-enrichment endpoint. Cold
  enrichment pays the wall-film/vaporization tax, which is most ethanol-forward at **cranking**,
  less at ASE, least at warmup: `Warmup ≥ ASE ≥ Cranking` table-1 weight at the same ethanol
  content. Don't use one linear blend for all three.
- **Live values:** build doc (worked blend numbers).

### Per-cylinder trim — `fuelTrim1..4Table` + `fuelCylNTrimTableIdx`

- **What it is.** 4 sbyte 5×5 trim tables (% direct, `fuelTrimRPM` × `fuelTrimLoad`); assignment
  scalars `fuelCylNTrimTableIdx` map each cylinder to a table (0 = reference/0%). One injector
  channel (`injCylN`) per cylinder.
- **How to set it.** Front cylinder = 0% (richest, reference); anchor each EGT-measured cylinder
  from its EGT; hold a fixed front-to-rear charge-temp delta to set the rear trim; **extrapolate
  unmeasured mid-rear cylinders RICH** (unmeasured + literature flags them hottest). A constant
  front-to-rear delta holds at every load cell. Apply a mild per-table **load shape**
  `M + [−1,+1,0,0,−1]` — a small cruise bump tapering off at idle and full boost (FFIM
  maldistribution worst at cruise, eases under boost). Keep two rear cylinders on separate tables
  even if identical, so one can split off when it gets its own probe. **Diagnose offset vs real
  maldistribution**: a front-to-rear EGT delta that **shrinks as load rises** is real airflow
  maldistribution; a load-constant delta is a sensor offset. Full method:
  [per_cylinder_trim_ffim_distribution.md](per_cylinder_trim_ffim_distribution.md).
- **Failure modes.** Unmeasured mid-rear cylinder leaner than estimated with no EGT to catch it
  (priority: more EGT channels). `Injector N trim` channel reports flow scaling, not cyl-trim
  output — can't read back active trim %. Don't let per-cyl trims justify global over-enrichment (F4).
- **Live values:** [supra/notes/per_cylinder_trim_results.md](../supra/notes/per_cylinder_trim_results.md).

### Acceleration enrichment (transient)

- **What it is.** Two tables: Table 1 = accel enrichment % (axes: **TPS rate of change × RPM**);
  Table 2 = enrichment correction % (often load/MAP-based, when to reduce it). For **transient
  spikes only** — not gradual transitions.
- **How to set it.** Higher TPS-rate → more enrichment; lower RPM at the same rate → more (worse
  wall-wetting at low port velocity). Gentle idle/low-RPM transitions are handled by the VE table —
  **over-enriching there causes a bog, not a cure.** Test cases to log: gentle snap from idle,
  part-throttle snap at cruise, mid-range snap, post-DFCO spike (vacuum→boost), rolling into boost.
- **Failure mode.** Used as a fix for steady-state VE error (wrong tool — it's for transients);
  decel/lift produces no tip-in so the filter won't catch overrun.
- **Live values:** build doc.

### Cold / cranking / warmup enrichment

- **What it is.** Cranking enrichment, afterstart enrichment (ASE), warmup enrichment — the
  wall-film/vaporization tax, **not** stoichiometric or air-starvation compensators.
- **How to set it.** Lives with cold-start: [engine_start.md → Cranking / ASE](engine_start.md).
  ASE as a 2D table CLT × post-start **revolutions** (not time). Their flex blends follow the
  cold-enrichment hierarchy in the `tblsVEBlend` block above.
- **Live values:** build doc.

### Decel fuel correction

- **What it is.** Negative (or positive) fuel correction during deceleration / overrun.
- **How to set it / failure mode.** The decelerate-fuel-correction table can fire **negative accel
  enrichment during a return-to-idle recovery** — trimming fuel the wrong way at low RPM and
  worsening a return-to-idle bog. **Raise its RPM floor** so it doesn't activate in idle recovery.
  See [throttle_feel.md](throttle_feel.md), [return_to_idle_bog.md](return_to_idle_bog.md).
- **Live values:** build doc.

### Fuel rail / base pressure — `fuelRailType` / `fuelRailBasepressure` (+ `fuelPressureInput`)

- **What they are.** `fuelRailBasepressure` is the regulator's **set differential at the reference
  condition** (manifold = atmospheric — i.e. key-on, pump primed, engine dead). It is **not** the
  pressure you read at idle. `fuelRailType` picks the regulator model (fixed vs MAP-referenced) and
  whether a sensor on `fuelPressureInput` drives **active** correction.
- **How to set it.** Base pressure must be the **engine-off, pump-primed** rail reading (no vacuum,
  no boost). Critically, `injectorsSize` is the injector flow **at base pressure** — so base and
  injector flow are a **matched pair**. ID-style injectors are rated at 3 bar; if you run a 4-bar
  base you must enter the flow at 4 bar (`Q₄ = Q₃ × √(4/3)`), not the 3-bar number. Set them
  together or not at all.
- **Reading the live channels.** `Effective fuel pressure` = the differential the injector actually
  flows against = rail − manifold; on a 1:1 reg it stays **flat across MAP** (the gauge rail falls
  under vacuum precisely to hold it). `Fuel pressure error` = effective − base; `Fuel pressure
  correction` = the √(P_eff/base) flow multiplier applied to PW. A flat `Effective fuel pressure`
  with a falling gauge rail confirms a healthy MAP-referenced regulator. A *rising* injector
  differential at idle = failed reference line.
- **Failure modes.** (1) Reading idle gauge pressure as if it were base — it's base minus your idle
  vacuum. (2) **Editing base alone** to match a measured rail without re-entering injector flow →
  drives the model *further* off (see F6). (3) **Enabling active correction on a map that was
  autotuned with it off** silently shifts the whole map's fueling by √(P_eff/base) — re-verify STFT
  before driving. (4) A persistent non-zero `Fuel pressure correction` = base/injector pair doesn't
  match reality (benign if constant — VE absorbs it — but the numbers lie).
- **Downstream:** injector **dead time** (`injOpeningTimeTbl`) is keyed on *effective fuel pressure*,
  so it only indexes correctly once base/injector are honest. Calibrate it from the injector's
  offset table: [injector_deadtime_calibration.md](injector_deadtime_calibration.md).
- **Live values:** build doc.

---

# Part 2 — Principles

## F1. `veTable` is the dose; `lambdaTable` is NOT a multiplier

In this fuel-model configuration the fuel equation does **not** divide the dose by the lambda
target. `lambdaTable` is **only a tuning reference and the closed-loop STFT target** — the
firmware does not multiply `veTable` by (stoich/target) to hit it open-loop. Consequences that
govern everything in Part 2:

- `veTable` is the **actual fuel dose** and must carry mixture itself: air-VE × whatever
  enrichment you want. This is why `veTable2` reads leaner/lower for ethanol, and why the dose
  legitimately rises into boost while pure air VE rolls off.
- When you copy a column's shape across MAP you must **add the desired λ enrichment by hand** —
  it does not come free from `lambdaTable`. Correct offset = (air-VE ratio) × (target-λ
  enrichment between the two MAP columns).
- Changing `lambdaTable` alone only moves the STFT target; real mixture changes are made in
  `veTable`. No double-count when you add boost enrichment by hand.

## F2. Best-torque vs protection enrichment — why boost rolloff is ~linear in MAP

Two regimes set the lambda target:

1. **Best-torque (MBT) mixture** — φ ~1.05–1.1 (λ ~0.90–0.95), essentially **load- and
   speed-independent**. In light boost you're near it already; the target is flat, not sloped.
2. **Protection enrichment** (richer than MBT) — fuel added purely to cap a temperature (EGT,
   or end-gas/knock) via evaporative + lower-flame-temp cooling. This is what grows with load.

Protection enrichment is **~linear in MAP**: charge mass ∝ MAP, each increment of fuel buys
~constant ΔT of flame cooling, so holding a fixed EGT cap needs enrichment ~linear in MAP. So
the rolloff can be a straight interpolation between endpoints — **dense bins there are wasted**.
Linearity breaks (and needs bins/attention) at three places: the **MBT→protection knee** (early
boost, ~120–160 kPa — the slope changes, so 130 kPa needs its own bin), the **knock wall**
(retarding timing spikes EGT → superlinear enrichment), and **compressor/turbine limits** (out
of the efficiency island IAT and EMAP climb nonlinearly). Full derivation + bin placement:
[lambda_target_vs_load.md](lambda_target_vs_load.md).

## F3. How enrichment changes with the charge: cam overlap, charge cooling, ethanol

Mixture requirement is set by what's *in* the cylinder, not just RPM/MAP:

- **Cam overlap dilutes the idle charge** with residual exhaust (idle is already a ~30%-EGR
  engine; overlap and turbo backpressure push it further — see [idle.md → P1](idle.md)). A
  diluted charge burns slowly and erratically, so idle wants slightly **rich** λ (faster flame,
  wider misfire margin) and the low-load VE corner is genuinely nonlinear (residual knee).
- **Charge cooling** (evaporative) is real but on EMU is **not** expressed as "ethanol VE higher
  than pump VE" — see F5. Pump gas has no ethanol evaporative cooling, so it leans on fuel
  *quantity* for charge cooling → **the pump lambda table should sit richer than the ethanol
  table** at full boost. Charge-cooling + knock-suppression benefit **saturates ~λ 0.76–0.78**;
  richer than that buys EGT protection, not knock margin.
- **Ethanol idle is not automatically leaner.** Ethanol *can* run leaner under load (more knock
  resistance), but at idle its high latent heat hurts vaporization at low port temp and it needs
  more liquid mass per unit air → higher wall-film sensitivity. Don't assume E100 wants a leaner
  idle target; optimize idle around **stability** (RPM/MAP variance, ignition-correction
  activity), not chemistry. Full treatment: [flex_fuel_ethanol_compensation_blend.md](flex_fuel_ethanol_compensation_blend.md).

## F4. FFIM maldistribution is corrected per-cylinder, not by global enrichment

A front-feed intake manifold distributes air evenly at idle but increasingly unevenly as air-mass
inertia builds — the rear (often mid-rear) cylinders run lean/hot, worst at **cruise**
(inertia/resonance dominated), easing under boost (pressure forces even filling). The fix is
**per-cylinder 3D fuel trim**, each cylinder trimmed to target individually. Therefore: **do NOT
over-enrich the global λ/VE target to protect the leanest cylinder** — that's already handled
per-cylinder, so the global WOT richness is purely an EGT/safety-margin choice (a per-cyl-trimmed
charge holds knock at a slightly leaner global target with more power). Full method:
[per_cylinder_trim_ffim_distribution.md](per_cylinder_trim_ffim_distribution.md).

## F5. EMU VE tables are fuel-dose proxies — pump vs ethanol divergence is a dosing choice

A common mistake is to flag `veTable2` (ethanol) reading **lower** than `veTable` (pump) at high
load as a charge-cooling "physics violation" (ethanol's evaporative cooling should raise its air
VE). **That reasoning is wrong for EMU.** The VE table is a value for **fuel-dose calculation** —
only a rough proxy of physical VE. So the pump-vs-ethanol offset is driven by **mixture/dose
requirements, not air physics**: if ethanol runs leaner in a region, `veTable2 < veTable` there
is expected, not a defect. The overall map *shape* (load knee, RPM hump) is still real air-VE
physics — but don't use air-VE reasoning to set the absolute pump-vs-ethanol offset; measured
lambda + mixture intent set it. Full correction: [ve_ethanol_table_charge_cooling.md](ve_ethanol_table_charge_cooling.md).

## F6. Base pressure is the engine-off differential; injector flow is referenced to it (√ΔP)

Base fuel pressure is the regulator's set **differential** at the reference condition (manifold =
atmospheric: key-on, pump primed, engine dead) — **not** the pressure observed at idle. Two facts
flow from this and govern every fuel-pressure edit:

- **A MAP-referenced (1:1) regulator holds the injector differential constant.** Its dome vents to
  the manifold, so under idle vacuum the *gauge* rail pressure falls by exactly the vacuum amount
  while rail − manifold stays at base. A gauge drop at idle is correct; the drop magnitude equals
  your idle vacuum. The flow-relevant quantity (`Effective fuel pressure`) is flat across MAP. A
  *fixed* (non-referenced) regulator instead holds gauge constant, so its injector differential
  *rises* under vacuum and the dose correction varies with MAP.
- **Injector flow scales with √ΔP, and `injectorsSize` is defined at base pressure.** Actual flow =
  `injectorsSize × √(P_eff / P_base)`, which is exactly the `Fuel pressure correction` channel.
  Because the rating is tied to base, **base pressure and injector flow are a matched pair** — an
  injector rated 1065 cc/min @ 3 bar becomes 1065·√(4/3) ≈ 1230 cc/min @ 4 bar. Change one without
  the other and the model carries a standing flow error (e.g. base 330 with a 3-bar-rated
  `injectorsSize` while the rail actually runs 400 ≈ a few-% constant offset; pushing base to 400
  alone widens it to ~15%).

Consequences for tuning moves:

1. **A constant base/injector mismatch is absorbable** — with a 1:1 reg the offset is constant
   across MAP, so the VE table (and STFT) eat it and lambda still lands on target. The setup is
   *functional*; the numbers just don't physically mean what they say. Honest fix = re-enter base
   and injector flow **together**, then re-verify VE — bookkeeping, not a performance change.
2. **Enabling active sensor correction re-anchors the fuel model.** It multiplies PW by
   √(P_eff/base) where it previously assumed P_eff = base. If the VE map was autotuned with
   correction *off*, switching it on shifts the whole map's fueling — leaner if P_eff > base,
   richer if below — by that factor. Always re-check STFT/lambda after the toggle; never assume
   neutral.
3. **`Effective fuel pressure` is the diagnostic.** Flat across idle→cruise→boost confirms the 1:1
   reg; its value vs base gives the sign/size of any correction shift; a rising idle differential
   flags a dead reference line.

---

## Map quality & validation

- **Machine-smoothed beats hand-smoothed.** A machine-smoothed (autotune) map tracks its lambda
  target markedly tighter in and above the boost-entry region (spread nearly halves) than a
  hand-built map; cruise is a wash (closed-loop deadband masks feedforward smoothness). Read the
  **high-MAP bins** for the map-quality signal. A uniform lean bias is a one-number global
  fuel-scale fix (e.g. map not re-scaled after per-cyl trims), not a tracking fault — re-center,
  then compare spread. Full method + metric: [lambda_tracking_map_smoothing.md](../ai-analysis-skills/lambda_tracking_map_smoothing.md).
- **Map generations:** handmade → hand-smoothed (inferior) → machine-smoothed (newest/best).
- **`lambdaDelay`** is active and logged Lambda is time-aligned to its cell, so same-row
  measured-vs-target attribution is valid even under accel.

## Pure-VE transition (2026-06-29)

The Supra is moving from a **fuel-dose-proxy** VE map to a **pure VE map**. Injector data is
now properly characterized and **fuel-pressure compensation is active**, so injector flow scales
by the orifice equation (`Q ∝ √ΔP`) and the old map is being **rescaled per-cell** to respect it
(dead-time + √ΔP vary by pulse width and per-cell ΔP — not a single global factor).

Consequences:
- Measured `λ/λ_target` now maps **1:1 to air-VE error** — lambda-derived corrections are cleaner
  than under the dose-proxy model.
- Air VE is **fuel-independent**, so `veTable2` should converge toward `veTable`; ethanol's
  stoich/dose difference is carried by the AFR target + injector model, **not** a lower VE number.
  The old "`veTable2 < veTable` is expected" reasoning no longer holds for this car.
- Apply log-derived **% deltas to the rescaled base**, not absolute raw values — a multiplicative
  trim commutes with the orifice rescale (`VE_final = VE_old × rescale × (1+corr)`), so order is
  free, but the rescaled map is the correct base to trim.

### Physics-consistency test for a pure-VE correction (2026-06-29)

Once the map is pure VE, a log-derived correction is only legitimate if it's genuine **air** error,
not injector/ΔP error smeared into the air model. Separate two questions:

**(a) Is the surface geometry physical?** A real VE surface must be: concave-rising along MAP
(steep off idle vacuum as residual dilution/throttling clears, asymptoting to a plateau near WOT —
slope positive and *decreasing*); smooth/monotonic in RPM up to the breathing peak; continuous at
the edge where corrected band meets untouched base. The `20260629_1753` smoothed VE1 passed all three
(e.g. RPM2553 MAP-slopes +8.4/+6.6/+5.1/+3.8/+2.6/+1.7; zero RPM-monotonicity violations in band).
Tiny reversals (≤0.3%) only in deep-boost base cells we never touched (turbo VE rolloff / texture).

**(b) Is the correction VE-attributable or fuel-system error?** Diagnostic signatures:
- **Sign-change across load** (rich at low MAP → lean at mid MAP) ⇒ VE-*curvature* error. A scalar
  fuel error (flow constant, stoich) is single-signed everywhere and cannot flip with load.
- **Lean worsens with pulse width / load** ⇒ NOT injector deadtime (deadtime error is worst at
  *short* pulses — the opposite trend).
- **Rail steady + small FP correction** (`20260629_1753`: mean +1.16%) ⇒ NOT ΔP droop.
  What survives all three filters is air-shaped → legitimately folds into a pure VE map.

**Provenance (corrected 2026-06-29):** for log `20260629_1753`, the **log is AFTER** the injector
deadtime fix + FP-comp enable; the **VE map is the old (pre-correction) one**. That is the whole
point — with fuel *delivery* now trustworthy, residual lambda error isolates VE error cleanly, so
**both the shape and the level** of the correction are valid and must be applied in full. (The
earlier "trust shape, level provisional" note assumed the opposite provenance and was wrong.)

**STFT is slow — gate it.** Short-term trim takes up to a few seconds to saturate, so off-idle /
transient driving it never winds in. Do NOT read the needed enrichment from STFT there; the WBO
`λ/λ_target` already carries the *full* open-loop deficit. Credit STFT (`deficit = λ_err + STFT`)
ONLY for samples held at idle/steady-state long enough to saturate (≈3 s). Consequence here: EMU's
own autotune (STFT-derived) **under-reported** the lean — screenshot showed +2–6% where the direct
clean-lambda field showed +5–8%. Use the direct field, not the autotune screenshot.

**Parametrization that preserves level (don't dilute a localized correction):** a global
per-row/col cubic (`full_smooth`) averages a localized +6% bump down toward the un-sampled base
cells at the ends — it under-applies. Use instead: per-cell **median** clean deficit (N≥20);
**confidence attenuation** `× min(1, √(N/50))` (tames the sparse, overrun-adjacent low-MAP rich
pocket and transient high-MAP clips); a **count-weighted local smooth** with heavy self-weight
(high-N cells barely move) — local averaging preserves the magnitude a global cubic destroys.
Result on `20260629_1753`: cruise-band lift +5–7% (was diluted to +1.3%), core residual ~1%.
**Data-coverage limit:** MAP > 93 kPa was lightly/unevenly sampled — corrected conservatively and
flagged; refine with a log carrying more high-load coverage.

## Related documents

- [lambda_target_vs_load.md](lambda_target_vs_load.md) — best-torque vs protection, boost rolloff (F2)
- [flex_fuel_ethanol_compensation_blend.md](flex_fuel_ethanol_compensation_blend.md) — flex blend curve, cold-enrichment blends, ethanol idle (F3)
- [per_cylinder_trim_ffim_distribution.md](per_cylinder_trim_ffim_distribution.md) — FFIM per-cylinder trim (F4)
- [ve_ethanol_table_charge_cooling.md](ve_ethanol_table_charge_cooling.md) — VE as dose proxy (F5)
- Fuel rail / base pressure — engine-off differential, √ΔP injector scaling, active-correction re-anchor (F6, settings block above)
- [injector_deadtime_calibration.md](injector_deadtime_calibration.md) — `injOpeningTimeTbl` encoding + ID1050X offset → table method
- [ve_correction_from_log.md](../ai-analysis-skills/ve_correction_from_log.md) / [ve_correctness_from_log_method.md](../ai-analysis-skills/ve_correctness_from_log_method.md) — correct VE from a log
- [autotune_ve_difference_filtering.md](../ai-analysis-skills/autotune_ve_difference_filtering.md) — gate EMU autotune VE-DIFFERENCE cells against clean log samples (drop tip-in AE + overrun artifacts)
- [ve_vs_map_at_constant_rpm.md](../ai-analysis-skills/ve_vs_map_at_constant_rpm.md) — VE shaping into boost
- [ve_idle_region_nonlinearity.md](../ai-analysis-skills/ve_idle_region_nonlinearity.md) — idle knee + delta-overlay smoothing
- [lambda_tracking_map_smoothing.md](../ai-analysis-skills/lambda_tracking_map_smoothing.md) — map-quality metric
- [idle.md](idle.md) — idle λ/VE for stability; cranking/ASE enrichment in [engine_start.md](engine_start.md)
