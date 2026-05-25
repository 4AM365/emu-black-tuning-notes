# Idle Session — 2026-05-24 (Supra build-specific)

Build-specific findings and decisions for the 2JZ-GE + VVT-i head + 264° cams + 10:1 CR + ID1050X + E25–E60 flex setup. Generic principles live in `notes/cranking_and_idle.md`; this file holds the verified state, the empirical observations against logs, and the decisions made for this engine.

## Findings from driving log (37 MB, 14.6 min, ~12 sec warm idle)

- PID **saturated at floor (−10%)** during warm idle. RPM hung at 1240 vs 1200 target.
- I.Idle correction near zero at steady state — base ignition table was the actual output.
- Banish (p.3470) on this exact signature: *"If the IAC displays as either all the way open or closed at all times, it's time for a throttle stop adjustment. The more range the IAC motor has in both directions, the better chances it has of controlling a stable idle speed."* The intervention is to fix the base airflow table, not widen PID limits.

## Action taken: `exports/Airflow - Active state air flow [%].emubt`

| Cell | Before | After | Δ |
|---|---|---|---|
| Row 2 (≈1200 RPM band), cols 4–7 (CLT 60/75/96/105°C) | 50, 50, 49.5, 49.5% | 42, 42, 41.5, 41.5% | −8% |
| Row 1 (≈1000 RPM band), cols 4–7 | 37.5, 36, 37.5, 37.5% | 33.5, 32, 33.5, 33.5% | −4% |

Predicted outcome: PID centers around −2 to −5%, RPM reaches target, I.Idle correction near zero, Ignition Angle settles at ~18° (the idle target).

## Verified-current settings (overriding stale supra-specs entries)

| Setting | Value | Notes |
|---|---|---|
| Idle RPM target (warm) | 1200 | Raised from 1100 for IAT stability buffer — drivetrain inertia rides through hot-day misfires |
| Idle lambda target (E0 endpoint, idle cells) | 0.93 | Slight enrichment for stability, well clear of bore-wash (~0.85) — Banish-aligned |
| Overrun enter / exit RPM | 3000 / 2950 | 50 RPM hysteresis. In Banish's recommended range for cam/comp |
| Overrun exit fuel enrichment | 16% with 2%/cycle decay | Conservative — avoids rich stumble post-cut |
| Overrun ignition enter / exit rate | 3° / 0.5° per cycle | Asymmetric: cut fast, restore slow |
| PPS hysteresis | 2% active / 3% inactive | 1% gap prevents flicker on pedal jitter |
| Cranking airflow (warm) | 50% | Excellent hot start — close to idle airflow demand (see principle in cranking_and_idle.md) |
| Idle ignition base (E25, warm idle cell) | 16.5° | Below MBT, leaves reserve. Per cammed/ethanol guidance |
| Idle ignition target | 18.0° (warm cells, flat across RPM) | ±10° controller swing range |

## Optional refinements queued

- **Idle RPM target reduction**: 1200 → 1100–1150 after airflow fix proves stable, per Banish "reduce 50 RPM at a time" approach. Hold at 1200 for now given IAT history.
- Everything else: nothing to do.

## Source synthesis on idle physics (relevant background)

Heywood (*Internal Combustion Engine Fundamentals* Ch. 6.4): residual gas fraction at idle is **~30%** on a throttled SI engine. The engine is intrinsically running on a 30% EGR'd charge at idle. Cycle-to-cycle combustion variability is inherent at light load — Heywood Ch. 9: "acceptable COV of imep is a few percent, depending on load." Some idle roughness is physics, not a tune bug; the tune's job is to manage it, not eliminate it.
