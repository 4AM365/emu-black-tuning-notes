# CLT signal noise — source, mechanism, and what actually fixes it

Analysis 2026-09-22. Log: `EMU_BLACK_V3\Supra\fullchannels.csv` (2026-09-19 19:38, 48 064 samples
@ 25 Hz, 1943 s). Calibration in force: `supra/tunes/supra export 09192026 post-tb-clean.xml.emub3`
(19:29, the export immediately preceding the log). All 564 channels scanned (§6); the argument rests on `CLT Voltage`, `IAT Voltage`,
`CAN Analog 5`, `Analog 5`, `PPS Voltage`, `CLT status`, `Coolant fan`, `RPM`, `MAP`.

---

> **Update 2026-09-28 (Will):** CLT and IAT were grounded to the **block**, not B29, which confirms the local-engine-ground reading in §1e. Both are being rewired to sensor ground. Re-log hot and re-run the §6 noise scan to verify.

> **Update 2026-09-29 — the rewire worked.** Hot re-log `allchannels_smoothclt.csv` (1263 s, CLT ≥ 92 for 770 s), same §6 method: `CLT Voltage` amp 1.58 → **0.12 quanta**, p99.9 0.177 → **0.020 V**, spikes ≥ 3 LSB 1–4 % hot → **0.00 %**; `IAT Voltage` 1.65 → 0.15 quanta, p99.9 0.098 → 0.020 V; hot-window mean |residual| 0.0218 → 0.0003 V; engine-off amp 0.00. Only 1-LSB code-boundary dither remains (1.4 % of CLT samples). CLT↔IAT residual correlation is still 0.05 — the "should become correlated" prediction in §4.4 did **not** appear, because there is now essentially no common disturbance left to correlate. **Not fixed:** §2 — the CLT table still reads 96 over 0.529–0.569 V (0.588 V → 94–96), so `CLT` sat at exactly 96.0 for 10.6 min; by this note's own fit that is ≈ 90 °C. Oil-pressure jitter (`CAN Analog 5`, §6b) is unchanged (2.68 quanta, 26.6 % spikes). Full write-up: [log_2026-09-29_allchannels_smoothclt.md](log_2026-09-29_allchannels_smoothclt.md) §4.

## 0. Summary

The CLT reading is corrupted by **engine-running electrical pickup on the CLT circuit itself**, then
**amplified ~2× by a defective cell in `cltTbl`** and further amplified by the intrinsic loss of
volts-per-degree that any NTC on a 2K2 pull-up suffers at operating temperature. The ECU is not at
fault; the conversion is not at fault; no sensor fault is being declared.

Three findings, independent of each other:

- **[A] The noise is real, electrical, and lives on the CLT wire.** Not the ECU, not a shared
  reference, not the fan. It is impulsive, engine-running-only, and **gets markedly worse as the
  car heat-soaks** (§1h) — diagnose it hot.
- **[B] `cltTbl` has one broken cell** that creates a 96 °C dead band across the normal operating
  point and an 8.6 °C step at its edge. This is a calibration bug, not noise, and it is what turns
  a 0.2 V glitch into a 20 °C reading.
- **[C] The 2K2 pull-up is a poor impedance match to this sensor when hot**, costing resolution and
  raising the ground-offset transfer ratio. Changing it is mitigation, not the cure.

---

## 1. [A] The noise is electrical, engine-running, and CLT-local

### 1a. Zero noise with the key on and the engine off

First 30 s of the log (`ECU State` 1, RPM 0, `Battery voltage` 12.162 V): `CLT Voltage` is dead flat
at one value for 751 consecutive samples — not one LSB of dither. At the sample the engine fires
(RPM 1414, battery steps to 14.1 V) the channel begins dithering immediately and never stops.

This rules out, in one stroke: the ECU's ADC, the 5 V rail at rest, the thermistor itself, and any
mechanical/thermal explanation. **The disturbance is produced by the running engine.**

### 1b. All of the CLT error is in the voltage; the conversion is clean

`CLT` lags `CLT Voltage` by exactly one log sample (40 ms). With that lag applied, re-running the
tune's own `voltage5VCLTBin`/`cltTbl` interpolation against the logged voltage reproduces the logged
`CLT` to a mean |error| of **0.50 °C, 81 % within 1 °C** — the residual is the log's own 8-bit
voltage quantization (5 V/255 = 19.6 mV). Nothing is wrong inside the ECU's conversion path.
`CLT status` = 1 for all 48 064 samples and `failSafeCLTValue` never substitutes.

> Use the lag. Comparing `CLT` to `CLT Voltage` on the same row makes the relationship look
> *inverted* during glitches and will send you chasing a phantom.

### 1c. Rate and character of the impulses

