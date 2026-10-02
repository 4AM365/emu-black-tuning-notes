# Prime pulse (key-on / first-sync injection)

Part of **Engine start → Cranking**. Canonical hub for how the EMU Black *Prime pulse* table
works, how to size it, and why it must be paired with a cut to the early cranking-fuel revs.
Cranking-fuel equation and wall-film theory live in
[engine_start.md → Cranking fuel equation](engine_start.md); this note is the prime-pulse-specific layer.

> **No hardcoded tune values.** The current cells live in `primePulseTable`, `crankingCorrTbl(2)`,
> `injectorsSize`, `injOpeningTimeTbl`, etc. Re-read them from the current `.xml.emub3` at analysis
> time; values below are cited to a dated export or stated as *method*, not baked in.

## What it is (EMU help — `docs/emu-black-help/Enginestart.md`)

- **Prime pulse** = one extra fuel dose fired **when the first crank/cam reluctor impulses appear**,
  before/at the first spark. **All injectors open simultaneously**, each for the table's amount.
  Purpose, in EMU's words: "to ensure the fastest engine startup … when the ignition system is
  synchronized and the first spark appears, vaporized mixture will be available."
- Symbol `primePulseTable`, `ubyte`, **8×1 vs CLT** on `cltBinsCranking` (= 0/17/34/51/69/86/103/120 °C,
  same axis as `crankingCorrTbl`). As of `supra 06132026.xml.emub3` it is **flat raw 8**, which EMU
  displays as **1.0 ms** (Will, 2026-08-12) → **scale = 0.125 ms/count** (`raw = round(ms × 8)`).
  Populated but *not* CLT-scheduled.
- **Invisible on the `Injectors PW` log channel** — observable only on the internal Scope. So you
  cannot verify it from a normal CSV; confirm by scope or by inference (rail-drop / faster catch).
- **Units = milliseconds** (EMU shows the value in ms). A useful flat-1 ms default doing work implies
  EMU applies the injection as a net fuel time (deadtime handled internally); the targets below are in
  the **same displayed-ms frame** as the current 1 ms, so they drop in directly. (Cranking-voltage
  deadtime for reference ≈ **1.4 ms**, measured `Injectors cal. time`, `crank_fail_0729.md`.)

## Why it helps: it front-loads the wall film

A cold start is wall-film-limited: the first fires are starved because a fraction *x* of each early
injection sticks to dry port/valve walls instead of vaporizing (Aquino x-τ model —
[engine_start.md → wall-film basis](engine_start.md)). The cranking-fuel table pays this "wall-film
tax" over the first ~N revolutions via its rev-1 enrichment E₁ (and `x = E₁/(1+E₁)`).

The prime pulse pays part of that tax **once, before the first intake event**, and into **all**
ports at once — so a cylinder's port is already wetted when its first intake stroke arrives. Result:
the first metered fires see more vapor → the engine catches in fewer revs. It does **not** add net
fuel to the strategy; it **moves** the earliest wall-film charge ahead of rev 1.

### The thermal logic runs the *opposite* way to intuition

"Hot walls have no film left, so a hot start needs prime to establish one" is the natural reading and
it is backwards. **The film is a tax, not a goal.** What the first spark needs is *vapor at the valve*;
liquid on the wall is the fraction of the shot that failed to become vapor.

- **Hot:** fuel flashes on contact with a ~90–120 °C port. Nearly all of the first metered injection
  vaporizes, so the tax ≈ 0 and there is nothing to pre-pay. Prime here adds liquid the engine did not
  need, onto plugs that are already the wrong heat range for it
  ([[project-supra-ignition-hardware]]) — pure downside.
- **Cold:** fuel does not flash. Most of the first shot condenses on a dry, cold wall, so the engine
  must pay a large tax *before* any cylinder sees a combustible vapor fraction. That payment is what
  the prime front-loads.

Hot walls do not need a film established; they need less prime, not more. The schedule is therefore
monotonic cold→hot and ends at **zero**, and the *only* place prime can buy revs is the cold end.

