# Valve timing, cam advance, and dynamic compression — equations

> **Software page:** *VVT* (cam phasing) feeding *Fuel → VE*. Use these to model — not
> eyeball — what advancing/retarding an intake cam does. Grounding: Heywood on low-speed
> backflow/reversion lowering VE (`corpus/ice_fundamentals.md`, "backflow of burned gases
> ... into the intake manifold"); Bell on cam advance trading top-end for bottom-end
> (`corpus/four_stroke_performance.md`). Kinematics below are standard slider-crank.

## Cam-event geometry (all CRANK degrees)
For an intake cam of duration `D_i`, lobe-separation `LSA`, advanced `A` from straight-up:
```
ICL      = LSA − A                 # intake centerline, °ATDC
IVO_BTDC = D_i/2 − ICL             # >0 opens before TDC
IVC_ABDC = ICL + D_i/2 − 180       # >0 closes after BDC
overlap  = IVO_BTDC + EVC_ATDC     # EVC_ATDC = D_e/2 − LSA  (exhaust fixed if VVT is intake-only)
```
Advancing the intake cam by A: IVO earlier (**overlap +A**), IVC earlier (**−A ABDC**).
Unit note: EMU cam tables are crank-referenced. **A crank° = A/2 cam°.** If a spec is in
cam degrees, double its crank effect (19 cam° = 38 crank° — usually too much overlap).

## Dynamic compression ratio (slider-crank, exact)
```
r = stroke/2 ;  Ap = π·bore²/4 ;  Vd = Ap·stroke ;  Vc = Vd/(SCR−1)
s(θ)   = r(1−cosθ) + L − √(L² − r²sin²θ)      # piston from TDC, L = rod length
V(θ)   = Vc + Ap·s(θ)
DCR    = V(θ_IVC)/Vc ,  θ_IVC = 180 + IVC_ABDC   # on the compression upstroke
```
Cranking pressure (illustrative, polytropic n≈1.3): `P ≈ P_atm·DCR^n`.

## Low-rpm trapped charge (reversion proxy)
At low rpm (quasi-static) the piston pushes charge back out until IVC, so
`VE_lowrpm ∝ V(θ_IVC)/V_BDC`, `V_BDC = Vc+Vd`. Earlier IVC ⇒ less give-back ⇒ higher
low-end VE. (At high rpm column inertia/ram reverses this — late IVC fills better — so
advance trades top-end for bottom-end.)

## Worked: Bradley 1JZ + 272 intake, advancing 0→19 crank° (LSA 114 assumed, rod 142.5, SCR 9)
| adv° | ICL | IVC ABDC | overlap | DCR | V_IVC/V_BDC |
|---|---|---|---|---|---|
| 0  | 114 | 70 | 44 | 6.82 | 0.758 |
| 19 | 95  | 51 | 63 | 7.82 | 0.869 |

- **DCR 6.82→7.82 (+15%)** — pulls anemic dynamic compression into the streetable 7.5–8.5
  band; better low/mid torque, idle stability, cold start (~164→198 psi cranking).
- **Low-rpm trapped charge +14.6%** (0.758→0.869) — the 272's reversion loss largely recovered.
- **Overlap 44→63° (+19°)** — the cost. Hurts idle (more so when idle is spark-only, no air
  trim) and high-boost VE on a restrictive exhaust (pre-turbine P > MAP → reversion).
- Robust to LSA: across 110–116°, 19° advance gives overlap 59–71°, DCR 7.73–8.00.

**Verdict pattern:** big advance like 19° is a **mid-load/mid-rpm (cruise/spool) target**,
not a global one — schedule it with VVT, parking/retarding at idle and high boost. This also
pulls the VE peak **down/broader at the bottom**, partly offsetting the duration's peak-up.
