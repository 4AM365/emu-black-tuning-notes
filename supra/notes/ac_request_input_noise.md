# A/C request input (`Switch 1`) chatter — clutch-switch-gated harness fault

Status: **root cause found and fixed 2026-08-29 — clutch switch was on chassis
ground instead of sensor ground (§0); re-log pending.** Analysis 2026-08-28.

**Owner, 2026-08-28 (supersedes any OEM-circuit theory below):** the car had no
clutch start switch from the factory. The one fitted is an owner install and
**runs to the EMU only** — it touches nothing the A/C amplifier can see. The EMU
sits between the HVAC computer and the compressor clutch and gates the request
further. So OEM shared-ground / C9 / C15 routing is ruled out as a mechanism;
the coupling is entirely inside the owner-installed EMU wiring.

## 0. Root cause found and fixed — 2026-08-29

**Owner, 2026-08-29: the clutch switch was returned to chassis ground, not EMU
sensor ground. It has been rewired to sensor ground.** That is exactly the
violation §4c predicted from the hardware revision, and exactly the check §8
step 0 put ahead of all loom work. On a pre-"P" unit the documented consequence
of feeding a switch input anything but sensor ground is *corruption of the other
switch inputs* — which is the whole observed signature: the aggressor pin
(`Switch 3`, clutch) reads clean while `Switch 1` and `Switch 2` glitch on the
same samples in opposite directions, only while that circuit is energized.

**Still to confirm:** everything below was measured before the fix. Re-log in the
vulnerable state (clutch pressed, A/C not requesting, compressor off) and re-run
the §7 state matrix. Until that log exists, the fault is *explained*, not
*proven fixed*. The same fix is expected to clear the speed-input glitching —
see [vss_signal_integrity.md](vss_signal_integrity.md).

**Re-log result, 2026-09-28** (`fullchannels.csv`, 09-19, post-fix): `Switch 1` shows 17 edges in 150 s with the clutch pressed (6.8/min, down from 416/min in `omg.csv`) and 68 in 1772 s released (2.3/min). The chatter is gone. A 3× pressed/released bias remains, which is small in absolute terms. Source: [sensor_inventory.md](sensor_inventory.md).

## 1. Which channel is the A/C request

Read from `omg.xml.emub3` (newest XML export in `EMU_BLACK_V3\Supra`, 2026-08-24):

- `acActivation` selects the A/C request input.
- `clutchPedalInput` selects the clutch-pedal input.

Index → channel mapping proved empirically, not assumed: in `omg.csv` the logged
`Switch 3` channel equals the logged `Clutch pedal switch` channel on **99.87 %**
of 25 483 samples, and `clutchPedalInput` reads 3. So the input list is
`N → Switch N`, and `acActivation` (reading 1) is the **`Switch 1`** channel.
`Switch 2` is the brake (it disagrees with `Brake pedal switch` on 98.6 % of
samples, i.e. it is the inverted brake line).

Do not re-derive from the symbol value alone — re-check the `Switch 3` /
`Clutch pedal switch` identity against the current XML before trusting it.

## 2. It is genuinely noisy

`omg.csv`, 1022 s at 25 Hz (0.04 s/sample):

| metric | value |
|---|---|
| `Switch 1` transitions | 690 (40.5 /min) |
| transitions bounding a run < 0.5 s | 611 of 690 |
| median run length | 0.08 s (2 samples) |
| shortest run | 0.04 s (1 sample) |

Single-sample toggles at ~7 Hz. No A/C amplifier, evaporator thermostat, or
pressure switch produces that; the OEM amplifier's own protections act on
**3 s** (compressor-lock ratio test) and hysteresis-band pressure thresholds
(`ac_compressor_engagement_oem.md`). This is an electrical artifact, not a
command.

## 3. It is not new

Every all-channels log that carries `Switch 1`, April → August 2026:

