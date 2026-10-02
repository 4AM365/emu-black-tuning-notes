# Cranking VE basis error + fuel rebuild (2026-08-06)

> Digest of [cranking_ve_basis.md](../cranking_ve_basis.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** why "0 % cranking enrichment" kept fouling plugs, and the two tables built to replace it.

**The rules:**

- v3 doses cranking through the main VE table, and the lookup clamps to the lowest-RPM row — a corner no wideband can ever autotune. If real trapped VE is below what that row claims, every cranking cell is silently enriched by the ratio. **A 0 % cell is not neutral.**
- Measure the ratio (B = VE_true / VE_table) instead of assuming it. Re-check it whenever the low-RPM VE row moves.
- Use the **`Injectors cal. time`** log channel for deadtime — it's the ECU's own value from battery voltage and fuel pressure. Don't back-solve it.
- Flat RPM and no fire across dozens of sparks with a full rail = quenched spark (wet/fouled plugs), not a mixture problem. Fuel-table work through fouled plugs is untestable.
- `u12` storage accepts negative cells. Keep the basis correction in the table, not in `crankingLambdaTarget`.
- EMU interpolates rows **linearly**. Enter all five rev rows — interpolating between rev 1 and rev 20 leaves the cold mid-rev cells ~5–6 points rich, which is exactly where a long cold crank lives.

**Key numbers (2026-08-06 log, re-verify — these drift with the tune):**

- Effective PW at hot crank ≈ 1.43 ms (2.84 total − 1.41 deadtime), ECU basis VE ≈ 63, real ≈ 50 → **B ≈ 0.79**, i.e. 0 % delivered λ ≈ 0.79.
- Seven crank attempts, zero fires, ≈3.4 g of liquid fuel into the ports.
- Rebuild: `corr = B(CLT) × [1 + E₁(CLT)·e^−(rev−1)/N(CLT)] − 1`, with N temperature-scheduled (16→4 revs cold→hot).

**When to care:** any cranking-fuel change, any edit to the low-RPM VE row, or a return of the flood/foul pattern.