## Measured catch speed — the test that decides whether you need prime at all

Prime pulse has exactly one deliverable: **fewer crank revolutions to first sustained fire.** It is
invisible on `Injectors PW` (EMU help, `docs/emu-black-help/Enginestart.md`: observable only on the
internal Scope), so the *only* way to judge it from a CSV is to count revs-to-catch before and after.

**Method** (channels: `RPM`, `Trigger sync status`, `Executed sparks count`, `Cranking correction`,
`Ignition Angle`, `Idle air %`, and **`CLT`** — add CLT, it is missing from the current crank layout):

1. **Sync** = first sample with `Trigger sync status` = 2 (and RPM leaves 0).
2. **Catch** = `RPM` crosses `crankingThreshold`; corroborated by `Cranking correction` → 0 and
   `Ignition Angle` stepping to `afterstartIgnitionLockAngle` (×0.5 °/count).
3. **Revs between** — do *not* trust the RPM integral alone; the RPM channel lags hard through the
   catch accel. Use `Executed sparks count` instead. It is a free-running ubyte (wraps 255→1, does not
   reset per start), and **cranking fires in wasted-spark pairs** so it counts ≈2× the running rate —
   calibrate the ratio on a steady idle stretch in the same log (measured **3.05 counts/rev** running,
   **≈6/rev** cranking) and divide.

**Result, `cranking_channels_recent_run.csv` (2026-08-24, one start, warm):**

| Quantity | Value |
|---|---|
| Cranking speed | 183 → 237 rpm |
| Sync → catch | **~0.5 s** (t 4.24 → 4.72) |
| Sparks in that window | 12 counts ÷ ≈6 per rev = **≈2 crank revolutions** |
| RPM-integral cross-check | 1.58 rev (low, as expected — RPM lags the accel) |
| CLT (inferred) | **≈70 °C** — `Idle air %` held 36.5–37.0 through crank vs `idleCrankingDC` on `cltBins4` |

**Two revolutions is a first-fire on roughly the first or second compression stroke — there is no
latency left for a prime pulse to remove.** At this CLT the correct prime value is **0**, and the flat
1.0 ms currently in the table is doing nothing useful and can only wet a hot plug.

*Live-tune conflict to resolve before trusting the CLT number:* the same log's `Cranking correction`
channel reads −16 → −20 % across the crank. On `crankingCorrTbl` in `majorimprovement.xml.emub3`
(2026-08-22) that column belongs to **CLT 103–120 °C**, not the ≈70 °C the airflow channel implies.
`Supra WAY MORE SAUCE.emub3` (2026-08-24 10:21) postdates that XML and predates the log, so the live
cranking table is probably not the exported one — ask which was loaded before pinning the CLT
([[feedback-stale-export-not-live-tune]]). The ≈2-rev catch result stands either way; only the CLT
label on it is in question, and both candidate readings are on the warm/hot side.

*Caveat on that log:* one 1.000 s seam at t 3.20→4.20 where the 4.20 row is a byte-identical duplicate
of 3.20 and the spark counter advances only 17→19 — a logger/export seam, **not** a second of fruitless
cranking. Don't score it against the catch.

### What the same log says the start budget is actually spent on

Catch is ~2 revs; **settling is ~25 s.** Prime pulse touches none of it.

| Phase | Window | Behaviour |
|---|---|---|
| Post-catch sag | t 4.72–5.24 | caught, then fell back to **386 rpm** (below `crankingThreshold`) for ~0.5 s |
| Afterstart flare | t 5.28–5.84 | **1810 rpm** peak; `Idle air %` stepped 37 → 62 at t 5.00, ignition locked 24 ° for the full `afterstartIgnitionLockTime` |
| Crash | t 5.84–6.72 | down to **932 rpm** |
| Decaying hunt | t 6.7–~30 | ~1.0–1.3 s period; 3 s peak-to-peak **1427 → 302 → 175 → ~50** rpm, inside ±50 rpm only by t ≈ 30 |