> **Caveat added 2026-09-22:** the RPM table below is pooled across the whole log, and §1h shows
> spike rate rises ~5× over the drive while the high-RPM samples sit late. **Do not read an RPM
> dependence out of it.** The burst-length and sign statistics underneath are time-robust; the
> rate-vs-RPM column is not.

Spike = |voltage residual vs 1 s median| ≥ 4 LSB. Running samples only:

| RPM | spike rate | median MAP |
|---|---|---|
| 400–900 | 3.3 % | 38 |
| 900–1200 | 5.0 % | 37 |
| 1200–1500 | 1.4 % | 35 |
| 1500–1900 | 1.9 % | 35 |
| 1900–2400 | 5.2 % | 43 |
| 2400–3000 | 5.6 % | 45 |
| 3000+ | **9.7 %** | 62 |

71 % of spike bursts are a single sample and 23 % are two — sub-40-ms impulses, aliased by the 25 Hz
log. **68 % push the node toward +5 V (reads colder), 32 % toward ground.** Impulsive, rate- and
one-sided: an impulsive switching source rather than a continuous one. Which switching source —
coil or injector — is **not** resolved by this log (§1g).

### 1d. It is not the radiator fan

The fan latches on at `coolantFanActTemp` and the car spends nearly the whole hot portion with it
running, so fan state and coolant temperature are almost perfectly confounded — except for 191
samples at `Coolant fan` = 0 with the engine hot (RPM ~2780, fan suppressed by `coolantFanVSSOff`).

| condition | mean \|residual\| | p99 |
|---|---|---|
| hot, fan ON | 0.0218 V | 0.079 V |
| hot, fan OFF | 0.0227 V | 0.098 V |

Identical. **The fan is exonerated.** (This also breaks the confound, which is what makes §1f valid.)

### 1e. CLT and IAT are not sharing a return — which is the whole finding

ECUMaster's own wiring diagram (`docs/emu-black-help/Images/iatClt.png`, transcribed in
[Sensorsandinputs.md](../../docs/emu-black-help/Sensorsandinputs.md)) draws both sensors as
**two-terminal** devices whose second terminals are **tied together and run to the EMU's Sensor GND
pin (B29)**. CLT signal is B5, IAT signal is B32. Nothing in the diagram touches engine or chassis
ground. Wired to spec, **CLT and IAT share one return conductor.**

They do not behave like it:

- **CLT vs IAT spike coincidence, both measured on the raw `* Voltage` channels** (not on the
  1 °C-quantized `IAT`, which is too coarse to threshold honestly):

  | spike threshold | P(CLT) | P(IAT) | P(both) | independent | lift |
  |---|---|---|---|---|---|
  | 2 LSB | 0.1561 | 0.1999 | 0.03231 | 0.03122 | **1.03×** |
  | 3 LSB | 0.1095 | 0.1179 | 0.01313 | 0.01291 | **1.02×** |

  Pearson r of the two residual series, running: **0.073** (hot only: 0.080). Independent to within
  measurement error.
- **`Analog 5` = Fuel pressure** (r = 0.9996 against the `Fuel pressure` channel), a 3-wire sensor on
  the ECU's own analog input and sensor ground: running residual **0.54 quanta**, i.e. below the
  log's own rounding. **`PPS Voltage`**: 1.16 quanta and the lowest sample-to-sample reversal rate of
  any input (0.378 — a smooth signal, see §6).

A disturbance on a genuinely shared B29 return would hit both temperature channels on the same
samples and would also show up on fuel pressure and PPS. It does none of those. The ECU's 5 V
reference and its sensor ground are sound, and **the two sensors are referenced to two different
things.**

> **Do not read this as "not a grounding problem."** It is the opposite. Engine ground is a
> *distributed conductor*, not a node: it carries coil primary returns, starter and alternator
> current, and two points on the block metres apart differ by tens of millivolts during a switching
> impulse. Two sensors each grounded locally to the engine at different points would glitch
> **independently** — exactly what is measured. Independence rules out a common bouncing *node*; it
> is positive evidence *for* local engine grounding. Earlier phrasing in this note conflated the two.

Most consistent reading of §1e + §1f together: **one or both sensors returns to engine/chassis ground
locally instead of being run back to B29.** A 1-wire NTC (threads into the boss, grounds through the
block) does this by construction and cannot be wired any other way; a 2-pin sensor does it only if
its second terminal was landed on a nearby stud rather than distributed from sensor ground.

### 1f. The coupling is a *series* disturbance in the sensor leg, not charge injected onto the wire

Three candidate mechanisms transfer to the ADC node with different, strongly separated temperature
dependences. With `R_pu` the pull-up and `R_th` the thermistor, and using `V/5 = R_th/(R_pu+R_th)`:

| mechanism | transfer to node | hot (V≈0.55) | cold (V≈1.6) | predicted hot/cold |
|---|---|---|---|---|
| series EMF in the sensor leg — ground offset, or magnetic pickup in the wire loop | `1 − V/5` | 0.89 | 0.68 | **1.3×** |
| current injected onto the signal wire (capacitive pickup) | `V/5` | 0.11 | 0.32 | 0.34× |
| noise on the 5 V pull-up rail | `V/5` | 0.11 | 0.32 | 0.34× |

Measured, with **RPM (1300–1700) and load (MAP 28–45) matched**, fan state shown not to matter:

| | n | mean \|residual\| | p99 |
|---|---|---|---|
| hot (V < 0.70) | 3948 | 0.0218 V | 0.079 V |
| cold (V > 1.30) | 2802 | 0.0077 V | 0.039 V |
| **ratio** | | **2.8×** | **2.0×** |

The two current-injection mechanisms predict **3× less** noise when hot. They are off by roughly an
order of magnitude in the wrong direction and are **ruled out**. The series-EMF model has the right
sign but under-predicts the magnitude — note the cold figure sits under one log LSB and is therefore
quantization-floored, so 2.8× is a *lower bound* on the true ratio and the gap is if anything wider.
The direction is what matters and it is unambiguous.

Referred back through the divider, the equivalent series disturbance at the sensor is **p99 0.110 V,
p99.9 0.199 V, peak 0.352 V**. A 100–350 mV impulsive offset between the sensor's ground reference
and the ECU's, or induced in an unshielded signal/return loop, at spark rate.

**Practical reading:** the CLT circuit's return is either not the EMU's own sensor ground, or the
signal and its return are not run as a tight pair away from ignition and injector wiring — or both.
Same conclusion for IAT, independently.

### 1g. Dwell does not vary with RPM — and controlling for that exposed a drift

Raised by Will 2026-09-22: dwell appears to fall with RPM, which would invalidate any per-spark
normalization. Checked — it does not.

| | correlation with `Dwell Time`, running |
|---|---|
| `Battery voltage` | **−0.986** |
| `RPM` | **−0.004** |
| `RPM`, partialled on `Battery voltage` | **−0.075** |

Dwell is a pure function of battery voltage (`vbattVBins`, the dwell table doing exactly its job:
4.45 ms at 13.0 V → 4.00 ms at 14.2 V). With vbat held at 13.6–13.9 V, dwell is **4.15 ms flat from
1000 to 3200 rpm**. The apparent RPM dependence is vbat rising at cruise. `Overdwell` is 0 for all
48 064 samples — no dwell limiting anywhere, and with coil-per-plug each coil has 20 ms between
events at 6000 rpm against ~4.3 ms commanded. Total dwell spread across the running log is 9 %
(p5 4.05, p95 4.40 ms), in the direction that *stabilizes* coil peak current against vbat.

**But chasing it found a confound in this note's own RPM analysis.** Spike rate is strongly
time-dependent (§1h), and the high-RPM samples in this log are concentrated late. The earlier
claim here — "roughly constant per spark while injector duty quadruples, therefore coil not
injector" — was computed on the pooled log and does not survive. Split by log half, per-1000-sparks
above 1200 rpm reads 8.7 / 6.3 / 13.5 (first half) and 13.9 / 17.4 / 14.4 (second) — flat-ish
within each half, but too noisy to carry the coil-vs-injector discrimination.

**Downgraded to unresolved.** The impulse source is not identified from this log. Coil current
remains the leading candidate on physical grounds (impulsive, sub-40 ms, engine-running-only), but
this log does not prove it over injector current.

### 1h. The fault worsens with heat soak — and it is temperature, not just time

Two distinct effects, separated by the warm-up ramp. Between t = 30 s and t = 400 s the engine runs
at a roughly steady 1050–1470 rpm while coolant climbs continuously:

| window | median RPM | `CLT Voltage` | mean \|residual\| | spike rate |
|---|---|---|---|---|
| 30–80 s | 1458 | 1.824 | 0.0075 V | 0.00 % |
| 80–130 s | 1473 | 1.471 | 0.0071 V | 0.00 % |
| 130–180 s | 1404 | 1.118 | 0.0082 V | 0.00 % |
| 180–230 s | 1297 | 0.882 | 0.0096 V | 0.16 % |
| 230–280 s | 1063 | 0.686 | 0.0098 V | 0.24 % |
| 280–330 s | 1070 | 0.529 | 0.0164 V | 1.28 % |
| 330–400 s | 1058 | 0.510 | 0.0203 V | 2.46 % |

**2.7× in mean residual across a single six-minute ramp.** Matched at RPM 1300–1700, cold
(V > 1.3) gives 0.0077 V and *early* hot (V < 0.7, t < 400 s) gives 0.0236 V — **3.1× with minutes
between them**, which is the §1f divider effect measured with the time confound removed. §1f
therefore stands, and stands more firmly than the pooled 2.8× it was first reported with.

