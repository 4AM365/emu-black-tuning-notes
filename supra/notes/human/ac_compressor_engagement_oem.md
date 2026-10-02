# OEM A/C engagement — plain version

**What this covers:** what the factory JZA80 (JDM SZ) had to see before the A/C
compressor clutch would pull in. Canonical note:
`supra/notes/ac_compressor_engagement_oem.md`.

## The rules
The A/C amplifier decides, but the **engine ECU actually closes the clutch relay**.
Amp raises a request on MGC → ECM sees AC1 → ECM drives ACMG → relay → clutch.
Either box can say no.

Amp needs all of: A/C switch (or AUTO) on, blower running, refrigerant pressure
inside the window, evaporator not near freezing, and the compressor lock sensor
showing the compressor is actually turning with the belt.

ECM vetoes it during hard low-speed acceleration, and any time the amp flags a
pressure fault.

## Key numbers
- Pressure cut: below 196 kPa (2.0 kgf/cm², 28 psi) or above 3,140 kPa (32.0 kgf/cm², 455 psi)
- Compressor lock trip: ≥450 rpm and compressor/engine speed ratio off by ≥20 % for ≥3 s → clutch off, A/C light blinks ~1 Hz
- ECM A/C cut: ≤25 km/h, ≤1,200 rpm, throttle ≥60° → clutch drops for a few seconds
- Evaporator sensor is a thermistor (4.5–5.2 kΩ @ 0 °C); the manual never states
  the frost cut-out temperature — don't quote one as fact
- OEM idle-up on engagement: GE M/T 700→900, GE A/T 700→800, GTE 650→800 rpm

## When to care
Any standalone-ECU A/C wiring or idle-up work: the clutch request has to route
through (or be replaced by) the ECM leg, and the lock sensor + pressure switch
interlocks live on the amplifier side, unchanged.

## What the A/C computer needs to see
Power: constant +B (ECU-B fuse, holds memory), IG, ACC, ground, panel dimming.
Command: the A/C control switch panel.
Sensors: room temp, ambient temp, solar, evaporator temp, and its **own** coolant
temp sensor (separate from the engine ECU's).
Positions: air mix damper, air outlet damper.
Interlocks: refrigerant pressure switch(es), compressor lock sensor, engine rpm
from the igniter, clutch-engaged feedback, and the engine ECU leg.
No vehicle-speed input.

Worth knowing: the condenser fans are switched by the pressure switch and a
condenser-fan water temp switch — not by the A/C computer. They can fail to run
without the computer knowing, which is the fastest route to a high-pressure cut
at hot idle.

**Before blaming the amplifier:** the EMU's own request input chatters at ~7 Hz
whenever the clutch pedal switch is closed, and that — not `acMinRPM` — causes
most logged compressor drop-outs. See
[A/C request input noise](ac_request_input_noise.md).

## The EMU gate: no A/C at idle, ever (2026-09-08)

*Holds only while `acMinRPM` sits above the idle target. On 2026-10-01 Will ran it at ~800 to test A/C at idle —
see `log_2026-10-01_new_cranking_rules.md`.*

The clutch output in this tune is **gated at 1800 rpm**, far above any idle
target, so the compressor and the idle controller never run at the same time.
Measured in `goodlog.csv`: clutch engaged for 37 % of the log, **minimum RPM
1804, zero samples under 1800**, and never once while `Idle state` = ACTIVE.

Two things follow, and they keep getting re-derived wrongly: **there is no A/C
load step onto an idling engine on this car** — don't model one or size idle
airflow authority against it — and **`idleACRPMIncrease` is inert**, because the
target increase only applies while the clutch is in.
