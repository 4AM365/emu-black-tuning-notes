# Sensor and switch inventory — digest

*Digest of [`../sensor_inventory.md`](../sensor_inventory.md). The canonical note wins.*

## What this covers
Every sensor and switch the Supra's EMU reads as of 2026-09-28: input, type, supply, ground, and
a status judged on the 09-19 `fullchannels.csv`.

## The rules
- ECU is rev F (pre-"P"): A/C request, brake and clutch on `Switch 1/2/3` must see **sensor ground only**.
- EMU-fed 5 V sensors (TPS, PPS, fuel pressure) and both NTCs (CLT B5, IAT B32 → B29) return to EMU sensor ground.
- VR crank/cam: VR− to sensor ground, shield at one end. Knock sensors are **Bosch donuts** (2-wire, isolated): sensor ground + shield.
- Switchboard sensors return to the **Switchboard's** sensor ground.
- Flex fuel, WBO heater, EGT: general ground is fine.
- Status test: a one-sample drop to 0 faster than physics allows = wiring. A zero that is the true value = normal. Oscillation around a clean mean = noise, flagged.
- Function channels carry logic (`Brake pedal switch` = NOT `Switch 2`). That's configured, not a fault.

## Key numbers
- **Wiring (step functions):** VSS drops to 0 from 27–117 km/h in one sample (8×), plus a 270 Hz phantom.
  CAN Analog 4 (pre-throttle boost) and CAN Analog 3 (pre-IC temp) stepped together at 602 s with the engine off. Something they share changed.
- **Noisy:** CLT, IAT (being rewired block → SGND), oil pressure (CAN An 5), turbo speed. TPS is borderline (partly real plate motion).
- **Cleared:** A/C request chatter is down from 416 to 6.8 edges/min with the clutch pressed after the 08-29 clutch-ground fix.
- Back pressure is alive on CAN Analog 6; its zeros are atmospheric.

## When to care
Before rewiring, before trusting a Switchboard or speed channel, and whenever an input glitches.
