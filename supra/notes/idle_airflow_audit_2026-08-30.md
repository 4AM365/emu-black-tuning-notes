# 2026-08-30 steady-idle airflow audit — today’s `latestdrivevischan.csv`

## Scope and calibration provenance

The visual-channel log is `C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra\latestdrivevischan.csv`
(08:47:44).  The readable export available beside it is `newtune.xml.emub3` (09:03:28),
**16 minutes later**, and Will confirmed that it is **not the tune used for this log**.
It must not be used to reconstruct any log epoch.

The selected log has no oil-pressure, vehicle-speed, A/C, lambda, or `Data changing`
channel.  Its results are therefore controller-owned steady holds, not proof that the
car was stationary, and it cannot independently regress oil pressure or external load.

## Terms and selection

The established active-idle identity is:

`Idle air = active base + custom oil correction + air PID correction`

Thus, for each settled sample:

`feed-forward = Idle air − air PID`

`base-reference command = Idle air − air PID − custom correction`

This last value is the controller's inferred feed-forward term, not automatically the
engine's physical airflow requirement.  At a true settled point, the best logged
requirement proxy is total `Idle air` with the PID and ignition corrections near zero.

The selection was: idle state 2, force-open-loop false, RPM 400+, MAP below 60 kPa,
TPS below 6%, absolute RPM error at most 50 rpm, 0.4-s RPM-rate magnitude at most
75 rpm/s, and at least eight seconds continuously in that state.  There are 4,370
samples.  The long uninterrupted holds (20+ s) are below; values are medians in %
except RPM and temperature.

| time s | duration s | RPM / target | CLT | charge temp | custom | air PID | total air | base-reference command |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 322.96–346.80 | 23.84 | 1008 / 1025 | 96 | 42 | 8 | +7.75 | 42.5 | 27.12 |
| 346.88–375.20 | 28.32 | 1019 / 1025 | 96 | 43 | 8 | +7.00 | 41.5 | 27.12 |
| 1440.16–1465.16 | 25.00 | 1019 / 1025 | 96 | 58 | 0 | +5.50 | 36.5 | 30.81 |
| 1537.48–1568.48 | 31.00 | 1019 / 1025 | 96 | 59 | 0 | +1.12 | 38.5 | 37.91 |
| 1609.20–1636.52 | 27.32 | 1021 / 1025 | 96 | 61 | 0 | −2.75 | 35.5 | 38.19 |

## What is pinned down

`Idle airflow custom corr.` is the active-only **oil-pressure** correction, not a
charge-temperature correction (owner-confirmed in `idle_drive_wobble.md`).  The
contemporaneous all-channel `bogevent.csv` is consistent with that identity during
active idle: correction is 0 at 1.00–2.875 bar, +1 at 2.812–2.938, and +5 at
3.438–3.625 bar.  The later XML must not be used to infer the exact table that was
live in this drive.

Will deliberately eliminated the custom-air correction during this log to remove a
variable.  The selected samples therefore span **separate intervention epochs**.
Never pool the +8-correction early holds with the zero-correction holds as a thermal
or charge-temperature trend; the apparent +8→0 reduction is an intentional change.

The apparent charge-temperature relationship is not causal evidence.  Across the
selected holds, charge temperature rose 42→61 while custom correction fell +8→0;
their correlation is −0.906 and both are almost completely time-ordered warm-up
signals.  EMU defines `Charge temp` as a calculated value from IAT and CLT through
the Charge-temp table (`docs/emu-black-help/Fueling.md`), and IAT is absent here.
It cannot be separated into actual inlet-air and coolant-model contributions from
this export.

Within the zero-custom holds, base-reference command shifts 30.81→37.91→38.19 % at
virtually constant 1,025-rpm target and 96°C CLT.  That 7.38-point spread is
significant.  It is not explainable from the logged variables and must be treated as
an unlogged state/load or another intervention epoch—not fitted into the CLT or
charge-temperature axis.

The **total** steady commanded air in those same three zero-custom holds is only
36.5 / 38.5 / 35.5 % (3.0-point span), because the PID changes +5.50 → +1.12 →
−2.75 %.  Thus the 7.38-point feed-forward movement is a state/calibration issue,
not evidence that the engine's physical airflow demand moved by 7.38 points.  Across
all 2,255 selected zero-custom samples, total air has essentially no linear relation
to charge temperature (r = −0.076) or CLT (r = −0.108); fan is on in every long hold
and ignition correction stays within −1.0…0.0°.  Charge temperature is not a
defensible base-air axis from this log.

## Calibration consequence

