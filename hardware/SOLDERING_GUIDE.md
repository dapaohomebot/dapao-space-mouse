# DaPao Space Mouse — Soldering & PCB Assembly Guide

Complete step-by-step instructions for assembling both PCBs from bare boards.

---

## Tools Required

| Tool | Notes |
|------|-------|
| Soldering iron | Fine tip, temperature-controlled (320–360°C) |
| Solder | 0.5–0.6mm diameter, 63/37 or 60/40 tin/lead (or lead-free SAC305) |
| Flux pen | No-clean rosin flux, essential for SMD work |
| Tweezers | Fine-tip for SMD components |
| Solder wick + pump | For fixing bridges |
| Multimeter | Continuity and voltage checks |
| Magnifier / loupe | SMD pads are small |
| IPA + cotton swabs | Flux cleanup |
| PCB holder / helping hands | Keeps board still while soldering |

---

## Bill of Materials (Both Boards)

### Lower PCB (dia88mm circular)

| Ref | Component | Package | Qty | Notes |
|-----|-----------|---------|-----|-------|
| U1 | Seeed XIAO ESP32-S3 | Module with castellation | 1 | Main MCU + BLE + USB |
| U2 | TP4056 | SOP-8 | 1 | LiPo charge controller |
| U3 | AP2112K-3.3V | SOT-23-5 | 1 | 3.3V LDO regulator |
| U4 | USBLC6-2SC6 | SOT-23-6 | 1 | USB ESD protection |
| J1 | USB-C receptacle (mid-mount) | Through-hole+SMD | 1 | Align with base ring cutout |
| J2 | JST-PH 2-pin (right-angle) | Through-hole | 1 | Battery connector |
| J3 | FPC connector 6-pin 0.5mm pitch | SMD top-contact | 1 | Cable to upper PCB |
| J4 | 5-pin header 2.54mm (right-angle) | Through-hole | 1 | Joystick module |
| SW1 | SPDT slide switch (MSK-12C02) | SMD | 1 | Power switch, aligns with base ring cutout |
| SW2 | Tactile switch 3x4mm | SMD | 1 | BOOT button |
| SW3 | Tactile switch 3x4mm | SMD | 1 | RESET button |
| R1–R5 | 10kΩ resistor | 0402 | 5 | Pull-ups for buttons + joystick SW |
| R6, R7 | 100kΩ resistor | 0402 | 2 | Battery voltage divider |
| R8 | 2kΩ resistor | 0402 | 1 | TP4056 charge current (500mA) |
| R9, R10 | 1kΩ resistor | 0402 | 2 | Charge/standby LED current limit |
| R11, R12 | 5.1kΩ resistor | 0402 | 2 | USB-C CC lines |
| C1–C4 | 100nF ceramic | 0402 | 4 | 3V3 decoupling near U1 |
| C5 | 10µF ceramic | 0805 | 1 | 3V3 bulk cap |
| C6 | 10µF ceramic | 0805 | 1 | VBUS bulk cap |
| C7 | 10µF ceramic | 0805 | 1 | BAT+ bulk cap |
| LED1 | Red LED | 0402 | 1 | Charge indicator |
| LED2 | Green LED | 0402 | 1 | Standby/charged indicator |
| H1–H4 | M2 brass standoff (5mm) | Through-hole | 4 | PCB mount posts |

### Upper PCB (dia54mm circular)

| Ref | Component | Package | Qty | Notes |
|-----|-----------|---------|-----|-------|
| SW4 | Kailh micro switch (6x6mm upright) | Through-hole | 1 | Left click — plunger faces UP |
| SW5 | Kailh micro switch (6x6mm upright) | Through-hole | 1 | Right click — plunger faces UP |
| SW6 | Kailh micro switch (6x6mm side-mount) | Through-hole | 1 | Back — plunger faces LEFT (outward) |
| SW7 | Kailh micro switch (6x6mm side-mount) | Through-hole | 1 | Forward — plunger faces RIGHT (outward) |
| J5 | FPC connector 6-pin 0.5mm pitch | SMD top-contact | 1 | Cable to lower PCB |
| C1 | 100nF ceramic | 0402 | 1 | 3V3 decoupling |
| H1, H2 | M2 brass standoff (3mm) | Through-hole | 2 | Mount to top frame posts |

### FPC Cable

| Item | Spec | Qty |
|------|------|-----|
| FPC flat flex cable | 6-pin, 0.5mm pitch, same-side contacts, ~80mm length | 1 |

---

## Lower PCB Assembly

### Step 1 — Inspect the bare board

Check the board under magnification:
- No shorts on pads
- All drill holes clean
- Silkscreen orientation marks visible

### Step 2 — SMD resistors and capacitors first (0402)

Start with the smallest, flattest components. Work in this order:

