# Idle session — 2026-05-24

> Digest of [idle_session_05242026.md](../idle_session_05242026.md) — the dense note is canonical; if they disagree, it wins.

**Finding (2026-05-24):** warm-idle PID sat saturated at its −10% floor and RPM hung at 1240 vs the 1200 target. The base airflow table was too high — per Banish, a saturated idle controller means fix the base table, not widen the PID limits.

**Action:** active airflow warm columns cut −8% on the 1200-rpm row and −4% on the 1000-rpm row. Predicted result: PID recenters to −2 to −5%, RPM hits target, ignition settles at the 18° idle target.

**Verified-current settings** (these override stale supra-specs entries): idle target 1200, idle lambda 0.93, overrun 3000/2950 rpm, warm cranking airflow 50%, idle ignition base 16.5° / controller target 18.0°.

**So-what:** some idle roughness is physics — ~30% residual gas at idle (Heywood) — so manage it, don't chase zero. Queued: drop the target to 1100–1150 in 50-rpm steps only after the airflow fix proves stable.
