# Stuck-throttle protection that allows brake boosting

## The conflict

Brake boosting = left-foot braking while the accelerator pedal is depressed, holding
the throttle open against the brakes to spool the turbo.

EMU Black has a **built-in brake-based "Stuck throttle" engine protection**
(Engine protection → Stuck throttle). It triggers on:

    brake pressed  AND  TPS > TPS level  sustained > Brake timeout,  above Minimum RPM
    → engine cut

It looks at **brake + TPS only, NOT pedal (PPS)** — so it cannot tell an intentional
brake-boost from a genuinely stuck throttle. As shipped on this car it is **enabled**
(TPS level 30%, Brake timeout 600 ms, Min RPM 1000). A launch brake-boost easily
exceeds 30% TPS for >600 ms, so **this feature will cut a brake-boost if a brake input
is wired.** (Confirm whether brake is actually assigned — pinout shows clutch on
Switch 3, no brake switch; if brake is unassigned the feature is currently inert.)

Resolution: don't rely on the brake-based box for real protection. Relax it enough to
tolerate your brake-boost technique, and make the **pedal/sensor-referenced** layers
(dual-TPS plausibility + DBW closed-loop position error) the primary defense — those
are brake-independent and never interfere with brake boosting.

## PPS is the correct discriminator

The dangerous case and the intentional case separate cleanly by pedal position:

| Scenario       | PPS (pedal)            | Throttle (TPS)        | Action       |
|----------------|------------------------|-----------------------|--------------|
| Brake boost    | HIGH (commanding it)   | open — commanded      | leave alone  |
| Stuck throttle | LOW (foot off)         | open — uncommanded    | fault / cut  |

Any protection that watches **PPS-vs-throttle** is inherently brake-boost-safe: it
cannot trip while the driver is commanding throttle, because brake boost holds PPS high.

## EMU Black configuration

The two relevant config screens:
- **TPS, PPS → TPS**: Main signal input = Analog input 2 (B4); Voltage 0%/100% =
  0.69 / 4.31 V; Main valid 0.12–4.86 V; **Check signal input = None** (dual-TPS
  plausibility currently OFF); Check valid 0.2–4.8 V; Error tolerance 0.49 V.
- **Engine protection → Stuck throttle**: Enable ✔; Minimum RPM 1000; TPS level 30;
  Brake timeout 600 ms.

Priority order — make the brake-independent layers primary:

1. **Dual-TPS plausibility via `Check signal input` (currently None = OFF).**
   This is the highest-value upgrade and the reason for the Bosch TB swap. With
   `Check signal input = None`, the redundant-sensor check is inactive and
   `Error tolerance 0.49 V` does nothing. After the Bosch swap: set
   `Check signal input` to the analog where TPS2 lands (free: input 1 or 3), set its
   valid min/max, and tune the error tolerance. Catches a *lying sensor*.
   Brake-independent. (Post-stall code **16384** is this plausibility fault firing.)

2. **Closed-loop DBW position-error monitor.** DBW target is pedal-derived (armed
   airflow table when PPS < 2.0%, then idle PID). A physically stuck blade means
   actual TPS won't follow target → position error → limp. Brake-independent. Set
   max position error tight; debounce just above servo settling (~200–400 ms).

3. **Brake-based "Stuck throttle" box — relax it to tolerate brake boosting.**
   Because it uses brake + TPS (no PPS), it can't distinguish brake-boost from a
   stuck throttle. **Confirmed on this car: brake switch is wired and this box was
   actively cutting brake-boosts at the stock 30% / 600 ms settings.** Normal
   trail-braking/heel-toe only peaks ~18% TPS for <0.5 s (logs `drivehome`,
   `drive_wobble`), so it never trips on normal driving — only deliberate brake-boost.

   Interim setting (before dual-TPS is live) — the safer lever is **TPS level**
   because raising it preserves a *fast* cut for a high/WOT-stuck blade and only
   ignores partial-throttle-while-braking:

   | Setting       | Stock   | Interim |
   |---------------|---------|---------|
   | Enable        | ✔       | ✔ keep  |
   | Minimum RPM   | 1000    | 1000    |
   | TPS level     | 30      | **70**  |
   | Brake timeout | 600 ms  | **1500 ms** |

   If it still cuts mid-boost, raise Brake timeout toward 2000–2500 ms before
   touching TPS level again. Then log a real brake-boost and set TPS level to just
   above measured peak (≈ peak + 10%) to recover sensitivity. Keep it
   enabled-but-permissive as a coarse brake+WOT backstop; the real protection is
   #1 and #2. After the Bosch swap makes #1 live, this box can be relaxed further.

4. **Bound the failure with a fuel/RPM cut — critical on this airflow cal.**
   Scale: 2.0% TPS = 0 airflow, 6.4% TPS = 100% airflow. The DBW mechanical
   spring-home angle (~5–7°) sits well *above* the 2% zero-airflow point, so a fault
   that drops to spring-home can still flow meaningful air. Pair the throttle limp
   action with a limp **fuel-cut RPM cap**, not just a throttle angle — otherwise
   spring-home airflow can run RPM up.

## Principle

The brake-based feature trips on brake + throttle and is blind to the pedal, so it
*inherently* trades sensitivity against brake boosting. The genuinely dangerous case
(throttle open, **pedal released**) is caught instead by the pedal/sensor-referenced
layers (dual-TPS plausibility + DBW position error), which never look at the brake.
Lean on those; keep the brake-based box permissive.
