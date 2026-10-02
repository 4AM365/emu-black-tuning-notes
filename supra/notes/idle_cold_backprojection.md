# Idle airflow requirement back-projected to cold — napkin model (2026-09-20)

**Ask (Will):** given the post-clean state of tune, infer oil temperature from coolant on cranking/warm-up (or
from oil pressure at a given RPM over time), back-project the idle airflow requirement to very cold
temperatures, and check that the Active-state table is over-aired *enough* — the strategy being to over-air
and let the PID pull it down.

**State of tune used:** `supra/tunes/supra export 09192026 post-tb-clean.xml.emub3` (19:05; identical to
`EMU_BLACK_V3\Supra\Supra.xml.emub3`). A QuickSave at 20:42 postdates it — if the §8 tables from
[`tb_clean_2026-09-19.md`](tb_clean_2026-09-19.md) were entered after 19:05, export the XML and re-run.
Both the export's `idleActiveAirflow` and the §8 proposal are scored below.
**Data:** `EMU_BLACK_V3\Supra\fullchannels.csv` (09-19): dirty-TB morning cold start from CLT 32 (old TPS frame,
converted with the carbon fit from the TB-clean note §5), clean-TB restart from CLT 51 on the old tables, clean
hot idle. **Coldest measured point on this engine is a 32 °C start. Everything below that is extrapolation.**
Script + generated tables: [`idle_cold_backprojection/`](idle_cold_backprojection/) (`backproject.py`, `requirement.md`).

## 1. Oil temperature from oil pressure — it works above ~65 °C oil and not below

