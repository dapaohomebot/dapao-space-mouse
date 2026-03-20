#!/usr/bin/env python3
"""
Generate Gerber + drill files for DaPao Space Mouse PCBs.
Produces standard RS-274X Gerbers that JLCPCB / PCBWay accept.
Run from the hardware/ directory.
"""
import os, math

def circle_poly(cx, cy, r, n=72):
    pts = []
    for i in range(n):
        a = math.radians(360 * i / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def write_gerber(path, layers):
    """layers: list of (layer_name, commands_list)"""
    with open(path, 'w') as f:
        f.write("%FSLAX46Y46*%\n")        # format spec
        f.write("%MOMM*%\n")              # metric
        f.write("%LPD*%\n")              # polarity dark
        f.write("G04 DaPao Space Mouse Gerber*\n")
        for layer_name, cmds in layers:
            f.write(f"G04 Layer: {layer_name}*\n")
            for cmd in cmds:
                f.write(cmd + "\n")
        f.write("M02*\n")

def circle_gerber_cmds(cx, cy, r, n=120):
    """Return Gerber arc commands for a circle outline."""
    cmds = []
    # Use D01 (draw) with linear moves around the circle
    pts = circle_poly(cx, cy, r, n)
    # Define a small circular aperture for the outline
    cmds.append("%ADD10C,0.10*%")
    cmds.append("D10*")
    # Move to start
    x0, y0 = pts[0]
    cmds.append(f"X{int(x0*1e6):+010d}Y{int(y0*1e6):+010d}D02*")
    for x, y in pts[1:]:
        cmds.append(f"X{int(x*1e6):+010d}Y{int(y*1e6):+010d}D01*")
    # close
    cmds.append(f"X{int(x0*1e6):+010d}Y{int(y0*1e6):+010d}D01*")
    return cmds

def filled_circle_cmds(cx, cy, r, aperture=11, size=None):
    """Fill a circle using a round aperture."""
    cmds = []
    size = size or r * 2
    cmds.append(f"%ADD{aperture}C,{size:.4f}*%")
    cmds.append(f"D{aperture}*")
    cmds.append(f"X{int(cx*1e6):+010d}Y{int(cy*1e6):+010d}D03*")
    return cmds

def pad_cmds(cx, cy, w, h, aperture, net=""):
    cmds = []
    cmds.append(f"%ADD{aperture}R,{w:.3f}X{h:.3f}*%")
    cmds.append(f"D{aperture}*")
    cmds.append(f"X{int(cx*1e6):+010d}Y{int(cy*1e6):+010d}D03*")
    return cmds

def rect_cmds(cx, cy, w, h, aperture):
    return pad_cmds(cx, cy, w, h, aperture)

def write_drill(path, holes):
    """holes: list of (x, y, dia, plated)"""
    with open(path, 'w') as f:
        f.write("M48\n")
        f.write("METRIC,TZ\n")
        f.write("FMAT,2\n")
        # Group by diameter
        by_dia = {}
        for x, y, dia, plated in holes:
            by_dia.setdefault((dia, plated), []).append((x, y))
        tool = 1
        for (dia, plated), coords in by_dia.items():
            f.write(f"T{tool:02d}C{dia:.3f}\n")
            tool += 1
        f.write("%\n")
        f.write("G90\nG05\n")
        tool = 1
        for (dia, plated), coords in by_dia.items():
            f.write(f"T{tool:02d}\n")
            for x, y in coords:
                f.write(f"X{int(x*1e4):+08d}Y{int(y*1e4):+08d}\n")
            tool += 1
        f.write("T00\nM30\n")


# ============================================================
# LOWER PCB — dia88mm circular, center at (100,100) mm
# ============================================================
LOWER_OUT = os.path.join(os.path.dirname(__file__), "lower_pcb/gerbers")
os.makedirs(LOWER_OUT, exist_ok=True)

cx, cy = 100.0, 100.0
outer_r = 44.0   # 88mm diameter
inner_r = 13.5   # 27mm center cutout

# Edge.Cuts
edge_cmds = circle_gerber_cmds(cx, cy, outer_r) + circle_gerber_cmds(cx, cy, inner_r)
write_gerber(f"{LOWER_OUT}/lower_pcb-Edge_Cuts.gbr", [("Edge.Cuts", edge_cmds)])

# F.Cu — copper layer with component pads
fcu = []
fcu.append("G04 F.Cu — Lower PCB*")
fcu.append("%ADD10C,0.10*%")

# GND pour (simplified — large filled circle minus keepouts)
# We represent it as the board outline on copper
fcu += circle_gerber_cmds(cx, cy, outer_r - 0.3)

# Mounting holes (annular rings) — 4x M2 at 30mm radius
mh_aperture = 20
fcu.append(f"%ADD{mh_aperture}C,4.40*%")  # 4.4mm pad
fcu.append(f"D{mh_aperture}*")
for angle in [0, 90, 180, 270]:
    mx = cx + 30 * math.cos(math.radians(angle))
    my = cy + 30 * math.sin(math.radians(angle))
    fcu.append(f"X{int(mx*1e6):+010d}Y{int(my*1e6):+010d}D03*")
# remove drill hole (dark polarity already handled by drill file)

# XIAO ESP32-S3 castellation pads (~18 pads, 1.6mm pitch on long sides)
# Positioned at approx (118, 88) center
xiao_cx, xiao_cy = 118.0, 90.0
xiao_w, xiao_h = 17.5, 21.0
apt = 30
fcu.append(f"%ADD{apt}R,1.50X2.00*%")
fcu.append(f"D{apt}*")
for i in range(7):  # left side
    fcu.append(f"X{int((xiao_cx - xiao_w/2)*1e6):+010d}Y{int((xiao_cy - 9 + i*3)*1e6):+010d}D03*")
for i in range(7):  # right side
    fcu.append(f"X{int((xiao_cx + xiao_w/2)*1e6):+010d}Y{int((xiao_cy - 9 + i*3)*1e6):+010d}D03*")

# USB-C connector pads at board edge (aligned with base ring cutout at 0° = right)
usbc_x, usbc_y = 144.0, 100.0
apt = 31
fcu.append(f"%ADD{apt}R,0.80X1.60*%")
fcu.append(f"D{apt}*")
for i in range(6):
    fcu.append(f"X{int((usbc_x - 1)*1e6):+010d}Y{int((usbc_y - 2.5 + i)*1e6):+010d}D03*")

# JST battery connector J2
jst_x, jst_y = 82.0, 110.0
apt = 32
fcu.append(f"%ADD{apt}C,1.80*%")
fcu.append(f"D{apt}*")
fcu.append(f"X{int((jst_x-1)*1e6):+010d}Y{int(jst_y*1e6):+010d}D03*")
fcu.append(f"X{int((jst_x+1)*1e6):+010d}Y{int(jst_y*1e6):+010d}D03*")

# FPC connector J3 (6-pin, 0.5mm pitch)
fpc_x, fpc_y = 100.0, 85.0
apt = 33
fcu.append(f"%ADD{apt}R,0.40X1.20*%")
fcu.append(f"D{apt}*")
for i in range(6):
    fcu.append(f"X{int((fpc_x - 1.25 + i*0.5)*1e6):+010d}Y{int(fpc_y*1e6):+010d}D03*")

# TP4056 U2 pads (SOP-8)
u2x, u2y = 135.0, 95.0
apt = 34
fcu.append(f"%ADD{apt}R,0.60X1.60*%")
fcu.append(f"D{apt}*")
for i in range(4):
    fcu.append(f"X{int((u2x - 1.905)*1e6):+010d}Y{int((u2y - 2.1 + i*1.27 + 0.635)*1e6):+010d}D03*")
    fcu.append(f"X{int((u2x + 1.905)*1e6):+010d}Y{int((u2y - 2.1 + i*1.27 + 0.635)*1e6):+010d}D03*")

write_gerber(f"{LOWER_OUT}/lower_pcb-F_Cu.gbr", [("F.Cu", fcu)])

# B.Cu — ground plane (simplified as filled board area)
bcu = circle_gerber_cmds(cx, cy, outer_r - 0.3)
write_gerber(f"{LOWER_OUT}/lower_pcb-B_Cu.gbr", [("B.Cu", bcu)])

# F.SilkS
silk = []
silk.append("%ADD10C,0.15*%")
silk.append("D10*")
# Board labels
for text_pos, label in [
    ((118, 85), "U1-XIAO"),
    ((135, 90), "U2-TP4056"),
    ((112, 105), "U3-LDO"),
    ((100, 85), "J3-FPC"),
    ((82, 112), "J2-BAT"),
    ((144, 97), "J1-USB"),
    ((56, 100), "SW1-PWR"),
    ((100, 100), "CENTER-CUT"),
]:
    # Just mark position with cross
    tx, ty = text_pos
    silk.append(f"X{int((tx-1)*1e6):+010d}Y{int(ty*1e6):+010d}D02*")
    silk.append(f"X{int((tx+1)*1e6):+010d}Y{int(ty*1e6):+010d}D01*")
    silk.append(f"X{int(tx*1e6):+010d}Y{int((ty-1)*1e6):+010d}D02*")
    silk.append(f"X{int(tx*1e6):+010d}Y{int((ty+1)*1e6):+010d}D01*")
write_gerber(f"{LOWER_OUT}/lower_pcb-F_SilkS.gbr", [("F.SilkS", silk)])

# F.Mask (expose pads — same positions as F.Cu pads)
write_gerber(f"{LOWER_OUT}/lower_pcb-F_Mask.gbr", [("F.Mask", fcu)])
write_gerber(f"{LOWER_OUT}/lower_pcb-B_Mask.gbr", [("B.Mask", bcu)])

# Drill file
lower_holes = []
# Mounting holes M2 (2.2mm drill)
for angle in [0, 90, 180, 270]:
    mx = cx + 30 * math.cos(math.radians(angle))
    my = cy + 30 * math.sin(math.radians(angle))
    lower_holes.append((mx, my, 2.2, True))
# USB-C mechanical pins
lower_holes += [(usbc_x, usbc_y - 2, 0.8, True), (usbc_x, usbc_y + 2, 0.8, True)]
# JST 2-pin
lower_holes += [(jst_x - 1, jst_y, 0.8, True), (jst_x + 1, jst_y, 0.8, True)]
# Joystick 5-pin header
for i in range(5):
    lower_holes.append((cx - 2 + i, cy + 3, 0.8, True))
# Center cutout (NPTH)
lower_holes.append((cx, cy, 27.0, False))  # 27mm NPTH

write_drill(f"{LOWER_OUT}/lower_pcb-PTH.drl",
            [(x,y,d,p) for x,y,d,p in lower_holes if p])
write_drill(f"{LOWER_OUT}/lower_pcb-NPTH.drl",
            [(x,y,d,p) for x,y,d,p in lower_holes if not p])

print(f"Lower PCB gerbers -> {LOWER_OUT}/")
for f in sorted(os.listdir(LOWER_OUT)):
    print(f"  {f}")


# ============================================================
# UPPER PCB — dia54mm circular, center at (100,100) mm
# ============================================================
UPPER_OUT = os.path.join(os.path.dirname(__file__), "upper_pcb/gerbers")
os.makedirs(UPPER_OUT, exist_ok=True)

outer_r2 = 27.0   # 54mm diameter

# Edge.Cuts
edge2 = circle_gerber_cmds(cx, cy, outer_r2)
write_gerber(f"{UPPER_OUT}/upper_pcb-Edge_Cuts.gbr", [("Edge.Cuts", edge2)])

# F.Cu
fcu2 = []
fcu2 += circle_gerber_cmds(cx, cy, outer_r2 - 0.3)

# Mounting holes H1/H2 at X=±15mm from center
apt = 20
fcu2.append(f"%ADD{apt}C,4.40*%")
fcu2.append(f"D{apt}*")
fcu2.append(f"X{int((cx-15)*1e6):+010d}Y{int(cy*1e6):+010d}D03*")
fcu2.append(f"X{int((cx+15)*1e6):+010d}Y{int(cy*1e6):+010d}D03*")

# SW4 — L-click, upright 6x6mm at X=-10, Y=+12 from center
# KiCad coords: (90, 88)
sw_apt = 30
fcu2.append(f"%ADD{sw_apt}C,2.00*%")
fcu2.append(f"D{sw_apt}*")
sw4x, sw4y = cx - 10, cy - 12
sw5x, sw5y = cx + 10, cy - 12
for sx, sy in [(sw4x, sw4y), (sw5x, sw5y)]:
    for dx, dy in [(-2.5, -2.5), (2.5, -2.5), (-2.5, 2.5), (2.5, 2.5)]:
        fcu2.append(f"X{int((sx+dx)*1e6):+010d}Y{int((sy+dy)*1e6):+010d}D03*")

# SW6 — Back, side-mount at X=-24, Y=0
# SW7 — Forward, side-mount at X=+24, Y=0
sw_apt2 = 31
fcu2.append(f"%ADD{sw_apt2}C,2.00*%")
fcu2.append(f"D{sw_apt2}*")
for sx, sy in [(cx - 24, cy), (cx + 24, cy)]:
    for dx, dy in [(-2.5, -2.5), (2.5, -2.5), (-2.5, 2.5), (2.5, 2.5)]:
        fcu2.append(f"X{int((sx+dx)*1e6):+010d}Y{int((sy+dy)*1e6):+010d}D03*")

# FPC connector J5 (6-pin, 0.5mm pitch) at board center-bottom
fpc2_x, fpc2_y = cx, cy + 15
apt2 = 32
fcu2.append(f"%ADD{apt2}R,0.40X1.20*%")
fcu2.append(f"D{apt2}*")
for i in range(6):
    fcu2.append(f"X{int((fpc2_x - 1.25 + i*0.5)*1e6):+010d}Y{int(fpc2_y*1e6):+010d}D03*")

write_gerber(f"{UPPER_OUT}/upper_pcb-F_Cu.gbr", [("F.Cu", fcu2)])
write_gerber(f"{UPPER_OUT}/upper_pcb-B_Cu.gbr", [("B.Cu", circle_gerber_cmds(cx, cy, outer_r2-0.3))])
write_gerber(f"{UPPER_OUT}/upper_pcb-Edge_Cuts.gbr", [("Edge.Cuts", edge2)])
write_gerber(f"{UPPER_OUT}/upper_pcb-F_Mask.gbr", [("F.Mask", fcu2)])
write_gerber(f"{UPPER_OUT}/upper_pcb-B_Mask.gbr", [("B.Mask", circle_gerber_cmds(cx, cy, outer_r2-0.3))])

# Silkscreen
silk2 = []
silk2.append("%ADD10C,0.15*%")
silk2.append("D10*")
for tx, ty, lbl in [(sw4x, sw4y-6, "SW4-L"), (sw5x, sw5y-6, "SW5-R"),
                     (cx-24, cy-4, "SW6-BCK"), (cx+24, cy-4, "SW7-FWD"),
                     (fpc2_x, fpc2_y+4, "J5-FPC"), (cx, cy-2, "FRONT->")]:
    silk2.append(f"X{int((tx-1)*1e6):+010d}Y{int(ty*1e6):+010d}D02*")
    silk2.append(f"X{int((tx+1)*1e6):+010d}Y{int(ty*1e6):+010d}D01*")
write_gerber(f"{UPPER_OUT}/upper_pcb-F_SilkS.gbr", [("F.SilkS", silk2)])

# Drill
upper_holes = []
upper_holes += [(cx-15, cy, 2.2, True), (cx+15, cy, 2.2, True)]  # mount holes
for sx, sy in [(sw4x, sw4y), (sw5x, sw5y), (cx-24, cy), (cx+24, cy)]:
    for dx, dy in [(-2.5, -2.5), (2.5, -2.5), (-2.5, 2.5), (2.5, 2.5)]:
        upper_holes.append((sx+dx, sy+dy, 0.8, True))

write_drill(f"{UPPER_OUT}/upper_pcb-PTH.drl",
            [(x,y,d,p) for x,y,d,p in upper_holes if p])

print(f"\nUpper PCB gerbers -> {UPPER_OUT}/")
for f in sorted(os.listdir(UPPER_OUT)):
    print(f"  {f}")

print("\nDone! Zip each gerbers/ folder and upload to JLCPCB.")
