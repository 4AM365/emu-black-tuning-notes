# Throttle body thermal growth (GS430 TB)

> Digest of [throttle_body_thermal_growth.md](../throttle_body_thermal_growth.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** this build's worked numbers for how the aluminum bore outgrows the stainless plate as the throttle body heats, and whether the implemented `idleCustomCorrection` matches the physics.

**The rules:**

- The bore (α 21.5 ppm/°C) grows faster than the plate (17.0). Idle flow is choked, so extra clearance is a direct mass-flow increase — at ΔT 50 °C that's +8 to +11%, biggest at low idle targets where the plate is nearly closed.
- TB growth alone justifies roughly 50–100% of the implemented `idleCustomCorrection`. The CAT 50 column matches almost exactly, so the table's zero-correction reference is ~CAT 25–30 °C.
- The −28% cell (CAT 70, 1000 rpm) is not an error — it matches the actuator-floor + extreme-soak (ΔT ≈ 80 °C) prediction almost exactly. It's sized for the worst-case hot-soak stall margin.
- Anything beyond ~−16% at CAT 70 needs a specific logged reason, not extrapolation.
- If you swap to a brass-plated throttle, the differential drops 3× and the current corrections would over-correct (~−3% predicted instead of ~−10%). Redo the table on any TB change.
- The lowered actuator floor is why the correction is so RPM-dependent; a higher floor would shrink the low-RPM magnitudes.

**Key numbers:** bore 73 mm; differential α 4.5 ppm/°C; actuator floor 2.4% TPS (`idleDBWTargetMin`), effective ~3.0%; +8–11% flow gain at ΔT 50 °C.

**When to care:** before editing `idleCustomCorrection`, after any throttle-body swap, or when hot-soak idle sags or hangs.