`Engine oil pressure` ÷ RPM (bar per krpm), morning warm-up, Walther 10W-30 curve (KV40 = 70, KV100 = 10.5
cSt, typical figures — model knowledge), laminar `P ∝ μ·N`, referenced to the early-hot anchor
(OP/N = 3.0 ≙ oil ≈ 80 °C per the oil note's R4 mapping):

| t [s] | CLT | RPM | OP bar | OP/N | μ/μ(80 °C) | oil °C inferred | note |
|---|---|---|---|---|---|---|---|
| 20 | 33 | 1417 | 7.25 | 5.13 | 1.71 | *62* | **relief-capped** — oil is really ≈ 30 |
| 100 | 51 | 1470 | 7.06 | 4.79 | 1.60 | *64* | capped |
| 200 | 73 | 1262 | 6.31 | 4.99 | 1.66 | *63* | capped |
| 220 | 78 | 2161 | 7.12 | 3.27 | 1.09 | *77* | at 2161 rpm the pump is on the cold relief (7.1–7.25 bar) |
| 280 | 96 | 1086 | 4.88 | 4.01 | 1.34 | 70 | first honest reading |
| 340 | 96 | 1014 | 3.81 | 3.69 | 1.23 | 73 | |
| 400 | 96 | 2056 | 6.06 | 2.98 | 0.99 | 80 | hot relief ≈ 6.0 bar at ≥ 1900 rpm |
| 480 | 96 | 1032 | 2.81 | 2.76 | 0.92 | 83 | |
| (post-clean, 15 min soaked) | 96–105 | 1015 | 2.1–2.2 | 2.1 | 0.70 | ≈ 95–100 | |

**Reading:** from a cold crank until CLT ≈ 90, OP/N sits flat at 4.8–5.1 bar/krpm whatever the oil is doing —
the pump is at its relief (cold relief ≈ 7.25 bar, hot ≈ 6.0; [`notes/oil_pressure.md`](../../notes/oil_pressure.md)
already has the hot plateau) — so the pressure channel **cannot see oil temperature below ≈ 65 °C**. It reads a
30 °C sump as "62 °C". The usable oil-temperature clock on a cold start is therefore:

- **at cranking, oil = coolant = ambient** (after any soak longer than an hour or two both are at ambient);
- **during warm-up the oil lags coolant:** from the honest readings, a 30 °C start had oil ≈ 70–73 when CLT
  first reached 96, i.e. the oil had covered ≈ 0.6–0.7 of the coolant's rise. The model below uses
  `T_oil = T_amb + 0.7·(CLT − T_amb)`.

That lag is the whole reason the CLT axis under-serves a cold start: **the CLT-30 column is visited with
oil at 30 (start at 30) or with oil at ~15 (start at −20).** One column, two oil temperatures, ~15 % apart
in demand.

## 2. The requirement model

Position needed to sustain target N at coolant CLT after a start at ambient a:

```
TPS_req = S_hot × (N / 1025) × D(T_oil) × √(T_amb / 303 K) / K(CLT)
```

| term | what | basis |
|---|---|---|
| `S_hot` = 2.9 % TPS | sustaining position, 1025 rpm, CLT ≥ 96, first minutes hot (oil ≈ 80 °C), table spark 18° | measured, clean TB, 09-19 (TB-clean note §8) |
| `N/1025` | air demand ∝ RPM, plate flow ∝ position on the clean TB | measured (MAP×RPM/N = 34–37 kPa at every cell, both TBs) |
| `D(T_oil)` | mass-per-rev demand vs oil temperature, at table spark | see below — the term with all the uncertainty |
| `√(T_amb/303)` | a choked plate passes more mass in cold air | physics; worth −7 % at −10 °C |
| `K(CLT)` = 1 − 0.0019·(95 − CLT) | plate passes less air per % TPS when the throttle body is cold (bore/plate clearance) | implied by the CLT-35 point after removing the engine-side term; 0.89 at CLT 35 |

**`D` — two models, and they bound the answer:**

- **Model H (physics, spark-corrected):** rubbing friction ∝ μ^0.3 (Heywood, cited in the oil note R4) on a
  share `b` of idle work, the rest viscosity-insensitive: `D = a + b·(μ/μ_80)^0.3`. Calibrated on the CLT-35
  rows with the +8° of ignition-PID advance they carried *converted back to air* at 2.5 %/° (the repo's
  "+6° ⇒ +15 % air"): D(32 °C oil) = 1.15 (measured mass/rev) × 1.20 = 1.38 → `b` = 0.54. This is what the
  table must carry **if the ignition PID contributes nothing**.
- **Model L (empirical):** power law `D = (μ/μ_80)^p` fitted through the CLT-35 rows *as logged*, i.e. with
  the ignition PID doing its +8° — p = 0.146. This is what the table must carry **if the ignition loop keeps
  helping the way it did on 09-19.**

**Check on the one clean point neither was fitted to** — clean TB, CLT 55–60, 1450 rpm, table spark, oil
≈ 53: measured **4.53 % TPS** (normalised 3.20 × 1450/1025). Model L 4.71 (+4 %), model H 5.13 (+13 %). So L is
close and H is conservative by ~0.6 % TPS at that cell; the truth is nearer L, and H is the over-air bound.
Hot column: model 2.95 vs measured 2.9. ✓

Viscosity → demand (model H), oil °C: −20 → 3.4× · −10 → 2.6× · 0 → **2.1×** · 10 → 1.8× · 20 → 1.6× ·
30 → 1.4× · 45 → 1.2× · 60 → 1.1× · 80 → 1.0 · 105 → 0.9. Heywood's "friction doubles at 20 °C" sits in the
middle of that — the model reproduces it because it was calibrated near there, not independently.

## 3. Result — worst case per `idleActiveAirflow` column

For each CLT column, the coldest start considered (−20 °C) that passes through it, at the `idleRPM` target
the export schedules there (1500 to CLT 50, 1450/1300/1150 through 60–80, 1025 from 90). Airflow-% in the
**1.5–6.5 window** (`idleDBWTargetMin/Max` raw 15/65).

| CLT col | target | oil °C on a −20 start | TPS req **L … H** | air-% req L … H | 19:05 export cell | export − req (L / H) | §8 proposal | §8 − req (L / H) |
|---|---|---|---|---|---|---|---|---|
| **0** | 1500 | −6 | **8.8 … 16.7** | 147 … 304 | 60 | −87 / −244 | 100 | −47 / −204 |
| **15** | 1500 | 4 | **6.4 … 9.0** | 98 … 150 | 58 | −40 / −92 | 90 | −8 / −60 |
| **30** | 1500 | 15 | **5.8 … 7.4** | 86 … 119 | 54 | −32 / −65 | 80 | −5 / −38 |
| **45** | 1500 | 26 | **5.3 … 6.3** | 76 … 97 | 50 | −26 / −47 | 71 | −5 / −26 |
| **60** | 1450 | 36 | **4.7 … 5.3** | 65 … 77 | 45 | −20 / −32 | 63 | −2 / −14 |
| **75** | 1225 | 46 | **3.7 … 4.0** | 45 … 50 | 37 | −7 / −13 | 44 | −1 / −7 |
| **96** | 1025 | 76 (30 start) | **2.95** | 29 | 28 | −0 | 28 | −1 |

Same table for a **30 °C start** (what was actually logged): CLT 30 → 5.4 … 6.8 % TPS, CLT 45 → 4.9 … 6.1,
CLT 60 → 4.3 … 5.3, CLT 75 → 3.3 … 4.2. The full per-start grid (−20 … +30) is in `requirement.md`.

### What this says

1. **Neither table is over-aired anywhere on the warm-up diagonal below CLT 96.** The 19:05 export is
   20–40 airflow-% *under* the low-bound requirement from CLT 60 down, which is exactly the +9 … +23 the
   dirty morning's PID carried and the +15 integral clamp it hit. The §8 proposal is within a few points of
   the low bound at CLT 15–75 — i.e. it is about right if the ignition PID keeps helping, and 15–60 under if
   it does not. **Under Will's strategy (PID pulls *down*), the table should sit above H at the coldest start
   he expects, not at L.**
2. **The 6.5 ceiling binds below about CLT 45 for a 1500 target on any cold start, under both models.** At
   CLT 30 the low bound is already 5.8 % TPS (86 %) and H is 7.4; at CLT 15, 6.4 … 9.0; at 0 °C, 8.8 … 16.7.
   With the window at 6.5 the cells are clipped at 100 % — no over-air is possible, the PID has no upward
   authority, and the ignition PID (up to the 30–35° `idleIgnitionMaxTorqueAngleTbl`) becomes the only thing
   holding the target. To *over-air* a 0 °C start at 1500 rpm the ceiling needs to be roughly **9–10 % TPS
   (model L) to ~17 (model H)**, and a 15 °C start needs ~7–9.5. The TB-clean note §6 flagged "short by
   1–1.5 % TPS below CLT 15"; the back-projection says shorter, because it includes the oil lag and the
   −20 °C start rather than a same-temperature start.
3. **The PID band is narrower than the cold uncertainty.** "Let the PID pull it down" has 25 airflow-% =
   1.25 % TPS of authority. The spread between a 30 °C start and a −20 °C start through the *same* CLT-30
   column is 5.4 vs 5.8 (L) / 6.8 vs 7.4 (H) — 0.4–0.6 % TPS = 8–12 airflow-% — and the L-to-H spread at
   that column is another 1.6 % TPS. A cell over-aired for a −20 start is 10–30 airflow-% high on a 30 °C
   start. That is inside the −25 clamp only at the low end of the range. Two consequences: (a) the table
   cannot be over-aired for *every* start temperature on a CLT axis alone — pick the coldest start you
   actually see and accept the PID sitting near −15 … −25 on warm starts through the cold columns; (b) the
   hot end of the diagonal (CLT ≥ 75) has enough authority either way — the problem is entirely the 1500-rpm
   cold columns.
4. **Cranking:** `idleCrankingDC` cold cell 86 % = 5.8 % TPS on this window, against a 1500-rpm requirement
   of 5.8 … 7.4 at CLT 30 and 6.4 … 9 at CLT 15. The catch-and-land into the Active table at a 0 °C start has
   no margin under either model. Not asked; noted because it uses the same window.

### Operating envelope (Will, 2026-09-20): Arizona, starts at 20–50 °C ambient

The −20 … 0 °C rows above are bounds, not targets. For the real envelope: oil when CLT first reaches 96 is
73 °C (20 °C start) to 82 °C (50 °C start) — a 1.35× viscosity ratio, ≈ 5 % of demand, ≈ 0.15 % TPS. **The hot
column is safe across the envelope.** At a 20 °C start the cold columns need CLT 30 / 1500 → 5.5 (L) … 6.8 (H),
CLT 45 → 4.9 … 6.1, CLT 60 → 4.3 … 5.3 % TPS; the §8 proposal (5.5 / 5.05 / 4.65) sits on the low bound at each
cell and 0.6–1.3 % TPS under the high one. So: §8 on the current window is adequate *if* the ignition PID is
allowed to carry cold warm-up as it did on 09-19 (model L); a table that is genuinely over-aired with the
ignition PID idle (model H) needs the 1500 row at 100 % for CLT ≤ 30 on a ceiling of ≈ 7 % TPS.

## 4. Assumptions, ranked by how much they move the answer

| assumption | effect | how to retire it |
|---|---|---|
| 10W-30 viscosity curve (KV40 70 / KV100 10.5) | sets μ ratios; ±20 % on KV moves D(0 °C) by ~±8 % | oil brand's datasheet |
| rubbing share `b` (0.54) / exponent `p` (0.146) — one calibration point at oil 32 °C | the whole L–H spread | **one logged cold start below 15 °C** — oil = ambient at crank, so it calibrates D directly |
| **`D` is labelled friction but is really rubbing friction + cold-combustion losses** (wall heat, vaporization — Heywood §12.7); the split is unmeasured. Pumping is *excluded* on evidence: MAP is 35–37 kPa in every row, so the pumping loop is the same size cold and hot and cannot be the cold increase. Will (2026-09-20): pumping likely dominates the *hot* idle work; if so `b` is smaller, the friction curve flatter (toward L) and the combustion cliff below ~40 °C steeper — roughly a wash in the 15–45 °C band, untested below it | shape of D below 30 °C | a cold log at table spark (ignition PID off) removes the 2.5 %/° assumption; the friction/combustion split needs a torque or motoring measurement |
| spark → air at 2.5 %/° | 0.20 of D35 in model H | ignition-gated data (oil note R8 asked for it too) |
| oil lag 0.7 | ±0.1 moves the cold-column oil by ±3 °C, D by ~±4 % | an oil-temp sensor (`oilTempInput` is unassigned) — or just cranking CLT |
| K(CLT) linear, 0.19 %/°C | −0.19 %/°C in TPS; plate material unknown (ES330 blade stamped "H") | same cold log; or the bore/plate expansion note once the material is known |
| `D` at table spark vs with ignition help | L vs H | decide policy: is the ignition PID allowed to carry cold idle? |

The first genuinely cold morning on the clean TB replaces most of this table. Until then the model is a
bound, not a calibration.

Not applied — Will enters tune changes. Values above are requirements in TPS and airflow-%; the window
(`idleDBWTargetMin/Max`) decides how they map to cells, and it is the ceiling that is short.
