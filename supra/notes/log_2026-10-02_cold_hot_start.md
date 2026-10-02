# Logs `newcoldstart.csv` + `newhotstart.csv` (2026-10-02) — cranking dose vs need

Sources: `EMU_BLACK_V3\Supra\LogAutosave\newcoldstart.csv` (1871 samples, 1088–1169 s) and
`EMU_BLACK_V3\Supra\newhotstart.csv` (1408 samples, 2445–2502 s). fw 3.071, E14 (`FF Blend VE` 91).
Tune: the binary `Supra.emub3` (10-02 09:34) postdates the 10-01 XML, and Will re-exported the XML after
the cold start with "a little" added cranking fuel, so table values are reconstructed from the log where
possible. No `Data changing` during either crank.

Cold log caveat: a 6.3 s logging gap at 1107.6–1113.9 with `ECU Reset` 0 → 19. Before it CLT read 39 /
IAT 34 and fuel pressure 0; after it CLT 29 / IAT 27 / rail 4.06 bar. The crank used the post-reset values.

## 1. What the logged cranking correction contains

`Cranking correction` = (1 + `crankingCorrTbl` blend)(1 + `TPSScaleTbl`) − 1. Verified three ways: 10-01
first sample (TPS 2.9) 24 = table 36 × (1 − 0.088); 10-02 cold tail −17 = table ≈ 0 at TPS 5.4 (scale
−16.3 %); 10-02 hot −9 = hot table 0 at TPS 2.9–3.1 (scale −9 %).

`TPSScaleTbl` has been [0, −58, −83, −100, −100, −100] at `tpsCrankingBins` [0, 19.2, 27.5, 33.3, 90,
99.6] since at least the 09-15 export (June exports: −21 at 19.2). It interpolates from 0 at TPS 0, so the
idle controller's cranking throttle position sits on the cut slope with no pedal input:

| start | cranking `Idle air %` | TPS | anti-flood cut |
|---|---|---|---|
| 09-29 cold (CLT 26) | 67.5 | 4.7 | ≈ −14 % |
| 10-01 / 10-02 cold (CLT 27–29) | 79–80 | 5.4–5.5 | **−16 %** |
| 10-02 hot (CLT 96) | 30 | 2.9–3.1 | **−9 %** |

Raising the cranking airflow does not by itself need more fuel: the VE equation scales the dose with MAP.
It needed more only through this scale (−14 → −16 %).

## 2. Cold start (CLT 29, IAT 27, 10.5–11 V)

- Starter 1116.0, first fuel 1116.52 (rail 4.0 bar — not the rev-axis exhaustion trap), first fires ~1118.4
  (~rev 6–7, net −2…−5 %). Then a **5.6 s hover at 290–720 rpm** (MAP 93 → 72) on net **−17 %** — the clamped
  last row (rev 20) plus the anti-flood cut; ~49 physical revs before the exit.
- Exit at 1123.96 (750). Fuel per unit air ((PW − cal. time)/(MAP·VE)) stepped **2.77 → 4.62–4.72 (×1.68)** in
  one sample as cranking −17 % was replaced by ASE 39 % × warmup 10 %. RPM 769 → 1715 in 0.7 s, in
  Afterstart (`Idle state` 5, PID off), with the throttle still at the cranking position. The fuel step lit it,
  not idle control.
- Fuel, not spark: ignition also stepped (13° → 22° lock), but on 10-01 the same 13° caught in 0.4 s on
  +13…+24 % net. Same spark, different fuel, different outcome.
- **Stepless target at the exit: ≈ +39 % net** (0.83 × 1.68 − 1), the same +40 % measured on 09-29 (CLT 26). Both
  sides use the same VE lookup, so the target does not depend on the VE basis.
- Afterstart hold (state 5 for 1.48 s, lock 0.44 s ≤ hold) then ACTIVE at 1334 rising: PID +5 air / +4.5°,
  settled at 1440 by 1126.2. Overshoot 1715 (vs 1991 on 10-01). No wiggle — the hold + lock ≤ delay worked cold.

