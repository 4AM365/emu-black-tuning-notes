# Cranking PW vs time to start — plain version

**What this covers:** every logged Supra crank, with the injector pulse it got and how long it took to reach
750 rpm. Canonical note (full table): `supra/notes/cranking_pw_vs_start.md`. Re-run
`supra/notes/cranking_pw_vs_start/scan_crank_events.py` to add new starts.

## The rules
- The dose at the **end** of the crank decides how long it takes, not the first second.
- Cold: end net PW ~2.0–2.5 ms → starts in 0.4–2.4 s. End net ~1.1 ms → 3.7–7.5 s or no start.
- Chart: `cranking_pw_vs_start/pw_vs_start_by_clt.png` (average PW vs time to start, by CLT, post-06-29 cranks).
- Hot: net ~1.6–2.2 ms → 0.3–0.6 s. Today's 1.41 ms took 1.08 s.
- Too rich fails too: the July +51–59 % cranks and the 08-06 rich cranks never started.

## Key numbers
- 10-02 cold: 3.47 ms first second, 2.17 ms (net 1.12) at the end → 7.5 s.
- Proposed tables at the same conditions: cold end 2.81 ms (net 1.75, ≈ 2.1 at 90 kPa); hot 3.12 ms (net 1.72).

## When to care
Before and after any change to cranking fuel, anti-flood, cranking airflow or the VE 500 rpm row.
