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

## Idle-to-Driving Handoff Smoothness

When the idle strategy exits (PPS crosses `idleOffIfTPSOver`, or clutch releases at a non-zero PPS), three things release simultaneously:

1. The airflow PID I-term (`Idle PID air % correction` snaps to 0)
2. The idle ignition correction (timing returns to base — felt as a torque pulse independent of airflow)
3. The source switches from idle-influenced (state 2 or transitional state 3) to characteristic (source 0)

If PID has accumulated meaningful negative correction at the moment of release, the open-loop airflow it had been suppressing returns instantly, producing a small TPS step *and* a timing-advance step on top of whatever the pedal was already commanding. The driver feels a bump even with a gradual pedal input.

### The 1500 RPM row of `idleActiveAirflow` is the lever

The 1500 RPM (and adjacent high-target) row of the active airflow table is what's in play during the clutch-in cruise-decel handoff — as the idle target ramps down from a high value (cruise RPM) toward the warm idle target, it passes through the 1500 cell briefly. **If this row is over-prescribed, PID winds negative each transit, and that wound-negative PID is what releases when idle finally exits.** The 1500 RPM region of the idle ref table needs to be accurate (PID near 0 in steady armed/active conditions at that target) to prevent the bump during idle handoff. Validate by logging `Idle PID air % correction` while sweeping through the 1500 target band; PID should sit within ±3% in that band, not pegged.

### DBW blend point should track the idle ref table + a fixed driver-preference offset

`idleDBWBlendPointTbl` defines the TPS value at which the idle strategy is fully exited (the upper end of the idle-to-characteristic blend region). For the handoff to feel consistent across CLT, the blend point at each CLT bin should be set as:

```
blend_point[CLT] ≈ idle_TPS_at_CLT + Δ
```

where `idle_TPS_at_CLT` is the TPS that the idle controller is actually commanding at that CLT (derived from `idleActiveAirflow` mapped through the actuator range), and **Δ is a fixed driver-preference offset** — typically 4–8% TPS — that sets how wide the blend window feels.

This matters because:

- Idle's commanded TPS varies massively across CLT (~3.9% TPS at CLT 96 vs ~6.9% TPS at CLT 0 for target 1200). A fixed blend-point value would mean a much narrower handoff window when cold than when warm, making cold-start handoff feel abrupt and warm handoff feel mushy.
- Using a fixed Δ above idle's TPS keeps the blend window's *perceived width* constant. The driver always gets the same amount of pedal travel between "idle is letting go" and "characteristic fully in charge."
- If `idleActiveAirflow` is rescaled (e.g., the 1500 or 1375 rows are dropped to fix PID accumulation), the blend point table **must be re-derived** off the new active values. Otherwise the blend window grows or shrinks unintentionally at the cells you just changed.

Practical method: after any change to `idleActiveAirflow`, compute the idle-TPS for each CLT bin from the warm-idle-target row used at that CLT, then write `blend_point = idle_TPS + Δ` into `idleDBWBlendPointTbl`. Test with a clutch-in cruise-decel and a steady pedal tip-in — the bump should be uniform across CLT.