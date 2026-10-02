# Oil pressure (human digest)

**What this covers:** the Supra's measured oil pressure vs RPM and coolant temp,
whether it's healthy, and the sensor/protection setup. Canonical: `../oil_pressure.md`.

**The rules**
- Sensor is a 0.5–4.5 V sender on analog input 204, tapped **post-filter on the
  sandwich plate** — the right spot (reads gallery-feed pressure + catches filter
  restriction). Logged channel is in **bar**.
- Verdict: **healthy, if anything on the robust side.** Clears every minimum by 2–3×.
- Cold + high RPM rides ~9 bar (132 psi) — relief-limited, normal; just warm the oil
  before flogging.
- After a soak, oil reaches the tap after **~45–55 crank revs** (a refill volume), so it
  arrives after the afterstart flare. More post-start RPM doesn't prime oil faster per rev,
  and cold it's already on the relief.
- The ECU's low-oil-pressure cut/failsafe is **switched OFF**. Enabling a conservative
  warning/cut is available as cheap insurance (optional, not urgent).

**Key numbers (hot, CLT ≥95 °C)**
- Idle (~950 RPM): ~2.2–2.5 bar / 32–36 psi (lowest sustained ~1.4 bar / 21 psi).
- 3000 RPM: ~5.3 bar / 76 psi.
- 3500+ RPM: plateaus ~6.0–6.3 bar / 88–92 psi (on the relief valve, pump has margin).
- Cold (28–50 °C): up to ~9.1 bar / 132 psi at RPM.

**When to care:** if hot idle ever sits below ~1 bar (15 psi), if the high-RPM plateau
sags over time (pump/relief wear), or if the post-filter reading drops relative to
history at the same RPM/temp (filter restriction). None present as of 2026-07-12.
