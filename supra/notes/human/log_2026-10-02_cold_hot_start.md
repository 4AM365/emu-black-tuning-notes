# Starts 2026-10-02 (`newcoldstart.csv`, `newhotstart.csv`) — plain version

**What this covers:** how much fuel the cold and hot cranks actually got, and what they needed.
Canonical note: `supra/notes/log_2026-10-02_cold_hot_start.md`.

## The rules
- The anti-flood pedal scale reads TPS, and the idle controller's cranking throttle position is on its
  slope. It cut cranking fuel 16 % cold and 9 % hot with your foot off the pedal. Make it 0 up to just above
  the highest cranking TPS.
- Cold: the engine fired around rev 6–7, then hovered 300–700 rpm for 5.6 s on −17 % (last row ≈ 0 plus the
  anti-flood cut). The moment it crossed 750, afterstart fuel came in 68 % richer per unit air and it took off.
  The fuel step lit it, not idle control.
- What the cranking dose should be at the exit: about +40 % net at ~29 °C (same as 09-29), i.e. about the
  ASE runtime-0 value.
- Hot: ~3 fueled revs to first fire on −9 % (all anti-flood). The start note's hot margin is +10–15 %.
- The fuel rail bleeds from 3.3 bar to 0 in ~5 s after shutdown. Find the leak path.
- The long afterstart hold worked cold (no wiggle). Hot, it held a 1906 flare and handed over while RPM was
  falling fast → dip to 715. Correction: the A/C clutch engaged 0.2 s before that handover with no A/C airflow feed-forward, so the dip is A/C-confounded and not a measure of the hold.

## Key numbers
- Logged cranking correction = (1 + table)(1 + anti-flood) − 1.
- Cold exit step ×1.68 per unit air; stepless target ≈ +39 % net.
- Hot: flare 1906, dip 715, settled ~1030 with PID −12.

## When to care
Any cranking-table, anti-flood, cranking-airflow or afterstart-delay change.
