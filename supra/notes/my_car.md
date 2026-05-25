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
- EMU Black
- ECUMaster CAN Switchboard for sensors
- GS430 throttle body
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