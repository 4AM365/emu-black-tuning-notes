# Speed-signal integrity — the VSS input is the root of the idle open-loop chatter

Status: **still noisy after the 2026-08-29 clutch-switch ground fix (owner, 2026-08-30) — the sensor-ground rewire did NOT clear the speed glitches. Cause on the VSS line remains open.** Source: `omg.csv` (2026-08-24, 1022 s @ 25 Hz,
all-channel capture carrying `Vehicle Speed`, `Gear`, `Gear unknown`, `Clutch pedal switch`
and — for the first time — **`Idle force open loop`**). Companion export `omg.xml.emub3`.

**09-19 re-check (2026-09-28, `fullchannels.csv`):** still faulty, and the fault shows as **step functions**. There are 8 one-sample drops to 0 from 27–117 km/h (5–22 Hz; ~1 g braking is 0.26 Hz/sample), none near a live edit, plus a 270 Hz (≈1460 km/h) phantom held 0.56 s at t 1635.6. That signature is wiring or connection, not an edge-threshold setting. Drops below ~4 Hz are the normal standstill timeout. See [sensor_inventory.md](sensor_inventory.md).

This note owns the **speed input itself**. Its consumers are many: `idleOpenLoopOverVss`,
`idleIncreaseTargetAboveVSS`, the ratio-based gear estimator, `coolantFanVSSOff`,
`revMatchMinVSS`, `flatShiftVssLimit`, `lcMaxVSS`, `ralMinVSS`. Fixing it once fixes all of them;
tuning around it fixes none.

Configuration symbols to re-read before acting (values change, do not trust a remembered one):
`vssSource`, `VSSSensorType`, `VSSInputFilter`, `VSSTrigerEdge`, `VSSPullup`, `vssFilter`,
`speedRatio`, `wheelSpeedSource`, `gearDetectionType`, `gearRatioTolerance`, `gearDelay`.
A filter is already configured in `omg.xml.emub3` and the glitches below survive it.

## 0. Cause: the clutch switch was on chassis ground, not sensor ground

**Owner, 2026-08-29: the clutch switch was returned to chassis ground instead of EMU sensor
ground; it has been rewired to sensor ground.** This ECU is hardware revision F — pre-"P" — and
ECUMaster documents that on those units *"only sensor ground can be applied to their input;
otherwise the measurement from other inputs may be disturbed"*
([Sensorsandinputs.md:841](../../docs/emu-black-help/Sensorsandinputs.md), repeated at :1252).
Full derivation of that mechanism, and the A/C-request half of the same fault, in
[ac_request_input_noise.md §4c / §0](ac_request_input_noise.md).

**The speed input carries the same fingerprint.** Glitch rate (|Δspeed| > 200 km/h/s) in
`omg.csv`, conditioned on clutch state:

| clutch | exposure | glitches | rate |
|---|---:|---:|---:|
| **pressed** | 93.0 s | 20 | **12.9 /min** |
| released | 926.3 s | 16 | 1.0 /min |

**13×.** And it is *state*-dependent, not edge-dependent — median distance from a glitch to the
nearest clutch transition is **3.32 s**, only 2 of 36 within 0.5 s. So it tracks the circuit being
*energized*, not the switch making or breaking. That is the same state-gated geometry as the
`Switch 1` chatter, which is why the ground fix is expected to clear this too.

**2026-08-30 update: the fix did not clear it.** Owner reports the speed signal still glitches
on the 2026-08-30 drive. Note the VSS input is a *digital* input (dedicated speed input, per
`docs/emu-black-help/Sensorsandinputs.md` §Digital inputs), NOT one of the three pre-"P" switch
inputs — so the sensor-ground coupling mechanism that owns the `Switch 1`/`Switch 2` chatter was
never guaranteed to own this one. The clutch-state-gated 13× glitch ratio below stands as measured;
what it implicates is the clutch *circuit* being energized, and the coupling path into the VSS
digital input is still unidentified. Candidates worth metering: shared return/routing between the
clutch-switch run and the VSS wiring, `VSSInputFilter`/`VSSPullup` config headroom, and the VSS
sensor's own ground. Whether the ground fix cleared the `Switch 1` (A/C request) chatter is a
separate question — verify from a log that carries `Switch 1`.

