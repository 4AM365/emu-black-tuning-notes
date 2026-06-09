# Hood removal vs charge/intake temps (EMU Black)

Method and general findings for quantifying how much an open/removed hood lowers intake charge temperature, using EMU Black temp channels against matched-ambient logs.

> **Car-specific values live in the build working docs**, not here. For the reference build's measured deltas, sensor-cal corrections, and log specifics see [`supra/notes/hood_removal_charge_temps.md`](../supra/notes/hood_removal_charge_temps.md). This note is intentionally car-agnostic.

## Channel-trust cautions (check before believing any temp result)

- **Confirm what each temp channel actually is.** `Charge temp` may be identical to the physical `IAT` sensor row-for-row (i.e. just the manifold/throttle intake-air sensor, not a coolant-blended model). Verify on a full-channel log before treating it as a model vs. a raw sensor.
- **Watch for the wrong calibration curve on a channel.** A temp channel logged with the wrong sensor cal (e.g. a generic "Custom temp cal") can read tens of °C off. To recover a true value: invert the wrong curve (T→V), then apply the correct curve (V→T). The recovery is exact if both curves are known.
- **Unwired temp channels read the EMU open-circuit default (a flat −40 °C).** Don't use them; pull ambient from a weather archive keyed to the log's timestamp/location instead.

## General findings (direction, not magnitudes)

- Removing the hood lowers intake/charge temp by a few °C at **matched ambient**, biggest at **idle / heat-soak** conditions.
- It lowers the *level* of air entering the tract (inlet/pre-IC); the manifold temp tracks down with it.
- It does **not** fix conduction-driven plenum soak from the hot cylinder head — the manifold-vs-pre-IC rise across the plenum is roughly unchanged hood-on vs hood-off.

## Method discipline

- **Compare like-for-like: idle-vs-idle is the control.** Drive composition (moving vs idling/blips) dominates manifold temp via soak time and can swamp the hood effect — a highway log can show *lower* charge temp on a hotter day.
- Match ambient between the logs you compare; derive ambient from the log timestamp + location against an hourly weather archive.
- **Preserve original log timestamps** (re-saving/exporting through cloud sync can reset file CreationTime). Name logs `YYYYMMDD_HHMM` so ambient lookup stays usable.
- Filter sensor dropouts (e.g. occasional reads to 0 °C) before taking medians.
