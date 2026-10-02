# Functions — settings reference

> **Software page:** *Functions*. Full symbol catalog: [tune_feature_tree.md → Functions](tune_feature_tree.md).

User-configurable functions layered on top of the engine maps — cruise control, fan/AC/water-meth triggers, diff control, and the custom function/map outputs (programmable logic on any input).

This is largely **configuration**, not tuning-principle territory — the exhaustive symbol list is in the catalog. This page is the home for any tuning notes that arise for this feature; the sub-nodes below mirror the software tree.

## Sub-nodes

- **Diff control** (26) — `diffCtrlDCTbl1Acc`, `diffCtrlDCTbl1Brk`, `diffCtrlDCTbl2Acc`, `diffCtrlDCTbl2Brk`, `diffCtrlDCTbl3Acc` …
- **Fan / AC / water-meth** (26) — `acEvapCal`, `acEvapCalBins`, `acActivation`, `acEvapMinTemp`, `acEvapTemp` …
- **Cruise control** (18) — `ccTargetSpeedBin`, `ccDeadband`, `ccIntegralLimitMax`, `ccIntegralLimitMaxRate`, `ccIntegralLimitMin` …
- **Custom functions / maps** (12) — `customFX2Bins8`, `customFX3Bins8`, `customFXBins8`, `customFY2Bins8`, `customFY3Bins8` …
- **Math / logic** (1) — `userFunctions`

## `userFunctions` encoding (decoded 2026-10-02, Supra export 13:54, fw 3.071)

380 bytes = 12 function records × 13 B + 32 operator records × 7 B.
- **Function record:** name (8 B ASCII, zero-padded) · output · action · (1 B, unknown) · first-operator index ·
  operator count. Virtual output = 0; "Set output only" = 0.
- **Operator record (7 B):** constant (u16 LE) · channel id · 3 B unknown (delays/flags; GUI showed 0.1 s / 0.1 s) · **type**.
  Type codes seen: 0 = Is True, 1 = Is False, 4 = Less, 6 = Greater. These fit the help's order (Equal 2,
  Not Equal 3, Less or Equal 5, Greater or Equal 7 presumed). Channel ids seen: 0x10 `Switch 1`, 0x11 `Switch 2`,
  0x39 `Engine runtime`.
- **Input selectors:** Fn n = 19 + n (`brakePedalInput` 21 = Fn 2 "Brakeinv" = `Switch 2` Is False;
  `lcActivationInput` 22 = Fn 3; `ralInput` 23 = Fn 4; `latchingSwitchInput` 25 = Fn 6; `acActivation` 26 = Fn 7).
- An empty operator line in the GUI is a real operator: it uses a slot, and the free-operator count shows it.
- Supra Fn 7 "AC Delay" = `Engine runtime` > 10 AND `Switch 1` Is True → `acActivation`. Rationale:
  [supra/notes/log_2026-10-02_restartbounce.md](../supra/notes/log_2026-10-02_restartbounce.md).
