# Oil-viscosity idle-airflow compensation — measured requirement

> **⚠ CONTRADICTED IN PART, 2026-08-30.** The **5.45 %/bar** oil-pressure slope below is
> **not reproduced** in later data. At settled hot idle (target 1200, CLT ≥ 94, base flat) the
> total requirement vs oil pressure measures **+0.01 %/bar** — the `Idle airflow custom corr.`
> table removes **+3.88 %/bar** and the airflow PID puts back **−3.91 %/bar**, cancelling. In a
> single warm-up-to-hot drive every candidate is monotone in time (r(oilP, runtime) = −0.99,
> VIF 150), so the oil coefficient is **not identified** and flips sign with conditioning.
> Treat the slopes below as time-decay attributed to oil pressure. See
> [idle_bog_and_airflow_hump_20260830.md §4](idle_bog_and_airflow_hump_20260830.md).

**Purpose.** Size the oil-temp-scheduled idle-airflow modifier that replaces the IAT-indexed
`idleCustomCorrection` (the "DBW TB heating" compensation). Answers two questions with logged
data: *how much idle airflow does the engine need when coolant is at the hot cells but the oil
is still cold*, and *how little does it need once the oil has caught up.*

Context and the failure this fixes: [idle_drive_wobble.md](idle_drive_wobble.md) §2026-07-30.
Live tables and the actuator window: [airflow_actuator.md](airflow_actuator.md).
Oil-pressure sensor cal and the RPM×CLT baseline: [`../../notes/oil_pressure.md`](../../notes/oil_pressure.md).
Raw measurement layer — airflow binned on (oil pressure, RPM, CLT) with no model subtracted,
plus the reachability map showing only 25 of 200 cells are observable:
[oil_pressure_airflow.md](oil_pressure_airflow.md).

---

## Evidence base

11 CSV logs spanning **2026-05-24 → 2026-07-30**: 6 cold-start warmups (segment begins CLT
28–44 °C and reaches ≥96 °C) plus 8 hot-restart segments. ~11,000 stable-idle samples, all at
**idle target 1200 rpm** (the target table is flat 1200 for every CLT ≥ 75, so hot idle is a
single-RPM dataset — see *Gaps* below).

Files: `20260524_1301`, `drive_wobble`, `drivehome`, `new_fuel_strategy`,
`all-channels-reduced-idlaircorr`, `20260613_1141`, `cold idle dip again (+3)`,
`died_hot_return_to_idle_again`, `crank_fail_0729`, `armedstatebogjuly17`, `randomlydied`,
`idle0719`, `before_increased_active_airflow`.

**Stable-idle mask.** `Idle state == 2` ∧ `TPS < 15` ∧ `PPS < 3` ∧ `Driven axle speed < 2`
∧ `|RPM − Idle target| < 60` ∧ rolling σ(dRPM/dt) < 100. Coolant fan is **on** in every hot
sample and A/C is off throughout, so neither is a differential confound.

### Airflow % and TPS % are interchangeable across the whole period

The actuator window was recovered **empirically per log** by regressing logged `TPS` on
`Idle air %` (`TPS = floor + air/100 × width`): recovered floors 2.38–2.64, ceilings 7.39–7.96
— i.e. `idleDBWTargetMin/Max` = **2.4 / 8.0** for every log in the set. So

```
TPS %  =  2.4 + airflow% / 100 × 5.6
```

holds throughout, and airflow % is directly comparable across all the intervening table
changes. Verified both ways on the extremes: 28.0 airflow% → 3.97 TPS (logged 3.9);
56.5 airflow% → 5.56 TPS (logged 5.5). Logs missing `Idle air %` (July 17–19) were converted
from logged TPS through the same relation.

### Independent re-verification — 2026-08-01, second pass

A fresh pass over **16** qualifying logs (every Supra CSV carrying `Idle air %` + `Idle state` +
`CLT` + the airflow PID — adds `hood on 0509 terrible day`, `all-channel-reference`,
`drive_home_today`, `20260526_09xx`, `more_tip_in` to the first-pass set) reproduced both anchors
independently, using **total commanded `Idle air %` at held-target idle** as the requirement:

- **Hot-oil anchor: 29.5 airflow % (IQR 27.0–30.5, n=9251 held samples across 7 logs)** — with the
  airflow PID at a settled median **−4** and RPM ~+7 above target, so the engine was getting slightly
  more air than it needed: the true minimum-to-live is **≤ 29**, ~28. *(Correction: −4 is a **free**
  settled output, NOT a clamp — the logged channel is the PID **output**, whose limits are −6/+15;
  the integral limits −4/+12 are internal and never appear in the log. Only a bit-exact pin at
  −6/−15/+15/+25 is a clamp. See the clamp-reading rule in the Method note.)*
- **Cold-oil anchor: the clean unclamped peak in `before_increased_active_airflow` reads 53 %
  median / 58 % p90 / 59.5 % max at PID +14–20 of the 25 clamp**, with RPM still sagging ~37 below
  the 1200 target — the requirement is if anything a hair *above* the reading. Logs still on the old
  +15 clamp censor at ~50 % (`all-channels-reduced` 90–180 s bin: 50 %, 84 % of samples pinned at
  the clamp) — lower bounds, exactly as flagged.
- **Adder confirmed: +25 airflow % central** (clean-to-clean 58 − 29 ≈ **+29**; censored-conservative
  ≈ **+20**). Airflow-vs-viscosity-index is monotone with the steep drop at index **2.4 → 2.1**,
  matching Result 3.

One addition from the broader set: in the **fast** warmup (`20260613_1141`, CLT hits 96 in 160 s)
the demand peak sits in the **pre-96** window (51.5 % at viscosity index 5.35), not after it. The
requirement tracks **oil**, not the coolant crossing — which is precisely why the compensation has
to be an **oil-temp-indexed table**, not a coolant-time afterstart ramp. `Engine oil temperature`
reads flat **0** in all 16 logs (failsafe → EMU substitutes 100 °C): no real oil-temp axis yet,
sensor pending.

---

## Result 1 — the two anchors

**Cold start** (segment begins CLT < 45 °C), binned by time since CLT first reached 96 °C:

| since CLT 96 | total airflow % | TPS % | PID corr | oil press | n | logs |
|---|---|---|---|---|---|---|
| 30–90 s | 48.2 | 5.1 | **+7.4** | 4.25 bar | 232 | 3 |
| **90–180 s** | **51.0** (q75 **56.5**) | **5.2–5.5** | **+15.0 — at clamp** | 4.25 bar | 517 | 3 |
| 3–6 min | 41.5 | 4.7 | +3.5 | 3.19 bar | 2367 | 2 |
| 6–10 min | 32.5 | 4.3 | −3.9 | 2.50 bar | 79 | 1 |
| >10 min | 31.0 | 4.1 | −4.0 (free, not clamp) | 2.06 bar | 36 | 1 |

**Warm restart** (segment begins CLT ≥ 90 °C — oil already partly hot), same binning:

| since CLT 96 | total airflow % | TPS % | PID corr | oil press |
|---|---|---|---|---|
| 0–30 s | 37.5 | 4.5 | −0.5 | 2.81 bar |
| 30–90 s | 42.9 | 4.8 | +6.1 | 3.62 bar |
| 90–180 s | 35.7 | 4.4 | −1.9 | 3.00 bar |
| 3–6 min | 30.4 | 4.1 | −6.0 | 2.31 bar |
| >10 min | 28.6 | 4.0 | −9.0 | 2.06 bar |

### The clean cold-oil measurement — `before_increased_active_airflow.csv`, 2026-07-30

The only cold start in the set logged **after** `idleAirPIDOutMax` was raised 15 → 25, so the
PID had headroom to actually satisfy the demand instead of clipping:

| t since CLT 96 | airflow % | TPS | PID | RPM (tgt 1200) |
|---|---|---|---|---|
| +100 s | 47.3 | 5.0 | +10.5 | 1135 |
| +120 s | 51.0 | 5.2 | +14.0 | 1190 |
| **+140 s** | **58.0** | **5.6** | **+18.8** | 1139 |
| +160 s | 57.0 | 5.6 | +17.5 | 1205 |
| +200 s | 45.0 | 5.0 | +5.9 | 1259 |
| +240 s | 42.5 | 4.8 | −1.3 | 1207 |
| +280 s | 38.5 | 4.5 | −5.4 | 1175 |

Peak demand **57–58 airflow % (5.6 % TPS)**, PID unsaturated at +18.8 of 25 — this is a real
measurement of the requirement, not a clip. It collapses ~19 points in the following 2 minutes.

### Anchors

| state | total airflow % | TPS % | basis |
|---|---|---|---|
| **Hot coolant (96 °C), cold oil** | **51–58** | **5.2–5.6** | cold-start peak, 1.5–3 min after CLT 96 |
| **Hot coolant, hot oil** | **28–31** | **3.9–4.1** | ≥10 min after CLT 96, 4 logs |
| **Difference** | **+20 to +29** | **+1.1 to +1.6** | ≈ **1.7–1.9×** the hot-oil requirement |

**Both anchors are conservative in the same direction.**
- The cold anchor is a *lower* bound wherever the PID clipped: on 2026-05-31 the PID sat pinned
  at its +15 output clamp for 99 % of the 30–90 s bin and 51 % of the 90–180 s bin while RPM
  sagged to 1121 against a 1200 target — the ECU wanted more air than it was allowed to give.
  **That saturation is the airflow starvation, captured.**
- The hot anchor: the PID settled around a mild **negative** trim (~−4 output) for 81–99 % of the
  >10 min samples (drivehome 99 %, new_fuel_strategy 94–98 %, all-channels-reduced 81 %), so the
  engine was running a touch richer in air than it strictly needed. *(Correction: −4 is a **free**
  settled output, not the −6 output clamp — so the loop had NOT run out of authority; it was
  regulating freely. The hot anchor ~29–31 is therefore a real settled requirement, an upper bound
  **only** in the specific windows where the output pinned bit-exact at −6/−15. True hot-oil
  requirement ≈ 29, possibly a hair under.)*

So **+25 airflow % (≈ +1.4 % TPS) is a sound central estimate of the cold-oil adder**, and the
true spread is wider than +20/+29, not narrower.

---

## Result 2 — the shape (and why idle "struggles then recovers")

Timeline of a cold start, pooled across the six warmups:

1. CLT reaches 96 °C at **100–190 s** of runtime.
2. Airflow demand keeps **rising for another 1.5–3 minutes** — it peaks *after* the coolant is
   already done. Peak at t96 + 90–180 s in five of six logs (05-31, 06-13, 07-17 seg3, 07-19,
   07-30); the sixth (05-24) is a warm-ish start with the peak at t96 + 80 s.
3. Demand then decays, reaching the hot-oil floor at **t96 + 8–12 min** ≈ **11–15 min total
   engine runtime**.

That rise-then-fall is the reported symptom exactly: fine for a bit, struggles, recovers. The
base table hands over to its 96/105 °C columns on schedule while the friction load is still
climbing, so the PID is left to cover a growing gap with a ~750 ms-lagged actuator — and in the
pre-07-17 tunes it hit its clamp partway up.

---

## Result 3 — it is oil, not coolant and not charge temperature

Oil pressure is a direct viscosity measurement. Normalizing it for pump speed
(`visc index = OP[bar] / RPM × 1000`, sampled at 1500–2500 rpm) over the warmups:

| runtime | drivehome | all-ch-reduced | 20260613 | CLT |
|---|---|---|---|---|
| 1 min | 3.72 | 3.97 | 3.87 | 48–67 |
| **3 min (CLT 96 reached)** | **3.06** | **3.39** | **3.34** | **96** |
| 6 min | 2.25 | 2.37 | 2.71 | 96 |
| 10 min | 1.89 | 2.04 | 1.99 | 96 |
| 18–23 min | 1.72 | 1.67 | — | 96 |

**Coolant is flat at 96 °C for the entire right-hand side of that table while the viscosity
index falls another 44 %.** That is the lag, measured, with no modelling.

Charge temp is ruled out as the driver: `Charge temp` **rises** 40 → 52 °C across the same
window, and hotter (less dense) charge would require *more* throttle to hold torque, not less.
The observed fall can only come from friction dropping.

Converged samples only (PID actively regulating, neither clamp, CLT pinned 96, target 1200):

| visc index | total airflow % | IQR | n |
|---|---|---|---|
| 3.0–3.6 | 43.5 | 42.0–48.9 | 294 |
| 2.7–3.0 | 42.5 | 41.0–44.0 | 590 |
| 2.4–2.7 | 41.0 | 40.0–42.5 | 677 |
| 2.1–2.4 | 33.0 | 32.0–34.0 | 155 |
| 1.8–2.1 | 32.5 | 31.5–34.0 | 75 |
| 1.4–1.8 | 31.0 | 30.6–32.0 | 34 |

Monotonic, with the steep part between index 2.4 and 2.1. *(The >3.6 bin is omitted — excluding
PID-saturated samples there leaves a biased remnant, n=107 with IQR 35–49.)*

**Use this as the interim x-axis.** One warmup logged with oil temp *and* oil pressure together
converts the whole table to a real oil-temp axis in one pass.

---

## Result 4 — viscosity-law cross-check (2026-08-01)

*Does the measured airflow-vs-oil-temperature obey lubricant theory?*

**Law.** Engine-oil viscosity follows Vogel / Walther (ASTM D341): μ falls steeply then flattens
with temperature. Heywood builds mechanical friction from exactly this — Vogel low-shear μ(T)
(Eq. 13.25), shear-thinned to the high-shear regime — `corpus/ice_fundamentals.md` §13.35.

**The magnitude that matters.** Heywood Fig. 13.35 (15W-40, 5.4 L, 2000 rpm):
*"friction in a just-started engine at 20 °C is twice that in a warmed-up engine at 90 to 100 °C"*
(`corpus/ice_fundamentals.md:34958`). Friction only ~**2×** across a swing where **bulk viscosity
rises ~10–13×** (Walther, any multigrade). Most FMEP — rings + gas pressure, valvetrain boundary
friction, pumping — is viscosity-insensitive, and multigrade shear-thinning cuts the rest. So
**friction ∝ μ^~0.3, not μ.**

**Match.** Measured idle airflow: hot-oil **29 %** → cold-oil peak **56 %** = **1.9×** — lands right
on Heywood's ~2× friction increase. Idle airflow tracks *friction*; friction ~doubles cold. ✓

**Consequence — do NOT scale the adder by oil pressure / bulk viscosity.** A linear-in-viscosity-index
fit over 15,821 clean clamp-excluded held-idle samples gives `air = 21.6 + 5.14·(OP/rpm×1000)`,
**R² only 0.45**, and extrapolates to **>100 % airflow at 30 °C** — nonsense, because it scales by μ
(13×) not friction (2×). The adder **saturates near +27–30 airflow % (≈ 2× the hot baseline)** and
does not climb past it however cold the oil. `corr(air, charge temp) = −0.47` (wrong sign)
reconfirms charge heating is not the driver.

**Oil-temp mapping (OP proxy, confounded).** Anchoring hot-idle μ at 105 °C oil: demand-peak
(viscosity index ≈ 3.3) ≈ oil **77 °C**; coldest held-idle oil (index ≈ 5.4) ≈ **60 °C**. Oil is
**never near 30 °C at hot-coolant idle**, so 30/49 °C cells are cold-start / extrapolated, not
measured. One warmup logged with the real oil-temp sensor replaces this proxy.

**Adder table — 1200 rpm row, friction-shaped, capped at the 2× ceiling:**

| oil °C | 30 | 49 | 68 | 86 | 105 |
|---|---|---|---|---|---|
| **+airflow %** | +28 | +27 | +24 | +13 | 0 |

105/86 measured; 68 near the peak; 49/30 sit at the friction ceiling (cold-start extrapolation, no
hot-coolant data that cold). Cooler note: the Chase Bays plate **diverts, not blocks** above ~82 °C
(*Maximum Boost* ch.4), so idle oil regulates ~90–105 °C — no table bin above 105 is needed.

## Result 5 — oil pressure as the compensation axis (2026-08-01)

The oil-temp table can be **replaced by an oil-pressure × RPM correction, and oil pressure is the
better axis.** Physics: pump gallery pressure `P ∝ μ·N` and viscous (Petroff) friction `∝ μ·N` — the
same product — so oil pressure folds viscosity (temperature) *and* engine speed into the exact
quantity idle airflow must overcome. No new sensor (logged today), and unlike oil temp the logs
already span the RPM axis, because cold start rides an elevated idle target at high pressure.
EMU exposes oil pressure as a valid custom-correction axis (owner's live table: X = oil pressure,
Y = engine RPM).

**Empirical validation** — 33,836 held idle-envelope samples (state 2, foot off, steady), 11 logs:
- `air = 22.5 + 4.1·P[bar]`, **R² 0.51**; adding RPM lifts R² by only **0.002** (RPM 0.6 %/100 rpm).
  `corr(air,P)=0.72 > corr(air,RPM)=0.42`. **Pressure alone ≈ pressure + RPM** — P already carries N.
- Operating locus is **diagonal**: hot idle ≈ 1200 rpm / ~2 bar; cold-start idle 1375–1600 rpm /
  5–7 bar. Off-diagonal corners (low rpm+high P, high rpm+low P) are unreachable.
- Idle oil pressure spans ~1.9 bar (hot) → 7.7 bar (cold start). The **10 bar column is
  relief-plateau, never reached at idle**; the 7.81 column only at cold-start elevated idle.

**Max idle oil temp ≈ 112–114 °C** — min sustained idle pressure ~1.9 bar back-mapped through Walther
(anchoring median idle ≈ 100 °C). The 82 °C cooler regulates it; nothing above that is exercised.

**Correction — fitted, not eyeballed** (dep = total `Idle air %` at held idle, 33,836 samples):
- demand `air = 4.13·P[bar] + 22.5`, **R² 0.51**; RPM adds R² 0.002, and the **viscosity index fits
  *worse*** (R² 0.49) → **raw pressure is the correct axis** (friction ∝ μ·N = P, not μ).
- hot-idle pressure `P_hot = 1.885e-3·N` (through origin; 3,911 hot foot-off samples incl. re-entry)
  = 1.89 / 2.07 / 2.26 / 2.59 / 2.83 bar at 1000 / 1100 / 1200 / 1375 / 1500 rpm.
- **correction(N,P) = clip( 4.13·(P − P_hot(N)), 0, 27 )** — the +27 clip is the Result-4 Heywood 2×
  ceiling (only bites above ~8 bar, which idle never reaches).

| rpm \ oil bar | 2.4 | 3.5 | 5.0 | 6.5 | 8.0 |
|---|---|---|---|---|---|
| **1000** | 2 | 7 | 13 | 19 | 25 |
| **1100** | 1 | 6 | 12 | 18 | 24 |
| **1200** | 1 | 5 | 11 | 17 | 24 |
| **1375** | 0 | 4 | 10 | 16 | 22 |
| **1500** | 0 | 3 | 9 | 15 | 21 |

**Rows are NOT flat** — the airflow *slope* is RPM-independent but the **zero-crossing rides P_hot(N)**
(higher rpm = higher hot pressure), so higher rows start rising later. That is exactly what makes idle
**re-entry** correct: a *hot* return at 1600–2200 rpm sits at ~3.6 bar → correction ≈ +1 (no flare);
a *cold* return at the same rpm sits at ~7 bar → +17 (kills the bog). Row-to-row spread ≤5 %. (The
correction applies only in ACTIVE idle; the armed portion of a return is governed by `idleArmedAirFlow`,
not this table.) **Sign is POSITIVE** — opposite the old IAT table (high P = cold = add air).

**Warm-up shape** (1150–1250 rpm, fitted): `P(t) = 2.40 + 3.71·e^(−t/6.16 min)`, **R² 0.67** — pressure
decays ~6.1 → 2.40 bar hot asymptote (~6 min constant), still falling after coolant pins at 96 °C. On
the **shipped bins** move the first breakpoint 1.25 → ~2.4 bar, else hot idle interpolates to a small
phantom correction (with the fitted values, ~+2, not the +6 the earlier eyeballed curve implied).

**Y axis = actual RPM, not idle target.** P is generated at the *live* rpm, so pairing it with actual
rpm keeps the cell on the true instantaneous (μ, N); the 2-D grid then decodes viscosity correctly —
a hot low-rpm sag lands at low P (small correction), a cold elevated idle at high P (big correction),
which idle-target-Y cannot separate. Minor caveat: base `idleActiveAirflow` is indexed on the idle
*target*; at steady idle they coincide and the PID backstops the transient difference.

