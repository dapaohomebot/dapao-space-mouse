# DaPao Space Mouse — Development Plan

## Concept

A joystick-style mouse with a cylindrical "space mouse" body:

```
        ┌─────────────┐
        │  [L]   [R]  │  ← Top: Left/Right mouse buttons
        │             │
        ├─────────────┤
       / ╲           ╱ \
      │   ╲_________╱   │  ← Concave cylindrical body
      │                  │     Tilts X/Y for cursor movement
       \ ╱─────────╲  /
        ├───────────┤
   [◄]  │           │  [►]  ← Side buttons: Back / Forward
        │  (BASE)   │
        └───────────┘
              ↓
        Push down = click
```

**Input mapping:**
| Input | Action |
|---|---|
| Tilt X/Y | Mouse cursor movement |
| Push down (Z-axis) | Primary click (configurable) |
| Top-left button | Left click |
| Top-right button | Right click |
| Left side button | Browser back |
| Right side button | Browser forward |

---

## Phase 1: Mechanical Design (3D Model)

### 1.1 — Concept & Dimensions
- [ ] Define overall size (target: ~60mm body diameter, ~80mm tall, ~100mm base diameter)
- [ ] Sketch cross-section showing joystick pivot mechanism
- [ ] Define tilt range (±15–20° feels natural for joystick mice)
- [ ] Choose assembly method: snap-fit clips + 2–4 screws

### 1.2 — Joystick Mechanism
- [ ] Design gimbal/ball-joint pivot at base of cylinder
- [ ] Spring-return centering mechanism (compression spring or elastomer)
- [ ] Z-axis travel for push-down click (~1–2mm)
- [ ] Options:
  - **Option A**: Hall-effect joystick module (analog X/Y + push) — simplest
  - **Option B**: Custom gimbal with hall sensors or potentiometers — more control
  - **Recommended**: Start with Option A (off-the-shelf analog joystick module like Alps RKJXV or similar)

### 1.3 — Body Shell
- [ ] Cylindrical body with concave profile (hourglass shape)
- [ ] Top plate with cutouts for 2 tactile switches (L/R buttons)
- [ ] Button caps/rockers for comfortable clicking
- [ ] Internal ribbing for strength
- [ ] Cable channel or USB-C port cutout at base

### 1.4 — Base
- [ ] Weighted base for stability (steel weight insert or thick walls)
- [ ] Anti-slip rubber pads on bottom
- [ ] Side button cutouts (2x, left and right)
- [ ] PCB mounting posts
- [ ] Bottom plate with screw access

### 1.5 — CAD Deliverables
- [ ] OpenSCAD parametric model (all dimensions as variables)
- [ ] Export STL files for each part
- [ ] Export STEP for PCB integration reference
- [ ] Print test fit parts on FDM (0.2mm layer, PLA/PETG)

**Parts list (printed):**
1. Base bottom plate
2. Base ring (with side button cutouts)
3. Body shell (concave cylinder)
4. Top cap (with button cutouts)
5. Button caps × 4 (2 top + 2 side)
6. Joystick coupler (connects joystick module to body)

---

## Phase 2: Electronics (PCB)

### 2.1 — Component Selection
- [ ] **MCU**: RP2040 (native USB HID, cheap, well-supported)
  - QFN-56 package, 2x ARM Cortex-M0+, 264KB SRAM
  - Native USB 1.1 with HID support
- [ ] **Joystick sensing** (pick one):
  - Option A: Off-the-shelf analog joystick module (2x potentiometer + push switch)
  - Option B: 2x Hall-effect sensors (SS49E or DRV5053) + magnets on gimbal
- [ ] **Buttons**: 4x Kailh micro switches or Omron tactile switches
  - 2x top (left/right click)
  - 2x side (forward/back)
- [ ] **Push-down detection**: Built into joystick module (Option A) or separate tactile switch under spring
- [ ] **USB-C connector**: USB 2.0 type-C receptacle (e.g., GCT USB4085)
- [ ] **Voltage**: 3.3V via LDO from USB 5V (AP2112K-3.3 or similar)
- [ ] **Decoupling**: Standard RP2040 caps (100nF × several, 1µF bulk)
- [ ] **Crystal**: 12MHz for RP2040
- [ ] **Flash**: W25Q16 (2MB SPI flash for RP2040 firmware)
- [ ] **Optional**: WS2812B RGB LED(s) for status/flair

### 2.2 — Schematic
- [ ] RP2040 minimal circuit (follow hardware design guide)
- [ ] USB-C with proper CC resistors (5.1kΩ to GND)
- [ ] ADC inputs for joystick X/Y (GP26–GP29)
- [ ] GPIO for 5 switches (4 buttons + push-down)
- [ ] BOOT and RESET buttons (for firmware flashing)
- [ ] Power LED
- [ ] ESD protection on USB lines (optional but good practice)

