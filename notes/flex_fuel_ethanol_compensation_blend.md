# Flex-fuel blend curve with ethanol pulse compensation

> **Car-specific values live in the build working docs**, not here. For the reference build see [`supra/notes/`](../supra/notes/) — esp. [`my_car.md`](../supra/notes/my_car.md) and [`timing_targets.md`](../supra/notes/timing_targets.md) (boost/lambda targets). This note is intentionally car-agnostic.

When EMU's ethanol fuel-scale table is responsible for the stoichiometric fuel
mass change, the table-switching blend curves should not re-create the old
ethanol fuel-mass curve by intuition. Use the fuel-scale table itself as the
curve source.

For a blend from table 1 at E0 to table 2 at E100:

```
table_1_weight(E) = 1 - ethanolFuelScale(E) / ethanolFuelScale(100)
```

This works in raw counts because the scale factor cancels. Read this car's
`ethanolFuelScale` (against the `ethanol10Bins` axis) from the live export,
then interpolate it onto the table-switching ethanol blend axis to get the
table-1 weight at each blend bin. Round the result to EMU's 0.5% blend-table
resolution and encode as `ubyte` for the blend symbol.

The curve is nonlinear (the fuel-scale table itself is nonlinear), so the
table-1 weight falls faster than ethanol % rises — re-derive it from the actual
fuel-scale table rather than assuming a straight line. The worked numbers for
this build live in `supra/notes/`.

Use this for `tblsFFLambdaBlend` when the lambda target endpoint should advance
with the same nonlinear ethanol compensation curve. Use it for `tblsVEBlend`
only when VE table interpolation should advance with that same compensation
progress; if VE1 and VE2 are identical true-VE models, the VE blend curve has no
fueling effect until VE2 is intentionally tuned away from VE1.

## VE tables vs lambda target changes

With ethanol pulse-width compensation active, the VE tables should remain airflow
models. Do not intentionally encode desired lambda-target differences into VE
unless it is a temporary workaround. A planned target change of 0.02 lambda is
roughly equivalent to a 2% VE fuel change, but the permanent VE correction should
come from measured lambda error:

```
VE_new = VE_old * measured_lambda / target_lambda
```

So if Lambda Target 2 is leaner than Lambda Target 1 by 0.02 in a high-load cell,
that is normally a target-table choice, not a reason to subtract 2% from VE2.
Only trim VE2 when the ethanol endpoint misses its own target during steady-state
logs.

## Full-boost lambda endpoint principle

Set two full-boost lambda endpoints — an E0 (pump) endpoint and an E100
(ethanol) endpoint — and let the flex blend interpolate between them by ethanol
content. The ethanol endpoint can generally be set leaner in lambda than the
pump endpoint because ethanol provides more knock resistance and charge cooling
than gasoline; both land inside the forced-induction best-torque/protection band
cited below. This build's actual endpoint values are in `supra/notes/`.

Reference basis:

- Hartman (`corpus/how_to_tune.md`, page 22) lists gasoline rich best torque at
  lambda `0.79` and safe best power at lambda `0.83`.
- Hartman (`corpus/how_to_tune.md`, WOT best-torque discussion) gives a typical
  gasoline WOT best-torque spread of lambda `.78-.90`, with mean best torque in
  the `.82-.85` range.
- Banish (`corpus/engine_management_advanced_tuning.md`) uses lambda `0.77` as
  a forced-induction WOT starting target during airflow mapping.
- Heywood (`corpus/ice_fundamentals.md`, page 490) frames lambda/relative
  air-fuel ratio as the cross-fuel mixture parameter, and says WOT maximum power
  is obtained rich of stoich at about lambda `0.9`, with richer mixtures used
  for charge cooling, knock reduction, and EGT control.
- Heywood (`corpus/ice_fundamentals.md`, pages 821 and 1516) explains why
  ethanol/high-octane/charge-cooling reduces knock pressure compared with pump
  gasoline. That supports using the leaner side of the best-torque band for the
  E100 endpoint, but it is an inference, not a direct Heywood prescription of a
  specific E100 full-boost lambda.

Do not confuse the full-boost endpoint with the boost-entry ramp. A safe
full-boost target at high MAP does not imply that the 80-100 kPa transition
columns should immediately jump to that same richness. Shape the transition
columns for smooth torque and lambda tracking, then verify the 130-200 kPa
columns under steady high-load logs.

## Cold-enrichment flex blend principle

Cranking, ASE, and warmup enrichment are not stoichiometric fuel-mass
compensators. With ethanol pulse-width correction active, the blend curves for
these tables should only control how quickly the ECU moves from the E0 endpoint
extra enrichment to the E100 endpoint extra enrichment.

Cold enrichment pays the wall-film and poor-vaporization tax. That tax is more
ethanol-sensitive during cranking than during warmup:

- Warmup: least ethanol-forward; once the engine is running and surfaces are
  heating, use a curve close to the ethanol fuel-scale shape unless logs prove
  it needs more ethanol-table authority.
- ASE: middle case; still wall-film dominated immediately after start, but less
  severe than cranking.
- Cranking: most ethanol-forward; poor cranking-speed mixture formation and cold
  vaporization can justify moving toward the E100 cranking table faster than the
  stoichiometric fuel-scale curve.

Therefore, do not blindly use one linear blend for all three. A reasonable
starting hierarchy is:

```
Warmup table1 weight >= ASE table1 weight >= Cranking table1 weight
```

at the same ethanol content, with all three ending at 100% table 1 at E0 and 0%
table 1 at E100.

## Ethanol and idle combustion stability

Higher ethanol content does not inherently mean higher idle CoV if the mixture is
fully vaporized, homogeneous, at the same lambda, and fired with suitable spark.
Under those idealized conditions ethanol can be at least as stable as gasoline
because it has good flame-speed and anti-knock characteristics.

In the real port-injected idle case, especially on a cammed engine with overlap,
higher ethanol can increase cycle-to-cycle variation unless the tune compensates
for mixture preparation:

- Ethanol's high latent heat cools the port/charge and can reduce vaporization at
  low airflow and low port temperature.
- More liquid fuel mass is required for the same air mass, increasing wall-film
  sensitivity if injector timing, warmup, ASE, or cranking compensation is not
  right.
- Idle already has low charge density and often high residual dilution from cam
  overlap; small mixture-prep errors therefore have a larger effect on flame
  kernel growth.
- Leaner ethanol idle lambda targets may be chemically tolerable but can still
  raise CoV if residual dilution and mixture stratification are the limiting
  factors.

Practical rule: do not assume E100 needs a leaner idle target just because it can
run leaner under load. For idle, optimize around stability: measured RPM variance,
MAP variance, ignition correction activity, lambda scatter once valid, and how
much timing reserve is needed to hold speed.