| log | date | tr/min while clutch **pressed** | tr/min while **released** |
|---|---|---|---|
| `LogAutosave\drive_home_today.csv` | 2026-04-08 | 261.7 | 3.0 |
| `LogAutosave\hood on 0509 terrible day.csv` | 2026-05-31 | 280.7 | 5.6 |
| `all-channels-reduced-idlaircorr.csv` | 2026-05-31 | 411.1 | 12.8 |
| `all-channel-reference.csv` | 2026-05-31 | 450.5 | 12.5 |
| `20260613_1141.csv` | 2026-06-13 | 381.5 | 14.4 |
| `died_hot_return_to_idle_again.csv` | 2026-06-28 | 451.3 | 1.5 |
| `omg.csv` | 2026-08-24 | 416.1 | 3.1 |

(`cold idle dip again 3 all channels.csv`, 2026-06-26, has zero clutch presses
and zero chatter — the control case.)

## 4. The trigger is the clutch-pedal switch, not RPM or road speed

In `omg.csv`, conditional `Switch 1` transition rates:

    clutch pedal PRESSED           6.94 Hz   (645 transitions / 2325 samples)
    clutch pedal released, running 0.05 Hz   ( 44 transitions / 21243 samples)

**140×.** The apparent RPM and road-speed correlations found first (0.01 Hz at
rpm 0, 0.25 Hz at 1000, 2.1 Hz at 1500–1750; 0.31 Hz stationary vs 1.41 Hz
moving) are confounds — you press the clutch while moving and while the engine
is spinning 1500–2000.

**Retracted:** an earlier version of this note cited "engine OFF, 0.01 Hz" as
evidence that engine state matters. It proves nothing — in `omg.csv` the clutch
pedal was **never** pressed during the 1823 engine-off samples, so the aggressor
was simply absent. Whether the fault reproduces with the engine stopped is
untested, and testing it is cheap (see §6).

Per-press behaviour (40 presses in the log): `Switch 1` sits at a steady 0
before the press, begins toggling a **median 0.08 s after the clutch switch
closes**, runs at 24–83 % duty for the whole press, and returns to steady 0
within a few samples of release. It chatters *on* from a steady *off* — the
EMU is being handed spurious A/C requests, not losing real ones.

`Switch 3` itself stays clean throughout (80 transitions in the whole log,
long runs). The aggressor signal is clean at its own pin; only `Switch 1` is
corrupted. That is coupling into `Switch 1`, not switch bounce shared by both.

Two presses (t = 182.0, 184.1 s, 0.12 s and 7.64 s, engine running ~1400 rpm,
stationary) produced **zero** chatter. Unexplained; worth reproducing, since
whatever was different there is the discriminator.

## 4b. The fault signature: two inputs moving as a complementary pair

Four discriminating tests on `omg.csv`:

**(a) The brake input glitches on exactly the same samples.** `Switch 2` is the
brake, inverted at the pin — a genuine match, not an artifact of an idle
channel: the states are balanced (S2 is 1 for 13 071 samples, 0 for 12 412) and
25 123 of 25 483 samples fit the inverted relation. The brake is applied 74
times in the log, but `Switch 2` has **254 edges**. The surplus is glitch. During
clutch presses, **every** coincident S1/S2 edge pair moves in **opposite
directions**: 101 × (S1 0→1 while S2 1→0) and 99 × (S1 1→0 while S2 0→1). Zero
same-direction pairs.

That is not common-mode. A lifted ground reference pushes both pins the same
way. Two pins moving *toward each other's level* is what resistive coupling
between them looks like: the low pin is dragged up while the high pin is dragged
down.

**(b) The brake pedal is not an aggressor.** With the clutch released, engine
running: brake pressed 0.045 Hz, brake released 0.061 Hz. No effect. So this is
not generic pedal-box harness movement — it is specific to the clutch circuit.

**(c) Per-press duty is scattered, not fixed.** Across the 24 presses ≥ 1 s,
`Switch 1` duty runs **0.00 → 0.78**, median 0.58, stdev 0.199 — including
presses with zero chatter at all. A fixed electrical offset would give a
repeatable duty. Scatter that wide reads as marginal or motion-dependent
contact.

**(d) No supply loading.** Battery voltage across clutch closure: 13.552 V
before → 13.586 V after, **+0.035 V**. The switch is not dragging a shared
supply down.

Taken together: something in the owner-installed clutch-switch wiring
intermittently couples the `Switch 1` and `Switch 2` conductors to each other,
and only does so while that circuit is energised. Chafe into the loom, a splice
made when breaking in for the install, a spread or partly-inserted pin in the
EMU connector, or moisture in a connector body are all consistent. The log
cannot distinguish among them — the bench tests in §6 can.

