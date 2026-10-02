# EMAP/MAP ratio and cam overlap — reversion, VVT scheduling, dynamic compression

> **Software page:** *VVT* (cam target map) + *Sensor setup → Back pressure*.
> Companions: [vvt.md](vvt.md) (MBT coupling), [valve_timing_dynamic_compression.md](valve_timing_dynamic_compression.md)
> (kinematics + DCR math), [boost.md](boost.md) (pre-turbine backpressure economics).
> Measurement tool: `skills/emu-black-emap-map-ratio/` (ratio table binned into veTable cells).
> **Channel status — corrected 2026-09-28: the sensor is alive.** `backpressureInput` = 205 is **`CAN Analog 6`** (CAN Switchboard), not ECU `Analog 6`: the 200-series indices are CAN analogs (`oilPressureInput` 204 = `CAN Analog 5`, r 0.999; `prethrottleBoostInput` 203 = `CAN Analog 4`; `customTemperatureInput1` 202 = `CAN Analog 3`). In `EMU_BLACK_V3\Supra\fullchannels.csv` (09-19 19:38) `Back pressure` tracks `CAN Analog 6` at r = 0.977 on pressurised samples, idles at 0.47 V (≈ 0 bar gauge) and reads 0.281 bar at MAP > 130 kPa. ECU `Analog 6` reading 0.000 V is just an unused pin. The earlier "no signal since 08-24" status (written 09-19) read the wrong channel; the hard 0.000 in idle-only logs (`whencold`, `losingit`) is atmospheric gauge rounding to zero, not a fault. The line damper can be judged from any log with a boost pull.

## 1. The ratio decides which way gas flows during overlap

During valve overlap the cylinder is briefly a passage connecting the exhaust
port to the intake port. Flow through that passage follows the pressure
difference across it; the overlap area/duration only scales *how much* flows.

**EMAP/MAP (both absolute) at the operating point:**

| ratio | direction | consequence |
|---|---|---|
| > 1 | exhaust → cylinder → intake (**reversion**) | internal EGR: hot residuals displace fresh charge AND heat the incoming charge. VE down twice — occupied volume + lower density. Burn slows (dilution). |
| ≈ 1 | little net flow | overlap nearly free; schedule cam by IVC effects alone |
| < 1 (**crossover**) | intake → cylinder → exhaust (**scavenging**) | residuals blown out, chamber and valves cooled, denser trapped charge. VE up, burn faster. Some short-circuited fresh charge (on port injection the fuel goes with it — EGT/lambda reads lean-ish at the sensor). |

More overlap simply multiplies whichever of these the pressure ratio has
selected — with a highly pressurized exhaust (ratio well above 1), more
overlap means proportionally more reversion. That premise holds exactly; the
flow scales roughly with overlap area·time and √ΔP (orifice flow).

Literature anchors (`corpus/`):
- Bell, *Maximum Boost*: "The street turbo, which is generally small, operates
  with exhaust manifold pressure somewhat higher than intake boost pressure.
  This situation, when presented with long-duration, high-overlap cams,
  creates a huge amount of reversion. Thus the 'turbo cam' tends to be a
  low-duration, very limited overlap cam." Judging turbine A/R "by the
  numbers" = measure turbine-inlet pressure and compare with boost. More TIP
  → more reversion → more chamber heat → lower charge density. The **crossover
  condition** (backpressure below boost) is where "power production takes on
  new dimensions."
- Heywood (`ice_fundamentals.md`): backflow of burned gases into the intake
  at low speed / high backpressure lowers VE; residual fraction rises with
  overlap and with p_exh/p_in.

## 2. Measurement status on this build (Supra) — MEASURED, 2026-07-10

Tune config: `backpressureInput = 205`, 2-point cal
(`backPressureCalBins`/`backPressureCal`), `backPressureFailSafe = 32`.

**Unit trap (cost a wrong conclusion once): the `Back pressure` log channel is
in BAR gauge, not kPa**, quantized at 1/32 bar ≈ 3.1 kPa/count. A boost pull
reads "1.1" — that's 110 kPa gauge. Read naively in kPa the channel looks
dead-flat; the tell is corr(Back pressure, MAP) ≈ 0.7–0.8 and band medians
rising monotonically with boost. The sensor has been live since at least
2026-04 (May and July logs agree within 0.03–0.08 per cell).

Measured table (12 logs, 2026-04 → 2026-07-10 incl. dedicated `bp1–3`;
122,360 running samples, 102/320 veTable cells at n≥20):
`supra/exports/emap_map_ratio_20260710_table.md` / `.csv`. Regenerate/extend:

```bash
python skills/emu-black-emap-map-ratio/scripts/emap_map_ratio.py \
  --tune "supra/exports/<latest>.xml.emub3" --out supra/exports/emap_ratio <logs...>
```

(Method: bar/kPa autodetect → liveness + corr(MAP) gate → gauge/absolute
autodetect → rolling-median despike → zero-phase Savitzky-Golay — exhaust
pulsation at firing frequency, 50–350 Hz on the I6, aliases hopelessly at
25 Hz sampling, so the cycle-mean is the only recoverable and the only needed
quantity → per-cell median. Self-test: MAP fed in as EMAP returns 1.00
everywhere. Validation 2026-07-10: steady-only medians (|dMAP/dt| < 30 kPa/s)
match all-sample medians within 0.03, so spool transients don't bias the
cells; ratio>1.05 outliers at MAP>140 concentrate at dMAP/dt ≈ +21 kPa/s —
spool spikes, real but transient.)

### Headline result — this turbine has crossover margin

| MAP (abs, kPa) | 108 | 123 | 137 | 152 | 167 | 181 |
|---|---|---|---|---|---|---|
| median EMAP/MAP | 1.03 | 1.00 | 0.93 | 0.91 | 0.91 | 0.83 |
| IQR | 0.19 | 0.21 | 0.19 | 0.13 | 0.14 | 0.10 |