**Architecture — one decision.** This correction is the FULL friction adder (0 → +27). Added to the
current base table (which still has cold CLT columns) it **double-counts at cold start**. Cleanest:
**flatten the base active-airflow CLT columns to their hot values** and let oil pressure own all the
warm-up air — measured demand shows the old cold columns over-delivered anyway (PID sat on its
negative clamp). Keeping the base as-is means halving the correction, and is worse.
*(Superseded in detail by Result 6: the double-count is demonstrated per-cell in the 06/13 data,
and the shipped table gains a negative low-P column that absorbs the old IAT table's soak trim.)*

## Result 6 — single-log validation + architecture reconciliation (2026-08-02, 06/13 data)

Independent re-derivation from `20260613_1141` alone (extract: `oil temp data.xlsx`, 17,246
samples @25 Hz, 690 s: cold start CLT 33 → drive → stall+instant restart at t=305.8 → hot idle),
against tune `supra 06132026.xml.emub3` (copied to `supra/tunes/`). Equilibrium mask: state 2,
MAP<60, |RPM − reconstructed target|<60 (target = `idleRPM`[CLT] on cltBins −40…110, or +200
VSS-elevated candidate), rolling |ΔRPM|<40, PID not pinned at −6 → 3,336 samples.

**Composition (re-verified, this log):** `Idle air % = idleActiveAirflow(CLT, target) +
idleCoolantFanCorr·fan + idleCustomCorrection + PID` — additive model residual −1.2 ± 3.0 vs
scalar −2.2 ± 3.3 (custom-active samples −1.8 vs −3.7). **The 06/13 custom table ran additive**
(`idleDCCorrBehaviour = 1` = Add), despite the 05/26 scalar-mode note. New table must be Add mode.

**Armed state is clean — help + data agree.** EMU Idle help (docs/emu-black-help/Idle.md), twice,
bold: *"Custom correction is used only in Idle Active state."* Empirically: armed samples (state 1,
n=603) give `air − idleArmedAirFlow(RPM)` = **−0.03 ± 0.15** — the armed output is the armed table
EXACTLY. Not even the fan +13 enters armed. So the oil-pressure correction cannot alter armed
behavior; a cold return's armed phase stays on the (cold-blind) armed table and the correction
engages only at active handoff — where oil pressure is already valid and instantaneous.

**Fit (fan-aware, this log):** `corrB = air − base_hot(N) − 13·fan` → `corrB = 5.45·P − 20.4`,
**R² 0.75** (vs fleet 4.13·P slope, R² 0.51 — fleet slope is attenuated by P-measurement noise and
fan-state mixing; the fan-explicit single-log slope is the cleaner structural estimate). Zero
crossing 3.73 bar pooled. Measured anchors: soaked hot idle (t>600 s, OP 2.34–2.44, CLT 96–98)
needs **31.5–32.5 total** → corrB **−8**; cold hold (OP 6.6–7.3, fan off, target ~1330) needs
50–57 total → corrB **+19 to +21**; (8.0 bar, 1375 row) measured **+21** vs line +23 →
**saturation near +24 confirms the Heywood 2× ceiling** (base_flat+cap = 40+24 = 64 ≈ 2.03× the
31.5 hot total, matching friction ~2× cold).

**The double-count, demonstrated in-data (kills the keep-base-as-is plan):** residual vs the
CLT-indexed base (`corrA`) at the same (6.5 bar, 1375 rpm) cell is **−1.0** during the cold start
(CLT<60 — the base's cold columns already deliver the air) but the fleet's hot-coolant/cold-oil
measurements at the same pressure need **+16**. One cell, two required values, CLT the hidden
variable → a (P, N) correction is only single-valued if the base stops carrying warm-up air.
Companion change: **flatten every `idleActiveAirflow` row to its 96 °C-column value**
(rows become 16.5 / 21.5 / 26.5 / 35 / 40). Hot behavior is untouched by construction.
**Executed 2026-08-02** → `supra/exports/Airflow - Active state air flow [%] (flattened for
oil-pressure corr 20260802).emubt` (bytes 21/2B/35/46/50 ×8 per row — identical to the tune's own
96 °C column bytes, encoding proven). **⚠ Import order: the oil-pressure correction must be live
first (or in the same session) — the flatten alone strands a cold start at 31–40 % open-loop
against the measured 50–57 % requirement.** *(Terminology note, same date: in the 2026-08-02
exchange Will's "armed state airflow table" referred to THIS Active-state map — the 87.5 cold
corner, CLT axis, 1500 bin — not `idleArmedAirFlow`; his directive was this flatten. Recorded in
`reference/lexicon/glossary.md`. The armed-descent analysis further below concerns the true 8×1
armed table and stands on its own.)*

**Base is deliberately fat at hot — keep it; let the correction go negative.** base+fan at 1200 =
39.5 vs measured soaked demand 31.5: the +8 surplus is the open-loop anti-stall guarantee
(standing rule: never trim base to recenter a negative trim). The old IAT table's −6 soak trim was
this same −8, proxied through CAT. Re-attribute it to the pressure axis: **the 2.38-bar column
carries −5…−8** (soak = thin oil = low P). Rolling hot idle at 1375–1500 rpm measures −13…−19
(those rows' hot values are transient-catch cushions, sized cold) — floor the table at **−8**
anyway: PID −6 covers part of the rest, riding a few % high while rolling is today's behavior too,
and a deeper negative would make the sensor-failure case dangerous.

**Shipped table** = `clip( 5.45·(P − P0(N)), −8, +24 )`, `P0(N) = 3.59 + (P_hot(N) − P_hot(1200))`
= [3.22, 3.40, 3.59, 3.92, 4.16] bar for N = [1000, 1100, 1200, 1375, 1500]:

| rpm \ oil bar | 2.00 | 3.50 | 5.00 | 6.50 | 8.00 |
|---|---|---|---|---|---|
| **1500** | −8 | −4 | +5 | +13 | +21 |
| **1375** | −8 | −2 | +6 | +14 | +22 |
| **1200** | −8 | 0 | +8 | +16 | +24 |
| **1100** | −8 | +1 | +9 | +17 | +24 |
| **1000** | −7 | +2 | +10 | +18 | +24 |

Measured-cell agreement: (2.38, 1200) −7 vs measured −7.2 ✓; (8.0, 1375) +22 vs +21 ✓;
(6.5, 1287–1437) +15 vs +18.8 and (3.5, 1200 post-restart) 0 vs +3.8 — line runs 3–4 under
mid-range (conservative direction; PID +15 covers). 1000/1100 rows extrapolated (no equilibrium
samples below ~1150 in this log). If the 0-floor (positive-only) variant is preferred, zero the
negatives: hot soak then rides ~+8 open-loop with PID −6 against it — roughly today's behavior
minus the old IAT trim.

**Sensor-failure direction (axis input):** `oilPressureFailSafe = 0` → failed sensor substitutes
**0 bar** → table clamps to the 2.38 column. Hot idle: −5…−8 ≈ the correct soak trim (fine).
Cold start: loses the adder → flattened base + PID +15 leaves ~−10 vs demand → low/rough first
minutes, alive (fleet precedent: +15-pinned starts sagged to ~1120 without stalling). The
oil-TEMP failsafe substitutes 100 °C (`oilTempFailSafe = 100`) — an oil-temp-axis table would
also fail to ~zero correction; the pressure axis additionally doesn't depend on that sensor at all.

**Oil vs coolant decoupling — when (answer to "only at startup?"):** never assume tracking; P
measures μ live, so the table is thermal-history-agnostic. Measured decouplings: (1) warm-up — the
big one, τ ≈ 6.1 min after CLT pins (Result 2/5); (2) running load changes — cooler/sandwich-plate
(opens ~82 °C oil) modulates the oil side only, CLT thermostat-pinned; (3) soak restarts — mild:
fleet warm-restart 0–30 s reads 2.81 bar vs 2.06 fully hot (+0.7-bar thickening ≈ +3 correction,
decays in minutes); the 06/13 stall+instant restart (0.4 s off) shows none (3.19 → 3.50 bar).
Cool-down while driving = case 2; cool-down parked = case 3. All three land on the correct cell
automatically because P is the input.

## Result 7 — deep-soak demand anchor (2026-08-02 evening, `oil data after 25 minutes.csv`)

8.1-minute post-drive idle hold, ECU uptime 17.4 → 25.5 min, target 1200 throughout, `Idle target`
logged directly; old IAT custom still active (walks −1 → −11 as the bay soaks). n=3,935 equilibrium
samples. Pressure stats agree with the floor analysis below (median 2.12, p5 1.88, min 1.69–1.81).
**Composition verification, cleanest yet: `air − (26.5 + 13·fan + custom + PID)` = +0.19 ± 0.27.**

What the pressure floor did not yet include — the **demand** there: total air settles
**26.5–28.5 %** (PID −4 free, custom −7…−11), i.e. **corr vs base+fan = −11 median, −13 in the
final minute**. Back-mapped viscosity index 2.06/1.2 ≈ 1.72 ≈ **oil 112–114 °C — the idle
oil-temp ceiling**, so ~1.8–2.1 bar is the physical bottom of the axis, not a data gap.

**Demand vs P is convex.** Anchors on the 1200 row: (2.06, −13) (2.12, −11) (2.40, −8; R6)
(3.62, +4; R6 restart) (6.5, +17…19) (8.0, +21…23 saturating). Slope ≈ **10 %/bar below ~3.5 bar**,
4.5–5.5 above — the μ^0.3 law (d demand/dP ∝ P^−0.7, largest at low P) with the Heywood 2× ceiling
bending the top. A 5-bin piecewise-linear table captures it if bin 1 sits at the floor.

**Idle-entry transient caution:** air walks 38 → 30.5 over the first two minutes at near-constant P
— that is the IAT custom walking −2 → −7 with bay soak plus the PID draining, ignition PID buffering
RPM meanwhile. Settling, not requirement; only the settled tail anchors.

**The fork — two coherent designs, one decision (reconciles the floor paragraph below):**
- **A. Fat base + signed table (recommended).** Keep `idleActiveAirflow` hot values as-is (flatten
  only the CLT dimension); the low-P column goes **negative** (−14 at the 1.75 bin, 1200 row),
  absorbing the old IAT table's soak trim. Argument: the custom correction is **active-state-only**
  (help + armed proof, R6) — every non-active state (armed handoff aside, recovery, afterstart,
  PID-reset moments) runs on base+fan alone, so the base must stay fat enough to carry them at any
  oil state; the standing open-loop-guarantee rule says the same. PID then centers ~0 at soak.
- **B. Trimmed base + positive-only table (the floor paragraph's "no-add, fail-high" design).**
  Re-anchor base at the soak state (≈14.5 + fan 13 ≈ 27.5 open-loop) and floor the table at 0.
  Same arithmetic in active state, but non-active states inherit the thin base mid-warm-up, and it
  trims base to recenter a trim — the exact move the guarantee rule forbids.
- Sensor-failure (0 bar → bin-1 column) is nearly a wash: hot idle correct either way; a failed
  sensor's cold start is short ~15 pts under A (PID-recoverable sag, fleet precedent) and ~15–30
  under B depending on how far base was trimmed.

**Final table (supersedes R6's; axis bin 1 moved 2.38 → 2.00 bar — 5-bin width is firmware-fixed,
so 2.38 is replaced, not prepended).** 2.00 vs the floor paragraph's 1.75 is a **functional
near-wash decided on provenance only**: the 2.00 cell is a measurement (1.95–2.15 band, ~4,000
samples read −11…−13) while a 1.75 cell is a free parameter tuned so interpolation passes through
those same points; both fits reproduce every anchor, encoding is clean either way (32/16 vs 28/16),
and the 0-bar failsafe reads bin-1 in both. *(Retracted 2026-08-02: an earlier draft claimed the
below-bin clamp made 2.00 the safer dip dynamic — the absolute-value check shows the opposite sign:
in a 1200→1050 sag with P 2.1→1.84, the 2.00 table clamps to −8.0 while the 1.75 table interpolates
−7.3, i.e. the lower bin is marginally MORE generous mid-sag. Difference ≤1 pt; the row valley
(±4–8) dominates dip behavior in either table.)* 1.75 remains an acceptable alternative:

| rpm \ oil bar | 2.00 | 3.50 | 5.00 | 6.50 | 8.00 |
|---|---|---|---|---|---|
| **1500** | −4 | 0 | +9 | +15 | +21 |
| **1375** | −6 | +1 | +10 | +16 | +22 |
| **1200** | **−13** | +3 | +11 | +17 | +23 |
| **1100** | −10 | +5 | +12 | +18 | +24 |
| **1000** | −6 | +6 | +13 | +19 | +25 |

The 1200/2.00 cell is the measured terminal value (air 26.5 at 2.06 bar, final minute; −12 would
center the 2.1–2.4 band instead — either is within PID range, endpoint preferred as the asymptote).
Interpolation reproduces the anchors (1200 row): 2.12 → −11.7 (meas −11), 2.40 → −8.7 (meas −8),
3.62 → +3.6 (meas +4); below 2.00 clamps at −13 (correct at soak, freeze-not-deepen during dips). The negative column is a deliberate
**valley centered on 1200** (the settled row): 1000/1100 relax to −6/−10 so a hot sag (corr keys on
actual rpm, base still reads target) gains +4…+8 recovery air; 1375/1500 cap at −6/−4 despite
rolling-idle steady-state wanting −13…−19, because those cells also serve the warm-start ramp
descent and starving the catch repeats the armed-bog failure. Cost: hot rolling idle rides a few %
high — today's behavior.

## Result 8 — cold-reference log kills the flatten and shrinks the P-term (2026-08-02 ~10 PM, `supra/logs/Cold oil reference.csv`)

Fresh CLT-28 cold start (coldest yet), 9.3 min, run as an **old-config baseline**: custom reads
0/−1 (IAT table live, P-table not), composition fits the **unflattened** base at +2.8 ± 5.5
(base has drifted since 06/13 — current XML export now blocking), and the **PID output floor is
now −10** (was −6). Slow warmup: CLT 96 at t=326 s. Pooled 3-log equilibrium grid (n=11,848;
entry-age > 20 s, pin-censored), need = air − base_hot(target) − 13·fan:

| CLT \ P bar | 1.7–2.5 | 2.5–3.5 | 3.5–4.5 | 4.5–5.5 | 5.5–6.5 | 6.5–7.5 |
|---|---|---|---|---|---|---|
| **≤35** | — | — | — | — | — | **+26.7** |
| **35–55** | — | — | — | — | — | +16.2 (47 % pinned → upper bd) |
| **55–80** | — | — | — | +2.5 | +3.5 | **+6.5** |
| **80–95** | — | — | +4.3 | −5.5 | −0.5 | — |
| **≥96** | **−11.5** (n=2828) | +4.1 | +3.6 / −2.5 | **−8.0** | −3.0 | — |

**1. δ(CLT) — the second-order term Will called — is measured and it equals the OLD cold columns.**
At P 6.5–7.5: +26.7 (CLT ≤ 35), +16 (35–55), +6.5 (55–80), ~0 (≥ 80). Old base CLT-30 column at
1200 = 52.5 = hot 26.5 + 26 — the old columns were carrying a real, correctly-sized cold-engine
term (combustion/quench/cold-bore), not redundant oil air. **The flatten is dead.**
`Airflow - Active state air flow [%] (flattened for oil-pressure corr 20260802).emubt` is
**SUPERSEDED — do not import.** v2 base: keep the CLT columns; only the 60/75 °C columns trim
~2–3 toward the measured +6.5/+2.

**2. The airtight P-core survives:** soak trim **−11.5 (IQR −12.5…−10, n=2828, two logs)** at
≤ 2.5 bar, zero-crossing ≈ 3.5 bar. The R7 valley column stands.

**3. Above ~3.5 bar at hot CLT, need is PATH-DEPENDENT — P stops being sufficient.** Same
(CLT≥96, P 3.5–5.5): 06/13 post-restart **+3.6…+4.1**; tonight's slow first warmup **−8.0 at
higher P**; fleet fast-warmup lag window **+7…+11** (Result 1). Supply/bulk viscosity (what the
gallery sensor reads) ≠ bearing-film viscosity (what friction feels); films shear-heat ahead of
the bulk on a slow warmup, so a long-running engine needs less than its P implies. Possible extra
confound: **A/C compressor state is not logged** and may differ across sessions (June midday vs
August 10 PM) — resolve before trusting mid-band cells.

**4. v2 shape (numbers pending current XML + A/C answer):** base keeps CLT columns (light 60/75
trim); corr v2 = R7 soak valley at 2.0 bar, ~−2 at 3.5, then **modest** positives (~half the fleet
lag-window implication: +2 / +5 / +6 at 5.0 / 6.5 / 8.0 on the 1200 row) so the high-P cells no
longer double-count δ(CLT) now that base carries it; PID (−10/+15) finishes both directions per
the conservative-FF principle. Open risk to re-measure after v2: the partial-hot restart
(733-rpm case) — steady need looks small (+4) but the transient path needs a fresh log to clear.
*(A/C confound resolved 2026-08-02: Will — A/C is never active in the idle region. The mid-band
path-dependence stands on bulk-vs-film viscosity alone.)*

**5. Warmup-locus back-calc of the base cold columns (Will's requested derivation).**
`base_v2 = measured air − 13·fan − corr_v2(P at that CLT)`, corr_v2 = [2.0 → −13, 3.5 → −2,
5.0 → +2, 6.5 → +5, 8.0 → +6] (1200-row; row spread ±1 ignored at data noise). Held-target
equilibrium, entry-age > 20 s, pin-censored:

| log | CLT | n | target | P bar | fan | air need | corr_v2 | **base_v2** | old cell | Δ |
|---|---|---|---|---|---|---|---|---|---|---|
| cold | 25–35 | 99 | 1371 | 7.31 | 0 | 61.5 | +5.5 | **56.0** | 58.9 | −2.9 |
| 0613 | 35–42 | 399 | 1320 | 7.12 | 0 | 51.0 | +5.4 | **45.6** | 51.9 | −6.3 |
| cold | 42–52 | 205 | 1286 | 6.94 | 0 | 41.0 | +5.3 | **35.7** | 45.6 | −9.9 |
| cold | 52–62 | 573 | 1255 | 6.88 | 0 | 36.5 | +5.2 | **31.2** | 39.8 | −8.6 |
| cold | 62–70 | 1001 | 1217 | 6.62 | 0 | 34.0 | +5.1 | **28.9** | 34.8 | −5.9 |
| cold | 70–80 | 1151 | 1200 | 6.31 | 0* | 30.0 | +4.6 | **25.4** | 31.0 | −5.6 |
| cold | 93–100 | 733 | 1200 | 5.06 | 1 | 32.5 | +2.1 | **17.4** | 26.5 | −9.1 |
| 0613 | 93–100 | 890 | 1200 | 3.62 | 1 | 43.5 | −1.7 | **32.2** | 26.5 | +5.7 |

\* 70–80 band straddles the fan-engage temperature — fan-mixing noise ±2–3 on that cell.

Readings: the **coldest column back-calcs to ≈ the old value** (56 vs 58.9); the 45–75 columns
back-calc −6 to −10 below old; the **96 column is three-valued by path** — 17.5 (slow warmup),
26.5–27 (soak-anchored: 28.5 − 13 + corr(2.1)), 32.2 (post-restart) — and stays **soak-anchored**
(the state the column serves most; PID −10/+15 absorbs the transient spread both ways).
Per-sample fan subtraction re-run confirms the bands (fan artifact ≤0.5): 56.0 / 35.8 / 31.4 /
28.8 / 25.5 / 17.5.

**⚠ Principle correction (Will, 2026-08-02): program the MEASURED values, not hedged ones.** The
earlier half-trim recommendation is retracted — deliberately-fat FF accumulates negative PID,
which is this car's documented windup-purge-stall mechanism. The idle_stall "halve the
feed-forward" principle is hereby SCOPED to unmeasured/extrapolated cells only; measured cells get
the measurement. See memory `feedback-program-correct-values-not-safe`.

**Proposed `idleActiveAirflow` v2 — measured anchors, old row-shape per column, rows = target:**

| tgt \ CLT | 0† | 15† | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| **1500** | 65 | 62 | 59 | 41.5 | 40 | 38 | 40 | 40 |
| **1375** | 63.5 | 57 | **56** | 40 | 36.5 | 33.5 | 35 | 35 |
| **1200** | 58.5 | 55.5 | 49.5 | **32** | **28.5** | **25.5** | **26.5** | 26.5 |
| **1100** | 52 | 49 | 43 | 25 | 23 | 20 | 21.5 | 21.5 |
| **1000** | 42.5 | 41 | 37 | 18 | 17 | 14.5 | 16.5 | 16.5 |

Bold = measured-anchor rows (locus targets 1371/1286/1243/1200/soak); other rows = old table's
row-to-row deltas applied from the anchor (row shape unmeasured off-locus). **† cols 0/15 are
EXTRAPOLATED** (coldest data 28 °C): ceiling-bounded so that total (base + corr at relief P)
≈ 2.0–2.3× the hot requirement per Heywood — a large cut from the old 87.5/75 guesses; first
genuinely cold morning log revises them. Locus totals reproduce by construction: 61.5 @CLT 28,
41.1 @47, 30.1 @75, 27.1 @soak — all within 0.5 of measured. The 75→96 uptick (+1) and the
top-row mid-CLT dip below the hot cushion are artifacts of soak-anchoring + the deliberate hot
transient cushion (rows 1375/1500 hot cells held); those cells are rare/transient territory.

**Companion corr v2 (pair, do not import one without the other):** 2.00-bar valley column
−6/−10/−13/−6/−4 (1000→1500, R7 anti-sag shaping), then ≈ −2 / +2 / +5 / +6 at 3.5 / 5.0 / 6.5 /
8.0 (±1 across rows).

**6. Tail-chase audit + the 30 → 45 °C cliff (Will's challenge, 2026-08-02 late).**
- **The algebra is clean:** corr_v2 is subtracted exactly once per sample, the composition it plugs
  into is empirically closed (±0.27), and demand comes from logged totals, not table lookups — the
  old table's SHAPE washes out through a converged PID.
- **But the coldest anchor leaks the old table anyway, through an unconverged loop:** in the
  CLT 28–35 window (age 20–45 s) the PID sat at **−9.4 of its −10 floor** — near-railed, integral
  still draining from the old base's fat cold value (~70 open-loop), ignition state unlogged in the
  11-channel export. So air 61.5 → **base_v2(col 30) = 56 is an UPPER BOUND; true value plausibly
  50–53.** The mid/hot anchors are clean — PID free at −4.7 (col 45), crossing 0 by age 65–110 s
  (cols 60/75), settled at soak (col 96). Cols 0/15 inherit the col-30 flag on top of being
  extrapolations. Partial vindication of the "applied the correction twice / chasing our tail"
  concern: not double-subtraction, but old-table inheritance through PID saturation at the cold end.
- **The cliff is not oil, and the 10W-30 KV curve agrees:** across CLT 28 → 50 the oil pressure
  moved 7.31 → 6.94 bar (corr term −0.2) — viscosity was effectively frozen while demand fell ~20.
  The drop is CLT-side: real cold-combustion decay (quench/wall-film/burn-rate, fast wall-warming
  time constant — Heywood §12.7.3 engine warm-up territory) PLUS the PID-settling leakage above.
  The split awaits ignition-gated data.
- **Idle ignition targets are CLT-scheduled, mildly more advanced cold** — CORRECTED 2026-08-02:
  an earlier draft claimed 44–40° cold targets; that was a **scale error** (sbyte decoded at
  1°/count instead of the idle-ignition family's 0.5°/count — see the emu-black-tune skill scaling
  table, updated). Corrected decode of `idleIgnitionTargetTbl` (CLT bins 0/43/96/130):
  **22/21/19.5/18.5° cold row → 18° flat at ≥96**, with `idleIgnitionMax/MinTorqueAngleTbl` =
  30–27° / 13–10° (scale inferred from joint plausibility of all three tables; one-cell EMU display
  check still owed). Consequences: (a) demand numbers embed this schedule — correct for programming
  this car; (b) +2–4° extra advance cold ≈ 0.5–1.5 airflow points — genuinely second-order,
  matching Will's original framing; (c) unchanged and load-bearing: the airflow PID's error signal
  is ignition-angle error → **true equilibrium gating requires angle-at-target**, i.e. the
  full-channel log (Ignition Angle + Idle ignition correction), not the 11-channel export. Next
  step: re-derive the col-30 anchor from tonight's full-channel autosave with angle-at-target gating.

### Armed state and the viscosity correction (2026-08-02) — evaluated, no change warranted

Directive considered: "we now account for oil viscosity → change the armed table accordingly."
**There is no mechanism for 'accordingly':** `idleArmedAirFlow` is firmware-1-D (airflow vs RPM on
`idleRPMBins`, 8 cells — no CLT, no pressure input), and the custom correction provably never
reaches armed (help: active-only; measured: armed output = armed table ± 0.15, fan +13 absent too).
The armed table cannot be made viscosity-aware; it can only be re-leveled, and re-leveling is a
hot/cold trade with asymmetric failures:

- **Sized toward cold** (cover the measured cold deficit, ≈ +13–15 at 1400 rpm / 6.5 bar): armed
  then sits **above hot torque-neutral** → hot returns hang above `target + rampDownOffset` and
  never enter Active — help's explicit warning, and hot is the dominant state. Unacceptable.
- **Sized near hot** (today's 31/34/37/39/40.5×4): cold descents run ~13–15 below cold-neutral →
  the fast plunge. That plunge is caught **at Active handoff by design of the new correction**:
  corr keys on live pressure and actual RPM, so a cold return enters Active at +15…+16 immediately
  (old system did the same job through the base's CLT columns — the catch moves axes, not size).

**Handoff matching is preserved.** The armed low bins (31/34/37 at 1000/1143/1286) match the *hot*
active open-loop (base_hot + fan = 29.5–39.5), which the flatten deliberately keeps — the specs'
"seamless PID handoff" intent still holds. At deep soak the new negative column makes Active run
~5–7 below armed at handoff; the same step existed under the old IAT custom (−7…−11) and is
PID-absorbed. The known armed issue — overrun-exit throttle slam, with the fatter high-RPM revision
proposed in supra-specs (→ 65–72 %) — is orthogonal to viscosity and must be sized from **in-gear
descent logs** (vehicle-coupled torque balance), not idle-soak data. Bound for any future revision:
armed(N) ≤ hot-neutral(N) − margin.

**Measured armed→active entries (2026-08-02, both logs) — the squeeze is two-sided.**
31 armed→active entries analyzed (descent slope over the last 1.6 s of armed in the 1450–2100 band;
undershoot = min RPM within 3 s of entry minus target):

- **06/13 log, cold oil (P>4.5, n=13):** median descent −212 rpm/s but **p10 −1022 rpm/s** — cold
  plunges are 2× faster than warm (p10 −550…−650). Worst event: t=360 (54 s after the hot restart,
  **P 5.66 / CLT 96 — the exact hot-coolant/cold-oil confound**): slope −976, entered 1556,
  **dipped to 733 rpm**. Warm entries same log: undershoot median **+88** (no dip at all).
- **25-min log, soaked (P 2.8–3.7, n=11):** undershoot **median −176, worst −479** (1558 → 1057) —
  even with slow descents (slopes −31…−240). Driver is the **handoff step-down**, not momentum:
  armed hands off 40.5, soaked active runs ~26–30 (old custom −7…−11 + PID −4), a −11…−14 step the
  moment the correction stack engages. This is TODAY'S behavior with the IAT table; the new −13
  column reproduces, not worsens, the same step.
- `armed_air − armed_table = +0.0` in every thermal group — third independent confirmation that
  armed delivers the bare table (no fan, no custom), cold included.

So the 1-D armed curve is squeezed from **both directions**: cold descents want it ~+15 (slow the
plunge), soaked handoffs want it ~−12 (shrink the step), hot wants it where it is. No single
RPM-only curve satisfies that; re-leveling moves the pain between thermal states.

**What the new table already fixes:** the worst measured event (733 rpm catch) enters active at
26.5 + 13 + corr(5.66, row 1375/1500) ≈ **+14–15 → ~54 %** under the new scheme vs ~34.5 % under
the old (CLT-blind base at 96 °C + CAT custom −5) — **+20 more airflow at the catch**, keyed on
live pressure, one PID cycle after entry. The pressure axis sees exactly the state the CLT axis
could not.

**If residual plunge/step remains after the table goes live, the structural lever is the
armed/active BOUNDARY, not the armed level: raise `idleRAMPDownOffset` (350 → ~600–800)** so the
viscosity-aware active state (corr + target ramp at `idleRAMPDownDecayRate`) takes the descent at
1800–2000 rpm instead of 1550 — cold gets the correction through the whole descent, soak spreads
the step over the ramp instead of at one instant. Prereqs before touching it: the
`idleMinMapToActivate = 25` kPa gate (known return-to-idle lockout, see
[`../../notes/return_to_idle_bog.md`](../../notes/return_to_idle_bog.md)), VSS/clutch gates, and
re-log returns for sizing.

**7. The 30 → 45 °C cliff — mechanism, cited (Heywood, `corpus/ice_fundamentals.md`).**
Measured: demand falls ~20 pts across CLT 28 → 50 with oil pressure frozen (7.31 → 6.94 bar).
After deducting the PID-settling inflation at the cold edge (§6), the real drop is carried by
three mechanisms that all ride **water-jacketed surface temperatures** — which is why the term
lands on the CLT axis:

- **Mixture preparation (dominant).** Port-injected spray mostly impinges: droplets must be
  "close to or less than about 20 µm" to follow the flow, "thus most of the droplets… impinge on
  the port and valve surfaces" (corpus:13150–13153). Cold, "only a moderate fraction of the fuel
  injected will vaporize" (corpus:13596–13597); warm, "only a few percent of the injected fuel
  enters the cylinder as a liquid" (corpus:13582–13583). Fuel entering as liquid burns late or
  not that cycle → less IMEP per unit air → extra throttle to hold RPM. The recovery clock is
  the cliff's clock: "the valve and port surface temperatures have a major impact on the liquid
  fuel vaporization" (corpus:13165–13167), the valve head warms "during the first minute or so,"
  and "the coolant (and thus intake port wall) temperature rises more slowly" (corpus:13173–13175)
  — Heywood couples the vaporizing surfaces to the coolant explicitly.
- **Combustion quality at cold walls.** "Heat is transferred from the hot in-cylinder burned
  gases to the combustion chamber… surfaces. This thermal energy is then transferred to the
  coolant" (corpus:13170–13172) — cold walls = larger per-cycle heat loss and wall quenching
  ("laminar flame quenching at a cool wall," corpus:18227), and cooler unburned charge burns
  slower (flame speed rises with flame temperature, corpus:16882; dilution/temperature reduction
  slows S_L, corpus:18038–18039). Slower, less complete, worse-phased burn cold → more air per
  unit torque. Fades as chamber surfaces warm — CLT-coupled, fast.
- **Ring/liner friction rides chamber-surface temperature, not pan oil.** Cold-engine friction is
  ~2× warm (corpus:34958, Fig 13.35), and the liner film sits on surfaces that feed the coolant
  loop (corpus:13170–13172) — so piston-assembly film viscosity recovers on the coolant clock
  while the gallery/pan bulk (what the pressure sensor reads) stays thick. Consistent with demand
  falling while P held ~7 bar.

Warm-up time-scale cross-check: "Engine warm-up can take several minutes, depending on the
initial engine temperature" (corpus:13610–13611) — the port/chamber surface recovery spans
exactly the first-minutes window where the cliff lives, while bulk oil takes 8–12 min (Result 2).

**Active-table decomposition guard (2026-08-02).** Do **not** derive the replacement
`idleActiveAirflow[CLT, idle-target]` table by subtracting the pressure correction evaluated
on one ordinary cold-warmup path. Along that path CLT and pressure co-vary, so it identifies
only their sum:

```
total air = B(CLT, idle target) + C(oil pressure, live RPM) + fan + PID
```

not `B` and `C` separately. That arithmetic would preserve the normal cold-start trajectory,
but a partly-hot restart at the same CLT and lower pressure would see the reduced `B` with little
`C` and can be under-aired. Anchor `B` at a defined hot-oil pressure where `C` is zero/minimum,
then identify the CLT/TB term from holds which vary pressure at the same CLT (cold start,
partly-hot restart, hot restart). Constrain the residual CLT curve smooth; call unsupported
corners a verification gap rather than borrowing the normal-warmup correlation.

**Deep-heat-soak pressure floor (2026-08-02).** `oil data after 25 minutes.csv`
(11,935 samples; stable active-idle mask: state 2, |RPM-target| <= 60, MAP 28..50,
2-s rolling RPM sigma <= 35) establishes the real hot-oil floor below the old 2.38-bar
bin: at target 1200, median pressure = 2.125 bar, p05 = 1.875 bar, and minimum =
1.812 bar (all-log transient minimum 1.688 bar). Therefore 2.38 bar is not a true
zero-correction anchor. Add a 1.75-bar bin (or replace 2.38 with 1.75 if width is
fixed) and set it to 0% for a positive-only correction table. With room for six bins,
preserve the prior 2.38/3.5/5/6.5/8 curve and prepend 1.75 = 0. This clamps the
most-heat-soaked and failed-low input to the intended no-add, fail-high base.

For the adopted **signed** table, use **2.00 bar** rather than 1.75 as the first
axis bin: it is a densely measured, sensor-resolution-aligned hot-oil value. The few
valid stable samples at 1.812 bar simply clamp to the same negative low-pressure
correction, so a below-minimum bin adds no information or protection.

**Positive-only base-anchor correction (2026-08-02).** The same 25-minute log means
the positive-only representation must lower the hot active base; merely keeping the 96 C
base and adding a zero-correction low-pressure bin leaves the removed IAT subtraction
unreplaced. At stable target 1200, median values are `Idle air = 28.5`, `fan = +13`,
`PID = -4`, and old IAT custom correction = `-7` (deepest stable sample: 27, +13,
-4, -9). Preserving the observed open-loop command with new `C(1.75 bar)=0` gives:

```
B_new(1200) = Idle air - fan - PID - C_new = 28.5 - 13 - (-4) - 0 = 19.5 %
```

(18 % at the deepest sample). Thus the 1200 hot base anchor is roughly 19.5 %, not
the old 26.5 % 96-C cell, if the new table is constrained positive-only. The pressure
table must then be re-fit relative to this anchor; do **not** blindly add the 7-point
base reduction to every pre-existing correction cell. At the 06/13 hot-coolant,
partly-warm-oil point (~3.5 bar), the log gives `C_new ≈ 4 %`, agreeing with the
candidate +5 cell. Equivalent representations are: (a) old higher base plus a negative
low-pressure correction, or (b) lower heat-soaked base plus a zero-floor positive table.
This calculation corrects the earlier overly-conservative "keep the 26.5 base" statement.

## Result 9 — first live-correction log validates the design and finds the mid-P band under-corrected (2026-08-04, `oil compensation test with hot restart and varied hot idle targets.csv`)

First log with the **oil-pressure × actual-RPM custom correction actually live** (tune
`first oil press log tune.xml.emub3`, on desktop). 681 s, 16,706 samples @25 Hz: cold-ish start
(CLT 35), drive cycle with repeated idle returns, a near-stall return-to-idle bog, and a deliberate
warm-oil idle-target sweep (900→1500) at the end. 11-channel export: TIME, RPM, MAP, Idle air %,
Idle PID air % correction, **Idle airflow custom corr.** (the correction output, logged directly),
Idle state, Engine oil pressure, CLT, Clutch, Idle target.

**Live tables decoded from the tune (the shipped R7-era config):**
- Actuator `idleDBWTargetMin/Max` = 24/80 → [2.4, 8.0] TPS %. PID limits **−15/+25**. Fan +13,
  `idleDCCorrBehaviour=1` (Add).
- `idleCustomCorrX` = 1C 38 50 68 80 = 28/56/80/104/128 raw **÷16 = 1.75/3.5/5.0/6.5/8.0 bar**
  (Will shipped the **1.75-bar** first bin, R7's alternative). `idleCustomCorrY` = 1000/1100/1200/
  1375/1500 rpm.
- **Custom (sbyte, Add, airflow %), rows 1000→1500:** [−6,7,13,19,25] [−10,6,12,18,25]
  [−14,5,11,17,24] [−6,4,10,16,22] [−4,3,9,15,21].
- Base `idleActiveAirflow` (÷0.5), 96 °C column 1000→1500 = 19/22/27.5/34/37.5 (unflattened,
  keeps CLT columns — post-Result-8 direction).

**Composition re-verified, cleanest yet: `air − custom − PID − base(CLT,tgt) − 13·fan` = 0.14 ± 0.95 %**
(n=4820 equilibrium). Fan step measured at CLT ~72–75 (implied_fan 0.2 below, 12.8 above). **Y-axis
confirmed = ACTUAL rpm** (bog at 296 rpm/target 1200 logged custom −3 = the 1000-row lookup at
2.25 bar, not the 1200-row −8.6).

**Four regimes:**
1. **Cold start (CLT 35→60, ~7 bar, tgt 1500): healthy.** Correction +17, PID +8–10 (headroom).
2. **Warm idle-target sweep (2.0–3.3 bar, tgt 900→1500): healthy.** PID −5 to −10, mildly fat at
   low targets (deep-soak min PID −10.5, floor −15 — ~4.5 % margin). RPM/base shape validated; no
   RPM-axis problem in the correction.
3. **The +25 rail = the return-to-idle bog (structural), NOT a sizing miss.** t≈372–384: armed→active
   return to tgt 1200 dumped to **296 rpm** (near-stall); PID railed +25 for ~12 s catching a
   ~900-rpm undershoot. As RPM collapsed, oil pressure collapsed with it (P∝μN → 0.75–1.2 bar), so
   the correction read the 1.75-bar/1000-rpm corner and **dipped to −6 — a minor aggravant** (~−0.3 %
   TPS). That corner is pinned at −6 by the legitimate deep-soak-900 requirement, so the table can't
   fix the bog without over-fattening soak. Real fix = `idleMinMapToActivate`/rampdown
   ([`../../notes/return_to_idle_bog.md`](../../notes/return_to_idle_bog.md)). **A static (P, rpm)
   table cannot fix a bog because P is a fast function of N and collapses during undershoot — oil
   pressure is not a valid viscosity proxy through an RPM transient.**
4. **THE FINDING — mid-P band badly under-corrected.** t≈256–318: hot coolant (CLT 85→96) but oil
   still genuinely thick (**4.8 bar, visc index ~4.1** — maximal hot-coolant/cold-oil divergence).
   **PID plateaued at +16–17 for ~35 s with RPM 30–50 low** (not lag — <1 s actuator). Base at its
   96 °C column (correct — combustion hot), so the shortfall is pure oil friction = the correction's
   job; it gave only +10. Required-correction (to healthy PID) at 4.8 bar ≈ **+27 to +32** vs shipped
   +10–11. The shipped table put its +24 ceiling at 8 bar; **the demand ceiling (Heywood 2×,
   ~+24–26) is actually reached by ~5 bar at hot CLT.** Confirmed against cold-start: 7.1 bar/1500/
   CLT35 also wanted ~+27 (PID had +10 headroom over correction +17).

**Proposed changes (measured; Will hand-enters):**
- **Base `idleActiveAirflow`: NO CHANGE.** Cold columns had PID headroom, hot columns appropriately
  fat; the mid-P gap is oil not CLT, so raising base would double-count at true cold starts.
- **Custom: raise the 5.0/6.5/8.0-bar columns to a ~+24–26 plateau; leave 1.75 and 3.5 columns.**
  Proposed rows 1000→1500: [−6,7,26,26,26] [−10,6,25,26,26] [−14,5,24,25,25] [−6,4,22,24,24]
  [−4,3,20,22,23]. One idea: **the demand curve saturates at a lower pressure than shipped**, so the
  5-bar column rises to the ceiling.

**Whole-log re-simulation (`newPID = oldPID − Δcorr`):** cold start +9.4→**+4.5**; mid-P +16.6→**+5.1**
(p05 +1.8); 3–4 bar −5.5→−5.5; soak −6.2→−6.2 (untouched). **Zero new ceiling breaches, 8/7648
transient floor touches.** Kept PID ~+5 (not 0) on the positive side as a buffer.

**Caveats:** (a) mid-band is **path-dependent** (Result 8: soak-restart at 4.8 bar can need less than
this cold-start-then-idle) — sized conservatively (PID +5, not 0); confirm with a soak-restart log at
~5 bar. (b) The rail needs the structural return-to-idle fix, not this table. (c) No full key-off/key-on
restart in this file (RPM never returned to 0 after the initial start); the 296-rpm event is a
near-stall-and-recover, not a restart.

## Result 10 — direct oil-pressure-sliced requirement tables, 2-month sweep (2026-08-05)

A different cut of the same requirement surface, requested directly: instead of fixing CLT and
reading airflow vs (RPM, pressure) as Results 5–9 do, **fix oil pressure into 5 bins (2/3/4/5/6
bar, nearest-bin) and build one `idleActiveAirflow`-shaped table per bin** — rows = idle-target RPM
axis (1000/1100/1200/1375/1500), cols = CLT axis (0/15/30/45/60/75/96/105), cell = median total
`Idle air %`. Script: `supra/scripts/oil_pressure_airflow_tables.py` (deterministic, reusable —
takes any list of CSVs, auto-skips logs without `Engine oil pressure`). Outputs under
`supra/notes/oil_pressure_airflow/`: 5 table `.md` + 5 matching sample-count `.md` + a combined
`oil_press_points.csv` (every binned sample, for audit) + `oil_press_log_summary.csv`.

**Scope swept:** every CSV touched in the OneDrive Supra folder in the 2026-06-05 → 08-05 window
(24 files) plus the repo's `Cold oil reference.csv` and the `bp1-3`/`analog_signals` logs already
local — 28 candidates. Per the brief, any log without `Engine oil pressure` in its header was
skipped unread (18 of the 24 OneDrive candidates: most July logs are boost/backpressure/cranking
captures with reduced channel sets that never included the oil-pressure channel). Two files this
note's own Result 7/9 cite as directly relevant — **`oil data after 25 minutes.csv`** (the deep-soak
floor log) and **`oil compensation test with hot restart and varied hot idle targets.csv`** (the
2026-08-04 live-correction log with a deliberate 900→1500 target sweep) — **are no longer present
in the OneDrive Supra folder** (confirmed via recursive search, 2026-08-05). Both would have
directly populated the empty 1000/1100/1375/1500 rows below; ask Will where they went before
re-running.

**Gating (two modes, chosen per-log by available channels):**
- *target* mode (Idle state + Idle target both logged): the canonical stable-idle mask — Idle
  state==2, |RPM−target|<60, TPS<15/PPS<3/driven-axle-speed<2 where those channels exist — plus a
  rolling 2 s **raw-RPM std < 25** stability gate. RPM axis = `Idle target`.
- *proxy* mode (reduced-channel exports with no Idle state/target — only `key_data.csv` in this
  sweep): RPM ∈ [700,1700], MAP ∈ [20,55] kPa (idle-load stand-in for the missing TPS/PPS gates),
  rolling RPM std < 20. RPM axis = actual RPM.
- **Correction versus the earlier `dRPM/dt`-based mask description:** re-deriving it here found
  d(RPM)/dt at this ECU's 25 Hz rate is dominated by single-sample quantization (a 4–8 RPM step
  over 0.04 s already reads ~100–200 RPM/s), so a d/dt threshold of 100 rejects nearly all real
  holds. Calibrated instead against confirmed Idle-state==2 samples in `20260613_1141.csv`: raw-RPM
  rolling std runs 16.4 median / 31.7 p75 there, so a **raw-RPM std** threshold is the correct
  statistic, not RPM's derivative.

**Only 4 of the 8 oil-pressure-bearing logs contributed samples.** `syncloss.csv` is a 0-row
truncated save (8192 B, header only — same signature as the already-known-dead `ahfuck.csv`, which
this sweep also excluded). `cold idle dip again.csv`, `died_hot_return_to_idle_again.csv`, and
`crank_fail_0729.csv` are short transient-only clips (52 s, 18 s, 44 s) capturing exactly the dip /
bog / cranking event they're named for — correctly zero steady-target-hold content, not a masking
bug. Contributors: `20260613_1141.csv` (1,749 samples), `Cold oil reference.csv` (7,826),
`key_data.csv` (2,183, proxy mode), `cold idle dip again 3 all channels.csv` (1, below the
`MIN_CELL_N=15` cell floor). 11,759 total samples, 16 of 200 grid cells populated:

**2 bar**

| RPM \ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| **1500** | | | | | | | | |
| **1375** | | | | | | | | |
| **1200** | | | | | | | 32.0 (71) | |
| **1100** | | | | | | | | |
| **1000** | | | | | | | | |

**3 bar**

| RPM \ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| **1500** | | | | | | | 44.5 (63) | |
| **1375** | | | | | | | 36.5 (92) | |
| **1200** | | | | | | | 43.5 (535) | |
| **1100** | | | | | | | 43.0 (190) | |
| **1000** | | | | | | | 43.0 (31) | |

**4 bar**

| RPM \ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| **1500** | | | | | | | | |
| **1375** | | | | | | | | |
| **1200** | | | | | | | 37.0 (2449) | |
| **1100** | | | | | | | | |
| **1000** | | | | | | | | |

**5 bar**

| RPM \ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| **1500** | | | | | | | 53.0 (17) | |
| **1375** | | | | | | | | |
| **1200** | | | | | | 29.5 (78) | 31.5 (1146) | |
| **1100** | | | | | | | | |
| **1000** | | | | | | | | |

**6 bar**

| RPM \ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| **1500** | | | | | | | | |
| **1375** | | | 56.0 (2135) | 48.5 (1886) | | | | |
| **1200** | | | | 41.0 (265) | 34.5 (1261) | 30.5 (1465) | 29.0 (45) | |
| **1100** | | | | | | | | |
| **1000** | | | | | | | | |

(cells blank below the 15-sample floor; n in parentheses; full grid incl. sub-floor cells in
`oil_press_<N>bar_n.md`)

**Reading the grid — two effects, both already on record in this note, not new physics:**

1. **The empty cells are the diagonal locus (Result 5), not a coverage gap.** Every populated cell
   in this sweep sits on the same track Result 5 mapped: hot idle rides low pressure at any RPM
   (2–5 bar, 1200 row dominates because that's the flat hot idle target), cold-start warmup rides
   high pressure with elevated RPM (the 6-bar table's 1375 row at CLT 30/45). The off-diagonal
   corners (1000/1100/1500 rows away from CLT 96, low-P/high-RPM, high-P/low-RPM) are corners idle
   physically never visits — building them needs the deliberate target sweep this note has asked
   for since Result 1, which is exactly what the now-missing Aug-04 log did.
2. **The CLT-96/1200 column is non-monotonic across P bins (32.0 → 43.5 → 37.0 → 31.5, 2→3→4→5 bar)
   because the pool spans two real confounds, not sampling noise (n runs 71–2449):** (a) **tune
   drift** — `20260613_1141.csv` and `key_data.csv` agree tightly at 3–4 bar (43.5/43.0 both
   dates), but `Cold oil reference.csv` (three weeks later, base table already retuned per Result 8)
   reads lower at the same nominal bin (37.0 at 4 bar); (b) **within-log path-dependence** —
   inside `Cold oil reference.csv` alone the 5-bar cell (31.5) is *lower* than its own 4-bar cell
   (37.0) even though nominally-higher pressure should mean more friction/more air. This is Result
   8 §3's already-documented finding reproducing itself here: on a slow first warmup, bearing-film
   viscosity clears ahead of the bulk-oil pressure the sensor reads, so a long-settled sample at
   "5 bar" can need less than an earlier, less-settled sample nominally at "4 bar." **Do not
   pool cells across tune epochs or treat one log's P-bin ordering as a clean viscosity axis without
   checking the per-log breakdown in `oil_press_points.csv` first.**

The 6-bar table is the cleanest read in the set — CLT 30→45→60→75→96 falling monotonically
(56.0→48.5→41.0→34.5→30.5→29.0) at roughly-fixed high pressure — because it's dominated by one
continuous warmup trace in `Cold oil reference.csv` rather than a pool across dates/tunes. It
reproduces Result 8 §7's CLT-driven warmup shape directly.

## Result 11 — current live tables back-tested and validated, 2026-08-05

Will shipped a new revision of both tables (read from the EMU software screenshot, not a tune
export — transcribed into `supra/scripts/oil_pressure_table_backtest.py`):

**`idleActiveAirflow` (base, rows = idle target 1000→1500, cols = CLT 0/15/30/45/60/75/96/105):**

| rpm \ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| 1500 | 87.5 | 75.0 | 62.0 | 52.0 | 47.5 | 43.0 | 34.5 | 34.5 |
| 1375 | 86.0 | 72.0 | 59.0 | 50.5 | 44.0 | 39.0 | 30.0 | 30.0 |
| 1200 | 81.0 | 67.0 | 52.5 | 42.5 | 36.0 | 31.0 | 24.0 | 24.0 |
| 1100 | 74.5 | 62.0 | 46.0 | 35.5 | 30.5 | 25.5 | 21.0 | 21.0 |
| 1000 | 65.0 | 54.0 | 40.0 | 28.5 | 24.5 | 20.5 | 18.5 | 18.5 |

**`idleCustomCorrection` (rows = RPM 1000→1500, cols = oil pressure 2/3/4/5/6 bar):**

| rpm \ bar | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| 1500 | −3 | 0 | 0 | 3 | 4 |
| 1375 | −6 | 0 | 2 | 10 | 16 |
| 1200 | −6 | 0 | 9 | 26 | 35 |
| 1100 | −5 | 0 | 12 | 31 | 42 |
| 1000 | −6 | 0 | 16 | 39 | 51 |

**Back-test method:** `predicted = bilinear(base, RPM, CLT) + 13·fan + bilinear(corr, RPM, OP)`,
compared sample-by-sample against logged `Idle air %`, gated only on `Idle state==2` (no
target-proximity or nearest-bin snapping — interpolation replaces both, since the ECU itself
interpolates the live tables continuously). First pass nearest-bin-snapped pressure and pooled
across all logs, which produced a spurious "+26 to +41 at 5-6 bar" miss — corrected once pressure
was interpolated and the incomparable-era logs were separated out. Script:
`supra/scripts/oil_pressure_table_backtest.py`; points: `oil_press_airflow/backtest_points.csv`.

**Only one log actually ran this table live** — `oil compensation test with hot restart and varied
hot idle targets.csv` (2026-08-04), fan channel merged in from the same-session `simplified
log.csv` export. Median residual (logged − predicted) **+0.04 %, n=7,648** — the table reproduces
this log almost exactly. Every other log predates this table (old IAT-based correction or an
earlier pressure-correction revision) and reads a large, real, non-noise offset — most starkly
`Cold oil reference.csv` at **median −30.0** (n=11,498, old scheme entirely) — pooling these into
one number is meaningless; per-log separation is required.

**Spatially, within the validated log:** CLT 96 (hot, fan on) residuals run **−5.0 to +0.6** across
every RPM row (1000–1500) — essentially exact. CLT 30–75 (the warmup transient) still shows real
spread, **−15 to +31**, both directions — expected, since the correction table has no CLT axis, so
the entire warmup-transient term still rides on the base table's cold columns, which is the
already-documented path-dependent term (bulk vs. film viscosity, Result 8). **Conclusion: this
table pair is validated for steady hot idle and ready to run; the cold-start columns are the
remaining open item and need a dedicated warmup log to tighten further, not this one.**

## Gaps and open items

- *(Partly resolved by Result 6: the 06/13 warm-up target ramp (`idleRPM` 1500→1200 vs CLT) plus
  VSS-elevated holds populate 1150–1550 actual rpm; only the 1000/1100 rows remain extrapolated.)*
- **The 1200-rpm row is the whole measurable set — by construction, not by gap.** The idle
  controller holds `Idle target` (flat 1200 for CLT ≥ 75), so mined idle logs can *only* ever yield
  the 1200 row; an RPM axis was never going to fall out of constant-target data. This is definitional,
  not a deficiency. **Plan: build the oil-temp table 2-D** (oil temp × idle-target), fill the 1200
  row from here, then populate other idle-target rows by **deliberately commanding those targets
  across oil temps** (a target sweep). Those rows are not copies of the 1200 row — airflow demand
  rises with idle RPM at fixed oil temp (see the `idleActiveAirflow` RPM shape: 1000→1500 spans
  ~31→65 % in the cold CLT-0 column), so each target is its own measurement.
- **No oil temp channel yet.** `oilTempInput = 0`; EMU's failsafe reads 100 °C. Until the sensor
  lands, the oil-pressure viscosity index above is the stand-in.
- **Thermostatic sandwich plate: not resolvable in these logs.** Small non-monotonic bumps in the
  viscosity index appear in 3 of 4 warmups (e.g. 05-31 rises 3.12 → 3.39 across the CLT-96
  crossing, 05-24 rises 3.47 → 3.59), which is the direction a cold-cooler-loop dump would push
  — but each is 1–2 LSB of the 1/16-bar channel and within the RPM/load binning noise. Neither
  confirmed nor refuted. A cleaner test needs the oil-temp sensor, or a steady fixed-RPM hold
  through the opening window.
  **Units check worth doing:** Chase Bays thermostatic plates are specified at **180 °F ≈ 82 °C**,
  not 180 °C. At 82 °C oil the plate opens mid-warmup, roughly where the demand peak sits, which
  is consistent with the hypothesis; a 180 °C element would never open at all.

## Method note

Requirement is read as **total commanded airflow** at samples where RPM held target — not base or
PID alone. **Full composition (verified on `key_data.csv` 2026-08-01, residual −0.5 ± 4.6):**

```
Idle air %  =  idleActiveAirflow(base)  +  idleCustomCorrection  +  airflow PID  +  coolant-fan corr
```

The **coolant-fan correction (+13)** is a constant, always-on term (aggressive fan strategy runs the
fan the whole time so it never disturbs idle) — it is easy to miss and offsets the implied base by
+13. base(96 °C, 1200 rpm) = **26.5**; base + fan open-loop = **39.5**.

Because the airflow PID's error signal is **ignition-angle error, not RPM error**
([airflow_actuator.md](airflow_actuator.md)), a negative PID with RPM below target is normal and is
not evidence of excess air.

**⚠ Clamp-reading rule (corrects an earlier error).** The logged `Idle PID air % correction` is the
PID **output** (P + I). Only the **output** limits are visible in the log — a value pinned bit-exact
at **−6 / −15 / +15 / +25** (the output min/max of that date's config). The **integral** limits
(**−4 / +12**) are internal and **never appear** in the log. So a settled output of −4 is a **free**
value (nowhere near the −6 output clamp), NOT "on the integral floor." Never infer a clamp from a
round output number that happens to equal an integral limit; only a sustained bit-exact pin at an
**output** limit is a clamp, and only those samples are censored.

## Result 12 — `goodrun.csv` (2026-08-16): first post-misfire-fix survey; requirement is BIMODAL and the 3.3–7.3 bar range carries no information

First log after the ignition fix (bad coil connector + marginal plug seating). 14-channel export:
TIME, RPM, MAP, `Idle air %`, `Idle PID air % correction`, `Idle airflow custom corr.`, `Idle state`,
`Engine oil pressure`, CLT, `Injectors PW`, TPS, EGT 1, EGT 2, `Knock voltage peak cyl 6`.
**No `Idle target`, no fan, no ignition angle, no VVT, no charge temp** — see *Channel gap* below.

Structure: a 10 s start attempt at t=33, key-off, then the real run t=591.9 → 1420.8 (13.8 min).
Cold start CLT 35 → warmup → hot idle (t 800–1075) → 3.5-minute drive with boost (t 1075–1290) →
hot idle (t 1293–1421). **Will edited `idleActiveAirflow` live twice during the log** — recoverable
because `bf = air − custom − PID` = base + fan is directly computable per sample:

| window | `bf` at CLT 96 | meaning |
|---|---|---|
| t 592–965 | **40.2–40.5** | native table; base(96,1200) = 27.4 if fan = +13 |
| t 965–987 | 50.1 | +10 live edit |
| t 987–1287 | 55.25 | +15 live edit — **the "too much air" experiment** |
| t 1287–1421 | 40.1–40.5 | reverted, bit-identical to native |

### 12.1 `Idle air %` is a mass-flow meter here — the throttle is choked, so MAP is NOT the air proxy

Baro ≈ 99 kPa (key-off MAP), idle MAP 32–38 kPa → pressure ratio 0.33–0.38, well under the 0.528
critical ratio. **The throttle is solidly choked at every idle sample in this log**, so mass flow
depends only on effective area and ambient upstream state — not on MAP and not on charge temp.
Consequence: `Idle air %` (∝ TPS, `TPS = 2.4 + air/100 × 5.6`, re-verified: air 60 → 5.76 vs logged
5.8; air 30.5 → 4.11 vs logged 4.1) reads **total air mass flow**, and MAP reads **air per cycle**.

Verified on the t=1293 live step-down (−15 base, same thermal state, 2 s apart):

| t | TPS | RPM | MAP | TPS/RPM ×10³ |
|---|---|---|---|---|
| 1291 | 4.5 | 1355 | 37 | 3.32 |
| 1298 | 3.7 | 1097 | 37 | 3.37 |

Air per cycle (MAP) unchanged, RPM tracks mass flow 1:1 within 1.5 %. `A_eff ∝ TPS` is near-linear
in this range (exponent 0.93–1.17 across the two step tests). **⚠ This retires an easy error: do not
read idle air demand off MAP or `Injectors PW` (PW is speed-density-derived from MAP, so it is not an
independent measurement) — at a choked throttle both are nearly invariant while true airflow doubles.**

**Loop authority, measured from the two step tests:** t=970 step +10 air % → +127 rpm (12.7 rpm/%);
t=1293 step −15.5 air % → −252 rpm (16.3 rpm/%). **≈ 13–16 rpm per airflow %** at hot idle.

### 12.2 The hot-oil anchor — the one rock-solid cell in the log

t 1300–1421, `Idle state == 2`, CLT 96, RPM 1150–1250, n = **1707** (2 minutes of hold):

| channel | median | p05 | p95 | min |
|---|---|---|---|---|
| **`Idle air %` (total requirement)** | **30.0** | 29.0 | 34.4 | 28.0 |
| PID | −7.4 | −8.9 | −3.3 | −9.5 (floor −15, **free**) |
| custom corr | −3 | −3 | −2 | −3 |
| **oil pressure** | **2.250** | 2.125 | 2.438 | 2.000 |
| RPM | 1197 | 1169 | 1246 | — |
| TPS | 4.0 | 4.0 | 4.3 | — |

PID free, RPM on target, held two minutes: **hot-oil hot-engine requirement at 1200 rpm = 30.0 total
airflow %.** In base-table units (correction ≡ 0 at the anchor, fan +13): **base(96 °C, 1200) = 17.0**
— 10.4 below the 27.4 the table was actually running, which is exactly the −7.4 PID + −3 custom the
loop was subtracting. Independently reproduces R7/R8's −11.5 soak trim.

### 12.3 Anchor pressure: 2.5 bar is ~0.25 bar high, and it costs about 1 airflow %

Measured over that same hold: median **2.25**, p05 2.125, p95 2.44, min 2.00 — the pressure never
settles at 2.5. Consistent with R7's 25-minute deep-soak log (median 2.125, p05 1.875, min 1.81);
this log's tail is only 2 min of post-drive soak, so 2.25 is if anything the *upper* end of soaked.
Practical cost of anchoring the zero at 2.5 instead of 2.25: with the measured within-window slope
(~3 %/bar, §12.4) ≈ **1 airflow %** ≈ 15 rpm — inside PID range, not worth arguing. **But** with a
2/3/4/5/6-bar axis there is no 2.5 bin; "zero at 2.5" is realised as an interpolation between the
2- and 3-bar cells, and §12.4 shows the demand step lands *inside* that interval. Put the measured
zero on the **2-bar cell** and let 3 bar carry the step, rather than trying to place a zero-crossing
in an unsampled gap.

### 12.4 THE FINDING — specific airflow is bimodal; CLT 39→96 and OP 7.3→3.3 bar change nothing

Steady-segment survey (`Idle state == 2`, 3 s rolling RPM σ < 22, |dRPM/dt| < 12 rpm/s, air σ < 3,
MAP < 50, TPS < 8.2, segments ≥ 3 s). Specific airflow = `air % / RPM × 1000` — the torque-demand
proxy, since air % is mass flow and per-cycle demand is flow/rpm:

| segment window | CLT | oil bar | RPM | total air % | PID | **air %/1000 rpm** |
|---|---|---|---|---|---|---|
| t 607 | 39 | 7.25 | 1518 | 84.5 | +7.4 | **55.7** |
| t 655 | 48 | 7.06 | 1481 | 78.0 | −0.2 | **52.7** |
| t 667 | 51 | 6.94 | 1430 | 75.0 | −1.2 | **52.4** |
| t 676 | 54 | 6.81 | 1341 | 67.0 | −4.4 | **50.0** |
| t 698 | 60 | 6.81 | 1405 | 69.0 | −1.4 | **49.1** |
| t 718 | 65 | 6.62 | 1372 | 69.5 | +2.5 | **50.7** |
| t 751 | 69 | 6.56 | 1386 | 74.0 | −1.9 | **53.4** |
| t 866 | 96 | 4.50 | 1199 | 60.0 | +10.5 | **50.0** |
| t 887 | 96 | 4.25 | 1194 | 60.0 | +11.4 | **50.3** |
| t 934 | 96 | 4.06 | 1221 | 63.5 | +8.5 | **52.0** |
| t 1053 | 96 | 3.31 | 1198 | 57.0 | +0.1 | **47.6** |
| — **drive, t 1075–1290** — | | | | | | |
| t 1296 | 96 | 2.12 | 1100 | 26.5 | −10.5 | **24.1** |
| t 1307 | 96 | 2.44 | 1239 | 30.0 | −8.0 | **24.2** |
| t 1369 | 96 | 2.25 | 1186 | 30.0 | −7.4 | **25.3** |
| t 1408 | 96 | 2.31 | 1266 | 30.0 | −7.8 | **23.7** |

**Specific airflow is flat at 48–56 across CLT 39 → 96 and oil pressure 7.25 → 3.31 bar, then halves
to 24–25 after the drive.** Two clusters, nothing in between. Ratio **2.0×** — precisely the
Heywood cold/hot friction ceiling (Result 4), so the pre-drive state sits *at* the ceiling and the
post-drive state at the floor, with the entire transition unsampled.

Three consequences, in order of importance:

1. **Above ~3.3 bar the pressure axis is informationless in this log.** 7.25 bar and 3.31 bar demand
   the same specific airflow. A correction table indexed on pressure must therefore be **flat
   (saturated) from ~3.3 bar up** — it must not keep climbing to 6–8 bar. This kills the shipped
   R11 shape (1200 row: 2 bar −6, 3 bar 0, 4 bar +9, 5 bar +26, 6 bar +35), which does the opposite:
   it is near-zero exactly where the demand is already at its ceiling, and maximal where demand is
   flat. It confirms R9 §4 ("the ceiling is reached by ~5 bar") and pushes the saturation point
   further down, to ~3.3 bar.
2. **The step is confounded with the drive.** Every ≥3.3 bar hot-CLT sample is pre-drive and every
   ≤2.5 bar sample is post-drive. Oil pressure is the only *logged* channel separating the two
   clusters — but so is "before vs after a 3.5-minute boosted drive." Candidates this log cannot
   separate: bearing-film vs bulk viscosity (R8 §3, already on record), VVT phaser position
   (oil-pressure-actuated, unlogged), idle ignition angle (the airflow PID's actual error signal,
   unlogged), alternator load recovering after the cold-start charge, and throttle-body/TPS thermal
   state ([throttle_body_thermal_growth.md](throttle_body_thermal_growth.md)). **Do not present the
   pressure attribution as settled on this log alone.**
3. **The CLT axis did nothing here either.** CLT 39 → 96 at roughly fixed pressure moved specific
   airflow 55.7 → 50 (−10 %). Contrast R8 §7, where CLT 28 → 50 dropped demand ~20 points. This log
   starts at CLT 35 with the oil already at 7.25 bar and never goes colder, so it does not contradict
   R8's cliff — it just does not reach it. The 0/15/30 base columns stay unmeasured.

### 12.5 The failed re-entry, quantified

The +15 base experiment (t 987–1293) reproduced the reported symptom exactly. At t 1282–1292 the
controller **was** in Active (`Idle state == 2`) and still could not come down: PID pinned bit-exact
at its **−15 output floor**, custom −1, total air 39–41.5, RPM parked at **1350–1428** against a
1200 target for ~10 s. Removing the 15 points of base at t=1293 dropped RPM to 1100 within one
second. So the failure is not a mode problem — it is arithmetic: base+fan 55.25 against a 30.0
requirement is a +25 error, the PID's negative authority is 15, and the residual +10 buys
**~150 rpm at 13–16 rpm/%**, which is exactly the observed hang. Armed airflow read a flat **40.5**
at every RPM from 1500 to 4800 (`idleArmedAirFlow` top bins), unchanged by the base edits — fourth
independent confirmation that armed delivers its own table only.

### 12.6 Deliverable A — base (`idleActiveAirflow`) at the hot-oil anchor, blank where unmeasured

Cells are **total commanded airflow %** at the anchor; the base-table entry is that minus the fan
term (+13 when the fan is on, which it is at CLT 96 — inferred, not logged in this export).
**Structural point: at cold CLT the oil is never near 2.25 bar, so the cold columns of a hot-oil-
anchored base table are unmeasurable by construction, not by sampling luck.** They can only ever be
derived by subtracting a trusted correction, which is the R8 §"decomposition guard" trap.

Total-air requirement (blank = no data in this log):

| rpm \ CLT | 0 | 15 | 30 | 45 | 60 | 75 | 96 | 105 |
|---|---|---|---|---|---|---|---|---|
| **1500** | | | | | | | | |
| **1375** | | | | | | | ≤ 39.5 † | ≤ 39.5 † |
| **1200** | | | | | | | **30.0** | **30.0** |
| **1100** | | | | | | | ≈ 27 ‡ | ≈ 27 ‡ |
| **1000** | | | | | | | | |

Same cells as base-table entries (total − 13 fan − 0 correction):

| rpm \ CLT | … | 96 | 105 |
|---|---|---|---|
| **1375** | | ≤ 26.5 † | ≤ 26.5 † |
| **1200** | | **17.0** | **17.0** |
| **1100** | | ≈ 14 ‡ | ≈ 14 ‡ |

† **upper bound only** — the 1362-rpm hold (t 1286, air 39.5) ran with the airflow PID railed at −15,
so the loop could not demonstrate a lower value; and with RPM 160 above target the idle *ignition*
PID was retarding to pull it down, which inflates the air needed. True 1375 value is below this.
‡ **weak** — the 1100-rpm hold (t 1296, air 26.5) is the 5 s undershoot trough after the base
step-down, not a converged equilibrium, and with RPM below target the ignition PID was advancing
(adding torque), which deflates the air needed. Treat as a lower bound.

**Only the 1200/96 cell is a measurement.** Filling 1000 and 1500 needs the deliberate hot-oil idle
target sweep this note has asked for since Result 1 (and which the missing 2026-08-04 log had).

### 12.7 Deliverable B — oil-pressure correction, RPM-independent, zero at the anchor

*(Bins and anchor **superseded by §12.12** — Will moved the anchor to 2.0 bar and the 2/3/4/5/6 axis is not binding. The measurements below stand; only the axis placement changed.)*

Measured at CLT 96, RPM 1150–1250 only (correction = total air − 30.0):

| oil bar | n | total air % | PID | **correction** | basis |
|---|---|---|---|---|---|
| 2.0–2.5 | 1707 | 30.0 | −7.4 free | **0** | anchor, converged |
| 2.5–3.3 | ~0 | — | — | **unsampled** | the step lives here |
| 3.3 | 315 | 57.0 | +0.2 | **+27** | converged (PID ≈ 0) |
| 3.4–3.8 | 308 | 58.5 | +4.9 | **≥ +28** | RPM under target |
| 3.8–4.2 | 753 | 61.5 | +8.9 | **≥ +31** | RPM under target |
| 4.2–4.6 | 826 | 60.0 | +10.8 | **≥ +30** | RPM under target |
| 4.6–5.0 | 367 | 61.0 | +10.2 | **≥ +31** | RPM under target |
| 5–7.3 | — | — | — | **+30 (held)** | §12.4: specific airflow flat to 7.25 bar |

Proposed table, **flat across every RPM row** (the RPM gradient is what was bouncing the engine —
see §12.8), on the shipped 2/3/4/5/6-bar axis:

| oil bar | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| **correction, all rows** | **0** | **+14** | **+30** | **+30** | **+30** |

- 2 bar = 0 by anchor definition (measured).
- 4/5/6 bar = +30, the measured ceiling; held flat to 6 because 7.25 bar demanded no more than
  3.3 bar did. Every ≥3.4 bar cell is a **lower** bound (PID positive, RPM under target), so +30 is
  conservative in the correct direction.
- **3 bar = +14 is the one interpolated cell and it is the weakest number here.** Nothing in this
  log holds idle between 2.5 and 3.3 bar. It is the midpoint of a step whose shape is unknown; the
  true curve could be a knee at 2.7 (→ 3 bar ≈ +25) or at 3.2 (→ 3 bar ≈ +3). **This is the single
  highest-value gap to log next** — a deliberate hot-CLT idle hold while the pressure drifts through
  2.5 → 3.5 bar, which is the first 3–4 minutes of any post-drive soak.

### 12.8 Why flat rows, confirmed in the data

The shipped R11 correction has a steep RPM gradient (5 bar: +39 at 1000 rpm vs +3 at 1500). The
Y axis is **actual** rpm (R9), so a sag *raises* the correction and a rise *lowers* it — positive
feedback through a ~750 ms-lagged actuator. Visible directly in this log's pre-drive hot window
(t 840–1000): RPM limit-cycles 1055 ↔ 1300 with a 20–40 s period while `Idle airflow custom corr.`
swings **+4 ↔ +20 in phase with the sag**, adding air exactly when RPM had already started
recovering. That is the reported "it up-throttles whenever it settles down." **Flat rows remove the
mechanism entirely** and cost little: §12.4 shows the specific requirement is set by thermal state,
not by which idle target is commanded, over the 1100–1500 band this table sees.

### 12.9 Architecture consequence — this is R7's fork B, and its one real risk

Anchoring base at the hot-oil state (17.0 at 96/1200) with a positive-only correction is R7 **fork B**:
it trims base to recenter a negative trim, which the open-loop-guarantee rule normally forbids. The
active-state-only nature of the custom correction (R6, help + measurement) means every non-Active
state — recovery (`Idle state == 4`), afterstart, PID-reset moments — then runs on the thinner base.
At hot soak that is correct by construction (requirement *is* 30). The exposure is
**`oilPressureFailSafe = 0`**: a failed sensor substitutes 0 bar → clamps to the 2-bar column →
correction 0 → a cold start runs on base + fan alone, ~30 points short of the measured 84.5 cold
requirement. Survivable only because the base keeps its CLT columns; do not flatten them (R8 §1
already retired that plan). Fork A (fat base, signed correction) avoids this at the cost of the
negative low-pressure column. Will's directive here is fork B; recorded, not re-litigated.

### 12.10 Channel gap — what the next log must carry

*(**Superseded by §12.11 + §12.13** — VVT and idle ignition angle ruled out as drivers; revised channel list and the four-test protocol live in §12.13.)*

This log cannot separate the §12.4 confound because the decisive channels are absent. In priority
order: **`Ignition Angle` + `Idle ignition correction`** (the airflow PID's error signal *is*
ignition-angle error — without it "equilibrium" cannot be gated, only guessed at from RPM);
**`Idle target`** (removes all target inference); **`VVT CAM1 angle` + target** (oil-pressure-actuated,
the leading unexamined candidate for a step that tracks a drive); **`Charge temp`**; **fan state**;
**`Battery voltage`** (alternator load at idle is worth real torque and decays exactly on the
warmup clock). Combustion health in this log is clean — knock voltage cyl 6 median 0.275–0.333 V
with σ 0.022–0.028 throughout, no drift, consistent with the ignition fix.

### 12.11 Confound list resolved (Will, 2026-08-16) — and the alternator number is NOT minor

Rulings on §12.4's candidate list, and what survives:

- **VVT — ruled out by Will. Not relevant here.** Removed from the candidate list; do not re-raise it.
- **Idle ignition angle — ruled out.** CLT-scheduled and flat at ≥96 °C (R8 §6: 18° flat above 96),
  so it changes minimally between two hot-CLT windows. It remains the airflow PID's *error signal*,
  which is a separate reason to log it (§12.12), but it is not a candidate driver of the 2× step.
- **Throttle-body thermal state — deliberately folded into the pressure correction.** Will's call, and
  the reasoning is sound: TB metal temperature has a long lag against a drive/soak, so it decays on
  roughly the same clock as bulk oil temperature, and a P-indexed table absorbs it without a second
  axis. The old IAT-indexed `idleCustomCorrection` was compensating the same physical thing on a
  worse-correlated proxy. **Consequence to keep in view:** the P table is therefore an empirical
  *warm-up-state* correction, not a pure viscosity term. It is valid only while those clocks stay
  coupled; it will mis-predict wherever they decouple (jump-start, very short trip, a large electrical
  or accessory load applied at steady idle).
- **Alternator — quantified below. ⚠ The current-swing estimate here is CORRECTED DOWN by §12.14 (voltage log): the differential is ~2.5–5 airflow %, not ~12. The budget arithmetic stands.
  Original text: it is a large fraction of the idle budget, not a rounding error,
  and it folds into the same P axis for the same reason.** Will's disposition (let the PID carry it)
  is still workable because it is slow-varying and the PID has −15/+25, but the magnitude below
  should be on record.

**Idle power budget, hot soaked, from this log's own fuel numbers** (supra-specs: ID1050X × 6,
E60 stoich 11.0, LHV 28.5 MJ/kg; `Injectors PW` 1.516 ms at 1200 rpm; dead time ≈ 0.8 ms at 14 V):

```
effective PW      1.516 − 0.8      = 0.716 ms
injections/s/inj  1200/120         = 10
effective duty    0.716e-3 × 10    = 0.716 %
fuel flow         1050 cc/min × 0.00716 × 6 inj × 0.771 g/cc   = 0.579 g/s
  → implied air   0.579 × 11.0     = 6.37 g/s   (speed-density cross-check: MAP 35 kPa,
                                      1200 rpm, VE ≈ 0.55 → 6.3 g/s ✓ independent agreement)
fuel power        0.579 g/s × 28.5 kJ/g                        = 16.5 kW
gross IMEP        η_i,gross ≈ 0.30 → 165 kPa → P_gross          =  4.95 kW
pumping           PMEP ≈ (105 − 35) = 70 kPa                    = −2.10 kW
NET CRANK BUDGET at hot idle (friction + accessories, output 0) ≈ **2.85 kW ≈ 3.8 hp**
```

Against that budget, at 14 V and an alternator efficiency of ~50 % (a 150 A unit at ~3000 alternator
rpm off a 1200 rpm crank is well below its efficiency peak):

| electrical draw | mechanical | share of the 2.85 kW hot-idle budget | airflow-% equivalent |
|---|---|---|---|
| 10 A | 0.28 kW | **10 %** | **≈ 3** |
| 40 A | 1.12 kW | 39 % | ≈ 12 |
| 80 A | 2.24 kW | 79 % | ≈ 24 |

**80 A cannot be the steady hot-idle draw** — it would consume nearly the whole budget and leave
nothing for rubbing friction (which at 1200 rpm on a 3.0 L is 50–70 kPa FMEP ≈ 1.5–2.1 kW). Working
backwards from the budget, hot soaked idle supports roughly **30–45 A**. 80 A is the *cold-start*
case: fans on, plus battery recharge after cranking — i.e. **exactly the pre-drive window**.

So the alternator swing between the two windows is plausibly **40 A ≈ 1.1 kW ≈ 12 airflow %**, which
is **~35–40 % of the 2× step** the correction table is being sized on. Not minor. It decays on the
battery-recharge clock, which overlaps the warm-up clock, so like TB thermal it will be absorbed into
the P table rather than seen by the PID. **Rule of thumb worth remembering: at this idle point,
10 A ≈ 3 airflow % ≈ 45 rpm.** Adding a 40 A load at steady idle (fans cycling, a winch, headlights
plus blower) is a ~12-airflow-% disturbance the FF table has no axis for.

### 12.12 Anchor moved to 2.0 bar; axis bins are free (Will, 2026-08-16)

Will's decision: **anchor the base table at 2.0 bar and make the correction positive-only from there.**
The 2/3/4/5/6 axis quoted in R11 came from an older tune screenshot and is not binding — bins are
free. Re-issued on bins placed where the curve actually moves (measured flat 2.0–2.6, the knee
somewhere in 2.6–3.4, plateau above 3.4):

| oil bar | 2.0 | 2.6 | 3.0 | 3.4 | 5.0 |
|---|---|---|---|---|---|
| **correction, all rows flat** | **0** | **0** | **+12** | **+28** | **+30** |

- **2.0 = 0** — anchor. Soaked idle measures 2.25 median / 2.00 min here, 2.125 / 1.81 in R7's
  25-minute log, so 2.0 is at the physical floor and anything below clamps to zero correction. Correct
  by construction, and the right failsafe value (`oilPressureFailSafe = 0` → this column).
- **2.6 = 0** — measured. Demand is flat at 30.0 across the whole 2.0–2.63 band (n = 1707).
- **3.0 = +12** — the one **unmeasured** cell, interpolated across the knee and deliberately hedged
  low. Nothing holds idle between 2.63 and 3.31 bar in any log to date. Hedging is sanctioned here by
  the standing rule as scoped in R8 §5 (program measured values; the halve-the-FF principle applies to
  unmeasured cells only), and the direction is chosen from the observed failure mode: too much air
  hangs the engine out of the idle region (§12.5), too little is caught by PID +25.
- **3.4 = +28, 5.0 = +30** — measured (+27 converged at 3.31; ≥+28…+31 at 3.4–5.0 with PID positive
  and RPM under target, so both are lower bounds).
- **Top bin at 5.0, not 6 or 8, is deliberate** — EMU clamps to the edge cell, so 5.0 = +30 extends
  the plateau to relief pressure automatically. §12.4 supports it: 7.25 bar demanded no more specific
  airflow than 3.31 bar did. Spending bins at 6/8 would buy resolution in a region with no gradient.

Base table is unchanged by the anchor move: correction is 0 at both 2.0 and 2.25 bar, so
**base(96 °C, 1200 rpm) = 30.0 total − 13 fan = 17.0** still stands.

### 12.13 The test plan — what the next logs must capture, and how to drive them

**Channels (revised priority after §12.11's rulings).** Drop VVT. Required set:

| channel | why |
|---|---|
| `Idle target` | removes all target inference; every "at target" gate depends on it |
| `Ignition Angle` + `Idle ignition correction` | the airflow PID's error signal **is** ignition-angle error — the only way to gate true equilibrium instead of guessing from RPM |
| `Engine oil pressure`, `Idle air %`, `Idle PID air % correction`, `Idle airflow custom corr.`, `Idle state`, RPM, CLT, MAP, TPS | the core set already in `goodrun.csv` — keep all of it |
| coolant-fan output state | makes the +13 explicit instead of inferred; also flags the fan-cycling disturbance |
| `Battery voltage` | **now logged and resolved — see §12.14. It is NOT a load proxy** (alternator stays in regulation at all speeds); it reads bay/alternator **thermal** state, which makes it a usable stand-in for the throttle-body term |
| `Charge temp` | cheap, and closes out the density question for good |
| `Lambda`, `Lambda is valid` | confirms the fuel side is not moving between windows |

**Before logging any of these: flatten the correction table's RPM rows.** The shipped RPM gradient
drives the 20–40 s limit cycle documented in §12.8; while it is live, every "steady" idle hold is a
limit cycle and every median is a cycle average rather than an equilibrium.

**Test 1 — the knee (highest value; this is the only weak cell in the deliverable).**
The question: after CLT pins at 96, does demand collapse smoothly as oil pressure drifts 4.6 → 2.2,
or does it hold high until something else changes? In `goodrun.csv` the pre-drive window walked
4.6 → 3.31 bar and demand only fell 60 → 57; the drive intervened before the answer arrived.
- Cold start, **do not drive**.
- Idle in place, pedal untouched, until CLT reaches 96 — then keep idling **15–20 more minutes**.
- Target to hit: oil pressure at held 1200 idle drifting from ~4.5 bar down to **≤ 2.3 bar** without
  the engine ever leaving the idle region.
- Success criterion: continuous coverage of the **2.6–3.4 bar band with ≥ 60 s of held idle per
  0.2 bar**. That single trace either fills the +12 cell with a measurement or proves oil pressure
  is not the variable.
- Watch out for: coolant-fan cycling (log the state), and the alternator settling — battery voltage
  should be flat before the tail of the run is trusted.

**Test 2 — the RPM rows (fills 1000 and 1500 in the base table).**
The base table's RPM axis has never been measured; 1000/1100/1375/1500 are all empty or bounded.
- Precondition: **fully soaked** — drive until held-1200 idle pressure is **≤ 2.3 bar**, then park.
- Sweep `idleRPM` target: **900 → 1000 → 1100 → 1200 → 1375 → 1500**, and back down.
- **≥ 60 s at each target** (the limit cycle is 20–40 s, so a shorter hold cannot produce a converged
  median), pedal untouched, in neutral, clutch out.
- Success criterion: at each target, RPM within ±30 of target with the airflow PID off both rails and
  its 10 s trend flat.
- This is the sweep Result 1 has asked for since May; the 2026-08-04 log that had it is missing from
  OneDrive.

**Test 3 — decoupling / path-dependence (validates that P alone is sufficient).**
- Drive to full heat, shut down, **sit 30–60 minutes**, restart.
- Target state to hit: **CLT 70–85 with oil pressure 3.3–4.2 bar** — a combination the normal warm-up
  path never produces (warm-up has that pressure only at cold CLT).
- Hold idle 5 minutes, untouched.
- What it decides: if demand at that (CLT, P) matches the correction table's prediction, P is
  sufficient and §12.11's folded-in terms are safely coupled. If it does not, the P axis is carrying a
  drive-history variable it cannot see, and the table needs a second input.

**Test 4 — the cold base columns (only after 1–3 land).**
A genuinely cold start (CLT ≤ 15 °C, i.e. a winter morning) with the validated correction live. Per
§12.6 the cold columns can only ever be recovered by subtracting a trusted correction, so this test is
worthless until Test 1 has fixed the knee. Idle in place ≥ 10 minutes before driving.

**One protocol note that applies to all four:** log continuously from key-on and do not touch the
pedal during any hold. Any pedal input inside a hold window puts the controller through
armed/recovery and invalidates the segment — the extractor in
`supra/scripts/idle_steady_segments.py` will drop it, but a 60 s hold interrupted at 40 s yields
nothing rather than a short answer.

**⚠ Stale reference spotted while checking specs (2026-08-16):** the `supra-specs` skill lists the
DBW/airflow calibration as `2.0 % TPS = 0 % airflow, 6.4 % = 100 %` (4.4 span). The live tune and
every log in this note give **2.4 / 8.0 (5.6 span)** — re-verified on `goodrun.csv` (air 60 → TPS
5.76 predicted vs 5.8 logged; the 4.4-span form predicts 4.64, which is wrong by 1.2 % TPS). The
skill also quotes steady idle airflow demand as 44–46 %, which is a pre-oil-correction-era figure.
Use `airflow_actuator.md` and this note, not the skill, for actuator scaling.

### 12.14 Battery voltage does NOT measure alternator load — and it shrinks the alternator term (2026-08-16, `goodrunwithvoltage.csv`)

`goodrunwithvoltage.csv` is the **same run** as `goodrun.csv` re-exported with `Battery voltage`
added (identical TIME base, identical channel values), so the two hot-idle windows are directly
comparable with no session confound.

**Answer: no, load is not inferable from voltage here. Three independent proofs:**

1. **Voltage is independent of engine speed.** Matched adjacent-in-time windows, so thermal drift is
   controlled:

   | window | idle | driving |
   |---|---|---|
   | t 995–1080 | 1187 rpm → **13.649 V** | 2091 rpm → **13.622 V** |
   | t 1080–1230 | 1271 rpm → **13.622 V** | 2710 rpm → **13.622 V** |

   Tripling alternator speed produces **zero** voltage rise. A current-limited (saturated) alternator
   would jump. It is in **voltage regulation with headroom at idle**, so terminal voltage is set by the
   regulator, not by the load.
2. **Voltage is at its maximum in the first minute** — 14.000 V at t 596–605, the highest reading of
   the entire run — which is exactly when battery-recharge load should peak. It only declines from
   there. The reverse of what a recharge-loaded alternator does.
3. **No step at fan engagement.** CLT crosses 66 → 86 across t 735–790 with the coolant fan coming in;
   voltage walks smoothly 13.92 → 13.81 with no discontinuity. A ~25–30 A step is invisible, i.e. the
   regulated source impedance is low enough to hide it.

**What voltage actually tracks: bay/alternator thermal soak.** Whole-run decline **14.00 → 13.40 V
(0.60 V, monotone)**, and **0.352 V of that falls after CLT has already pinned at 96 °C** (t=798) —
so it is not coolant. It is the classic negative temperature coefficient of the internal regulator
(−7 to −20 mV/°C ⇒ 0.60 V ≈ 30–85 °C of regulator heating), on a clock much longer than coolant.
**Relabel the channel: `Battery voltage` is a bay-thermal-state proxy in this log, not a load channel** —
which makes it a *useful* stand-in for exactly the throttle-body-thermal term folded into the pressure
axis in §12.11, just not for the alternator.

**Bounding the alternator term anyway — it is smaller than §12.11 assumed.** *(⚠ The ohmic arithmetic in this paragraph is WITHDRAWN by §12.15 — the battery is AGM and charge acceptance is polarization-limited, not resistance-limited. The conclusion survives and the term shrinks further, to 1–3 airflow %.)* Voltage cannot measure
current, but it does bound the *recharge* component, because charge current is driven by
`V_alt − V_battery_EMF` and **both halves moved to shrink it**: the setpoint fell 0.60 V while the
battery's EMF rose as it charged (key-on rest **12.297 V** ≈ 60–70 % SoC).

```
early  13.95 V alt − ~12.45 V EMF = ~1.50 V  ÷ 0.05–0.10 Ω charge acceptance = 15–30 A
late   13.40 V alt − ~12.75 V EMF = ~0.65 V  ÷ same                          =  7–13 A
Δ recharge load ≈ 8–17 A  →  at 10 A ≈ 3 airflow % (§12.11)  →  **2.5–5 airflow %**
```

And the *fixed* loads are common to both windows: **the coolant fan is on in both** (CLT 96 in each),
so the single largest draw does not differ. Only the recharge term does.

**⚠ Correction to §12.11.** That section put the alternator swing at ~40 A ≈ 12 airflow % ≈ 35–40 % of
the 2× step, on the assumption of an 80 A → 40 A change. **The voltage trace does not support it** —
the alternator was never pulled down, at any speed, at any point in the run. Revised: the alternator /
recharge differential is worth **~2.5–5 airflow %, i.e. 8–17 % of the 30-point step.** Still not zero,
still absorbed into the P table on the same clock, but a minor term — which is where Will placed it.
The §12.11 budget arithmetic itself stands (net crank budget 2.85 kW, 10 A ≈ 3 airflow % ≈ 45 rpm);
only the assumed current swing was wrong.

**So the §12.4 step is still unexplained, and the candidate list is now short.** VVT out (Will),
idle ignition angle out (flat above 96 °C), alternator bounded at ≤5 of 30 points. What remains:
bulk-vs-film oil viscosity (R8 §3) and throttle-body/bay thermal state — and the latter now has a
logged proxy in `Battery voltage`, which drops 0.325 V between the two hot windows (13.730 →
13.405, matched gating) with the same flat-then-step shape as oil pressure. Neither separates them;
**Test 1 in §12.13 (idle through the whole warm-up without driving) remains the experiment that does.**

**Side observation, not a tuning matter** *(sharpened in §12.15 — it is an AGM, and Will tops it periodically with an AGM charger)*: a regulated 13.4–14.0 V is low for a lead-acid battery,
which wants 14.2–14.4 V to reach full charge. At the 13.40 V this alternator settles to when hot, the
battery will hold a partial charge indefinitely. Worth knowing; it does not affect any table here.

### 12.15 Battery is AGM (Will, 2026-08-16) — retires §12.14's ohmic estimate and closes the alternator candidate

**⚠ The ohmic charge-current arithmetic in §12.14 is withdrawn.** It was wrong for any lead-acid and
badly wrong for AGM: charge acceptance is **polarization-limited, not resistance-limited**. An AGM's
internal resistance is very low — this one's crank sag measures it directly (rest **12.297 V** →
**10.270 V** during the t=33 crank, ΔV **2.03 V**; at a 2JZ starter's ~250–350 A that is
**~6–8 mΩ** total including cables and terminals) — so an ohmic model of charging predicts ~280 A,
which is nonsense. The battery's surface/polarization voltage rises within seconds of charge onset
and is what actually sets the current. Do not convert a charging-voltage differential to amps this way
again.

**The valid bound is from the alternator side, and it is unchanged and chemistry-independent:** output
never sags and is completely insensitive to speed (1187 → 2710 rpm, zero change, §12.14), so total
draw stayed comfortably inside the alternator's idle capability throughout. No channel in this log
resolves accessories vs recharge.

**Two new arguments that close the candidate anyway:**

1. **The voltage decay is linear, not exponential.** Sampled across the whole run: 13.97 / 13.92 /
   13.89 / 13.81 / 13.78 / 13.70 / 13.62 / 13.57 / 13.49 / 13.41 V at minutes 0.07 / 1.0 / 2.0 / 3.0 /
   3.5 / 5.1 / 7.8 / 9.8 / 11.8 / 13.8 — a near-constant **−0.043 V/min for 14 minutes with no knee.**
   A recharge signature is a fast early taper that flattens. A large-thermal-mass soak driving a
   temperature-compensated regulator is a long ramp that still looks linear at 14 minutes. This is the
   latter.
2. **Both comparison windows sit past the bulk-charge phase.** Pre-drive hot idle is minutes
   **3.8–8.1**, post-drive is **11.8–13.8**. Whatever recharge current flowed, the bulk of it went in
   during minutes 0–3 — the *warm-up* window, not either window being compared. And at only 13.9 V
   into an AGM resting at 12.30 V, the accepted current is modest to begin with and tapers within the
   first minutes.

**Revised alternator term: ~1–3 airflow %, under 10 % of the 30-point step.** Down again from
§12.14's 2.5–5, and down from §12.11's 12. Treat the alternator as **closed** — Will's original
read was right, and the remaining §12.4 candidates are **bulk-vs-film oil viscosity** and
**throttle-body / bay thermal state**, nothing else.

**The charging-system observation gets sharper with AGM, and Will already compensates for it.**
Key-on rest **12.30 V** on an AGM is roughly **50 % SoC** (AGM curve: 12.8–13.0 V = 100 %, 12.6 = 75 %,
12.3 = 50 %). AGM absorption wants **14.4–14.8 V**; this alternator peaks at **14.00 V cold and settles
to 13.40 V hot**, which is below even a proper AGM float (13.6–13.8 V). So the car cannot charge its
own battery past a partial state, which is exactly why Will tops it periodically with an AGM-specific
charger — that practice is the compensation, not a workaround. **Relevance to idle tuning: this makes
the recharge load *smaller*, not larger** (a low charge voltage limits accepted current), which is a
third independent reason the alternator cannot be the §12.4 step.

## Result 13 — the pressure axis is DEAD at hot idle; RPM is the whole signal (2026-08-16, `bighotidle.csv`)

**Falsification first (warm-restart test, live in the car).** Will ran §12.12's proposed correction
(0/0/+24/+30/+30) on a **warm restart** at CLT 96 / ~4.5 bar. The car was **over-aired and would not
enter the idle region**; he halved the table, then zeroed it entirely. Compare:

| | CLT | oil bar | requirement |
|---|---|---|---|
| `goodrun`, **cold** start, min 4–8 | 96 | 4.1–4.6 | **60** |
| warm restart | 96 | ~4.5 | **≈33** |

**Same coolant, same oil pressure, ~2× different requirement.** Oil pressure is not the variable, and
the entire R5→R12 pressure-axis architecture is retired as a *correction axis*. It only ever worked
because oil pressure and engine-metal heat both decay from a cold start on similar clocks; a warm
restart decouples them and the table fails immediately and in the dangerous direction (over-air →
no idle re-entry). The μ^1.66 exponent in §12.16 predicted exactly this.

**Will's summary, and it matches the data: the adder "only seems to matter in the few minutes after
cold start during a drive."**

### 13.1 Requirement vs idle target, hot, correction = 0

`bighotidle.csv`, 743 s, CLT 96–98, oil 2.0–3.2 bar, custom correction **0**, PID limits ±25 and free
(−7 to −10, never railed). Target recovered from `bf = air − custom − PID` = base(96, target) + fan,
which steps cleanly with each commanded target; only segments where **actual RPM matches that target**
are used:

| idle target | actual RPM | total `Idle air %` = **requirement** | PID | oil bar |
|---|---|---|---|---|
| **1000** | 955–992 | **19–21** | −10 to −13 | 2.00–2.25 |
| **1100** | 1047–1149 | **25–26.5** | −8 | 2.19–2.31 |
| **1200** | 1156–1200 | **32.5–33.5** | −9.5 | 2.44–2.94 |
| **1300** | 1321–1363 | **43.5–44.5** | −7.5 | 2.81–2.94 |
| **1375** | 1383–1445 | **49.0** | −6.9 | 3.06–3.19 |

Monotone, ~6.5 airflow % per 100 rpm from 1000 to 1375. **Base-table entry = requirement − 13 (fan):
7 / 13 / 20 / 31 / 36.** Current live base (from `bf` − 13) reads 18.4 / 20.75 / 29.9 / 38.9 / 42.9 —
**uniformly 7–11 fat**, which is exactly the negative PID the loop carries at every target.

### 13.2 Zero pressure sensitivity inside 2.0–3.2 bar

At matched target, pressure does nothing:

- target **1200**: t=309 → 2.94 bar / 33.5; t=685 → 2.44 bar / 33.5. **Flat over 0.5 bar and 6 minutes.**
- target **1100**: 2.31 → 26.5; 2.25 → 25.0.
- target **1000**: 2.25 → 21.0; 2.00 → 18.5 (−2.5 over 0.25 bar *or* 3.7 min — indistinguishable).

**⚠ Scope limit: this log does NOT test above ~3.2 bar at matched target.** While pressure was 4.3–4.8
(t 0–150) the FF was still over-aired, so RPM hung **130–190 above target** (actual 1327–1388 against
target 1200) and those segments read the hang, not a requirement. The apparent 54 → 43.5 fall at
~1375 rpm is **t=90 vs t=600 — 8.5 minutes of soak, not 1.4 bar.**

### 13.3 No decaying term on a warm restart — the cold-start-adder model holds

At target 1200 the requirement is 33.5 at t=309 and 33.5 at t=685: **flat for 6 minutes** while
pressure fell 2.94 → 2.44. In `goodrun`'s *cold* start the same window carried a ~30-point excess.
So the adder is present after a cold start and absent after a warm restart, independent of oil
pressure — the surface/metal-heat model (R8 §7, Heywood mixture preparation) on a
**time-since-cold-start** axis, not a pressure axis.

### 13.4 Idle lambda target 0.90 (Will, 2026-08-16)

Richened idle target λ 0.93 → **0.90**; the lean stumble at 0.93 went away. Consistent with best-torque
λ ≈ 0.88–0.92 — 0.93 sits lean of it, so it loses torque per unit air *and* raises cyclic variability
at the idle load point, which reads as stumble.

**Consequence for §13.1: those requirements are λ-0.90 numbers.** Richening raises torque per unit air,
so it **lowers** the airflow requirement; a return to 0.93 invalidates the table. Verified not to be a
confound *within* this log — `Injectors PW` is flat at 1.548 ms throughout and the fuel-per-air index
(`PW × RPM / MAP`) tracks RPM only, with no step.

### 13.5 What this changes

- **Correction table: zero it** (done). Do not re-issue on a pressure axis.
- **Base `idleActiveAirflow`, 96/105 columns: 7 / 13 / 20 / 31 / 36** at targets 1000/1100/1200/1300/1375
  — measured, λ 0.90, fan assumed +13 (CLT 96–98, fan on; not logged in this export).
- **The cold-start term still exists and is still unmeasured on its own axis.** It is worth ~+30 at
  1200 rpm in the first minutes of a cold start (goodrun) and ~0 on a warm restart (this log). Needs a
  time-since-start or engine-metal-temperature axis; `Charge temp` is the best available proxy and is
  still not in the export.
- **§12.12's correction table is WITHDRAWN — do not import it.** §12.7's is also dead. The measured
  cells in §12.4/§12.7 remain valid as *observations of two states*, not as a pressure curve.

### 13.6 Charge temp tested and it does nothing either (`bighotidlewithcat.csv`, same run + `Charge temp`)

CAT runs **50 → 65 °C**, monotone: `corr(CAT, time) = +0.90`, `corr(CAT, oil pressure) = −0.73`. It is
the same soak channel wearing a different hat. At **matched idle target**, correction = 0 era only:

| target | CAT 55–59 | CAT 59–62 | CAT 62–66 |
|---|---|---|---|
| 1000 | — | 21.0 | 21.0 |
| 1100 | — | 26.0 | 25.5 |
| **1200** | **33.5** (OP 2.94) | **33.0** (OP 2.69) | **33.5** (OP 2.44) |
| 1300 | — | 44.0 | 44.0 |
| 1375 | — | 49.0 | 49.0 |

**The requirement does not move — across CAT 55→68 °C or oil pressure 2.9→2.4 bar simultaneously.**
Hot idle airflow is a function of **idle target RPM alone** in this regime. (Span caveat: 13 °C of CAT
and 0.5 bar of OP; the invariance is exact but the range is narrow.)

**Mechanism note — CORRECTED 2026-08-16 (Will): the CAT sensor is PRE-throttle** (no plenum sensor).
So it *does* enter the choked-flow equation, via `ṁ ∝ A·P_up/√T_up`. Magnitude: 50 → 65 °C is
`√(338/323) = 1.023`, i.e. **2.3 % less mass flow at fixed area ≈ +0.8 airflow % at 1200 rpm** —
below this data's noise floor. The measured invariance stands; only the reasoning changes. What it does enter is MAP and the
ECU's speed-density air **estimate**. So CAT's only route to idle quality is the fuel side.

### 13.7 Idle mixture — the CAT-enrichment plan, and the one gate on it

Will's plan: keep λ target 0.93 and add fuel through the charge-temp fuel correction as CAT rises.
The instinct is standard and the magnitude is real — at CAT 65 °C vs ~33 °C ambient the ECU computes
**~10 % less air**, and if the sensor over-reads true mean charge temperature by even 15 °C (normal at
idle heat soak: the sensor sits in hot manifold metal while the air's residence time is short), that is
a **~4.5 % under-fuel**, i.e. commanded λ 0.93 delivering ~0.97 actual. That would stumble.

**Gate: is idle closed-loop on lambda?**
- **Closed loop** → STFT trims the added fuel straight back out to hold 0.93, so the CAT table does
  nothing at idle. Then the 0.93 stumble was *genuinely* lean-of-best-torque, and **λ 0.90 target is
  the correct and sufficient fix** — normal for a 264°-cam 3.0 L at 1200 rpm, where residual fraction
  is high and best-torque λ sits rich.
- **Open loop** → the CAT over-read is unopposed and the CAT fuel table is exactly the right lever.

Cannot be resolved from any log so far: **`Lambda`, `Lambda is valid`, and `Short term trim` are not
in any of these exports.** Add them; it is a one-line answer once they are there.

### 13.8 The founding symptom is a TRANSIENT, and that is why no axis ever fit

Will, 2026-08-16: the observation that started the oil-pressure work is **idle rpm sagging after a
short drive with cold oil and a hot engine**.

Put it next to today's warm-restart test — the thermal coordinates are the same (hot CLT, hot engine
metal, oil still cold at ~4.5 bar) and the outcomes are **opposite**: today the car was
**over-aired** and would not enter idle, requirement ≈33 at 1200. The founding case **sags**.

The two are not in conflict on thermal state, because thermal state is not what separates them:
**one is steady-state, the other is a return-to-idle transient.** The oil-pressure correction was
built as a steady-state feed-forward table to fix a handoff/undershoot event. Wrong instrument, and
it is why every axis tried (oil pressure, CLT, charge temp, alternator) fits one dataset and breaks
on the next.

R9 §3 already reached this and it was not carried forward: *"a static (P, rpm) table cannot fix a bog
because P is a fast function of N and collapses during undershoot — oil pressure is not a valid
viscosity proxy through an RPM transient."* During the sag, P falls **with** rpm, so a pressure-indexed
correction moves the wrong way exactly when air is needed.

**Levers that actually address a return-to-idle sag** (none of them the base or a correction table):
`idleMinMapToActivate` (the 25 kPa over-gate locks idle out under engine braking — documented root
cause, [`../../notes/return_to_idle_bog.md`](../../notes/return_to_idle_bog.md)), `idleRAMPDownOffset`
(where the descent hands off to Active), the armed→active level match, and PID D-term/authority
through the catch.

**Log needed — none of the logs to date contain this event.** `goodrun`'s drive *raised* oil
temperature (3.3 → 2.6 bar across it), so it is not a cold-oil return. Required: **cold start, drive
3–5 minutes, return to idle**, full rate, carrying `Idle state`, `Idle target`, RPM, `Idle air %`,
airflow PID, oil pressure, MAP. **Decisive question: does RPM undershoot and recover (transient →
handoff/gate fix), or settle low with the PID pinned positive (steady deficit → table fix)?** Those
have nothing in common, and the whole R5→R13 effort assumed the second without ever logging the first.

### 13.9 Base stays fat — and the current base already IS the design (Will, 2026-08-16)

Will's standing principle, restated: **keep base airflow high and let the PID trim down; if the engine
dies before the PID can air up, we're finished.** He is right about the direction, and it reconciles
with the R8 §5 "program measured values" correction once the two failure modes are separated:

- **PID reset / zero-out** (state change, recovery, afterstart): a fat base stores **negative**
  integral, so a reset lands the engine **high — a flare, which is survivable.** A base trimmed to the
  measured requirement stores positive integral and a reset lands it **low — a stall.** Fat is
  unambiguously the safe side.
- **Transient needing fast air** (load step, fan cycle, handoff catch): a *deeply* negative integral
  has to climb out of its hole before it can add air. That slew, not the reset, is this car's
  documented windup-purge-stall mechanism.

Both are satisfied by the same rule: **the base's fat margin and the integral limit should be the
same number.** Margin buys the open-loop guarantee; capping the integral at that margin stops the
store getting deeper than the loop can unwind.

**⚠ §13.5's "base = 7 / 13 / 20 / 31 / 36" is WITHDRAWN.** That was the bare requirement with zero
cushion. Correct form is `requirement + margin`, and measuring today's margin shows **the live base is
already right**:

| target | requirement (§13.1) | live base (`bf` − 13) | margin | settled PID |
|---|---|---|---|---|
| 1000 | 7 | 18.4 | **+11.4** | −10 to −13 |
| 1100 | 13 | 20.8 | **+7.8** | −8 |
| 1200 | 20 | 29.9 | **+9.9** | −9.5 |
| 1300 | 31 | 38.9 | **+7.9** | −7.5 |
| 1375 | 36 | 42.9 | **+6.9** | −6.9 |

**The −7 to −13 PID is not an error to be tuned out — it is the cushion doing its job**, and it is
roughly uniform across the RPM axis, which is what a correctly-shaped base looks like. Only the **1000
row is out of family (+11.4 vs +7–10 elsewhere); trim ~3.** Everything else: no change.

**Cushion sizing — what it must actually cover at hot idle:** coolant-fan cycling (the fan term is
+13, modeled, but its transition is real), electrical load steps (**3 airflow % per 10 A**, §12.11),
power steering at lock, gear engagement. **6–10 airflow % is the right size**, which is where the live
table sits. The cold-start term (up to +30) lives in the base's CLT columns, not the hot cushion, and
the oil term is now small (§13.9's μ^0.3 table, ≤+15 at relief pressure).

**Action item, needs the tune:** the airflow PID's **integral** limits are internal and never appear in
the log (clamp-reading rule, Method note). Output is now ±25, which is correct for the P term. Set the
**integral** limit to ≈ **−10** — matching the measured margin — so it can hold target in steady state
but cannot dig a hole deeper than one PID cycle can climb out of.

### 13.10 Matched-point comparison, and what it settles (2026-08-16)

Will's cherry-picked points from `bighotidle.csv` matched into `goodrun.csv` (CLT 95–97, RPM ±45,
oil pressure ±0.20 bar, `Idle state == 2`):

| | RPM | oil bar | `goodrun` (cold start) | `bighotidle` (warm restart) | Δ |
|---|---|---|---|---|---|
| A | 1233 | 3.19 | **56.5** (PID −0.25, at target) | **39.0** (PID −14.9, RPM 1247 vs tgt 1200) | **≥17.5** |
| **B** | **1192** | **2.81** | **55.0** (PID +0.19, at target) | **33.0** (PID −9.75, at target) | **22.0** |

**B is the decisive pair:** both converged, both PID free of the rails, both on target, MAP 37 in each.
Identical coolant, RPM, oil pressure — 67 % different airflow requirement. (A understates the gap;
`bighotidle` was over-aired there, so 39 bounds the 1200 requirement from above.)

Full sweeps, CLT 96, RPM 1150–1280:

| oil bar | `goodrun` | `bighotidle` |
|---|---|---|
| 2.0–2.6 | 30.0 *(post-drive)* | 33.0 |
| 2.6–3.0 | 55.0 | 33.0 |
| 3.0–3.4 | 56.5 | 39.5 |
| 3.4–3.8 | 58.5 | 41.5 |
| 3.8–4.4 | 61.5 | 43.5 |

### 13.11 The three questions, answered from the above

**1. Is oil pressure a poor proxy for viscosity? — No, and that is the point.**
`P ∝ μ·N` held: at point B both logs read 2.81 bar at 1192 rpm, so the gallery correctly reported
**the same viscosity in both** — and the requirement still differed by 22. **The proxy did its job;
the model built on it was wrong.** Oil pressure is not on trial here, viscosity is. (Genuine but
second-order imperfections remain on record: bulk-gallery vs bearing-film viscosity, R8 §3, and P
collapsing with rpm through a transient, R9 §3.)

**2. Was CLT the big issue before? — No, but the CLT columns have been carrying this term.**
CLT is neither necessary nor sufficient: in `goodrun` specific airflow was **flat at ~50–56 from CLT 39
to CLT 96** (§12.4), and point B holds CLT at 96 in both logs with a 22-point spread. R8's measured
δ(CLT) — +26.7 at ≤35 °C, +16 at 35–55, +6.5 at 55–80, ~0 at ≥80 — is real but lives below ~55 °C.
What has actually been happening: **on a canonical cold start, CLT is a decent clock for the pedestal**,
so the CLT columns absorbed it and looked correctly sized (R8 §5's back-calc). That is exactly the R8
"decomposition guard" trap — along one warm-up path everything co-varies, so you identify only the sum.
The columns work until the path changes.

**3. Is viscosity not the big issue? — Correct. It is real, it obeys Heywood, and it is small.**
Within either branch the pressure slope is **~5 %/bar**: `goodrun`'s cold branch runs 55.0 → 61.5
across 2.8 → 4.1 bar, exponent **μ^0.24**; `bighotidle`'s bound gives **μ^0.31**. Heywood's is **0.3**.
Total viscosity contribution across the entire idle pressure range (2.0 → 7.3 bar) is **≈ +13–15
airflow % at 1200 rpm** — smaller than the single 22-point pedestal at one fixed pressure. The R9-era
`μ^1.66` was never a viscosity law; it is the shape a pedestal takes when forced onto a viscosity axis.

**Synthesis: CLT and oil pressure are both clocks, and the thing they were clocking is the pedestal.**
Both work on the canonical cold-start path and both fail off it (warm restart, short drive).

```
requirement = f(idle target rpm)                    large, measured, §13.1
            + ~5 %/bar oil pressure                 real, μ^0.3, ≤ +15 total
            + pedestal(heat put into the structure) ~ +22, killed by a drive, axis unknown
```

**Open, and unresolved by any log to date:** does the pedestal decay on its own during a long idle, or
does it need a drive? `goodrun` drove before finding out; `bighotidle` was a warm restart with no
pedestal to begin with. That is still Test 1 (§12.13): cold start, **do not drive**, hold 1200 through
CLT 96 and keep idling 15–20 minutes. If the requirement walks 55 → 33 with no drive, the pedestal is
a decaying soak term and a time/temperature axis will carry it. If it stays near 55 until you drive,
it is load-driven structure heating and no idle-only axis will ever see it.

### 13.12 THE TAIL-CHASE, IDENTIFIED: oil pressure is 91 % RPM, and the base table already owns RPM

Will's question — during a deliberate target sweep, how much of oil pressure is just RPM? Measured on
`bighotidle.csv`, t > 470 (the deliberate sweep, correction = 0, CLT 96, viscosity ~constant), n = 6837:

```
P = 2.301e-3 · N − 0.201     r = 0.953     R² = 0.908
through-origin slope 2.127e-3 bar/rpm   (R5 fleet fit: 1.885e-3)
residual sd about the line: 0.115 bar, against a 1.69–3.50 bar range
```

| RPM | P (bar) | 1.885e-3·N | total air |
|---|---|---|---|
| 970 | 2.06 | 1.83 | 21.0 |
| 1077 | 2.25 | 2.03 | 25.5 |
| 1170 | 2.44 | 2.21 | 33.5 |
| 1328 | 2.88 | 2.50 | 44.5 |
| 1437 | 3.13 | 2.71 | 49.0 |

**91 % of oil-pressure variance at hot idle is RPM.** So a `(P, N)` table is close to rank-deficient
there — you cannot identify separate P and N effects from hot idle data at all, only their sum along
the locus.

**And this is the tail-chase, exactly.** `idleActiveAirflow` is indexed on **idle target RPM** and
already carries the full N dependence of the requirement (21 → 49 across 1000 → 1437 in the table
above). A correction indexed on **raw P** then re-applies N a second time, because P *is* N. Sweeping
1000 → 1400 rpm moves P 2.06 → 3.13 and air 21 → 49; attribute that air change to pressure and you get
**~24 airflow % per bar** — which is almost exactly the slope of the §12.12 table this note has already
had to withdraw. **The steep table was partly the RPM axis, counted twice.**

**Where the error entered: R5.** It rejected the viscosity index in favour of raw pressure on the
argument that friction ∝ μ·N = P. The physics is right and the bookkeeping is wrong — **N is already
in the base table**, so the correction's job is only what is left over, which is **μ**. Raw P "fitting
better" (R² 0.51 vs 0.49) is exactly what double-counting a real axis looks like.

**Fix — index the correction on `P/N`, not `P`:** viscosity index in **bar per 1000 rpm**,
`index = OP[bar] / RPM × 1000`. Measured span:

| state | index |
|---|---|
| hot idle, any target | **1.9–2.1** |
| `goodrun` hot CLT / cold oil (4.12 bar @ 1197) | 3.44 |
| cold start (7.25 bar @ 1518) | 4.78 |

Zero the correction at **≈ 2.0**. A hot idle at *any* target then reads zero automatically — which
also dissolves the phantom-correction problem §13.9 had to patch by moving axis bins, and restores
R5 Result 3's original index axis. Residual `sd(P | RPM) = 0.115 bar` sets the noise floor: at 1200 rpm
that is ±0.10 of index, so bins finer than ~0.25 index are meaningless.

## Result 14 — Test 1 was already in the archive: the pedestal decays CONTINUOUSLY over 15 min at pinned CLT 96 (2026-08-16, `all-channels-reduced-idlaircorr.csv`)

Six **565-channel** logs exist in the OneDrive Supra folder carrying everything the recent 14–17 column
exports lack — `Idle target`, `Ignition Angle`, `Idle ignition target`, `I.Idle`, `Back pressure`
(EMAP), `Charge temp`, `Lambda 1`, `Lambda target`, `Short term trim`, `VVT CAM1 angle` + target +
solenoid DC + status, per-cylinder knock, `VE`, `Warmup enrichment`, `Afterstart Enrichment`.
Present: `all-channels-reduced-idlaircorr.csv` (53 MB), `20260613_1141.csv`, `all-channel-reference.csv`.
**Missing from the folder** (listed in R10, gone now): `drivehome.csv`, `20260524_1301.csv`,
`new_fuel_strategy.csv`.

`all-channels-reduced-idlaircorr.csv`: cold start **CLT 29**, CLT 96 reached at t = 258 s, then
**15.8 minutes at CLT pinned 96** with `Idle target` = 1200 held repeatedly (driving interleaved, but
held-idle samples throughout). Mask: `Idle state == 2`, TPS < 10, MAP < 55, CLT ≥ 95,
|RPM − `Idle target`| < 60, target == 1200.

| min since CLT96 | n | total air | air/1000 rpm | oil bar | **CAM1 angle** | CAM1 tgt | CAM1 DC | CAT | ign | PID |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 503 | **50.0** | 43.7 | 4.25 | **4.0** | 2.5 | 40 | 44 | 21.0 | +15 |
| 2 | 739 | 50.0 | 41.0 | 4.25 | 3.0 | 2.5 | 40 | 44 | 20.0 | +15 |
| 3 | 541 | 47.5 | 39.7 | 3.38 | 2.5 | 2.5 | 42 | 47 | 20.0 | +14.6 |
| 4 | 1375 | 42.5 | 35.7 | 3.25 | 1.5 | 2.5 | 42 | 48 | 17.5 | +6.4 |
| 5 | 1128 | 41.5 | 35.3 | 3.06 | 0.5 | 2.5 | 43 | 49 | 17.5 | +2.6 |
| 6 | 61 | 37.0 | 30.7 | 2.69 | **0.0** | 2.5 | 44 | 49 | 17.5 | −1.6 |
| 8 | 310 | 33.5 | 27.2 | 2.50 | 0.0 | 2.5 | 44 | 51 | 17.0 | −2.9 |
| 11 | 50 | 35.5 | 28.5 | 2.25 | 0.0 | 2.5 | 44 | 49.5 | 17.0 | −2.2 |
| 14 | 120 | 33.0 | 26.1 | 2.06 | 0.0 | 2.5 | 47 | 52 | 16.5 | −3.4 |
| **15** | 500 | **31.0** | **25.2** | **2.00** | 0.0 | 2.5 | 47 | 54 | 15.5 | −4.0 |

### 14.1 The pedestal is a smooth decay, not a latch

**50.0 → 31.0 airflow % (spec 43.7 → 25.2) over 15 minutes with CLT pinned at 96 the whole time.**
Monotone, no step, no threshold. **This is Test 1, already run.** `goodrun`'s apparent "step" was a
drive landing in the middle of exactly this curve. So the term **is** continuous and **is** indexable —
the question was never whether, only on what.

### 14.2 A named knock-on effect: the VVT phaser does not track while the oil is thick

`VVT CAM1 angle target` is **2.5° constant** all the way through. The actual cam runs **4.0° → 0.0°**
while `VVT CAM1 solenoid DC` climbs **40 → 47 %** and `VVT CAM1 status` = **5** (non-zero = not
following). So the phaser **overshoots target by 1.5° on thick oil and undershoots by 2.5° once it
thins**, with the solenoid working progressively harder. Cam position tracks the requirement closely
over the first half of the decay.

**Scope, honestly:** cam angle pins at 0.0 by minute 6 while the requirement keeps falling 37 → 31
through minute 15. **Cam explains roughly the first half of the decay and none of the tail.**
*(Will ruled VVT out earlier on general grounds; this is the measurement, recorded as data. It does not
resurrect VVT as "the" answer — it identifies one contributor with a hard ceiling on its explanatory
range.)*

### 14.3 What this log rules out — with channels the short exports never had

- **Combustion quality / CoV:** `Knock Engine Noise` flat at 5.0; per-cylinder knock-voltage σ 0.015–0.042
  with no trend across the decay. No combustion-stability signature.
- **Mixture:** `Lambda 1` flat 0.94–0.96, `Short term trim` −0.2 to +3.8, `VE` flat 41.7–42.4. Not fuel.
- **Charge temp: wrong sign.** CAT *rises* 44 → 54 °C while the requirement *falls*.
- **Ignition: wrong sign.** `Ignition Angle` falls 21.0 → 15.5° against a constant `Idle ignition
  target` of 18 and constant `I.Idle` = 1.0. Retarding costs torque, so it would demand *more* air.

### 14.4 Viscosity still does not close it, even after the cam parks

Across the whole window: spec ratio 43.7/25.2 = 1.73 for a μ ratio (P at fixed 1200 rpm) of
4.25/2.00 = 2.13 → **exponent 0.72**. In the cam-free tail alone (min 6 → 15): 30.7/25.2 = 1.22 for
2.69/2.00 = 1.345 → **exponent 0.67**. Heywood's is **0.3**. Consistent power law, roughly **2.2×
too steep for viscous friction** — so a real residual soak term survives after both the phaser and
viscosity are accounted for. Will's framing is right: **the structure is not heat-soaked yet even at
CLT 96, and it has knock-on effects beyond oil viscosity and wall friction.**

### 14.5 Consequence for the axis

Oil pressure walks 4.25 → 2.00 monotonically over precisely the window in which the requirement decays,
so **on a cold start it is a perfectly serviceable index** — not because it measures the mechanism, but
because it is the best continuously-varying clock available. It failed on the warm restart (§13.10)
because on *that* path the oil is thick while the structure is already soaked, and pressure cannot tell
the two apart.

**So the correction needs a cold-start gate, not a better axis.** A pressure-indexed correction that is
armed only when the start was cold reproduces both datasets; the same table with no gate is what
over-aired the warm restart. Deciding the gate variable (CLT at start, or engine-off time, or a
running-time latch) needs the tune to see what EMU actually exposes.

### 14.6 Design directive (Will, 2026-08-16): over-air during warm-up is acceptable; **surprise air starvation is not**

This flips the sizing rule. Size the feed-forward to the **upper envelope** of the requirement across
all thermal paths at a given index, not to the median or to any single path.

Envelope at **idle target 1200**, total `Idle air %`, pooled across the cold-start and warm-restart
branches (§13.10, §14):

| oil bar | cold start | warm restart | **envelope** | worst-case over-air |
|---|---|---|---|---|
| 2.0–2.6 | 31 | 33 | **33** | 0 |
| 2.6–3.0 | 55 | 33 | **55** | **22** |
| 3.0–3.4 | 56.5 | ≤39 | **56.5** | 17.5 |
| 3.4–3.8 | 58.5 | 41.5 | **58.5** | 17 |
| 3.8–4.4 | 61.5 | 43.5 | **61.5** | 18 |

**Over-air is only a failure when it exceeds the PID's negative authority** — that is the exact
mechanism by which the warm restart could not enter the idle region (§13). The arithmetic:

```
warm-restart excess with an envelope-sized FF   ≈ 22–28 at 1200 rpm
airflow PID output minimum, current              = −25
```

So an ungated envelope table is **marginal today and was overshot by the §12.12 table** (base+fan ~40
+ correction +30 = 70 against a 33 requirement = **+37 excess**, well past −25 → hang). Two coherent
designs:

- **A. Ungated envelope + wider negative authority (matches the directive).** Program the envelope
  column above; set the airflow PID **output minimum to ≈ −35** and the **integral minimum to match**.
  Never starves on any path. **Cost, named:** a warm restart then runs a steady **−22 to −28 integral**,
  and a transient needing fast air has to climb out of that hole — the windup-slew risk of §13.9,
  now deliberately accepted rather than stumbled into.
- **B. Cold-start-gated correction.** Arm the pressure correction only when the start was cold. FF is
  then correct on both paths, PID sits near zero, no deep integral, no authority change. Needs a gate
  variable — CLT at start, engine-off time, or a running-time latch — which requires reading the tune
  to see what EMU exposes.

A is one parameter and available now; B is better behaved but needs the tune. **Under the directive as
stated, A is the design.**

### 14.7 VVT scoped down (Will, 2026-08-16)

Will: the 2.5° target *"is just enough to take the slack out of the gear, not enough to actually
advance it."* Accepted, and it bounds §14.2 tightly: if 2.5° is take-up, the cam's measured **4.0°**
is only **~1.5° of real advance**, and 0.0° is slack, not retard. At 1.5° of cam on a 264° grind the
overlap/residual change at idle is small — consistent with §14.2's own finding that cam position
explains at most the first half of the decay and pins at 0 while the requirement keeps falling.
**VVT stays scoped out as a driver.**

One byproduct worth keeping: `VVT CAM1 solenoid DC` climbing **40 → 47 %** to hold the same commanded
angle across the warm-up is an independent, control-loop readout of oil viscosity — a second viscosity
channel that is not the gallery pressure sensor, if one is ever wanted for cross-checking.


## Result 15 — Were the earlier CAT and oil-viscosity findings imagined? No. The observations reproduce; the attributions were wrong (2026-08-16)

Will's question, and it deserves a direct accounting because two sessions of work rest on it.

### 15.1 The oil finding reproduces exactly

Result 1 (11 logs, 2026-05-24 → 07-30): hot coolant + cold oil = **51–58** airflow %, hot coolant +
hot oil = **28–31**, difference **+20 to +29**. Result 8's soak trim: **−11.5 at ≤ 2.5 bar**
(n = 2828, two logs).

Today's cleanest single trace, `all-channels-reduced-idlaircorr.csv` at target 1200 with CLT pinned at
96 for 15 minutes (§14): **50.0 → 31.0** as oil goes **4.25 → 2.00 bar**. Same numbers, same span,
independent log, independent tune era. **The correlation was never imagined and is not in question.**

### 15.2 The CAT finding is the same signal through a different sensor

Today, raw `r(excess, CAT) = −0.808` (n = 18,038) — a strong, real correlation, exactly what earlier
sessions saw. It collapses to **−0.103** only once **oil pressure** is controlled, and to
**−0.5 airflow % across 9 °C** in the window where CAT moves alone. Meanwhile
`r(excess, oilP | RPM, tgt, CAT, CLT) = +0.552`.

Before oil pressure was logged, CAT was the only clock in the car, so it took the credit. Once oil
pressure was logged, it took the credit. `r(CAT, oilP) = −0.875`. **Both sensors were reading one
warm-up soak signal.** Neither session hallucinated; each regressed on the best clock it had.

### 15.3 What was actually wrong — attribution, not observation

1. **Causal share.** Measured exponent on μ is **0.67–0.72** (§14.4), including in the cam-free tail.
   Viscous friction gives **0.3** (Heywood). So viscosity is worth roughly **a third to a half** of the
   swing; the remainder is a soak term riding the same clock. The R9-era `μ^1.66` was that error at
   its maximum.
2. **Portability.** Every dataset through R12 was collected on **one path** — a normal cold start,
   where CAT, oil pressure, CLT, structure heat and battery-recharge load all move together. The R8
   "decomposition guard" warned in writing that such a path identifies only the *sum*. It was overrun
   anyway. **The 2026-08-16 warm restart is the first genuinely off-path measurement**, and it is the
   only thing that could have exposed this: same CLT 96, same 2.81 bar, same 1192 rpm →
   **55.0 (cold start) vs 33.0 (warm restart)** (§13.10).

### 15.4 What stands unchanged

- Requirement at 1200 falls ~20 points (50 → 31) over the 15 min after CLT pins at 96 — many logs,
  many tune eras.
- Hot-soaked requirement at 1200 ≈ **30–33**.
- The −11.5 soak trim at ≤ 2.5 bar is real; it is the same phenomenon seen from the hot end.
- **On a cold start, hot coolant + cold oil genuinely needs ~+20 more air.** Program for it.

### 15.5 What changes in practice

Very little, and only in one place: **the correction must not fire on a warm restart.** An
oil-pressure-indexed table remains a perfectly serviceable index for the cold-start path — the only
path where this term is large — because pressure is the best continuously-varying clock available
there. It just needs a cold-start gate (§14.6 option B), or the envelope sizing plus wider PID
negative authority (§14.6 option A) if a gate variable is not available in EMU.

**Standing methodological rule, promoted out of R8's guard to the top of this note: a correlation
established on the canonical cold-start path is a clock reading, not a mechanism, until it is
reproduced on a path where the clocks disagree** — warm restart, short drive, or a long undriven idle.

## Symbol definitions used throughout Results 12–16 (added 2026-08-16 at Will's request)

**These are analysis constructs, not tune parameters or log channels unless stated.** Several were used
in chat without being defined — corrected here.

| symbol | definition | measured or inferred |
|---|---|---|
| **μ** | dynamic (absolute) viscosity of the **engine oil**. | **NEVER MEASURED.** Inferred only: gallery pressure `P ∝ μ·N`, so at fixed RPM a *pressure ratio* is taken as a *viscosity ratio*. Every "μ ratio" statement in this note is a pressure ratio relabelled. There is no viscometer and no oil-temp sensor (`oilTempInput = 0`). |
| **exponent on μ** | fitted `k` in `demand ∝ μ^k`. | Fitted from pressure ratios. Physical reference: Heywood gives engine friction ∝ μ^~0.3 because most FMEP is viscosity-insensitive. Measured here 0.67–0.72; the R9-era 1.66 was the same error at maximum. |
| **P_hot(N)** | fitted gallery pressure at fully soaked oil vs engine speed = **1.885e-3 · N bar** (R5). 2.26 bar at 1200 rpm. | Fitted, 3911 hot foot-off samples; re-confirmed 2026-08-16 (2.25 measured at 1197). |
| **viscosity index** | `oil pressure [bar] / RPM × 1000` — bar per 1000 rpm. Removes the speed term so what is left is the viscosity term. Hot idle ≈ **1.9–2.1**; hot-CLT/cold-oil ≈ 3.4; cold start ≈ 4.8. | Derived per sample. **This, not raw P, is the correct correction axis — see §13.12.** |
| **bf** | `Idle air %` − `Idle airflow custom corr.` − `Idle PID air % correction` = **base(CLT, idle target) + fan**. Reconstructs the live base-table lookup from any log, including through mid-log table edits. | Derived; composition verified to ±0.27 (R7) and ±0.95 (R9). |
| **excess** | `Idle airflow custom corr.` + `Idle PID air % correction` = total deviation from the base lookup. | Derived. Immune to correction-table edits, which is why it is the right dependent variable when the FF changed mid-log. |
| **spec_air** | `Idle air %` / RPM × 1000. Airflow per unit engine speed — a **torque-demand proxy**, valid because at a choked throttle `Idle air %` is mass flow and per-cycle demand is flow/rpm (§12.1). | Derived. |
| **pedestal** | The offset in required airflow at **matched** CLT, RPM, and oil pressure between a cold-start idle and a warm restart: **+22 airflow % at 1200 rpm** (§13.10). | Measured at one cell only. Mechanism unknown; killed by a drive; decays smoothly over ~15 min (§14.1). |
| **envelope** | Per-cell **maximum** requirement across all thermal paths, as opposed to the median or any single path. | Pooled from measured cells. |
| **FF** | **feed-forward** = base + fan + custom correction, i.e. everything the PID is not. **Not flex fuel.** | — |

## Result 16 — Target airflow cold vs hot, and Will's negative-only correction (2026-08-16)

### 16.1 The two anchor columns

Total commanded `Idle air %` required to hold each idle target. **Hot** = fully soaked (≈2.0–2.4 bar,
viscosity index ≈2.0). **Cold oil at hot CLT** = the cold-start branch (≈4.3+ bar, index ≈3.4–3.8).

| idle target | **HOT oil** | **COLD oil, hot CLT** | basis |
|---|---|---|---|
| 1000 | **20** | 34–43 | hot measured (§13.1); cold **not measured** |
| 1100 | **26** | 44–49 | hot measured; cold **not measured** |
| **1200** | **33** | **55–61.5** | **both measured** (§13.1, §13.10, §14) |
| 1300 | **44** | 67–75 | hot measured; cold **not measured** |
| 1375 | **49** | 72–83 | hot measured; cold **not measured** |

**⚠ Only the 1200 row is measured on both sides.** The idle-target schedule is flat 1200 for CLT ≥ 75,
so a hot-CLT/cold-oil state at any other target essentially never occurs — it is not a sampling gap,
it is unreachable without a deliberate target sweep during the first minutes after CLT 96. The cold
column elsewhere is the **span between the two ways of extending the 1200 measurement**: additive
(+23 at every target) and proportional (×1.69). Take the per-cell max for an envelope.

Base-table cell = total − 13 (fan). Cold-oil-anchored 96/105 column, envelope form:
**30 / 36 / 48.5 / 62 / 70** at 1000 / 1100 / 1200 / 1300 / 1375.

### 16.2 Will's inversion — leave the base high, correct downward — is better than §14.6 option A

Directive: size the base table for the **cold** case and let the oil-pressure correction **subtract**
air as the oil thins, so a sensor failure defaults high.

**This is the better architecture, and the arithmetic is why.** Under §14.6 option A (envelope base
*plus* a positive correction) the FF stacked to ~70 against a 33 requirement — a **+37** excess past
the PID's −25, which is exactly the hang that happened. Under the inversion the base *is* the
envelope, nothing is added on top, and the worst case is:

```
warm restart, target 1200, cold-oil pressure, correction reads 0
  FF = 56  vs requirement 33  →  excess +23   (PID min −25: fits)
```

and the correction, not the PID, carries the removal on every normal path — so the PID sits near zero
instead of parked deep negative. That retires the windup-slew cost named in §13.9/§14.6.

Correction magnitude required, negative-only, zero at the cold-oil end:

| idle target | correction at hot oil (index ≈2.0) |
|---|---|
| 1200 | **−23** |
| 1375 | −34 |

The 1375 excess exceeds PID authority, but that cell is only exercised during warm-up at cold CLT,
where the cold-oil value is the correct one — so it does not arise in practice. Worth re-checking if
the idle target schedule ever puts 1375 at CLT ≥ 90.

### 16.3 ⚠ THE FAILSAFE IS BACKWARDS AS SHIPPED — one parameter decides whether this design is safe

`oilPressureFailSafe = 0` (R6). EMU clamps an axis input below the first bin to the first bin's value.
With a **negative-only** correction on a rising-pressure axis, the low-pressure end is the
**most-negative** cell — so a failed sensor substituting 0 bar reads **maximum air removal**, i.e.
**exactly the starvation this design exists to prevent.** The failure direction is inverted from intent.

**Required companion change: set `oilPressureFailSafe` to a HIGH value (≈6–7 bar), not 0.** Then a
failed sensor reads "cold oil" → correction 0 → base stays at its cold envelope → over-air → PID trims
→ engine lives. **Do not ship the negative-only table with the failsafe at 0.**

### 16.4 Terminology check on "armed state table"

Will's directive says "armed state table," and he has noted he uses that interchangeably with the idle
air base table (lexicon entry, 2026-08-16). The design only works on the **`idleActiveAirflow` (Active
state) base map** — that is the table the custom correction adds to. The true `idleArmedAirFlow` is
firmware-1-D on RPM only and the custom correction **provably never reaches it** (R6: help says
active-only; measured armed output = armed table ± 0.15). So the oil-pressure value cannot default
anything in armed state. Read as `idleActiveAirflow`.

## Result 17 — Why the μ exponent reads 0.7 instead of 0.3, and the CLT-gated correction (2026-08-16)

### 17.1 Hypotheses for the exponent discrepancy

Measured `demand ∝ μ^0.67–0.72` (§14.4) against Heywood's ~0.3. **All four hypotheses below bias the
apparent exponent in the same direction — too high — and H2 alone is sufficient. No exotic physics is
required.**

**H2 (leading, and sufficient on its own): the pedestal contaminates every single-path fit.**
Demand along a cold-start warm-up is `viscosity term + pedestal term`, and both decay on the same
clock. Fitting a two-term signal with one term puts the whole decay on the surviving axis. The measured
exponent is therefore `(true viscosity exponent) + (pedestal projected onto the pressure axis)`, which
is exactly the R8 decomposition-guard failure mode. **Self-correction to §14.4: the min 6→15 window was
described as the "cam-free tail," which is true, but it is NOT pedestal-free — demand still falls
37 → 31 there. So the 0.67 tail figure is contaminated too and is not a cleaner estimate.**

**H1: gallery pressure under-reports viscosity at the cold end.** `P ∝ μ` holds only while the pump is
off relief and the leakage paths stay laminar. Any pressure-capping mechanism at the cold/high end —
relief valve cracking, **oil-filter bypass valve** opening on high ΔP — makes the observed pressure
ratio *smaller* than the true viscosity ratio. A smaller denominator with the same numerator inflates
the fitted exponent. R5 placed the relief plateau above idle range, but *partial* relief below that was
never excluded. **Testable without new hardware:** `VVT CAM1 solenoid DC` climbs 40 → 47 % across the
same warm-up (§14.7) and is an independent viscosity readout — if its trajectory is more curved than
pressure's, pressure is being capped.

**H3: 0.3 is the wrong reference exponent for a light-load idle point.** Heywood's ~0.3 is total FMEP at
2000 rpm, where ring friction under gas load and boundary terms dominate and are viscosity-insensitive.
At 1200 rpm with MAP 35 kPa the gas-pressure-dependent ring load is far smaller, so the **hydrodynamic
(μ-linear) share of FMEP is a larger fraction** than in Heywood's case, pushing the true exponent for
*this* operating point up toward 0.5. Part of the gap is a bad reference, not a bad measurement.

**H4: bearing-film vs bulk viscosity (R8 §3, unchanged).** The gallery reads bulk supply viscosity;
friction is set by shear-heated film viscosity. If the film/bulk gap narrows through warm-up, the μ
swing friction actually experiences is larger than the bulk swing measured — exponent inflated again.

**Checked and rejected: oil-pump parasitic drag.** Pump power `= P × Q`; at 1200 rpm, Q ≈ 10–15 L/min,
so 4.3 bar → ~86 W and 2.0 bar → ~40 W. The **46 W** difference is **1.6 %** of the 2850 W idle budget
(§12.11) — far too small to matter.

**Practical consequence: stop using the exponent as a design input.** It is a diagnostic that told us
the pressure axis was over-explaining; it is not a number to build a table from. Program measured cells.

### 17.2 Will's +offset at 5 bar — one constraint

5 bar at 1200 rpm is viscosity index 4.2, i.e. cold-start territory. Measured demand there is the
cold-oil branch: **55–61.5 total at target 1200.** The offset is consistent with the data.

**⚠ Double-count check:** §16.2 raised the base's 96 column to the *cold* envelope (48.5 base + 13 fan
≈ 61.5 total) precisely so the correction could go negative. **Adding a positive 5-bar offset on top of
that base double-counts.** Pick one:

| architecture | base 96 col (1200) | correction at 5 bar | correction at 2 bar |
|---|---|---|---|
| **A. base cold-anchored** | 48.5 | **0** | −23 |
| **B. base hot-anchored** | 20 | **+23** | 0 |

Either way `base + fan + correction` at 5 bar must total **≈55–61**. B is the positive-offset form Will
described; A is the fail-high form from §16.2. **A fails safe on an oil-pressure sensor loss only if
`oilPressureFailSafe` is set high (§16.3); B fails safe with the failsafe at 0.** That is the real
selection criterion between them.

### 17.3 The CLT gate — valid, and there is a strictly better implementation

Will's proposal: arm the correction only at hot CLT, so it engages as the base table hands over to its
96 °C column. **The logic is sound and it targets the measured deficit precisely** — the shortfall
appears exactly when CLT pins at 96 while the oil is still thick (base gives ~40, requirement 50–61).
It also has the right *offset* behaviour for free: CLT switches it on at ~3.5 min, and falling oil
pressure switches it off over the following ~12 min, which matches the measured decay (§14.1).

**Do it as a table axis, not a boolean gate.** EMU's custom correction is 2-D; the live table is
X = oil pressure, Y = engine RPM (R5/R9). **Change Y from RPM to CLT.** Then:

- The cold-CLT rows are simply **zeros** — the gate, with smooth interpolation instead of a step.
- No discontinuity to cross during warm-up, and no chatter as CLT cycles 96–98 with the fan.
- **It fixes the §13.12 double-count for free** — the RPM axis was re-applying a dependence the base
  table already owns (91 % of oil-pressure variance at hot idle *is* RPM), so removing RPM from the
  correction is a strict improvement independent of the gating question.

Ways it can still go wrong:

1. **Warm restarts over-air.** Correction fires on CLT 96 while oil reads 4–5 bar and the structure is
   already soaked → +20 excess at target 1200. **Will accepts this**, and it fits inside PID −25
   *provided the base is not also fat* — the 2026-08-16 hang was +37 because base and correction were
   both raised. Keep the total FF at the envelope, not above it.
2. **Cold CLT with hot oil** (short-trip restart in cold ambient): correction off, base's cold columns
   fire. Safe direction. Fine.
3. **CLT sensor failure:** check `cltFailSafe`. If it substitutes a hot value the correction arms
   permanently; if cold, it disarms permanently. Either is survivable but the direction should be known
   before shipping.
4. **The 1375/1500 rows disappear as a safeguard.** Dropping RPM from Y means one pressure curve serves
   every target. §16.2 showed the required correction is −23 at 1200 but −34 at 1375; a single curve
   under-serves the high targets. Those targets only occur at cold CLT where the correction is zeroed
   anyway, so it does not bite — but re-check if the idle-target schedule ever puts 1375 at CLT ≥ 90.

### 17.4 Architecture A confirmed (Will, 2026-08-16): base cold-anchored, correction SUBTRACTS air

Will: *"I want to take away airflow."* §17.2's fork is resolved to **A**. Also standing, per Will the
same day: **"armed" always means Active** — stop flagging the distinction, read every such directive as
`idleActiveAirflow`.

**Shipping shape.** X = oil pressure, **Y = CLT** (§17.3 — replaces the RPM axis, which was
double-counting). Cold-CLT rows = **0**. Hot-CLT row, base 96 column set so `base + fan` = 56 total at
target 1200 (base = **43**):

| oil bar | 2.0 | 2.5 | 3.0 | 3.5 | 4.0 | 5.0 |
|---|---|---|---|---|---|---|
| **correction, hot-CLT row** | **−24** | −22 | −8 | −3 | 0 | **0** |
| resulting total at 1200 | 32 | 34 | 48 | 53 | 56 | 56 |
| measured demand | 31–33 | 33.5–35.5 | 41.5–56 | 47.5–58.5 | 50–61.5 | 55–61.5 |

The 3.0–4.0 bar cells are the weak ones: `goodrun` (today) reads 55–61.5 there while
`all-channels-reduced` (May/June) reads 41.5–50 at the same pressures. **Tune-epoch spread, per R10 —
do not average them.** Values above follow today's log at the ends and split the difference in the
middle, which is the conservative direction under Architecture A (less subtraction = more air).

**⚠ `oilPressureFailSafe` MUST be raised — this is now load-bearing, not advisory.** Under A the
correction's most-negative cell sits at the *low*-pressure end, and EMU clamps a below-range axis input
to the first bin. With `oilPressureFailSafe = 0` a failed sensor reads **−24** — the deepest air removal
in the table — which is the starvation the whole architecture exists to prevent. Set it to **≈6–7 bar**
so a dead sensor reads "cold oil", correction 0, base holds its cold envelope, PID trims down.
**Architecture A with the failsafe at 0 is strictly more dangerous than no correction at all.**

Second reason not to over-fatten the base: the correction span *is* the failsafe exposure. Base at 56
total needs −24; base at 61.5 needs −28.5. Every point of extra base is another point of air a failed
sensor can remove.

**⚠ Open item that gates programming the cold column: the 55–61.5 cold-oil anchor comes from `goodrun`,
which may predate the λ 0.93 → 0.90 change** (the hot 33 anchor is from `bighotidle`, definitely at
0.90). The *span* is confirmed inside `goodrun` alone at constant λ (55 → 30 across its drive), so the
pedestal is real either way — but the absolute cold number wants **one hot-CLT/cold-oil measurement at
λ 0.90** before the 96 column is set from it. A warm-restart hold at 4–5 bar, or the first minutes after
CLT 96 on the next cold start, supplies it.

### 17.5 The 2026-08-16 hang, exact numbers — and a correction to the earlier arithmetic

From `bighotidle.csv`, `Idle state == 2`, CLT ≥ 96, n = 1939 (t ≈ 80–160 s), target **1200**:

| quantity | value |
|---|---|
| `bf` (base + fan) | **43.00** → **base = 30.0** at the 96 column (fan +13) |
| `Idle airflow custom corr.` | **+29** |
| **FF open loop** (base + fan + custom) | **71.9** |
| airflow PID | −17.4 median, **floor reached −18.6** in this log — effectively railed |
| total `Idle air %` delivered | **54.5** |
| RPM | **1377** against target 1200 → **+177 hang** |
| oil pressure | 4.4 bar |

Earlier in the session the excess was quoted as **+37**, computed against the *hot-oil* requirement of
33. **That was wrong** — at CLT 96 with 4.4 bar oil and a not-yet-soaked structure the requirement is
the cold branch, ≈ **40–45**, not 33. Corrected arithmetic:

```
FF 71.9  −  PID authority 18.6  =  53.3 minimum deliverable
53.3  −  requirement ~40–45     =  8–13 airflow % irreducible excess
8–13 × 13–16 rpm per airflow %  =  105–200 rpm hang     (observed +177) ✓
```

**Architecture A would not have hung here.** Base raised to 43 with the correction at 0 above ~4 bar
gives FF = 56 at that same point, an excess of 11–16 over requirement — inside the −18.6 that was
available then and comfortably inside the ±25 now. The failure was **base 30 plus a +29 correction**,
i.e. a correction sized on a contaminated axis stacked on a base that was already right for hot.

### 17.6 Gate the cold rows — Will's first instinct, and the reason is specific

Will weighed leaving the correction live during warm-up ("it would reflect actual airflow demand for
that RPM") against gating it ("ring drag would be doubly conflated with RPM"). **Gate it.** Three
reasons, in order of force:

1. **The base's cold CLT columns were measured with no pressure correction active** (R8 §5's
   warmup-locus back-calc). They already contain the pressure-correlated part of warm-up demand.
   Turning the correction on in the cold rows adds it a second time — and R8 §6 demonstrated that
   double-count per-cell, not as a worry but as a measurement.
2. **The base already owns the RPM axis.** The "reflect demand for that RPM" instinct is right about the
   physics and wrong about the bookkeeping: `idleActiveAirflow` is indexed on idle target, and §13.12
   showed 91 % of oil-pressure variance at hot idle *is* RPM. The correction does not need to carry it.
3. **Will's own objection is the sharpest form of it.** Ring/liner drag during warm-up rides
   chamber-and-liner surface temperature, which is **coolant-coupled** (R8 §7, Heywood) — so it belongs
   on the CLT axis. Oil pressure would pick the same term up because both fall together on a cold start.
   Two axes, one term.

**What gating costs:** the correction becomes blind to an unusually cold ambient — colder than the log
set's CLT-28 minimum. That is real, and the right place to fix it is the base's **0/15 °C columns**,
which R8 already flagged as extrapolated rather than measured. Fix it there; do not un-gate.
