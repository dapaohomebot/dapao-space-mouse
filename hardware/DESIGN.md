# DaPao Space Mouse — PCB Hardware Design

## Architecture: Dual-Board Stack

```
                  ┌─────────────────────┐
                  │    UPPER PCB (∅54mm) │ ← Inside body top
                  │  L/R clicks + FWD/BACK │
                  │     FPC connector    │
                  └──────────┬──────────┘
                             │ FFC/FPC cable (flexible)
                             │ (allows tilt movement)
                  ┌──────────┴──────────┐
                  │    LOWER PCB (∅88mm) │ ← Inside base
                  │  ESP32-S3 + charger  │
                  │  joystick + battery  │
                  │  USB-C + FPC conn    │
                  └─────────────────────┘
```

## Board Specifications

### Lower PCB (Base Board)
- **Shape**: Circular, ∅88mm (fits inside 94mm base ID with 3mm clearance)
- **Layers**: 2-layer (top + bottom copper)
- **Thickness**: 1.6mm standard
- **Mounting**: 4× M2 holes on 30mm radius (matching base standoffs)
- **Center cutout**: ∅27mm hole for joystick module (mounts from below)

### Upper PCB (Button Board)
- **Shape**: Circular, ∅54mm (fits inside 60mm body with 3mm clearance)
- **Layers**: 2-layer
- **Thickness**: 1.0mm (thinner to save space in body top)
- **Mounting**: 2× M2 holes for top frame attachment
- **Note**: This board tilts with the body — the FPC cable must flex

---

## Lower PCB — Schematic

### Power Section
```
USB-C VBUS (5V) ──┬── TP4056 VIN ── BAT+ ──┬── Slide Switch ── AP2112K VIN ── 3V3
                   │                          │
                   ├── CC1 ── 5.1kΩ ── GND    ├── Battery Voltage Divider
                   ├── CC2 ── 5.1kΩ ── GND    │     BAT+ ── 100kΩ ── VBAT_SENSE ── 100kΩ ── GND
                   │                          │
                   └── USBLC6 ── D+/D-        └── LiPo Battery (JST-PH)
                                                    3.7V 500-800mAh
```

### Power Components
| Ref | Component | Pins | Notes |
|-----|-----------|------|-------|
| U1 | ESP32-S3-WROOM-1 | Module | BLE + USB MCU |
| U2 | TP4056 | SOP-8 | LiPo charge IC, PROG resistor sets charge current |
| U3 | AP2112K-3.3 | SOT-23-5 | 3.3V LDO, 600mA |
| U4 | USBLC6-2SC6 | SOT-23-6 | USB ESD protection |
| J1 | USB-C Receptacle | 16-pin SMD | Charging + USB data |
| J2 | JST-PH 2-pin | Through-hole | LiPo battery connector |
| J3 | FPC 6-pin 0.5mm | SMD | Connection to upper PCB |
| J4 | Joystick header | 5-pin TH | Joystick module connection |
| SW1 | Slide switch | SPDT TH | Power on/off |
| SW2 | Tactile switch | SMD | BOOT (GPIO0) |
| SW3 | Tactile switch | SMD | RESET (EN) |
| D1 | Red LED | 0603 | Charging indicator |
| D2 | Green LED | 0603 | Power indicator |

### ESP32-S3 Pin Assignment
| GPIO | Function | Direction | Notes |
|------|----------|-----------|-------|
| GPIO1 | JOY_X (ADC1_CH0) | Input | Joystick X axis analog |
| GPIO2 | JOY_Y (ADC1_CH1) | Input | Joystick Y axis analog |
| GPIO3 | JOY_SW | Input | Joystick push switch (pull-up) |
| GPIO4 | VBAT_SENSE (ADC1_CH3) | Input | Battery voltage (via divider) |
| GPIO5 | BTN_LEFT | Input | From upper PCB via FPC (pull-up) |
| GPIO6 | BTN_RIGHT | Input | From upper PCB via FPC (pull-up) |
| GPIO7 | BTN_BACK | Input | From upper PCB via FPC (pull-up) |
| GPIO8 | BTN_FWD | Input | From upper PCB via FPC (pull-up) |
| GPIO19 | USB_D- | USB | USB data minus |
| GPIO20 | USB_D+ | USB | USB data plus |
| GPIO38 | LED_STATUS | Output | Optional RGB LED (WS2812B) |
| GPIO0 | BOOT | Input | Boot button (active low) |
| EN | RESET | Input | Reset button (active low) |

### FPC Connector Pinout (J3 — Lower PCB)
| Pin | Signal | Description |
|-----|--------|-------------|
| 1 | 3V3 | Power to upper PCB |
| 2 | GND | Ground |
| 3 | BTN_LEFT | Left mouse button (active low) |
| 4 | BTN_RIGHT | Right mouse button (active low) |
| 5 | BTN_BACK | Back button (active low) |
| 6 | BTN_FWD | Forward button (active low) |

