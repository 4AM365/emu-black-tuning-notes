# Knock sensors — EMU Black settings and the principles behind them

> **Software page:** *Knock sensors*. Full symbol catalog: [tune_feature_tree.md → Knock sensors](tune_feature_tree.md). Timing tables that this page constrains are on [ignition.md](ignition.md).

Organized like [idle.md](idle.md): settings first, then the principles behind them.

> **Car-specific values live in the build working docs**, not here — esp.
> [`supra/notes/knock_chatter_cov_results.md`](../supra/notes/knock_chatter_cov_results.md).

---

# Part 1 — Settings

### Knock detection setup

- **What it is.** Per-cylinder band-pass window around each combustion event, a rolling baseline,
  and the retard response. Inputs are assigned per cylinder (`ksInputCylinder1..8`).
- **How to set it.** Assign each cylinder's knock input, set the frequency band to the bore's knock
  frequency ([knock_frequency.md](knock_frequency.md) — `F = 900/(π·R)`), window it to the combustion event, and set the baseline tracking + retard authority per
  EMU's knock setup. Confirm the channel is reading combustion (not mechanical noise) before trusting
  it — the knock packet is only above the noise floor in the **boost region**.
- **Failure modes.** Using knock at **idle** (ring-down energy is tiny, packet buried in
  injector/valvetrain noise → use RPM CoV at idle, [idle.md → P4](idle.md)). Window mis-timed →
  reads valvetrain events.
- **Live values:** build doc.

### Knock retard

- **What it is.** The timing pulled when a cylinder's windowed energy crosses the spike threshold,
  plus its restore rate (`kscutDelay`, per-cyl retard).
- **How to set it.** Enough authority to protect, restored gently so the re-advance doesn't stack a
  torque step. Walk **boost** timing up in **1° steps** ([ignition.md](ignition.md)) watching
  per-cylinder retard + EGT; back off the table where a cylinder keeps pulling retard.
- **Live values:** build doc.

---

# Part 2 — Principles

## K1. Reading knock voltage as a combustion-stability (CoV) proxy

`Knock voltage peak cyl N` (the per-event band-pass peak, one value per firing) has cycle-to-cycle
scatter that, **on no-knock cycles**, proxies combustion CoV (the structural analogue of
CoV-of-IMEP) — a way to rank one fuel/ignition map against another without a cylinder-pressure
transducer. Two traps, **both** must be handled:

1. **Operating-point mixing.** The channel mean rises steeply and deterministically with RPM/load
   (mechanical noise), so a naive std/mean is dominated by that trend — a log that merely roams more
   of the boost map looks noisier. **Detrend within fine cells** (e.g. 250 rpm × 10 kPa):
   `resid = (peak − cell_mean)/cell_mean`, then `CoV = std(resid)·100`.
2. **Where you measure.** Map smoothness only bites while **interpolating across cells** — restrict
   to positive transients (dRPM/dt > 0 or dMAP/dt > 0); at steady state rough-vs-smooth washes out.

No-knock cycles only (`Knocking cylinders == 0` AND cyl-N retard == 0); express as CoV (std/mean),
not raw std (the signal is heteroscedastic). It's a qualitative ranking tool, not a calibrated
CoV-of-IMEP. Full method: [knock_voltage_cov_combustion_stability.md](../ai-analysis-skills/knock_voltage_cov_combustion_stability.md).

## K2. Knock-band *variance* is a cylinder-uniformity proxy

Two signals live in the channel: **spikes** (true/incipient knock) and **baseline wander/"grumble"**
(the variance of the per-event noise floor). Maldistribution makes the baseline **walk**: lean
cylinders burn faster/hotter (sharper dP/dθ → more HF content into the block) and sit nearer the
autoignition edge (intermittent trace knock that lifts the floor without crossing the spike
threshold), and their higher COV-of-IMEP makes the windowed energy oscillate. So **watch variance,
not just spike count** — a flat, smooth baseline at max power is the acoustic fingerprint of all
cylinders doing the same thing every cycle (it went dead-smooth after the per-cylinder fuel trims).
Full mechanism: [knock_sensor_baseline_vs_cylinder_uniformity.md](knock_sensor_baseline_vs_cylinder_uniformity.md).

## K3. Knock vs the other limits

Octane sets resistance to detonation; the **fuel's burn rate** sets MBT timing — keep them separate
([ignition.md → I1](ignition.md)). Ethanol barely knocks, so on E-heavy fuel the limit becomes
torque/EGT, not knock. Charge cooling + knock-suppression benefit from enrichment **saturates ~λ
0.76–0.78** ([fueling.md → F3](fueling.md)); richer buys EGT margin, not knock margin.

---

## Related documents

- [knock_frequency.md](knock_frequency.md) — bore → knock band, the `900` constant, Bessel-root modes (1.66×/2.08×), fuel/CR/humidity/water-injection sensitivity (all sub-band)
- [knock_voltage_cov_combustion_stability.md](../ai-analysis-skills/knock_voltage_cov_combustion_stability.md) — CoV-from-knock method (K1)
- [knock_sensor_baseline_vs_cylinder_uniformity.md](knock_sensor_baseline_vs_cylinder_uniformity.md) — variance as uniformity proxy (K2)
- [ignition.md](ignition.md) — the timing tables knock constrains
- [fueling.md](fueling.md) — per-cylinder trim (removes the maldistribution that walks the baseline)
