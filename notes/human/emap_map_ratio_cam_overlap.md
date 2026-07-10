# EMAP/MAP ratio and cam overlap

> Digest of [emap_map_ratio_cam_overlap.md](../emap_map_ratio_cam_overlap.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** how the exhaust-to-intake pressure ratio decides whether cam overlap helps or hurts, and how to schedule VVT-i from it.

**The rules:**

- EMAP/MAP > 1 → overlap backflows hot exhaust (reversion). < 1 → overlap flushes residuals out (scavenge). Overlap size only scales whichever the ratio picked.
- Measured on the Supra: ratio ≈ 1.0 at MAP 108–123 kPa, 0.83–0.93 at 137–181 — the boost region *scavenges*. Cruise is always ratio > 1 (mild internal EGR) by arithmetic.
- One phaser, two effects in lockstep: advance adds overlap AND closes the intake valve earlier. +5° advance ≈ +0.3 dynamic compression and ~3% more low-rpm trapped charge.
- All EMU cam numbers are crank degrees — halve for physical cam rotation. Card math: advertised overlap = 36 + advance; at 0.050" lift = advance − 10 (a gap below 10°).
- Cruise advance is deliberate dilution for pumping-loss economy. Rank cam by minimum fuel at fixed speed, never by MAP; then re-add spark for the slower burn.
- The knock chain under boost ends at spark: cam in → fuel up (fuel follows air) → spark down if knock. Never pull fuel from a knock-limited cell.
- Boost is allowed to wander: keep advance and spark falling as MAP rises past target, so overshoot self-protects.

**Key numbers:** `Back pressure` logs in **bar** (×100 for kPa). Baseline overlap 36° vs stock ~5–10°. DCR 8.15 parked → 9.15 at 20° advance.

**When to care:** before touching `cam1AdvTbl` or boost targets, and when diagnosing knock or fuel economy at cruise or under boost.
