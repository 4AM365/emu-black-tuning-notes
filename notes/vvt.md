# VVT — EMU Black settings and the principles behind them

> **Software page:** *VVT*. Full symbol catalog: [tune_feature_tree.md → VVT](tune_feature_tree.md). This build runs Toyota **VVT-i** (single intake-cam phaser).

The dedicated VVT document, organized like [idle.md](idle.md):

- **Part 1 — Settings**: one block per EMU Black VVT table — what it is, how to set it, how it
  fails, where the live values + street-tune procedure live.
- **Part 2 — Principles**: how cam advance changes combustion (and therefore MBT), and what sets
  the solenoid PID's authority.

> **Car-specific values live in the build working docs**, not here. For the reference build's VVT
> PID gains, setpoint, and cam-vs-load map see [`supra/notes/`](../supra/notes/) and the
> **`emu-black-vvti-street-tune`** skill. This note is intentionally car-agnostic.

---

# Part 1 — Settings (one block per EMU Black VVT table)

### Cam target map (cam advance vs load / RPM)

- **What it is.** The commanded cam advance the PID drives toward, per RPM × load.
- **How to set it.** Sweep VVT advance at fixed TPS and **take the MAP peak** as peak trapped air
  (V2). Optimize per cell, not globally; lock the cam target per cell **before** pulling ignition
  for MBT, or timing chases a moving target. Re-sweep ignition at any changed cell (V2). Full
  street procedure: **`emu-black-vvti-street-tune`** skill.
- **Failure modes.** Tuning ignition against an unlocked cam target; using one global advance
  across all loads (V1 says the optimum moves with load).
- **Live values:** build doc + the street-tune skill.

### VVT setpoint

- **What it is.** The inflection point between "need more" and "need less" — where all PID
  calculations originate. **The most important parameter.**
- **How to set it.** Set with the engine **fully warmed up** (V3).
- **Live values:** build doc.

### VVT solenoid PID — P / I / D

- **What it is.** The closed loop driving solenoid duty to hold the cam at target.
- **How to set it.** Run a **high P gain** (the initial attack) and rein in overshoot with a
  strong **integral** and **derivative** damping — P-only works but oscillates at the gains you
  want. The **integral** corrects steady-state offset (cam running slightly fast/slow); its
  **correction limit** prevents windup — if accumulated error is large, fix P first. **Derivative**
  suppresses overshoot and lets you run aggressive P. Finalize **fully hot** (V3).
- **Failure mode.** Integral windup masking an under-set P; tuning cold (oil-pressure authority is
  wrong).
- **Live values:** build doc.

### Solenoid output range

- **What it is.** Min/max solenoid duty.
- **How to set it.** Not critical — a wide range (e.g. ~5–90%) is fine; use the **floor** to
  eliminate VVT-i clatter on startup if needed.
- **Live values:** build doc.

---

# Part 2 — Principles

## V1. Cam advance shifts MBT — two competing mechanisms, load decides

VVT-i cam advance is not a free lever: it changes in-cylinder charge composition and effective
compression, so it **moves MBT timing**. Two mechanisms compete and **which dominates depends on
load**:

- **Overlap → residual gas fraction.** Advancing the intake cam grows overlap with the open
  exhaust valve. At **light load** (EMAP > IMAP) exhaust blows back into the intake → more overlap
  = **more residual dilution** → slower flame → **MBT toward more advance**. Under **boost**
  (IMAP > EMAP, reasonable pre-turbine backpressure) fresh charge scavenges residuals out → more
  overlap = **less dilution** → faster burn → **MBT toward less advance**.
- **IVC → effective compression.** Advancing the cam also moves intake-valve-closing earlier,
  trapping more air before compression starts → higher effective CR → faster flame → **MBT toward
  less advance** at low RPM. At high RPM air-column inertia (ram) can flip this at the engine's
  tuned resonance.

Net heuristics: **cruise/light load** → cam advance moves MBT *toward more* advance; **boost/high
load** and **low RPM** → *toward less* advance; **high RPM** → effects can flip at resonance.

## V2. The cam table and the ignition table are coupled

Because cam position moves MBT (V1), **changing the cam table shifts optimum ignition at the
affected cells** — plan to re-sweep ignition there afterward ([ignition.md → I5](ignition.md)).
Cam advance also moves light-load EGT, idle stability, part-throttle drivability, and knock margin,
so **optimize per operating point, not a single global advance**. Boost scavenging is a real
performance lever (a few % torque + valve/chamber cooling) **only while pre-turbine backpressure
stays below intake pressure** — at high PR (small turbine, high boost) the margin closes and the
benefit disappears. When sweeping on the street, **trust the MAP peak at fixed TPS**: MAP is the
direct trapped-air-mass signal and nets overlap + IVC + ram without modeling them (per
`emu-black-vvti-street-tune`).

## V3. Oil pressure and temperature set the PID's authority

The PID's forcing function is **oil pressure physically moving the cam**, so its authority changes
significantly with oil pressure and temperature. **Finalize the VVT tune fully hot.** Some tuners
disable VVT cold; the floor of the solenoid range can also be used to eliminate startup clatter.

---

## Related documents

- [ignition.md](ignition.md) — base timing; cam/ignition coupling (V2 = I5)
- [fueling.md](fueling.md) — VVT moves you within the existing MAP-indexed VE map (no discrete VVT-state fuel corrections needed if the MAP axis covers the range)
- [boost.md](boost.md) — pre-turbine backpressure sets whether boost scavenging pays (V2)
- `emu-black-vvti-street-tune` skill — the full MAP-peak street sweep procedure
