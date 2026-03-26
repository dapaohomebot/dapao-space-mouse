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

## File Structure

```
case/
├── space_mouse.scad        ← Master assembly file (open this in OpenSCAD)
├── export_stls.sh          ← Batch export all parts to STL
├── ASSEMBLY_GUIDE.md       ← Step-by-step build guide
├── README.md               ← This file
├── parts/                  ← Individual part files (open to export single STLs)
│   ├── params.scad         ← Shared parameters, helper functions & utilities
│   ├── base_plate.scad     ← Part 1: Bottom plate
│   ├── base_ring.scad      ← Part 2: Base shell (USB-C, PCB mounts)
│   ├── body_shell.scad     ← Part 3: Concave body with side button cutouts
│   ├── top_frame.scad      ← Part 4: Top frame ring + divider
│   ├── button_top_left.scad  ← Part 5: Left rocker button
│   ├── button_top_right.scad ← Part 6: Right rocker button
│   ├── button_side.scad    ← Part 7: Side button caps (print 2)
│   └── joystick_coupler.scad ← Part 8: Joystick coupler
└── stl/                    ← Exported STL files (after running export_stls.sh)
```

## Parts List (8 printed parts)

| # | Part | Qty | Description |
|---|------|-----|-------------|
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

### Export Individual Parts
Open any file in `parts/` directly in OpenSCAD — each renders its own part automatically. Press **F6** to render, then **File → Export → Export as STL**.

### Batch Export All Parts
```bash
chmod +x export_stls.sh
./export_stls.sh
```

### Key Parameters to Customize
All parameters live in `parts/params.scad`. Change them there and all parts update automatically.

| Parameter | Default | What it does |
|-----------|---------|--------------|
| `body_od_top/bottom` | 60mm | Body diameter at edges |
| `body_od_waist` | 44mm | Narrowest point of concave |
| `body_height` | 55mm | Body shell height |
| `base_od` | 100mm | Base diameter |
| `top_frame_divider` | 2mm | Gap between L/R buttons |
| `top_btn_dome` | 2mm | How much buttons dome above frame |
| `side_btn_z_frac` | 0.78 | Side button position (0=bottom, 1=top of body) |
| `side_btn_width/height` | 14×10mm | Side button cutout size |

## Print Settings

| Setting | Value |
|---------|-------|
| Layer height | 0.2mm |
| Infill | 20% |
| Walls | 3 perimeters |
| Material | PLA or PETG |
| Supports | Minimal (base_ring USB-C overhang, body side button overhangs) |

### Part-Specific Print Notes

- **base_plate** — Print flat, pockets face down
- **base_ring** — Print upright, supports for USB-C overhang
- **body_shell** — Print upright, supports for side button cutouts
- **top_frame** — Print upside down (flat ring on bed)
- **button_top_left/right** — Print dome-side down. The hinge tab is thin (~1mm) — this is intentional as a living hinge for the rocker action
- **button_side** — Print 2 copies, flat side on bed
- **joystick_coupler** — Print upright, flange on top

See [ASSEMBLY_GUIDE.md](ASSEMBLY_GUIDE.md) for full step-by-step build instructions.
