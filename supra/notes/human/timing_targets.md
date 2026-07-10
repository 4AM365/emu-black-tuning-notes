# Timing targets (10:1 CR, E60)

> Digest of [timing_targets.md](../timing_targets.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** WOT timing targets and boost ceilings for this build (10:1 CR, BorgWarner 61.44 mm, 264° cams).

**The rules:**

- Walk timing up in 1° steps watching per-cylinder knock channels. E60 has headroom but knock is still possible — especially if ethanol content is lower than you think.
- E60 WOT targets: 32–38° in the NA cells; 20–24° at 10 psi; 19–23° at 14; 17–21° at 18; 14–17° at 22. That's +3–6° over 93 octane at each point.
- Boost ceilings: 93 octane 14–15 psi conservative, 16–18 with active knock monitoring; E60 aggressive ceiling 22–24 psi.
- The 500 ft-lb flat-curve target is ~19–22 psi at 17–21° peak-boost timing on E60.
- Running 10° below MBT at 10 psi on pump gas costs ~60–70 ft-lb (≈290–300 vs ~360 at MBT) — retard is expensive.
- Idle: base ignition 16.5° (E25 cells, warm), idle-controller target 18.0° at warm CLT.

**When to care:** before adding timing or boost anywhere — especially near or above 14 psi, or whenever the ethanol blend is uncertain.
