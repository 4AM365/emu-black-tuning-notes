# A/C request input noise — digest

Digest of [`../ac_request_input_noise.md`](../ac_request_input_noise.md). The canonical note wins.

## What this covers
Whether the EMU's HVAC request signal is actually noisy, and what makes it noisy.

**Confirmed fixed (re-log 09-19, checked 2026-09-28):** with the clutch pressed, `Switch 1` edges fell from 416 to 6.8 per minute.

## Resolved 2026-08-29
**The clutch switch was returned to chassis ground instead of EMU sensor ground. Rewired to
sensor ground.** That is the pre-"P" switch-input violation this note predicted, and it explains
the whole signature. Everything below was measured *before* the fix — re-log in the vulnerable
state (clutch pressed, A/C not requesting) and re-run the state matrix before calling it closed.
The same fix is expected to clear the speed-input glitching
([vss_signal_integrity](vss_signal_integrity.md)).

## The rules
- The A/C request is the **`Switch 1`** log channel. Polarity checked — the switch
  inputs are not inverted, so the channel is the raw pin state.
- **It is noisy** — 40 ms single-sample toggles, far faster than anything the A/C
  amplifier can command. Present in every all-channels log since April 2026.
- **The trigger is the owner-installed clutch switch.** Not RPM, not road speed —
  those were confounds. The car has no OEM clutch start switch, so this is a
  coupling between two of Will's own runs at the EMU end.
- **The clutch signal itself stays clean.** Only the request line is corrupted, so
  it is coupling *into* `Switch 1`.
- **The ECU is hardware revision F — pre-"P".** ECUMaster documents that on
  pre-P hardware the three built-in switch inputs are *not* independent: only
  **sensor ground** may be applied to them, "otherwise the measurement from other
  inputs may be disturbed." That is exactly the observed pattern — the clutch pin
  reads clean while the two other switch inputs glitch together in opposite
  directions. Leading mechanism now.
- **Probably a fixed tie, not an intermittent connection.** The request pin gets
  parked near mid-rail whenever the clutch circuit is energized, and noise decides
  each sample. No pull-up or pull-down is configured on the switch inputs, so a
  high-impedance pin is free to be bent either way.
- It reaches the compressor: most clutch drop-outs are the request falling, not the
  RPM threshold. Lowering `acMinRPM` will not fix this.

## Key numbers
- Clutch pressed + compressor off: **~400 edges/min**. Clutch released: ~12/min.
- Clutch pressed + compressor **engaged**: ~45/min — an order of magnitude quieter.
- Brake state changes nothing (433 vs 444 /min).
- 37 of 70 compressor clutch edges land inside a clutch press, which occupies 9 % of the log.

## Why the engaged column is quiet
The amplifier's request output is a hard pull when requesting and a soft divided
level when not. A stiff source can't be dragged to mid-rail; a divided one can.
That is the mechanism.

## When to care
Any A/C-at-idle or idle-wobble work — the short-cycling in
[`idle_drive_wobble`](idle_drive_wobble.md) is mostly this.

**Test in the vulnerable state only:** clutch pressed, A/C *not* requesting.
Meter the request pin — mid-rail confirms a fixed tie. Then unplug the clutch
switch at the switch end and work the pedal to separate "energized wire" from
"loom moving". Start where the loom was opened for the clutch-switch install.
