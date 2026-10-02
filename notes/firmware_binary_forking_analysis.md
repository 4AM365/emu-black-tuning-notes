# EMU Black V3 firmware `.bin` — forking / custom-firmware analysis

**Date:** 2026-08-18
**Analyzed:** `C:\Program Files (x86)\Ecumaster\EMU Black V3\Firmware\emuBlack_3_0XX.bin` (focus 3.061)
**Question asked:** Can we fork 3.061 to add/repurpose tuning functions? Or build ground-up firmware for EMU Black?

> Purpose of this note: I keep forgetting what I found and re-running the same teardown. This is the record so I don't. If you're re-reading this to decide whether to try again — the short answer is at the bottom under **VERDICT**.

---

## What the file actually is

Every `emuBlack_3_0XX.bin` = **28-byte header + two encrypted payload sections.**

Header layout (all little-endian), confirmed by parsing all 12 files 019–061:

| Offset | Bytes | Field | Value in 3.061 |
|--------|-------|-------|----------------|
| 0x00 | 4 | magic | `"emb3"` (65 6d 62 33) |
| 0x04 | 4 | format | `1` |
| 0x08 | 4 | version | `3061` (0x0BF5) |
| 0x0C | 4 | len sec1 | 194632 |
| 0x10 | 4 | len sec2 | 16994 |
| 0x14 | 4 | **CRC sec1** | 0x29C6 (low 16 bits used) |
| 0x18 | 4 | **CRC sec2** | 0x08EC |
| 0x1C | — | payload | sec1 then sec2 |

- **The two checksums are CRC-16/MODBUS** (poly 0x8005, init 0xFFFF, refin/refout) computed over each *encrypted* section. Confirmed exact match on 3.057, 3.059, 3.061. `len1 + len2 + 28 == filesize` exactly.
- **There is NO digital signature.** No RSA/ECDSA block, no HMAC — just those two CRC-16s. Integrity only, not authentication. A modified image can be made to pass the CRC by recomputing it. (Whether the *bootloader on the ECU* does more than CRC is unknown — see caveats.)

## The encryption (this is the wall)

The payload is not plaintext ARM code — it's encrypted/obfuscated. Evidence and what it rules in/out:

1. **Entropy ≈ 7.97 bits/byte** across both sections — looks random at a glance.
2. **BUT it is position-keyed, not avalanche.** This is the key finding:
   - `3.059`, `3.060`, `3.061` are **all exactly 211654 bytes** and differ by only **4–6 bytes total.** (059↔060: 4 bytes. 060↔061: 6 bytes. Longest identical run: 114,537 bytes.)
   - Exact diff offsets 059/060/061 (file offsets): 0x25BC, 0x2A50–0x2A51, 0x158F8, 0x17AE8, 0x17B5C.
   - A real cipher (AES-CBC/CTR, etc.) would avalanche — change a few plaintext bytes and ~50% of ciphertext flips. Here it doesn't. **So ciphertext[i] depends only on plaintext[i] and position i, with a keystream that is identical across builds.** i.e. `cipher = plain XOR keystream(i)`, keystream fixed.
3. **Not a simple repeating XOR though.** Column-mode over a 256 period gives only ~8% dominance (a true 256-periodic XOR key would be ~90%+). Distribution-matching shows a weak ~1.25× signal and autocorrelation spikes at *exact* multiples of 256 (~11× the random baseline), concentrated in the first ~4 KB.
4. **Leading hypothesis: a fixed-key stream cipher — most likely RC4 (or a custom byte PRNG) with a key embedded in `EMU_BLACK_V3.exe`.** RC4 fits every observation: same keystream every build (fixed key), full-byte high entropy, and the subtle 256-boundary bias RC4 is known for. A LCG/PRNG keystream seeded by a constant would fit equally.

### Why this matters for cracking it
Because the keystream is **fixed across all versions**, this scheme dies to **known-plaintext**:
- If we ever obtain ONE decrypted image (dump an unprotected MCU over SWD, or an older/leaked plaintext build), then `keystream = cipher XOR plain` recovers the ENTIRE keystream, and **every** version decrypts forever after.
- Even without full plaintext, the cross-version diffs *already* tell us exactly which plaintext bytes changed between builds (the XOR of two versions cancels the keystream: `cipherA XOR cipherB = plainA XOR plainB`).
- The fixed key / PRNG seed almost certainly lives in `EMU_BLACK_V3.exe` (16.9 MB). Finding the encrypt/decrypt routine there is the realistic crack path — not brute force.

