# DaPao Space Mouse — Development Plan

## Concept

A wireless joystick-style mouse with a cylindrical "space mouse" body:

```
        ┌─────────────┐
        │  [L]   [R]  │  ← Top: Left/Right mouse buttons
        │             │
        ├─────────────┤
       / ╲           ╱ \
      │   ╲_________╱   │  ← Concave cylindrical body (bare plastic)
      │                  │     Tilts X/Y for cursor movement
       \ ╱─────────╲  /     Push down + tilt Y = scroll
        ├───────────┤
   [◄]  │           │  [►]  ← Side buttons: Back / Forward
        │  (BASE)   │
        │ ⊕ steel ⊕ │  ← Weighted base (steel inserts)
        └───────────┘
              ↓
        Push down = click
```

## Design Decisions

| Decision | Choice |
|---|---|
| Connectivity | **Wireless** (BLE via ESP32-S3) + USB-C for charging |
| Joystick | **Off-the-shelf** analog joystick module (Alps RKJXV or similar) |
| Scroll | **Tilt-while-pushed** (hold push-down + tilt Y = scroll) |
| Base weight | **Steel inserts** in base cavity for stability |
| Grip | **Bare plastic** (no rubber/silicone overlay) |

**Input mapping:**
| Input | Action |
|---|---|
| Tilt X/Y | Mouse cursor movement |
| Push down (Z-axis) | Middle click / modifier for scroll |
| Push down + Tilt Y | Scroll up/down |
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
- [ ] Choose assembly method: snap-fit clips + 2–4 M2 screws

### 1.2 — Joystick Mechanism
- [ ] Mount off-the-shelf analog joystick module (Alps RKJXV or similar) to PCB/base
- [ ] Design coupler: rigid connection from joystick stick to body shell
- [ ] Spring-return centering is built into the module
- [ ] Z-axis push-down click is built into the module (push switch)
- [ ] Verify travel range matches body tilt geometry

### 1.3 — Body Shell
- [ ] Cylindrical body with concave profile (hourglass shape)
- [ ] Bare plastic surface — optimize wall thickness for comfortable grip (2–3mm)
- [ ] Top plate with cutouts for 2 tactile switches (L/R buttons)
- [ ] Button caps for comfortable clicking
- [ ] Internal ribbing for strength
- [ ] Joystick coupler socket at bottom of body

### 1.4 — Base
- [ ] Weighted base with **steel insert cavities** (2–4 pockets for steel slugs/washers)
  - Target added weight: 50–80g of steel
  - Pockets sized for standard steel washers (M8–M10) or cut steel rod
- [ ] Anti-slip rubber pads on bottom (4x adhesive feet)
- [ ] Side button cutouts (2x, left and right of base ring)
- [ ] PCB mounting posts (4x M2 standoffs)
- [ ] Battery compartment (below PCB or beside it)
- [ ] USB-C port cutout at back of base (for charging)
- [ ] Bottom plate with screw access
- [ ] Power switch cutout (slide switch)

### 1.5 — CAD Deliverables
- [ ] OpenSCAD parametric model (all dimensions as variables)
- [ ] Export STL files for each part
- [ ] Export STEP for PCB integration reference
- [ ] Print test fit parts on FDM (0.2mm layer, PLA/PETG)

**Parts list (printed):**
1. Base bottom plate (with steel insert pockets)
2. Base ring (with side button cutouts + USB-C port)
3. Body shell (concave cylinder, bare plastic)
4. Top cap (with L/R button cutouts)
5. Button caps × 4 (2 top + 2 side)
6. Joystick coupler (connects joystick module shaft to body shell)
7. Battery holder/bracket

---

## Phase 2: Electronics (PCB)

### 2.1 — Component Selection
- [ ] **MCU**: ESP32-S3 (native USB + BLE 5.0)
  - ESP32-S3-WROOM-1 module (integrated antenna, flash, PSRAM)
  - Or ESP32-S3-MINI-1 for smaller footprint
  - BLE HID for wireless mouse
  - USB HID fallback when plugged in (wired mode)
- [ ] **Joystick**: Off-the-shelf analog module
  - 2x potentiometer (X/Y) → ESP32-S3 ADC
  - 1x push switch (Z-axis) → GPIO
  - 5-pin header: VCC, GND, X, Y, SW
- [ ] **Buttons**: 4x Kailh micro switches or Omron B3U tactile
  - 2x top (left/right click)
  - 2x side (forward/back)
