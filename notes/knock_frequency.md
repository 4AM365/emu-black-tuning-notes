# Knock resonance frequency — bore → frequency band

> Cross-cutting reference note for [knock_sensors.md](knock_sensors.md) (the *Knock sensors*
> software page). This page derives **where to put the knock-detection band** from the bore, why
> ECUMaster's `900` constant is what it is, and why the higher modes are **not** integer harmonics.

---

## 1. The formula

Knock is an **acoustic resonance of the burned gas** trapped in the cylinder, not a vibration of the
metal. The end-gas autoignites, launches pressure waves across the chamber, and they settle into the
standing-wave modes of the (roughly) cylindrical gas cavity. The sensor hears the block ringing at
those gas-mode frequencies (EMU quotes the resulting block vibration as **3–20 kHz**).

The dominant mode is the **first circumferential mode** — gas sloshing side-to-side across the bore.
Its frequency is the **Draper equation**:

```
f = α · c / (π · B)
```

- `α` = the mode constant — a **root of the derivative of the Bessel function** `J′ₘ(x)=0` (see §3)
- `c` = speed of sound in the **burned gas** (~960–980 m/s at combustion temperatures)
- `B` = bore diameter

For the first mode `α₁,₀ = 1.8412`. Bigger bore → wider cavity → **lower** knock frequency.

## 2. ECUMaster's simplified `F = 900 / (π·R)` — where the 900 comes from

EMU Black's help gives the working form (R = cylinder **radius** in mm, F in kHz):

```
F = 900 / (π · R)
```

This is the Draper equation with the physics collapsed into one number. Rewrite Draper with `B = 2R`:

```
f(kHz) = α · c / (π · 2R)  =  (α·c/2) / (π·R)
```

So ECUMaster's constant is **`900 = α·c/2`**. Back-solve for the sound speed it assumes:

```
c = 1800 / α = 1800 / 1.8412 ≈ 978 m/s
```

i.e. the `900` bakes in **the first Bessel root (1.8412)** *and* **an assumed burned-gas sound speed
of ~978 m/s**. That ~978 m/s is consistent with first-principles burned-gas conditions (γ≈1.27,
T≈2400 K, M≈28.6 g/mol → c≈941–978 m/s), so the constant is physically sound. It uses **radius**, not
diameter — don't feed it bore.

## 3. Higher modes are Bessel roots, NOT integer harmonics

If the first band sits in valvetrain/piston noise you may want the next mode. **It is not double the
frequency.** A straight organ pipe has harmonics at integer multiples (1f, 2f, 3f) because its modes
are sines with integer wavenumbers. The cylinder is a **2-D circular cavity** whose modes are Bessel
functions, and the roots of `J′ₘ(x)=0` are **not** evenly spaced:

| Mode | (m,n) | Bessel root α | Ratio to 1st (α/1.8412) | Use |
|------|-------|---------------|--------------------------|-----|
| 1st  | (1,0) | 1.8412 | **×1.00** | first circumferential — the fundamental, EMU's default |
| 2nd  | (2,0) | 3.0542 | **×1.66** | second circumferential — next band up if the fundamental is masked |
| 3rd  | (0,1) | 3.8317 | **×2.08** | first radial — rarely needed |

So the modes land at **1.00 : 1.66 : 2.08**, not 1 : 2 : 3. **Doubling (×2.00) lands in a dead zone
between the 2nd and 3rd modes** — you'd be ~20% above the real 2nd resonance and detect nothing. To
move up a mode, multiply the fundamental by **1.66** (2nd) or **2.08** (3rd).

## 4. Knock-frequency table — common bores × modes

`F₁ = 900/(π·R)`, then `F₂ = F₁ × 1.66`, `F₃ = F₁ × 2.08` (using exact Bessel ratios 1.6589 / 2.0811).

| Engine | Bore (mm) | Mode 1 (×1.00) | Mode 2 (×1.66) | Mode 3 (×2.08) |
|--------|-----------|----------------|----------------|----------------|
| Honda K20 (K-series) | 86.0 | 6.66 kHz | 11.05 kHz | 13.86 kHz |
| Honda K24 (K-series) | 87.0 | 6.59 kHz | 10.93 kHz | 13.71 kHz |
| Toyota 2JZ-GTE | 86.0 | 6.66 kHz | 11.05 kHz | 13.86 kHz |
| Toyota 1JZ-GTE | 86.0 | 6.66 kHz | 11.05 kHz | 13.86 kHz |
| Nissan RB25DET | 86.0 | 6.66 kHz | 11.05 kHz | 13.86 kHz |
| Nissan RB26DETT | 86.0 | 6.66 kHz | 11.05 kHz | 13.86 kHz |
| Chevy SBC 350 (4.00″) | 101.6 | 5.64 kHz | 9.36 kHz | 11.74 kHz |

> The four JDM inline-sixes (2JZ, 1JZ, RB25, RB26) and the K20 **all share an 86 mm bore**, so they
> have identical knock bands — 6.66 kHz fundamental. Only bore matters; displacement/stroke/CR don't
> (see §5). K24 and the big-bore SBC are the only ones that move.

## 5. Sensitivity — fuel and CR barely move it; bore dominates

Because `f ∝ c` and `c = √(γ·R_u·T / M)`, only the burned-gas sound speed can shift the band once bore
is fixed. Both common build changes are **sub-2%** — inside the skirt of any reasonable filter band:

- **Pump gas → ethanol (E85/E100):** burned-gas `c` drops **~1.5%** (≈ −100 Hz on a 2JZ). Lower flame
  temperature (~80–100 K, plus charge cooling) drops `c`; partly offset by lighter, water-rich
  products (ethanol products M≈28.1 vs gasoline 28.6 → +0.9%) and a slightly lower γ.
- **CR 9 → 10 (or back):** `c` moves **~+0.4%** (≈ +25 Hz). Pressure cancels in an ideal gas; CR only
  raises the compressed-charge baseline ~18 K, and combustion adds a roughly fixed ΔT on top, so the
  burned-gas temperature barely shifts.

**Practical upshot:** set the band once from the bore (`6.66 kHz` for the 86 mm sixes). It covers
every fuel blend and CR you'll run — important for the flex-fuel Supra (0–100% ethanol by fill-up):
**no fuel-dependent knock frequency is needed.** Bore dominates by ~50×; everything else is noise.

*(γ≈1.27 / T≈2400 K burned-gas assumptions are standard thermo, not a corpus table; the stoich
product molar masses and `c=√(γRT)` form are exact.)*

---

## Related documents

- [knock_sensors.md](knock_sensors.md) — the *Knock sensors* software page (detection, retard, CoV)
- [knock_sensor_baseline_vs_cylinder_uniformity.md](knock_sensor_baseline_vs_cylinder_uniformity.md) — knock variance as a uniformity proxy
- [ignition.md](ignition.md) — the timing tables knock constrains