## 4c. The ECU is hardware revision F — pre-"P" switch inputs

**Owner-reported, 2026-08-28: the unit is hardware revision F, CPU G.** That is
well before revision "P", and it changes the prior on the whole §4b signature.

ECUMaster documents a hardware-revision split on the three built-in switch
inputs (black-plug terminals 10, 23, 36) — `docs/emu-black-help/Sensorsandinputs.md`
lines 841 and 1252, same text twice:

> In the hardware revision "P" ... or newer, each input operates independently,
> and positive voltage can be applied to them (although they activate when
> switched to ground). In the case of older versions, **only sensor ground can be
> applied to their input; otherwise, the measurement from other inputs may be
> disturbed.**

So on this ECU the switch inputs are **not** independent. The documented failure
mode of feeding one of them anything other than **sensor ground** is *corruption
of the other switch inputs* — which is verbatim the observed behaviour: `Switch 3`
(clutch) stays clean at its own pin while `Switch 1` and `Switch 2` glitch, on the
same samples, in **opposite directions**, only while the clutch circuit is
energized (§4b(a)). A shared internal measurement path dragged off-reference by
one input's return explains the complementary-pair geometry more economically
than a resistive tie in the loom, and it explains why the aggressor pin itself
reads clean.

This does not retire the loom hypothesis — a non-sensor-ground return and a chafe
produce overlapping symptoms, and the state matrix (§7) still says the victim
line is only bendable when its source is soft. But it promotes one cheap check
above all the harness work: **what is the clutch switch's return actually tied
to?** If it lands on chassis ground, an engine/body ground stud, or any node that
is not EMU sensor ground, this is a documented hardware limitation being provoked
by the install, not a fault to hunt for.

The MUX-switch section of the same help page ([:914](../../docs/emu-black-help/Sensorsandinputs.md))
carries the same insistence for ground-controlled switches sharing an input —
"it is crucial that these switches are activated using sensor ground" — which is
consistent with the pre-P switch inputs sharing a measurement path.


## 5. It is reaching the compressor

`AC Clutch` output in the same log:

- 70 edges, **37 of them while the clutch pedal is pressed** — the pedal is down
  only 9.1 % of the time, so chance expectation is ~6.
- 35 clutch drop-outs, attributed: **22 caused by the request falling**
  (`Switch 1` 1→0 within 1 s), 4 by RPM below `acMinRPM`, 9 other. Zero by
  `acMaxTPS`.
- Compressor duty cycle: 35 ON periods, median **1.2 s ON / 2.0 s OFF**,
  shortest ON 0.04 s.

So the short-cycling recorded in `idle_drive_wobble.md` is **majority
request-side noise**, not the `acMinRPM` threshold. Lowering `acMinRPM` (the
planned 1700 → 850) will not fix it; that change addresses the 4 drop-outs, not
the 22.

## 6. What it is not — corrections from the owner, 2026-08-28

- **The car has no OEM clutch start switch.** Will installed one; it runs to the
  EMU only and touches nothing else. Every OEM-harness theory below the line in
  the first draft of this note (shared C9 ground, back-fed ST1 circuit,
  theft-deterrent leg, diode-OR idle-up node) is therefore **dead**. The
  coupling is between two of his own runs, at the EMU end.
- **Architecture, confirmed by owner:** HVAC computer → EMU `Switch 1` → EMU
  gates → compressor clutch. The EMU sits between the amplifier and the clutch
  and vetoes further. So the noise is on the amplifier→EMU leg, upstream of
  every EMU-side decision.
- **Log polarity checked, not assumed.** `sw1Invert`, `sw2Invert`, `sw3Invert`
  all read 0 in `omg.xml.emub3`, so the `Switch N` channels are raw pin states
  and the observed opposite-direction glitching between `Switch 1` and
  `Switch 2` is real at the pins. (Separately: `Switch 2` anticorrelates with the
  `Brake pedal switch` function channel, which says the brake switch is wired
  active-low — it does not mean the log is flipped.)
- **The ECU is hardware revision F (CPU G)** — pre-"P", so the switch inputs are
  the non-independent kind. See §4c; this is now the leading mechanism.
