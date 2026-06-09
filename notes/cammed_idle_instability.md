# Why Cammed Builds Idle So Badly

A cammed engine doesn't idle poorly because the tune is wrong. It idles poorly because
**at idle it is running on a charge so diluted by leftover exhaust that combustion is
barely stable** — and big cams make that dilution worse. The tune's job is to manage a
combustion process that is inherently close to the misfire limit, not to "fix" it. This
note explains the chain from cam geometry to RPM wobble, so the calibration choices in
[engine_start.md](engine_start.md) and [idle_stall.md](idle_stall.md) read as
consequences rather than rules.

> **Car-specific values live in the build working docs**, not here. For the reference build see [`supra/notes/`](../supra/notes/) — esp. [`idle_session_05242026.md`](../supra/notes/idle_session_05242026.md) and [`my_car.md`](../supra/notes/my_car.md). This note is intentionally car-agnostic: it explains the physics and the levers, not the literal targets for any one cam package.

---

## The one-sentence answer

Big cams trap and re-induct a large fraction of burned gas at idle; that diluted charge
burns slowly and erratically; erratic combustion means erratic torque; erratic torque
means the crank speed wanders and the idle controller is forever chasing it.

---

## The dilution → instability ladder (Heywood 9.4.3)

Combustion stability is governed by how much **inert burned gas** is mixed into the fresh
charge. Heywood (*Internal Combustion Engine Fundamentals* §9.4.3, Fig. 9.36) characterizes
it directly in terms of residual/EGR fraction at a fixed operating point:

| Burned-gas dilution | Combustion behavior | Stability |
|---|---|---|
| ~0% | fast, repeatable burn | good — COV of IMEP ~0.6% |
| ~10% | distribution widens | acceptable |
| **>20%** | slow-burn → partial-burn → misfire cycles appear and multiply | **poor** |
| higher still | "the point is eventually reached where the engine will not run at all" | dead |

The mechanism is a one-way ratchet: as dilution rises, *all stages of combustion lengthen*.
First some cycles burn so slowly they barely finish before the exhaust valve opens (slow
burn). Then some don't finish at all (partial burn). Then some never light (misfire). Each
weak or dead cycle is a torque hole. The proportion of bad cycles **increases rapidly**
once you're past the limit — it is not gradual.

---

## Idle is already a 30%-EGR engine — before you add cams

Here is the part that surprises people. On *any* throttled SI engine, the residual gas
fraction at idle is **~30%** (Heywood §6.4). The physics: at idle the throttle is nearly
shut, so manifold pressure is deep vacuum (~30–40 kPa) while the cylinder still has to push
its exhaust out against ~atmospheric pressure. When the intake valve opens into that vacuum,
burned gas blows *back* out of the cylinder and out of the exhaust port into the low-pressure
intake, then gets re-inducted. A stock engine idles with roughly a third of its charge being
last cycle's exhaust.

So a perfectly stock engine idles right around the **~20% "poor stability" threshold
already.** Idle roughness is not a defect you can tune away — Heywood Ch. 9 puts acceptable
COV of IMEP at "a few percent." Some idle shake is physics. The tune manages it; it cannot
delete it.

Cams take an engine that is already at the edge and push it over.

---

## How camshafts push past the limit

### 1. Valve overlap forces extra reversion at low MAP

Overlap is the window where intake and exhaust valves are open *together* near TDC.
Heywood §1.6: "If the intake flow is throttled to below exhaust manifold pressure, then
backflow of burned gases from the cylinder into the intake manifold occurs… During the
valve overlap period, backflow of burned gas from the exhaust port into the cylinder
occurs." Idle is precisely the condition this describes — intake throttled far below exhaust
pressure. A long-duration cam has a wider overlap window, so more burned gas changes
direction during it. More overlap at idle MAP = more residual = more dilution = further past
the stability limit.

Note that duration alone does it: a cam reground to more duration has more overlap **even at
the same lobe separation angle**, because each lobe is simply wider. Tightening LSA makes it
worse again.

### 2. The trapped residual can't be scavenged at idle

At high RPM and open throttle, intake momentum and a tuned exhaust scavenge the residual out
during overlap — that's what the cam is *for*. At idle there is no momentum and no
scavenging energy: the fresh charge can't sweep the burned gas out, so it stays. The cam's
breathing advantage at 6000 rpm is its breathing liability at 800.

### 3. On a turbo engine, exhaust backpressure makes reversion worse