Levers for that live in [idle.md](idle.md) / [engine_start.md](engine_start.md) (`idleCrankingDC` hot
bin vs `idleActiveAirflow` at target, `idleControlAfterstartDelay`, `afterstartIgnitionLockTime`,
idle-PID gains) — **not** in the fuel one-shot.

## Sizing method (per injector)

Size the prime to deposit **one cylinder's rev-1 wall film**, not the whole equilibrium puddle. The
equilibrium film is ≈ `x·N·(base dose)` — many ms-equivalents; laying that in one shot floods and
fouls (the documented 07-29 failure). The conservative, correct target is the single rev-1 deposit:

```
prime_eff(CLT)  ≈  E₁(CLT) × base_λ1_dose(CLT)     [effective ms, per injector]
```

- **`base_λ1_dose`** = the λ=1 cranking charge for one cylinder. Anchor: **1.72 ms effective** at
  MAP≈95 / VE≈64 / E25 / 36 °C (orifice model, `crank_fail_0729.md`; measured effective PW 1.43 ms
  in `cranking_ve_basis.md` corroborates the order). Scale by charge density ∝ 1/T_charge across CLT
  (colder = denser = larger dose): ≈ **1.72 × 309/T[K]**. Ethanol raises it (~+15 % E100, richer
  AFR_st) — use `crankingCorrTbl2`'s CLT column when on E85+.
- **`E₁(CLT)`** = rev-1 wall-film fraction over **true** stoich = Will's 08-06 rebuild schedule
  **0.70 (cold, E0) → 0.08 (hot)** (`cranking_ve_basis.md`). Intermediate bins interpolate that
  amplitude onto the concave shape of the current `crankingCorrTbl` rev-1 row. **Do not** use the
  raw table's implied E₁ — it carries the wrong VE basis (B≈0.79) and the old over-rich fouling error.

**CLT schedule is the whole point:** aggressive cold (big dry film to charge), **~zero hot**. A hot
restart has warm walls that flash fuel and residual charge present; extra prime liquid just pools and
fouls the cold heat-range-7 BKR7EIX plugs ([[project-supra-ignition-hardware]], the 112 °F fouling
saga). Zero the top CLT bins.

**Sanity anchor to running PW:** cold prime lands near ~1× the warm-idle injector PW and tapers to 0
hot — the lean side of the common "~1–2× running PW cold" heuristic, which is correct for this
fouling-prone cold-plug build.

## The coupled cut — prime and rev-1 enrichment are the SAME fuel

**Adding a prime pulse without cutting the early cranking revs double-doses the wall-film charge and
re-creates the flooding/fouling.** They are two delivery paths for one job. Conserve total early fuel:

```
prime  +  new rev-1 dose  ≈  old rev-1 dose
```

Since `prime ≈ E₁·base` and `old rev-1 = base·(1+E₁)`, the new rev-1 dose → ≈ `base` (i.e. the rev-1
enrichment goes toward **zero over true stoich**, keeping a small catch margin). Concretely on
`crankingCorrTbl` (row 0 = rev 1, closed-throttle):

- **Rev 1:** reduce by ≈ the prime's percentage-of-base (≈E₁: cold ~50–70 pts, warm ~5–15 pts, **hot 0**),
  keeping ~**10–15 % catch margin** (ignition near the flammability limit is probabilistic — the floor
  is a catch margin, not zero).
- **Rev 3:** reduce by ~half of the rev-1 cut (prime residue still helping the first few fires).
- **Rev 7 / 13 / 20:** ~no change — the one-shot prime is evaporated/entrained by then and the film is
  maintained by the running injection.
- If the **08-06 physics rebuild** is already loaded, rev-1 is already near the true-stoich floor, so
  the prime mostly lets you shave the remaining **cold** rev-1 margin rather than take a big cut.
- Apply the same logic to `crankingCorrTbl2` (ethanol) with its larger E₁; hot cells still → 0 prime.

