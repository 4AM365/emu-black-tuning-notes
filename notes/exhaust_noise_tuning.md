# Exhaust note tuning — what actually sets the sound

> **Not an EMU software page** — a cross-cutting physics/principle note (like
> [throttle_body_thermal_growth.md](throttle_body_thermal_growth.md)). Covers what governs an
> engine's exhaust *acoustic signature* and which levers move it.

## The one framing that makes everything else fall into place

**What you hear = the engine acoustic SOURCE spectrum × the duct/muffler TRANSFER function**,
plus two parasitic additions: **flow-generated (regenerated) noise** and **shell breakout noise**.

```
  combustion/blowdown pulses          pipes + chambers + resonators
  (SOURCE: set by displacement,  ──►  (FILTER: set by geometry, area      ──►  tailpipe + shell
   cylinders, cam, firing order)       ratios, lengths, lining, temp)          radiation = "the note"
        rich in harmonics              shapes WHICH harmonics survive          + flow noise + breakout
```

Munjal frames the filter half precisely: a muffler works "through impedance mismatch or to
dissipate the incoming sound into heat, while allowing the mean flow to go through almost
unimpeded. The former… are called **reflective, reactive, or nondissipative** mufflers… the latter…
**dissipative or absorptive** mufflers, or simply silencers." In practice every real muffler is a
blend of both (Munjal, *Acoustics of Ducts and Mufflers* 2nd ed., Preface / Ch.1).

**The trap to avoid:** material, bore, and cam do **not** all act on the same half. Cam acts almost
purely on the **source**. Material acts almost purely on **breakout** (the shell), not the gas
acoustics. Bore straddles both. Keep the column "which half" in mind or you'll chase the wrong part.

Two reference quantities used throughout:

- **Firing frequency** (the fundamental pitch) — for a 4-stroke: `f_fire = (RPM/60) × (N_cyl / 2)`.
  Inline-6 at 800 rpm idle ≈ 40 Hz; at 3000 rpm ≈ 150 Hz. **Set by RPM and cylinder count — NOT by
  displacement, material, or bore.** This is why pitch tracks revs and cylinder count, and timbre is
  everything else.
