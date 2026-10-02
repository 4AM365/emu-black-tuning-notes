# Idle airflow back-projected to cold (napkin, 2026-09-20)

> Digest of [idle_cold_backprojection.md](../idle_cold_backprojection.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** a bounded estimate of the idle position/airflow the clean-TB engine needs at cold starts down to −20 °C, how oil temperature can (and cannot) be read from oil pressure, and whether the 09-19 19:05 export or the §8 proposal is "over-aired enough" for the over-air-and-let-PID-pull-down strategy.

**The rules:**

- **Oil pressure cannot see oil temperature below ≈ 65 °C** — from a cold crank until CLT ≈ 90 the pump sits on its relief (OP/N flat at 4.8–5.1 bar/krpm) and reads a 30 °C sump as "62 °C". Use cranking CLT (= ambient = oil after a soak) and an oil lag of ≈ 0.7× the coolant rise.
- The same CLT column is visited with very different oil temperatures depending on the start temperature (CLT 30 with oil at 30 or at ~15). A CLT-only axis cannot serve every start — pick the coldest start you actually see.
- Requirement model: `TPS = 2.9 × N/1025 × D(oil) × √(T_amb/303) / K(CLT)`. Two bounds for D: **L** (ignition PID keeps helping, as on 09-19) and **H** (table must carry it all). Checked on the one clean point not used for fitting (CLT 60 / 1450: measured 4.53, L 4.71, H 5.13).
- D is rubbing friction **plus cold-combustion losses** (split unmeasured); pumping is excluded — MAP is 35–37 kPa cold and hot, so the pumping loop doesn't change. If pumping dominates hot idle work (Will), the friction curve is flatter and the combustion cliff steeper; ~a wash at 15–45 °C.
- **Coldest measured point is a 32 °C start.** Below that this is extrapolation; the first cold morning log recalibrates it.
- **Neither table is over-aired below CLT 96.** The 19:05 export is 20–40 airflow-% under the *low* bound from CLT 60 down; the §8 proposal ≈ meets the low bound and is 15–60 under the high one.
- **The 6.5 ceiling binds below about CLT 45 for a 1500 target on any cold start.** Over-airing a 0 °C start needs a ceiling of ~9–10 % TPS (L) to ~17 (H); a 15 °C start ~7–9.5. The cranking cold cell (5.8 % TPS) has no margin either.
- The PID's pull-down authority (25 airflow-% = 1.25 % TPS) is smaller than the cold uncertainty; expect the PID near −15…−25 on warm starts through cold columns if the cells are sized for a −20 start.

**Key numbers (worst case, −20 °C start, TPS L … H):** CLT 0 → 8.8 … 16.7 · 15 → 6.4 … 9.0 · 30 → 5.8 … 7.4 · 45 → 5.3 … 6.3 · 60 → 4.7 … 5.3 · 75 → 3.7 … 4.0 · 96 → 2.95 (30 start). Model H D(oil): 0 °C 2.1×, 20 °C 1.6×, 45 °C 1.2×.

**Arizona envelope (starts 20–50 °C):** hot column safe (oil 73–82 °C at CLT 96, ~3 airflow-% spread). Cold columns at a 20 °C start: §8 meets the low bound (ignition PID helps) and is 0.6–1.3 % TPS under the high bound; genuinely over-aired needs the 1500 row at 100 % for CLT ≤ 30 on a ~7 % ceiling.

**When to care:** before sizing the 1500-row cold cells, the cranking cold cell, or the actuator ceiling; and the morning of the first cold start — log it.
