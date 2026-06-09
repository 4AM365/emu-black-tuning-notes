---
name: emu-black-temp-sensor-recal
description: >-
  Re-calibrates an EMU Black custom temperature sensor by copying a known-good
  sensor's voltage→temperature curve onto it, and writes the corrected cal as an
  importable .emubt. Use whenever a temp input reads systematically wrong and the
  user says "my Pre-IC/charge/oil/custom temp sensor reads too cold/hot", "wrong
  temp curve", "fix my custom temp calibration", "copy the IAT curve onto custom temp
  1", "recalibrate the sensor", or has a custom-temp input running the wrong curve
  while an identical sensor is already calibrated correctly in the tune. Resamples
  the correct curve onto the custom sensor's N cal nodes (zero error at the nodes),
  can also report the correction for values already logged on the wrong curve, and
  emits the .emubt. Not vehicle-specific — pass the reference curve as input. Pairs
  with emu-black-tune (read the correct curve out of the tune) and
  emu-black-emubt-export.
---

# EMU Black custom temp-sensor re-cal

If a custom-temperature input (Pre-IC, secondary IAT, oil, etc.) is running the
**wrong** voltage→temperature curve, it reads systematically off (e.g. ~30 °C too
cold). When that sensor is the **same physical type** as one already calibrated
correctly in the tune (typically the **IAT** sensor), the fix is to **resample the
correct curve onto the custom sensor's cal nodes**.

## Method

1. Read the **correct** curve out of the tune (e.g. `iatTbl` over `voltage5VIATBin`)
   with `emu-black-tune`; save it as a CSV of `voltage_raw,temp_C`.
2. Resample it onto the custom sensor's **N** cal nodes (default 10), keeping the
   nodes that cover the operating band → zero error at the nodes, tiny error between.
3. Emit the `.emubt` for the custom cal symbols (sign-magnitude hex, handles negative
   temps).
4. (Optional) For values **already logged** on the wrong curve, invert the wrong
   curve (T→V) then apply the correct one (V→T) to recover true temperature.

## Usage

```bash
python scripts/temp_sensor_recal.py \
    --ref iat_curve.csv \
    --symbol customTemp1Cal --bins-symbol customTemp1CalBins \
    --bins 10 --out "Custom temp cal 1.emubt" \
    [--keep 0,3,4,5,6,7,8,9,12,13] [--wrong wrong_curve.csv]
```

- `--ref` correct curve CSV (`voltage_raw,temp_C`; `voltage_raw` is the ubyte node,
  display V = raw × 5/255).
- `--keep` optionally pins which reference nodes to keep (else auto-spread).
- `--wrong` prints old-vs-new and the implied logged-value correction.
- Standard library only.

## Notes

- The `.emubt` temps are **ubyte sign-magnitude** hex (negatives set the high bit) —
  the same encoding `emu-black-emubt-export` uses; verify a couple of cells in EMU
  after import.
- Always confirm the reference curve against the EMU display before trusting the
  output (read it with `emu-black-tune`).
- Worked Supra example (Pre-IC re-cal from the IAT curve): `notes/hood_removal_charge_temps.md`,
  `supra/notes/`.
