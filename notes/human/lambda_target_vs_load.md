# Lambda target vs load

> Digest of [lambda_target_vs_load.md](../lambda_target_vs_load.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** why the lambda target's boost rolloff is nearly linear in MAP, where it bends, and how to spend the fixed 8 MAP bins.

**The rules:**

- Two regimes: best-torque mixture (λ ~0.90–0.95) is flat across load; everything richer is protection enrichment for EGT or knock, and that grows ~linearly with MAP. A straight interpolated rolloff across the boost range is physically right — dense bins there are wasted.
- The real kink is the MBT-to-protection knee (~120–160 kPa). Put a bin ON it and bracket both sides — that's why 130 kPa earns its own bin.
- Only ~3 points are needed across the linear rolloff; top bin lands on the veTable MAP boundary. The axis is fixed at 8 columns — there is no 9th slot.
- Charge-cooling and knock-suppression benefits saturate around λ 0.76–0.78. Richer than that only buys EGT margin, at the cost of power, BSFC, and bore-wash/fouling risk if sustained.
- The pump table should sit richer than the ethanol table — pump gas has no evaporative cooling, so it leans on fuel quantity for charge cooling.
- FFIM maldistribution is NOT a reason to over-enrich the global target: with per-cylinder trims running, every cylinder is already corrected, so WOT richness is purely an EGT/safety-margin choice. (Earlier claim to the contrary — corrected.)
- Knock retard and compressor/turbine limits steepen the top of the curve; a well-intercooled, lightly-retarded engine stays linear up top, so keep the upper bins coarse.

**Key numbers:** typical high-boost pump targets λ 0.72–0.80; cooling/knock benefit saturates ~λ 0.76–0.78; knee lives ~120–160 kPa.

**When to care:** rebinning the lambda-target MAP axis, choosing WOT richness, or deciding whether a rich global target is protecting anything the per-cylinder trims don't already handle.
