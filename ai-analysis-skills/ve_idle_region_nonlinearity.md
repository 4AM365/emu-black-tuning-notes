# VE is genuinely second-order in the idle / low-load region (do not over-smooth)

> **Car-specific values live in the build working docs**, not here. For the reference build see [`supra/notes/`](../supra/notes/) — esp. [`my_car.md`](../supra/notes/my_car.md) and [`mass_flow_estimator_quirk.md`](../supra/notes/mass_flow_estimator_quirk.md). This note is intentionally car-agnostic.

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

## When it bites hardest

Both mechanisms are strong on a large-cam + active-VVT engine. The idle knee shows up
as a low-RPM `veTable` row that climbs steeply out of deep vacuum, then **plateaus**
across the mid-MAP columns. A single global cubic over the full `mapBins` × `rpmBins`
range flattens this and (per Banish) invites idle surge and tip-in hesitation.

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
  high-load plateau survive intact. Verified in practice: with delta-overlay a
  low-RPM row's high-MAP cells come out byte-identical to base, knee preserved,
  while the low-MAP cells carry the smooth correction.
- This is simpler AND more faithful than chasing polynomial order — it cannot
  destroy a feature it never touches, and it sidesteps deep-vacuum corner
  extrapolation. (Reference-build pipeline lives under `supra/`.)

## RPM-axis caveat: freezing unaltered cells can violate the VE hump

Delta-overlay preserves base off the band, but that creates a trap on the SPEED
axis: if the autotune raises a mid-RPM cell while the unvisited cells ABOVE it (still
below the engine's VE peak RPM) stay at base, the corrected cell
can poke above them — a false local peak below the peak and a non-physical double hump.
VE must rise monotonically to its peak, so unaltered cells above an upward correction
must be lifted too. Fix: extrapolate the correction UP the RPM axis — hold the top
anchor's delta from the band top to the peak bin, then taper to 0 by redline. This
yields a single hump peaking near the engine's VE-peak RPM. Add a per-column
non-decreasing-to-peak cummax as a cheap safety net. Verified in practice: a low-MAP
column went from a false mid-RPM peak + dip to a clean monotone rise peaking at the
VE-peak bin, declining gently to redline.
"Unaltered" cells are not sacred on the RPM axis — physics (the hump) outranks them.

## Off-band anchor blocks are real; apply airflow corrections to BOTH VE tables

When deriving anchors from `T != base`, distinguish **coherent blocks** from
**scattered noise**. Scattered sub-percent specks in no-data regions are screenshot
transcription noise — exclude them. A **contiguous block with consistent magnitude**
(e.g. a few adjacent cells all reading a similar small positive correction in a
high-load/high-RPM patch) is a real correction even if it sits outside the main
idle/cruise band — include it.

When such a block is real, apply the same delta to **both** `veTable` (pump) and
`veTable2` (ethanol), each on its own base so their relative offset is preserved —
even if the block only appeared in one table's autotune screenshot.

**Caveat (2026-05):** justifying "both tables" by claiming VE is fuel-independent
air VE is WRONG for EMU — the VE table is a fuel-dose proxy (see
`ve_ethanol_table_charge_cooling.md`). Same-delta-to-both is still a fine
first cut for an airflow-ish modeling error, but the two tables legitimately diverge
where the fuels want different mixtures; don't treat their offset as a bug.