**Interim mitigation in force (owner, 2026-08-30):** `idleOpenLoopOverVss` set to **400 km/h** —
the force-open-loop feature is effectively disabled so VSS noise cannot reset the idle PIDs. The
VSS idle-target increase remains live above ~5 km/h (a target step is a bounded nuisance under
noise; an integral wipe is not). The decoupling-gate policy (low threshold, see
[notes/idle.md → Activation gates](../../notes/idle.md)) stays the goal once the channel is clean.

## 0b. Why you cannot filter this away

The artifact is **not** an isolated spike. It is a coherent 0.5–0.7 s burst of phantom pulses that
ramps and decays like real acceleration — t = 201.32 s reads
`0.25 → 38.1 → 65.7 → 76.6 → 81.75 → 43.8 → 16.3 → 5.3` km/h with the car parked. Measured
consequence: a 5-sample median filter removes **zero** samples (nothing deviates more than
10 km/h from its 5-sample median). Any window long enough to swallow a 0.7 s burst also delays
every legitimate threshold crossing by 0.7 s, which is worse than the disease. Rejecting it in
software would need a plausibility gate (speed against RPM × gear ratio, or a slew limit), not a
filter — and none of that is necessary if the ground fix holds. **Fix it at the pin.**

## 1. The raw defect

- **36 samples** step by more than **200 km/h per second** — physically impossible.
- **Phantom speed at a standstill.** Three separate events read **81.75** and **46.25 km/h**
  while the 2-second rolling median of the same channel was **0.2 km/h** (parked, `Gear` 0,
  RPM ~1000–1300, `PPS` 0). This is the same defect the owner reported on 2026-08-27 as
  "flickers to 63 km/h at a standstill" — now captured with the downstream channels attached.

## 2. Downstream 1 — the gear estimator loses lock constantly

`gearDetectionType` is ratio-based, so it inherits every speed glitch. `Gear unknown` asserts
**214 times** in 1022 s: median run **0.20 s**, **140 of 214** shorter than 0.5 s. It also emits
nonsense assignments — `Gear` 6 at 1300 rpm and 0 km/h, `Gear` 5 at a dead stop.

## 3. Downstream 2 — `Idle force open loop` chatters (the confirmed mechanism)

`Idle force open loop` asserts **23 times / 35.2 s total**: median run **0.20 s**, **17 of 23**
under 0.5 s, shortest **0.04 s** (one sample).

**What clears the gate is `Gear unknown`, not a real neutral.** Restricted to samples above the
threshold with the clutch released (n = 2064):

| | force = 0 | force = 1 |
|---|---|---|
| `Gear unknown` = 0 | 706 | 870 |
| `Gear unknown` = 1 | **480** | **8** |

98 % of gear-unknown samples have the force cleared. So *Neutral enables closed loop* is being
satisfied by an **unknown** gear, and the gate toggles at the gear estimator's flicker rate
(~2.5 Hz) instead of at road-speed crossings. The 706 unforced gear-known samples are almost all
`Idle state` 0 — idle not activated, so the flag never sets.

## 4. What the chatter costs

Per EMU help (`docs/emu-black-help/Idle.md`), the force disables **all** idle PIDs **and resets
the integral terms**. **15 of the 23 assertions landed while idle was ACTIVE (state 2).** What
was thrown away at those onsets:

| discarded | median | range |
|---|---|---|
| `Idle ignition correction` | −3.0° | −8.0 … +17.0° |
| `Idle PID air % correction` | −3.06 % | −5.69 … +10.56 % |

It reads as square steps in the log. t = 883.4–885.2 s, rolling at 47 km/h in 5th, pedal up:
the ignition correction toggles **−6.5 → 0 → −6.0 → 0 → −5.5 → 0** four times in 1.8 s, air
correction with it, and RPM bumps ~70 each time the retard is dropped.

