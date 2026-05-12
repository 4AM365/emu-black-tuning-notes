# General Principles
- The goal of timing is to place the point of greatest charge gas expansion where 50% of fuel is burned (CA50) at a crank angle where the piston and rod have maximum mechanical advantage over the crankshaft. This is MBT (Maximum Brake Torque).

- Knock is a measurement of sudden fuel burn in the engine which results in slapping pistons against a cylinder wall, rods against a main bearing, and so on. You're hearing metal knock against metal.

- Preignition is a condition where a hot combustion chamber will ignite a mixture on its own, artificially advancing your timing. Low-speed preignition is a favorite in the Mazda and Ecoboost world where small turbos cause extreme cylinder conditions at low RPM during normal cruising.

- Detonation is a condition where the end-gases of a mixture ignite from multiple points after ignition has occurred.

- Going too early/negative in timing means your pressure peak (peak BMEP) will occur so early that the piston fights the engine and tries to slow it down. Torque will decrease and EGT will increase.

- Your octane choice controls resistance to detonation (the charge end-gas igniting itself after ignition has occurred). 

- Your fuel choice controls rate of burn. Ethanol generally needs another 3-8 degrees of timing to reach MBT.

- Generally, our goal is to achieve MBT everywhere. On less stable fuels, a mixture will transition to detonation much earlier, so we have to pull out timing to manage it. This is called a knock limited engine. 

- On ethanol, our issue is choosing how much timing we want so we don't physically break the engine with excessive torque, because it's extremely hard to make it knock. Peak anti-knock effects are achieved around 60% ethanol by mixture (E60). 

- MBT timing follows a U-shape for a given MAP across the rev range. (1)

# Cams, ethanol

- Cams that are longer in duration, even if they share a lobe separation angle with stock cams, have more overlap
- The effect of a higher overlap cam on a turbo car is that there is always more pressure in the exhaust than the intake because of the restriction of the turbine, so exhaust gas will blow back into the intake. The RPM you idle at determines how much the intake inertia fights the exhaust pressure.

- You will need more timing at idle when you have more overlap, because exhaust gas causes charge dilution, and flame front velocity (remember CA50%?) is slower through a polluted charge.

| Fuel | Cams | Timing |
| --- | --- | --- |
| Pump gas | Stock | 10-12 |
| Pump gas | Cammed | 13-16 |
| Ethanol | Stock | 13-16 |
| Ethanol | Cammed | 16-19 |
| Ethanol | Big cams | 19-22 |

# Cruise ignition timing

- The same principles for idle timing apply for cruise. You may find that a stock cam pump gas car needs a maximum of 35 degrees timing at cruise, while a cammed ethanol car can reach 42 degrees of timing at cruise. 

- Your cruise timing should be determined experimentally with the use of an EGT sensor. Lower EGT means closer to MBT.

