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

**The resonance is a whole-cavity mode — the standing wave spans the entire gas body in the bore, not
an isolated sub-volume.** The question is *what fills that cavity when knock fires*: the medium is the
**bulk gas**, which at the moment of knock is **~uniformly hot burned products**, so `c` is the
**burned-gas** sound speed (~978 m/s), NOT the unburned/fresh charge and NOT a volume-average. Why the
bulk is burned: knock fires ~10–12° ATDC, when mass-fraction-burned is already high (~70–95%) — the
flame has swept most of the chamber and the autoigniting end-gas is the *trigger*, not the *medium*. The
small residual unburned end-gas pocket (cooler, `c ≈ 600 m/s`) drags the local mode down slightly but
occupies little volume late in the burn, so it's a minor perturbation.

The constant proves it empirically: the unburned charge (~750 K, M≈29, γ≈1.33) has `c ≈ 535 m/s` → an
86 mm bore would resonate at ~3.6 kHz and EMU's constant would be ~490, not 900. `F = 900/(π·R)` only
works on the hot burned-gas `c ≈ 978 m/s` (≈6.66 kHz at 86 mm, which is what sensors actually see). This
is why §6 derives the ~2400 K burned-gas temperature, and why every sensitivity lever (§5: ethanol,
water injection, rich) acts on **flame temperature**, not intake/charge temp — if the medium were the
unburned charge, IAT and boost would set the band, and they essentially don't.

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

`F₁ = 900/(π·R) = 572.96 / bore(mm)`, then `F₂ = F₁ × 1.66`, `F₃ = F₁ × 2.08` (exact Bessel ratios
1.6589 / 2.0811). Sorted by bore; all values in **kHz**.

| Engine | Bore (mm) | Mode 1 ×1.00 | Mode 2 ×1.66 | Mode 3 ×2.08 |
|--------|-----------|--------------|--------------|--------------|
| Honda Goldwing GL1800 (flat-6) | 74.0 | 7.74 | 12.85 | 16.11 |
| Honda B-series (B16 / B18C) | 81.0 | 7.07 | 11.73 | 14.72 |
| Mitsubishi 4G63 (Evo / DSM) | 85.0 | 6.74 | 11.18 | 14.03 |
| Honda K20 · Nissan SR20DET | 86.0 | 6.66 | 11.05 | 13.86 |
| Toyota 2JZ-GTE · 1JZ-GTE | 86.0 | 6.66 | 11.05 | 13.86 |
| Nissan RB25DET · RB26DETT | 86.0 | 6.66 | 11.05 | 13.86 |
| Honda K24 (K-series) | 87.0 | 6.59 | 10.93 | 13.71 |
| Ford Coyote 5.0 | 92.2 | 6.21 | 10.31 | 12.93 |
| Nissan VR38DETT (R35 GT-R) | 95.5 | 6.00 | 9.95 | 12.49 |
| GM LS1 / LS6 (5.7L) | 99.0 | 5.79 | 9.60 | 12.04 |
| Subaru EJ25 (WRX / STI) | 99.5 | 5.76 | 9.55 | 11.98 |
| Toyota 1FZ-FE (Land Cruiser) | 100.0 | 5.73 | 9.50 | 11.92 |
| Chevy SBC 350 (4.00″) | 101.6 | 5.64 | 9.36 | 11.74 |

> **Bore is the whole story.** The K20, SR20DET, and the four JDM inline-sixes (2JZ, 1JZ, RB25, RB26)
> all share an **86 mm bore** → identical 6.66 kHz fundamental regardless of displacement, stroke, or
> CR (see §5). Across this entire list the fundamental only spans ~5.6–7.7 kHz.
>
> *Goldwing:* 2001–2017 GL1800 = 74 mm (7.74 kHz); 2018+ GL1800 = 73 mm (7.85 kHz) — same band in
> practice. *1FZ-FE:* factory 100 × 95 mm. *LS varies by displacement* — the 6.2L LS3 is 103.25 mm
> (~5.55 kHz). A typical few-thou overbore moves any of these <1% — ignore it.