### Joystick Header Pinout (J4)
| Pin | Signal | Description |
|-----|--------|-------------|
| 1 | 3V3 | Joystick VCC |
| 2 | GND | Joystick GND |
| 3 | JOY_X | X-axis potentiometer wiper |
| 4 | JOY_Y | Y-axis potentiometer wiper |
| 5 | JOY_SW | Push switch (active low) |

### Charge Circuit Detail
```
        TP4056
        ┌──────────┐
VBUS ───┤VIN    BAT├─── BAT+ (to LiPo via protection)
        │          │
GND ────┤GND   CHRG├─── R ── LED_RED ── GND  (charging)
        │          │
        │   STDBY  ├─── R ── LED_GRN ── GND  (full)
        │          │
        │    PROG  ├─── 2kΩ ── GND  (500mA charge current)
        └──────────┘
```

### Power Path
```
LiPo BAT+ ── Slide Switch ── AP2112K VIN ── 3V3 output
                                   │
USB VBUS ── TP4056 ── BAT+ ──────┘
(when plugged in, charges battery AND powers device)
```

---

## Upper PCB — Schematic

### Very simple board — just switches and connector

```
        FPC Connector (J5)
        ┌──────────┐
3V3 ────┤1      6  ├──── BTN_FWD
GND ────┤2      5  ├──── BTN_BACK
        │3      4  ├──── BTN_RIGHT
        │BTN_LEFT  │
        └──────────┘
            │ │ │ │
            │ │ │ └── SW7 ── GND  (Forward, right side of body)
            │ │ └──── SW6 ── GND  (Back, left side of body)
            │ └────── SW5 ── GND  (Right click, top right half-circle)
            └──────── SW4 ── GND  (Left click, top left half-circle)

Each button: signal pin ── switch ── GND
(Pull-up resistors are on the lower PCB, 10kΩ to 3V3)
```

### Upper PCB Components
| Ref | Component | Position | Notes |
|-----|-----------|----------|-------|
| J5 | FPC 6-pin 0.5mm | Center/bottom | Matching connector to lower PCB |
| SW4 | Kailh/Omron micro | Top-left | Left click (under half-circle button) |
| SW5 | Kailh/Omron micro | Top-right | Right click (under half-circle button) |
| SW6 | Tactile switch | Left edge | Back button (faces outward through body) |
| SW7 | Tactile switch | Right edge | Forward button (faces outward through body) |
| C1 | 100nF | Near J5 | Decoupling |

### Upper PCB Layout Notes
- SW4 and SW5 (L/R click) are positioned so their plungers face UP
  through the top frame — the half-circle rocker buttons press down on them
- SW6 and SW7 (Back/Forward) are positioned at the LEFT and RIGHT edges
  with plungers facing OUTWARD through the body shell side cutouts
- FPC connector at the bottom/center, cable routes down through the body
  interior to the lower PCB
- Keep the board thin (1.0mm) — limited vertical space in body top

---

## Inter-Board Connection

**FFC (Flat Flexible Cable):**
- Type: 6-conductor, 0.5mm pitch FFC
- Length: ~80mm (enough slack for full joystick tilt)
- Route: From lower PCB center → up through body interior → to upper PCB

The FFC must be long enough to accommodate ±18° tilt in all directions
without strain. Route it loosely through the center of the body shell.

---

## PCB Fabrication Notes

### Both Boards
- Manufacturer: JLCPCB
- Min trace width: 0.2mm (8mil)
- Min clearance: 0.2mm
- Via size: 0.3mm drill / 0.6mm pad
- Copper weight: 1oz
- Surface finish: HASL (lead-free)
- Solder mask: any color (black looks nice)

### Lower PCB Specific
- Circular outline ∅88mm
- Center cutout ∅27mm for joystick module
- USB-C connector at edge (aligned with base USB-C port)
- Keep clear area under ESP32-S3 antenna (no copper pour)
- 4× M2 mounting holes at 30mm radius

### Upper PCB Specific
- Circular outline ∅54mm
- 1.0mm board thickness (if available, else 1.6mm)
- Edge-mount switches for side buttons (SW6, SW7)
- 2× M2 mounting holes

---

## Design Validation Checklist

- [ ] ESP32-S3 reference design followed (decoupling, boot circuit)
- [ ] USB-C CC resistors present (5.1kΩ)
- [ ] Antenna keepout zone clear
- [ ] Battery protection circuit (DW01A + FS8205 or integrated in TP4056)
- [ ] Charge current set correctly (PROG resistor)
- [ ] All button pull-ups on lower PCB
- [ ] FPC pinout matches between boards
- [ ] Board outlines fit inside case (with tolerances)
- [ ] Mounting holes align with case standoffs
- [ ] USB-C position aligns with base port cutout
- [ ] Joystick center cutout clears the module
