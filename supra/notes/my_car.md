# Car
- 1994 Toyota Supra - JDM, SZ

# Engine
- Stock bottom end
- GE VVT-i Head
- BC0311 264 duration cams
- Shimless buckets, fluidampr

# Fuel
- AEM 50-1200 (x2)
- Custom 8AN feed
- Radium filter, FF bypass, FF sensor, DMR regulator, Radium fuel rail
- ID1050x

# Intake / Exhaust
- SPA exhaust manifold
- Custom 4" exhaust
- Borg S362

# Drivetrain
- R155 w/ DM thrust washer and bearing retainer
- OSG TR2CD clutch
- Driftmotion throwout bearing
- Wilwood m/c, Grannas bracket
- DM AL driveshaft
- GS430 diff
- Sketchy Russian Torsen diff

# Electronics
- EMU Black — **hardware revision F, CPU G** (owner-read from the About window,
  2026-08-28). Pre-"P" hardware: the three built-in switch inputs (black plug
  terminals 10, 23, 36) are **not** independent and accept **sensor ground only**;
  anything else on one of them can corrupt the readings of the others
  (`docs/emu-black-help/Sensorsandinputs.md` :841, :1252). Bears directly on
  `ac_request_input_noise.md` §4c.
- ECUMaster CAN Switchboard for sensors
- Throttle body: Toyota/Denso DBW, **Lexus ES330 part no. 22030-20060** (junkyard unit; corrected from "GS430" by Will 2026-09-19). Plate stamped "H", material **unknown** — not assumed stainless.
- GS430 throttle pedal

# Build Constants

| Parameter | Value |
|---|---|
| TPS calibrated zero | 2.0% TPS = 0% Airflow |
| TPS full scale | 6.4% TPS = 100% Airflow |
| Airflow% formula | `(TPS% − 2.0) / 4.4 × 100` |
| TPS from Airflow% | `TPS% = 2.0 + (Airflow% / 100) × 4.4` |
| E60 stoich AFR | ~11.0:1 |
| WOT lambda target | 0.80 |
| Drivetrain loss | ~15% (through R155) |
| Overrun fuel cut exit | 2050 RPM (current) |
| Rev limit | 7000 RPM |
| Hot idle airflow | ~38% |
| Compressor mass flow @ 5500 RPM / 107 kPa / 95% VE / 31°C CAT | ~293 g/s |
| Compressor PR @ 107 kPa boost | ~2.06 |
| Compressor PR @ 135 kPa boost | ~2.34 |

# Powerband / Resonance Notes

- This Supra shows a resonance-sensitive region around 5500 RPM. Be cautious adding load, ignition advance, or aggressive lambda changes through that area.
- Above the 5500 RPM resonance region, power can generally be added more confidently, assuming logs confirm stable lambda, knock margin, EGT/thermal behavior, and drivetrain response.