Vacuum cells behave as constructed (EMAP_abs ≈ baro ⇒ ratio ≈ 100/MAP: ~2.7 at
35 kPa, ~1.3 at 79 kPa). Under boost the ratio crosses 1.0 at ≈ 120–130 kPa
MAP and keeps falling — **0.83 at 181 kPa**. Bell's crossover condition holds
at both boost targets (107 kPa gauge: ratio ≈ 1.0; 135 kPa: < 0.93).

Feasibility check (turbine power balance, first principles): compressor work
at PR 1.81, η_c 0.74 ≈ 75 kJ/kg; matching turbine work at η_t ≈ 0.62, EGT
~950 K needs turbine PR ≈ 1.44, i.e. pre-turbine ≈ 151–158 kPa abs with a free
exhaust ⇒ predicted ratio ≈ 0.86 at MAP 181 — measured 0.83. The measurement
is consistent with a pre-turbine tap and a generously sized turbine (matches
"boost dead flat to 7000").

### A falling ratio is NOT falling restriction

Absolute backpressure **rises** with boost — ~11 kPa gauge at MAP 108 up to
~50 kPa gauge at MAP 181. Only the *ratio* falls, because MAP rises faster
than EMAP. That is normal, not paradoxical, for a wastegated turbo with
margin:

1. **The wastegate caps turbine work.** Below target the gate is shut and all
   exhaust squeezes through the turbine (spool cells measured 1.1–1.25, spikes
   higher mid-transient). At target, excess flow bypasses — the turbine only
   takes the pressure drop needed to feed the compressor, the gate dumps the
   rest nearly free.
2. **Available exhaust energy grows faster than required compressor work.**
   Turbine power ∝ ṁ_exh·cp·T3·(1−PR_t^−0.248): as load rises, mass flow and
   EGT both climb, so the turbine PR needed per unit of compressor PR falls.
3. A large turbine A/R keeps its own PR low until approaching its flow limit.

So crossover here means *correctly sized with margin at the current targets* —
not globally "optimal." The same margin that buys crossover and a flat curve
costs transient spool (the 1.1–1.25 spool readings are that cost, visible).
Whether that trade is optimal depends on the goal; for a flat 450–500 ft-lb
street curve it is the right shape. Watch: no boost data above ~5700 rpm yet —
if the ratio climbs back toward 1 at redline/135 kPa, the turbine is running
out of margin exactly where EGT peaks.

### 2.1 Re-measure after the DBW boost-region rework (2026-07-18)

Single log, `backpressure measurement smooth.csv` (11,630 running samples, 57
cells at n≥20, only 374 samples above MAP 110 — thin in boost, so treat as a
confirmation pass, not a replacement for the 12-log 07-10 dataset). Plot:
`supra/notes/emap_map_ratio_20260718.png`.

| region (MAP abs) | 85–105 | 105–135 | 135–165 | ≥165 |
|---|---|---|---|---|
| median EMAP/MAP | 1.10 | 0.97 | 0.89 | 0.88 |
| median EMAP (abs) | 100 | 113 | 133 | 149 |

Crossover holds and sits **slightly lower than 07-10** at the bottom of boost
(0.97–0.98 near MAP 108–123 vs 1.00–1.03 before; 0.87–0.88 at 167 vs 0.91).
Direction is consistent with the DBW rework: holding a given MAP with a more
open throttle means the compressor supplies less of that MAP against less
throttle ΔP, so the turbine takes a smaller PR to get there. Magnitude
(~0.03–0.05) is at the edge of the 0.03–0.08 log-to-log agreement already
recorded above — real-looking, not yet separable from noise on one log.

**Floor artifact — do not over-read the vacuum columns.** The channel is gauge
and quantized 1/32 bar, so off-boost EMAP pins at exactly 100 kPa abs
(0 counts) in every region below MAP ~105. The left-side ratios (2.9 at MAP
35, 6.0 at MAP 20 overrun) are therefore `100/MAP` by construction with ±3.1
kPa of unresolvable headroom, not a resolved measurement of EMAP.

### 2.1b Crossover is LOST above ~6000 rpm (2026-07-19) — resolves the §2 open item

`boost0719.csv` (23,617 samples, 24 boost events, 1,251 above MAP 105 — the
first log with real top-end boost coverage). Plot:
`supra/notes/emap_map_ratio_20260719.png`. Band medians confirm 07-10/07-18
(0.97 at 105–135, 0.90 at 135–165, 0.87 above 165), but pooled by RPM at
MAP>140:

| RPM | 4000–4800 | 4800–5400 | 5400–6000 | **6000–7100** |
|---|---|---|---|---|
| ratio | 0.88 | 0.87 | 0.90 | **1.04** |
| n | 172 | 159 | 83 | 42 |