On top of that there is a slower drift. At **matched** hot voltage (V 0.43–0.55):

| window | median RPM | mean \|residual\| | spike rate |
|---|---|---|---|
| 0–600 s | 1507 | 0.0160 V | 0.78 % |
| 600–1100 s | 1286 | 0.0187 V | 1.12 % |
| 1100–1500 s | 1031 | 0.0214 V | **3.49 %** |
| 1500–1950 s | 1207 | 0.0202 V | **4.11 %** |

Bulk dither rises only 1.26×, but **spike rate rises 5.3×**. The background is roughly unchanged
while the *impulses get far more frequent* as the car heat-soaks. That is the signature of a
thermally marginal connection — terminal tension, a corroded crimp, or a run that shifts against a
noise source as things expand — not of a fixed coupling geometry.

Oil pressure moves the **opposite** way over the same drive (31.5 % → 5.0 % spike rate), one more
reason to treat it as an unrelated fault (§6b).

**Consequence for the backprobe: test hot, after a long drive.** A cold engine will show close to
nothing — the first three windows above have a literal 0.00 % spike rate.

## 2. [B] `cltTbl` has one broken cell — and it is doing most of the visible damage

`voltage5VCLTBin` is 8-bit, `V = raw × 5/255`. Fitting Steinhart-Hart (`1/T = a + b·lnR + c·ln³R`,
`R = 2200·V/(5−V)`) to the 14 points of `cltTbl` as read from the 09-19 export:

- Drop the **0.588 V** cell → the remaining 13 points fit to **RMS 0.32 °C**, and the fitted curve
  predicts **87.4 °C** at that bin. The table says 96.
- Drop the **0.451 V** cell instead → RMS 2.18 °C, and the curve predicts 97.8 °C where the table
  says 96 — i.e. that cell is fine.

The verdict is not close. **The 0.588 V cell is a duplicate of the 0.451 V cell's value and is wrong
by +8.6 °C.** The sensor's own characteristic, recovered from the other 13 points, is a perfectly
well-formed NTC (≈3747 Ω @ 0 °C, 2126 @ 20, 677 @ 60, 270 @ 90, 194 @ 100). The table is good
everywhere else; this is one bad entry, almost certainly a typo or a wizard rounding artifact.

Two consequences, both severe at exactly the temperature that matters:

1. **A dead band.** 0.451–0.588 V all reads 96 °C. **The log sits there 65 % of the hot running
   time.** True span of that band on the real curve: ~96.5 °C down to ~87.4 °C. The ECU cannot see a
   9 °C change at operating temperature.
2. **A cliff at its edge.** The next segment (0.588→0.824 V) runs at **−89 °C/V**, so one 19.6 mV
   LSB = 1.75 °C and a 0.2 V glitch = 18 °C. Every noise spike that escapes the dead band lands on
   the cliff. Correcting the cell drops that segment's slope to ≈ −66 °C/V and removes the
   discontinuity.

Measured `CLT` excursions, hot and running (deviation from the 1 s median): p90 = 2 °C, p99 = 6 °C,
p99.9 = 13 °C, **max 26 °C**; 2.25 % of samples ≥ 5 °C off, 0.23 % ≥ 10 °C off.

**Fix:** set the `cltTbl` cell at `voltage5VCLTBin` index 4 (raw 0x1E = 0.588 V) to **87 °C**. One
cell. It costs nothing, removes the 8.6 °C step and the dead band, and halves the noise gain — do it
before touching any hardware. Separately, the table spends 9 of its 14 points below 51 °C and only 4
above 96 °C; regenerating it with the CLT wizard biased toward 60–120 °C would improve accuracy in
the band the engine actually lives in (it does not reduce noise).

---

## 3. [C] The 2K2 pull-up is a poor match when hot — a real but secondary lever

`cltPullup` is a **bool**, not a selector: the EMU Black's CLT/IAT inputs carry a fixed internal
**2K2** (analog inputs 1–6 get 4K7 and a 3-way `anNPullup` selector; CLT/IAT get neither a choice of
value nor any `DigitalFilter` symbol). The only way to change it is to clear `cltPullup`, fit an
external resistor from the CLT pin to +5 V, and regenerate the table with the wizard's `Rx` set to
the new value. (`docs/emu-black-help/Sensorsandinputs.md` :16, :397.)

At 90 °C this sensor is ~270 Ω against a 2200 Ω pull-up — badly mismatched. Sensitivity is maximized
when `R_pu ≈ R_th`, and a lower pull-up wins on all three axes at once:

