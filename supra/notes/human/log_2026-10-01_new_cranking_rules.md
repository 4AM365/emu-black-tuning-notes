# Log 2026-10-01 (`new_cranking_rules.csv`) — plain version

**What this covers:** the first log on firmware 3.071: the load warnings, A/C at idle, and the cold start.
Canonical note: `supra/notes/log_2026-10-01_new_cranking_rules.md`.

## The rules
- The 72 "Cannot find symbol" warnings are all new 3.071 features at their defaults. Nothing of the tune was lost.
- Two things did change underneath: the rev-limiter cut-percent setting was replaced by a "cut pattern", and the
  internal wideband's calibration tables were replaced. Check the limiter; expect the λ reading might have moved.
- A/C at idle cycles because the request line (`Switch 1`) blips for ≤ 40 ms. Each blip drops the clutch for the
  engage delay while the extra air stays on → flare → PID pulls air → clutch re-engages short of air → dip to ~800 →
  the A/C min-RPM gate drops it again. Fix the blips first (new switch debounce setting, or a relay so the pin only
  ever sees sensor ground).
- Fresh A/C engagements with the feed-forward only dip ~75 rpm. The feed-forward works.
- Release flares because the clutch and the extra air drop together. Proposal: two spare functions — one debounces the
  request and drives the air correction, the second follows it with a ~0.5–0.6 s off-delay and drives the clutch.
- IAT is not ambient at idle here: it climbed 22 → 46 °C at a constant ~26 °C ambient, and the A/C air need didn't
  follow it. Use head pressure or a real ambient sensor for the A/C table's temperature axis.
- Cold start: attempt 1 hovered at 300–480 rpm (VE lean-out had cut the cranking dose ~8 %); after the table edit,
  attempt 2 caught in 0.4 s.
- Post-start overshoot (1991) is manifold discharge + the 24° ignition lock. The wiggle is the PID engaging at the
  peak and cutting air at the same moment the lock released — the lock (0.6 s) outlasted the afterstart delay
  (0.4 s), which the start note already forbids. Keep lock ≤ delay; the 24° angle itself is fine. Holding the throttle longer lands cleanly on a cold
  start. The hot cranking-airflow bin is sized for hot coolant + cold oil on purpose (~34 %, vs ~20 % once the oil is
  hot) — don't lower it; a long hold on a hot-oil restart just sits high until the PID trims it.

## Key numbers
- A/C air need at 1025 hot: **+14.2 air-%** (MAP +5.4 kPa). The compressor load is a roughly fixed torque; the air to carry it grows ×1.0–1.2 from 1025 to 1250. Ambient: ~0.23 air-%/K (≈ 10 on a 10 °C day, ≈ 17 at 40 °C), probably more on hot days.
- Request blips: 2.4/min clutch released, 68.6/min clutch pressed.
- Afterstart delay: 4 = 0.4 s (0.1 s/count). Cold cranking airflow 80 % ≈ sustaining 76–80 % at 1425.

## When to care
Any A/C-at-idle tuning, any start/afterstart change, and before trusting λ across the 3.071 update.
