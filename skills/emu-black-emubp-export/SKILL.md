---
name: emu-black-emubp-export
description: >-
  Pulls scalar PARAMETERS from an EMU Black XML tune into an importable .emubp
  parameters file (a <variables> block of scalar symbols). Use whenever the
  deliverable is a group of settings/scalars rather than a single table — cam
  (VVT) setup, cam PID gains, overrun/decel-cut parameters, idle PID, boost
  control scalars, trigger/sensor config. Trigger on phrases like "pull the cam
  settings from <vehicle> to emubp", "export the overrun parameters", "make an
  emubp of the VVT PID", "compare <vehicle>'s cam params to the example",
  "transfer these settings to <vehicle>'s folder". Resolves a vehicle NAME
  (supra, bradley, land cruiser, ...) to its XML tune via EMU_SOURCE_INDEX.md.
  Distinct from emu-black-emubt-export, which writes TABLES (.emubt); this skill
  writes SCALARS (.emubp). Pairs with emu-black-tune (decode/scaling).
---

# EMU Black .emubp Parameter Exporter

`.emubp` is EMU Black's **parameter** export: a minimal XML project whose
`<variables>` block holds one or more **scalar** `<symbol>` elements (each with a
`value`, `storage`, and `type`). It is the scalar sibling of `.emubt` (which holds
`<tables>`). EMU imports an `.emubp` by symbol name, setting just those scalars.

Use this skill to pull a *group of settings* out of any vehicle's XML tune and
write it as an `.emubp` — e.g. "pull the cam settings from land cruiser to emubp".

> Scalars only. A symbol carrying `data=`/`width=` is a **table** and belongs in a
> `.emubt` (use **emu-black-emubt-export**). The script skips tables with a warning.

## File shape

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="1.0">
  <variables>
    <symbol name="vvtCam1KP" value="1434" storage="word" type="value"/>
    <symbol name="vvtCam1Deadband" value="1" storage="ubyte" type="value"/>
  </variables>
</project>
```

- `version="1.0"` (same as a single-table `.emubt`).
- Each scalar keeps its `storage` (`ubyte`/`sbyte`/`word`/`sword`/…) and `type`
  (`value`/`bool`/`paramList`) **from the source tune** — these are firmware-stable
  and authoritative for that vehicle.
- **Filename = EMU's exact group title.** EMU's own group exports are named like
  `CAM 1 - CAM 1 PID.emubp`, `CAM 1 - CAM 1 parameters.emubp`,
  `overrun parameters.emubp`. Match that so the user knows which dialog it re-imports.

## Primary path: `scripts/pull_emubp.py`

Stdlib-only. Three ways to choose the symbols:

**1. Template mode (PREFERRED).** Point at an `example … .emubp` (EMU's own group
export) — it fixes the symbol **list and order**; the script pulls each symbol's
*current* value from `--source` and prints a template-vs-pulled comparison.

```bash
python scripts/pull_emubp.py --source bradley \
  --template ".../bradley/example CAM 1 - CAM 1 PID.emubp" \
  --out ".../bradley/bradley CAM 1 - CAM 1 PID.emubp"
```

**2. Prefix mode.** Every scalar whose name starts with the prefix, in file order.

```bash
python scripts/pull_emubp.py --source "land cruiser" --prefix vvtCam1 \
  --out "land cruiser CAM 1 settings.emubp"
```

**3. Explicit symbols.**

```bash
python scripts/pull_emubp.py --source supra \
  --symbols "boostTargetMin boostTargetMax wgFreq" --out "supra boost scalars.emubp"
```

### `--source` resolution

A **vehicle name** (resolved via the index below), a **folder** (newest
`*.xml.emub3` is used), or a **direct `.xml.emub3` file**. Known vehicle names win
over a same-named local directory (the repo has its own `supra/` folder), so
`--source supra` always means the OneDrive tune, not the repo subdir. The chosen
tune path is printed every run — confirm it's the file you meant. Only XML exports
are readable; a binary `.emub3` (starts with `PK`) is skipped.

Vehicle map mirrors [`EMU_SOURCE_INDEX.md`](../../EMU_SOURCE_INDEX.md):
`supra`, `bradley`, `land cruiser`/`fj80`, `napier`/`gs300` (V1), `base maps`,
`default`. Update both if a vehicle is added.

## Gotchas

- **Casing in prefix mode is exact.** EMU mixes case within a group — e.g. cam-1 is
  mostly `vvtCam1*` but `vvtCAM1CtrlDelay` has a capital `CAM`. `--prefix vvtCam1`
  silently misses it. For a complete, correctly-ordered group, prefer **template
  mode** (explicit names) or pass both prefixes / use `--symbols`.
- **Template defines membership, source defines values.** If a template symbol is
  absent from the source tune it's reported under `MISSING` and omitted — a real
  signal that the two firmwares/feature-sets differ, not a silent drop.
- **`storage`/`type` come from the source**, not the template, so an export is
  always self-consistent with the vehicle it was pulled from.

## Cross-vehicle transfer caveats (engine-specific scalars)

Copying a group between vehicles is legitimate for setup defaults, but some scalars
are physically tied to one car and must **not** be run as-is on another:

- **Trigger/phase offsets** — `vvtCam1TriggerOffset` zeroes the cam sensor against
  that engine's trigger; meaningless elsewhere, find empirically.
- **PID gains** — matched to a phaser/solenoid/oil response; a starting point only.
- **Enable gates** (`*MinRPM`, `*MinCoolantTemp`, `*MinOilTemp`) — reflect that
  engine's warm-up and idle, re-check per vehicle.

Always print the comparison and call out which transferred scalars are
engine-specific before the user imports.

## Workflow

1. Identify the group and find EMU's `example … .emubp` for it (or list symbols).
2. Run `pull_emubp.py` with `--source <vehicle>` and `--template`/`--prefix`.
3. Read the printed source-tune path and the comparison table; flag engine-specific
   scalars and any `MISSING`/`SKIPPED` symbols.
4. Verify against a hand-pull of one symbol the first time on a new group, then have
   the user import and spot-check in EMU before running the engine.

## Relationship to other skills

- **emu-black-tune** — decoding/scaling of the source XML (read-side).
- **emu-black-emubt-export** — the TABLE (`.emubt`) sibling of this skill.
- Verified on this repo: template mode reproduces the hand-built
  `supra CAM 1 - CAM 1 PID.emubp` and `supra overrun parameters.emubp`
  byte-for-byte.