§2 said to watch for exactly this ("if the ratio climbs back toward 1 at
redline/135 kPa, the turbine is running out of margin exactly where EGT
peaks"). It does. Peak EMAP 183 kPa abs at MAP 173.

**Transient artifact ruled out.** The obvious confound is lift-off (MAP
collapses fast, EMAP lags high). All three cuts of the RPM≥6000 boost samples
agree: steady |dMAP/dt|<30 kPa/s → 1.01, rising-RPM → 1.05, fast-falling →
1.02, across 6 independent events.

**Strength:** n=42 pooled; no individual veTable cell up there reaches n≥20,
so the binned table's top rows stay blank and this finding lives only in the
pooled band. Needs deliberate top-gear pulls held past 6000 to firm up.

**Consequence for `cam1AdvTbl`:** the §8 proposal schedules the top-RPM boost
cells on the assumption of crossover. That assumption fails above ~6000. Cut
advance (overlap) in the >6000 boost columns until the extra pulls confirm or
overturn — reversion there lands where EGT peaks and knock margin is thinnest.

### 2.2 What drives the ratio UP (the inverse of §2's argument)

§2 explains why a *falling* ratio isn't falling restriction. The mirror
question — "is a high ratio just an unwastegated turbine at choke?" — is a
common and only partly-right framing. Both named conditions do raise the
ratio, but they are special cases.

Turbine PR follows from the power balance:

```
ṁ_c·cp_a·T1/η_c·(PR_c^0.286 − 1)  =  ṁ_t·cp_e·T3·η_t·(1 − PR_t^−0.248)
```

Solving for PR_t, the ratio rises with: (1) **turbine flow capacity too small
for the mass flow** — dominant, and it bites well before choke; (2) **η_t off
peak** (bad U/C blade-speed ratio — a small turbine at high flow is off-peak
*and* near choke, which is why the two get conflated); (3) **low T3** — less
available energy per unit mass; (4) **high compressor demand** (PR_c up, η_c
down). Choke is the asymptote of (1): flow goes insensitive to PR, so EMAP
climbs steeply for nothing.

**Wastegate framing must be inverted.** The gate is a *parallel flow path*,
not an EMAP reducer:

- Gate shut is **normal below target**, not a fault — every spool event runs
  all flow through the turbine. That is exactly where this build's ratio is
  worst (spool 1.1–1.25 vs 0.88 at target). Nothing wrong there.
- Gate open does **not** guarantee low EMAP. An undersized gate port/valve is
  itself the restriction at high flow — that is boost creep, presenting as
  high EMAP with the gate commanded fully open. What matters is total
  effective flow area at the turbine inlet (turbine + gate) vs mass flow.

**Keep two distinct problems separate:** the *ratio* governs gas direction
during overlap (reversion vs scavenge — the cam question); *absolute* EMAP
governs pumping work (PMEP, piston pushing against backpressure on the
exhaust stroke) regardless of ratio. On this build absolute EMAP rises with
boost (~13 kPa gauge at MAP 117 → ~49 at MAP 168) while the ratio falls.
Both true, no contradiction.

Bell anchors (`corpus/maximum_boost.md`): judging A/R "requires measurement of
exhaust manifold pressure, or turbine inlet pressure, and comparison with
boost pressure"; too-small A/R shows as "fading power in the upper third of
the engine's rev range"; and the cost chain is explicit — more turbine inlet
pressure "creates more reversion, which creates more combustion chamber heat,
which reduces charge densities."

## 3. The single-phaser coupling: one knob moves two things

VVT-i phases the **intake cam only** (this build: `cam2AdvTbl` all zeros,
`vvtCam1MaxAdvance = 25` crank°). Cams are **Brian Crower BC0311 Stage 2**
(card on file, 2026-07-10): 264°/264° advertised, 218°/218° @0.050″, lift
8.74 mm both, **ICL 110° / ECL 118° / LSA 114°**, at the phaser's parked
(0-advance) position. That pins the event math exactly:

|  | advertised (seat) | @0.050″ lift |
|---|---|---|
| IVO | 22° BTDC + A | 1° ATDC − A |
| IVC | 62° ABDC − A | 39° ABDC − A |
| EVC (fixed) | 14° ATDC | 9° BTDC |
| **overlap(A)** | **36 + A** | **A − 10** |

Two traps this table kills:
- **Overlap is set by IVO and EVC** (the TDC-side events), *not* IVC and EVO
  (the BDC-side events, 39° ABDC / 47° BBDC on the card — adding those gives a
  meaningless 86°).
- **At 0.050″ lift these cams have a 10° overlap *gap* at 0 advance** — high-
  lift overlap doesn't exist until 10° of advance, and maxes at +10° at full
  table advance (20°). The scary-sounding 36–56° advertised overlap is
  seat-to-seat, where flow area is tiny. Effective overlap on this build is
  mild, which is why 38.5° advertised overlap idles fine and why adding
  advance under crossover boost is a measured lever, not a cliff.

Advancing the intake cam by A crank degrees does **both, always, in fixed
proportion**:

- **Overlap +A** (IVO earlier against a fixed EVC) → more of whatever §1 says
  the pressure ratio has selected.
- **IVC −A** (earlier, less ABDC) → less low-rpm give-back → more trapped
  charge at low speed → higher dynamic compression. At high rpm ram/inertia
  filling reverses the sign (late IVC fills better up top).

You cannot buy the IVC benefit without paying (or collecting) the overlap
consequence. The EMAP/MAP table is what tells you, cell by cell, whether the
overlap term is a cost or a rebate.

### Stock-equivalence: half the advance ≈ the same total overlap

The BC0311s moved the overlap *baseline*, so advance numbers can't be
compared to stock directly. Stock-ish 2JZ intake (~233° adv, ICL ~115 —
approximate, from the GTE figures in
[piston_valve_clearance_cam_advance.md](piston_valve_clearance_cam_advance.md);
GE-VVTi stock card not on file) parks at roughly **5–10° advertised
overlap**; the BC0311 parks at **36°**. OEM VVT-i schedules commonly peak
around **35–45° crank** of advance in mid-rpm part load (external/model
knowledge, unverified) → stock max *total* overlap ≈ **40–55°**. This build's
20° table peak → 36 + 20 = **56°**. So: **~half the advance, but the same
maximum total overlap as a stock schedule — the cams pre-spent the other
half.** For the internal-EGR/cruise role of advance, total overlap is the
operative quantity; the half-size advance table is not conservative, it's
equivalent.

The IVC side does *not* cancel the same way: the 264s park IVC at 62° ABDC
vs stock ≈ 51° — later, trading low-rpm trapping for top-end breathing. At
max advance stock reaches IVC ≈ 8–16° ABDC (DCR near static — affordable
only at NA part load); this build's 20° reaches IVC 42° (DCR 9.15) at real
boost pressures. Same advance-number logic, entirely different cylinder
pressures — which is why the advance ceiling here is set by knock data under
boost, not by copying NA-style schedules.

## 4. Scheduling rules keyed to the measured ratio

Per veTable cell, once the ratio table exists:

| measured EMAP/MAP | overlap term | scheduling rule for intake advance |
|---|---|---|
| vacuum cells (MAP < baro; EMAP ≈ baro ⇒ ratio > 1 by construction) | mild reversion = internal EGR | Moderate advance is *useful dilution*: residuals are free filler gas → same fresh charge at wider throttle/shallower vacuum → less pumping work (dominant), plus cooler peak temps → less wall heat loss (second-order). Fuel saved is the outcome, not the mechanism. Spark must re-phase for the slower burn (MBT toward more advance, [vvt.md](vvt.md) V1) or the gain is thrown away as late combustion. Bounded by the dilution cliff (burn-stability scatter). Idle and near-idle want minimum overlap (residuals destabilize the already-slow idle burn — this is why `cam1AdvTbl` floors to 0–2.5° at 1000 rpm). |
| ~0.9–1.1 under boost | near-neutral | Overlap ~free; set advance for IVC/trapping via the MAP-peak street sweep (`emu-black-vvti-street-tune`). Spool cells: earlier IVC + scavenge margin both help — this is where max advance belongs. |
| > ~1.1–1.2 under boost | reversion, scaling with overlap | Taper advance toward the floor. Hot-residual charge heating raises knock tendency and EGT; VE falls; more boost to compensate raises TIP further (Bell's "chasing one's tail"). |
| < ~0.9 under boost (crossover) | scavenging | Advance pays twice (scavenge + trap) — but cap by piston-valve clearance ([piston_valve_clearance_cam_advance.md](piston_valve_clearance_cam_advance.md)) and port-injection short-circuit fuel loss. Verify with MAP-peak sweep, not open-loop faith. |

**Applied to the measured table (2026-07-10):** the reversion-defensive taper
in `cam1AdvTbl` (advance → 2.5° by 118–130 kPa) is defending against a
condition this turbine does not have. Measured ratio ≈ 1.0 at 108–123 kPa and
0.83–0.93 at 137–181 kPa — the boost columns are *scavenge* territory, where
overlap pays. The 20° island can extend right into the boost columns, gated
by: (a) piston-valve clearance
([piston_valve_clearance_cam_advance.md](piston_valve_clearance_cam_advance.md)),
(b) short-circuited port-injected fuel polluting the WBO during high overlap
(anchor on EGT/plugs, don't chase the lambda reading), (c) DCR rise on
low-ethanol fills (§6), and (d) the `vvtiMapBins10` axis ceiling at 130 kPa —
extend the axis first or the 107 and 135 kPa targets share one column.
Verify each extended cell with the MAP-peak sweep (`emu-black-vvti-street-tune`).

## 5. VE consequences (fuel side)

The EMU VE table is a fuel-dose proxy indexed on MAP×RPM — cam position is
*inside* the number, not a separate axis. Where scheduled advance changes:

- **Reversion cells (ratio > 1)**: more advance → residuals displace fresh
  charge → true trapped air *falls* → VE table value must fall. The charge
  also arrives hotter (density − ; knock +).
- **Scavenge cells (ratio < 1)**: more advance → VE value must rise; part of
  the injected fuel may short-circuit during overlap (reads lean at the WBO
  while the cylinder is not actually lean — don't chase it with global fuel).
- **Low-rpm cells**: earlier IVC raises trapped charge quasi-statically —
  ≈ +2.5–3 VE points per 5° advance on this geometry (see §6) — independent
  of the overlap term.

After any cam-table change, re-correct the affected VE cells from closed-loop
STFT (existing flow: `emu-black-ve-from-log`, gates per `emu-black-log`).

## 6. Dynamic compression / knock (this build's numbers)

Geometry: 86×86 mm, rod 142 mm, SCR 10.0, 264° intake duration. Cam card
(BC0311) pins base ICL at **110°** — the ICL-110 column below is the live one
(advertised-IVC convention; the 0.050″ convention, IVC 39−A, gives DCR ≈ 9.3
at 0 advance — true effective compression sits between, since near-seat flow
is small).

DCR = V(θ_IVC)/Vc (math in [valve_timing_dynamic_compression.md](valve_timing_dynamic_compression.md)):

| advance (crank°) | IVC shift | DCR @ base ICL 110 | DCR @ base ICL 120 | trapped V_IVC/V_BDC (ICL 110) |
|---|---|---|---|---|
| 0 | — | 8.15 | 7.52 | 0.815 |
| 5 | −5° | 8.44 | 7.85 | 0.844 |
| 10 | −10° | 8.70 | 8.15 | 0.870 |
| 15 | −15° | 8.94 | 8.44 | 0.894 |
| 20 | −20° | 9.15 | 8.70 | 0.915 |
| 25 | −25° | 9.34 | 8.94 | 0.934 |

Robust slopes: **+0.25–0.30 DCR and +2.5–3 % trapped charge per 5° advance**;
full 25° authority ≈ **+1.2 DCR — about a full point of compression** at
whatever cells carry high advance. Compression-pressure proxy (∝DCR^1.3):
+4–6 % per 5°.

**Filler gas vs DCR:** residuals do NOT change the geometric DCR (a volume
ratio, set by IVC alone). They change the compression *starting conditions*:
P_IVC rises with the dilution-driven MAP rise (the pumping-relief win seen
from inside the cylinder), and T_IVC rises because hot residuals blend into
the fresh charge (10–20% residual fraction is a meaningful temperature bump,
slightly offset by the burned gas's lower γ). At cruise pressures this is
knock-irrelevant and pure efficiency; under boost the same T_IVC rise is
exactly why reversion is knock-hostile and why internal EGR ≠ cooled external
EGR for knock.

Knock reading:
- High-advance cells are the high-DCR cells. On E60 the margin is large, but
  the flex axis means the same cam table runs on low-ethanol fills — the
  pump-gas ignition table (Table 1) must respect the DCR at the *advanced*
  cam position, not the parked one.
- Reversion (ratio > 1) adds **hot** residuals: charge temperature rises even
  as dilution slows the burn. Under boost the heating term dominates → knock
  and EGT worsen. Scavenging (< 1) removes hot residuals and cools valves →
  knock margin improves. So the EMAP/MAP table is *also* a knock-risk map:
  cells with ratio > 1 and high advance are compounding risks (high DCR + hot
  charge). On this build the measured boost cells sit at 0.83–1.0 (§2), so
  added overlap there *cools* the residual load and partially offsets the DCR
  penalty of the same advance — but only the knock channels can confirm the
  net, especially on low-ethanol fills.
- Where the schedule reduces advance as boost rises (the 20° island falling to
  2.5° by 130 kPa), DCR falls as cylinder pressure rises — partially
  self-compensating for knock, at the cost of low-end trapping.

## 7. Current `cam1AdvTbl` snapshot (2026-06-29 export, 0.5°/count verified)

Advance in crank°, RPM up, MAP right (axes `vvtiRpmBins10` × `vvtiMapBins10` —
note the MAP axis tops out at **130 kPa**; above that the last column rides):

| RPM \ MAP | 20 | 32 | 44 | 57 | 69 | 81 | 93 | 106 | 118 | 130 |
|---|---|---|---|---|---|---|---|---|---|---|
| **7000** | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 |
| **6333** | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 |
| **5667** | 6.5 | 6.5 | 6.5 | 6.5 | 6.5 | 6.5 | 6.5 | 5.0 | 4.0 | 2.5 |
| **5000** | 10.0 | 10.0 | 10.5 | 10.5 | 11.0 | 11.0 | 11.0 | 8.0 | 5.0 | 2.5 |
| **4333** | 14.0 | 14.0 | 14.5 | 14.5 | 15.0 | 15.0 | 15.0 | 10.5 | 6.5 | 2.5 |
| **3667** | 15.5 | 16.0 | 16.5 | 17.0 | 17.5 | 18.0 | 18.5 | 13.0 | 7.5 | 2.5 |
| **3000** | 13.5 | 14.0 | 14.5 | 16.0 | 18.0 | 20.0 | 20.0 | 14.5 | 8.5 | 2.5 |
| **2333** | 8.5 | 8.5 | 9.0 | 12.0 | 16.0 | 19.5 | 20.0 | 15.0 | 9.0 | 2.5 |
| **1667** | 2.5 | 2.5 | 2.5 | 2.5 | 9.5 | 11.0 | 12.5 | 9.0 | 6.0 | 2.5 |
| **1000** | 2.5 | 2.5 | 2.5 | 2.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

**Provenance (Will, 2026-07-10): this table was copied from another,
similar car and has never been verified on this engine — the cruise region
in particular is a guess, no sweeps run.** Its *shape* passes the physics
smell test (advance floors at idle and redline, 20° island at 2333–3000 rpm ×
81–93 kPa, boost taper), so it's a reasonable prior — but no cell-level
optimum in the vacuum region should be cited as validated.

The 2026-07-10 EMAP measurement shows the right-hand taper was built on an
assumption (EMAP ≫ MAP under boost) that is **false for this turbine** — the
boost columns measured 0.83–1.0. The island's right boundary should move
right, per §4. Status by region: **boost columns = measured basis (EMAP
ratio); vacuum/cruise columns = unverified copy, pending MAP-peak sweeps**
(`emu-black-vvti-street-tune`, cruise band first: MAP 40–80, RPM 2000–3500).

## 8. Proposed table (2026-07-10) — crossover-informed boost columns

> **Units: all cam-table values, card events, overlap and advance figures in
> this note are CRANK degrees.** Verified 2026-07-10, four independent ways:
> (1) EMU help (`docs/emu-black-help/VVT.md`): the log channels are "the angle
> of the camshaft **relative to the crankshaft**" — measured on the ECU's
> crank-angle clock; (2) magnitude physics: the street-swept cruise optimum of
> 18–20 units read as crank° gives IVC 42–44° ABDC, DCR ≈ 9.1, overlap ≈ 56°
> advertised — textbook street-turbo numbers; read as cam° it would mean
> 36–40 crank°, DCR ≈ 10, 72–76° overlap at part throttle — not a drivable
> calibration; (3) the logged PID overshoot to 27.5 units *past* a 19.5
> target requires free travel beyond 27.5 — fine within a ~60-crank°-stop
> phaser, impossible if units were cam° (27.5 cam = 55 crank, at the stop);
> (4) the standing note in
> [valve_timing_dynamic_compression.md](valve_timing_dynamic_compression.md);
> (5) ECUMaster's official EMU Black V3 Software Guide (p. 55): scope pulse
> angles — the frame cam position is measured in — run **0–720°, the full
> crank cycle** (a cam-degree frame would be 0–360), and this tune's
> `vvtCam1TriggerOffset = 417` only fits that 720° frame; (6) ECUMaster USA's
> official VVT-setup video uses Max advance = 30 — as crank° that's a
> conservative half-authority cap (like this tune's 25), whereas as cam° it
> would sit exactly on the mechanical stop, which no PID ceiling should do.
> Conversion: crank° = 2 × cam°; 20° crank = 10° cam.
>
> **Cap vs authority:** `vvtCam1MaxAdvance = 25` is a *configured ceiling*,
> not the phaser's mechanical stop. The 2JZ-GE VVT-i phaser is commonly
> quoted at ~60° crank (30° cam) total travel (external figure, unverified on
> this unit; logged travel proves ≥ 27.5° crank). Hypothetically the table
> could command toward 60° crank — but three walls arrive first: P-V
> clearance shrinks ~0.09–0.10 mm per crank° of advance with unmeasured
> GE-piston reliefs (27.5° is the demonstrated-safe envelope), DCR reaches
> ~SCR (≈10) as IVC approaches BDC… i.e. ~2° ABDC at 60°, and advertised
> overlap would hit 96°. The 20–25° region is the sane calibration space.

**Superseded 2026-07-10 (same day) by §8.1** — the axis-extension version
below is the one to import. First iteration (old 130-kPa-top axis), kept for
history: `supra/exports/VVTI - cam1AdvTbl intake advance [deg]
(crossover-informed proposal 20260710).emubt`. **Only the 106/118/130 columns
move** (21 cells): the vacuum region is held as-is — not because it is
validated (it is a copied, unverified table, see §7) but because replacing
one guess with another has no basis; it awaits MAP-peak sweeps. Idle row and
6333/7000 rows unchanged (no boost EMAP data above ~5700 rpm; late IVC is
preferred near redline anyway).

| RPM \ MAP | 20 | 32 | 44 | 57 | 69 | 81 | 93 | 106 | 118 | 130 |
|---|---|---|---|---|---|---|---|---|---|---|
| **7000** | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 |
| **6333** | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 |
| **5667** | 6.5 | 6.5 | 6.5 | 6.5 | 6.5 | 6.5 | 6.5 | **6.5** | **6.0** | **6.0** |
| **5000** | 10.0 | 10.0 | 10.5 | 10.5 | 11.0 | 11.0 | 11.0 | **10.0** | **10.0** | **10.0** |
| **4333** | 14.0 | 14.0 | 14.5 | 14.5 | 15.0 | 15.0 | 15.0 | **14.0** | **13.0** | **13.0** |
| **3667** | 15.5 | 16.0 | 16.5 | 17.0 | 17.5 | 18.0 | 18.5 | **16.0** | **15.0** | **15.0** |
| **3000** | 13.5 | 14.0 | 14.5 | 16.0 | 18.0 | 20.0 | 20.0 | **18.0** | **16.0** | **16.0** |
| **2333** | 8.5 | 8.5 | 9.0 | 12.0 | 16.0 | 19.5 | 20.0 | **18.0** | **16.0** | **16.0** |
| **1667** | 2.5 | 2.5 | 2.5 | 2.5 | 9.5 | 11.0 | 12.5 | **12.0** | **12.0** | **12.0** |
| **1000** | 2.5 | 2.5 | 2.5 | 2.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

Design constraints honored: max 20° (already exercised by the current table;
logged transient overshoot to 27.5° with no contact — P-V envelope
demonstrated, though GE-piston K is still unmeasured, see
[piston_valve_clearance_cam_advance.md](piston_valve_clearance_cam_advance.md));
each column a smooth arch in RPM; boost-column advance follows the measured
ratio (≈1.0 at 106–123 → carry island advance; <0.93 beyond → scavenge, but
the 130 column also serves everything above 130 kPa where data ends at 181,
so it stays 3–4° below the island rather than matching it).

### 8.1 Extended-axis version (the one to import)

New `vvtiMapBins10`: **20 35 49 64 79 93 108 152 196 240** — all exact
veTable mapBins values (ratio table / VE / sweep cells share column centers);
196 ≈ 3rd-gear target (207 abs), 240 covers the 4th-gear target (235 abs);
152 sits in the best-measured crossover cell (ratio 0.91). Bundle with the
re-mapped table (axis edits do NOT move table values — import both together):
`supra/exports/VVTI - vvtiMapBins10 + cam1AdvTbl (extended axis proposal
20260710).emubt`.

Proposed `cam1AdvTbl` on the new axis (°crank; vacuum columns = current table
resampled, unchanged by design):

| RPM \ MAP | 20 | 35 | 49 | 64 | 79 | 93 | 108 | 152 | 196 | 240 |
|---|---|---|---|---|---|---|---|---|---|---|
| **7000** | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 |
| **6333** | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 |
| **5667** | 6.5 | 6.5 | 6.5 | 6.5 | 6.5 | 6.5 | 6.5 | 6.0 | 5.5 | 5.0 |
| **5000** | 10.0 | 10.0 | 10.5 | 11.0 | 11.0 | 11.0 | 10.0 | 10.0 | 9.0 | 8.0 |
| **4333** | 14.0 | 14.0 | 14.5 | 15.0 | 15.0 | 15.0 | 14.0 | 13.5 | 12.0 | 11.0 |
| **3667** | 15.5 | 16.0 | 16.5 | 17.5 | 18.0 | 18.5 | 16.0 | 15.5 | 14.0 | 12.0 |
| **3000** | 13.5 | 14.0 | 15.0 | 17.0 | 19.5 | 20.0 | 18.0 | 17.0 | 15.0 | 13.0 |
| **2333** | 8.5 | 8.5 | 10.0 | 14.5 | 19.0 | 20.0 | 18.0 | 17.0 | 15.0 | 12.0 |
| **1667** | 2.5 | 2.5 | 2.5 | 6.5 | 11.0 | 12.5 | 12.0 | 12.0 | 10.0 | 8.0 |
| **1000** | 2.5 | 2.5 | 2.5 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

Delta vs the current calibration's *effective* command at the same MAP points
(current table interpolated, clamped above 130 — its real behavior today):

| RPM \ MAP | ≤93 | 108 | 152 | 196 | 240 |
|---|---|---|---|---|---|
| **7000–6333** | 0 | 0 | 0 | 0 | 0 |
| **5667** | 0 | +1.5 | +3.5 | +3.0 | +2.5 |
| **5000** | 0 | +2.5 | +7.5 | +6.5 | +5.5 |
| **4333** | 0 | +4.0 | +11.0 | +9.5 | +8.5 |
| **3667** | 0 | +4.0 | +13.0 | +11.5 | +9.5 |
| **3000** | 0 | +4.5 | +14.5 | +12.5 | +10.5 |
| **2333** | 0 | +4.0 | +14.5 | +12.5 | +9.5 |
| **1667** | 0 | +3.5 | +9.5 | +7.5 | +5.5 |
| **1000** | 0 | 0 | 0 | 0 | 0 |

The big +13…+14.5° deltas at 152 kPa are against the old clamped 2.5° floor —
that column is where the measured crossover (0.91) says the old
reversion-defense was most wrong. 196/240 taper 2–4° below 152 on thin/no
data + peak EGT + pump-fill DCR exposure.

### Calibration history that bounds this proposal (Will, 2026-07-10)

1. **Phantom cells.** The turbo cannot reach the high-MAP columns below
   ~2900 rpm — the log data confirms it (boost cells populate from 2895 rpm;
   ≥137 kPa only from ~3900 rpm). The 1667–2333 × 152–240 cells are never
   dwelled in; their values exist for interpolation smoothness on transients
   only. Keep them smooth; don't tune them.
2. **Knock history at 5000–6000 rpm under boost.** An earlier map ran more
   cam advance there; it knocked; Will pulled the advance back attributing it
   to reversion. **The measured ratio contradicts the reversion attribution**
   (0.83–0.93 at 152–181 kPa, 5289–5632 rpm — outflow, not backflow;
   unmeasured above 5632, extrapolation labeled as such). The knock is fully
   explained without reversion, by three compounding effects of advance at
   high load ([vvt.md](vvt.md) V1):
   - earlier IVC → higher DCR (+0.25–0.3 per 5°) and more trapped mass →
     higher peak pressure/temperature;
   - scavenging strips residual dilution → faster burn → knock-limited spark
     moves DOWN — with the ignition table unchanged, effective timing became
     over-advanced relative to the new limit;
   - if VE wasn't recorrected after the cam change, more trapped air on the
     same dose ran the cells lean.
   Pulling cam advance was a *valid symptom fix* that paid for knock margin
   with airflow. The alternative — keep the advance, remove 1–3° of spark in
   those cells, recorrect VE — likely nets more torque at equal knock margin;
   A-B it. Flex-fuel confound: note the ethanol content of the tank when that
   knock occurred; Table 2 high-load timing was also being advanced in the
   same era (two levers moving at once).
3. **Rollout implication**: stage it. Rows 3000–4333 (strongest EMAP data, no
   knock history) can take the proposed columns as-is. Rows 5000–5667 are the
   knock-history rows — apply their increases only together with an ignition
   pre-pull (1–3°) in the same cells, per-cyl knock voltage watched, ethanol
   content known.
4. **Knock-limited accounting (2026-07-10): the chain terminates — fuel is
   never removed.** Cam advance → air ↑ → VE ↑ (fuel follows air to hold
   lambda; STFT finds it). Knock → spark ↓ only. Spark doesn't change trapped
   air, so the VE stays; removing fuel after retard would lean a knock-limited
   cell (rich-of-stoich fuel is a knock suppressant + EGT armor) — never do
   it. Per-cell decision: torque from +air vs torque from −spark; net ≤ 0 →
   revert that cell. No cascade.
5. **Flex constraint / possible exit**: `tblsCAM1 = 0` in the tune — ONE cam
   table serves all fills (while tblsVE/IGN/Lambda = 253, flex-blended), so
   boost-region advance must respect the worst tank. The switching hook
   exists; **verify in the EMU software whether CAM1 gets a second
   switchable/blendable table** — if yes, scavenge-informed boost advance can
   live on the ethanol side only, like the two ignition tables, dissolving
   the knock-limited objection.
6. **Boost-tolerance design rule (Will's constraint, 2026-07-10): knock
   margin must not depend on tight boost control.** The wastegate is the
   slowest, most hysteretic loop in the system; spark is cycle-fast, cam
   ~100 ms. Encode robustness in the MAP axis: cam columns above target
   (196/240) keep a monotone downward advance gradient (overshoot →
   automatically less advance), the spark table's high-MAP rows carry the
   overshoot margin sized for the worst fill (spark outruns any spike; cam
   can't), per-cyl knock retard is backstop only, and the boost PID is never
   tightened for knock's sake. Criterion for the staged cells: knock-free at
   target + real overshoot band at scheduled spark — not merely at target.
   Cost: a degree or two of peak-cell cam/spark at exactly-target boost.

**Verification expectations after flashing:**
- **Natural-experiment result (2026-07-10), cold-inhibit vs hot:** below
  CLT 88 the VVT is inhibited and the cam parks at ≈ −2° while hot it tracks
  the table — a free 0°-vs-commanded A/B. Mining five full logs at steady
  cruise (matched RPM×TPS cells, |ΔMAP|<4 kPa over 0.5 s, moving): hot/
  advanced runs **+2 to +3 kPa more MAP at the same TPS/RPM** (pooled, cam
  Δ 8–11°; within-log paired cells in the 0613 log: +2.0 kPa at cam Δ
  14–17°). Direction confirms the dilution/pumping-relief mechanism (§ test
  logic): ~3% relief on a ~60 kPa vacuum depth. Confounds bounded: TB
  thermal growth < ~0.5 kPa (same sign), IAT Δ ≈ 3 °C negligible;
  within-log pairing removes baro/ethanol. PW channel unusable for this
  (flex fills differ across logs, cold runs open-loop — STFT pinned 0, and
  PW scales with the MAP shift itself). **This confirms the copied table's
  advance is doing the intended thing at cruise — it does not locate the
  optimum.** Only the sweep does:
- **Step 0 — sweep the cruise band** (the copied, unverified region): the
  override protocol in `emu-black-vvti-street-tune`, cruise band first (MAP
  40–80 × 2000–3500 — the highest-mileage cells). **Cruise ranking signal =
  minimum injector PW at fixed speed** (economy objective; expect the winner
  at *higher* MAP/TPS — pumping-loss relief), bounded by combustion
  stability; MAP-peak ranking applies only to boost cells. Every corrected
  cam cell then wants its ignition cell re-swept (dilution slows the burn →
  MBT toward MORE advance, [vvt.md](vvt.md) V1/V2) and its VE cell
  recorrected from STFT.
  **Sweep log channel list** (exact EMU names): TIME, RPM, TPS, PPS, Gear,
  Driven axle speed, VVT CAM1 angle / angle target / solenoid DC / status,
  Engine oil pressure, CLT, IAT, Charge temp, Baro, Idle state, Warmup
  enrichment, Afterstart Enrichment · Injectors PW, Battery voltage, Fuel
  pressure, Effective fuel pressure, Fuel pressure correction, Lambda 1,
  Lambda target, Lambda is valid, Short term trim, Ethanol content, MAP,
  EGT 1, EGT 2 · Knock voltage peak cyl 1–6, Ignition Angle, Ignition From
  Table. Ranking = min (PW − deadtime) at fixed speed/gear (fuel = BSFC
  proxy; road load fixes torque, so efficiency shows in fuel, not MAP). MAP
  attributes mechanism only: at fixed TPS, MAP↑+PW↓ = dilution/pumping
  relief; MAP↓+PW↑ = fresh trapping. (Fixed-orifice reminder: lower MAP at
  fixed TPS = MORE flow, not less.) Cells to sweep first: the measured
  cruise cells 2400–2800 rpm / TPS 10–10.5% / MAP 38–45.
- **Open-wastegate cells (vacuum + spool)**: deeper MAP at same TPS/RPM =
  confirmation (MAP-peak method). This is the direct signal.
- **Cells at governed boost target**: the boost PID hides the MAP gain — look
  for **lower Boost DC at target, faster time-to-target, higher turboshaft
  speed at the same boost** instead of higher MAP.
- **Fuel**: scavenge/trapping gains raise true VE in the changed cells —
  expect lean STFT there and re-correct VE (`emu-black-ve-from-log`); during
  high overlap the WBO also reads short-circuited charge, so anchor on
  EGT/plugs before believing large lambda shifts.
- **Knock**: changed cells gain +0.25–0.3 DCR per 5° added — E60 has margin,
  low-ethanol fills lean on conservative Table 1; watch per-cyl knock voltage
  on the first pump-gas tank.

## Open items

1. ~~Get the backpressure sensor reading~~ — **done 2026-07-10**: sensor was
   alive all along; log channel is in bar (§2).
2. ~~Pull the cam card~~ — **done 2026-07-10**: BC0311, ICL 110 / ECL 118 /
   LSA 114 (§3); DCR column pinned (§6).
3. Extend `vvtiMapBins10` above 130 kPa so the 107 and 135 kPa boost targets
   get distinct cam cells before scheduling overlap there.
   **Not a defect — a deliberate resolution choice (Will, 2026-07-19.)** The
   130 column already applies to every point above 130 kPa, so it *is* the
   boost schedule; extending the axis only buys resolution *across* boost
   levels. Will will move it when he wants resolution there. The 2.5° sitting
   in those columns is an unmapped region, not a misconfiguration — do not
   re-flag it as one. Separately: the cruise high-advance block (MAP 69–93,
   2333–4333 rpm) is never entered under boost; keep cruise-dilution strategy
   out of boost/turbo-sizing analysis.
   **Unverified:** `cam1AdvTbl`'s X axis is *assumed* to be `vvtiMapBins10`
   (MAP). `vvtiTPSBins10` (0–100) also exists and no axis selector was found
   in the tune or `docs/emu-black-help/VVT.md`. Confirm in EMU before trusting
   any column labelling in §7/§8.
4. Confirm the sensor tap location is pre-turbine (the power-balance check in
   §2 says the numbers are consistent with pre-turbine; a post-turbine tap
   would make the crossover reading trivial and the §4 conclusions void).
5. ~~High-RPM rows (>5700) have no boost samples yet~~ — **partially done
   2026-07-19** (§2.1b): 42 pooled samples at RPM≥6000/MAP>140 show the ratio
   back at ~1.04, i.e. crossover lost at redline. Still below per-cell n≥20;
   log 2–3 deliberate top-gear pulls held past 6000 to firm it up. **Do not
   extend advance above ~5300 rpm until then** — the §8 proposal assumes
   crossover that the data says isn't there.
6. Lambda vs target under boost (2026-07-19, `boost0719.csv`): running rich of
   target by 5.2% median, but the error thins monotonically with RPM (−9.5% at
   3500–4500 → +1.6% at 5500–7100) — a `veTable` RPM-slope issue, not an
   offset. Cannot yet attribute any of it to the DBW boost-region rework: the
   two pre-rework logs disagree by more than the pre/post difference (n=24 and
   n=38), and `boost0719.csv` lacks `Ethanol content` on a flex-fuel car. Add
   `Ethanol content` + `Short term trim` to the logged channel set.
7. Boost runs ~13 kPa under target at steady high load (67 vs 77) with
   `Boost DC` 43% median / 90% peak — not saturated, so unused PID authority,
   not a wastegate flow limit. Bears on §2.2: the measured ratios are at
   *actual* boost, below what the targets ask for.
