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

# MBT / KLSA Ignition Timing (° BTDC) — 238 / 264 / 272° Cams, E0 vs E100

Rows: RPM 1k→8k | Columns: MAP 30→200 kPa
≤100 kPa = MBT | >100 kPa = KLSA | ≤60 kPa capped 55° BTDC
E0 KR = max(0,(MAP−100)×0.15)° | E100 KR ≈ 0° (RON ~108)

---
## 238° Cam Duration

### E0

| RPM | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 130 | 140 | 150 | 160 | 170 | 180 | 190 | 200 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1k | 55 | 55 | 52 | 45 | 40 | 35 | 31 | 27 | 24 | 22 | 20 | 17 | 14 | 12 | 11 | 8 | 6 | 4 |
| 2k | 55 | 55 | 54 | 47 | 42 | 37 | 33 | 29 | 26 | 24 | 22 | 19 | 16 | 14 | 13 | 10 | 8 | 6 |
| 3k | 55 | 55 | 55 | 49 | 44 | 39 | 35 | 32 | 29 | 26 | 24 | 21 | 18 | 16 | 15 | 12 | 10 | 8 |
| 4k | 55 | 55 | 55 | 51 | 46 | 41 | 37 | 34 | 31 | 29 | 27 | 23 | 20 | 18 | 17 | 14 | 12 | 10 |
| 5k | 55 | 55 | 55 | 53 | 48 | 43 | 39 | 36 | 33 | 31 | 29 | 26 | 23 | 20 | 19 | 16 | 14 | 12 |
| 6k | 55 | 55 | 55 | 55 | 50 | 45 | 41 | 38 | 35 | 33 | 31 | 28 | 25 | 23 | 22 | 19 | 17 | 14 |
| 7k | 55 | 55 | 55 | 55 | 52 | 47 | 43 | 40 | 37 | 35 | 33 | 30 | 27 | 25 | 24 | 21 | 19 | 17 |
| 8k | 55 | 55 | 55 | 55 | 54 | 49 | 45 | 42 | 39 | 37 | 35 | 32 | 29 | 27 | 26 | 23 | 21 | 19 |

### E100

| RPM | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 130 | 140 | 150 | 160 | 170 | 180 | 190 | 200 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1k | 53 | 46 | 39 | 32 | 26 | 21 | 17 | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 8 | 7 | 6 | 5 |
| 2k | 55 | 48 | 41 | 34 | 28 | 23 | 19 | 16 | 15 | 14 | 13 | 12 | 11 | 10 | 10 | 9 | 8 | 7 |
| 3k | 55 | 50 | 43 | 36 | 31 | 25 | 21 | 18 | 17 | 16 | 15 | 14 | 13 | 12 | 12 | 11 | 10 | 9 |
| 4k | 55 | 52 | 45 | 38 | 33 | 27 | 23 | 20 | 19 | 18 | 17 | 16 | 15 | 14 | 14 | 13 | 12 | 11 |
| 5k | 55 | 54 | 47 | 40 | 35 | 29 | 25 | 22 | 21 | 20 | 19 | 18 | 17 | 16 | 16 | 15 | 14 | 13 |
| 6k | 55 | 55 | 49 | 42 | 37 | 32 | 27 | 24 | 23 | 22 | 21 | 20 | 19 | 18 | 18 | 17 | 16 | 15 |
| 7k | 55 | 55 | 51 | 44 | 39 | 34 | 29 | 26 | 25 | 24 | 23 | 22 | 21 | 20 | 20 | 19 | 18 | 17 |
| 8k | 55 | 55 | 53 | 46 | 41 | 36 | 32 | 28 | 27 | 26 | 25 | 24 | 23 | 22 | 22 | 21 | 20 | 19 |

---
## 264° Cam Duration

### E0

| RPM | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 130 | 140 | 150 | 160 | 170 | 180 | 190 | 200 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1k | 55 | 54 | 47 | 42 | 37 | 33 | 28 | 25 | 22 | 20 | 18 | 15 | 12 | 10 | 9 | 6 | 4 | 2 |
| 2k | 55 | 55 | 49 | 44 | 39 | 35 | 31 | 27 | 24 | 22 | 20 | 17 | 14 | 12 | 11 | 8 | 6 | 4 |
| 3k | 55 | 55 | 51 | 46 | 41 | 37 | 33 | 29 | 26 | 24 | 22 | 19 | 16 | 14 | 13 | 10 | 8 | 6 |
| 4k | 55 | 55 | 53 | 48 | 43 | 39 | 35 | 32 | 29 | 26 | 24 | 21 | 18 | 16 | 15 | 12 | 10 | 8 |
| 5k | 55 | 55 | 55 | 50 | 45 | 41 | 37 | 34 | 31 | 29 | 27 | 23 | 20 | 18 | 17 | 14 | 12 | 10 |
| 6k | 55 | 55 | 55 | 52 | 47 | 43 | 39 | 36 | 33 | 31 | 29 | 26 | 23 | 20 | 19 | 16 | 14 | 12 |
| 7k | 55 | 55 | 55 | 54 | 49 | 45 | 41 | 38 | 35 | 33 | 31 | 28 | 25 | 23 | 22 | 19 | 17 | 14 |
| 8k | 55 | 55 | 55 | 55 | 51 | 47 | 43 | 40 | 37 | 35 | 33 | 30 | 27 | 25 | 24 | 21 | 19 | 17 |