Do not re-level `idleActiveAirflow` from this log by comparing it with the later XML.
Use only a known live export for each log segment, or derive the needed term from the
logged channels after every intervention.

## All-channel binary cross-check

`latestdrive.emublog3` was paired to `bogevent.csv`, which is an all-channel export
of the same 1383.68–1392.12-s records.  The binary records begin after a 12-byte
header; record 1 is time zero.  RPM, oil pressure, IAT, Charge temp, CLT, total idle
air, air PID, custom correction, DBW target, TPS, MAP, vehicle speed and fuel pressure
all reconstruct the paired CSV with maximum absolute error no greater than 0.0005
(exact for integer channels).  They can therefore be used over the complete drive.

The five long holds above add the following constraints:

- Early +8-custom holds: oil pressure 3.50–3.625 bar, IAT 33–34°C, A/C off,
  fan on, speed 0.25 km/h, DBW target/TPS 4.7%, MAP 37 kPa.
- Later zero-custom holds: oil pressure 1.875 bar, IAT 50–53°C, A/C off,
  fan on, speed 0.25 km/h, DBW target/TPS 4.35–4.5%, MAP 35 kPa.

In the 2,255 zero-custom settled samples, total `Idle air` has no meaningful linear
correlation with oil pressure (r = +0.008), IAT (r = −0.042), Charge temp (r =
−0.076), CLT (r = −0.108), MAP (r = −0.013), or fuel pressure (r = −0.084).
Oil pressure only spans 1.75–2.00 bar there: median total air is 36.0% at 1.75 bar
and 36.5% at 2.00 bar.  This log therefore does **not** support adding IAT, Charge
temp, CLT, MAP, or fuel pressure as another axis of the custom-airflow correction.

The apparent IAT/Charge-temp correlation belongs to the *feed-forward reconstruction*,
not total air: `base-reference command = total air − PID` makes it move whenever the
air PID moves.  Its IAT correlation (r = +0.656) is consequently not a physical demand
measurement.  The actual hold requirement proxy remains total commanded air with a
small PID, about 35.5–38.5% in the available zero-custom holds.

## Correct allocation: what remains after the oil correction

The correction belongs in `idleCustomCorrection`, not `idleActiveAirflow`.  In robust
10-second, ACTIVE-state holds at fixed 1,025-rpm target and 96°C CLT *while custom
correction is nonzero*, the calculated baseline is exceptionally stable:

`baseline = Idle air − air PID − custom = 27.06…27.19 %`

Over those holds, oil pressure falls 4.062→2.125 bar, IAT rises 33→45°C, Charge temp
rises 42→53°C, and the custom term moves +9→+7.  The baseline changes only 0.13 %.
This is direct evidence that the custom table is absorbing the oil-state demand and
that no remaining IAT/Charge-temp correction is measurable in that epoch.

The possible secondary drivers are not independently identifiable from this drive:
oil pressure versus IAT has r = −0.976, versus Charge temp r = −0.977, and IAT versus
Charge temp r = +0.999 in the fixed-target/CLT holds.  They are one heat-soak trajectory,
not independent experiments.  A multiple regression would assign arbitrary portions
of the same effect to each variable.

The zero-custom data contains a non-physical discontinuity instead: at 1535.04 s the
baseline is 31.00 %, at 1547.72 s it is 36.25 %, and at 1554.98 s it is 38.19 %, while
oil pressure remains 1.875 bar, IAT/Charge temp remain 52/59°C, CLT remains 96°C,
fuel pressure remains 3.188 bar, A/C is off, fan is on, and MAP/TPS stay 35 kPa/4.5%.
This is a live controller/calibration-state change, not a new physical correction
surface.  Exclude that epoch from custom-table fitting.

## Plant airflow requirement (not feed-forward)

For a held RPM, commanded `Idle air` and DBW target describe the actuator request;
the density-normalized trapped-air proxy is, from the ideal-gas relation,

`mass index = MAP × RPM / (Charge temp + 273.15)`.

Displacement and gas constant are fixed, so it is sufficient for relative comparison.
Only ACTIVE samples with no force-open-loop, RPM within 20 rpm of target, RPM-rate
below 35 rpm/s, and idle ignition correction within 0.5° were used.  At 1,025-rpm
target and 96°C CLT, 10-second medians give:

| oil-pressure band | n | OP bar | IAT / charge °C | total idle air % | DBW target % | MAP kPa | mass index | change from high |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| >3.5 bar | 4 | 3.969 | 33 / 41.5 | 44.25 | 4.85 | 38 | 123.078 | 0% |
| 2.5–3.5 bar | 2 | 3.438 | 34.5 / 43.5 | 43.50 | 4.75 | 37 | 119.275 | −3.09% |
| ≤2.5 bar | 34 | 2.000 | 50 / 57 | 37.50 | 4.50 | 37 | 114.036 | −7.35% |

