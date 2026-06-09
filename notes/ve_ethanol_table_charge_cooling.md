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

## Still worth a real check (for the right reason)

If the available logs were captured at low ethanol content, the flex blend weights the
pump table heavily and the ethanol table carries little authority under boost — so its
high-load `veTable2` *dose* stays unverified. Confirm it against delivered lambda on a
high-ethanol boost pull, and let the measured mixture (not air theory) set the values.
