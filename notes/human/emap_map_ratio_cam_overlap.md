# EMAP/MAP ratio and cam overlap

> Digest of [emap_map_ratio_cam_overlap.md](../emap_map_ratio_cam_overlap.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** how the exhaust-to-intake pressure ratio decides whether cam overlap helps or hurts, and how to schedule VVT-i from it.

**Status (corrected 2026-09-28):** the sender is alive. It sits on the CAN Switchboard (`CAN Analog 6`), not ECU `Analog 6`, and reads 0.28 bar under boost in the 09-19 `fullchannels.csv`. Zero readings in idle-only logs are just atmospheric pressure. Any logged pull can judge the new damper.

**The rules:**

- EMAP/MAP > 1 → overlap backflows hot exhaust (reversion). < 1 → overlap flushes residuals out (scavenge). Overlap size only scales whichever the ratio picked.
- Measured on the Supra: ratio ≈ 1.0 at MAP 108–123 kPa, 0.83–0.93 at 137–181 — the boost region *scavenges*. Cruise is always ratio > 1 (mild internal EGR) by arithmetic.
- One phaser, two effects in lockstep: advance adds overlap AND closes the intake valve earlier. +5° advance ≈ +0.3 dynamic compression and ~3% more low-rpm trapped charge.
- All EMU cam numbers are crank degrees — halve for physical cam rotation. Card math: advertised overlap = 36 + advance; at 0.050" lift = advance − 10 (a gap below 10°).
- Cruise advance is deliberate dilution for pumping-loss economy. Rank cam by minimum fuel at fixed speed, never by MAP; then re-add spark for the slower burn.
- The knock chain under boost ends at spark: cam in → fuel up (fuel follows air) → spark down if knock. Never pull fuel from a knock-limited cell.
- Boost is allowed to wander: keep advance and spark falling as MAP rises past target, so overshoot self-protects.

- Re-checked 2026-07-18 after the DBW boost-region rework: crossover still holds, ~0.03–0.05 lower at the bottom of boost (more open throttle → turbine works less for the same MAP). One thin log; suggestive, not proven.
- **Crossover is lost above ~6000 rpm** (07-19 data): ratio goes 0.88 → 0.87 → 0.90 → **1.04** across 4000→7100 rpm. Not a lift-off artifact — steady, rising, and falling samples all agree. So don't add advance above ~5300 rpm; the boost-column proposal assumes scavenging that isn't there at redline.
- Mixture under boost runs *rich* of target (−5.2% median), not lean — but thins with RPM (−9.5% at 3500–4500, +1.6% at 5500–7100). That's a VE RPM-slope shape, not an offset. Can't yet blame the DBW rework: pre-rework logs are thin and disagree, and ethanol wasn't logged.
- The vacuum columns are a sensor floor, not a measurement: gauge channel pins at 0, so anything below MAP ~105 is just `100/MAP`.
- A high ratio is not "unwastegated + choked." It's turbine PR from the power balance: too little turbine flow capacity, off-peak turbine efficiency, low EGT, or high compressor demand. Choke is the extreme tail of the first.
- The wastegate is a parallel path, not an EMAP reducer. Gate shut below target is normal (that's where spool ratios are worst); an undersized gate can be wide open and still be the restriction (boost creep).
- Ratio drives overlap gas direction; *absolute* EMAP drives pumping loss. Different problems, same cause — here absolute EMAP rises with boost while the ratio falls.

**Key numbers:** `Back pressure` logs in **bar** (×100 for kPa). Baseline overlap 36° vs stock ~5–10°. DCR 8.15 parked → 9.15 at 20° advance.

**When to care:** before touching `cam1AdvTbl` or boost targets, and when diagnosing knock or fuel economy at cruise or under boost.
