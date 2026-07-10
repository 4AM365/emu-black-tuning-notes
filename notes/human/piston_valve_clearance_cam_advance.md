# Piston-to-valve clearance and cam advance (2JZ-GTE)

> Digest of [piston_valve_clearance_cam_advance.md](../piston_valve_clearance_cam_advance.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** how much intake cam advance you can run before the valve meets the piston, worked for the high-lift GSC S2 on a 2JZ-GTE.

**The rules:**

- The only collision on this head is valve-to-piston, pinching a few degrees after TDC overlap — intake and exhaust valves can't hit each other.
- The stock GTE is non-interference: ~9.5 mm valve-to-piston gap at TDC tolerates ~9.7 mm of lift, and the stock cam only lifts 8.25 mm.
- Running clearance stays large, not marginal: S2 at 0° advance ~8.4 mm, at +15° ~7 mm — all far above the 2.0 mm street floor. An early 3 mm assumption was ~3× too pessimistic.
- You lose ~0.09–0.10 mm of clearance per crank degree of advance near TDC; from 8.4 mm you'd need far more than 15° to threaten contact in normal running.
- The S2's real exposure is peak lift, not overlap: 10.20 mm exceeds the ~9.7 mm TDC budget, so a floated valve (over-rev) or belt break near TDC can now kiss the piston. The free-running safety net is gone.
- Base circle and shims set lash and seating only — they do not move the valve-to-piston numbers.
- The lift model is conservative (predicts contact early); clay-test is the real authority, checked at the most-advanced VVT position.

**Key numbers:** K ≈ 9.5 mm stock closed-valve gap at TDC; 2.0 mm (0.080″) street clearance floor; ~0.1 mm clearance cost per crank degree of advance.

**When to care:** before widening VVT advance limits or installing a high-lift cam, and when judging what an over-rev or belt break would cost.
