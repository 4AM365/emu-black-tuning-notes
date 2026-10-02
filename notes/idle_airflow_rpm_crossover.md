# When lower idle RPM can require more airflow

This is a distinction between **air per cycle**, **net combustion airflow per
second**, and the EMU's DBW **Airflow %** command (a throttle-position command,
not a mass-flow measurement).

For a four-stroke engine, fresh-air mass flow is

```
m_dot_air = rho_i * V_d * eta_v * N / 120
```

where `N` is rpm, `rho_i` is inlet density and `eta_v` is effective fresh-charge
volumetric efficiency.  At unchanged MAP, charge temperature, and `eta_v`, a
speed reduction always reduces mass flow in direct proportion to RPM.  If `eta_v`
falls at lower speed, this equation says mass flow falls even more; lower VE alone
cannot explain a higher *mass flow per second*.

Idle is governed instead by torque balance.  Let `T_loss` be friction, pumping,
accessory and any driveline torque loss, and let `q` be the usable indicated work
per kg of fresh air (which includes combustion stability, residual dilution,
lambda, and ignition phasing).  Then, approximately,

```
m_air,cycle = T_loss * 4*pi / q
m_dot_air   = (N / 120) * T_loss * 4*pi / q
```

Thus a worsened low-RPM combustion condition (`q` smaller) raises the required
air **per cycle**.  It can also raise required net air **per second** if that
penalty is larger than the RPM and loss-torque reduction.  For low/high points,

```
m_dot_low / m_dot_high
  = (N_low / N_high) * (T_loss,low / T_loss,high) * (q_high / q_low)
```

Worked 900 vs 1000 rpm example, holding loss torque constant:

| Low-RPM usable work per kg (`q_low/q_high`) | `m_dot_900/m_dot_1000` |
|---:|---:|
| 1.00 | 0.900 |
| 0.90 | 1.000 |
| 0.85 | 1.059 |

So at 900 rpm, a 10% deterioration in torque per kg is the exact crossover; a
15% deterioration makes required net airflow 5.9% higher even though RPM is 10%
lower.  With declining `T_loss` at lower RPM, the required deterioration is
larger.  A cammed turbo engine can have such a deterioration near the low-idle
stability limit because residual dilution/reversion and partial burns reduce
cycle work, but it must be demonstrated from a log, not assumed.

For this Supra, do not infer net mass flow from the EMU `Estimated mass airflow`
channel at idle: `supra/notes/mass_flow_estimator_quirk.md` documents that
overlap/reversion can overstate it substantially.  Compare logged idle-air command,
MAP, lambda, ignition state and RPM instead.  The June 29 XML's active-airflow
table begins at 1000 rpm, so it contains no calibrated answer below 1000 rpm.

Sources: `corpus/ice_fundamentals.md` pp. 135--136 (idle has negligible brake
output; friction/pumping/accessory work must be supplied) and pp. 220--221
(residual fraction is typically about 30% at SI idle);
`notes/cammed_idle_instability.md` (residual dilution and partial-burn mechanism).
