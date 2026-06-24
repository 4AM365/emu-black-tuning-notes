# Piston-to-valve clearance & cam-advance tolerance (2JZ-GTE)

First-principles geometry for "how much intake cam advance before valve collision," worked for a
high-lift cam (GSC S2) on a 2JZ-GTE. Cross-cutting reference; not an EMU software page.

## The collision mode that matters

On the 2JZ pent-roof 4-valve head the intake and exhaust valves are spatially separated — they
**cannot strike each other**. The only valve collision is **valve-to-piston**, and on the intake
side it pinches near **TDC overlap**: the piston is parked at the deck while the intake valve is
cracking open. Minimum clearance lands a few degrees *after* TDC (piston velocity ∝ sinθ is near
zero at TDC, so the fast-moving valve briefly closes the gap before the piston outruns it).

## Piston kinematics (2JZ: bore 86, stroke 86, rod 142)

r = 43 mm, L = 142 mm, r/L = 0.303. Drop below deck vs crank angle θ ATDC:

    drop(θ) = r(1−cosθ) + L(1 − √(1 − (r/L)²sin²θ))

| θ ATDC | 5° | 7° | 10° | 15° | 20° | 25° | 30° |
|--------|------|------|------|------|------|------|------|
| drop (mm) | 0.21 | 0.42 | 0.85 | 1.90 | 3.36 | 5.20 | 7.40 |

## Lift model

Raised cosine per lobe (peak Lmax at the centerline CL, zero at ±duration/2):

    lift(θ) = Lmax · (1 + cos(2π(θ−CL)/dur)) / 2,  clamped to 0 outside ±dur/2

Overstates the near-seat flank slightly → **conservative** (predicts contact early). Good enough for
a "roughly" estimate; clay-test is the real authority.

Clearance(θ) = **K** + drop(θ) − lift(θ), where K = closed-valve-to-piston-crown gap at TDC.

## Cam specs used

- Stock 2JZ-GTE intake: ~233° adv duration, ~8.25 mm lift, ~115° CL → opens ~1.5° BTDC (tiny overlap).
- **GSC S2** (billet, VVTi & non-VVTi): intake **274° adv / 239°@0.040″ / 10.20 mm / 110° CL**;
  exhaust 274° / 10.50 mm / 118° CL. Requires re-shimming (⇒ non-stock, reduced base circle) and
  upgraded springs; VVTi version needs bucket-bore / casting clearance checks. Base circle/shim only
  set lash & seating — they do **not** move the V-P numbers; the published lift profile already is
  what the valve does once lashed.

## The key number: K ≈ 9.5 mm (stock GTE)

A reported OEM 2JZ-GTE measurement: **~9.5 mm** closed-valve-to-piston gap at TDC, tolerating
**~9.7 mm of valve lift at TDC before contact** (incl. lash). Stock intake lift 8.25 mm < 9.7 mm ⇒
the GTE is **non-interference / free-running** with stock cams. The dished low-compression GTE piston
with deep valve reliefs is what buys this. (Varies with gasket/deck/pistons; GE high-comp pistons
have less. Clay-test to confirm.)

## Conclusions

1. **Normal-running P-V clearance is large**, not marginal. With K = 9.5 mm: stock cam dips only to
   ~9.5 mm, S2 @ 0° advance to ~8.4 mm, S2 @ +15° advance to ~7 mm — all far above the 0.080″
   (2.0 mm) street floor. **An early K=3 mm assumption was ~3× too pessimistic** and made the S2
   look like it had no advance headroom; with the real geometry it has lots.
2. **Marginal loss with advance ≈ 0.09–0.10 mm of intake clearance per crank degree** near TDC
   overlap (accelerates as you climb the flank). From ~8.4 mm you'd need *far* more than 15° of
   advance to threaten contact in normal operation.
3. **The real exposure the S2 introduces is at FULL lift, not overlap.** Its 10.20 mm peak lift
   exceeds the ~9.7 mm TDC budget by ~0.5 mm. During normal valve motion this never matters (peak
   lift occurs ~110° ATDC, piston ~30 mm down). But it **removes the free-running safety net**: a
   floated valve (over-rev) or belt break with a valve held open in a ~±8° window around TDC can
   now kiss the piston. A constant-10.2 mm "floated" clearance curve dips to ~−0.7 mm at TDC.
4. Maintaining *stock* clearance while running the cam is impossible without retarding ~10–20° (which
   defeats the cam). The point of the cam is to spend some of that 9.5 mm; you just verify what's left
   stays above the floor.

## Method to redo for another cam/engine

Plug new r, L (kinematics), Lmax/dur/CL (lift), and the engine's measured K. Clearance = K + drop −
lift; min over θ near TDC is running clearance; constant-Lmax curve is the float/belt-break exposure.
Always clay-confirm K and the worst-case (most-advanced VVT) position before trusting numbers.
