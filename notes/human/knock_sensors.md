# Knock sensors — EMU page

> Digest of [knock_sensors.md](../knock_sensors.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** setting up knock detection and retard in EMU, and how to read the knock channel as a combustion-quality signal instead of just counting spikes.

**The rules:**

- Set the frequency band from the bore: `F = 900/(π·R)` — R is cylinder radius in mm, F in kHz. Window it to the combustion event and confirm it reads combustion, not mechanical noise, before trusting it.
- Knock detection only works in boost. At idle the ring-down energy is buried in injector/valvetrain noise — use RPM CoV for idle stability instead.
- Retard needs enough authority to protect, restored gently so the re-advance doesn't stack a torque step. Back the timing table off wherever one cylinder keeps pulling retard.
- Knock-voltage scatter on no-knock cycles proxies combustion CoV — a way to rank fuel/ignition maps without a pressure transducer. But it only works if you detrend within fine RPM/MAP cells AND restrict to rising-RPM/MAP transients; otherwise the operating-point trend swamps everything.
- No-knock cycles only (`Knocking cylinders == 0` and per-cylinder retard zero), expressed as CoV, not raw std. It ranks; it doesn't calibrate.
- Watch baseline *variance*, not just spikes: a walking floor means lean/hot cylinders. Flat and smooth at max power means every cylinder is doing the same thing every cycle.
- Ethanol barely knocks — on E-heavy fuel the limit is torque/EGT. Enrichment's knock benefit saturates around λ 0.76–0.78; richer buys EGT margin only.

**Key numbers:** detrend cells ~250 rpm × 10 kPa. Walk boost timing in 1° steps on per-cylinder retard + EGT.

**When to care:** wiring or configuring knock inputs, judging whether a knock reading is trustworthy at a given load, and ranking two maps for combustion smoothness.