**Is that much ASE needed? (Will, 2026-10-02.)** WBO valid at +36 s after the exit on both cold starts (10-01
CLT 27, 10-02 CLT 29). First readings λ 0.75–0.79 vs target 0.90 with ASE still 9–12 % → 14–17 % rich. On 10-01,
at +60 s with ASE already 0 and warmup 11 %, λ 0.80 — still 11 % rich. So the late ASE tail is surplus and the cold
base (warmup/VE) is itself ~11 % rich (cf. `project_supra_rich_idle` — rich at low IAT). The first 36 s are blind, so
the time-zero ASE magnitude is not measured. Bracket at ~29 °C from the cranks: −17 % hovered, +13…+24 % caught
(10-01 #2, wet ports), +39 % took off. The stepless rule needs ASE runtime-0 and the cranking tail to *match*, not
to be large: lower both together.

## 3. Hot start (CLT 96, oil hot — 1.8 bar idle before shutdown)

- Shutdown 2468.8. **Rail pressure bled 3.31 → 0 bar in ~5 s** (pump off). A sound pump check valve,
  regulator and injectors hold rail pressure for minutes; leak path not identifiable from the log. If it is
  injector leak-down, a hot soak puts fuel in the ports.
- Restart without a key cycle (`ECU Reset` unchanged) → no prime. Starter 2475.08, RPM sync 2475.40, pump
  on 2475.48 (rail 3.94 bar in < 0.1 s), first fuel 2475.64. First fire 2476.60 after ~1 s ≈ 3 fueled revs at
  **net −9 % (all anti-flood; hot table 0)**. Exit 2476.72. The note's hot catch margin is ~+10–15 %
  (`notes/engine_start.md` → self-priming revs); this crank ran 9 % below base.
- **Run-up: flare to 1906** on the held 30 % cranking airflow (over-aired for hot oil, by design) + 22° lock.
  Hold 1.44 s; ACTIVE engaged at 1284 rpm **falling ~800 rpm/s** → airflow PID −7.2 / ign −7 (engine above
  target) as it fell through 1025 → **dip to 715**, then PID +19.6 / ign +15.5 → 1582 → 971 → settled ~1030
  (PID −12, the envelope over-air). The fixed hold that lands a cold start at rest catches a hot start mid-fall.
  One scalar cannot do both; the cold equilibrium is reached in ~1.4 s, the hot one is not.
  **Correction (2026-10-02, later):** the A/C was requested (`Switch 1` from 2477.36) and the clutch engaged at 2478.00, 0.2 s
  before ACTIVE, with no A/C airflow correction (that applies only from ACTIVE). The 715 dip is a compressor-load step on the
  decaying engine plus the 800 rpm A/C gate cycling it. It is not a measure of the hold; see `log_2026-10-02_restartbounce.md`.

## 4. Proposals (Will applies)

1. `tpsCrankingBins` / `TPSScaleTbl`: flat 0 up to just above the highest cranking TPS (100 % air → 6.5 %
   TPS), e.g. bins [0, 8, 19.2, 27.5, 33.3, 99.6] with [0, 0, −58, −83, −100, −100]. Restores +19 % cold /
   +10 % hot on every cranking rev with no table edit.
2. Cold exit rows to the stepless target (≈ ASE runtime-0 at each CLT, pump table): rev 13 at CLT 17 / 34
   ≈ 41 / 34 (aseTbl runtime-0 there); table 2 from aseTbl2 (≈ 68 / 58). Rev 20: today it fed a firing 300–700 rpm
   hover for ~30 revs at ≈ 0, which trapped the start lean. The 09-29 rationale for keeping it low (a crank that
   hasn't exited by rev 20 isn't catching) did not hold here. Will's call.
3. Hot rows 1/3 (CLT 86–120): after #1 the net is ≈ +5 / +3 %; the engine_start catch-margin is +10–15 %. Plug
   fouling (BKR7EIX) caps it there.
4. Hot afterstart: decide between hold length (cold benefit) and a hot ACTIVE entry on the falling edge.

Shape proposed to Will 2026-10-02 (per-cell values in chat, from the post-cold-start XML): **every cell =
max(current, ASE runtime-0 at that CLT)** — `aseTbl` for table 1, `aseTbl2` for table 2. The rule floors the
cranking dose at the running dose it hands over to, so there is no exit step at any rev or CLT, and the wall-film
peak stays on top at cold early revs. Monotone (non-increasing) in both CLT and revs by construction. At CLT 29
it gives ≈ +38 % net vs the +39 % the exit step asks for; at CLT 96 ≈ +13 %, inside the +10–15 % warm catch
margin. Columns 51/69 and CLT 0 have no start data; they follow the rule. Cost: a crank that never catches runs
on that floor instead of decaying toward 0 (pedal clear-flood still available).
**Decision (Will, 2026-10-02): hand-off value 30.** Implemented as: scale `aseTbl` and `aseTbl2` ×0.78 (every
cell, so the tail trims too) so the blended ASE runtime-0 at CLT 29 = 30 (was 38.4); then cranking cells =
max(current, new ASE runtime-0 at that CLT). Cranking tail at CLT 29 = 30.1 blended; at CLT 96 ≈ 10.5 (bottom of
the warm catch margin). Cold base richness (~11 % at ASE 0) is separate and not touched by this.
**Revision (Will: "don't go overboard", 2026-10-02):** flooring every rev at the hand-off put 2.47 ms net into the
first second of a 29 °C crank — the 07-29 fouling-crank level (`cranking_pw_vs_start.md` → Fouling-era doses). Final
shape: rows 13/20 = hand-off (ASE runtime-0 after the ×0.78 trim); rows 1/3/7 = current XML × that column's
former anti-flood factor (TPS from the cranking airflow at that CLT), floored at 0, so the early revs deliver what
caught cleanly before the anti-flood fix (≈ 2.04 ms net at 29 °C). Monotone in CLT in every row; rises from rev 7
to 13, which unwinds the cranking-speed VE basis (B) as RPM climbs (the 09-29 proposal). Hot early rows land at 0,
matching the May–June hot cranks that caught in 0.3–0.6 s at ≈ 0 %.
**Tables issued 2026-10-02 (final for the next start).** Cranking: rev 1 = current × that column's former
anti-flood factor; revs 3–20 = the same for rev 3; floored at 0. ASE: every cell ×0.29, except rows whose runtime-0
fell below the cranking tail at that CLT, which are scaled up to meet it (0 °C and 46 °C rows; E85 0/23/46 °C rows),
keeping each row's decay shape. Hand-off at 29 °C: cranking ≈ +10.5 %, ASE ≈ +11.6 % (blended E14); at 96 °C 0 vs
≈ +3 %. Values in the chat of 2026-10-02.

**Superseding decision (Will, 2026-10-02): front-load, never add fuel with revs — "start with the fuel and light
off faster".** In delivered fuel (`cranking_pw_vs_start.md` → Delivered fuel): the cold light-off dose is ≈ 31–33
mg/injection at cranking MAP (≈ +11 % net at 29 °C); ~44 mg did not light faster; the 10-02 tail decayed to 17 mg
and hovered. So hit the light-off dose at rev 1 and hold it: rev 1 = trimmed rev 1, revs 3–20 = trimmed rev 3
(monotone, no rise). Hand-off ≈ +11 % at 29 °C → ASE ×≈0.29 of the original tables (hot runtime-0 ≈ 3 %).
Literature (Banish ~l.3175–3187; Bosch p.108 summary in `corpus/gasoline_engine_management_bosch.md`): post-start
enrichment covers fuel precipitating on cold walls and goes to zero as the engine warms; Banish: decrease it with
temperature "to avoid flooding on hot restarts". No corpus number for hot ASE; nothing supports 10–15 % hot. Hot
stall-and-restart in traffic (06-28 `died_hot_return_to_idle_again`): caught in 0.28 s at 23.9 mg (E25) ≈ the 24 mg
a 0 % hot cell gives with the anti-flood fixed. Risk of the low hand-off: the 750 → idle run-up now gets ≈ +11 %
instead of ≈ +39 % ASE, untested; the WBO is blind for it.

**Final (Will, 2026-10-02): the first revision stands — the rise is a phase change, not more fuel per revolution.**
With the exit at 400/500 the hover and run-up always ran on ASE (≈ +38–40 % at 26–29 °C); the cranking table only had
to give the catch. With the exit at 750 that whole stretch now sits in the cranking table, so its late rows must carry
what ASE used to carry there. Old exits came around rev 5–10, so the rev 7 → 13 rise reproduces the old sequence:
rows 1/3/7 = the catch dose that worked (≈ +10 % net at 29 °C), rows 13/20 = hand-off (30). Cost: a crank still not
firing by rev 13 gets ≈ 2.4 ms net at cranking MAP (07-29 level) — pedal clear-flood remains. The "second revision"
below is superseded.
**Second revision (Will, 2026-10-02: "it doesn't make sense to add more fuel for successive revolutions"):** agreed.
Wall-film demand per cycle only falls with revs. The rev-7 → 13 rise existed only to meet the hand-off value of 30
and to unwind the cranking-speed VE basis (B), which depends on RPM, not revs; the rev axis can't see RPM (10-02 sat
at 300–700 rpm for ~40 revs, 10-01 #2 reached 750 in ~3). Monotone version: rev 1 = trimmed rev 1; revs 3–20 =
trimmed rev 3 (no decay below it). Hand-off then = what the early revs deliver, ≈ +11 % at 29 °C, so ASE time-zero
comes down to meet it (≈ ×0.29 of the original `aseTbl`, or a few points above — a small step is harmless). Support:
λ 14–17 % rich at +36 s with ASE 9–12 %, still 11 % rich with ASE 0; cranks at ≈ +10 % net caught (09-29, 10-01 #2).
Risk: the first 36 s after the hand-off are blind. The alternative — flat at 30 — puts ≈ 2.4 ms net into the first
second, the 07-29 fouling level.
*First draft (retracted the same day): raised hot columns to ~14 % while leaving 51/69 at 5–16 %, so the table gave
more fuel hot than warm. Will: "make a table that makes sense."*

**Hot restart and rail preload (Will, 2026-10-02):** Will attributes the slow hot catch to the missing prime.
The log puts the rail at 3.94 bar 0.16 s before the first injection, so the injections were not short of
pressure. The lost time was ~0.5 s of sync/pump start before the first injection, plus ~3 fueled revs at −9 %.
