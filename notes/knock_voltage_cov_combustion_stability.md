# Knock-voltage scatter as a combustion-stability (CoV) proxy

Method for reading combustion quality from knock-sensor "chatter" — a way to rank one fuel/ignition map against another without a cylinder-pressure transducer.

> **Car-specific values live in the build working docs**, not here. For the reference build's worked results (the map-vs-map CoV comparison and dataset specifics) see [`supra/notes/knock_chatter_cov_results.md`](../supra/notes/knock_chatter_cov_results.md). This note is intentionally car-agnostic.

## The metric

`Knock voltage peak cyl N` = per-combustion-event peak of the band-pass-filtered
knock-sensor signal in that cylinder's window, one value per firing. Its cycle-to-cycle
scatter, on **no-knock** cycles, proxies combustion CoV (the structural analogue of
CoV-of-IMEP). Express scatter as a Coefficient of Variation (std/mean, %) — NOT raw std,
because the signal is heteroscedastic (swing scales with mean).

## The two methodological traps (both must be handled)

1. **Operating-point mixing (the big one).** The MEAN of this channel rises steeply and
   deterministically with RPM and load (mechanical engine noise). A naive std/mean over a
   coarse window is then dominated by that deterministic trend, so a log that merely
   *roams more of the boost map* looks noisier — a pure artifact.
   **Fix:** detrend within fine cells. Bin RPM × MAP finely (e.g. 250 rpm × 10 kPa),
   subtract each cell's local mean, normalize: `resid_norm = (peak − mean_cell)/mean_cell`.
   Then `corrected CoV = std(resid_norm)·100`. This isolates scatter *around* the local
   operating point and cancels any absolute-level offset between the groups being compared.

2. **Where you measure.** Map smoothness only bites while *interpolating across cells* —
   i.e. on transitions: accelerating through RPM (dRPM/dt > 0) or ramping into boost
   (dMAP/dt > 0). At steady state you sit in one cell and rough-vs-smooth washes out. So
   restrict to positive transients before measuring. (On a given car the high-MAP region
   may already be almost entirely transitional, in which case the transition gate barely
   changes the set and the operating-point detrend does the real work — check this per
   dataset.)

Also: no-knock cycles only (`Knocking cylinders == 0` AND cyl-N retard == 0). It's a
qualitative proxy, not a calibrated CoV-of-IMEP — use it to rank tunes, not as an absolute.
Ethanol blend and other uncontrolled run-to-run variables can shift the level, so compare
maps on like-for-like logs where you can.
