# Boost — EMU Black settings and the principles behind them

> **Software page:** *Boost*. Full symbol catalog: [tune_feature_tree.md → Boost](tune_feature_tree.md). Pedal-referenced throttle/WGDC mapping is on [dbw.md](dbw.md).

The dedicated boost-control document, organized like [idle.md](idle.md):

- **Part 1 — Settings**: one block per EMU Black boost table — what it is, how to set it, how it
  fails, where the live values live.
- **Part 2 — Principles**: how the feed-forward boost model works, the torque-shaping philosophy,
  and the exhaust-reservoir physics behind spool retention.

> **Car-specific values live in the build working docs**, not here. For the reference build see
> [`supra/notes/`](../supra/notes/) — esp. [`my_car.md`](../supra/notes/my_car.md) and
> [`timing_targets.md`](../supra/notes/timing_targets.md) (boost/lambda targets). Numbers below are
> illustrative examples, not this build's calibration.

---

# Part 1 — Settings (one block per EMU Black boost table)

### Base WGDC table (feed-forward)

- **What it is.** Open-loop wastegate duty vs MAP/RPM (the feed-forward core, B1).
- **How to set it.** Build it **from logged ramp runs before activating PID**: override WGDC, pull,
  and write the WGDC that produced each observed boost into the matching cell. Use ~100% in the
  unspooled region to prioritize spool, reduce WGDC up the RPM axis to cancel creep, shape the
  midrange/top per the torque philosophy (B2).
- **Failure mode.** Enabling PID on top of an unmapped base table → the loop fights a bad
  feed-forward.
- **Live values:** build doc.

### Boost target table (PPS-referenced)

- **What it is.** The target boost vs **pedal** and RPM — what the closed loop and margin
  protection chase.
- **How to set it.** Reference on **`ppsBoostBins`** (pedal), closed-throttle column at zero boost,
  rising monotonically to a top-right peak (B2; cross-check [dbw.md → Boost-vs-PPS](dbw.md)
  and [ve_vs_map_at_constant_rpm.md](ve_vs_map_at_constant_rpm.md)). For **spool retention**, set
  the **0% PPS / high RPM** cells **non-zero** (~60–80 kPa) so WGDC stays up and the gate stays
  closed through a shift (B3) — gate the aggressive version behind VSS.
- **Failure mode.** Zero target at 0% PPS / high RPM → gate opens during the shift, boost falls
  out; no VSS gate → boost spike on low-speed re-engagement.
- **Live values:** build doc.

### Boost PID

- **What it is.** Closed-loop correction layered on the feed-forward base.
- **How to set it.** Only after the base table is mapped (B1). Distinguish **PID hunting** (large
  oscillating `Boost PID correction` → gains too aggressive) from **margin triggering**
  (`Boost out of margin = 1` → thresholds too tight) — different fixes. For a street tune with
  limited on-boost time, lean on a good feed-forward base and modest PID.
- **Failure mode.** Conflating margin-protection triggers with PID oscillation.
- **Live values:** build doc.

### Margin protection

- **What it is.** A **safety limiter**, not closed-loop control — traditional PID tuning logic does
  not apply.
- **How to set it.** For a street tune, **widen thresholds (±8–10 kPa)** to reduce false triggers;
  it can also serve the B2 role of capping midrange boost if used carefully. Read
  `Boost out of margin` to confirm whether it (vs PID) is acting.
- **Live values:** build doc.

### Timing-based anti-lag (shift strategy)

- **What it is.** Aggressive ignition retard on the shift event to dump heat into the exhaust and
  keep the turbine spinning.
- **How to set it.** ~15–25° retard on **clutch activation + RPM/speed gate** (RPM > 3000–4000,
  VSS > 20–30 mph, TPS recently high >60% in last 500 ms, clutch switch active); duration
  500–1000 ms max with a ~200 ms taper. **Monitor EGTs** — this raises exhaust temps significantly.
  Cross-link: decel/overrun ignition handling in [ignition.md](ignition.md).
- **Failure mode.** Ungated or too-long activation → EGT runaway.
- **Live values:** build doc.

---

# Part 2 — Principles

## B1. Feed-forward first, PID on top

EMU Black v3 boost control is **feed-forward**: a known WGDC is fed in, boost is measured, and a
correction (PID, fixed value, or table) is layered on. So the **base WGDC table is built
experimentally before PID is enabled** — override WGDC, do a pull, log it, and write the WGDC that
produced the observed boost into that MAP/RPM cell (e.g. 120 kPa at 45% WGDC → put 45 in the 120
column for that RPM). Climbing RPM lets you **reduce WGDC to cancel boost creep**. Establish the
open-loop relationship first, then layer PID — and keep **margin protection** (a safety limiter)
distinct from **PID** (closed-loop control): traditional PID logic does not apply to margin
protection.

## B2. Shape boost as a torque curve, referenced to the pedal

Boost is a torque lever, so shape it deliberately: **prioritize spool** by commanding a high WGDC
(~100%) where the turbo isn't lit, **pull boost back in the midrange** to manage torque (keeping
timing near MBT but boost efficient for a flat curve), then **build boost again above peak-torque
RPM** out to redline — mechanical advantage improves up top, so there's little downside to more
boost there. **Match boost to pedal position** so power is asked-for, not a hammer that lands
whenever you breathe on the throttle (the map peaks top-right, high PPS / high RPM). Know where
your **cams peak** (dyno of this engine at fixed boost, or the N/A version) — that's the region to
keep timing near MBT and trim boost for efficiency. Not every engine needs midrange torque
limiting; most respond well to added boost above peak torque.

## B3. The exhaust manifold is a pressure reservoir (spool retention)

Between shifts the manifold holds pressure that bleeds via turbine flow (productive) and via leaks
+ heat loss (not). You can **keep the wastegate shut through the shift window** by commanding a
high boost target at 0% PPS / high RPM — the ECU chases the (unmet) target, so WGDC stays high and
the gate stays closed. Pairing **overrun fuel cut with the DBW held open (~10–15% TPS)** turns the
engine into an air pump: no combustion, but airflow keeps the turbine spinning (RPM still falls
from drag/pumping, just not catastrophically). Guard the **boost spike on re-engagement** with a
VSS threshold (~50–60 mph) so it captures shifts but not low-speed coasting.

---

## Related documents

- [dbw.md](dbw.md) — boost-vs-PPS mapping, pre-throttle boost reference, WGDC on pedal
- [ignition.md](ignition.md) — boost timing (less advance per boost increment), anti-lag retard
- [fueling.md](fueling.md) — lambda vs load, full-boost endpoints, protection enrichment
- [vvt.md](vvt.md) — boost scavenging pays only while pre-turbine backpressure < intake pressure