| `R_pu` | V @ 90 °C | mV/°C @ 90 °C | node Z (Ω) | gnd transfer `α` | V @ 0 °C | mV/°C @ 0 °C | self-heat |
|---|---|---|---|---|---|---|---|
| **2200 (current)** | 0.547 | **15.7** | 241 | **0.891** | 3.15 | 33.2 | 1.1 mW |
| 1500 | 0.763 | 20.9 | 229 | 0.847 | 3.57 | 29.1 | 2.2 mW |
| **1000** | 1.064 | **27.1** | 213 | **0.787** | 3.95 | 23.7 | 4.2 mW |
| 680 | 1.422 | 32.9 | 193 | 0.716 | 4.23 | 18.5 | 7.5 mW |
| 470 | 1.825 | 37.5 | 172 | 0.635 | 4.44 | 14.1 | 12.3 mW |

Lower `R_pu` simultaneously raises mV/°C at the operating point, lowers node impedance (less
capacitive pickup — not the dominant path here, but free), and lowers `α`, the fraction of a ground
offset that reaches the ADC. The cost is cold-end headroom: the whole curve shifts toward 5 V, so
sub-zero readings compress and may approach the input's short-to-5V validity limit. Self-heating is
not a concern in liquid.

Translating the log's measured voltage noise into °C error at the operating point:

| `R_pu` | p90 | p99 | p99.9 | worst |
|---|---|---|---|---|
| 2200 | 3.8 | 6.2 | 11.3 | 20.0 °C |
| 1000 | 1.9 | 3.2 | 5.8 | 10.2 °C |
| 680 | 1.4 | 2.4 | 4.3 | 7.7 °C |

**1K is the balanced choice** — 1.7× the resolution, 0 °C still lands at 3.95 V with 24 mV/°C of
cold-end resolution, and it does not push the cold end near the rail. But note what the table says:
even at 680 Ω the worst-case excursion is still 7.7 °C. **A pull-up change scales the symptom; it
does not remove the source.** Wiring does.

A pull-*down* is not applicable. It is for voltage-output sensors; an NTC needs a pull-up to form the
divider at all.

---

## 3b. What the manual actually says

Thin, but not empty. The V3 help has **no CLT-noise section** and no filtering option for these
inputs. What it does contain that bears on this:

- **The wiring diagram is the prescription** (`Sensorsandinputs.md` §IAT, CLT → `Images/iatClt.png`).
  Two-terminal sensors, both returns tied to **B29 Sensor GND**, signals to **B5** (CLT) and **B32**
  (IAT). No engine or chassis ground anywhere in it. That is the whole of ECUMaster's guidance and
  it is enough.
- **"missing sensor ground" is named as a cause of a reading going toward 5 V** (`Sensorsandinputs.md`
  :324, in the sensor-status definitions). For an NTC on a pull-up, losing the ground end pulls the
  node to the rail. The log's **68 % / 32 % asymmetry toward +5 V (colder)** is consistent with an
  intermittent, partial loss of ground reference. Consistent, not proof — 68/32 is a modest bias.
- **The pull-up is described as "in rare cases … not optimal for the specific sensor used"**
  (:397) — ECUMaster's framing is sensor-range matching, not noise. They do not offer it as a noise
  remedy, which matches the conclusion in §3.
- **Shielding guidance exists only for VR triggers** (:169, :195, :243, :248): shielded cable,
  shield grounded **at one end only**. There is no equivalent instruction for temperature sensors,
  but the principle transfers and costs nothing.
- **Pre-"P" switch-input warning** (:841, :1252) — relevant to this ECU (revision F) and already
  acted on 2026-08-29, but it is about the three built-in switch inputs, not these.

## 4. Order of operations

1. **Fix the `cltTbl` cell at 0.588 V (96 → 87 °C).** Free, immediate, removes the dead band and the
   8.6 °C step, halves the noise gain. Nothing else should happen first.
2. **Establish what the sensor actually is and where its return goes.** Count the pins. A 1-wire NTC
   grounds through the block by construction and no amount of routing fixes that — it wants
   replacing with a 2-pin part. A 2-pin sensor needs its second terminal traced: B29, or a stud?
   Direct measurement, engine running ~2000 rpm: scope or AC volts between the sensor's ground
   terminal (or its boss) and the EMU's B29. §1f predicts **100–350 mV of impulsive offset** there.
   That is a falsifiable number — if it is absent, this diagnosis is wrong.
3. **Fix the wiring** — this is the actual cure. Return the CLT to **EMU sensor ground (B29)**, not
   the block, the head, or a chassis stud. Run signal and return as a **twisted pair** the whole way
   to the ECU. Keep it off the coil harness; cross at right angles rather than running parallel. Do
   the same for IAT if convenient, though §6 shows its disturbance is smaller and oppositely
   signed — it is not obviously the same fault. If a shield is used, ground it **at the
   ECU end only**. §1g points at the coil grounds as the current source worth relocating if the
   sensor rewiring alone does not finish it.