- [ ] **Battery**: LiPo single cell 3.7V
  - 500–800mAh (fits in base, weeks of battery life at BLE power)
  - JST-PH 2-pin connector
- [ ] **Charging IC**: TP4056 or MCP73831
  - USB-C input → LiPo charging
  - Charge status LED (red=charging, green=full)
- [ ] **Voltage regulation**: 3.3V LDO (AP2112K-3.3 or ME6211)
  - Input from LiPo (3.0–4.2V) or USB 5V
- [ ] **Power switch**: Slide switch (SPDT) between battery and LDO
- [ ] **USB-C connector**: USB 2.0 type-C (charging + wired data fallback)
- [ ] **ESD protection**: USBLC6-2SC6 on USB lines
- [ ] **Decoupling**: Per ESP32-S3 design guide
- [ ] **Optional**: WS2812B RGB LED for status/pairing indication

### 2.2 — Schematic
- [ ] ESP32-S3 module circuit (WROOM-1 reference design)
- [ ] USB-C with CC resistors (5.1kΩ) + data lines to ESP32-S3 USB
- [ ] LiPo charging circuit (TP4056/MCP73831 + protection)
- [ ] Power path: USB 5V → charger → LiPo → LDO → 3.3V
- [ ] ADC inputs for joystick X/Y (GPIO1–GPIO10 range)
- [ ] GPIO for 5 switches (4 buttons + push-down) with pull-ups
- [ ] BOOT and RESET buttons (for firmware flashing)
- [ ] Power switch in battery path
- [ ] Battery voltage divider for fuel gauge (ADC pin)
- [ ] Charge status LED
- [ ] Power LED

### 2.3 — PCB Layout
- [ ] Target board size: fits inside base (~70×70mm or circular)
- [ ] 2-layer PCB (JLCPCB compatible)
- [ ] Keep antenna area clear (no ground/traces under ESP32-S3 antenna)
- [ ] USB-C at edge for charging port
- [ ] Joystick module header centered
- [ ] Battery connector at edge
- [ ] Mounting holes matching base posts (4x M2)
- [ ] KiCad project with proper DRC + antenna keepout

### 2.4 — PCB Deliverables
- [ ] KiCad schematic (.kicad_sch)
- [ ] KiCad PCB layout (.kicad_pcb)
- [ ] Gerber files for fab
- [ ] BOM with LCSC/JLCPCB part numbers
- [ ] Pick-and-place file (for SMT assembly)

---

## Phase 3: Firmware

### 3.1 — Platform & Framework
- [ ] PlatformIO with Arduino framework
- [ ] Target: ESP32-S3
- [ ] BLE HID mouse (primary mode)
- [ ] USB HID mouse (fallback when plugged in)
- [ ] Libraries: ESP32-BLE-Mouse or NimBLE + custom HID

### 3.2 — Core Features
- [ ] **Joystick → Mouse movement**
  - Read ADC X/Y values
  - Auto-calibration on startup (sample center position)
  - Configurable deadzone (~5–10% of range)
  - Sensitivity curve (linear with optional acceleration)
  - Convert tilt magnitude to mouse delta (larger tilt = faster cursor)
- [ ] **Scroll emulation (tilt-while-pushed)**
  - Detect push-down held
  - While pushed: tilt Y → scroll delta (instead of cursor Y)
  - Tilt X still moves cursor X (or disabled during scroll — TBD)
  - Scroll speed scaling (slower than cursor for precision)
- [ ] **Button handling**
  - Software debouncing (5–10ms)
  - Top-left → Left click (HID button 1)
  - Top-right → Right click (HID button 2)
  - Push-down tap → Middle click (HID button 3)
  - Push-down hold → scroll mode modifier
  - Side-left → Back (HID button 4)
  - Side-right → Forward (HID button 5)
- [ ] **BLE HID reporting**
  - BLE HID mouse profile
  - ~125Hz report rate (8ms BLE interval — good balance of latency vs power)
  - Report: buttons (5 bits) + X delta + Y delta + scroll delta
- [ ] **Power management**
  - Deep sleep after N minutes of inactivity
  - Wake on any button press or joystick movement
  - Battery voltage monitoring via ADC
  - Low battery warning (blink LED)

