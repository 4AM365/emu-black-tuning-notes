# Oil versus coolant as an airflow reference

> Digest of [oil_temp_vs_coolant_airflow_reference.md](../oil_temp_vs_coolant_airflow_reference.md). The dense note is canonical.

**Verdict:** keep coolant temperature as the base-table reference and add oil temperature as a
separate, smooth idle-air correction. Do not replace coolant with oil temperature.

**Why:** at the same 96°C coolant temperature, the Supra has needed 51–58% idle air with cold oil
but only 28–31% with hot oil: a 20–29-point difference (1.1–1.6% TPS). Oil therefore resolves a
real long warm-up state that coolant misses. Coolant still carries cold port/wall, combustion, and
throttle-body thermal effects that oil cannot represent.

**Heat exchanger:** a coolant-to-oil exchanger is worthwhile if its bypass/thermostat strategy
warms oil when coolant is hotter and rejects oil heat when oil becomes hotter at load. It reduces
the required cold-oil air adder; it does not make the fluid temperatures interchangeable.

**Safety:** the current readable tune has no actual oil-temperature input assigned and defaults
oil-temperature failure to 100°C. For an oil correction that removes air as oil warms, failure
must instead read cold so a sensor fault leaves extra air rather than causing a stall.

**Current decision:** oil pressure is diagnostic/protection only; install and use a real oil-
temperature sensor for the correction. Any current oil-temperature chart axis is a time-model
inference, not sensor data or a value to tune from directly.