## 5. What moves the band — and why bore is the only one that matters

```
KNOCK FREQUENCY
│
└─ Draper eq:   f = α · c / (π · B)
   │
   ├─ B  bore ........................ DOMINANT — this sets the band
   │
   ├─ α  Bessel-function root ........ exact mode selector (×1.00 / 1.66 / 2.08)
   │
   └─ c  speed of sound (burned gas) = √(γ · Rᵤ · T / M)
      │
      ├─ CR ......................... via compression baseline T = T·CR^(γ-1) . negligible  (~0.5%)
      │
      ├─ water injection ........... via charge temperature T (latent heat) .. largest 2nd-order (~1–4%)
      │
      ├─ mixture richness (λ) ...... via flame temp T (rich → cooler) ........ ~2%  (see §6)
      │
      └─ γ  ratio of specific heats
         │
         ├─ humidity ............... negligible  (<0.5%)
         │
         └─ fuel (ethanol) ........ minor       (~1.5%)
```

Because `f ∝ c` and `c = √(γ·Rᵤ·T / M)`, only burned-gas sound speed can shift the band once bore is
fixed — and every secondary input is small enough to live inside the skirt of a normal filter band:

- **CR 9 → 10 (or back):** `c` moves **~+0.5%** (≈ +30 Hz on a 2JZ). Only the compression baseline
  shifts — `T_compressed = T_ivc·CR^(γ−1)`, ~+25 K per CR point — while combustion adds a roughly fixed
  ΔT on top, so burned-gas temperature barely moves. Full derivation in §6.
- **Ambient humidity:** **<0.5%**. Even saturated intake air is only ~3–4 mol% water; its competing
  effects (slightly lower γ and flame temp, slightly lighter products) nearly cancel.
- **Pump gas → ethanol (E85/E100):** burned-gas `c` drops **~1.5%** (≈ −100 Hz). Lower flame
  temperature (~80–100 K, plus charge cooling) drops `c`; partly offset by lighter, water-rich
  products (ethanol products M≈28.1 vs gasoline 28.6 → +0.9%) and a slightly lower γ.
- **Water / water-meth injection:** the **largest** of the secondary effects, but still **~1–4%**
  (≈ −70 to −270 Hz at aggressive rates). Water's latent heat (~2.26 MJ/kg, ~6× gasoline) is the whole
  point — it attacks charge and flame temperature hard, dropping `c` via √T. Partly self-cancelling:
  the light water molecule (M=18) lowers burned-gas molar mass (raises `c`) and lowers γ. Net a few
  percent lower at heavy rates — bigger than ethanol, but still inside a normally-chosen band.
- **Mixture richness (running rich — e.g. λ0.75 pump at full tilt):** lowers flame temp → `c` down
  **~2%**, same bucket as ethanol/water. Counter-intuitively *more* fuel runs *cooler* past stoich
  (O₂-limited; see §6 for the λ→ΔT fractional-heat math). Bites hardest at full power — exactly where knock
  detection matters most — so the band sits at the low end of its range there, but still in-band.

**Practical upshot:** set the band once from the bore (`6.66 kHz` for the 86 mm sixes). It covers every
fuel blend, CR, humidity, water-injection, and mixture state you'll run — important for the flex-fuel Supra
(0–100% ethanol by fill-up): **no fuel- or condition-dependent knock frequency is needed.** Bore
dominates by ~50×; the rest never leaves the filter band.

*(γ≈1.27 / T≈2400 K burned-gas assumptions are standard thermo, not a corpus table; the stoich
product molar masses and `c=√(γRT)` form are exact.)*

## 6. Where the 2400 K burned-gas temperature comes from (q ÷ cp)

The `c` used in §1–5 assumes burned-gas `T ≈ 2400 K`. That is built from two pieces:

