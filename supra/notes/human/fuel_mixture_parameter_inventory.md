# Fuel-mixture parameter inventory

> Digest of [fuel_mixture_parameter_inventory.md](../fuel_mixture_parameter_inventory.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** every XML symbol that can move the delivered mixture, grouped, plus what changed between the on-target 09-19 export and 09-22.

**The rules:**

- **Six groups:** base dose (VE tables, injector model, per-cylinder trims), fuel type (ethanol scale and blends), temperature/density (`chargeTempTbl`, sensor tables, fuel-temp correction, baro), enrichment (cold and transient), closed loop (STFT), and the WBO conversion tables that decide what λ reads.
- **Nothing fuel-related changed 09-19 → 09-22.** Only `cltSensorCal`, two `idleActiveAirflow` cells and checksums differ. Edits after 09-22 are unreadable (binary only) — ask for a fresh XML before ruling tune edits in or out.
- **STFT's window is a parameter:** `shortTermMinLambda` ÷ 128 ≈ 0.797. Below that the trim is off, so it cannot act on a 0.78 idle. Its integral floor and its low-airflow gain scalers make it slow and short-ranged there too.
- **Baro is fixed** in these logs, so `baroCorrection` is inert; the fuel-temperature correction is ≈ 0 below ~35 °C fuel.
- Values are not copied into the note — read them from the current XML.

**Key numbers:** 1771 symbols; 3 differ 09-19 → 09-22; STFT λ window 0.797–1.203.

**When to care:** before proposing any fuel-mixture change, to check which term actually moves at the cell in question.