- If you don't have an EGT sensor, put one in. The EMU supports it natively and you can get them for $20. You're looking for a k-type thermocouple. Put it one inch from the head in your exhaust header. When you drill the header (don't be afraid), put a magnet on it to catch the shavings. You don't even need to unbolt the thing. Use some nickle antiseize when you thread the thermocouple in, and go about 1 turn past finger tight. The hotter the exhaust gets, the tighter it will get.

- Don't be afraid of timing in low-load regions. Remember that not only does exhaust reversion slow down flame front - lower cylinder pressures (manifold vacuum) slow it down too. Your tiny flame kernel will travel a long way to get anywhere.

- Timing is a magical thing that makes your car quiet, peaceful, spool quickly, and efficient. You will lose some of the hot rod character and make up for it with real performance. The difference between exciting boost and normal cruise will be enhanced.

- Across the MAP range, you will lose roughly 2 degrees per 30 kPa. Your timing will peak at 20kPa and go down from there.

- Across the RPM range you will add timing, because the piston face is trying to outrun the flame front and doing a better job of it.

# Boost ignition timing

- By now, you get the idea. Bigger cams, lower pressure, and cooler fuels mean more timing.

- MBT for a 2jz in boost will be generally in the low 20s. Again, 5 degree spread for ethanol vs pump gas.

- A good indicator of MBT is CA50% at 8 degrees ATDC. 

# Charge burn (CA100) duration

- Modeled with the Wiebe function

- Knock occurs in last 10% of burn, observing knock can help you estimate duration of combustion so you can work backward to find CA50 and thus MBT

# CA100 Burn Duration Tables (° crank angle)

All values are estimated total 0–100% mass fraction burned duration in crank degrees.  
Basis: Wiebe function parameterization, Heywood (1988) Ch. 9; Tabaczynski et al. SAE 760760; laminar flame speed ethanol corrections after Gülder (1984) SAE 841000.

**Cam definitions (intake duration @ 0.050" lift):**
- Low overlap: ~220–230°, stock-style, high residual fraction at light load
- Medium overlap: ~248–258°, mild performance, moderate residual scavenging
- Large overlap: ~268–278°, aggressive, low residuals, high turbulence intensity

**Ethanol corrections applied as uniform offsets to laminar flame speed effect:**
- E0 (93 pump): baseline
- E30: −4° uniform
- E60: −7° uniform
- E85: −11° uniform

**Cam overlap corrections applied as MAP-dependent offsets (residual dilution reduction):**
- Medium vs. Low: −8° @ 30 kPa, tapering to −2° @ 100 kPa
- Large vs. Low: −14° @ 30 kPa, tapering to −3° @ 100 kPa

---

## Low Overlap Cams (~220–230° dur.)

### E0 — 93 Pump Gas

| MAP (kPa) | 2000 RPM | 3000 RPM | 4000 RPM | 5000 RPM | 6000 RPM |
|-----------|----------|----------|----------|----------|----------|
| 30        | 78       | 80       | 82       | 84       | 86       |
| 40        | 70       | 71       | 72       | 73       | 74       |
| 50        | 62       | 63       | 64       | 65       | 66       |
| 60        | 55       | 56       | 57       | 58       | 59       |
| 70        | 49       | 50       | 51       | 52       | 53       |
| 80        | 44       | 45       | 46       | 47       | 48       |
| 90        | 40       | 41       | 42       | 43       | 44       |
| 100       | 37       | 38       | 39       | 40       | 41       |

### E30

| MAP (kPa) | 2000 RPM | 3000 RPM | 4000 RPM | 5000 RPM | 6000 RPM |
|-----------|----------|----------|----------|----------|----------|
| 30        | 74       | 76       | 78       | 80       | 82       |
| 40        | 66       | 67       | 68       | 69       | 70       |
| 50        | 58       | 59       | 60       | 61       | 62       |
| 60        | 51       | 52       | 53       | 54       | 55       |
| 70        | 45       | 46       | 47       | 48       | 49       |
| 80        | 40       | 41       | 42       | 43       | 44       |
| 90        | 36       | 37       | 38       | 39       | 40       |
| 100       | 33       | 34       | 35       | 36       | 37       |

### E60

| MAP (kPa) | 2000 RPM | 3000 RPM | 4000 RPM | 5000 RPM | 6000 RPM |
|-----------|----------|----------|----------|----------|----------|
| 30        | 71       | 73       | 75       | 77       | 79       |
| 40        | 63       | 64       | 65       | 66       | 67       |
| 50        | 55       | 56       | 57       | 58       | 59       |
| 60        | 48       | 49       | 50       | 51       | 52       |
| 70        | 42       | 43       | 44       | 45       | 46       |
| 80        | 37       | 38       | 39       | 40       | 41       |
| 90        | 33       | 34       | 35       | 36       | 37       |
| 100       | 30       | 31       | 32       | 33       | 34       |

### E85

| MAP (kPa) | 2000 RPM | 3000 RPM | 4000 RPM | 5000 RPM | 6000 RPM |
|-----------|----------|----------|----------|----------|----------|
| 30        | 67       | 69       | 71       | 73       | 75       |
| 40        | 59       | 60       | 61       | 62       | 63       |
| 50        | 51       | 52       | 53       | 54       | 55       |
| 60        | 44       | 45       | 46       | 47       | 48       |
| 70        | 38       | 39       | 40       | 41       | 42       |
| 80        | 33       | 34       | 35       | 36       | 37       |
| 90        | 29       | 30       | 31       | 32       | 33       |
| 100       | 26       | 27       | 28       | 29       | 30       |

---

## Medium Overlap Cams (~248–258° dur.)

### E0 — 93 Pump Gas

| MAP (kPa) | 2000 RPM | 3000 RPM | 4000 RPM | 5000 RPM | 6000 RPM |
|-----------|----------|----------|----------|----------|----------|
| 30        | 70       | 72       | 74       | 76       | 78       |
| 40        | 64       | 65       | 66       | 67       | 68       |
| 50        | 57       | 58       | 59       | 60       | 61       |
| 60        | 51       | 52       | 53       | 54       | 55       |
| 70        | 46       | 47       | 48       | 49       | 50       |
| 80        | 42       | 43       | 44       | 45       | 46       |
| 90        | 38       | 39       | 40       | 41       | 42       |
| 100       | 35       | 36       | 37       | 38       | 39       |

### E30

| MAP (kPa) | 2000 RPM | 3000 RPM | 4000 RPM | 5000 RPM | 6000 RPM |
|-----------|----------|----------|----------|----------|----------|
| 30        | 66       | 68       | 70       | 72       | 74       |
| 40        | 60       | 61       | 62       | 63       | 64       |
| 50        | 53       | 54       | 55       | 56       | 57       |
| 60        | 47       | 48       | 49       | 50       | 51       |
| 70        | 42       | 43       | 44       | 45       | 46       |
| 80        | 38       | 39       | 40       | 41       | 42       |
| 90        | 34       | 35       | 36       | 37       | 38       |
| 100       | 31       | 32       | 33       | 34       | 35       |

### E60

| MAP (kPa) | 2000 RPM | 3000 RPM | 4000 RPM | 5000 RPM | 6000 RPM |
|-----------|----------|----------|----------|----------|----------|
| 30        | 63       | 65       | 67       | 69       | 71       |
| 40        | 57       | 58       | 59       | 60       | 61       |
| 50        | 50       | 51       | 52       | 53       | 54       |
| 60        | 44       | 45       | 46       | 47       | 48       |
| 70        | 39       | 40       | 41       | 42       | 43       |
| 80        | 35       | 36       | 37       | 38       | 39       |
| 90        | 31       | 32       | 33       | 34       | 35       |
| 100       | 28       | 29       | 30       | 31       | 32       |

### E85

| MAP (kPa) | 2000 RPM | 3000 RPM | 4000 RPM | 5000 RPM | 6000 RPM |
|-----------|----------|----------|----------|----------|----------|
| 30        | 59       | 61       | 63       | 65       | 67       |
| 40        | 53       | 54       | 55       | 56       | 57       |
| 50        | 46       | 47       | 48       | 49       | 50       |
| 60        | 40       | 41       | 42       | 43       | 44       |
| 70        | 35       | 36       | 37       | 38       | 39       |
| 80        | 31       | 32       | 33       | 34       | 35       |
| 90        | 27       | 28       | 29       | 30       | 31       |
| 100       | 24       | 25       | 26       | 27       | 28       |

---

## Large Overlap Cams (~268–278° dur.)

### E0 — 93 Pump Gas

| MAP (kPa) | 2000 RPM | 3000 RPM | 4000 RPM | 5000 RPM | 6000 RPM |
|-----------|----------|----------|----------|----------|----------|
| 30        | 64       | 66       | 68       | 70       | 72       |
| 40        | 60       | 61       | 62       | 63       | 64       |
| 50        | 54       | 55       | 56       | 57       | 58       |
| 60        | 49       | 50       | 51       | 52       | 53       |
| 70        | 44       | 45       | 46       | 47       | 48       |
| 80        | 40       | 41       | 42       | 43       | 44       |
| 90        | 37       | 38       | 39       | 40       | 41       |
| 100       | 34       | 35       | 36       | 37       | 38       |

### E30

| MAP (kPa) | 2000 RPM | 3000 RPM | 4000 RPM | 5000 RPM | 6000 RPM |
|-----------|----------|----------|----------|----------|----------|
| 30        | 60       | 62       | 64       | 66       | 68       |
| 40        | 56       | 57       | 58       | 59       | 60       |
| 50        | 50       | 51       | 52       | 53       | 54       |
| 60        | 45       | 46       | 47       | 48       | 49       |
| 70        | 40       | 41       | 42       | 43       | 44       |
| 80        | 36       | 37       | 38       | 39       | 40       |
| 90        | 33       | 34       | 35       | 36       | 37       |
| 100       | 30       | 31       | 32       | 33       | 34       |

### E60

| MAP (kPa) | 2000 RPM | 3000 RPM | 4000 RPM | 5000 RPM | 6000 RPM |
|-----------|----------|----------|----------|----------|----------|
| 30        | 57       | 59       | 61       | 63       | 65       |
| 40        | 53       | 54       | 55       | 56       | 57       |
| 50        | 47       | 48       | 49       | 50       | 51       |
| 60        | 42       | 43       | 44       | 45       | 46       |
| 70        | 37       | 38       | 39       | 40       | 41       |
| 80        | 33       | 34       | 35       | 36       | 37       |
| 90        | 30       | 31       | 32       | 33       | 34       |
| 100       | 27       | 28       | 29       | 30       | 31       |

### E85

| MAP (kPa) | 2000 RPM | 3000 RPM | 4000 RPM | 5000 RPM | 6000 RPM |
|-----------|----------|----------|----------|----------|----------|
| 30        | 53       | 55       | 57       | 59       | 61       |
| 40        | 49       | 50       | 51       | 52       | 53       |
| 50        | 43       | 44       | 45       | 46       | 47       |
| 60        | 38       | 39       | 40       | 41       | 42       |
| 70        | 33       | 34       | 35       | 36       | 37       |
| 80        | 29       | 30       | 31       | 32       | 33       |
| 90        | 26       | 27       | 28       | 29       | 30       |
| 100       | 23       | 24       | 25       | 26       | 27       |

---

## Summary of Key Corrections Applied

| Variable         | Effect on CA100                                    |
|------------------|----------------------------------------------------|
| MAP 30→100 kPa   | −40 to −45° (dominant effect)                     |
| RPM 2000→6000    | +8° at fixed MAP (turbulence gain < time loss)    |
| Low→Medium cam   | −2 to −8° (MAP-dependent, largest at light load)  |
| Low→Large cam    | −3 to −14° (MAP-dependent, largest at light load) |
| E0→E30           | −4° uniform                                       |
| E0→E60           | −7° uniform                                       |
| E0→E85           | −11° uniform                                      |

> **Note:** All values are model-estimated from empirical literature parameterization, not directly measured on a specific engine. Real CA100 varies with combustion chamber geometry, spark plug location, compression ratio, and mixture preparation quality. Use as a calibration starting point, not a ground truth.

# Reading
(1) Heywood 1988

(2) Ricardo 1920s-30s

(3) Caris & Nelson 1959