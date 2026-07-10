# Rolling return-to-idle wobble

> Digest of [idle_drive_wobble.md](../idle_drive_wobble.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** why RPM craters (~1800 → 525 at a 1200 target) and limit-cycles when you neutral-coast down to idle, and the three measured faults behind it.

**The rules:**

- **Fault 1 — rich low-RPM VE.** Lambda dove to 0.68 vs the 0.93 target as RPM cratered into MAP 60+ kPa. The 500-rpm VE row is the live lever; idle airflow rows below the 1200 target floor are never read.
- The −17–19% rich figure came from pre-correction E25 logs. After the −18% pump / +10% ethanol correction, the residual depends on fuel: still ~−18% at E60, only ~−9% at E25. **Re-measure lambda at the fuel you actually run before leaning the 500/842 rows** — a lean sized from the E25 log over-leans at E25.
- Short-term trim is clamped ±2–3% and slow: it can't correct a fast dip and won't show true VE. Set VE from measured lambda error, apply ~80%, lean both VE tables by the same ratio.
- **Fault 2 — fan correction drops out at speed.** The +13% `idleCoolantFanCorr` is VSS-gated off above ~56 km/h, so high-speed returns land on bare ~26.5% airflow with the PID clamped at +12. Fix with more PID authority and a faster update interval (200 → ~50 ms); leave the fan +13% alone.
- **Fault 3 — idle locked out by the MAP gate.** `idleMinMapToActivate` at 25 kPa doesn't let idle grab until ~582 rpm on a hot coast-down — too late. Recommended **18 kPa** (valid window 17–32): idle catches at ~1060 rpm, inside the ~160 ms DBW lag. Re-verify coast-downs after the change.
- Feed-forward was oversized: PID sat saturated at −9.75%. Halving the corrections restored authority both directions.

**Key numbers:** idle MAP floor 32 kPa; worst engine-braking MAP 17 kPa; gate 25 → 18 kPa; PID update 200 → ~50 ms.

**When to care:** hot return-to-idle stalls or bogs, coast-down RPM dips, or before touching the low-RPM VE rows or the idle activation gate.