4. **Re-log and re-measure** with the same method (`CLT Voltage` residual vs 1 s median, split by
   RPM and load, key-on-engine-off as the zero reference). Wiring done right should collapse the
   spike rate toward the engine-off floor. CLT and IAT glitches should also become *correlated*
   once they genuinely share B29 — that is the confirmation signature, not a new problem.
5. **Only then** consider the external 1K pull-up + regenerated table, as insurance and for the
   resolution gain. It is worth doing on its own merits but it is step 5, not step 1.

## 5. What not to do

- Don't add an RC filter at the ECU pin as the first move. It trades the glitch for lag on a channel
  that feeds warmup enrichment, ASE, the idle reference and fan logic, and it hides the fault you
  still have. There is no `cltDigitalFilter` in firmware for the same reason.
- Don't touch `failSafeCLTValue` / `failReportCLT`. They never fired in this log (`CLT status` = 1
  throughout); the excursions are valid conversions of a corrupted voltage, so the fault detector is
  behaving correctly and cannot help here.
- Don't read `CLT` against `CLT Voltage` on the same row — see §1b, apply the one-sample lag.
- Don't conclude anything about the sensor element. Its recovered R(T) fits Steinhart-Hart to
  0.32 °C RMS; it is healthy.

## 6. Channel noise inventory — all 564 channels scored

Method: residual vs a 25-sample (1 s) running median, normalized by each channel's own quantization
step `q` so units drop out. Two metrics, and **both are needed**:

- **amp** = residual σ in quanta. Below ~1.0 the channel is only showing log rounding.
- **rev** = fraction of consecutive first-differences that change sign. White noise → 0.67. A smooth
  physical signal sampled at 25 Hz → well under 0.35. This is what separates *noise* from *fast real
  dynamics*, and without it every control output looks broken.

131 channels had enough range to score. After removing computed/control outputs (PID terms, `VE`,
`Idle target`, `DBW Out. DC`, `Injectors PW`, accumulators like `Fuel usage` and `Turboshaft speed`),
the raw-input picture:

| channel | what it is | amp, engine off | amp, running | rev | p99.9 | verdict |
|---|---|---|---|---|---|---|
| `CAN Analog 5` | **Engine oil pressure**, on the CAN Switchboard (r = 0.9987) | 0.06 | **2.69** | 0.75 | 0.392 V = **1.6 bar** | **worst absolute jitter of any real sensor** |
| `Mux switch voltage raw` | unused — `MUX switch 1/2/3` are constant 0 | 0.95 | 3.75 | 0.80 | 1.13 V | floating input, ignore |
| `Battery voltage` | — | 1.22 | 2.59 | 0.61 | 0.271 V | alternator ripple, normal |
| `IAT Voltage` | IAT, B32 | 0.84 | **1.65** | 0.82 | 0.098 V | mildly noisy — see below |
| `TPS voltage` / `Analog 2` | same input, logged twice | 3.36 | 1.62 | 0.59 | 0.333 V | throttle genuinely moving |
| `CLT Voltage` | CLT, B5 | 0.84 | **1.58** | 0.70 | **0.177 V** | **the problem** |
| `Internal MAP voltage` | — | 0.00 | 1.26 | 0.78 | 0.333 V | 67 % of bursts ≥ 3 samples → real aliased manifold dynamics |
| `PPS Voltage` | pedal, ratiometric | 1.66 | 1.16 | **0.378** | 0.294 V | clean (lowest rev of any input) |
| `Analog 5` | **Fuel pressure** (r = 0.9996; −0.75 vs MAP → MAP-referenced FPR) | 0.30 | **0.54** | 0.79 | 0.137 V | clean, below rounding |
| `CAN Analog 2/3/4/6` | Switchboard, other | ≤0.17 | ≤0.27 | — | 0.02 V | clean |
| `Knock voltage peak cyl 1–6` | — | 0.2–0.4 | 1.9–3.6 | 0.67–0.71 | — | that is the measurement, not a fault |
| `Analog 1/3/4/6`, `CAN Analog 1/7–12` | unused | — | — | — | — | railed or flat 0 (back pressure is `CAN Analog 6`, alive — corrected 2026-09-28) |

### 6a. CLT and IAT are *not* the same fault

Correcting an earlier claim in this note. Spike character, running, threshold 3 quanta:

| channel | n | 1-sample | 2-sample | ≥3-sample | toward +5 V | p99.9 |
|---|---|---|---|---|---|---|
| `CLT Voltage` | 1784 | 71 % | 24 % | 6 % | **70 %** | 0.177 V |
| `IAT Voltage` | 828 | **99 %** | 1 % | 0 % | **18 %** | 0.098 V |