### 2.3 — PCB Layout
- [ ] Target board size: fits inside base (~80mm diameter circular or shaped)
- [ ] 2-layer PCB (keep cost low for JLCPCB)
- [ ] USB-C at edge for cable exit
- [ ] Joystick connector header or direct solder pads
- [ ] Mounting holes matching base posts
- [ ] KiCad project with proper DRC

### 2.4 — PCB Deliverables
- [ ] KiCad schematic (.kicad_sch)
- [ ] KiCad PCB layout (.kicad_pcb)
- [ ] Gerber files for fab
- [ ] BOM with LCSC/JLCPCB part numbers
- [ ] Pick-and-place file (if doing SMT assembly)

---

## Phase 3: Firmware

### 3.1 — Platform & Framework
- [ ] PlatformIO with Arduino framework (or TinyUSB directly)
- [ ] Target: RP2040
- [ ] USB HID composite device: Mouse + extra buttons

### 3.2 — Core Features
- [ ] **Joystick → Mouse movement**
  - Read ADC X/Y values
  - Deadzone calibration (center position)
  - Sensitivity curve (linear or acceleration)
  - Convert tilt angle to mouse delta
- [ ] **Button handling**
  - Software debouncing (5–10ms)
  - Top-left → Left click (HID button 1)
  - Top-right → Right click (HID button 2)
  - Push-down → Middle click or configurable (HID button 3)
  - Side-left → Back (HID button 4)
  - Side-right → Forward (HID button 5)
- [ ] **USB HID reporting**
  - Standard HID mouse descriptor
  - 1000Hz polling rate (1ms USB interval)
  - Report: buttons (5 bits) + X delta + Y delta

### 3.3 — Advanced Features (post-MVP)
- [ ] DPI/sensitivity switching (button combo or dedicated button)
- [ ] Adjustable deadzone via serial config
- [ ] Auto-calibration on startup (read center position)
- [ ] RGB LED control (if fitted)
- [ ] Scroll emulation (e.g., hold push-down + tilt Y = scroll)

### 3.4 — Firmware Deliverables
- [ ] PlatformIO project with clean structure
- [ ] `src/main.cpp` — entry point
- [ ] `src/joystick.h/cpp` — ADC reading, deadzone, scaling
- [ ] `src/buttons.h/cpp` — debouncing, state machine
- [ ] `src/usb_hid.h/cpp` — HID descriptor, report sending
- [ ] `platformio.ini` — RP2040 board config
- [ ] README with flashing instructions

---

## Phase 4: Integration & Testing

- [ ] Print all case parts, test fit
- [ ] Solder PCB (or order assembled from JLCPCB)
- [ ] Flash firmware, verify USB enumeration
- [ ] Test each input (all 5 buttons + X/Y + push)
- [ ] Calibrate joystick center and sensitivity
- [ ] Assemble full unit
- [ ] Use it for a day — note ergonomic issues
- [ ] Iterate on case shape and button placement

---

## Bill of Materials (Estimated)

| Component | Qty | Est. Cost |
|---|---|---|
| RP2040 (QFN) | 1 | $0.70 |
| W25Q16 SPI Flash | 1 | $0.30 |
| 12MHz Crystal | 1 | $0.15 |
| USB-C Connector | 1 | $0.30 |
| AP2112K-3.3 LDO | 1 | $0.20 |
| Analog Joystick Module | 1 | $1.50–3.00 |
| Tactile Switches (Kailh/Omron) | 4 | $2.00 |
| Passive components (caps, resistors) | ~15 | $0.50 |
| PCB fab (5 pcs) | — | $5.00 |
| 3D printing filament | — | $2.00 |
| USB-C cable | 1 | $2.00 |
| **Total (est.)** | | **~$15–17** |

---

## Development Order

```
Week 1-2:  Phase 1.1–1.2  →  Nail down the joystick mechanism
Week 2-3:  Phase 1.3–1.5  →  Full CAD model, print prototypes
Week 3-4:  Phase 2.1–2.4  →  Schematic + PCB layout
Week 4-5:  Phase 3.1–3.4  →  Firmware (can start in parallel with PCB fab)
Week 5-6:  Phase 4         →  Assemble, test, iterate
```

---

## Open Questions

1. **Wired or wireless?** — Plan assumes wired USB-C. Wireless adds battery, charging circuit, and BLE/2.4GHz radio (ESP32-S3 would be better MCU for wireless).
2. **Joystick module vs custom gimbal?** — Off-the-shelf module is faster to prototype; custom gimbal gives better feel but needs more mechanical design.
3. **Scroll wheel?** — Not in current spec. Could add scroll via tilt-while-pushed or a thumb wheel on the side.
4. **Weighted base?** — Steel slugs or pennies in the base? How heavy should it feel?
5. **Grip surface?** — Bare plastic, or add rubber/silicone grip to the concave sides?
