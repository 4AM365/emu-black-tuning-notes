# Stuck-throttle protection vs. brake boosting

> Digest of [stuck_throttle_protection_brake_boost.md](../stuck_throttle_protection_brake_boost.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** why EMU's brake-based stuck-throttle cut kills brake-boost launches, and how to layer protection so the safety net stays real without tripping on you.

**The rules:**

- The built-in box triggers on brake + TPS and never looks at the pedal, so it cannot tell a brake-boost from a stuck throttle. Confirmed on this car: it was cutting brake-boosts at the stock settings.
- Pedal position is the discriminator. A genuinely stuck throttle is open with the pedal *released*; a brake-boost holds the pedal high. Any pedal-referenced protection is inherently brake-boost-safe.
- Make the brake-independent layers primary: dual-TPS plausibility via `Check signal input` (currently None = OFF until the Bosch TB swap lands TPS2; fault code 16384 is this check firing) and the closed-loop DBW position-error monitor (tight error, debounce ~200–400 ms above servo settling).
- Relax the brake box, don't disable it: TPS level 30 → 70, brake timeout 600 → 1500 ms. Raising TPS level is the safer lever — it keeps a fast cut for a WOT-stuck blade and only ignores partial throttle while braking.
- If it still cuts mid-boost, push timeout toward 2000–2500 ms first. Then log a real brake-boost and set TPS level to measured peak + ~10% to recover sensitivity.
- Pair the throttle limp action with a fuel-cut RPM cap. Spring-home (~5–7°) sits well above the 2%-TPS zero-airflow point on this cal, so a plate that fails home still flows enough air to run RPM up.

**Key numbers:** airflow scale 2.0% TPS = 0 airflow, 6.4% = 100%. Stock box: TPS 30% / 600 ms / min RPM 1000. Interim: 70% / 1500 ms. Normal trail-braking peaks ~18% TPS for <0.5 s — the relaxed box never sees it.

**When to care:** before any brake-boost launch, after an unexplained cut mid-boost with the brake covered, and when the Bosch TB swap makes dual-TPS live (then relax the brake box further).
