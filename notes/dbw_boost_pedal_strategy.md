# DBW boost-region pedal strategy

Date: 2026-07-10

Principle: in positive manifold pressure, using the throttle blade as the main
torque reducer creates avoidable pressure drop across the blade. If the boost
target table already varies target pressure with pedal, the DBW characteristic
can open the throttle more aggressively in the high-MAP rows and let boost
target, wastegate duty, and normal spark/fuel controls carry more of the torque
request.

For the Supra table, `dbwCharacteristic1` is keyed by `dbwPPSBins` on X and
`dbwMAPBins` on Y:

- PPS bins raw: `0 14 2C 43 59 6F 85 9C B2 C8`
- PPS bins displayed: `0, 10, 22, 33.5, 44.5, 55.5, 66.5, 78, 89, 100 %`
- MAP bins: `20, 46, 71, 97, 123, 149, 174, 200 kPa`
- DBW characteristic display scale: `raw * 0.5 = throttle target %`

The proposed edit leaves 20-71 kPa unchanged, makes only a small transition at
97 kPa, and adds most opening from 123-200 kPa. Endpoints remain unchanged:
closed pedal still commands 4% target and WOT still commands 100%.

This is a calibration hypothesis, not a dyno-proven VE gain. The expected
benefit is lower throttle pressure drop and reduced pumping work in the high-MAP
part-pedal region. Verify with logs by comparing MAP, pre-throttle pressure if
available, DBW target/TPS, boost target, lambda, and knock/noise at fixed pedal
positions before and after import.
