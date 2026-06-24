# Spark-map delta for a cam-duration + compression-ratio change (E100)

> **Software page:** *Ignition* ([ignition.md](ignition.md), deep ref [timing.md](timing.md)),
> coupled to *VVT* ([valve_timing_dynamic_compression.md](valve_timing_dynamic_compression.md)).
> Worked for the Supra 2JZ-GE: **264° → 272° intake cam** and **CR 10 → 9**, on the **pure-ethanol
> table** (`ignTable2`, sbyte ×0.5°/count, E100 endpoint).

## Both changes move MBT the same way: more advance

Grounding: Hartman (`corpus/how_to_tune.md:1187`) — big-cam part-throttle advance is *more*
aggressive due to flame-speed loss from overlap dilution of the inlet charge. Heywood
(`corpus/ice_fundamentals.md`): residual fraction ~30% idle → ~5% full load (§6.4); residual/EGR
dilution lowers T_b and lengthens flame thickness → lower laminar flame speed (≈line 16883); MBT is
set by the trapped fuel/air/**residual** mass (≈line 2094). The note `timing.md` agrees in prose:
`:69` "bigger cams … mean more timing"; `:76`/`:78` short cams and **high** compression *reduce*
peak timing (so long cams and **low** CR *add* it).

- **Cam 264 → 272 (+8° duration):** more overlap + later IVC → more residual dilution and lower
  effective compression at **low rpm / light load** → slower burn → **more advance there**; fades to
  ~0 at high-rpm WOT (good fill, fast burn, low dilution). Load/rpm-shaped.
- **CR 10 → 9 (−1 point):** on E100 there is **no knock-relief bonus** (ethanol isn't knock-limited
  on this table), only the burn-rate shift — lower TDC density/temp → slower flame → **+1 to +2°**,
  largest at heavy load. NOTE: on the **pump** table (`ignTable`) the same CR drop *would* add more in
  the heavy-load/low-rpm corner via knock relief — don't reuse this there.

### CR↔timing — academic source

Banish, *Engine Management: Advanced Tuning* (`corpus/engine_management_advanced_tuning.md:3344`):
higher CR packs the charge denser so *"the flame front [can] easily hop from one molecule to the
next… burning at a faster rate **again require less ignition timing advance** to reach peak pressure."*
Read in reverse = our case: **lower CR → slower flame → more advance.** The corpus gives the
**direction/mechanism only**; the ~1°/CR-point magnitude is a practitioner rule of thumb, not a
book coefficient. (Heywood backs the mechanism: S_L scales with unburned-gas T and p, both lower at
lower CR.)

## Delta tables to add to `ignTable2` (crank °, NA load range)

RPM high→low top-to-bottom, MAP light→heavy left-to-right (EMU orientation). All in the
**264 → 272 / 10 → 9 direction** (positive = advance the map further).

**Cam only (264 → 272):**

| RPM ↓ / kPa → | 25–35 | 40–50 | 55–70 | 75–90 | 95–100 |
|---|---|---|---|---|---|
| 6500–7000+ | +1 | +1 | +1 | 0 | 0 |
| 5000–6000 | +1 | +1 | +1 | +1 | 0 |
| 3500–4500 | +2 | +2 | +1 | +1 | 0 |
| 2000–3000 | +3 | +2 | +2 | +1 | 0 |
| 1000–1500 | +3 | +3 | +2 | +1 | +1 |

**CR only (10 → 9, Banish relation):**

| RPM ↓ / kPa → | 25–35 | 40–50 | 55–70 | 75–90 | 95–100 |
|---|---|---|---|---|---|
| all rpm | +1 | +1 | +1 | +2 | +2 |

**Combined (sum):**

| RPM ↓ / kPa → | 25–35 | 40–50 | 55–70 | 75–90 | 95–100 |
|---|---|---|---|---|---|
| 6500–7000+ | +2 | +2 | +2 | +2 | +2 |
| 5000–6000 | +2 | +2 | +2 | +3 | +2 |
| 3500–4500 | +3 | +3 | +2 | +3 | +2 |
| 2000–3000 | +4 | +3 | +3 | +3 | +2 |
| 1000–1500 | +4 | +4 | +3 | +3 | +3 |

Crossover: the **cam** term dominates the upper-left (light/low-rpm dilution), the **CR** term
dominates the right (heavy-load density). Signs are solid (every cell ≥ 0); magnitudes are ±1–2°
MBT-shift ballparks — confirm on a dyno / knock-ear + EGT. Remember the FF blend scalar < 1 delivers a
fraction of any `ignTable2` step at partial ethanol (`timing.md:194`).

## ⚠ Conflict flagged: timing.md's numeric duration MBT tables

`timing.md`'s **272° E100 − 264° E100** subtraction gives the cam delta the *opposite* sign at light
load (−1 to −3° at 30–80 kPa, 0 at ≥90 kPa) — i.e. it says the bigger cam wants *less* cruise
advance. That contradicts the file's own prose (`:69`,`:76`), Hartman, and Heywood. Treat those
numeric duration tables' **light-load trend as inverted/unreliable** (model-generated); the WOT cells
(≥90 kPa, ≈0) are fine. The physics view above (more cruise advance) is the one to trust until the
tables are re-derived.

## Caveats

- **VVT-i scheduling** assumed comparable to today. Park the 272 *retarded* at idle/light load to cut
  overlap and the upper-left adds shrink (see [valve_timing_dynamic_compression.md](valve_timing_dynamic_compression.md)).
- **E100 only.** This is the `ignTable2` endpoint; the pump endpoint behaves differently on the CR term.
