# Judging VE / fuel-table correctness from an EMU log

A complete "are the fuel tables correct?" assessment needs three passes, because a
VE error manifests differently depending on whether closed loop is active.

## 1. Steady-state cells → read Short Term Trim, NOT lambda error

When the engine is in a cell long enough for closed loop to act (lambda valid,
roughly steady RPM/MAP), the wideband **tracks the target** — STFT absorbs the VE
error. So:

- `Lambda 1 ≈ Lambda target` in steady cells tells you closed loop is *working*, not
  that VE is right.
- **The VE error lives in `Short term trim`.** Small STFT (±1–2%) = base VE is good.
  Large positive STFT = base VE lean; large negative = base VE rich.
- Sign matters: if STFT **never goes meaningfully negative anywhere**, no cell is
  rich → a correction should be **only-add** (never pull fuel).

## 2. Open-loop / acceleration cells → read lambda error directly

During rising RPM / fast transients, closed loop can't keep up, so the VE error
appears **directly as lambda error** (`Lambda 1 − Lambda target`). Filter to
rising-RPM + TPS>10% and bin onto the real veTable axes. This is the only place the
base dose is exposed without closed-loop masking. (On this build the log is
`lambdaDelay`-corrected, so cell attribution under accel is trustworthy — see the
lambda-delay memory.) The lean region typically forms a **diagonal band** climbing
up-and-right (lean load shifts to higher MAP as RPM rises).

## 3. Coverage → you can only vouch for cells you have data in

Build a per-cell sample-count map on the veTable grid (valid running samples). The
tables are "correct" only where adequately sampled. Always call out:

- **Unvisited high-RPM rows** (a street log rarely reaches redline) — completely
  unverified.
- **Unvisited high-MAP columns** above the max boost actually seen.
- **The high-RPM × high-boost corner** — empty in any street log, and the single
  place a lean cell destroys the engine. Never claim correctness here without a
  dedicated full-throttle pull to redline at target boost.

## Summary rule

Steady cells: STFT. Accel cells: lambda error. Everywhere: check coverage before
vouching. A clean STFT map + a corrected accel band validates the *street envelope*
only — boost and top-end remain unproven until logged under load.