**Worst case, t = 201.64 s** — a genuinely stopped idle at 1300 rpm. Speed read 81.75, the
estimator assigned `Gear` 6, the force set, `Idle PID air % correction` +0.94 and
`Idle ignition correction` +2.0 were wiped to exactly 0, `Ignition Angle` stepped **20.5 → 18.5°**
and `Idle target` moved 1360 → 1375. The idle loop was blanked at a stop by a sensor artifact.
That is the stall-risk shape from [return_to_idle_bog.md](../../notes/return_to_idle_bog.md).

## 5. This closes the "frozen-PID mode" open item

The unexplained mode in `added features.csv` (2026-08-27) — both PID outputs exactly 0 with the
angle exactly at target, rolling in gear, RPM above target — is this gate. That log had no VSS
or `Idle force open loop` channel; `omg.csv` has both and shows the identical signature with the
flag asserted. See [idle_drive_wobble.md](idle_drive_wobble.md).

## 6. Same harness as the A/C chatter

The clutch-switch input group is an owner install that runs to the EMU only, and it already
demonstrably injects chatter into the A/C request line
([ac_request_input_noise.md](ac_request_input_noise.md), 2026-08-28, derived from this same log).
The clutch channel itself is comparatively clean here — 40 press events, median 1.44 s, only 6
under 0.5 s — so the *gate* chatter is the speed/gear path, not the clutch line. Two faults in
the same switch-input group; fix them together.

## 7. Provenance caveats for this log

- **Live edits.** `Data changing` = 1 through t = 787.8 s and `Making permanent` through
  t = 788.0 s. Everything in §3–§4 is drawn from t > 839 s, after the last edit. Do not pool the
  first 788 s with the rest.
- **The companion export does not describe the whole log.** The log shows a live **+500 rpm A/C
  idle-up** (settled stopped idle target 1500 with `AC Clutch` = 1 against a 1000 base) while
  `idleACRPMIncrease` in `omg.xml.emub3` reads 0. Confirm with the owner which was in force
  before reasoning on A/C idle-up from either artifact.

## 2026-08-30 confirmation — `bogevent.csv`

The short rolling return-to-idle event in `C:\Users\WTCra\OneDrive\Documents\EMU_BLACK_V3\bogevent.csv`
repeats the same mechanism in a much more consequential form.  Pedal release enters `Idle state`
2 at 1816 rpm, then RPM falls to 567 rpm in 2.00 s (least-squares slope **-761 rpm/s**).  During
the active part of that descent, `Idle force open loop` asserts 10 times for 35 samples =
**1.40 s**.  Each onset zeroes both corrections exactly as the help says:

| First assertion | `Gear unknown` | air before → forced → after | PID air before → forced → after |
|---|---:|---:|---:|
| 1387.88 s | 0 | 40.5 → 36.0 → 45.5 % | +4.69 → 0.00 → +9.88 % |
| 1388.36 s | 0 | 47.5 → 35.0 → 46.5 % | +12.94 → 0.00 → +11.94 % |
| 1388.60 s | 0 | 46.5 → 34.5 → 46.0 % | +12.25 → 0.00 → +12.00 % |
| 1390.92 s | 0 | 44.5 → 32.0 → 44.0 % | +12.50 → 0.00 → +12.00 % |

Every assertion begins while `Gear unknown=0`; the immediately following clear transitions
back to `Gear unknown=1` in the first three examples.  The clutch switch is released throughout
these force spans.  This is the prior gear-estimator/VSS gate chatter, not an air-PID output
clamp: the live controller has to rebuild +9…+13 % of requested air after every reset.  Mixture
goes rich only after the first reset (λ 0.936 vs 0.901 target at onset; λ 0.858 by 675 rpm), so it
compounds the torque loss but does not initiate it.  `Fuel Cut`, trigger error, protection,
check-engine, `Data changing`, and `Making permanent` are all zero; the cumulative trigger-error
count remains fixed at 8.

The 09:03 post-log `newtune.xml.emub3` reads `idleOpenLoopOverVss=400` (the owner intended
400 km/h to disable this gate), yet the log's force flag still asserts while the displayed
`Vehicle Speed` is only 29…33.  Therefore either this export was not the event's live
calibration or the gate's source/scaling differs from the displayed speed.  Do not compensate by
changing idle-air tables until that discrepancy is resolved; the force flag is authoritative for
this event.