- **Speed of sound** `c = √(γRT)` — every duct resonance scales with `c`, so **exhaust gas
  temperature shifts the whole acoustic signature up or down in frequency.** Hotter gas = higher c =
  features move up. (Munjal's TL/resonance results all assume a specified mean-flow temperature.)

---

## Table 1 — Exhaust material

Material barely touches the **gas-borne plane-wave acoustics inside** the pipe (transmission loss is
set by *geometry, area ratios, and temperature* — not wall metal). What material changes is
**breakout noise** — sound radiated *through the shell wall* — governed by the wall's mass, stiffness,
and damping (panel "mass law"), plus the gas temperature it runs at.

| Material | Density / wall behavior | Effect on note | Which half | Grounding |
|---|---|---|---|---|
| **Mild / aluminized steel** | Dense, higher internal damping, usually thicker wall | Most breakout suppression → **dullest, deepest, "quietest" timbre**; absorbs shell ring | Filter (breakout) | Mass law (general); breakout = Munjal Ch.7 §7.6 |
| **304 / 409 stainless** | Lighter, stiffer, less self-damping; runs hotter (lower conductivity) | More shell ring → **brighter, harder, slightly "raspier"** edge; hotter gas raises c → features shift up in freq | Filter (breakout) + small source-temp shift | Breakout Munjal §7.6; temp→c general |
| **Titanium** | Very light, low damping, holds heat | **Brightest / most metallic ("tinny") timbre**, pronounced shell ring; noticeable high-freq content | Filter (breakout) | Mass law (general) |
| **Inconel / thick-wall race** | Dense + very high temp capability | Like steel for breakout but tolerates pre-turbo / header heat without softening | Filter (breakout) + durability | Durability/temp uniformity = Munjal §8.1(iv) |
| **Ceramic coat / wrap (any base)** | Keeps gas hotter inside | Raises internal c → shifts resonances **up**; reduces radiated heat, mild effect on perceived loudness | Source-side temp | temp→c general |

**Bottom line:** material is a **timbre/brightness** knob (via shell breakout + gas temp), **not** a
tuning or loudness knob. Thicker, denser, better-damped wall = duller and quieter shell; thin Ti =
bright and ringy. It does **not** change the fundamental pitch or the muffler's designed attenuation.

---

## Table 2 — Bore (pipe inner diameter)

Bore is the one that **straddles both halves**. Three distinct mechanisms:

| Mechanism | Larger bore → | Smaller bore → | Half | Grounding |
|---|---|---|---|---|
| **Gas velocity / flow noise** | Lower velocity → less regenerated "rush"; lower back-pressure | Higher velocity → more high-freq **flow-generated rasp/hiss**, more back-pressure | Source/flow | Munjal §6.13 flow-generated noise; §8.1(ix) |
| **Plane-wave cutoff freq** | Lower cutoff → higher-order modes propagate sooner; more high-freq passes differently | Higher cutoff → cleaner plane-wave behavior to higher freq | Filter | Duct theory, Munjal Ch.1 (3-D waves) |
| **Area-expansion ratio into a chamber** | For a *fixed* chamber Ø, bigger pipe = **smaller** area ratio = **less** TL | Smaller pipe = bigger area ratio = **more** chamber attenuation | Filter | Munjal §8.2 (TL rises with area-expansion ratio) |

**Perceived result:** oversize bore tends toward **hollow, droney, "loses low-end fullness"** (velocity
drops, low-rpm pulse energy bleeds, chamber TL falls). Undersize bore tends toward **raspy and
restricted at high flow** but can feel "tighter" low down. Bore is sized for the **back-pressure ↔
power ↔ flow-noise** trade — Munjal lists back-pressure ("affects brake power, volumetric efficiency,
and hence specific fuel consumption") as a top-tier design constraint, §8.1(ii).

---

## Table 3 — Cam (duration, overlap, LSA, EVO timing)

Cam acts **almost entirely on the SOURCE** — it shapes the pulse train *before* any pipe touches it.
Munjal does **not** cover this; grounding is gas-dynamics/combustion (Graham Bell *Four-Stroke
Performance Tuning*; Heywood §6, §15.7).

| Cam parameter | Effect on the source pulse train | Effect on note |
|---|---|---|
| **Duration ↑** | Bigger, later-closing events; rougher low-rpm cylinder filling | More **low-rpm irregularity**; fuller, more aggressive midrange bark |
| **Overlap ↑** (TDC, intake+exhaust open together) | Charge cross-talk, reversion, incomplete low-rpm fill → **uneven pulse amplitudes idle-to-idle** | The classic **lopey / choppy "cammed" idle** sound |
| **LSA tighter** (e.g. 108° vs 114°) | More overlap for a given duration → more idle dilution variance | Choppier, "nastier" idle; LSA is the dominant idle-character knob |
| **EVO advanced** (exhaust opens earlier) | Higher cylinder pressure at blowdown → **sharper, higher-amplitude pulse front** | More high-freq content → **"crack/bark"**, louder leading edge |

**Bottom line:** cam sets the **rhythmic regularity and pulse sharpness** of the source — the "character"
(lope, bark) — not the muffler filtering. A wild cam through a quiet muffler still *lopes*, just softly.

---

## Table 4 — Other key parameters (often bigger levers than the three above)

| Parameter | What it sets | Half | Grounding |
|---|---|---|---|
| **Cylinder count + firing interval** | **Fundamental pitch** (`f_fire` above) and even- vs odd-fire character (inline-6 even = smooth; cross-plane V8 = burble; flat-plane = scream) | Source | General; firing order |
| **Displacement per cylinder** | **Pulse energy/amplitude** → loudness + low-frequency weight. Bigger swept volume per cylinder = bigger, lower, louder blowdown pulse. Big engines also rev lower → lower `f_fire` → deeper note | Source | General; blowdown energy Heywood §6 |
| **Primary/header length + collector** | Tuned scavenging resonance; **equal-length = even pulse spacing** (smooth exotic wail), unequal = burble (boxer rumble) | Source/gas-dyn | Graham Bell |
| **Total system length & diameter** | **Organ-pipe standing waves → drone.** Open-open: `f ≈ n·c/(2L)`; quarter-wave: `f ≈ (2n−1)·c/(4L)` | Filter | Duct acoustics, Munjal Ch.2 |
| **Muffler type — reflective vs absorptive** | Reflective (chambered): selective TL with **"domes and troughs"**, quieter, can drone if a trough sits on `f_fire`. Absorptive (straight-through glasspack): broadband high-freq soak, flows well, raspier, **packing burns out over time** | Filter | Munjal Preface/Ch.2 §2.19, Ch.6; ageing = *Maximum Boost* ch.11 |
| **Helmholtz / quarter-wave resonator** | **Narrow-band drone killer** tuned to one frequency. Helmholtz `f ≈ (c/2π)·√(A/(V·L_eff))`; quarter-wave (J-pipe) `L = c/(4f)` | Filter | Munjal §2.14–2.16, §8.3 (extended-tube/Helmholtz/concentric) |
| **Gas temperature** (turbo, ceramic coat, insulation) | Scales `c` → shifts **all** resonances; a **turbine is ~⅓ of a muffler** and drops the note hard | Both | *Maximum Boost* ch.11; temp→c general |
| **Back-pressure target** | The master trade: insertion loss ↔ back-pressure ↔ size/durability. Quieter usually costs flow | Filter | Munjal §8.1 (requirements list) |

---

## The actionable lever for the usual complaint (cruise drone)

Drone is almost always a **standing-wave resonance** of the full system landing near the firing
frequency at a common cruise RPM. Don't chase it with bore or material — **tune it out with a
resonator** sized to that frequency:

1. Find the drone frequency: `f_drone = (RPM_cruise/60) × (N_cyl/2)`.
2. Kill it with a **quarter-wave (J-pipe)** stub of length `L = c/(4·f_drone)` (use hot-gas `c`,
   ~500–550 m/s in a street exhaust, not 343), or a **Helmholtz** resonator tuned to `f_drone`.

Munjal: the branch/quarter-wave resonator "acts primarily as an impedance mismatch element, ensuring
that hardly any power leaves the source at the resonance frequencies" (§2.14–2.16). That's exactly the
narrow-band notch you want for drone.

---

## Recipe: a sharp, raspy note (levers ranked)

**Sharp** = a hard, high-amplitude pulse front (a *crack/bark*) — comes from the **source**.
**Raspy** = sustained high-frequency content (a *buzz/hiss*) — comes from **letting the highs
through**. Both live at the high-frequency end, so every ideal choice is "produce more highs, or
suppress fewer." Ranked by leverage:

| # | Lever | Ideal choice | Half | Why | Cost |
|---|---|---|---|---|---|
| 1 | **Muffler type** | Straight-through **absorptive** glasspack / perf-core; minimal reflective chambers | Filter | Reflective chambers notch out highs; absorptive passes them broadband — the highs *are* the rasp | Loud everywhere; packing burns out |
| 2 | **Bore** | **Slightly undersized** (high gas velocity) | Source/flow | Velocity drives flow-generated rasp; raises area-ratio → less chamber TL | Back-pressure → VE/power loss |
| 3 | **Cam** | **Long duration + advanced EVO + tight LSA** | Source | Advanced EVO → higher blowdown pressure → sharper, louder pulse front; tight LSA → ragged idle edge | Idle quality, low-rpm driveability |
| 4 | **Aspiration / gas temp** | **NA**, hot/short, no insulation | Both | A turbine is ≈⅓ of a muffler and eats highs; hotter gas raises `c`, shifting energy up | Impossible on a turbo build |
| 5 | **Material** | **Thin-wall titanium** (or thin stainless) | Filter (breakout) | Light, low-damping wall rings → bright, metallic shell breakout | Tinny; durability |
| 6 | **Resonator** | **Delete** Helmholtz / quarter-wave | Filter | Those are narrow-band notches that remove highs — keep them and you lose rasp | Cruise drone returns |
| 7 | **Header** | **Equal-length short primaries, abrupt collector** | Source/gas-dyn | Crisp, evenly-spaced pulse fronts = clean sharp edge (vs cast-manifold mush) | Fab cost / packaging |
| 8 | **Architecture** (fixed) | **More cylinders + small displacement/cyl + high redline** | Source | Higher firing freq → brighter/raspier; big swept volume/cyl makes a low *thud*, not a rasp | Not changeable post-build |

**#1 and #2 are the two biggest movers** and the ones to turn first. On a turbo even-fire I6 (e.g. a
2JZ), lever #4 works hard against you and the architecture (#8) caps the ceiling — a sharp/raspy
result then leans almost entirely on #1 (straight-through absorptive, post-turbo) and a tight
downpipe bore; you won't get a flat-plane rasp out of it.

## Sourcing / honesty note

- **Munjal, *Acoustics of Ducts and Mufflers* (2nd ed., 2014)** is the authority for the **filter half**
  — reflective vs dissipative action, TL of expansion chambers, resonator tuning, breakout, flow noise,
  and the §8.1 design trade-offs. In-repo retrieval extract:
  [corpus/acoustics_of_ducts_and_mufflers.md](../corpus/acoustics_of_ducts_and_mufflers.md)
  (source `.epub` + ref card in `../../reference/agentic-library/engine-dynamics/`).
  **The extract carries no equations** — formula *forms* above
  (`c/4L`, Helmholtz, mass law, `f_fire`) are standard duct acoustics; for the exact transfer matrices
  open the `.epub`.
- **Source half** (cam, displacement, firing, header tuning) is **not** Munjal's domain — grounded in
  Graham Bell *Four-Stroke Performance Tuning* and Heywood §6/§15.7 ([corpus](../corpus/ice_fundamentals.md)).
- The **turbo "≈⅓ of a muffler"** line is Corky Bell, *Maximum Boost* ch.11
  ([maximum-boost/chapter-11-exhaust-systems.md:266](../maximum-boost/chapter-11-exhaust-systems.md)).
