# VVT (VVT-i)

> Digest of [vvt.md](../vvt.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** the cam target map, the VVT setpoint and solenoid PID, and why cam advance moves MBT — so cam and ignition tables are coupled.

**The rules:**

- Cam advance moves MBT. Lock the cam target per cell before pulling ignition, or timing chases a moving target; re-sweep ignition at any cell you change.
- The optimum advance moves with load — never run one global advance. Light load: overlap adds residual dilution, MBT wants *more* advance. Boost and low RPM: scavenging and earlier IVC speed the burn, MBT wants *less*. High RPM can flip at resonance.
- The sweep signal depends on the cell. Boost/near-WOT: MAP peak at fixed TPS = trapped air — trust it. Throttled cruise: the signal inverts — rank cells by minimum injector pulse width at fixed speed (the economy winner), bounded by combustion stability, then re-find MBT.
- The VVT setpoint is the most important parameter — every PID calculation originates there. Set it fully warmed up.
- PID: run high P for the initial attack, integral for steady-state offset, derivative to suppress overshoot. If the integral winds up, the real problem is an under-set P — fix that first.
- Oil pressure is what physically moves the cam, so finalize the whole VVT tune fully hot; a cold tune has the wrong authority.
- Solenoid output range isn't critical (~5–90% is fine); use the floor to kill VVT-i startup clatter.
- Boost scavenging pays (a few % torque plus valve cooling) only while pre-turbine backpressure stays below intake pressure — at high pressure ratio the benefit disappears.

**When to care:** before editing the cam target map, after any cam change that shifted MBT at affected cells, and during any VVT PID or hunting work — always with the engine hot.
