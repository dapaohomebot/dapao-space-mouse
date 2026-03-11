# DaPao Space Mouse — 3D Printed Case (v2)

## Button Layout

```
          ┌─────────────────────┐
         ╱   [LEFT]  │  [RIGHT]  ╲     ← Half-circle rocker buttons
        │    click    │   click    │       Hinged at back, click at front
         ╲           │           ╱        Like a traditional mouse
          └──────────┴──────────┘
          ┌─────────────────────┐
         ╱                       ╲
  [BACK]│    concave body shell    │[FWD]  ← Side buttons on body
         │                         │         Aligned below L/R buttons
         ╲                       ╱
          └─────────────────────┘
          ┌─────────────────────┐
          │       base ring      │
          │   (USB-C / switch)   │
          └─────────────────────┘
          ┌─────────────────────┐
          │     base plate       │   ← Steel inserts underneath
          └─────────────────────┘
```

## Files

| File | Description |
|---|---|
| `space_mouse.scad` | Main parametric OpenSCAD model (v2) |
| `export_stls.sh` | Batch export all parts to STL |
| `stl/` | Exported STL files (after running export) |

## Parts List (8 printed parts)

| # | Part | Qty | Description |
|---|---|---|---|
| 1 | `base_plate` | 1 | Bottom plate with steel insert pockets + rubber foot recesses |
| 2 | `base_ring` | 1 | Base shell: PCB mounts, USB-C port, power switch |
| 3 | `body` | 1 | Concave hourglass body with side button cutouts |
| 4 | `top_frame` | 1 | Ring + center divider that holds the two half-circle buttons |
| 5 | `button_top_left` | 1 | Left mouse button — half-circle rocker, hinged at back |
| 6 | `button_top_right` | 1 | Right mouse button — half-circle rocker, hinged at back |
| 7 | `button_side` | 2 | Side buttons (back + forward) — curved to match body |
| 8 | `joystick_coupler` | 1 | Connects joystick stick to body shell |

## How to Use

### Preview in OpenSCAD
1. Open `space_mouse.scad` in [OpenSCAD](https://openscad.org/downloads.html)
2. Set `RENDER_PART = "assembly"` → see full assembly
3. Set `EXPLODE = 15` → separate parts for inspection
4. Set `CROSS_SECTION = true` → see internal structure

### Export for Printing
```bash
chmod +x export_stls.sh
./export_stls.sh
```
Or manually: change `RENDER_PART` to each part name → F6 → Export STL.

### Key Parameters to Customize
| Parameter | Default | What it does |
|---|---|---|
| `body_od_top/bottom` | 60mm | Body diameter at edges |
| `body_od_waist` | 44mm | Narrowest point of concave |
| `body_height` | 55mm | Body shell height |
| `base_od` | 100mm | Base diameter |
| `top_frame_divider` | 2mm | Gap between L/R buttons |
| `top_btn_dome` | 2mm | How much buttons dome above frame |
| `side_btn_z_frac` | 0.55 | Side button position (0=bottom, 1=top of body) |
| `side_btn_width/height` | 14×10mm | Side button cutout size |

## Print Settings

| Setting | Value |
|---|---|
| Layer height | 0.2mm |
| Infill | 20% |
| Walls | 3 perimeters |
| Material | PLA or PETG |
| Supports | Minimal (body side button overhangs only) |

### Part-Specific Print Notes

- **base_plate** — Print flat, pockets face down
- **base_ring** — Print upright, supports for USB-C overhang
- **body** — Print upright, supports for side button cutouts
- **top_frame** — Print upside down (flat ring on bed)
- **button_top_left/right** — Print dome-side down. The hinge tab is thin (~1mm) — this is intentional as a living hinge for the rocker action
- **button_side** — Print 2 copies, flat side on bed
- **joystick_coupler** — Print upright, flange on top

## Assembly Order

1. Insert steel washers into base plate pockets
2. Mount PCB to base ring standoffs (M2 screws)
3. Plug joystick module into PCB
4. Screw base plate to base ring (4× M2)
5. Attach joystick coupler to joystick stick (set screw)
6. Place body shell over coupler (flange seats into body bottom ring)
7. Mount tactile switches to top frame switch posts
8. Snap top frame into body shell top (press-fit lip)
9. Place left and right half-circle buttons into top frame (hinge tabs at back)
10. Press side button caps into body cutouts (retention clips hold them)
11. Stick rubber feet on bottom

## Design Notes

### Top Buttons (Half-Circle Rockers)
The L/R buttons are two half-circles that together form a full circle on top.
They're separated by a center divider in the top frame. Each button:
- Pivots on a thin **living hinge** at the back edge
- Has a **plunger nub** underneath at the front that presses a tactile switch
- Is slightly **domed** for a comfortable click surface
- Clearance gap around edges prevents binding

### Side Buttons (Forward/Back)
Positioned on the concave body at 55% height (adjustable via `side_btn_z_frac`):
- **Left side** = Back (under left mouse button)
- **Right side** = Forward (under right mouse button)
- Curved outer face matches the body profile
- Retention clips on top/bottom edges hold the cap in the cutout
- Inner nub presses a tactile switch mounted inside the body
