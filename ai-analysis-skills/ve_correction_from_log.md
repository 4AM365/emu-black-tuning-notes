# VE table correction from a closed-loop log (EMU Black, flex fuel)

> **Car-specific values live in the build working docs**, not here. For the reference build see [`supra/notes/`](../supra/notes/) — esp. [`my_car.md`](../supra/notes/my_car.md) and [`mass_flow_estimator_quirk.md`](../supra/notes/mass_flow_estimator_quirk.md). This note is intentionally car-agnostic.

Derivation and method used to correct `veTable` / `veTable2` from a closed-loop CSV log
(reference-build script lives under `supra/`).

## Per-cell correction factor

Injected fuel ∝ base VE × (1 + STFT/100) × (other corrections). With air fixed,
lambda is inversely proportional to fuel, so to make the base table deliver target
lambda with STFT back at zero:

```
new_VE = old_VE × (1 + STFT/100) × (λ_actual / λ_target)
```

- The `(1 + STFT/100)` term folds in the trim the ECU is *already* applying.
- The `λ_actual/λ_target` term folds in any residual error the loop hasn't caught.
- In settled closed loop, λ_actual ≈ λ_target, so the factor reduces to ~`(1+STFT/100)`.

## Use closed-loop samples only

Filter to `F.Short term trim == 1`. Open-loop samples (`F.Short term trim == 0`)
occur in the light-load / decel zone (target λ ≈ 1.0, STFT frozen) and are
transient-contaminated — the acc-enrichment filter only catches tip-*in*, not
throttle-lift. Including them produces spurious large negative corner corrections in
the low-MAP / low-mid-RPM decel zone that hit the clamp. Restricting to closed loop
bounds the correction to the genuine settled mixture error.

Full steady-state mask: `Lambda is valid==1 & F.Short term trim==1 & Fuel Cut==0 &
Overrun status<2 & ASE==0 & Warmup==0 & |Acc. enrichment %|≤1`.

**Gotcha:** `Overrun status` baseline is **1**, not 0 (1 = normal, 3/4 = active
cut). Filtering `==0` rejects the entire log.

## Distribute bilinearly, gate on dwell

Spread each sample's factor across the 4 surrounding cells by bilinear weight (same
as EMU's autotune accumulation), then correct a cell only if accumulated weight ≥
~25 (≈1 s @ 25 Hz). Clamp ±15 %/pass. Cells the engine never visited are left
untouched — expect corrections to concentrate at idle + light cruise on a street log
(no WOT, so injector duty stays low and the high-load/high-RPM corner is unvisited).

## Apply the SAME factor to both VE tables

Apply the same multiplicative factor to both `veTable` (pump) and `veTable2`
(ethanol). This preserves their existing relative offset and keeps `veTable2` valid
for future ethanol fills, instead of dumping the whole correction into the pump table.
When a log is captured at low ethanol content, the flex blend weights the pump table
heavily and the ethanol table carries little authority, so a single-table autotune
would leave `veTable2` stale. This is the key difference from a naive single-table
autotune.

**Justification — corrected (2026-05):** the original rationale here said "VE is
volumetric efficiency of air, fuel-independent, so the correction is identical for
both tables." That is the WRONG model for EMU. The ECUMaster VE table is a **fuel-dose
proxy**, not pure air VE (see `memory/emu_ve_table_is_fuel_dose_proxy.md`), so the two
flex tables legitimately differ by mixture/dose and need not move identically. The
real reason same-factor is a reasonable FIRST CUT: a closed-loop dose error measured
at one ethanol content corrects the *blended* result, and distributing it
proportionally keeps both tables in play until each is validated on its own fuel.
Where the two fuels want different mixtures (e.g. ethanol leaner at high load ->
lower veTable2), expect them to diverge — that is correct, not an error.

## Encoding facts

- `veTable` / `veTable2`: `u12`, row-major, **scale 0.1** (raw 444 → 44.4 %). The
  width (MAP columns) × height (RPM rows) match `mapBins` × `rpmBins`. Verify the
  scale against the log VE channel before applying corrections.
- `mapBins` / `rpmBins` carry the axis values (scale 1). Their span and count are
  build-specific — read them from the project, not from this note.
- Checksums go stale after editing `data`; EMU recomputes on import.