The turbine is a restriction, so exhaust manifold pressure sits **above** intake pressure
across the idle/low-load range. That pressure ratio is exactly the thing driving backflow
during overlap. A turbo cammed engine reverts harder at idle than the same cammed engine
N/A. The RPM you idle at sets how much intake momentum you have to fight that reversion —
which is why the lever is *raise the idle target* (below).

---

## The knock-on effects that make it feel even worse

**Slow flame, so it wants more timing — but that steals controller authority.** A diluted
charge has a lower flame speed (the inert gas gets in the way of the flame front), so the
burn needs to start earlier to still center near the MBT crank angle. Cammed builds therefore
idle with more advance than stock (see the timing table in `engine_start.md`). But
ignition is also the *fast* idle-stability lever — the controller swings timing to catch RPM
dips. If you've spent your advance just getting a clean burn, you have less headroom to swing
into. Dilution simultaneously demands more base timing and shrinks the reserve.

**Per-cycle torque variation, not just slow drift.** Because the bad cycles (slow/partial/
misfire) are *random* cycle-to-cycle, the torque output is noisy at the firing frequency, not
a smooth offset. The crank speed jitters. On a closed-loop idle this reads as the controller
never settling — and on a build with cylinder-to-cylinder maldistribution (front-feed
manifolds), one chronically lean cylinder misfiring every few cycles adds a periodic torque
hole on top.

**Less stored energy to ride through a hole.** A weak cycle has to be bridged by flywheel
inertia until the next firing. Cammed builds often pair with lightweight flywheels, which
store less energy — so the same misfire produces a *bigger* RPM dip. This is why the fix is
partly "spin faster": kinetic energy goes with RPM².

---

## What the tuner actually does about it (and why)

None of these "cure" the instability — they move the operating point back from the cliff
edge and give the controllers something stable to work with.

| Lever | Why it works against dilution |
|---|---|
| **Raise the idle RPM target** (often a bit higher in summer than winter) | More intake momentum to fight reversion → lower residual; more flywheel energy (∝RPM²) to ride through weak cycles |
| **Run idle lambda slightly rich** (λ a little below 1) | A rich charge tolerates dilution better — faster flame, wider misfire margin. EMU help says it outright: "Lambda < 1 usually results in more stable idle" |
| **More base timing at idle** | Compensates the slow diluted-charge flame so peak pressure still lands near MBT |
| **Nail per-cylinder fuel trim first** | Removes the worst chronic-misfire cylinder before asking the PID to hold a stable speed |
| **Stable lambda above all** | EMU help: "lambda instability will cause RPM fluctuations" the airflow PID cannot fix — see below |

---

## Why this makes the airflow/PID job structurally harder

Two EMU Black realities follow directly from cammed dilution, and both are documented
elsewhere in this repo:

- **The mass-flow estimator lies at idle.** The high reverted flow through the throttle
  reads as airflow even though most of it is exhaust going back out — the channel can
  overstate true combustion airflow by ~10× at idle. Don't validate idle VE against it.
  See [supra/notes/mass_flow_estimator_quirk.md](../supra/notes/mass_flow_estimator_quirk.md).

- **The PID cannot fix combustion instability.** EMU's own idle help: "If the engine speed
  is unstable with a constant airflow setting, it likely indicates problems such as incorrect
  fueling… PID controllers cannot compensate for such issues." A diluted charge that
  occasionally misfires produces RPM noise that no amount of airflow-PID authority will
  smooth, because the disturbance is *inside the cylinder*, faster than the airflow loop
  (manifold time constant ~740 ms) can respond. The controllers' job is to hold the mean;
  the cycle-to-cycle scatter is combustion's, and you reduce it only by reducing dilution
  (RPM, lambda, timing) — not by chasing it.

This is also why idle quality on a cammed build should be measured as **crank-speed
fluctuation (RPM CoV)**, not knock voltage — see
[supra/notes/idle_rpm_cov_stability.md](../supra/notes/idle_rpm_cov_stability.md).

---

## The takeaway for the video

Cammed idle instability is not a calibration failure — it's the lean/dilute combustion limit
made visible. The cam buys top-end breathing by accepting more overlap, and at idle that same
overlap floods the cylinder with inert exhaust, dragging combustion toward the slow-burn /
misfire regime that Heywood's stability curve warns about. Everything the tuner does at idle —
higher target, richer lambda, more timing, tight per-cylinder fuel, a well-built airflow base
table — is in service of one goal: **keep the diluted charge burning repeatably enough that
the controllers only have to manage drift, not combustion.**
