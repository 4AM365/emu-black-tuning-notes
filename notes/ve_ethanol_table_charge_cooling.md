# EMU VE tables are fuel-dose proxies — pump vs ethanol divergence is NOT a pure-air-VE question

> **Car-specific values live in the build working docs**, not here. For the reference build see [`supra/notes/`](../supra/notes/) — esp. [`my_car.md`](../supra/notes/my_car.md) and [`mass_flow_estimator_quirk.md`](../supra/notes/mass_flow_estimator_quirk.md). This note is intentionally car-agnostic.

## Correction to an earlier wrong call (2026-05)

A common mistake is to flag `veTable2` (ethanol) reading LOWER than `veTable` (pump) at
high load as a charge-cooling "physics violation," arguing that ethanol's evaporative
cooling should make its *air* VE higher. **That reasoning is wrong for EMU.**

**The ECUMaster EMU VE table is a value for FUEL DOSE calculation — only a rough proxy
of actual engine VE, not pure physical volumetric efficiency.** So the pump-vs-ethanol
difference is driven by MIXTURE / dose requirements, not air physics. If ethanol runs
a leaner mixture than E0 in a region, the ethanol map values get LOWER there.
Therefore `veTable2 < veTable` at high load is expected behavior, not a defect.

## What this means

- Do NOT apply first-principles air-VE reasoning (residual fraction, charge cooling)
  to decide what the *absolute* pump-vs-ethanol offset "should" be. Those physics still
  shape the overall map (the load-axis knee, the RPM hump are real — see
  `ve_idle_region_nonlinearity.md`), but the fuel/fuel offset between the two flex
  tables is a dosing choice that measured lambda + mixture intent drive.
- Charge cooling is a real effect, but on this ECU it is not expressed as "ethanol VE
  higher than pump VE." Don't expect that signature.

## Where the ethanol stoich/density fuel actually lives (NOT in VE2)

The big ethanol fuel increase (~+57% at E100, ~+44% at E85 — the 14.7/9.0 stoich mass
ratio less the density offset) is applied **automatically from ethanol content by a
dedicated fuel correction, separate from the VE table.** This is why `veTable2 ≈ veTable`
(or even `<`) is normal: VE2 only carries the *residual* dosing trim, not the stoich.

- **V3 firmware:** table **`ethanolFuelScale`** indexed by **`ethanol10Bins`** (E0→E100).
  Verified on the Supra V3 tune: raw `0 E 1D 2D 43 57 6C 85 A2 C2 E3` → at ×0.25 scale
  gives E0=0%, E50≈+22%, E85≈+44%, **E100=0xE3=227 ≈ +57%**. (Confirm the 0.25 scale in EMU.)
- **V2 firmware (e.g. project v2.175, Andrew's car):** the table doesn't exist; the
  equivalent is a single scalar **`ethanolScaleFactor`** (V2-only; V3 replaced it with the
  table above). Andrew's value `16400` most likely decodes ÷10000 = **1.64×** (up to +64%
  fuel at E100, interpolated by ethanol %). **Read the displayed value in EMU to confirm:**
  ~1.6 = correction active (VE2≈VE1 correct); ~1.0 = effectively off (then VE2 would have to
  carry stoich and the car leans on ethanol).

**Consequence / trap:** with `ethanolScaleFactor`/`ethanolFuelScale` active, do NOT bulk-add
the ~50% to `veTable2` — it double-counts and runs dangerously rich. The "VE2 should be ~57%
richer than VE1" instinct misattributes the stoich correction to the VE map.

## Still worth a real check (for the right reason)

If the available logs were captured at low ethanol content, the flex blend weights the
pump table heavily and the ethanol table carries little authority under boost — so its
high-load `veTable2` *dose* stays unverified. Confirm it against delivered lambda on a
high-ethanol boost pull, and let the measured mixture (not air theory) set the values.
