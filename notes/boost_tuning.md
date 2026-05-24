# Boost Tuning

## How the model works
- EMU Black v3 uses a feed-forward system. A known value is fed in, measurements are taken, and then a correction is made with either PID, a known value, or a table.

- The base map needs to be set up experimentally. Override your WGDC in boost settings, do a pull, and log the result. If you reach 120 kPa boost at 45% WGDC for instance, go to the 120 column and enter 45 for that RPM.

- The nice thing about this is that as you climb in RPM, you can reduce WGDC to cancel out boost creep.

- I like to populate the region where the turbo isn't spooled with a high number like 100% to prioritize spool, then pull back the boost in the midrange to manage torque. After 5000 RPM, we can build boost again out to redline. Margin protection can also fill this role if you're careful with it.

- I also like to match boost to pedal position so the car is manageable. You don't want a big hammer of boost hitting whenever you breathe on the throttle — you want to ask for something and get it. The map peaks at the top right.

- Critically, you should know where your cams peak. Look at a dyno chart of your car with fixed boost, or an N/A version of the same engine. It's ideal to keep timing close to MBT in that region but pull back the boost for a more efficient burn and a flat torque profile.

- Not all cars need torque limited in the midrange. That said, almost all engines respond well to adding boost above the peak-torque RPM because mechanical advantage improves. There is little downside to this.

---

## Spool Retention Between Shifts

The exhaust manifold acts as a pressure reservoir. Pressure bleeds via turbine flow (productive) and via leaks and heat loss (not).

- Keep the wastegate shut during the shift window by commanding a high boost target at 0% PPS / high RPM in the boost target table. The ECU chases the target even though no boost is actually being made — WGDC stays high and the gate stays closed.
- Overrun fuel cut + DBW held open (10–15% TPS) converts the engine into an air pump: fuel is cut (no combustion, no drivetrain torque), but airflow through the cylinders keeps the turbine spinning. RPM still drops from drivetrain drag and pumping losses, but not catastrophically fast.
- Extended decel with the wastegate closed and fuel cut active risks a boost spike on re-engagement. Mitigate with a VSS threshold (activate only above 50–60 mph) — this captures shifting scenarios and avoids low-speed coasting issues.
- Boost target at 0% PPS / high RPM cells should be non-zero. Set to 60–80 kPa to maintain WGDC during overrun.

## Timing-Based Anti-Lag (Shift Strategy)

- Aggressive timing retard (15–25°) on clutch activation + RPM/speed gate dumps heat into the exhaust and keeps the turbine spinning.
- Gate conditions: RPM > 3000–4000, VSS > 20–30 mph, TPS recently high (>60% in last 500 ms), clutch switch active.
- Duration: 500–1000 ms max with a taper over the last 200 ms.
- Monitor EGTs — this raises exhaust temperatures significantly.

## Boost PID and Margin Protection

- Margin protection is a safety limiter, not closed-loop control. Traditional PID tuning logic does not apply.
- Distinguish between margin protection triggering (`Boost out of margin` = 1) and PID hunting (large oscillating `Boost PID correction`). These need different fixes: margin triggering means thresholds are too tight; PID hunting means gains are too aggressive.
- For a street tune with limited on-boost time: widen margin thresholds (±8–10 kPa) to reduce false triggers, and build the base WGDC table from logged ramp runs before activating PID.
- Build the feed-forward WGDC table from ramp-run data first. Establish the open-loop relationship, then layer PID on top.