Opposite sign bias, different burst structure, and 1.8× different tail. IAT's σ looks similar to
CLT's (1.65 vs 1.58 quanta) but that is dither around a code boundary, not impulses; converted
through the IAT curve near 27 °C (≈ 54 mV/°C) its p99.9 is about **1.8 °C**, which is tolerable.
CLT's p99.9 through the as-built table at the operating point is **11–16 °C**.

So: rewire IAT to B29 while you are in there, but do not expect it to be the same defect, and do not
use it as corroboration. **The CLT circuit is the outlier.**

### 6b. Oil pressure deserves its own look

`CAN Analog 5` has the largest absolute jitter of any genuine sensor here: **σ 0.22 bar, p99.9
1.6 bar on a 4.1 bar median** (the filtered `Engine oil pressure` channel reads σ 0.143 bar, p99.9
1.00 bar). Dead flat with the engine off (0.06 quanta), so it is engine-dependent — but the residual
is **flat across RPM and pressure**:

| RPM band | median OP | mean \|residual\| |
|---|---|---|
| 400–1000 | 2.19 bar | 0.0375 V |
| 1000–1500 | 3.06 bar | 0.0368 V |
| 1500–2000 | 5.75 bar | 0.0430 V |
| 2000–2800 | 5.44 bar | 0.0385 V |
| 2800+ | 5.94 bar | 0.0350 V |

Hydraulic pump ripple would scale with mean pressure; it does not. It is also symmetric (46 %
positive) and shows no coincidence with CLT (lift 0.93×).

**Wiring confirmed by Will 2026-09-22: this sensor is on sensor ground with a short run into the CAN
Switchboard, and the coils sit close to that run.** The grounding hypothesis that applies to CLT does
not apply here. Coil proximity was the natural next guess — the log does not support it:

| RPM band | median OP | spike rate | per 1000 sparks |
|---|---|---|---|
| 400–1200 | 2.25 bar | 12.9 % | **62.8** |
| 1200–1800 | 6.00 bar | 17.3 % | **59.5** |
| 1800–2600 | 5.31 bar | 15.9 % | **36.2** |
| 2600+ | 5.94 bar | 14.2 % | **21.9** |

The rate is **flat in time (≈15 % of samples at any engine speed) and falls 3× per spark** from idle
to 3000 rpm. At matched oil pressure (5.0–6.5 bar) the amplitude *decreases* with RPM
(0.0468 → 0.0357 V) and so does the spike rate (23.8 % → 13.5 %). Coil-synchronous pickup does the
opposite — see §1g, where CLT holds roughly constant per spark. Combined with 66 % single-sample
bursts and a **symmetric** sign split (46 % positive), this reads as **continuous broadband noise at
a roughly fixed level**, aliased by the 25 Hz log — a σ of 2.69 quanta against a 3-quanta threshold
predicts ≈15–26 % exceedance, which is what is measured.

Engine-running-only but not engine-speed-dependent leaves: the Switchboard's ADC or reference, CAN
transport jitter, the sensor element, alternator ripple riding a ratiometric supply (though
`Battery voltage` coincidence is 0.94×, i.e. independent), or the fuel pump. **Separate
investigation, cause unresolved from this log — but not the coils.** It matters because the
oil-pressure-vs-duty work in [op_vs_dbw_1000rpm.md](op_vs_dbw_1000rpm.md) and the viscosity
correction in [oil_viscosity_idle_airflow.md](oil_viscosity_idle_airflow.md) both read this channel:
any single-sample OP reading carries ±0.2 bar of noise, so bin and average, never threshold on one
sample.

### 6c. What the matrix says about shared paths

Spike-coincidence lift, running, 3-quanta threshold (1.0 = independent):

- `CLT` ↔ `IAT` ↔ `CAN Analog 5` ↔ `Battery voltage`: all **0.93–1.26×**. Mutually independent.
- `Internal MAP voltage` ↔ `TPS voltage` ↔ `PPS Voltage` ↔ `Analog 5`: **48–116×**. That is not
  noise — pedal moves, throttle follows, manifold pressure changes, MAP-referenced fuel pressure
  follows. A useful positive control: the method does detect genuinely shared events when they exist.

---

## 7. Field procedure — backprobing the CLT circuit

Written 2026-09-22 ahead of Will's backprobe session. Ordered by information per minute. Pin
references from ECUMaster's diagram: **B5** = CLT signal, **B32** = IAT signal, **B29** = Sensor GND.

### 7a. Count the terminals first

One terminal → the block *is* the return, by construction, and no routing change can fix it. The
answer is a 2-pin sensor, not a jumper (see the warning in 7e). Two terminals → continue.