Thus the plant does require less charge mass as this run heat-soaks: actuator request
falls about 0.35% throttle and the charge-mass proxy falls 7.35%.  It strongly tracks
oil pressure on this trajectory, but oil pressure, IAT, and Charge temp themselves are
nearly inseparable here (OP–IAT r = −0.976, OP–Charge-temp r = −0.977, IAT–Charge-temp
r = +0.999).  This drive proves the combined drift, not a unique oil-vs-temperature
causal split.

Potential secondary drivers were held or nearly held: A/C off; fan on; fuel pressure
3.188–3.312 bar; VVT target 2.5° and actual 2.0–2.5°; ignition target 18° and actual
17.5–18.5°.  None supplies a separate correlation in this record.  Separate the cause
with a deliberately orthogonal test: vary inlet/charge temperature while oil pressure
is held, then vary oil state at the same inlet temperature; keep target, fan, A/C,
VVT, ignition target, and lambda target fixed.

## Low-RPM / low-pressure recovery corner

At 414.72 s, the log is ACTIVE with force-open-loop clear but is **not** settled:
RPM 862 versus 1,025 target, oil pressure 2.50 bar, CLT 96°C, IAT/Charge temp 36/45°C,
A/C off, fan on.  Total idle air is 49.5%, comprising 26.875% scheduled base
(`49.5 − 19.625 PID − 3 custom`), +3% custom correction, and +19.625% air PID.
Ignition correction is +11° and actual timing is 29° against an 18° target.  Nearby
samples hold 850–925 rpm with approximately +19…+21% air PID and 28…31° timing while
still below the target.

This demonstrates a major missing **low-RPM / low-pressure oil-state** correction;
the engine requires rescue air and advance at that corner.  It is not valid to copy
the +20% PID into a table: pressure falls with RPM (`P ∝ viscosity × pump speed`),
and the trace includes throttle transport and RPM recovery dynamics.  Size the custom
surface from a deliberate held 900-rpm test at the same oil state, then retain a
positive rescue margin.  Do not reduce positive PID authority before that corner has
scheduled air; doing so would simply turn this observed sub-target recovery into a
stall.

## Required next log

Export the full `latestdrive.emublog3` CSV (the existing `latestdrive.csv` is header
only), including Engine oil pressure, Engine oil temperature if available, IAT,
Charge temp, CLT, coolant fan, A/C clutch/pressure, vehicle speed/gear unknown,
lambda/target, idle state/force-open-loop, all three airflow terms, and `Data changing`.
Hold each test point for at least 30 seconds after a 15-second settle period.  Change
one factor at a time: deep-soak oil state at fixed 1,025-rpm target, A/C or fan state,
and a repeat after a known calibration save.  This creates the comparisons needed to
assign the remaining 7.4-point shift instead of baking it into the base table.

## Decision check: oil / idle-air / RPM scatter

The all-channel scatter must be segmented before it can answer whether to make a
*new or larger* oil-pressure correction.  `Idle airflow custom corr.` is nonzero for
much of 0â€“1,200 s (for example, its typical value is +6% around 2.06 bar and +9% near
4.00 bar), while it is zero for the final approximately 1,500â€“2,170 s.  Pooling those
epochs mixes calibration states: by definition,

`Idle air = scheduled base + custom correction + air PID`.

The final zero-custom, tightly settled 1,025-rpm holds only cover approximately
1.875â€“2.00 bar.  That is not enough pressure span to identify an oil slope; it cannot
validate a new low-pressure air add.  The low-RPM bog also cannot size one: as RPM
falls, pump speed (and therefore displayed oil pressure) falls, while the air PID and
idle-spark controller are simultaneously rescuing the engine.  It is an important
recovery/stall-protection observation, not a steady-state causal experiment.

Decision: retain the existing oil-state schedule in the **custom correction** location
until a controlled test disproves it, but do not increase or reverse its low-pressure
cells from this drive.  A deliberate held-RPM, varied-oil-state experiment is required
to size a new term; otherwise the table risks encoding the consequence of an RPM dip
rather than its cause.

## Does the custom-air term create an idle re-entry step?

Use the state equation from the log skill, rather than infer from a scatter:

`Delta Idle air = (ACTIVE base - ARMED base) + custom correction + air PID`.