*(Note: the ARM vector-table known-plaintext guess at offset 0 failed — the code section either isn't at file offset 0 of sec1, has a different load layout, or sec1 is data-first. Didn't chase it further.)*

---

## The REAL fork surface (no firmware hacking needed)

You do **not** need to touch the `.bin` to add or repurpose most "tuning functions." EMU's behavior is heavily data-driven by plaintext XML that ships in the install:

- **`XML\Project\version3_061.xml`** (574 KB, plain text) is the full definition layer for the matching firmware:
  - **1799 `<symbol>`** definitions (every scalar/table, with storage type, divider, unit, min/max, default, axis bins)
  - **245 `<table>`**, **281 `<rule>`** (conditional enable/disable/visibility logic), **12 `<function>`** slots
  - CAN stream defs (`userCANStream`, `userFunctions`, OBD2, dash protocols), wizards, log groups
- **`userFunctions` / Fn 1–12** = the stock **programmable-logic engine** already in firmware. This is the intended "add a function" mechanism: build logic from inputs/comparators/timers/tables, drive outputs, custom CAN — all configured, no code.
- Other repurposing surfaces already exposed: spare PWM tables (`pwmTable2`), rotary switch cals, generic analog inputs, CAN RX/TX mapping.

**What XML editing CAN do:** expose/rename/rescale parameters, change min/max/units/dividers, alter which options show, repoint tables, wire up CAN. Basically reshape the calibration + UI over the *existing* firmware capabilities.

**What XML editing CANNOT do:** add a genuinely new control algorithm the firmware doesn't already implement (e.g. a new closed-loop strategy, a new trigger decoder). Those live in the encrypted binary.

---

## Ground-up firmware for EMU Black

Feasible in principle, very large in practice:

1. **MCU is almost certainly an STM32 (ARM Cortex-M).** Need to confirm the exact part (open the unit, read the chip) — determines core, flash/RAM map, peripherals.
2. **Readout protection (RDP) is likely set** on the production MCU, so you probably can't just SWD-dump the stock firmware to learn the hardware mapping.
3. You'd have to reverse the **board**: which pins/timers drive injectors & ignition, ADC channel↔sensor mapping, trigger input conditioning, flyback/driver ICs, CAN transceiver. That's bench reverse-engineering, not software.
4. The stock **bootloader** owns the `emb3` update format. To flash your own image through it you'd need to break the encryption (above) AND match whatever the bootloader validates. Alternatively, flash raw via SWD/JTAG if RDP allows — which on a protected part means a full chip erase (wipes the stock firmware you'd want as reference).
5. Realistic effort: multi-month reverse-engineering + bare-metal engine-management firmware from scratch. Doable by a determined person; not a weekend fork.

An easier middle path if the goal is "my own logic on this hardware": treat EMU as the base ECU and offload custom functions to an external device (Arduino/STM32/Teensy) over CAN, using EMU's user CAN streams + `userFunctions` to exchange data. Gets you custom behavior without cracking anything.

---

## VERDICT (so I don't redo this)

- **Direct `.bin` patching to add functions: NO** — practical wall is the fixed-keystream encryption over an opaque, undocumented ARM image. No signature (only CRC-16/MODBUS you can recompute), so it's *obfuscation not authentication*, but you still can't author code into a blob you can't read. Cracking it = find the key/PRNG in `EMU_BLACK_V3.exe` OR get one plaintext image (known-plaintext breaks all versions at once because the keystream is reused). That's a reverse-engineering project, not a config change.
- **"New tuning functions" the normal way: YES, via XML + Fn1–12 + CAN** — that's the intended and by far the cheapest surface. Start in `XML\Project\version3_061.xml`.
- **Ground-up firmware: possible but very large** (confirm STM32 part, reverse the board, deal with RDP + bootloader). External CAN co-processor is the pragmatic alternative.

## If re-attempting the crack, start here
1. Disassemble `EMU_BLACK_V3.exe` and search for the update/encrypt routine — look for RC4 KSA (`S[i]=i` 0..255 init loop) or an XOR-with-PRNG over a buffer right after CRC-16/MODBUS. The key/seed is the prize.
2. Or get any single decrypted image (SWD dump of an unprotected/dev unit, older plaintext build) → XOR against the matching `.bin` → full keystream → all versions decrypt.
3. Cross-version diffs are already a free oracle: `cipherA XOR cipherB` = plaintext delta. Diffing many consecutive builds maps which regions are code vs. rarely-changing tables.

## Scripts
Teardown scripts saved under this session's scratchpad (`an1.py`..`an8.py`): header parse, entropy/autocorrelation, XOR key attempts, cross-version diff, CRC identification. Re-runnable with miniconda python.