## Hard preconditions (else the prime does nothing / hurts)

1. **Rail must be full at first trigger.** A prime pulse into an empty/filling rail delivers ≈nothing
   — `fprDeltaCorrection` clamps at 2.39× below 70 kPa and can't rescue an unfilled rail. The 07-29 /
   08-06 saga was exactly this (key-on prime not pumping → 0 bar at rev 1). Fix rail-prime first;
   the injector prime pulse presupposes pressure. See [crank_fail_0729.md](../supra/notes/crank_fail_0729.md).
2. **It speeds a *healthy* catch; it is not a fix for a U-limited or fouled-plug no-start.** Prime
   makes vapor available sooner, but if the plugs are wetted/fouled or vapor-λ is out of band (low U
   at high cranking MAP), no amount of prime lights it — read EGT+RPM texture first
   ([engine_start.md → zero-heat-release](engine_start.md)).
3. **Foot off during crank.** Any TPS off the cranking position triggers the anti-flood cut
   (`TPSScaleTbl`); prime + a stab of pedal is a flood, not a start ([[feedback-floodclear-crank-segments]]).

## Worked target (method fixed; re-read the tune before writing)

`base ≈ 1.72 × 309/T`, `E₁` = rebuild amplitude on the current rev-1 shape. Prime per injector in
displayed ms (`raw = round(ms × 8)`). **Revised 2026-08-24** after the measured-catch result above:
the ~70 °C bin catches in ≈2 revs with the present flat 1.0 ms, so everything from 69 °C up goes to
**zero** — there is no latency there to buy back, and liquid on a hot BKR7EIX is all cost.

| CLT °C | E₁ (E0) | base λ1 (ms) | prime (ms) | raw byte | basis |
|--------|---------|--------------|------------|----------|-------|
| 0   | 0.70 | 1.95 | **1.35** | 11 | derived — **untested, no cold log** |
| 17  | 0.70 | 1.83 | **1.25** | 10 | derived — untested |
| 34  | 0.50 | 1.73 | **0.85** | 7  | derived — untested |
| 51  | 0.30 | 1.64 | **0.50** | 4  | derived — untested |
| 69  | 0.22 | 1.55 | **0**    | 0  | **measured**: ≈2 revs to catch at ≈70 °C |
| 86  | 0.14 | 1.48 | **0**    | 0  | hotter than a measured-zero point |
| 103 | 0.08 | 1.41 | **0**    | 0  | fouling margin |
| 120 | 0.08 | 1.35 | **0**    | 0  | fouling margin |

Net vs the current flat 1.0 ms: **more cold, zero from 69 °C up.** The flat table is simultaneously
too little for a cold start and enough to wet a hot-restart plug.

**Order of work: delete the hot half first, then test whether the cold half is needed at all.** The
cold column is a derivation, not a measurement — the only log in hand is warm. Log a genuine cold
start with `CLT` in the layout and count revs-to-catch by the method above; if a cold start also
catches in ~2–4 revs, the honest answer is **no prime pulse anywhere** and the whole table goes to 0.

### Repeat-attempt exposure (the "second cold crank floods it" worry)

Prime fires on **every** sync event, so a failed attempt followed by a retry lays it twice. One-deposit
sizing keeps that harmless; "flood the port" sizing does not:

- Cold prime 1.35 ms × 1230 cc/min (`injectorsSize`, = 20.5 cc/s) = **≈20.6 mg** per injector.
- Cold base λ1 dose ≈ 1.95 ms ≈ **29.8 mg** → prime = **0.69 × base**.
- Two attempts = **1.4 base doses** of extra liquid, against a 20-rev crank that meters **20+** base
  doses. **≈7 % of the crank's fuel** — inside the noise of the CLT-column enrichment itself.
- A 5–8 ms "wet the port" prime would instead put **5–8 base doses** on cold walls before any fire,
  twice. That is the mechanism behind the documented 07-29 fouling failure.

The one-deposit rule is what makes the retry case safe. Do not size prime off flooded-engine intuition.