The custom term and air PID are not applied in ARMED; both become active in ACTIVE.
With PPS <=4% and actual ignition angle constrained to 18 +/-3 degrees for the entire
0.4-second before/after window, the log has 11 ARMED -> ACTIVE entries.  Ten have a
nontrivial custom term (8â€“13%, median 12%).  Their median observed total-air change is
only +1.25% (44.5 -> 45.75%), with a -8.5 to +13.0% range; the median post-entry PID is
+0.34%.  Therefore the implied median base-table switch is about -11.1%:

`1.25 - 12.0 - 0.34 = -11.09%`.

The correction is definitely introduced at the state boundary, but these data do not
show it alone creating a 12% net actuator step: the ACTIVE and ARMED base requests
mostly counteract it.  A low-custom (+1%) qualified entry still steps +7%, proving the
net step is not uniquely caused by the custom term.  All qualified entries are at
elevated targets (1,369â€“1,755 rpm; median 1,559), so this log does not prove what the
same transition will do at a 1,025-rpm target after the clutch/VSS target changes are
removed.

### State-matching rule for a 1,025-rpm re-entry

At the actual ACTIVE-entry speed `R_e = target + live ramp-down offset`, select a
reference custom value `C_ref` for the normal re-entry oil/thermal condition.  Set the
tables so the two state outputs meet:

`armed(R_e) = active_base(R_e) + C_ref`, with `PID = 0` at handover.

The active table therefore holds the residual `active_base = A_ref - C_ref`; the armed
table holds the *total* `A_ref` because custom correction is not applied while ARMED.
`A_ref` must be the **zero-PID hold requirement**, not a deliberately high value: a
negative air-PID correction closes the throttle after entry and can create the very RPM
undershoot/bog being diagnosed.  Example only: if the observed handover requirement is
37.5% and `C_ref = +7%`, use active base 30.5% and armed 37.5% at `R_e`.  A custom
value of +9% then produces a +2% entry offset; a value of +5% produces -2%.  A static
armed table cannot perfectly match a custom correction that changes by more than that
across oil states, so choose `C_ref` for the usual re-entry condition and keep the PID
near zero at handover; negative authority is a limit for disturbances, not the normal
re-entry strategy.

## Airflow-kP versus the DBW closing-floor event

`bogevent.csv`, t=1383.68--1392.12 s, shows that the DBW output floor and the
airflow-PID negative command are related but are not the same saturation.  The
post-drive `newtune.xml.emub3` has `idleAirFlowKP=717`; with the established
`raw/1024` scale this is 0.700 % airflow/degree (the XML postdates the log, so it
is a configuration cross-check rather than proof of the earlier setting).  Directly
from the event, selecting ACTIVE, force-open-loop=0, and nonzero air PID gives:

`air PID = 0.7334 * idle-ignition correction - 0.0103`, `R^2=0.997`, n=90.

Thus the logged controller is essentially proportional at 0.73--0.77
airflow-%/degree, consistent with the 0.700 setting plus a small integral term.
At the negative ignition rail, the recorded `-8 deg` correction gives approximately
`-6.1%` air PID.  Halving kP (717 -> about 358 raw, 0.350 %/degree), while holding
the integrator state fixed, changes that term by:

`Delta air = (0.7334 - 0.3667) * 8 = +2.93% airflow`.

With the `[2.4, 8.0]% TPS` actuator range in the post-drive XML, that corresponds to
`Delta TPS = 2.93 * (8.0-2.4)/100 = +0.164% TPS` of retained opening.  The change is
therefore a worthwhile way to reduce the *later* overspeed-closing pulse and its
ringing; it does not remove the fast ignition torque correction.

Crucial sequence check: the longest `DBW Out. DC=-35%` run is 1.36 s,
1386.84--1388.16.  It starts in ARMED with zero air PID and remains at the closing
floor after ACTIVE begins, while air PID is **positive** (+4.4 to +5.4%).  It cannot
have been caused by negative airflow PID.  The later 0.64 s floor run,
1389.48--1390.08, *is* accompanied by `-5.1...-6.2%` air PID and `-7...-8 deg`
ignition correction; this is the part that a half-kP test can materially shorten.

Consequently, test `idleAirFlowKP` 717 -> 358 as a reversible damping experiment,
with KI and the PID output limits unchanged initially.  Success is not merely a
smaller negative PID number: require both (1) the negative-PID/floor run to be
shorter and (2) the pre-PID 1.36-s DBW-floor run to be absent or materially shorter.
If (2) remains, its cause is the ARMED/ACTIVE/DBW target trajectory or actuator
tracking, not the airflow-P gain; use oil temperature directly for the feedforward
reference rather than asking kP to mask that state-transition error.

