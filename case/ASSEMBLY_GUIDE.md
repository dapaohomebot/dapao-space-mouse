# DaPao Space Mouse — Assembly Guide

A step-by-step guide for building and assembling the 3D printed space mouse.

---

## Parts List

### 3D Printed Parts (print all in PLA or PETG)

| # | File | Qty | Description |
|---|------|-----|-------------|
| 1 | `parts/base_plate.scad` | 1 | Bottom plate — steel insert pockets, rubber foot recesses |
| 2 | `parts/base_ring.scad` | 1 | Base shell — PCB mounts, USB-C port, power switch cutout |
| 3 | `parts/body_shell.scad` | 1 | Concave hourglass body with side button cutouts |
| 4 | `parts/top_frame.scad` | 1 | Ring + center divider holding the L/R buttons |
| 5 | `parts/button_top_left.scad` | 1 | Left half-circle rocker button |
| 6 | `parts/button_top_right.scad` | 1 | Right half-circle rocker button |
| 7 | `parts/button_side.scad` | 2 | Side button caps (back + forward) |
| 8 | `parts/joystick_coupler.scad` | 1 | Connects joystick stick to body shell |

### Hardware

| Item | Qty | Notes |
|------|-----|-------|
| M2 × 8mm screws | 8 | 4 for base plate, 4 for PCB |
| M2 nuts | 4 | For PCB standoffs |
| Seeed XIAO ESP32-S3 | 1 | Main MCU |
| Analog joystick module (25×25mm) | 1 | Standard 5-pin thumbstick |
| Tactile switches (6mm) | 4 | 2 for top buttons, 2 for side buttons |
| Steel washers (22mm OD) | 4 | For weight — press-fit into base plate pockets |
| Self-adhesive rubber feet (10mm) | 4 | Stick under base plate |
| LiPo battery (fits base ring cavity) | 1 | ~300–500mAh recommended |
| Power switch (7×4mm slide/rocker) | 1 | Fits cutout in base ring |
| USB-C breakout (if not using XIAO directly) | 1 | Optional |
| M2 × 3mm set screw | 1 | For joystick coupler |

---

## Print Settings

| Setting | Value |
|---------|-------|
| Layer height | 0.2mm |
| Infill | 20% |
| Walls | 3 perimeters |
| Material | PLA or PETG |

### Part-Specific Notes

| Part | Orientation | Supports |
|------|-------------|----------|
| `base_plate` | Flat side down | None |
| `base_ring` | Upright | Yes — USB-C overhang |
| `body_shell` | Upright | Yes — side button cutout overhangs |
| `top_frame` | Upside down (flat ring on bed) | None |
| `button_top_left` | Dome-side down | None |
| `button_top_right` | Dome-side down | None |
| `button_side` | Flat side on bed | None |
| `joystick_coupler` | Upright, flange on top | None |

> **Tip:** The hinge tabs on the top buttons are intentionally thin (~1mm). This is a **living hinge** — it flexes to give the rocker action. Don't try to thicken them.

---

## Assembly Steps

### Step 1 — Prepare the Base Plate
Press the 4 steel washers into the pockets on the underside of the **base plate**. They should be a firm press-fit. These add weight and keep the mouse stable during use.

### Step 2 — Mount the PCB
Seat the **XIAO ESP32-S3** (and any breakout boards) onto the **base ring** standoffs. Secure with M2 screws and nuts. Connect the joystick module wiring and tactile switch leads at this stage — it's much easier before everything is assembled.

### Step 3 — Install the Joystick Module
Place the joystick module on its mounting pad inside the base ring. The joystick stick should protrude upward through the center clearance hole. Secure if needed with a dab of hot glue or M2 screws.

### Step 4 — Install Power Switch & Battery
Slide the power switch into its cutout on the base ring wall. Tuck the LiPo battery into the battery compartment cavity. Connect the battery to the PCB via the power switch.

### Step 5 — Attach Base Plate to Base Ring
Align the base plate with the base ring (4 screw holes at 45°). Fasten with 4× M2 × 8mm screws. Stick the 4 rubber feet onto the base plate underside.

### Step 6 — Attach the Joystick Coupler
Slide the **joystick coupler** down over the joystick stick. The flange sits at the top. Tighten the M2 set screw in the side of the coupler to lock it to the joystick stick at your preferred height.

### Step 7 — Place the Body Shell
Lower the **body shell** down over the coupler. The coupler flange should seat into the internal mounting ring at the bottom of the body. The body should sit firmly on top of the base ring.

### Step 8 — Mount Tactile Switches in Top Frame
Press the two tactile switches onto the switch mount posts on the underside of the **top frame** (front of each half, one per button). Secure with M2 screws through the post holes if needed.

### Step 9 — Snap Top Frame onto Body
Press the **top frame** down into the top of the body shell. The insertion lip press-fits into the body's top socket. It should click in snugly.

### Step 10 — Install Top Buttons
Place the left and right **half-circle rocker buttons** into the top frame. The hinge tabs go at the back (away from you when using the mouse). The plunger nubs should sit above the tactile switches.

### Step 11 — Install Side Button Caps
Press the two **side button caps** into the cutouts on the body shell — one on each side. The retention clips on the edges hold them in place. The inner nub should make contact with the tactile switch mounted inside the body.

---

## Wiring Overview

```
XIAO ESP32-S3
├── GPIO 1,2,3 → Joystick (X, Y, SW)
├── GPIO 4 → Top button Left
├── GPIO 5 → Top button Right
├── GPIO 6 → Side button Left (Back)
├── GPIO 7 → Side button Right (Forward)
└── Battery → via slide power switch
```

> Refer to `hardware/DESIGN.md` for full schematic details and PCB layout.

---

## Troubleshooting

**Body doesn't sit flush on base ring**
→ Check that the coupler flange isn't too thick — it should seat fully inside the body's bottom mounting ring. Adjust coupler height with the set screw.

**Top frame pops off**
→ The lip press-fit may need a drop of CA glue if your printer tolerance is loose. Or adjust `tol` in `params.scad` and reprint.

**Side buttons feel loose**
→ The retention clips may need slight adjustment. Increase `side_btn_height` by 0.2mm and reprint the caps.

**Top button doesn't spring back**
→ The living hinge may be too thin for your filament. Try PETG instead of PLA for more flex.

**Mouse tips over**
→ Add more steel washers or use heavier inserts. You can also increase `steel_pocket_depth` in `params.scad`.
