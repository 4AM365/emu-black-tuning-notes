# Idle knife edge — 2026-09-19 (hungry cold, hanging hot, riding the DBW stop)

> Digest of [idle_knife_edge_2026-09-19.md](../idle_knife_edge_2026-09-19.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** the morning cold start (`whencold.csv`) and the afternoon hot session (`losingit.csv`) against `fucquedup.xml.emub3` and the 08-24 / 09-09 baselines — cylinder-out check, where the air actually went, why the DBW stop and the PID rails are involved, and what the tune can and cannot fix.

**The rules:**

- **No cylinder is out.** Per-cylinder knock-window fingerprint, cyl 3/6 EGT delta, idle roughness and the engine's air intake all match the 08-24 baseline. Mixture is ~4–6 % lean of target at light load (STFT +2…+5), rich ~3 % at idle cold — ordinary trims, not a dead hole.
- **The engine's idle air demand did not change.** At ~1000 rpm, MAP×RPM is 36–38.5 k on every day measured; cold oil (3.6–4.1 bar) needs only ~7 % more than hot-soaked (1.7 bar). "Hungry" and "needs less air than ever" are both statements about `Idle air %`, which is a **position command**, not air.
- **The sustaining plate position moves ~1 % TPS across the oil/TB temperature clock on the same CLT column** (TPS 5.9–6.1 at 3.6–4.1 bar → 4.8–5.0 at 1.7 bar, CLT ≥ 96 throughout). `idleActiveAirflow` is flat above 96 °C by construction, so nothing in the open loop can see it. That is the knife edge.
- **The DBW servo's stall point wanders — resolved the same evening: it was carbon fouling of the throttle body** (and the TPS frame moved −1.09 in a DBW relearn) ([tb_clean_2026-09-19](tb_clean_2026-09-19.md)); the oil/TB-clock rule above still stands on the clean TB. At a fixed −30 % clamp the plate parked at 4.5, 5.6, 7.5 and 8.6 % TPS within one 8-minute window; on 09-08 −7 % held 6.0. The hot-soaked sustaining position (4.8–5.0) sits inside the unreliable band, so −30 hangs the idle and −40 chokes it (t=379: plate 7.2 → 3.6 in 0.8 s, RPM 1791 → 396). No `dbwMinDC` value is right for this mechanism.
- **The PID is not mis-gained — it is saturating against a plant that stopped responding.** Plate stuck above command → RPM high → integral runs to `idleAirFlowIntegralLimitMin`, output to `idleAirPIDOutMin` (both −25 in the log = ~1.5 % TPS). When the servo finally lets go, that wound-down command lands below the sustaining position: the choke. Cold is the mirror image: `whencold` t 37–172 held 20–80 rpm short of the 1500 target with the I term parked at +15 (`idleAirFlowIntegralLimitMax`) — the cold cells were ≥ 24 airflow-% low.
- **Oil pressure "lower than usual" is thinner oil on a hot day**, and it reduced the air the engine needed. Not the pump.
- Tune edits (tables, clamps, `dbwMinDC`, `idleDBWTargetMin`) move the problem between morning and afternoon. Mechanism-level fixes: sweep the servo's duty→position curve hot and cold (or swap the TB), and an open-loop term that can see the oil/TB clock (the disabled oil-pressure correction, gated against warm restarts).

**Key numbers:** engine-side air at ~1000 rpm 36–38.5 k MAP×RPM (all days). Sustaining TPS 4.8–5.0 hot-soaked vs 5.9–6.1 with oil at 3.6–4.1 bar. Servo stall at −30 %: 4.5 … 8.6 % TPS. PID authority ±25 airflow-% ≈ ±1.5 % TPS. 44 live tune edits in the 509-s log.

**When to care:** before touching any idle table, PID clamp, `dbwMinDC` or `idleDBWTargetMin` again — and before believing an `Idle air %` number means airflow.