### Correction: the 16:56 (t about 1016 s) bog is not a negative-air-P event

The prior section describes a later short event and must not be used to explain the
large bog at 16:56.  In the matching visible-channel trace, ARMED begins at t=1014.84
with zero air PID.  TPS then falls from 7.7% to 2.7% by t=1015.88 before ACTIVE enters
at t=1016.24.  The full-channel display shows this as the sustained `DBW Out. DC=-35%`
closing drive identified by the owner.  Once ACTIVE starts, the engine falls from
1813 rpm to 1270 rpm while its target moves 1772 -> 1487 rpm and air PID is positive:

`+0.25, +2.06, +5.13 ... +8.69%` (idle-ignition correction `+0.5 ... +11.5 deg`).

Therefore the closing-floor episode happens first; the airflow PID is trying to
rescue the resulting air deficit afterward.  Cutting kP in half cannot prevent this
floor run and, at the +11.5-degree recovery point, would remove roughly
`0.733/2 * 11.5 = 4.2%` of the rescue-air response (about 0.24% TPS for the 5.6% TPS
actuator window).  It is nevertheless a standard and valid way to **reduce subsequent
closed-loop overshoot** if the delayed airflow loop is ringing: `Delta air_PID =
kP * Delta ignition-correction + I`, so halving kP halves the delayed P component.
The target-step/ARMED trajectory and kP are thus two different levers: fix the former
to prevent the initial close; test the latter against the amplitude and decay of the
post-recovery overshoot.  Schedule the steady requirement from oil temperature rather
than relying on either gain change to supply feedforward.

**Owner constraint (2026-08-30):** the ramped-target change is firmware behavior and
is intrinsically a step function, not an independently removable calibration
discontinuity.  Treat it as the fixed disturbance that the idle system must tolerate.
The practical levers are the armed/active feedforward trajectory (including oil-temp
requirement) and loop damping: lower airflow kP can reduce the post-step delayed-air
overshoot, but must be evaluated against the reduced positive rescue response as well.

### Response criterion for this target-step system

Do **not** use the conventional quarter-amplitude / roughly 1.5-cycle-settle criterion
for this idle system.  A forced downward target step is routine here, while a single
RPM undershoot can put the engine into the DBW closing-floor / recovery sequence.  For
each falling target segment define `e(t) = RPM(t) - idle_target(t)`.  The desired
response is one-sided and asymptotic: start with `e > 0`, then reduce toward zero
without a negative crossing (`e >= 0`, apart from measurement noise) and without a
sustained `DBW Out. DC=-35%` command.  In control terms, choose an overdamped or
near-critically-damped response, not an underdamped response with an allowed first
overshoot.  Airflow-kP reduction is the first damping lever for the delayed-air path;
if a lower kP still crosses, inspect integral carryover and state/feedforward geometry
rather than accepting a repeatable crossing as normal settling behavior.

### Fast ignition / slow airflow allocation

The desired architecture is not merely lower gain; it is intentional time-scale
separation.  Let `theta` be idle-ignition correction and `u_air` be airflow-PID output:

`u_air = Kp_air * theta + Ki_air * integral(theta dt)`.

Ignition uses RPM error and changes torque essentially within a combustion cycle;
airflow's job is to bring `theta` gradually back to zero, preserving symmetric spark
reserve for the next disturbance and avoiding sustained retarded combustion.  The
immediate air P term is not rate-separated: the active event fit is
`u_air = 0.733 * theta - 0.010` (`R^2=0.997`).  Thus the current 0.7-ish air kP makes
air command copy every fast spark correction, while the DBW/manifold delivers that
copy late.

Size the P leakage against the maximum immediate air movement allowed for the full
spark window, rather than around a conventional oscillation target:

`Kp_air <= DeltaA_fast_allowed / abs(theta_max)`.

For the observed negative side `theta_max = 8 deg`, allowing at most 2--3 airflow %
of immediate closing gives `Kp_air <= 0.25--0.375 %/deg`.  Current ~0.70 gives 5.6%;
the proposed half value ~0.35 gives 2.8%, which is in that deliberately slow band.
The integral, not P, then performs recentering.  Pick its rate from a deliberate
recenter horizon: `Ki_air = DeltaA_residual / (abs(theta_bias) * t_center)`.
For example, after oil-temp feedforward leaves a 4% residual, holding only 2 degrees
of spark bias for 10 seconds requires `4/(2*10)=0.20 %/(deg*s)`, close to the
present air-KI scale.  This preserves output range for genuine catches; it changes
the *rate and immediate coupling*, not the available rescue authority.

