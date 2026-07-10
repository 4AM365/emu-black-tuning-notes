# Ignition — EMU settings hub

> Digest of [ignition.md](../ignition.md) — the dense note is canonical; if they disagree, it wins.

**What this covers:** which EMU ignition table owns each job, and the five principles (MBT/KLSA, knock vs preignition, cam/fuel/load demand, knock-band variance, VVT coupling) behind every cell.

**The rules:**

- `ignTable`/`ignTable2` (pump/ethanol, blended by ethanol content): target MBT where the fuel allows, KLSA where it doesn't. U-shape vs RPM, ~2° less per 30 kPa across MAP, more timing up the RPM axis.
- Cruise MBT is found with an EGT sensor, not guessed — lower EGT means closer; rising MAP at constant pedal confirms it. Build a ~1° plateau across the cruise MAP band.
- Don't dial timing by reshaping the flex blend — advance Table 2; the blend fraction scales the delta that reaches the wheel.
- Preignition (chamber lights the mixture before the spark, runaway) is far more destructive than knock (end-gas after the spark). Over-advance costs torque and raises EGT before it knocks.
- Knock voltage is a boost-region tool only; at idle use RPM CoV. And watch knock-band *variance*, not just spikes — a walking baseline means the cylinders aren't uniform.
- Idle ignition: base advance below MBT so the PID has recovery reserve; knock a high hot idle down with retard (reversible), not air.
- Overrun retard: enter fast, exit slow — a fast advance restore stacks with the re-fuel event and makes the airflow PID chase it.
- Lock cam advance per cell before pulling for MBT; re-verify timing wherever you change cam advance.

**Key numbers:** idle/low-load starting ranges 10–12° (pump/stock) to 19–22° (ethanol/big cam); cruise reaches high-30s (pump) to low-40s (cammed ethanol); boost MBT low-20s° BTDC on a 4-valve I6. Walk boost timing in 1° steps.

**When to care:** before editing any EMU ignition table, and when deciding which lever — base table, idle, blend, or overrun — owns a symptom.
