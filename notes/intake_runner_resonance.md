# Intake runner resonance — can you back-calc runner length from the VE table?

> **Software page:** *Fuel → VE table*. Related: [vvt.md](vvt.md) (IVC moves the tuning),
> [per_cylinder_trim_ffim_distribution.md](per_cylinder_trim_ffim_distribution.md).

## Question
Work backward from `veTable` (16 MAP × 20 RPM, u12) to the intake resonance RPM, then invert
a resonance model for effective runner length L. Measured valve→plenum: **Supra (2JZ) ≈ 8 in**.
Bradley (1JZ) ≈ 12 in — **but see the hard caveat below.**

## ⚠ Only validate against MEASURED tables
**Bradley's veTable is currently an unmeasured GUESS** (seeded from a known-good shape, not
tuned from 1JZ data). Its broad VE peak (~5000–5400 rpm) is therefore **not physical data**
and must not be used to test or fit any model. An earlier version of this note ran a
"cross-car ratio test" (Bradley/Supra peak ratio 0.95) and claimed it selected the Helmholtz
model and that one order K≈5.5 reproduced both measured lengths. **That was circular and is
retracted** — it fit physics to a fabricated table. Lesson: two different engines whose VE
tables look alike is the fingerprint of a copied/guessed calibration, not evidence.

## What the Supra table (real, autotuned) shows
- 93 kPa NA column, raw counts (peaks scale-free): single **broad** peak ≈ **5300–5600 rpm**,
  no sharp harmonic ripple (machine-smoothed → ripple filtered out).
- Single-car back-calc, Helmholtz `f_H=(a/2π)√(A/LV)`, a=350 m/s, runner ID≈44 mm,
  V=Vcl+Vd/2, assumed order K≈5.5 → **L≈8.9 in** vs measured 8. Consistent, but **soft**:
  - the broad peak is likely dominated by cam/port/exhaust breathing, not intake resonance
    (5000–5500 rpm is over-determined);
  - runner area A (linear in L), V convention/CR, charge-temp (a∝√T), and order K are all
    assumed (±10–20% each). Treat as order-of-magnitude corroboration, not a measurement.
- Quarter-wave organ-pipe `f=a/4L` would give sharp harmonics and needs an implausible order
  (~9) to land at 5460; the smooth single peak is more Helmholtz-like. (Single-car, so this is
  a weak preference, not the "test" the retracted version claimed.)

## Forward use — seeding Bradley's table from the Supra's
The point of the runner-length physics is **forward**, not inverse: how should a 1JZ VE table
differ from the 2JZ one we copy it from? Helmholtz `f∝√(A/LV)`:
- Runner 8→12 in (×1.5) pushes the intake-tuning component **down** ~ /√1.5;
- but the smaller 1JZ cylinder (V ratio ≈0.83) pushes it **back up** by ~√1.2;
- net intake-tuning RPM shift ≈ **−10%** — *second order*.
The **dominant** differences (1JZ shorter stroke→higher-revving, plus unknown cam/VVT, turbo,
head/port) set the peak and are **not derivable** from the tune. So: copy the Supra's measured
VE *shape* as a seed (axes already rev-extended to 8200), run safe-rich, and **build the real
1JZ table from logs/autotune**. Don't pre-bake a resonance reshape larger than the ~10%
second-order shift; the real engine differences swamp it. Get 1JZ cam/turbo/injector/head
specs before attempting anything better than a copy.

## To measure it for real (either engine)
Compute air-VE from a log (MAP, IAT, RPM, inj PW, λ → trapped air mass) at fixed NA load,
**VVT locked**, un-smoothed → the true peak and any ripple appear and L inverts cleanly.