#### Airflow-slew benchmark

Score airflow rate over a 1-second window (not one 40-ms quantized log sample).  With
oil-temperature feedforward carrying the roughly 15% slow demand, use **0.2--0.5
airflow %/s** as the normal ignition-recentering rate: a 2--4% residual is then removed
in roughly 4--20 s, while ignition remains near its target and retains torque reserve.
Treat **about 1 airflow %/s** as the upper bound for a sustained non-emergency trim;
if spark is already at its authority rail, the answer is missing feedforward or a real
load transient, not permission for the slow air loop to chase it at tens of %/s.

This is far below the 16:56 behavior.  While ACTIVE and force-open-loop clear, air PID
jumped +1.81% in 0.04 s (45.3 %/s), +1.38% in 0.04 s (34.4 %/s), and +1.69% in
0.04 s (42.2 %/s).  On force-open-loop release it jumped +4.56% in 0.04 s
(114 %/s).  These are P-path copies of fast ignition corrections, not slow recentering.
Even kP=0.35 %/degree makes a normal 2-degree ignition jump in 40 ms into a 0.70%
air step (17.5 %/s).  Therefore halving P is a damping improvement but cannot, by
itself, make airflow a genuinely slow loop; a near-zero P term or a firmware-level
airflow slew limiter would be required for a literal slew limit.  The existing
KI~0.20 %/(degree*s), evaluated over seconds, is already in the intended recentering
rate range.

**Next-test recommendation (2026-08-30):** set `idleAirFlowKP = 128` raw (0.125
airflow %/degree), leaving `idleAirFlowKI=205` raw unchanged for the first test.  Zero
P is unnecessarily absolute: KI performs the slow recentering, but a small P path
still gives a bounded response to a persistent ignition offset.  At 0.125 %/degree,
the observed -8-degree correction produces only -1.0% immediate air (rather than
-5.6% today); the +11.5-degree catch produces +1.44%.  KI then supplies the slow
0.4 %/s response at a normal 2-degree bias (and 1.6 %/s at an 8-degree transient).
Retain the existing output limits; assess the run by the one-sided RPM approach and
ignition return to target, not by how quickly airflow moves.

## `more_pid` validation (2026-08-30)

Source: `C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\Supra\more_pid.csv`,
0--496.68 s at 25 Hz, paired with the XML exported 12 seconds earlier.  Scope is
idle/DBW behavior only: this reduced log has no lambda, fuel, knock, or ECU-state
channels, so it cannot certify fueling, combustion safety, or a true engine stop.

### What was live

The XML confirms the intended architecture: `idleAirFlowKP=307` raw = 0.300 %/degree,
`idleAirFlowKI=410` raw = 0.400 %/(degree*s), integral limits -25/+15%, output limits
-25/+25%, VSS idle-target add disabled, clutch target add 0, and force-open-loop above
400 km/h.  At the warm 1000-rpm cell the active table is 49% versus 42% armed, a
nominal +7% ACTIVE bias; logged custom correction is exactly zero throughout.

### Results

The active controller is unambiguously carrying a negative bias: across all 7,248
ACTIVE samples, air PID median is -18.44% (p5 -25.00, p95 -0.06; range -25.00 to
+7.31).  In 4,836 stationary, 1025-rpm ACTIVE samples it is -21.12% median, and is
pinned at -25% for 31.5% of those samples.  Overall it is bit-exactly at -25% for
66.04 s of the 496.68-s log; it never reaches the +15 integral limit.

The strategy does produce calm short holds, but they are *stable while saturated*,
not centered.  Three parked-idle closing-floor holds at t=142.36--188.28,
259.00--301.04, and 462.40--496.68 run `DBW Out. DC=-35%` for their entire
45.96/42.08/34.32-s durations.  Their RPM-error median/p5/p95 are respectively
-12/-32/+29, -20/-38/-3, and -12/-29/+8 rpm.  The last is particularly quiet
(11.7-rpm standard deviation) but has air PID -25% median and actual TPS 4.0% while
the controller continues requesting close.

Return quality remains mixed.  Fourteen ARMED->ACTIVE entries occur.  Over the first
2.5 s, seven cross at least 25 rpm below their moving target and five cross at least
50 rpm below; worst errors are -89, -102, -76, -82, and -117 rpm.  One recovery at
t=393.12 reaches 454 rpm versus a 1025-rpm target, then recovers without a confirmed
stop; air PID rises to +7.31 and ignition correction to +17 degrees.  This is a real
catch, but not the desired one-sided/asymptotic response.

### Decision