```
T_burned  ≈  T_compressed  +  ΔT_combustion  ≈  750 K  +  1650 K  ≈  2400 K
```

### The 750 K baseline is CR-dependent (adiabatic compression)

`T_compressed` is not a fixed number — it's the intake charge compressed adiabatically, so it scales
with **compression ratio**:

```
T_compressed = T_ivc · CR^(γc − 1)       γc ≈ 1.35 (unburned charge),  T_ivc ≈ 330 K

CR  8  →  330 · 8^0.35   ≈ 686 K
CR  9  →  330 · 9^0.35   ≈ 712 K
CR 10  →  330 · 10^0.35  ≈ 739 K    ← the ~750 K baseline (≈ CR 10, ~330 K trapped charge)
CR 11  →  330 · 11^0.35  ≈ 764 K
```

So **CR enters knock frequency only through this baseline** — the combustion rise below is
~CR-independent (same fuel energy, same charge mass per unit air). A CR point is ~+25 K on a 2400 K
total ≈ +1% on T → **+0.5% on `c`**, which is the §5 CR row. Heywood uses ~700 K / 10 atm for this
end-of-compression state ([ice_fundamentals.md](../corpus/ice_fundamentals.md) §3.6).

### The 1650 K is the combustion rise — an energy balance, `ΔT = q ÷ cp`

```
ΔT_comb [K]  =  q_charge [kJ/kg]  ÷  cp [kJ/(kg·K)]

q_charge  =  LHV × f        LHV ≈ 44,000 kJ/kg_fuel,  f = m_fuel/m_charge = 1/15.7 = 0.064
          =  44,000 × 0.064  ≈  2,800 kJ/kg_charge
cp (burned gas, high-T)  ≈  1.7 kJ/(kg·K)
ΔT  =  2,800 / 1.7  ≈  1,650 K
```

Units cancel to kelvin: `(kJ/kg) ÷ (kJ/(kg·K)) = (kJ/kg)·(kg·K/kJ) = K`. `q/cp` is literally "how many
degrees this released energy heats this gas."

**Caveat:** `cp ≈ 1.7` is an *effective* high-T value. Cold-air `cp = 1.005` would give a ~2,800 K rise
(→ ~3,500 K) — far too hot, because it ignores cp rising with T and energy lost to **dissociation**
(OH, O, H; Heywood §3.6). So 1650 K is a calibrated shortcut, not a rigorous adiabatic-flame-temp calc
(that needs enthalpy tables + equilibrium, §3.6–3.7). It lands near the right T, which is all the
knock-band estimate needs.

### Running rich lowers it — the fractional-heat-distribution math

More fuel past stoichiometric runs **cooler**, not hotter. Work per **unit mass of trapped air** (the
quantity the cylinder fixes at a given MAP/VE) and let `λ` = relative AFR (`λ<1` = rich),
`AFR_s ≈ 14.7`. Two terms of `ΔT = q ÷ (m·cp)` move with λ:

- **Numerator — heat released `Q(λ)`.** Fuel supplied per unit air is `1/(AFR_s·λ)`, but past stoich
  **oxygen caps the burn**: released heat plateaus at `Q₀ = LHV/AFR_s` because only the O₂-supportable
  fuel oxidizes — the rest leaves as **CO/H₂/HC** (Heywood §3.5: rich combustion efficiency "steadily
  decreases as the mixture becomes richer," lines ~5377–5379; rich products carry CO + H₂, line ~5726).
  So `Q` stops climbing at λ=1 and edges *down* beyond it.
- **Denominator — charge to heat `m·cp`.** The excess unburned fuel `Δm_f = (1/AFR_s)(1/λ − 1)` is
  thermal ballast: extra mass, a *higher* specific heat (hot fuel vapor cp≈2.5 vs products ≈1.7), and
  it cools the charge by vaporizing (latent heat) before the burn.

Numerator flat, denominator rising → ΔT falls. The pure-dilution floor (`Q≈Q₀`, ignoring the cp bump)
is a clean closed form:

```
ΔT(λ) / ΔT(1)  =  (AFR_s + 1) / (AFR_s + 1/λ)
```

| λ (rich) | dilution-floor ΔT | real (+ ballast cp, latent, CO/H₂ equilibrium) |
|----------|-------------------|------------------------------------------------|
| 1.00 | 0%    | 0% |
| 0.90 | −0.7% | ~−1 to −2% |
| 0.85 | −1.1% | ~−2 to −3% |
| 0.80 | −1.6% | ~−3 to −4% |
| 0.75 | −2.1% | ~−4 to −6%  (≈ 100–150 K) |
| 0.70 | −2.7% | ~−5 to −7% |

The dilution term alone is small (~2% at λ0.75); the real drop is roughly **double** once the
excess-fuel heat capacity, latent cooling, and equilibrium (CO/H₂) losses are added. Heywood's full
adiabatic-flame-temp curve (Fig 3.13) peaks *slightly* rich (line ~5742: *"Maximum flame temperatures
occur slightly rich of stoichiometric"*) and is down **~100–150 K** by λ0.75.

**Effect on the band:** ~100–150 K on a 2400 K burned gas is ~4–6% on T → via `c ∝ √T`, ~−2–3%, partly
offset by lighter rich products (CO/H₂ lower M, raise `c`) → **net ~−2%** (≈ 6.66 → ~6.5 kHz on an
86 mm bore). *(This corrects an earlier ~150–250 K estimate — the constant-property energy balance caps
the drop lower than that.)* It stacks with ethanol + water injection (all lower flame temp), but even
combined stays inside a normal filter band. The irony: at **full-tilt rich** — where knock detection
matters most — the resonance sits at the **low end** of its range; center the band on the dry-stoich
value and it still captures the hot-rich peak.

### Temperature drop ≠ energy shed (don't read the ΔT column as energy)

The ΔT column above is **temperature**, not energy. The **chemical energy shed** going rich is a
separate, much larger number — the fraction of *injected* fuel energy you fail to release, which is
essentially the **excess-fuel fraction `1 − λ`**:

```
energy shed  ≈  excess fuel / injected fuel  =  (m_f − m_f,stoich)/m_f  =  1 − λ
```

The excess fuel has no O₂ left to burn (O₂-limited), so to first order its whole heating value leaves as
CO/H₂/HC.

| λ | fuel injected (1/λ) | **energy shed ≈ 1−λ** | burned-gas ΔT (the col above) |
|------|------|------|------|
| 1.00 | 1.00× | ~4% (stoich residual) | 0% |
| 0.90 | 1.11× | ~10% | ~1–2% |
| 0.85 | 1.18× | ~15% | ~2–3% |
| 0.80 | 1.25× | ~20% | ~3–4% |
| 0.75 | 1.33× | **~25%** | ~4–6% |
| 0.70 | 1.43× | ~30% | ~5–7% |

**Why they differ so much:** the *absolute heat released* is ~constant (oxygen-capped — it can't exceed
what the fixed air charge supports, ~2,900 kJ/kg air either way). So temperature falls only because that
near-constant heat is **spread** over more mass + higher-cp fuel ballast + latent cooling (dilution, not
loss → the small ΔT column). The shed energy is large because its denominator is the *injected fuel* —
the extra ~33% fuel at λ0.75 does ~zero thermal work and is dumped. **Practical read:** running λ0.75
for EGT/knock margin throws away ~25% of that added fuel as cooling insurance, not power — correct when
deliberate, but it quantifies the cost of going richer than the cooling actually needs.

---

## Related documents

- [knock_sensors.md](knock_sensors.md) — the *Knock sensors* software page (detection, retard, CoV)
- [knock_sensor_baseline_vs_cylinder_uniformity.md](knock_sensor_baseline_vs_cylinder_uniformity.md) — knock variance as a uniformity proxy
- [ignition.md](ignition.md) — the timing tables knock constrains
