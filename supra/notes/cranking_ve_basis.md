# Cranking VE basis error + cranking-fuel rebuild (2026-08-06)

Why "0 % cranking enrichment" was still fouling plugs on this car, and the tables built to fix it.
General theory: [notes/engine_start.md → The VE basis is the silent multiplier](../../notes/engine_start.md).

## The measurement

`0806 rich cranks.csv` (Desktop, 348 s, nine crank windows — seven real attempts plus two
deliberate flood-clears at TPS 98–99 % showing PW 0.032 ms, i.e. the −100 % anti-flood bin now
reachable). Channels included `VE` and **`Injectors cal. time`** — the ECU's own computed
deadtime from battery voltage and fuel pressure. Use that channel; do not back-solve deadtime.

| quantity | median over 433 fueled crank samples |
|---|---|
| `Injectors PW` | 2.839 ms |
| `Injectors cal. time` (deadtime) | 1.406 ms |
| **effective PW** | **1.433 ms** (0.0294 cc = 0.0221 g/event) |
| `VE` (ECU basis) | 63.3 |
| MAP / RPM / TPS | 91 kPa / 175–220 / 3.5 % |
| Fuel pressure | 3.94 bar (rail full from sample 1 — prime working) |

**Max RPM across the whole log: 220. Zero fire events in seven attempts**, with full rail, normal
spark count and clean sync — the quenched-spark signature of [crank_fail_0729.md](crank_fail_0729.md),
not a mixture-width problem. 17.3 s of fueled cranking ≈ 26 cycles × 6 injectors × 0.0221 g =
**≈3.4 g (4.6 cc) of liquid into the ports with nothing burning it**.

## The error

Will's anchor: measured VE at 1200 rpm idle is firmly ~50, and the ECU's own `veTable` row for
1184 rpm at low MAP agrees (~49) — that row was autotuned against a live wideband. The cranking
lookup clamps to the lowest-RPM row, which reads ~63–64 at 90–98 kPa and **was never measured at cranking speed**.
(Will, 2026-09-30: that 500 rpm bin was added on purpose to rescue running bogs, and it works. Its cells serve a
bogging running engine, not cranking. So B belongs in the cranking table, not in the VE axis.)

→ **B = VE_true / VE_table ≈ 50 / 63.3 = 0.79.** At `crankingLambdaTarget` λ 1.00 with a 0 % cell,
the delivered mixture is λ_liquid ≈ **0.79 against real air** — a 26 % overfuel labelled "no
enrichment". Cold cells inherit the same factor, which is why the flooding saga escalated so fast.

Verify B before trusting the hot end: read `Lambda 1` on the first pull-up once the WBO validates
(~25–33 s), or A-B the 86 °C column ±10 % and keep whichever catches cleaner. If VE_true is 55
rather than 50, every cell shifts ≈ +10 points.

## Rebuild parameters (chosen, 2026-08-06)

`corr(CLT, rev) = B(CLT) × [1 + E₁(CLT) · e^−(rev−1)/N(CLT)] − 1`, CLT bins [0,17,34,51,69,86,103,120].

| param | table 1 (E0) | table 2 (E100) |
|---|---|---|
| B | 0.86 → 0.78 (cold → hot; wall-heating term only exists warm) | same |
| E₁ (rev-1 enrichment over **true** stoich) | 0.70 → 0.08 | 1.15 → 0.14 |
| N (film-charging revs) | 16 → 4 | 20 → 4 |

- E₁ cold on table 1 gives λ_true ≈ 0.59 — Hartman's ~1.5:1 cold cranking.
- Table 2 stays positive at 86 °C where table 1 has gone negative: ethanol's 78 °C BP + high HoV
  keep it wet until coolant passes its own boiling point.
- N is now **temperature-scheduled** (refinement #1 from engine_start.md): warm columns collapse
  by rev 7, cold columns legitimately drag to rev 20.

Exported (negatives, sign+magnitude `u12`) to Desktop as
`Cranking - Cranking fuel 1/2 [%] (physics rebuild 20260806).emubt`.
`crankingLambdaTarget` unchanged — the negatives carry B themselves.

## Two process lessons

1. **`u12` holds negatives.** Its name says unsigned; EMU writes `-7 -D -10`. Never rule out a
   negative cell from the storage name — ask for an EMU export containing one. (Cost here: a
   whole proposal built around pushing B into `crankingLambdaTarget` instead.)
2. **EMU's row interpolation is linear.** Entering the rev-1 and rev-20 rows and interpolating
   loses the first-order concavity — at CLT 0 / rev 7 linear gives 33 where the exponential wants
   27, so every cold mid-rev cell lands 5–6 points rich, exactly where a long cold crank lives.
   Enter all five rows.