**R11, R12 — USB-C CC pull-downs (5.1kΩ)**
> Near J1 (USB-C connector). Solder before the connector blocks access.
1. Apply flux to both pads
2. Tin one pad with a small amount of solder
3. Place resistor with tweezers, hold against tinned pad
4. Reflow the tinned pad to tack the component
5. Solder the other pad — touch iron + solder simultaneously, 2 seconds
6. Check: no bridges, both ends flush

**R8 — TP4056 PROG resistor (2kΩ)**
> Sets charge current to 500mA. Located near U2.

**R1–R5 — Button/joystick pull-ups (10kΩ each)**
> Near J3 FPC connector area.

**R6, R7 — Battery voltage divider (100kΩ each)**
> Near U1 analog input GPIO4.

**R9, R10 — LED current limit (1kΩ each)**
> Near LED1, LED2.

**C1–C4 — Decoupling caps (100nF, 0402)**
> Place one on each side of U1 footprint.

**C5, C6, C7 — Bulk caps (10µF, 0805)**
> Larger than 0402 — easier. One each on 3V3, VBUS, BAT+ rails.

**LED1 (Red), LED2 (Green)**
> Note polarity: cathode (K) mark on silkscreen is the shorter side.

### Step 3 — SMD ICs

**U4 — USBLC6-2SC6 (SOT-23-6)**
> USB ESD protection, next to J1. Pin 1 dot on silkscreen.
1. Apply flux
2. Tin pad 1
3. Place chip, align all pins
4. Tack pin 1
5. Solder remaining pins
6. Inspect under magnifier for bridges

**U3 — AP2112K-3.3V (SOT-23-5)**
> LDO regulator between battery and ESP32.
1. Same technique as U4
2. Pin 1 = EN (tie to VIN — check silkscreen)

**U2 — TP4056 (SOP-8)**
> LiPo charge controller. 8 pins, 1.27mm pitch.
1. Apply generous flux to all pads
2. Tin one corner pad
3. Align chip carefully (pin 1 dot matches silkscreen dot)
4. Tack corner pad
5. Solder remaining pins drag-style: load iron tip with solder, drag across pins in one smooth motion
6. Use wick to clean any bridges
7. Verify with continuity meter: no adjacent pin shorts

### Step 4 — SMD switches

**SW1 — Power slide switch**
> Must align with the cutout in the base ring wall. Dry-fit the PCB in the base ring before soldering to confirm alignment.
1. Check physical alignment with base ring first
2. Solder SMD pads on both sides of switch body

**SW2, SW3 — BOOT and RESET tactile switches**
> Near U1. Solder 4 pads each.

### Step 5 — FPC connector J3

> **Critical:** The FPC connector is the most delicate part. Work slowly.
1. Apply flux
2. Align connector on pads (notch matches silkscreen outline)
3. Tack two corner pads with minimal solder
4. Check alignment is perfect — very hard to correct after soldering all pins
5. Solder each pin: iron on pad, not pin, 1.5 seconds max per pin
6. Inspect every pin gap under magnifier

### Step 6 — Through-hole: J1 (USB-C)

> Mid-mount USB-C sits flush or slightly recessed in the board edge slot.
1. Insert from front, check alignment with base ring cutout
2. Tack one pin
3. Verify alignment again
4. Solder all pins from the back
5. Add flux and reflow top-side SMD pads if present

### Step 7 — Through-hole: J2 (JST battery), J4 (joystick header)

1. Insert from front
2. Tape in place if needed
3. Flip board, solder from back
4. Trim leads flush with flush cutters

### Step 8 — U1: XIAO ESP32-S3

> The XIAO is a castellated module — it solders directly to pads on your board.
1. Apply flux to all castellated pads on the board
2. Place XIAO module — USB-C end faces outward toward board edge
3. Check alignment: all castellations sitting on their pads
4. Tack two corner pads
5. Verify alignment — critical, no adjustment after all pads soldered
6. Solder all pads: touch iron to pad edge + castellation, 2 seconds each
7. Add flux and reflow if any joint looks cold (dull/grainy)
8. **Do not cover the antenna area** (unmarked keepout zone near the PCB edge of the module — no copper fills, no components within 3mm)

### Step 9 — First power test (before mounting)

> **Do this before installing in the case!**

1. Connect a LiPo battery to J2
2. **Do not connect USB yet**
3. Flip SW1 to ON
4. Measure 3V3 rail with multimeter: should read 3.25–3.35V
5. LED2 (green) should light — battery fully charged / standby
6. Connect USB-C — LED1 (red) lights if battery needs charging
7. Check with your phone/laptop: "XIAO ESP32S3" should appear in BLE scan after flashing firmware

---

## Upper PCB Assembly

### Step 1 — SMD first: C1 decoupling cap and FPC connector J5

