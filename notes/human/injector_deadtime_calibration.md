# Injector dead-time calibration

> Digest of [injector_deadtime_calibration.md](../injector_deadtime_calibration.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** filling the Injectors cal. table (`injOpeningTimeTbl`) from ID1050X manufacturer data — where errors bite, the conversion, and the post-import checks.

**The rules:**

- Dead time rises at lower battery voltage and higher effective fuel pressure. Getting it wrong skews mixture most where pulse width is short: idle and light cruise, plus transients that swing rail pressure.
- The Y axis is live effective (differential) fuel pressure — the table only indexes correctly once base pressure and `injectorsSize` are honest.
- Use the manufacturer's dynamic flow data, never hand-invented values. ID's psid rows map straight onto EMU's kPa-g rows (×6.895).
- Extrapolate the off-sheet edges (6–7 V, 17 V, 200 kPa) instead of clamping. The old flat table clamped and under-stated dead time at cranking voltage.
- The ID sheet's Slope (cc/min) column is the flow curve — it belongs to `injectorsSize`, not this table.
- Try EMU's Injectors wizard first for recognized injectors; use the repo script (`injector_deadtime_to_emubt.py`) when the model isn't listed or you want it on record.
- After import: the 500 kPa row (top of the grid) must show the HIGHEST dead times — if not, row order is flipped. Spot-check 400 kPa / 14 V ≈ 1.00 ms, then re-check idle lambda/STFT.

**Key numbers:** `injOpeningTimeTbl` is ubyte 12×4, scale 1/32 ms per count (`raw = round(ms × 32)`). This build's values run 0.72 ms (200 kPa / 17 V) to 3.00 ms (500 kPa / 6 V).

**When to care:** swapping injectors, changing base fuel pressure, or chasing idle/light-cruise mixture error that STFT keeps absorbing.
