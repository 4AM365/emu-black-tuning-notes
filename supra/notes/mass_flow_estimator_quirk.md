# EMU mass-flow estimator at idle — cammed-overlap quirk

The EMU `Estimated mass airflow` log channel reports **gross throttle flow** (or speed-density-derived equivalent), not net cylinder fill. On this build's cammed 2JZ-GTE this matters because high cam overlap causes significant reversion at low MAP:

- During overlap, exhaust gas pushes back into the intake while air also flows in from the throttle
- The throttle plate must be held more open at idle than a stock-cam build would need
- EMU's estimator sees the high airflow through the throttle and reports it as mass flow, but most of the difference vs. cylinder fill is reverted exhaust going back out

**Symptoms:**
- Reported idle mass airflow can approach or even exceed cruise values (e.g. ~60 g/s reported at 1200 RPM idle, vs. true net combustion airflow of ~6 g/s)
- The number gets *more* accurate at higher MAP/higher RPM where reversion is small relative to fresh charge
- Validated against measured mass at full-tilt (per Will, 2026-05-26)

## When to trust the channel

- **WOT / high-load** — accurate, validated. Use for boost mapping, injector sizing checks, knock-vs-mass-flow analysis.
- **Cruise / mid-load** — likely accurate to within ~5-10 %.
- **Idle / low-load / closed-throttle decel** — DO NOT use for fuel-mass calculations or VE validation. The estimator overstates real combustion airflow by up to ~10×. Use first-principles instead:

```
ṁ = ρ × V_d × (RPM/2) × VE_effective / 60
where:
  ρ        = MAP × M / (R × T_charge)        # ideal gas density
  V_d      = 3.0 L = 3000 cm³                 # displacement
  VE_eff   ≈ 0.55–0.60 at idle MAP on this cam  # read from VE table at MAP×RPM
```

For idle (1200 rpm, MAP 35 kPa, CAT 70 °C, VE 0.55):
- ρ ≈ 0.355 kg/m³
- V̇ ≈ 16.5 L/s
- ṁ ≈ **5.9 g/s**

That's the correct anchor for any idle-region physics work (TB thermal growth, fuel-pump headroom, injector minimum PW, custom-corr sanity checks).

## What this means for tuning

- The VE table at the idle cells is **already calibrated** for the net effective fill on this cam; don't try to "correct" it based on the mass-flow estimator
- When analyzing log behavior at idle, don't compare the mass-flow channel to absolute physical limits (e.g., turbo compressor map, MAF sensor range) — those compare to gross flow, not net
- The estimator's accuracy at full tilt is what matters for boost / fueling work; treat the idle reading as "model-output garbage" and ignore
