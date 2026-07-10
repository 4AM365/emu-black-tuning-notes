# Sport (launch control / 2-step)

> Digest of [sport.md](../sport.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** how EMU Black launch control ("2-step") arms, holds, and releases, the V2 vs V3 symbol split, and the diagnosis of Andrew's intermittent 2-step. Most other Sport features (pit limiter, rolling launch, trans-brake, flat-shift) are unused on this build.

**The rules:**

- LC engages only when ALL gates are true: activation input active, VSS at or below `lcVssLimit`, TPS at or above `lcActivationTPS`, RPM rising into the soft→hard cut band. There is no separate enable — assigning the activation input (`lcInput`) is what turns the feature on.
- VSS climbing past the limit is what releases the limiter on launch. Set it ~3–5 km/h; 1 km/h is tight enough that sensor noise or the car rocking drops LC out.
- Intermittent 2-step root-cause order: (1) flaky activation input — the #1 cause, especially a CAN-sourced switch whose device drops off the bus; (2) VSS limit too tight; (3) TPS/RPM window not consistently met; (4) clutch interlock, if a clutch input is assigned.
- V2 and V3 firmware use different symbol families. V2 is a simple soft/hard limiter — no prestage, no DBW target table, no RPM-target PID. Don't expect V3 names in a V2 tune.
- Andrew's car (v2.175): `lcInput=34` = CAN switch #2, but nothing in the tune sources that switch — the arm bit is effectively unsourced, the likely cause of the intermittent launch. Recommended fix: hardwire a momentary to an EMU switch pin (10/23/36) and point `lcInput` there, taking the bus out of a launch-critical trigger.
- Verify by logging `LC state` alongside each gate (VSS, TPS, RPM, input) rather than guessing.

**Key numbers:** Andrew's set 1 — activation 4000 RPM, hard cut 5000, TPS 40%, VSS limit 1 km/h (too tight), spark cut, no clutch gate.

**When to care:** setting up or debugging launch control — especially an intermittent 2-step — and any time a launch trigger runs through CAN.