- **Not necessarily an intermittent connection.** Owner's hypothesis, and it now
  fits better than the make/break reading: a *fixed* resistive tie between the
  clutch run and the request line parks the request pin near mid-rail whenever
  the clutch circuit is energized, and ordinary noise then decides each sample.
  Nothing has to be making and breaking. Supported by there being **no pull-up
  or pull-down configured on the switch inputs** (only the analog inputs carry
  `anNPullup` symbols), so a high-impedance pin is free to be bent either way.

## 7. The state matrix — the fault has exactly one live configuration

Owner's test: if a fixed tie plus a weak source is the mechanism, the chatter
should appear in **one** state configuration, not scale smoothly. It does.

Pooled across all seven logs carrying `Switch 1` (April–August 2026):

| clutch switch | A/C clutch output | time observed | `Switch 1` edges/min |
|---|---|---:|---:|
| released | off | 53.6 min | 12.4 |
| released | engaged | 33.3 min | 0.7 |
| **pressed** | **off** | 10.2 min | **399.7** |
| pressed | engaged | 1.1 min | 44.6 |

Reproduced independently in all seven logs (per-log pressed+off 305–466 /min;
pressed+on 0–118 /min, the high outlier having only 3.0 s exposure).

**Brake state is irrelevant** — `omg.csv`, clutch pressed, compressor off:
brake released 433 /min (83.6 s) vs brake applied 444 /min (5.0 s). The brake
input glitches as a *victim* alongside `Switch 1`; its state gates nothing.

### Why the compressor-engaged column is quiet

Per `ac_compressor_engagement_oem.md`, the amplifier's `MGC` output is
**< 1 V when requesting, 4–6 V when not** (AC-64). Requesting is a hard pull;
not-requesting is a soft divided level. The EMU only engages the clutch when the
request is genuinely asserted — so the quiet cell is exactly the cell where the
source is stiff. A stiff source cannot be bent to mid-rail; a divided one can.
That is the mechanism, and the matrix is its fingerprint.

## 8. Diagnosis — what to check on the car

**Test in the vulnerable state only:** clutch pedal pressed, A/C *not* requesting
(compressor off). Testing with the compressor engaged will read clean and prove
nothing.

0. **Trace the clutch switch's return before anything else** (§4c). This ECU is
   hardware revision F — pre-"P" — so its switch inputs are documented as
   sensor-ground-only, with cross-input corruption as the stated consequence of
   violating that. If the clutch switch grounds anywhere other than EMU sensor
   ground, move it there and re-log. Costs one wire; potentially retires the
   whole fault. Do this before opening the loom.
1. **DMM on the EMU `Switch 1` pin**, clutch pressed, A/C off. Parked near
   mid-rail confirms the fixed-tie model — no scope needed. Sitting solidly at a
   rail sends you back to a make/break fault, and then it wants a scope.
2. **Unplug the clutch switch at the switch end**, leave its wire in place, work
   the pedal. Quiet ⇒ the *energized wire* is the aggressor. Still chattering ⇒
   the loom moving is.
3. **Ohm the clutch run against the request run** with the EMU unplugged, flexing
   the harness. Start where the loom was opened for the clutch-switch install.
4. Only if 1–3 come back clean, treat it as amplifier-side and read the panel
   self-diagnosis (`ac_compressor_engagement_oem.md`).

**Interim mitigation, not a fix:** debounce the request in the ECU — a Function
with ~0.5–1 s ON/OFF delay feeding a User switch, with `acActivation` pointed at
that — so a 40–80 ms glitch cannot reach the clutch output. Owner applies tune
changes; this is a proposal, not an export.

## 9. Open

- Some presses produce no chatter at all. Under a fixed divider that should not
  happen unless the noise floor moved. Unexplained.
- Whether the clutch switch's return lands on EMU sensor ground or on chassis /
  engine ground. Unknown as of 2026-08-28, and it decides between §4c (documented
  pre-P hardware limitation, provoked by the install) and §4b (a resistive tie in
  the loom). Answer this first.
- Whether `Switch 2` is corrupted by the same tie or a second one — it glitches
  on the same samples as `Switch 1` during presses, which argues one shared
  aggressor, but its rate varies far more between logs.
