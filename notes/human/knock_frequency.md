# Knock frequency — bore sets the band

> Digest of [knock_frequency.md](../knock_frequency.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** where to put the knock filter band, what ECUMaster's `900` constant actually encodes, and why nothing but bore meaningfully moves the frequency.

**The rules:**

- Knock is the burned *gas* ringing in the bore, not the metal. The medium is hot combustion products (c ≈ 978 m/s) — that sound speed and the first Bessel root are what the `900` bakes in.
- `F = 900/(π·R)` takes the cylinder RADIUS in mm, not the bore diameter. Don't feed it bore.
- Higher modes are Bessel roots, not harmonics: multiply the fundamental by 1.66 (2nd mode) or 2.08 (3rd). Doubling lands in a dead zone between them — you'd detect nothing.
- Bore dominates by ~50×. CR, humidity, ethanol, water injection, and richness each shift the band ≤~4% — all inside a normal filter skirt.
- Set the band once from bore and leave it. A flex-fuel car needs no fuel- or condition-dependent knock frequency.
- Running rich at full tilt drops the band ~2% via flame temperature — center on the dry-stoich value and it still captures the hot-rich case.
- Going λ0.75 for margin sheds ~25% of the injected fuel energy unburned (CO/H₂) — cooling insurance, not power. Deliberate is fine; know the cost.

**Key numbers:** `F₁ = 572.96 / bore(mm)`. 86 mm (2JZ/1JZ/RB/K20/SR20) → 6.66 kHz fundamental, 11.05 kHz 2nd mode. 1FZ-FE (100 mm) → 5.73 kHz. EMU quotes block vibration 3–20 kHz.

**When to care:** configuring knock frequency on any engine, and whenever you're tempted to move the band for a fuel, CR, or water-injection change — don't.