**C1 (100nF 0402)**
> Near J5. Solder before J5 blocks access.

**J5 — FPC connector**
> Same technique as J3 on lower PCB. Most delicate part.
1. Flux, align, tack corners, verify, solder all pins

### Step 2 — SW4 and SW5 (upward-facing L/R click switches)

> These are standard 6x6mm through-hole tactile switches, plunger faces UP.
> They sit on the front (top) of the board.

1. Insert SW4 at position X=-10mm, Y=+12mm from board center (left quadrant, toward front)
2. Insert SW5 at position X=+10mm, Y=+12mm (right quadrant, toward front)
3. Both switches should be **upright** — plunger pointing away from board
4. Solder 4 pins each from the back
5. Trim leads

### Step 3 — SW6 and SW7 (side-facing Back/Forward switches)

> **Important:** These use side-mount switches. The plunger faces outward through the top_frame wall cutouts.

1. SW6: Insert at left board edge (X=-24mm), **rotate 90°** so plunger faces LEFT (outward)
2. SW7: Insert at right board edge (X=+24mm), **rotate 90°** so plunger faces RIGHT (outward)
3. Both switches sit at Y=0 (board centerline)
4. Test plunger clearance through the top_frame cutouts before soldering — dry-fit the board into the top_frame
5. Solder 4 pins each, trim leads

### Step 4 — Mounting holes H1, H2

> Install M2 brass standoffs (3mm) — these mate with the top_frame mount posts.
1. Insert standoffs from the back of the board
2. Secure with M2 nuts on the front side

### Step 5 — Upper PCB function test

1. Connect the 6-pin FPC cable to J5 (lift latch, insert cable shiny-side up, press latch down)
2. Connect other end to J3 on the lower PCB
3. Power on via SW1
4. Test each button: open serial monitor on XIAO, confirm GPIO signals trigger correctly

---

## FPC Cable Connection

The 6-pin FPC cable connects J3 (lower PCB) to J5 (upper PCB):

| Pin | Signal | Lower PCB J3 | Upper PCB J5 |
|-----|--------|-------------|-------------|
| 1 | 3V3 | Pin 1 | Pin 1 |
| 2 | GND | Pin 2 | Pin 2 |
| 3 | BTN_LEFT | Pin 3 | Pin 3 (SW4) |
| 4 | BTN_RIGHT | Pin 4 | Pin 4 (SW5) |
| 5 | BTN_BACK | Pin 5 | Pin 5 (SW6) |
| 6 | BTN_FWD | Pin 6 | Pin 6 (SW7) |

**Cable routing:** The FPC cable exits J3 upward, routes through the body shell interior, and enters J5 from below. Keep the cable loose enough that the body shell can be installed — don't route it too tight.

---

## Continuity Checks (Before Power-On)

Run these checks with a multimeter in continuity mode after soldering each board:

### Lower PCB
- [ ] VBUS to GND — should be **open** (no short)
- [ ] 3V3 to GND — should be **open**
- [ ] BAT+ to GND — should be **open**
- [ ] USB-C VBUS pin to J2 Pin1 — continuity through TP4056
- [ ] J4 Pin1 (3V3) to 3V3 rail — continuity
- [ ] J3 Pin1 to 3V3 rail — continuity
- [ ] SW1 COM to BAT+ — continuity (switch ON)

### Upper PCB
- [ ] 3V3 to GND — should be **open**
- [ ] J5 Pin2 to SW4/SW5/SW6/SW7 GND pins — continuity
- [ ] J5 Pin3 to SW4 signal pin — continuity
- [ ] J5 Pin4 to SW5 signal pin — continuity
- [ ] J5 Pin5 to SW6 signal pin — continuity
- [ ] J5 Pin6 to SW7 signal pin — continuity

---

## Common Soldering Problems

**Cold joint (dull/grainy appearance)**
> Reheat with iron + add a tiny amount of fresh solder + flux. A good joint is shiny and slightly concave.

**Solder bridge between SMD IC pins**
> Apply flux, drag solder wick over bridge, press with iron. The wick wicks away excess solder.

**FPC connector misaligned**
> If the connector is off more than ~0.1mm, desolder by flooding with flux + adding solder to all pins, then lift with iron. Clean pads with wick, start over.

**XIAO won't enumerate on USB after soldering**
> Check solder on USB-C pins and D+/D- lines to U4 (ESD protection). A cold joint on any of these will kill USB.

**Button registers continuously (stuck)**
> Check that the pull-up resistors are soldered correctly. Measure the BTN pin to 3V3 — should read ~3.3V when button not pressed, ~0V when pressed.

**Battery charges but 3V3 drops under load**
> Check U3 (LDO) solder joints. SOT-23-5 packages are prone to lifted pins if overheated.