The new active-air bias is effective at preventing a documented complete stall in this
record and gives several quiet 1025-rpm holds.  Its cost is explicit: the controller
is routinely parked at both the -25% air command and the DBW -35% physical close
drive, so it has no negative centering reserve and return-to-idle is still not
consistently one-sided.  This log validates the *safe-side bias concept* but does not
yet validate it as a finished general-drive calibration.  The next useful change is
not more base air or less output range; it is to tune the airflow P/I balance against
the repeated entry crossings while retaining enough positive catch authority.

### All-channel qualification: the apparent two-stage pull-down

The paired `more_pid_all_channels.csv` changes the attribution of two observations
above.  The 454-rpm sample is preceded by `Idle state=4`, `Idle control active=0`, and
zero air-PID correction while DBW target source is 3 (blend).  ACTIVE resumes only
after the dip has already reached 511 rpm.  It is therefore a blend/handover catch,
not a valid air-PID return event, and must be excluded from air-PID scoring.

The all-channel log also records live calibration writes (`Data changing=1`) repeatedly
from 249.16--312.20 s and again after 462.92 s.  In particular, the apparent I-term
jump from -25% to -18% at 279.76 s coincides exactly with a live write; it is not
evidence of a two-step controller response.  Statistics crossing those intervals are
not pooled with untouched calibration data.

An untouched return at 412.40--427.36 s shows the intended cascade plainly.  The idle
target ramps 1370 -> 1025 rpm over 2.96 s; during that interval total commanded air
goes 52.5 -> 47.5%, while air PID moves smoothly -0.125 -> -1.188%.  Once the target
is at 1025 rpm, ignition correction is initially -7 degrees and the air-PID I term
then continuously removes air: total air 47.5 -> 25.5%, PID -1.188 -> -23.5%, over
12.0 s, with no second discontinuity.  The governing logged relationship is
`air_PID = P(theta) + I`, where the monitored P term is about -2.1% at the -7-degree
ignition correction and the I term supplies the progressive trim.  This is a genuine
two-*phase* visual (scheduled target ramp, then slow I recentering), but not two
airflow steps.  It is consistent with the deliberate cold-oil-safe ACTIVE base and
fast-spark/slow-air allocation.

### Target trajectory is the primary decel-idle calibration

For a linear ramp-down offset the ECU commands
`r_target(t) = r_idle + max(0, offset_0 - d*t)`, where `d` is the configured
`idleRAMPDownDecayRate`. Define tracking error `e = RPM - r_target`. The air loop
uses ignition correction `theta` as its reference, so during an over-speed descent
`e > 0` gives `theta < 0` and `dI_air/dt = Ki_air * theta < 0`. If the target falls
faster than the engine can follow, the integrator arrives at base idle already
negative; after the target stops falling, that stored closing command continues and
creates the undershoot/bog.

In the untouched 412.40--415.36 s return, `idleRAMPDownDecayRate=125 rpm/s` commands
1370 -> 1025 rpm in 2.96 s. Actual RPM goes 1386 -> 1215 rpm, an average
`(1215 - 1386)/2.96 = -57.8 rpm/s`, leaving `e=+190 rpm` at the endpoint. Here the
I term is still +0.92%, because early ramp tracking was below target; the later
negative I is therefore a controlled recentering tail rather than carried windup.
The same calculation diagnoses a more aggressive decay setting: negative I already
present at ramp completion is the unsafe signature.

The firmware ramp is linear, not exponential. A lower linear decay rate is the
available approximation to a gentle exponential-like approach: choose it so the
target does not outrun the naturally achievable RPM descent, then judge success by a
one-sided approach to base idle without a sustained pre-endpoint negative I term.

Across the 13 clean ACTIVE moving-target ramps in this log, handover begins close to
the commanded trajectory (start error median `RPM - target = +9 rpm`). It does not
remain close: only 31.7% of 898 moving-ramp samples are within +/-50 rpm, with median
error +61 rpm and 90th-percentile +167 rpm. The endpoint error is commonly +130 to
+250 rpm. Thus the engine meets the 1375-rpm ARMED handover condition, but the
125-rpm/s ACTIVE target descent usually outruns the actual engine trajectory.

The 13 complete clean ramps have median actual speed slope -66.7 rpm/s (middle half
-99.6 to -55.1 rpm/s), against the fixed -125 rpm/s command. With approximately zero
handover error, the first-order endpoint prediction is
`e_end = (125 - 66.7) * (350/125) = +163 rpm`, matching the observed +169 rpm in the
412.40-s run. Thus target-path matching—not faster airflow gain—is the first lever for
tight tracking. A reversible first test is decay 60--70 rpm/s (350-rpm offset duration
5.0--5.83 s); it brackets the measured median plant descent. Validate per state-2 ramp:
keep the moving-target error mostly within +/-50 rpm, require no sustained negative
air-I before the ramp endpoint, and confirm ignition correction is not sitting at its
negative authority boundary.