### 3.3 — Advanced Features (post-MVP)
- [ ] DPI/sensitivity switching (button combo: e.g., hold both side buttons)
- [ ] BLE pairing management (pair button combo)
- [ ] USB HID mode when cable detected (auto-switch)
- [ ] Adjustable deadzone/sensitivity via USB serial config tool
- [ ] Battery percentage reporting via BLE battery service
- [ ] RGB LED effects for status (pairing, low battery, charging)
- [ ] OTA firmware update via ESP32-S3 web server

### 3.4 — Firmware Deliverables
- [ ] PlatformIO project with clean structure
- [ ] `src/main.cpp` — entry point, mode switching
- [ ] `src/joystick.h/cpp` — ADC reading, deadzone, scaling
- [ ] `src/buttons.h/cpp` — debouncing, state machine
- [ ] `src/hid_ble.h/cpp` — BLE HID mouse profile
- [ ] `src/hid_usb.h/cpp` — USB HID fallback
- [ ] `src/scroll.h/cpp` — scroll-while-pushed logic
- [ ] `src/power.h/cpp` — sleep, wake, battery monitoring
- [ ] `platformio.ini` — ESP32-S3 board config
- [ ] README with flashing + pairing instructions

---

## Phase 4: Integration & Testing

- [ ] Print all case parts, test fit
- [ ] Verify steel insert pockets fit standard washers
- [ ] Solder/order assembled PCB
- [ ] Flash firmware, verify BLE pairing
- [ ] Test each input (all 5 buttons + X/Y + push + scroll)
- [ ] Calibrate joystick center and sensitivity
- [ ] Test charging circuit (charge time, status LEDs)
- [ ] Measure battery life (target: 1+ week typical use)
- [ ] Test USB fallback mode
- [ ] Assemble full unit with steel weights
- [ ] Use it for a day — note ergonomic issues
- [ ] Iterate on case shape, button placement, and firmware tuning

---

## Bill of Materials (Estimated)

| Component | Qty | Est. Cost |
|---|---|---|
| ESP32-S3-WROOM-1 Module | 1 | $2.50 |
| USB-C Connector | 1 | $0.30 |
| TP4056 / MCP73831 (Charging IC) | 1 | $0.30 |
| AP2112K-3.3 LDO | 1 | $0.20 |
| LiPo Battery 3.7V 500–800mAh | 1 | $3.00–5.00 |
| Analog Joystick Module | 1 | $1.50–3.00 |
| Tactile Switches (Kailh/Omron) | 4 | $2.00 |
| Slide Switch (power) | 1 | $0.10 |
| USBLC6-2SC6 (ESD) | 1 | $0.25 |
| Passive components (caps, resistors, LEDs) | ~20 | $1.00 |
| PCB fab (5 pcs, 2-layer) | — | $5.00 |
| 3D printing filament (~50g) | — | $2.00 |
| Steel washers/inserts (base weight) | 4–6 | $1.00 |
| Rubber feet (adhesive) | 4 | $0.50 |
| M2 Screws + standoffs | 6 | $0.50 |
| **Total (est.)** | | **~$20–24** |

---

## Development Order

```
Week 1-2:  Phase 1.1–1.2  →  Joystick mechanism + coupler design
Week 2-3:  Phase 1.3–1.5  →  Full CAD model, print prototypes
Week 3-4:  Phase 2.1–2.4  →  Schematic + PCB layout (order PCB + parts)
Week 4-5:  Phase 3.1–3.2  →  Core firmware (BLE HID + joystick + buttons)
Week 5-6:  Phase 3.3–3.4  →  Scroll, power management, polish
Week 6-7:  Phase 4         →  Assemble, test, iterate
```

*Firmware dev can start on an ESP32-S3 dev board + breadboard joystick in Week 3 while waiting for PCBs.*

---

## Design Decisions Log

| # | Decision | Rationale |
|---|---|---|
| 1 | Wireless (BLE) via ESP32-S3 | Clean desk, no cable drag. USB-C for charging + wired fallback. |
| 2 | Off-the-shelf joystick module | Faster prototyping, proven mechanism, built-in centering spring + push switch. |
| 3 | Scroll = tilt-while-pushed | No extra hardware needed. Push-down becomes dual-purpose (tap=click, hold+tilt=scroll). |
| 4 | Steel inserts in base | Stability without making the whole base massive. Adjustable weight. |
| 5 | Bare plastic grip | Simpler manufacturing. Concave shape provides natural grip. Can add texture in slicer. |
