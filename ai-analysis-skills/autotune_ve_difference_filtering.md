# Filtering EMU autotune "VE DIFFERENCE" cells against a log

EMU Black's Σλ autotune VE-DIFFERENCE grid is a raw lambda-driven suggestion. It excludes
fully-cut overrun samples but **does not robustly reject** (a) the acceleration-enrichment
transient just after a PPS tip-in, nor (b) overrun **re-light ramp** samples (`Overrun fuel
corr.` ramping +1…+16 back to 0) — both briefly skew measured lambda and leak into the cell
average. Before applying the grid, gate every suggested cell against the log's *clean* samples.

## Method (validated on log `20260629_1753.csv`, 50 Hz, 9 % ethanol)

1. **Flag tip-in / AE window.** `dPPS/dt > 60 %/s` over a ~120 ms window marks a tip-in;
   hold contamination for **0.8 s** after (AE decay). Exclude those samples.
2. **Flag overrun.** Exclude where `Overrun fuel corr. != 0` (covers full cut −100 **and**
   the +1…+16 re-light ramp) **or** `PPS < 1 & RPM > 1500` (off-throttle decel still settling).
   In this log that was 26.6 % of samples — overrun is the dominant contaminant, exactly the
   "above-3k off-throttle enleanment" risk.
3. **Per cell, compute clean fuel error** on the survivors:
   `err% = ((1 + STFT/100) · λ_meas/λ_tgt − 1) · 100`, nearest-bin assigned to the autotune grid.
4. **Gate each autotune delta `at` by the clean median `ce`:**
   - `clean_n == 0` → **drop** (cell unsupported by this log; the AT value is stale accumulation).
   - `clean_n < 8` → **drop** (too few clean samples to trust).
   - `sign(at) ≠ sign(ce)` and `|at| > 1` → **drop** (contradiction = contamination artifact).
   - `|at| ≥ 3` and `|ce| < 2` → **drop** (AT wants a big move, clean error ≈ 0).
   - else → **apply `at`** (clean data agrees in direction).
5. Apply kept deltas to the VE raw: `new = round(old · (1 + at/100))`, clamp u12 ≤ 4095.

## Result on this log

38 of 52 autotune cells applied, **14 dropped.** The dropped set is exactly the contamination
the user flagged: the big low-MAP negatives whose clean error was ~0 or opposite
(`1868/35 −7.8` vs clean +0.0; `2211/35 −8.2` vs +3.0; `2553/35 −2.9` vs +2.1;
`1526/49 −6.1` vs +0.4; `1184/49 −5.5` vs −1.6), sparse overrun-only cells
(`2211/20`, `1526/20`, `842/49`, `4947/152`, `2553/93`), one tip-in-poisoned positive
(`3237/49 +4.7` vs clean −2.1), and three no-data cells (`842/35`, `1184/20`, `4605/49`).

The **kept** changes are a coherent, genuine lean band — broad +2…+6 % across 1800–5000 rpm /
49–93 kPa where clean error independently read **larger** than the autotune suggestion (autotune
was conservative there), plus real light-load richness pulled at MAP 20–35 (e.g. `2895/20 −6.1`,
clean −12.7). Applied to `veTable` (table 1 dominates the blend at 9 % ethanol; veTable2 left
untouched). Output: `supra/exports/Fuel tables - VE table 1 [%] (autotune-filtered 20260629).emubt`.

See also: [ve_correction_from_log.md](ve_correction_from_log.md), [../notes/fueling.md](../notes/fueling.md).
