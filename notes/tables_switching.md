# Tables switching — EMU Black settings and the principles behind them

> **Software page:** *Tables switching*. Full symbol catalog: [tune_feature_tree.md → Tables switching](tune_feature_tree.md). This is the page that **blends the dual (pump/ethanol) table sets by ethanol content** — the fuel/ignition/VE/cam tables it blends live on their own pages.

Organized like [idle.md](idle.md): settings first, then principles.

> **Car-specific values live in the build working docs**, not here — esp. the worked blend numbers
> referenced from [`supra/notes/`](../supra/notes/).

---

# Part 1 — Settings

### Flex-fuel input — `flexFuelEthanolContentBins`, `flexFuelSensorBins`, `ethanol10Bins`

- **What it is.** The flex-fuel sensor calibration (frequency → ethanol %) and the ethanol-content
  axis that every blend table is indexed on.
- **How to set it.** Standard GM-type flex sensor cal; any ethanol reading 0–100% is valid on this
  build (it fills to varying content). Only flag a **sensor dropout** (loss of FF input), not an
  unusual content value.
- **Live values:** build doc.

### Per-domain blend selectors — `tblsVE`, `tblsIGN`, `tblsASE`, `tblsCAM1` / `tblsCAM2`, `tblsCranking`, `tblsWarmup`

- **What it is.** The mode/config that says *how* each domain's two tables (table 1 = E0, table 2 =
  E100) combine — and on what axis.
- **How to set it.** Leave each on ethanol-content blending unless a domain intentionally uses a
  different axis. Confirm the mode before editing values — additive vs scalar vs blended changes what
  the stored bytes mean.
- **Live values:** build doc.

### Blend curves — `tblsVEBlend`, `tblsFFLambdaBlend`, `tblsFFCrankingBlend`, `tblsFFWarmupBlend`

- **What it is.** The actual weighting curve (table-1 weight vs ethanol %) for VE, lambda target, and
  the cold-enrichment tables. ubyte, 0.5% resolution.
- **How to set it.** **Derive the curve from EMU's `ethanolFuelScale`, not by intuition:**
  `table_1_weight(E) = 1 − ethanolFuelScale(E)/ethanolFuelScale(100)` (works in raw counts; the scale
  cancels). The curve is **nonlinear** — table-1 weight falls faster than ethanol % rises — so
  re-derive it, don't assume a straight line. Cold-enrichment blends are **not** stoichiometric
  compensators; they only set how fast the ECU moves from the E0 to the E100 extra-enrichment
  endpoint, and the wall-film tax is most ethanol-forward at cranking: `Warmup ≥ ASE ≥ Cranking`
  table-1 weight at the same content. Full method:
  [flex_fuel_ethanol_compensation_blend.md](flex_fuel_ethanol_compensation_blend.md).
- **Failure modes.** Reshaping a blend curve to dial in timing/fuel (wrong lever — advance table 2
  instead). Using one linear blend for all of VE/cranking/ASE/warmup.
- **Live values:** [flex_fuel_ethanol_compensation_blend.md](flex_fuel_ethanol_compensation_blend.md) + build doc.

---

# Part 2 — Principles

## TS1. The blend curve is derived, not drawn

When EMU's ethanol fuel-scale table already handles the stoichiometric fuel-mass change, the blend
curves must be **re-created from that fuel-scale table** so they don't double-count or fight it. The
table-1 weight = `1 − ethanolFuelScale(E)/ethanolFuelScale(100)` in raw counts. Because the fuel-scale
table is nonlinear, so is the blend — eyeballing a straight line mistimes the handoff.

## TS2. Don't tune *through* the blend — tune the endpoints

The blend scalar is a weighting, not a value. To change mixture or timing at a given ethanol content,
edit the **endpoint table** (table 2 for E100) and let the blend interpolate; reshaping the blend to
"get more timing" is the classic mistake ([ignition.md → Flex ignition blend](ignition.md)). The
blend scalar is < 1 at any partial content, so an endpoint delta delivers proportionally less at the
wheel — account for the blend fraction when stepping values.

## TS3. Identical endpoints → the blend does nothing

If VE1 and VE2 are the same model, `tblsVEBlend` has no fueling effect until VE2 is intentionally
tuned away from VE1. The flex tables legitimately diverge where the two fuels want different mixtures
(ethanol leaner at high load → `veTable2 < veTable`) — that divergence is the *point* of the blend,
not a bug ([fueling.md → F5](fueling.md)).

---

## Related documents

- [flex_fuel_ethanol_compensation_blend.md](flex_fuel_ethanol_compensation_blend.md) — full blend-curve derivation + cold-enrichment blends
- [fueling.md](fueling.md) — the VE / lambda / per-cylinder tables being blended
- [ignition.md](ignition.md) — flex ignition blend (advance table 2, don't reshape the curve)
- [engine_start.md](engine_start.md) — cranking/ASE/warmup blends