### E100

| RPM | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 130 | 140 | 150 | 160 | 170 | 180 | 190 | 200 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1k | 46 | 41 | 34 | 28 | 23 | 19 | 15 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 6 | 4 | 3 | 2 |
| 2k | 48 | 43 | 36 | 31 | 25 | 21 | 17 | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 8 | 7 | 6 | 5 |
| 3k | 50 | 45 | 38 | 33 | 27 | 23 | 19 | 16 | 15 | 14 | 13 | 12 | 11 | 10 | 10 | 9 | 8 | 7 |
| 4k | 52 | 47 | 40 | 35 | 29 | 25 | 21 | 18 | 17 | 16 | 15 | 14 | 13 | 12 | 12 | 11 | 10 | 9 |
| 5k | 54 | 49 | 42 | 37 | 32 | 27 | 23 | 20 | 19 | 18 | 17 | 16 | 15 | 14 | 14 | 13 | 12 | 11 |
| 6k | 55 | 51 | 44 | 39 | 34 | 29 | 25 | 22 | 21 | 20 | 19 | 18 | 17 | 16 | 16 | 15 | 14 | 13 |
| 7k | 55 | 53 | 46 | 41 | 36 | 32 | 27 | 24 | 23 | 22 | 21 | 20 | 19 | 18 | 18 | 17 | 16 | 15 |
| 8k | 55 | 55 | 48 | 43 | 38 | 34 | 29 | 26 | 25 | 24 | 23 | 22 | 21 | 20 | 20 | 19 | 18 | 17 |

---
## 272° Cam Duration

### E0

| RPM | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 130 | 140 | 150 | 160 | 170 | 180 | 190 | 200 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1k | 55 | 52 | 46 | 41 | 36 | 32 | 28 | 25 | 22 | 20 | 18 | 15 | 12 | 10 | 9 | 6 | 4 | 2 |
| 2k | 55 | 54 | 48 | 43 | 38 | 34 | 31 | 27 | 24 | 22 | 20 | 17 | 14 | 12 | 11 | 8 | 6 | 4 |
| 3k | 55 | 55 | 50 | 45 | 40 | 36 | 33 | 29 | 26 | 24 | 22 | 19 | 16 | 14 | 13 | 10 | 8 | 6 |
| 4k | 55 | 55 | 52 | 47 | 42 | 38 | 35 | 32 | 29 | 26 | 24 | 21 | 18 | 16 | 15 | 12 | 10 | 8 |
| 5k | 55 | 55 | 54 | 49 | 44 | 40 | 37 | 34 | 31 | 29 | 27 | 23 | 20 | 18 | 17 | 14 | 12 | 10 |
| 6k | 55 | 55 | 55 | 51 | 46 | 42 | 39 | 36 | 33 | 31 | 29 | 26 | 23 | 20 | 19 | 16 | 14 | 12 |
| 7k | 55 | 55 | 55 | 53 | 48 | 44 | 41 | 38 | 35 | 33 | 31 | 28 | 25 | 23 | 22 | 19 | 17 | 14 |
| 8k | 55 | 55 | 55 | 55 | 50 | 46 | 43 | 40 | 37 | 35 | 33 | 30 | 27 | 25 | 24 | 21 | 19 | 17 |

### E100

| RPM | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 130 | 140 | 150 | 160 | 170 | 180 | 190 | 200 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1k | 43 | 39 | 33 | 27 | 22 | 18 | 15 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 6 | 4 | 3 | 2 |
| 2k | 45 | 41 | 35 | 29 | 24 | 20 | 17 | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 8 | 7 | 6 | 5 |
| 3k | 47 | 43 | 37 | 32 | 26 | 22 | 19 | 16 | 15 | 14 | 13 | 12 | 11 | 10 | 10 | 9 | 8 | 7 |
| 4k | 49 | 45 | 39 | 34 | 28 | 24 | 21 | 18 | 17 | 16 | 15 | 14 | 13 | 12 | 12 | 11 | 10 | 9 |
| 5k | 51 | 47 | 41 | 36 | 31 | 26 | 23 | 20 | 19 | 18 | 17 | 16 | 15 | 14 | 14 | 13 | 12 | 11 |
| 6k | 53 | 49 | 43 | 38 | 33 | 28 | 25 | 22 | 21 | 20 | 19 | 18 | 17 | 16 | 16 | 15 | 14 | 13 |
| 7k | 55 | 51 | 45 | 40 | 35 | 31 | 27 | 24 | 23 | 22 | 21 | 20 | 19 | 18 | 18 | 17 | 16 | 15 |
| 8k | 55 | 53 | 47 | 42 | 37 | 33 | 29 | 26 | 25 | 24 | 23 | 22 | 21 | 20 | 20 | 19 | 18 | 17 |


# Reading
(1) Heywood 1988

(2) Ricardo 1920s-30s

(3) Caris & Nelson 1959