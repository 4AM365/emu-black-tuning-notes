# Denso / Toyota coil reference

> Digest of [denso-coils.md](../denso-coils.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** reusable coil part numbers, dwell behavior, and connector numbers for Toyota-engine standalone builds. Which coil a specific car runs lives in that build's working doc, not here.

**The rules:**

- Denso 90919-A2004 (2GR/2AR family): 3 ms dwell is max energy; 5 ms loses some. Takes up to 26 V — same energy, faster charge.
- Dwell scales down with voltage and load: ~2.8 ms across the board at 6 V, tapering to 1.0–2.0 ms at 16 V (Frankenstein Motorworks 2GR table in the canonical note).
- GM D585 is the common aftermarket benchmark coil — reliable and available, but not a Toyota plug-in.
- Part-number map: 90919-A2004 (mid-era 2GR/2AR/1AR), 90919-A2005 (2AR and others, cross-refs Denso 673-1309), 90919-02260 (late broad fitment), 90919-A2013 (dealer consolidation of early 2GR coils).
- Connectors: Yazaki 90980-11885, Sumitomo 90980-12176.

**Key numbers:** 3 ms max-energy dwell; 26 V ceiling.

**When to care:** picking coils for a swap, filling in `dwellTime`, or ordering connectors and replacements.
