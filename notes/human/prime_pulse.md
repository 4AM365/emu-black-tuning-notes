# Prime pulse — digest

*View of [notes/prime_pulse.md](../prime_pulse.md). Canonical note wins on any conflict.*

## What this covers
The EMU Black *Prime pulse* — a one-shot injection fired on the first crank/cam pulse (all injectors
at once) so the first spark has vapor available. How to size it across CLT, how to measure whether
it is buying anything, and why you must cut early cranking fuel when you add it.

## The rules
- **The only thing prime delivers is fewer crank revolutions to catch.** Measure that first. If the
  engine already catches in ~2 revs, prime has nothing left to buy — set the bin to 0.
- **The film is a tax, not a goal.** Hot ports flash fuel to vapor, so the tax ≈ 0 and prime is pure
  downside (liquid on cold-heat-range plugs). Hot walls need *less* prime, not more — the "hot start
  has no film so it needs prime" intuition is backwards.
- **Prime = the rev-1 wall film, delivered early.** Size it to one cylinder's rev-1 deposit, never the
  whole puddle. That sizing is also what makes a *retry* safe: two attempts ≈ 1.4 base doses ≈ 7 % of
  a 20-rev crank's fuel. A 5–8 ms prime would be 5–8 base doses, twice — that's the 07-29 fouling.
- **Prime and the rev-1 cranking enrichment are the SAME fuel.** Add prime *and* cut the early cranking
  revs by the same amount, or you double-dose. You're moving fuel ahead of rev 1, not adding it.
- **Preconditions:** rail full at first trigger, foot off the pedal. Prime speeds a *healthy* catch —
  it won't fix fouled plugs or a vapor-λ no-start.
- **Never port a prime-pulse ms number between builds — port the mass.** The community "≈2 ms" advice
  is a 440 cc/min figure (≈11 mg); this build's 1.375 ms at 1230 cc/min is ≈21 mg on the same
  per-cylinder displacement, i.e. already ≈2× the generic dose.
- **`primePulseTable` is fuel-blind** — no `primePulseTable2`, no FF blend. Size on E0 and leave the
  ethanol delta with `crankingCorrTbl2`; an E100 first-principles size is ≈2.5× the E0 one and would
  drown a gasoline start.
- **Prime is net fuel time** (EMU adds dead time internally) — a 1.0 ms default would inject nothing
  otherwise. Confirm on the Scope before writing.

## Key numbers
- `primePulseTable`: 8×1 vs CLT (0/17/34/51/69/86/103/120 °C), **0.125 ms/count** (raw 8 = 1.0 ms).
  Currently flat 1.0 ms.
- **Measured** (`cranking_channels_recent_run.csv`, 2026-08-24, CLT ≈70 °C): sync → catch ≈ **0.5 s /
  ≈2 crank revolutions**. Post-catch is where the time goes: sag to 386 rpm, flare to 1810, crash to
  932, then ~25 s of decaying hunt. Prime touches none of that.
- Suggested prime (ms / raw): 0 °C **1.35/11**, 17 **1.25/10**, 34 **0.85/7**, 51 **0.50/4**,
  and **0** from 69 °C up. Cold column is derived, **not** measured — no cold log exists yet.
  **Re-verified 2026-09-10** against `updatedarmedstate.xml.emub3` at 4 bar (`fuelRailBasepressure`
  = 400, `injectorsSize` = 1230): same table to within one raw count.
- Literature: only **15–30 %** of the first cold injection becomes vapor (U at 20 °C; ≈30 % at 0 °C,
  ≈50 % warm per Heywood), and a robust first fire wants in-cylinder **φ 0.7–0.9**. Since prime ∝ 1/U
  and U is known only to ±2×, this is measure-don't-model territory.
- **Fork:** the sized table leaves the *first* fire at φ_v ≈ 0.62 (U 0.30) — by design, since the
  strategy charges the film over N ≈ 16 revs. Firing on rev 1 instead needs ≈2.5 ms cold (φ_v ≈ 0.79)
  and gives up fouling margin. Will's call.
- Prime is invisible on `Injectors PW` (Scope only). Judge it by revs-to-catch, counting
  `Executed sparks count` (free-running ubyte; ≈6/rev cranking wasted-spark vs ≈3/rev running).

## When to care
Setting up cold-start or chasing a slow catch. Add `CLT` to the cranking log layout first — without it
you cannot index anything. Not a lever for post-catch flare, hunting, or a fouled-plug no-start.
