# The car — build sheet and constants

> Digest of [my_car.md](../my_car.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** the hardware list and the calibration constants every other note assumes.

**The rules:**

- 1994 JDM Supra SZ. Stock bottom end, GE VVT-i head, BC 264° cams, Borg S362 on an SPA manifold, custom 4" exhaust. R155 box, OSG clutch, GS430 diff.
- Fuel: twin AEM 50-1200 pumps, ID1050x injectors, flex-fuel sensor. E60 stoich ~11.0:1; WOT lambda target 0.80.
- Control: EMU Black (**hardware rev F, CPU G** — pre-"P", so its 3 built-in
  switch inputs are sensor-ground-only and can cross-corrupt each other) with
  ES330 throttle body (22030-20060, junkyard; plate material unknown) and GS430 pedal (full DBW), CAN Switchboard for sensors.
- The build-constants table lists the original 2.0–6.4% TPS↔airflow mapping — the live actuator range is 2.4–8.0 (see [airflow_actuator.md](airflow_actuator.md)). Don't compute from the old constants.
- Rev limit 7000; overrun fuel-cut exit 2050 rpm; drivetrain loss ~15% through the R155.
- Resonance-sensitive region around **5500 rpm** — be cautious adding load, advance, or aggressive lambda changes through it. Above it, add power more confidently once logs confirm lambda, knock margin, EGT, and drivetrain behavior.

**Key numbers:** hot idle airflow ~38%; compressor ~293 g/s at 5500 rpm / 107 kPa / 95% VE / 31 °C CAT; PR 2.06 at 107 kPa, 2.34 at 135 kPa.

**When to care:** any build-specific question — check here before assuming generic 2JZ hardware or targets.
