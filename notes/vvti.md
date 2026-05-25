# VVT-i PID Tuning

## Solenoid Output Range

Max and min solenoid output aren't critical — I use 5% to 90% to keep the range wide. You could use the floor to eliminate VVT-i clatter on startup.

## Setpoint

The setpoint is where all calculations originate and is the inflection point between "we need more" and "we need less." It's the most important parameter. Set the system with the engine fully warmed up. Some tuners disable VVT-i entirely when cold.

## PID Overview

**Proportional** — the initial attack. You want a high P gain; you can rein it in with a strong integral.

Think of it like chasing a car moving away from you. You approach it, but if you go too fast without slowing down you'll overshoot.

- Proportional control varies the command in proportion to the error between current position and target. As the error shrinks, duty cycle decreases.
- If the system is running slightly fast or slow, integral control measures that offset over time (an integral is the area under a curve) and adds or subtracts duty cycle to squeeze the error down.
- Proportional-only control can work, but high P gain causes overshoot. You need damping to allow aggressive P without oscillation.

**Integral** — corrects steady-state offsets by accumulating error over time and nudging duty cycle in the right direction. The integral correction limit prevents windup — if the accumulated error is too large, the proportional term probably needs adjustment first.

**Derivative (damping)** — prevents overshoot, allows more aggressive P, and suppresses oscillation.

## Oil Pressure and Temperature Effects

The forcing function of the PID is oil pressure physically moving the cam. Its authority changes significantly with oil pressure and temperature. Always finalize the tune with the engine fully hot.

---

## How Intake Cam Advance Affects Combustion (and MBT)

VVT-i cam advance isn't a free lever — it shifts MBT timing by changing the in-cylinder charge composition and effective compression. Two mechanisms compete, and **which one dominates depends on load**:

### Mechanism 1: Overlap → residual gas fraction
- Advancing the intake cam opens the intake valve earlier, growing the overlap with the open exhaust valve.
- Whether overlap *adds* or *removes* residuals depends on the pressure differential between intake and exhaust during overlap:
  - **At light load (vacuum)**: exhaust pressure > intake manifold pressure. Exhaust gas blows back into the intake during overlap. More overlap → **more residual dilution** in the next charge → slower flame propagation → **MBT moves toward more advance** (the burn has to start earlier to complete on time).
  - **Under boost**: intake pressure > exhaust pressure (assuming pre-turbo back-pressure is reasonable). Fresh charge scavenges through the cylinder, pushing residuals out the exhaust port. More overlap → **less residual dilution** → faster, cleaner burn → **MBT moves toward less advance** (the burn finishes sooner).

### Mechanism 2: IVC → effective compression
- Advancing the intake cam also moves IVC (intake valve closing) earlier. Earlier IVC traps more air mass before the piston starts compressing → higher effective compression ratio → higher cylinder pressure peak → faster flame speed → **MBT moves toward less advance** at low RPM.
- At high RPM the air column has inertia and a later IVC actually traps more air (ram effect). At low RPM the static effect (earlier IVC = more trapped) dominates.

### Net effect on MBT

The two mechanisms can point opposite ways. Practical heuristics:
- **Cruise / light load**: overlap → more residual dilution dominates. Cam advance → **MBT moves toward more advance**.
- **Boost / high load**: overlap → scavenging dominates (provided pre-turbo back-pressure isn't pathological). Cam advance → **MBT moves toward less advance**.
- **Low RPM, any load**: IVC effect strengthens. Cam advance → **MBT moves toward less advance** (because trapped air mass and effective compression rise).
- **High RPM**: ram tuning interacts; effects can flip at the engine's tuned resonance points.

### Why this matters for tuning

1. **Ignition table and cam table are coupled.** When you change the cam table, the optimum ignition at affected cells shifts. After cam optimization, plan to re-sweep ignition at the changed cells (or accept that the previous ignition is a small bit off MBT now).
2. **Cam advance affects more than torque.** Light-load EGT, idle stability, part-throttle drivability, and knock margin all move with cam position. Optimize for the operating point, not a single global advance value.
3. **Boost scavenging is a real performance lever.** On a well-set-up turbo engine, increasing overlap under boost extracts a few percent of torque by clearing residuals AND cooling the intake valve face / chamber. But the pre-turbo back-pressure needs to be lower than intake boost pressure for it to work — at high PR (small turbine, high boost) this margin closes and the benefit disappears.
4. **MAP-at-fixed-TPS sweeps are robust to this.** When sweeping VVT advance on the street to find peak torque at a cell, MAP is the direct air-mass-trapped signal. It reflects the net of overlap + IVC + ram effects without needing to model them. Trust the MAP peak (per `emu-black-vvti-street-tune`).
