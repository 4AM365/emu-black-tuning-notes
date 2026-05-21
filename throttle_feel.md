# Throttle Response Tuning

Throttle response feel is determined by three factors:

1. TPS rate limit
2. DBW characteristic
3. Boost vs. PPS mapping

---

## TPS Rate Limit

Controls the "bucking" sensation at low speed by limiting how quickly the throttle body opens or closes.

The adjustment range is 0–1300°/sec, with a 125°/sec RPM-referenced adjustment range added on top of the selected value. Start at a conservative value and increase it until response feels snappy enough.

### What I Tried

My first instinct was to set it much lower at low speeds and much higher at high speeds. When I set the universal limit around 250°/sec (where it actually affects physical sensation), it interfered with DBW throttle body operation at idle.

### What Worked

I settled on a universal limit of **700°/sec**, actually *reducing* the limit at high speed so lift-off behavior is gentler under high power.

> **Note on engine protection:** Lift-off rod failures are a real risk on high-boost engines. The mechanism: when you lift off at high RPM, MAP drops, overrun fuel cut activates, and the drivetrain drives the engine rather than the other way around. Every piston on the power stroke is now being *pulled* down by the crank with no combustion pressure behind it — loading the rod in tension, which rods handle far worse than compression. The more direct mitigations are overrun fuel cut strategy (minimum RPM threshold, hysteresis, partial fuel reduction instead of a hard cut) and ignition cut instead of fuel cut. A slower throttle closure rate delays MAP drop and thus fuel cut onset, so it helps indirectly, but it's not the primary lever.

### The Real Fix

Parking lot jerkiness was ultimately solved with a **scooped DBW characteristic under 50% PPS**, while bumping up the characteristic above 50% PPS so throttle blips remain effective for downshifts.

---

## DBW Characteristic

This makes a bigger difference than TPS rate limit.

A linear mapping at high RPM gives the most predictable closing feel. However, it can be beneficial to blow the throttle body open early to increase system efficiency, then control power level by selecting wastegate duty cycle based on pedal position.

---

## DBW Characteristic Type

You can define DBW characteristic and rate limit based on **MAP** instead of RPM.

### Potential Issue

This creates potential for circular logic: a "gentle" throttle map at low MAP means you never get enough TPS to actually build MAP, even though WGDC will be higher (since it's PPS-based).

### My Preference

I like the car to feel "ready to launch"—get MAP up early, then use TPS to apply power. This also means **pre-throttle boost reference vs. MAP** is preferable: you can have whatever pressure you need in the intake plenum based on power demand, with power "ready to go" in the charge pipes.

---

## Creep and Low-Speed DBW

The DBW characteristic map has no VSS or gear input. The RPM axis provides implicit partial gear awareness — first-gear creeping naturally lives in the low-PPS/low-RPM quadrant, with limited overlap against higher-gear operation at the same RPM.

- Primary tool for creep behavior: soften the low-PPS/low-RPM quadrant of the characteristic map.
- The TPS rate limit controls transient rate (how fast the throttle moves), not steady-state target. A conservative rate limit affects blip response — asymmetric open/close rates are preferable if the ECU supports them.
- Consider raising the idle closed-loop cutoff threshold so the idle PID stays active into the low-speed creeping range, rather than operating in a hand-off zone between idle control and driver demand.

## Off-Throttle Parachute Feel

Abrupt lift-off causes the powertrain to rock and the driveshaft to unwind — a "parachute" sensation.

- The armed state airflow table is the primary lever: hold higher airflow at high RPM with PPS = 0 to prevent an instant torque drop to zero. The trade-off is reduced engine braking feel.
- EMU does not support context-aware TPS closing rates based on PPS rate of change (as OEM calibrations do). Work around it with armed state and accept the trade-off.
- Decel ignition retard tables can soften the power-off transition as a secondary tool.

## Decelerate Fuel Correction

The decelerate fuel correction table can fire negative acceleration enrichment during recovery phases — trimming fuel in the wrong direction at low RPM. Review the RPM floor for decelerate correction; it may need to be raised to avoid activating during idle recovery.