## Literature / patent benchmarks, and the re-verification against `updatedarmedstate.xml.emub3` (2026-09-10)

Re-derived independently against the newest XML export (**`updatedarmedstate.xml.emub3`, 2026-09-09
11:19**) with Will's stated cranking rail condition of **4 bar**. Symbols read fresh:
`fuelRailBasepressure` = 400 kPa (confirms the 4 bar assumption is the tune's own base, so
`injectorsSize` needs no √ΔP correction), `injectorsSize` = 1230 cc/min, `crankingLambdaTarget`,
`crankingCorrTbl`/`2` rev-1 row, `veTable` row 0 (500 rpm clamp), `injOpeningTimeTbl`,
`primePulseTable` (still flat raw 8 = 1.0 ms).

> **Caution:** the binary `Supra WAY MORE SAUCE.emub3` (2026-09-09 14:42) **postdates** that XML by
> ~3.5 h. Values below are from the XML; confirm nothing in the fuel/cranking group moved after it
> ([[feedback-stale-export-not-live-tune]]).

**The derivation reproduces:** cold `base λ1` comes out **1.93 ms** vs the note's `1.72 × 309/T`
formula's 1.95 ms, and `prime = E₁ × base` lands on raw **11 / 10 / 7 / 4** at CLT 0/17/34/51 — the
existing table to within one count. The table above stands; the current injector calibration confirms it.

### Evaporated fraction U — the term that actually sets the answer

The literature bounds on *U* (fraction of the first injection that becomes combustible vapor) are wide:

| source | condition | U |
|---|---|---|
| Heywood §11 (`corpus/ice_fundamentals.md` ~L27807, single-cyl 900 rpm / 0.5 bar) | warm-ish | "initially only about 50 %"; unaccounted-for fuel accumulates over "10 or so injections" |
| PFI cold-start studies (fast-FID in-cylinder HC) | 20 °C | **0.15–0.30** first cycle |
| same family, different fuel | 22 °C / 0 °C | **0.57 / 0.30** |
| Heywood §7.5 (`~L13593`) | cold start, qualitative | first (and sometimes second) injection per cylinder is dosed far above stoich; succeeding injections must then be **cut below** stoich to burn off the excess |

Required in-cylinder **φ ≈ 0.7–0.9** for a robust first fire (PFI cold-start literature). So the sizing
identity is `φ_v = U × m_liquid_available / m_stoich`, and **prime ∝ 1/U** — a quantity known only to
about ±2× at 0 °C. This is measure-don't-model territory; see the revs-to-catch method above.

### Cross-check of the table against that identity (CLT 0, E0, MAP 85 kPa, VE_true 0.80)

Liquid seen by the first intake event = prime + the rev-1 metered dose (`crankingCorrTbl` +58 % on the
VE-equation base at λ 0.90 → 2.58 ms). Stoich requirement 29.5 mg.

