# DaPao Space Mouse — Bill of Materials (BOM)

Full component list for both PCBs. All prices approximate USD at time of writing.

---

## Lower PCB (dia88mm)

| Ref | Description | Package | Qty | Approx Price | Source / Part # |
|-----|-------------|---------|-----|-------------|-----------------|
| U1 | Seeed XIAO ESP32-S3 | Castellated module | 1 | $6.90 | Seeed Studio SKU: 113991114 |
| U2 | TP4056 LiPo charge controller | SOP-8 | 1 | $0.15 | LCSC: C16581 |
| U3 | AP2112K-3.3V LDO regulator | SOT-23-5 | 1 | $0.12 | LCSC: C51118 |
| U4 | USBLC6-2SC6 USB ESD protection | SOT-23-6 | 1 | $0.20 | LCSC: C7519 |
| J1 | USB-C receptacle mid-mount | Through-hole+SMD | 1 | $0.30 | LCSC: C165948 |
| J2 | JST-PH 2-pin connector right-angle | Through-hole | 1 | $0.15 | LCSC: C173752 |
| J3 | FPC connector 6-pin 0.5mm top-contact | SMD | 1 | $0.20 | LCSC: C11021 |
| J4 | 5-pin header 2.54mm right-angle | Through-hole | 1 | $0.10 | generic |
| SW1 | SPDT slide switch MSK-12C02 (power) | SMD | 1 | $0.10 | LCSC: C431541 |
| SW2 | Tactile switch 3x4mm (BOOT) | SMD | 1 | $0.05 | LCSC: C318884 |
| SW3 | Tactile switch 3x4mm (RESET) | SMD | 1 | $0.05 | LCSC: C318884 |
| R_PU5 | 10kΩ resistor (JOY_SW pull-up only) | 0402 | 1 | $0.01 | generic 0402 |
| R5, R6 | 100kΩ resistor (VBAT divider) | 0402 | 2 | $0.01 ea | generic 0402 |
| R7 | 2kΩ resistor (TP4056 PROG, 500mA) | 0402 | 1 | $0.01 | generic 0402 |
| R8, R9 | 1kΩ resistor (LED current limit) | 0402 | 2 | $0.01 ea | generic 0402 |
| R10, R11 | 5.1kΩ resistor (USB-C CC lines) | 0402 | 2 | $0.01 ea | generic 0402 |
| ~~R_PU1–R_PU4~~ | ~~BTN pull-ups moved to upper PCB~~ | — | — | — | see upper PCB R1–R4 |
| C1–C4 | 100nF ceramic cap (decoupling) | 0402 | 4 | $0.01 ea | generic 0402 |
| C5–C7 | 10µF ceramic cap (bulk) | 0805 | 3 | $0.05 ea | generic 0805 |
| LED1 | Red LED (charge indicator) | 0402 | 1 | $0.02 | generic 0402 |
| LED2 | Green LED (standby indicator) | 0402 | 1 | $0.02 | generic 0402 |
| H1–H4 | M2 brass standoff 5mm | Through-hole | 4 | $0.05 ea | generic |
| — | Lower PCB fabrication (JLCPCB 5x) | dia88mm 2-layer 1.6mm | 1 set | ~$5–8 | JLCPCB / PCBWay |

**Lower PCB subtotal (single unit): ~$12–15**

---

## Upper PCB (dia54mm)

| Ref | Description | Package | Qty | Approx Price | Source / Part # |
|-----|-------------|---------|-----|-------------|-----------------|
| SW4 | Kailh micro switch 6x6mm upright (L-click) | Through-hole | 1 | $0.30 | LCSC: C455292 |
| SW5 | Kailh micro switch 6x6mm upright (R-click) | Through-hole | 1 | $0.30 | LCSC: C455292 |
| SW6 | Kailh micro switch 6x6mm side-mount (Back) | Through-hole | 1 | $0.35 | LCSC: C455292 (rotated 90°) |
| SW7 | Kailh micro switch 6x6mm side-mount (Fwd) | Through-hole | 1 | $0.35 | LCSC: C455292 (rotated 90°) |
| R1–R4 | 10kΩ pull-up resistors (BTN_LEFT/RIGHT/BACK/FWD) | 0402 | 4 | $0.01 ea | generic 0402 |
| J5 | FPC connector 6-pin 0.5mm top-contact | SMD | 1 | $0.20 | LCSC: C11021 |
| C1 | 100nF ceramic cap (3V3 decoupling) | 0402 | 1 | $0.01 | generic 0402 |
| H1, H2 | M2 brass standoff 3mm | Through-hole | 2 | $0.05 ea | generic |
| — | Upper PCB fabrication (JLCPCB 5x) | dia54mm 2-layer 1.0mm | 1 set | ~$5–8 | JLCPCB / PCBWay |

**Upper PCB subtotal (single unit): ~$7–10**

---

## Off-Board Hardware

| Item | Description | Qty | Approx Price | Source |
|------|-------------|-----|-------------|--------|
| Joystick | Analog thumbstick module 25x25mm (5-pin) | 1 | $1.50 | AliExpress / Amazon |
| Battery | LiPo 3.7V ~400mAh with JST-PH 2-pin | 1 | $4.00 | AliExpress / Adafruit |
| FPC cable | 6-pin 0.5mm pitch same-side ~80mm | 1 | $1.00 | AliExpress |
| M2 screws | M2 x 8mm stainless | 8 | $0.50 | generic |
| M2 nuts | M2 hex nut | 4 | $0.30 | generic |
| M2 set screw | M2 x 3mm grub screw | 1 | $0.10 | generic |
| Steel washers | 22mm OD round steel washer | 4 | $0.50 | hardware store |
| Rubber feet | Self-adhesive 10mm round | 4 | $0.50 | Amazon |
| Filament | PLA or PETG ~100g | 1 | $2.00 | generic |

**Off-board subtotal: ~$10–12**

---

## Total BOM Cost (Single Unit)

| Section | Cost |
|---------|------|
| Lower PCB (parts + fab) | ~$12–15 |
| Upper PCB (parts + fab) | ~$7–10 |
| Off-board hardware | ~$10–12 |
| **Total** | **~$30–40** |

> Note: PCB fab prices drop significantly for 5-board minimum orders. The cost above assumes ordering 5 boards (standard JLCPCB minimum) and building 1.

---

## PCB Ordering Notes

### JLCPCB Gerber export settings (from KiCad)
1. File -> Fabrication Outputs -> Gerbers
2. Output folder: `hardware/lower_pcb/gerbers/` or `hardware/upper_pcb/gerbers/`
3. Enable layers: F.Cu, B.Cu, F.SilkS, B.SilkS, F.Mask, B.Mask, Edge.Cuts
4. Also export Drill files (NC Drill, Excellon format, PTH + NPTH separate)
5. Zip the gerbers folder and upload to JLCPCB

### Recommended specs
| Setting | Lower PCB | Upper PCB |
|---------|-----------|-----------|
| Layers | 2 | 2 |
| Thickness | 1.6mm | 1.0mm |
| Surface finish | HASL (lead-free) or ENIG | HASL |
| Silkscreen | White | White |
| Solder mask | Green | Green |
| Min hole size | 0.3mm | 0.3mm |
