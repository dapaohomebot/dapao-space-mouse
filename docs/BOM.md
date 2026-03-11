# Bill of Materials — DaPao Space Mouse (Dual PCB)

## Lower PCB Components

| Ref | Component | Description | Qty | Package | Est. Cost |
|-----|-----------|-------------|-----|---------|-----------|
| U1 | ESP32-S3-WROOM-1 | WiFi+BLE5 module, 4MB flash | 1 | Module | $2.50 |
| U2 | TP4056 | LiPo charge controller | 1 | SOP-8 | $0.30 |
| U3 | AP2112K-3.3 | 3.3V 600mA LDO | 1 | SOT-23-5 | $0.20 |
| U4 | USBLC6-2SC6 | USB ESD protection | 1 | SOT-23-6 | $0.25 |
| J1 | USB-C Receptacle | USB 2.0 Type-C | 1 | SMD 16-pin | $0.30 |
| J2 | JST-PH 2-pin | LiPo battery connector | 1 | TH | $0.10 |
| J3 | FPC 6-pin 0.5mm | Connector to upper PCB | 1 | SMD | $0.20 |
| J4 | Pin header 5-pin | Joystick module connector | 1 | 2.54mm TH | $0.10 |
| SW1 | Slide switch SPDT | Power on/off | 1 | TH | $0.10 |
| SW2 | Tactile switch | BOOT button | 1 | SMD | $0.10 |
| SW3 | Tactile switch | RESET button | 1 | SMD | $0.10 |
| D1 | Red LED | Charging indicator | 1 | 0603 | $0.05 |
| D2 | Green LED | Power/charge complete | 1 | 0603 | $0.05 |
| R1-R2 | 5.1kΩ Resistor | USB-C CC pull-down | 2 | 0402 | $0.02 ea |
| R3 | 2kΩ Resistor | TP4056 PROG (500mA) | 1 | 0402 | $0.02 |
| R4-R5 | 1kΩ Resistor | LED current limit | 2 | 0402 | $0.02 ea |
| R6-R10 | 10kΩ Resistor | Button/joystick pull-ups | 5 | 0402 | $0.02 ea |
| R11-R12 | 100kΩ Resistor | Battery voltage divider | 2 | 0402 | $0.02 ea |
| C1-C4 | 100nF Capacitor | ESP32 decoupling | 4 | 0402 | $0.02 ea |
| C5 | 10µF Capacitor | 3V3 bulk decoupling | 1 | 0603 | $0.05 |
| C6 | 10µF Capacitor | VBUS capacitor | 1 | 0603 | $0.05 |
| C7 | 10µF Capacitor | BAT+ capacitor | 1 | 0603 | $0.05 |

## Upper PCB Components

| Ref | Component | Description | Qty | Package | Est. Cost |
|-----|-----------|-------------|-----|---------|-----------|
| J5 | FPC 6-pin 0.5mm | Connector to lower PCB | 1 | SMD | $0.20 |
| SW4 | Kailh micro switch | Left click (plunger UP) | 1 | TH | $0.50 |
| SW5 | Kailh micro switch | Right click (plunger UP) | 1 | TH | $0.50 |
| SW6 | Tactile switch | Back (plunger faces LEFT) | 1 | Side-mount | $0.30 |
| SW7 | Tactile switch | Forward (plunger faces RIGHT) | 1 | Side-mount | $0.30 |
| C8 | 100nF Capacitor | Decoupling | 1 | 0402 | $0.02 |

## Interconnect

| Item | Description | Qty | Est. Cost |
|------|-------------|-----|-----------|
| FFC cable | 6-conductor, 0.5mm pitch, ~80mm | 1 | $0.50 |

## Mechanical & Other

| Item | Description | Qty | Est. Cost |
|------|-------------|-----|-----------|
| Joystick module | Alps RKJXV or similar | 1 | $1.50–3.00 |
| LiPo battery | 3.7V 500–800mAh | 1 | $3.00–5.00 |
| Lower PCB fab | ∅88mm circular, 2-layer, 1.6mm | 5 pcs | $5.00 |
| Upper PCB fab | ∅54mm circular, 2-layer, 1.0mm | 5 pcs | $3.00 |
| PLA/PETG filament | Case printing (~50g) | — | $2.00 |
| Steel washers | Base weight (M8–M10) | 4–6 | $1.00 |
| Rubber feet | Adhesive pads | 4 | $0.50 |
| M2 screws + standoffs | Assembly hardware | 8 | $0.75 |

## Cost Summary

| Category | Est. Cost |
|----------|-----------|
| Lower PCB components | ~$5.00 |
| Upper PCB components | ~$1.80 |
| FFC cable | $0.50 |
| PCB fabrication (both) | ~$8.00 |
| Joystick + battery | ~$5.00–8.00 |
| Mechanical | ~$4.25 |
| **Total** | **~$24–28** |

---

*LCSC part numbers to be finalized during schematic capture in KiCad.*
