# Functions — digest

Canonical: [../functions.md](../functions.md).

**What this covers.** The Functions software page, and how the 12 user functions (`userFunctions`) are stored in the tune XML.

**The rules**
- A user function can stand in for a physical input: point an input selector (e.g. `acActivation`) at Fn n, which the XML stores as the value 19 + n.
- Use output "Virtual" and action "Set output only" when the function only feeds a strategy. A non-Virtual output also drives that pin.
- An empty operator line in the GUI is a real operator and uses a slot. Remove it with right-click → Remove operator.
- Every operator has True and False delays. A False delay bridges input dropouts shorter than the delay, which works as a debounce.

**Key numbers.** XML: 12 × 13 B function records + 32 × 7 B operator records. Operator type: 0 Is True, 1 Is False, 4 Less, 6 Greater. Channel ids: 0x10 Switch 1, 0x11 Switch 2, 0x39 Engine runtime.

**When to care.** Reading or checking any function from an XML export, or gating a strategy on runtime or a switch combination (e.g. the Supra's A/C after-start delay).
