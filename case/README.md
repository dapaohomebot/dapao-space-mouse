# DaPao Space Mouse — 3D Printed Case

## Files

| File | Description |
|---|---|
| `space_mouse.scad` | Main parametric OpenSCAD model |
| `export_stls.sh` | Batch export all parts to STL |
| `stl/` | Exported STL files (after running export) |

## Parts Overview

```
    ┌──────────────┐
    │   Top Cap    │  ← Part 4: top_cap (with button cutouts)
    │  [L]   [R]   │  ← Parts 5a/5b: button_top_left/right
    ├──────────────┤
   ╱ ╲            ╱╲
  │   ╲__________╱  │  ← Part 3: body (concave shell)
  │                  │
   ╲ ╱──────────╲ ╱
    ├──[coupler]──┤  ← Part 6: joystick_coupler
    │              │
[◄] │  Base Ring   │ [►]  ← Part 2: base_ring (+ side buttons)
    │              │
    └──────────────┘
    ┌──────────────┐
    │  Base Plate  │  ← Part 1: base_plate (with steel pockets)
    └──────────────┘
```

## How to Use

### Preview in OpenSCAD
1. Open `space_mouse.scad` in OpenSCAD
2. Set `RENDER_PART = "assembly"` to see full assembly
3. Set `EXPLODE = 15` to separate parts for inspection
4. Set `CROSS_SECTION = true` to see internal structure

### Export for Printing
Change `RENDER_PART` to each part name and export STL, or run:
```bash
chmod +x export_stls.sh
./export_stls.sh
```

### Customization
All dimensions are parametric variables at the top of the file:
- `base_od` — base diameter (default 100mm)
- `body_od_top/bottom` — body diameter at edges (default 60mm)
- `body_od_waist` — narrowest point of concave (default 44mm)
- `body_height` — body shell height (default 55mm)
- `steel_pocket_d/depth` — steel insert dimensions
- `tilt_clearance` — gap for joystick tilt freedom

## Print Settings

| Setting | Value |
|---|---|
| Layer height | 0.2mm |
| Infill | 20% |
| Walls | 3 perimeters |
| Material | PLA or PETG |
| Supports | Yes for base_ring (side button overhangs) |

### Part-Specific Notes

- **base_plate**: Print flat (bottom down). Steel pockets face down.
- **base_ring**: Print upright. Needs supports for USB-C and side button overhangs.
- **body**: Print upright (narrow waist up or down). No supports needed — concave walls are self-supporting at ~60° from vertical.
- **top_cap**: Print upside down (flat top on bed). Button cutouts need no support.
- **button caps**: Print flat. Small parts — print several at once.
- **joystick_coupler**: Print upright. Flange on top.

## Assembly Order

1. Insert steel washers into base plate pockets
2. Mount PCB to base ring standoffs (M2 screws)
3. Plug joystick module into PCB
4. Attach joystick coupler to joystick stick (set screw)
5. Place body shell over coupler (coupler flange seats into body bottom)
6. Insert tactile switches into top cap mounts
7. Press-fit top cap into body shell top
8. Insert side button caps into base ring
9. Insert top button caps into top cap
10. Screw base plate to base ring (4x M2)
11. Stick rubber feet on bottom