| prime | liquid/port | φ_v @ U 0.25 | φ_v @ U 0.30 | φ_v @ U 0.40 |
|---|---|---|---|---|
| 1.000 ms (current flat) | 54.7 mg | 0.46 | 0.56 | 0.74 |
| **1.375 ms (this note's table)** | 60.5 mg | 0.51 | **0.62** | 0.82 |
| 2.500 ms (= one extra rev-1 dose) | 77.6 mg | 0.66 | **0.79** | 1.05 |

**Finding:** at the mid literature U the note's cold cell leaves the *first* fire at φ_v ≈ 0.62 —
below the 0.7–0.9 robust band. That is not an error; it is the deliberate consequence of the current
strategy, which charges the film over `N` = 16 revs (cold, E0) rather than trying to fire on rev 1.
The prime as sized pre-pays the film tax the tune already books; it does not buy a rev-1 catch.

### The strategy fork (Will's call, not the note's)

- **A — keep the one-deposit rule (table above, raw 11/10/7/4/0/0/0/0).** Total early fuel conserved,
  repeat-crank exposure stays ~7 % of the crank's fuel, BKR7EIX fouling margin intact. Cold catch
  still takes several revs by design.
- **B — size for a rev-1/rev-2 cold catch (~2.5 ms cold, raw 20).** Puts φ_v ≈ 0.79 at U 0.30, matching
  the literature band, but **φ_v ≈ 1.05 if U is really 0.40** — i.e. it overshoots rich on a
  warmer-than-labelled port, on the fouling-prone cold plug. Only viable with the coupled rev-1 cut
  above actually applied, and it doubles the two-attempt liquid exposure.

Option B is what a first-principles first-fire calculation asks for; option A is what this build's
plug heat range and fouling history ask for. Both are internally consistent; they differ only in
whether rev-1 firing is a goal.

### Community ms figures are a trap — normalize to mass

Haltech / Megasquirt / HPA discussion converges on "**≈2 ms**, sometimes 5 ms, trial-and-error"
(Haltech KB; MSEXTRA threads; HPA forum — Andre Simon: *"this really does come down to one of those
'trial and error' areas"*). Those are **440–550 cc/min injector** numbers. At 440 cc/min, 2 ms =
**10.9 mg**; this build's 1.375 ms at 1230 cc/min = **21.0 ms-equivalent → 21.0 mg**, on the same
~500 cc/cylinder displacement. **The table is already ~2× the generic community dose in fuel mass** —
it only *looks* small because the injectors are ~3× the size. Never port a prime-pulse ms value
between builds; port the mass.

US 5,408,975 (*Priming control system for fuel injected engines*) corroborates the shape rather than
the magnitude: priming quantity is a pure function of temperature, independent of TPS and RPM, fired
on first crank detection into all throttle bodies simultaneously, monotonically decreasing cold→hot
(its example runs 1044.5 ms at −50 °C down to 8.2 ms above 50 °C on a two-cylinder snowmobile with
tiny injectors). It also adds a **second** priming pulse only if the engine has not reached 800 rpm
within ~0.5 s — a retry concept EMU Black does not expose.

### Ethanol: `primePulseTable` is fuel-blind

There is **no `primePulseTable2`** in the export, and no FF blend symbol for it — one table serves
E0 through E100. Running the same `prime = E₁ × base` rule on the E100 parameters
(`E₁` 1.15 → 0.14 per `cranking_ve_basis.md`, stoich 9.0, ρ 0.789) gives a cold requirement of
**≈3.42 ms**, i.e. **2.5× the E0 number**. Sizing the single table for E100 would badly over-prime a
gasoline start. **Size on E0 and leave the ethanol delta with `crankingCorrTbl2`, which already
carries it** — an under-primed E85 cold start costs revs, an over-primed E0 cold start fouls plugs.

### Deadtime frame

`primePulseTable` is almost certainly **net fuel time**, with EMU adding `injOpeningTimeTbl`
internally: at 400 kPa the table reads **1.531 ms @ 10 V / 1.375 ms @ 11 V** (raw/32 ms), so a factory
default of 1.0 ms would inject literally nothing if deadtime were the caller's responsibility, and
0.125 ms resolution would be meaningless under a 1.5 ms latency. **Confirm on the internal Scope**
(the only place prime is visible): if the observed injector on-time equals the table value rather than
value + ~1.5 ms, add the cranking-voltage deadtime to every non-zero cell before writing.

## Related

- [engine_start.md](engine_start.md) — cranking fuel equation, wall-film (Aquino) decay, VE basis
- [../supra/notes/crank_fail_0729.md](../supra/notes/crank_fail_0729.md) — base-dose orifice model, rail-prime failure, fouled-plug no-start
- [../supra/notes/cranking_ve_basis.md](../supra/notes/cranking_ve_basis.md) — B basis, E₁/N rebuild schedule
- Memories: [[cranking-fuel-equation-decode]], [[supra-cranking-airflow-is-flare-setpoint]], [[cranking-vapor-not-liquid]], [[project-supra-ignition-hardware]]
