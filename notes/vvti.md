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
