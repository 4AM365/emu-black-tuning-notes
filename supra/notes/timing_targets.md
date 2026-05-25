# Timing Targets — Supra build-specific (10:1 CR, BorgWarner 61.44mm, 264° cams)

Specific calibration targets derived for this build. Generic timing principles live in `notes/timing.md`.

## E60 Timing Targets (10:1 CR, WOT)

Walk up in 1° steps while monitoring per-cylinder knock channels. E60 has headroom but knock onset is still possible, especially if ethanol content is lower than expected.

| Boost (psi) | E60 Target (°BTDC) | vs. 93 octane |
|---|---|---|
| 0 (VE cells) | 32–38° | +4–6° |
| 10 | 20–24° | +4–5° |
| 14 | 19–23° | +4–5° |
| 18 | 17–21° | +4–5° |
| 22 | 14–17° | +3–4° |

## Safe Boost Ceiling

- 93 octane, 10:1 CR, good intercooling: 14–15 psi conservative; 16–18 psi with active knock monitoring.
- E60, 10:1 CR: aggressive ceiling 22–24 psi.
- Target for 500 ft-lb flat curve: ~19–22 psi / 17–21° timing at peak boost on E60.
- 10° below MBT at 10 psi on pump gas ≈ 290–300 ft-lb (MBT at that point ≈ 360 ft-lb).

## Notes

- Idle base ignition (E25 cells, warm idle): 16.5° BTDC. Within the "ethanol / cammed" guidance range of 16–19° in `notes/timing.md`.
- Idle ignition target (the angle the idle controller drives toward): 18.0° at warm CLT.