If the intended trajectory is instead -200 rpm/s, do not lower the target rate to
match this log; supply more planned braking torque/air removal. With the present
median -66.7 rpm/s plant response and 350-rpm offset, a -200-rpm/s target would finish
in `350/200 = 1.75 s` and first-order endpoint error would be
`(200 - 66.7) * 1.75 = +233 rpm`. In the 412.40-s ramp at +190 rpm error, idle timing
is already 11 degrees against an 18-degree target (`idle ignition correction=-7`),
near the configured low-torque ignition floor. Therefore increasing ignition kP alone
cannot create the required tracking torque once this floor is reached. The needed
lever is rate-aligned feed-forward air removal (table shape or a suitable custom/state
correction) plus only enough air-P response to follow the ignition command; air-I
remains a slow residual trim and negative authority remains a guardrail, not the
means of producing the -200-rpm/s trajectory.

The warm `idleIgnitionMinTorqueAngleTbl` decodes to 13, 12, 11 and 10 degrees at
800, 1067, 1333 and 1600 rpm respectively (raw values 26, 24, 22, 20 at 0.5 deg/count).
At the +190-rpm-error point the log is actually 11 degrees against an 18-degree idle
target, confirming practical contact with this low-torque floor. A modest 2--3-degree
lowering in the decel-relevant 1100--1600-rpm region is a reasonable reversible
authority experiment for the requested -200-rpm/s ramp, but is not a steady-idle
solution. Local references support spark as the fast idle-speed actuator
(`corpus/engine_management_advanced_tuning.md:2658-2662`) and note that late spark
raises exhaust temperature (`corpus/how_to_tune.md:16114-16117`), while 8--20 degrees
is a typical idle timing range (`corpus/how_to_tune.md:16135-16140`). Keep the new
floor out of sustained normal idle use, log EGT/lambda/knock, and restore the prior
floor if it is held for more than the short decel transition or compromises catch.

Owner clarification: `more_pid_all_channels.csv` was recorded at very hot oil while
the ACTIVE table intentionally represents cold-oil-safe airflow and its logged custom
air correction is zero. Therefore the large negative air-I in this record is primarily
the delayed removal of hot-oil surplus, not a clean measure of the braking required by
the requested -200-rpm/s target. For example, at 415.36 s the scheduled base is
`47.5 - (-1.188) = 48.688%`; by 423.36 s total air is 30.5% with -17.875% PID while
RPM is near target. A roughly 18-point hot-state correction must be available at
ACTIVE entry before this trace can be used to size target-tracking kP or a lower spark
floor. A lower floor remains transient reserve, not the primary cure for this thermal
feed-forward mismatch.

### Literature benchmark: idle minimum-torque angle for this mildly cammed engine

There is no universal minimum-torque spark angle: it depends on burn rate, residual
gas, mixture distribution, compression and cam overlap. EMU itself defines this map
as an assumed minimum-torque angle and only requires it to be below the idle-target
angle (`docs/emu-black-help/Idle.md:225-230`). The literature gives useful bounds:
Banish notes that larger-duration/overlap cams need more idle advance
(`corpus/engine_management_advanced_tuning.md:556-564`), while also noting that many
modern DOHC engines with stock cams idle in single-digit advance
(`corpus/engine_management_advanced_tuning.md:4048-4053`). Hartman gives 8--20 degrees
as a typical idle-timing working range at low speed
(`corpus/how_to_tune.md:16135-16140`) and warns that late spark raises exhaust
temperature (`corpus/how_to_tune.md:16114-16118`).

For this mildly cammed engine, retain the measured 18-degree warm steady-idle target;
benchmark an ACTIVE-only transient floor of 9--10 degrees in the 1100--1600-rpm
decel range, with 8 degrees as a short-duration lower test bound rather than a normal
operating target. The present map is 13/12/11/10 degrees at 800/1067/1333/1600 rpm.
A literature-consistent, catch-preserving first test is 13/11/9/8 degrees. Relative
to an 18-degree target, this expands negative spark-angle authority from 6/7/8 to
7/9/10 degrees over the last three bins; this is correction-angle authority, not a
claim of proportional torque change. Stop the sweep at the first sign of roughness,
misfire, delayed recovery, or adverse EGT/lambda/knock behavior.