**Answered 2026-09-25 (Will): the ECU CLT sensor is two-pin.** The 1-wire case is ruled out. While
the connector is off, also meter the sensor's own ground pin to its threaded body: it should read
open. Continuity there means the element is shorted to the case, which grounds it through the block
however the harness is wired.

### 7b. Trace the return with the ECU **unplugged**

DC continuity with everything connected proves nothing: B29 ties to ECU ground ties to battery
negative ties to the block, so a meter reads low ohms whichever path the sensor actually uses. The
test only works with the ECU connector off, which isolates B29 from the vehicle ground net.

Source check 2026-09-25: ECUMaster's EMU Black pinout lists **29, 38, 39 as sensor grounds, "not
connected to the engine"**, and **17, 24, 27, 28 as power grounds** to the block. Neither the pinout
nor the V3 help says how sensor ground joins device ground inside the ECU — only that it must not be
landed on the engine. The inside-the-box tie is inferred (the ADC needs a common reference with the
supply), not documented, and it is why a beep from a sensor-ground wire to the block, with the ECU
plugged in, says nothing about how that wire is routed.

ECU unplugged, CLT connector still plugged in, measure from the **harness-side** CLT ground wire to:

| | to B29 pin | to engine block | reading |
|---|---|---|---|
| wired to spec | ~0–1 Ω | open / high | dedicated return |
| **the suspected fault** | open / high | ~0–1 Ω | bonded locally to the engine |

While the connector is apart, inspect the terminals. A corroded or loose crimp **in the return** is
its own version of this fault — it inserts series impedance that converts ground current into
exactly the offset §1f measures.

### 7c. The falsifiable running measurement

**Do this after a long drive, fully heat-soaked.** Per §1h the spike rate is ~0 % in the first
three minutes and 4–9 % late in a 32-minute drive; a cold engine will show you nothing.

Engine warm, ~2000 rpm. Two-channel scope, AC coupled, 100 mV/div, 1 ms/div:

- **Ch1** → CLT sensor **ground** terminal (or its boss, if 1-wire)
- **Ch2** → CLT sensor **signal** terminal
- **Reference for both** → EMU **B29**, back-probed at the ECU connector

Use a **battery-powered scope or a differential probe**. A mains-earthed scope clipped to sensor
ground while probing the block creates a new ground loop and can shunt or inject the very thing
being measured.

**Prediction from the log (§1f, §1g):** impulse train at spark rate — `RPM/20` Hz, so **100 Hz at
2000 rpm** — amplitude **100–350 mV peak**, **predominantly positive-going**, sub-40-µs events.
If that is not there, this diagnosis is wrong.

**The discriminator, in one shot:**

| observation | meaning |
|---|---|
| Ch1 and Ch2 move **together** (common-mode); math A−B is clean | the **return** is the problem — ground offset, as diagnosed |
| Ch2 moves, Ch1 is quiet | pickup on the **signal wire** — routing and shielding, not grounding |
| both quiet | the disturbance is not at the sensor; look at the ECU-side harness run |

**DMM-only fallback:** true-RMS AC mV between the CLT ground terminal and B29, running vs engine
off. A meter badly under-reads a ~1 %-duty impulse train — 200 mV peaks may show as ~20 mV. So **any
AC reading above ~5 mV that appears only when running is meaningful; absence proves nothing.**

### 7d. Confirm by substitution before committing to a repair

Temporary flying lead from the CLT sensor's ground terminal to B29 (or to another sensor's SGND on
the ECU side), existing return disconnected. Re-log: 30 s key-on/engine-off **first** — that is the
zero reference — then idle, then one pull past 3000 rpm. Confirmed if `CLT Voltage` p99.9 collapses
from 0.177 V toward the engine-off floor. Check `CLT Voltage` and `IAT Voltage` are both in the log
config before driving.

### 7e. ⚠ Do not bond the block to sensor ground

If the sensor turns out to be 1-wire, the tempting shortcut — a jumper from the sensor boss to B29 —
is the wrong move. It puts engine-ground current onto EMU sensor ground and corrupts every other
input on it. That is precisely the failure already documented on this car twice
([ac_request_input_noise.md](ac_request_input_noise.md),
[vss_signal_integrity.md](vss_signal_integrity.md)), and this ECU is revision F, pre-"P". Fit a
2-pin sensor and run a proper return.

---

## Related

- [ac_request_input_noise.md](ac_request_input_noise.md) — the same "returned to the wrong ground" failure on a switch input
- [vss_signal_integrity.md](vss_signal_integrity.md) — ditto, speed signal
- [../../notes/sensors_and_inputs.md](../../notes/sensors_and_inputs.md) — P5, the general NTC noise-gain principle
- [../../notes/idle_stall.md](../../notes/idle_stall.md) §E — why CLT noise destabilizes idle through four loops at once
