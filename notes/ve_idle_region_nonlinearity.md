# VE is genuinely second-order in the idle / low-load region (do not over-smooth)

When smoothing or interpolating a VE table, the idle / low-RPM / low-MAP corner
carries a **real nonlinear feature** that low-order global polynomial fits wash out.
Two independent mechanisms, both documented in the repo corpus:

## 1. Residual-gas knee on the load (MAP) axis — Heywood §6.4

Residual gas fraction is "primarily a function of intake and exhaust pressures,
engine speed, compression ratio, valve timing" (Heywood, *Internal Combustion
Engine Fundamentals*, §6.4, Figs 6.25–6.26). At low MAP the clearance-volume
residuals sit near exhaust pressure (~1 bar) while fresh charge arrives at ~0.35 bar,
so burned gas back-flows into the intake and dilutes the fresh charge. Residual
fraction climbs steeply as MAP drops below ~0.5 bar → VE is **depressed and
concave** at low manifold pressure. Result: VE-vs-MAP rises steeply out of idle,
then plateaus — a knee in the low-MAP corner, NOT a straight line.

## 2. Cam inflection on the speed (RPM) axis — Banish

A larger-than-stock cam "shifts the power band upward in speed... low RPM
volumetric efficiency usually drops from stock. Somewhere in the midrange there
will be an **inflection point** where the new VE matches the stock values" (Banish,
*Engine Management: Advanced Tuning*, p.523). Mis-modeling it causes the exact
failure mode "idle speed changes are met with slight over-fueling... leading to
surging" and "higher RPM tip-in events would be under-fueled, leading to
hesitation or bucking."

## Applies to this build

The Supra runs 264° cams + active VVT — both mechanisms are strong here. The idle
knee is visible in the base `veTable`: e.g. the 1184-RPM row rises 41→48→60% then
**plateaus** ~61.5% from 79–137 kPa. A single global cubic over the full
20–240 kPa / 500–7000 rpm range flattens this and (per Banish) invites idle surge
and tip-in hesitation.

## Practical rule

- "Smooth and linear" is correct for the high-load plateau; it is wrong for idle.
- A global low-order polynomial fit of **absolute VE** is dominated by the broad
  smooth high-load region and **rounds the sharp idle knee off** (a quartic still
  can't hold a slope that drops from +6.5%/cell to ~0 in one step). Raising order
  just starts to oscillate.

## Method that preserves it: smooth the CORRECTION, not absolute VE

When applying autotune/log corrections, use **delta-overlay**:

    final = base + smooth(autotune_delta)

- `delta = autotune − base`, nonzero only where the autotune had data (the
  operating band); project it outward (reach-capped inverse-distance), then smooth
  the small correction surface with a light separable [1,2,1] blur (2 passes).
- Add back to base. Because the blur decays to ~0 off the band, every untouched
  cell **stays exactly at base** — so the residual knee, cam inflection, and
  high-load plateau survive intact. Verified: with delta-overlay the 1184-rpm row's
  high-MAP cells (137–240 kPa) come out byte-identical to base, knee preserved,
  while the low-MAP cells carry the smooth correction.
- This is simpler AND more faithful than chasing polynomial order — it cannot
  destroy a feature it never touches, and it sidesteps deep-vacuum corner
  extrapolation. Pipeline: `supra/tunes/ve_smooth.py`.

## RPM-axis caveat: freezing unaltered cells can violate the VE hump

Delta-overlay preserves base off the band, but that creates a trap on the SPEED
axis: if the autotune raises a mid-RPM cell while the unvisited cells ABOVE it (still
below the engine's VE peak, ~5500 rpm on this build) stay at base, the corrected cell
can poke above them — a false local peak below 5500 and a non-physical double hump.
VE must rise monotonically to its peak, so unaltered cells above an upward correction
must be lifted too. Fix: extrapolate the correction UP the RPM axis — hold the top
anchor's delta from the band top to the peak bin, then taper to 0 by redline. This
yields a single hump peaking near 5500. Add a per-column non-decreasing-to-peak
cummax as a cheap safety net. Verified: the MAP79 column went from a 4947-rpm false
peak + 5974 dip to a clean monotone rise peaking at 5632, declining gently to 7000.
"Unaltered" cells are not sacred on the RPM axis — physics (the hump) outranks them.

## Off-band anchor blocks are real; apply airflow corrections to BOTH VE tables

When deriving anchors from `T != base`, distinguish **coherent blocks** from
**scattered noise**. Scattered ±0.3–0.9% specks in no-data regions are screenshot
transcription noise — exclude them. A **contiguous block with consistent magnitude**
(e.g. VE2 autotune showed +2.1/+2.7/+2.8/+3.2% at 152–167 kPa, 4600–5300 rpm) is a
real correction even if it sits outside the main idle/cruise band — include it.

A real correction was applied to **both** `veTable` (pump) and `veTable2` (ethanol),
each on its own base so their relative offset is preserved. The boost block above
appeared only in VE2's autotune screenshot, but was injected into VE1 too — same
delta, each on its own base (VE1 4947/152: 74.9→77.5; VE2: 73.2→75.9). Pipelines:
`ve_smooth.py` (VE1), `ve2_smooth.py` (VE2).

**Caveat (2026-05):** I justified "both tables" by claiming VE is fuel-independent
air VE. That model is WRONG for EMU — the VE table is a fuel-dose proxy
(`memory/emu_ve_table_is_fuel_dose_proxy.md`). Same-delta-to-both is still a fine
first cut for an airflow-ish modeling error, but the two tables legitimately diverge
where the fuels want different mixtures; don't treat their offset as a bug.
