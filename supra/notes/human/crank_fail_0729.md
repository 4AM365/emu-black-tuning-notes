# Crank fail, 29 Jul 2026 — why it wouldn't light (human digest)

Digest of [crank_fail_0729.md](../crank_fail_0729.md). Canonical note wins on any conflict.

**What this covers:** a no-start that turned into a multi-day tail-chase. Real cause was simple;
the detour was long.

**The resolution (start here):** over-fueling during cranking fouled all six plugs (#6 wettest —
it carries a +8% per-cylinder cranking trim). After that, nothing could fire, so every fuel/air
experiment — including the throttle-restriction "make vacuum" attempts — was a fouled-plug no-fire,
not a verdict on the strategy. The long-crank pattern is drowning it and waiting for a spark to
punch through a wet plug.

**Fix (old-school recipe):**
1. Clean/replace all six plugs — the actual blocker; everything else is moot until they arc.
2. Way less cranking fuel — undo the additions, err lean (the window is wide, ~3:1 on vapor λ).
3. Crank at the post-start landing airflow, foot OFF. Landing = Active airflow **1500-rpm row**:
   87.5 / 75 / 62 / 52 / 47.5 / 45 / 45 / 45 % across CLT 0→105. Cold cranking airflow is already
   86% ≈ that 87.5%, so for a cold start the throttle already cranks where it lands. ~98 kPa, fine.
4. Keep `idleDBWTargetMin` at 2.4% (it's the idle anti-stall floor — don't lower it for vacuum).
5. Prime the rail to 4 bar before the starter engages. Foot off — pedal past ~33% TPS trips the
   anti-flood fuel cut (flood-clear, not a start).

**The physics detour (true, but not the problem here):** the spark sees vapor, the table commands
liquid — vapor λ = liquid λ ÷ U (evaporated fraction). At 98 kPa/36°C only light ends boil, so U
is low and you can't out-fuel it (excess pools and shorts the plug). Lower MAP raises U — but the
73 mm throttle can't make vacuum at 178 rpm (floor pulls only 88→78 kPa), and it costs the idle
floor, and the car starts fine at ~98 kPa anyway once the plugs spark. So vacuum was never needed.

**Key numbers:** 61 sparks, EGT flat 47°C, no rpm bumps = zero fires. Ignitable window ~3:1 (a ±10%
fuel change is noise). Idle authority 2.4–8.0% TPS; airflow% = authority%. Cranking floor MAP ~88
(78 only by lowering the idle min, which reopens idle stall). #6 wet = its +8% crank trim, not a leak.

**When to care:** any no-start on this car. First move is always plugs, not tables — a fouled plug
mimics every fuel/air fault and invalidates every test until it's clean.
