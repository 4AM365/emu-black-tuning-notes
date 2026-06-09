# Coil Setup

This is reusable coil/hardware reference (part numbers, dwell behavior), not a per-car calibration. The specific coil a given build runs lives in that build's working doc (e.g. [`supra/notes/my_car.md`](../supra/notes/my_car.md)).

## D585

The GM D585 is a common aftermarket coil used with standalone ECUs. It is not a plug-in replacement for Toyota coils but is a reliable, widely available option.

Several different coils are commonly swapped onto Toyota-engine builds (2JZ, 1JZ, etc.) when running standalone ECUs.

## Denso 90919-A2004

Info from Frankenstein Motorworks (2GR & 2AR) — coils are roughly equivalent.

- 3 ms dwell = max energy
- 5 ms = some energy loss
- Will accept up to 26 V — same energy but faster charge

Frankenstein Motorworks 2GR coil dwell table (ms):

| Load | 6 V | 8 V | 10 V | 12 V | 14 V | 16 V |
|------|-----|-----|------|------|------|------|
| 80%  | 2.8 | 2.8 | 2.8  | 2.8  | 2.7  | 2.0  |
| 60%  | 2.8 | 2.7 | 2.5  | 2.3  | 2.2  | 1.9  |
| 20%  | 2.8 | 2.5 | 2.125| 1.750| 1.375| 1.0  |

## Toyota / Denso COP Reference

| Coil family                                        | OEM part numbers                               | Typical applications                                                                      |
| -------------------------------------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Early 2GR COP                                      | **90919-02251** (superseded)                   | Early **2GR-FE / 2GR-FSE** (Camry, Avalon, Highlander, Sienna, Lexus ES/GS)              |
| Mid-era Toyota COP (2GR / 2AR / 1AR)               | **90919-A2004**                                | **2GR-FE**, **2AR-FE**, **1AR-FE** across multiple Toyota platforms                       |
| Later service replacement (consolidated)           | **90919-A2013**                                | Dealer replacement for earlier 2GR-family coils including 90919-02251                     |
| Very common 2AR / multi-engine COP                 | **90919-A2005** *(cross-ref Denso 673-1309)*   | **2AR-FE / 2AR-FXE**, also used on several other Toyota engines                           |
| Late-model Toyota COP (broad fitment)              | **90919-02260**                                | Later Toyota platforms incl. **2GR-FKS**, Tacoma, supersedes older coils                 |
| Denso aftermarket Toyota COP                       | **Denso 673-1301** (superseded SKU)            | Toyota / Lexus OE-style replacement                                                       |
| Non-Toyota comparison coil (aftermarket benchmark) | **GM / ACDelco D585-style**                    | Common aftermarket / standalone ECU coil (not Toyota plug-in)                             |

## Connector Part Numbers

- Yazaki: 90980-11885
- Sumitomo: 90980-12176
