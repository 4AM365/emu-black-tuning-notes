# Exhaust note tuning

> Digest of [exhaust_noise_tuning.md](../exhaust_noise_tuning.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** what actually sets an exhaust's sound — the engine's pulse train (source) vs the pipes and muffler (filter) — and which part moves pitch, timbre, drone, and rasp.

**The rules:**

- Everything you hear = source spectrum × duct/muffler filter, plus flow noise and shell breakout. Know which half a part acts on before swapping it, or you'll chase the wrong one.
- Pitch is RPM × cylinder count, nothing else: `f_fire = (RPM/60) × (N_cyl/2)`. Displacement, bore, and material never change the fundamental.
- Material is a timbre knob only — it changes shell breakout, not gas acoustics. Thick mild steel = dull and quiet; thin titanium = bright and ringy. It won't change loudness targets or tuning.
- Cam acts on the source: overlap and tight LSA make the lopey idle, advanced EVO makes the crack/bark. A wild cam through a quiet muffler still lopes, just softly.
- Bore straddles both halves. Undersize = raspy and restricted (plus back-pressure cost); oversize = hollow, droney, loses low-end fullness.
- Cruise drone is a standing wave landing on the firing frequency. Don't chase it with bore or material — kill it with a quarter-wave stub `L = c/(4·f_drone)` or Helmholtz resonator, using hot-gas c.
- Want sharp and raspy: straight-through absorptive muffler and slightly-undersized bore are the two big movers. A turbo works against you — the turbine is roughly a third of a muffler.

**Key numbers:** inline-6 firing frequency ≈ 40 Hz at 800 rpm, 150 Hz at 3000. Hot-exhaust speed of sound ~500–550 m/s (not 343) for resonator sizing.

**When to care:** picking exhaust parts (muffler type, bore, material), diagnosing cruise drone, or predicting how a cam swap changes the sound.
