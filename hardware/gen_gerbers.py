#!/usr/bin/env python3
"""
Generate Gerber + drill files for DaPao Space Mouse PCBs.
Rev 1.2: Updated for Kailh GM 8.0 THT (SW4/SW5), Blue Dot SMD (SW6/SW7),
         and SW_BT tactile on lower PCB.
Produces RS-274X Gerbers accepted by JLCPCB / PCBWay.
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
    with open(path, 'w') as f:
        f.write("%FSLAX46Y46*%\n")
        f.write("%MOMM*%\n")
        f.write("%LPD*%\n")
        f.write("G04 DaPao Space Mouse Gerber rev1.2*\n")
        for layer_name, cmds in layers:
            f.write(f"G04 Layer: {layer_name}*\n")
            for cmd in cmds:
                f.write(cmd + "\n")
        f.write("M02*\n")

def circle_gerber_cmds(cx, cy, r, n=120):
    cmds = []
    pts = circle_poly(cx, cy, r, n)
    cmds.append("%ADD10C,0.10*%")
    cmds.append("D10*")
    x0, y0 = pts[0]
    cmds.append(f"X{int(x0*1e6):+010d}Y{int(y0*1e6):+010d}D02*")
    for x, y in pts[1:]:
        cmds.append(f"X{int(x*1e6):+010d}Y{int(y*1e6):+010d}D01*")
    cmds.append(f"X{int(x0*1e6):+010d}Y{int(y0*1e6):+010d}D01*")
    return cmds

def write_drill(path, holes):
    with open(path, 'w') as f:
        f.write("M48\n")
        f.write("METRIC,TZ\n")
        f.write("FMAT,2\n")
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

def smd_pad(cmds, cx, cy, w, h, aperture):
    cmds.append(f"%ADD{aperture}R,{w:.4f}X{h:.4f}*%")
    cmds.append(f"D{aperture}*")
    cmds.append(f"X{int(cx*1e6):+010d}Y{int(cy*1e6):+010d}D03*")

# ============================================================
# LOWER PCB — dia88mm circular, center at (100,100) mm
# ============================================================
BASE = os.path.dirname(os.path.abspath(__file__))
LOWER_OUT = os.path.join(BASE, "lower_pcb/gerbers")
os.makedirs(LOWER_OUT, exist_ok=True)

cx, cy = 100.0, 100.0
outer_r = 44.0
inner_r = 13.5

# --- Edge.Cuts ---
edge_cmds = circle_gerber_cmds(cx, cy, outer_r) + circle_gerber_cmds(cx, cy, inner_r)
write_gerber(f"{LOWER_OUT}/lower_pcb-Edge_Cuts.gbr", [("Edge.Cuts", edge_cmds)])

# --- F.Cu ---
fcu = []
fcu += circle_gerber_cmds(cx, cy, outer_r - 0.3)

# Mounting holes annular rings x4 at R=30mm
apt = 20
fcu.append(f"%ADD{apt}C,4.40*%")
fcu.append(f"D{apt}*")
for angle in [0, 90, 180, 270]:
    mx = cx + 30 * math.cos(math.radians(angle))
    my = cy + 30 * math.sin(math.radians(angle))
    fcu.append(f"X{int(mx*1e6):+010d}Y{int(my*1e6):+010d}D03*")

# XIAO ESP32-S3 castellated pads
xiao_cx, xiao_cy = 118.0, 90.0
apt = 30
fcu.append(f"%ADD{apt}R,1.50X2.00*%")
fcu.append(f"D{apt}*")
for i in range(7):
    fcu.append(f"X{int((xiao_cx - 8.75)*1e6):+010d}Y{int((xiao_cy - 9 + i*3)*1e6):+010d}D03*")
    fcu.append(f"X{int((xiao_cx + 8.75)*1e6):+010d}Y{int((xiao_cy - 9 + i*3)*1e6):+010d}D03*")

# J1 USB-C (board edge, 0 deg)
usbc_x, usbc_y = 144.0, 100.0
apt = 31
fcu.append(f"%ADD{apt}R,0.80X1.60*%")
fcu.append(f"D{apt}*")
for i in range(6):
    fcu.append(f"X{int((usbc_x - 1)*1e6):+010d}Y{int((usbc_y - 2.5 + i)*1e6):+010d}D03*")

# J2 JST-PH battery connector (2-pin, 2mm pitch)
jst_x, jst_y = 82.0, 110.0
apt = 32
fcu.append(f"%ADD{apt}C,2.00*%")
fcu.append(f"D{apt}*")
fcu.append(f"X{int((jst_x - 1)*1e6):+010d}Y{int(jst_y*1e6):+010d}D03*")
fcu.append(f"X{int((jst_x + 1)*1e6):+010d}Y{int(jst_y*1e6):+010d}D03*")

# J3 FPC connector (6-pin, 0.5mm pitch)
fpc_x, fpc_y = 100.0, 85.0
apt = 33
fcu.append(f"%ADD{apt}R,0.40X1.20*%")
fcu.append(f"D{apt}*")
for i in range(6):
    fcu.append(f"X{int((fpc_x - 1.25 + i*0.5)*1e6):+010d}Y{int(fpc_y*1e6):+010d}D03*")

# U2 TP4056 SOP-8
u2x, u2y = 135.0, 95.0
apt = 34
fcu.append(f"%ADD{apt}R,0.60X1.60*%")
fcu.append(f"D{apt}*")
for i in range(4):
    fcu.append(f"X{int((u2x - 1.905)*1e6):+010d}Y{int((u2y - 1.905 + i*1.27)*1e6):+010d}D03*")
    fcu.append(f"X{int((u2x + 1.905)*1e6):+010d}Y{int((u2y - 1.905 + i*1.27)*1e6):+010d}D03*")

# U3 AP2112K SOT-23-5
u3x, u3y = 110.0, 112.0
apt = 35
fcu.append(f"%ADD{apt}R,0.60X1.00*%")
fcu.append(f"D{apt}*")
for i in range(3):
    fcu.append(f"X{int((u3x - 0.95 + i*0.95)*1e6):+010d}Y{int((u3y + 1.4)*1e6):+010d}D03*")
for i in range(2):
    fcu.append(f"X{int((u3x - 0.95 + i*1.9)*1e6):+010d}Y{int((u3y - 1.4)*1e6):+010d}D03*")

# SW1 power switch (SPDT, board edge, 180 deg = left side)
sw1_x = cx - outer_r + 2.0  # board edge left
sw1_y = cy
apt = 36
fcu.append(f"%ADD{apt}R,1.20X1.80*%")
fcu.append(f"D{apt}*")
for i in range(3):
    fcu.append(f"X{int((sw1_x + 1.0)*1e6):+010d}Y{int((sw1_y - 1.5 + i*1.5)*1e6):+010d}D03*")

# SW2 BOOT + SW3 RESET (3x4mm tactile SMD, near XIAO)
apt = 37
fcu.append(f"%ADD{apt}R,1.00X1.20*%")
fcu.append(f"D{apt}*")
for bx, by in [(xiao_cx - 5, xiao_cy + 13), (xiao_cx + 5, xiao_cy + 13)]:
    for dx in [-1.5, 1.5]:
        fcu.append(f"X{int((bx+dx)*1e6):+010d}Y{int(by*1e6):+010d}D03*")

# SW_BT Bluetooth sync (3x4mm tactile SMD, board edge at 90deg = top)
# 90 deg: x=cx, y=cy+outer_r => (100, 144). Place just inside edge.
swbt_x = cx
swbt_y = cy + outer_r - 3.0
apt = 38
fcu.append(f"%ADD{apt}R,1.00X1.20*%")
fcu.append(f"D{apt}*")
for dx in [-1.5, 1.5]:
    fcu.append(f"X{int((swbt_x+dx)*1e6):+010d}Y{int(swbt_y*1e6):+010d}D03*")

# Resistors/caps (0402 generic pads)
apt = 40
fcu.append(f"%ADD{apt}R,0.60X0.80*%")
fcu.append(f"D{apt}*")
passives = [
    # R_PU5 JOY_SW pull-up
    (108, 92), (109, 92),
    # R_PU_BT BT sync pull-up
    (103, 137), (104, 137),
    # R5/R6 VBAT divider
    (108, 97), (108, 99),
    # R7 PROG
    (130, 100), (131, 100),
    # R8/R9 LED
    (138, 100), (138, 102),
    # R10/R11 CC
    (140, 104), (140, 106),
    # C1-C5 decoupling
    (112, 88), (114, 88), (116, 88), (118, 88), (120, 88),
]
for px, py in passives:
    fcu.append(f"X{int(px*1e6):+010d}Y{int(py*1e6):+010d}D03*")

write_gerber(f"{LOWER_OUT}/lower_pcb-F_Cu.gbr", [("F.Cu", fcu)])
write_gerber(f"{LOWER_OUT}/lower_pcb-B_Cu.gbr", [("B.Cu", circle_gerber_cmds(cx, cy, outer_r - 0.3))])
write_gerber(f"{LOWER_OUT}/lower_pcb-F_Mask.gbr", [("F.Mask", fcu)])
write_gerber(f"{LOWER_OUT}/lower_pcb-B_Mask.gbr", [("B.Mask", circle_gerber_cmds(cx, cy, outer_r - 0.3))])

# Silkscreen
silk = []
silk.append("%ADD11C,0.15*%")
silk.append("D11*")
labels = [
    (xiao_cx, xiao_cy - 13, "U1-XIAO-ESP32S3"),
    (u2x, u2y - 6, "U2-TP4056"),
    (u3x, u3y - 5, "U3-LDO"),
    (jst_x, jst_y - 4, "J2-BAT"),
    (usbc_x - 4, usbc_y - 6, "J1-USB-C"),
    (fpc_x, fpc_y - 4, "J3-FPC-6P"),
    (sw1_x + 4, sw1_y - 4, "SW1-PWR"),
    (swbt_x, swbt_y - 4, "SW_BT-SYNC"),
    (cx, cy, "LOWER-PCB-R1.1"),
]
for tx, ty, lbl in labels:
    silk.append(f"X{int((tx-1)*1e6):+010d}Y{int(ty*1e6):+010d}D02*")
    silk.append(f"X{int((tx+1)*1e6):+010d}Y{int(ty*1e6):+010d}D01*")
write_gerber(f"{LOWER_OUT}/lower_pcb-F_SilkS.gbr", [("F.SilkS", silk)])

# Drill
lower_holes = []
# M2 mounting x4
for angle in [0, 90, 180, 270]:
    mx = cx + 30 * math.cos(math.radians(angle))
    my = cy + 30 * math.sin(math.radians(angle))
    lower_holes.append((mx, my, 2.2, True))
# USB-C mech holes
lower_holes += [(usbc_x, usbc_y - 2, 0.8, True), (usbc_x, usbc_y + 2, 0.8, True)]
# JST holes (2-pin, through-hole)
lower_holes += [(jst_x - 1, jst_y, 1.0, True), (jst_x + 1, jst_y, 1.0, True)]
# Joystick 5-pin header
for i in range(5):
    lower_holes.append((cx - 2 + i, cy + 3, 0.8, True))
# Center cutout NPTH 27mm
lower_holes.append((cx, cy, 27.0, False))

write_drill(f"{LOWER_OUT}/lower_pcb-PTH.drl",  [(x,y,d,p) for x,y,d,p in lower_holes if p])
write_drill(f"{LOWER_OUT}/lower_pcb-NPTH.drl", [(x,y,d,p) for x,y,d,p in lower_holes if not p])

print(f"Lower PCB gerbers -> {LOWER_OUT}/")
for f in sorted(os.listdir(LOWER_OUT)):
    print(f"  {f}")


# ============================================================
# UPPER PCB — dia54mm circular, center at (100,100) mm
# Rev 1.3: SW4/SW5 Kailh GM 8.0 THT, SW6/SW7 Blue Dot SMD
# ============================================================
UPPER_OUT = os.path.join(BASE, "upper_pcb/gerbers")
os.makedirs(UPPER_OUT, exist_ok=True)

outer_r2 = 27.0

# --- Edge.Cuts ---
edge2 = circle_gerber_cmds(cx, cy, outer_r2)
write_gerber(f"{UPPER_OUT}/upper_pcb-Edge_Cuts.gbr", [("Edge.Cuts", edge2)])

# Switch positions
sw4x, sw4y = cx - 10.0, cy - 12.0   # SW4 L-click
sw5x, sw5y = cx + 10.0, cy - 12.0   # SW5 R-click
sw6x, sw6y = cx - 22.0, cy           # SW6 Back  (Blue Dot, board edge)
sw7x, sw7y = cx + 22.0, cy           # SW7 Fwd   (Blue Dot, board edge)

# --- F.Cu ---
fcu2 = []
fcu2 += circle_gerber_cmds(cx, cy, outer_r2 - 0.3)

# H1/H2 mount hole pads at X=+-15mm
apt = 20
fcu2.append(f"%ADD{apt}C,4.40*%")
fcu2.append(f"D{apt}*")
fcu2.append(f"X{int((cx-15)*1e6):+010d}Y{int(cy*1e6):+010d}D03*")
fcu2.append(f"X{int((cx+15)*1e6):+010d}Y{int(cy*1e6):+010d}D03*")

# SW4 / SW5 — Kailh GM 8.0 THT Cherry-MX footprint (3-pin)
# Pin layout per Cherry MX standard (mm from switch center):
#   NC  at (-3.81, 0)
#   COM at (0,    +3.81)   -- wired to GND
#   NO  at (+3.81, 0)      -- wired to BTN signal
# Plus two mounting/stabilizer legs at (+-5.08, -6.35) -- not electrically connected
apt = 30
fcu2.append(f"%ADD{apt}C,2.00*%")   # 2mm pad for THT
fcu2.append(f"D{apt}*")
for sx, sy in [(sw4x, sw4y), (sw5x, sw5y)]:
    # NC pin
    fcu2.append(f"X{int((sx-3.81)*1e6):+010d}Y{int(sy*1e6):+010d}D03*")
    # COM pin
    fcu2.append(f"X{int(sx*1e6):+010d}Y{int((sy+3.81)*1e6):+010d}D03*")
    # NO pin
    fcu2.append(f"X{int((sx+3.81)*1e6):+010d}Y{int(sy*1e6):+010d}D03*")

# SW6 / SW7 — Kailh Blue Dot SMD (2-pin)
# Pads: 1.8x2.8mm, spaced 5mm centre-to-centre (horizontal)
apt = 31
fcu2.append(f"%ADD{apt}R,1.80X2.80*%")
fcu2.append(f"D{apt}*")
for sx, sy in [(sw6x, sw6y), (sw7x, sw7y)]:
    fcu2.append(f"X{int((sx-2.5)*1e6):+010d}Y{int(sy*1e6):+010d}D03*")   # GND pad
    fcu2.append(f"X{int((sx+2.5)*1e6):+010d}Y{int(sy*1e6):+010d}D03*")   # SIG pad

# J5 FPC (6-pin, 0.5mm pitch)
fpc2_x, fpc2_y = cx, cy + 15.0
apt = 32
fcu2.append(f"%ADD{apt}R,0.40X1.20*%")
fcu2.append(f"D{apt}*")
for i in range(6):
    fcu2.append(f"X{int((fpc2_x - 1.25 + i*0.5)*1e6):+010d}Y{int(fpc2_y*1e6):+010d}D03*")

# R1-R4 pull-ups (10k 0402), C1 decoupling (100nF 0402)
apt = 40
fcu2.append(f"%ADD{apt}R,0.60X0.80*%")
fcu2.append(f"D{apt}*")
passives2 = [
    # R1 SW4 pull-up
    (sw4x - 1, sw4y + 6), (sw4x + 1, sw4y + 6),
    # R2 SW5 pull-up
    (sw5x - 1, sw5y + 6), (sw5x + 1, sw5y + 6),
    # R3 SW6 pull-up
    (sw6x + 3, sw6y - 3), (sw6x + 5, sw6y - 3),
    # R4 SW7 pull-up
    (sw7x - 5, sw7y - 3), (sw7x - 3, sw7y - 3),
    # C1 decoupling
    (cx - 1, cy + 8), (cx + 1, cy + 8),
]
for px, py in passives2:
    fcu2.append(f"X{int(px*1e6):+010d}Y{int(py*1e6):+010d}D03*")

write_gerber(f"{UPPER_OUT}/upper_pcb-F_Cu.gbr", [("F.Cu", fcu2)])
write_gerber(f"{UPPER_OUT}/upper_pcb-B_Cu.gbr", [("B.Cu", circle_gerber_cmds(cx, cy, outer_r2-0.3))])
write_gerber(f"{UPPER_OUT}/upper_pcb-F_Mask.gbr", [("F.Mask", fcu2)])
write_gerber(f"{UPPER_OUT}/upper_pcb-B_Mask.gbr", [("B.Mask", circle_gerber_cmds(cx, cy, outer_r2-0.3))])

# Silkscreen
silk2 = []
silk2.append("%ADD11C,0.15*%")
silk2.append("D11*")
for tx, ty, lbl in [
    (sw4x, sw4y-8,  "SW4-GM8-L"),
    (sw5x, sw5y-8,  "SW5-GM8-R"),
    (sw6x, sw6y-5,  "SW6-BlueDot-BCK"),
    (sw7x, sw7y-5,  "SW7-BlueDot-FWD"),
    (fpc2_x, fpc2_y+5, "J5-FPC-6P"),
    (cx, cy+2, "UPPER-PCB-R1.3"),
]:
    silk2.append(f"X{int((tx-1)*1e6):+010d}Y{int(ty*1e6):+010d}D02*")
    silk2.append(f"X{int((tx+1)*1e6):+010d}Y{int(ty*1e6):+010d}D01*")
write_gerber(f"{UPPER_OUT}/upper_pcb-F_SilkS.gbr", [("F.SilkS", silk2)])

# Drill — GM 8.0 THT needs through holes (1.5mm drill per Cherry spec)
upper_holes = []
# H1/H2 mount holes
upper_holes += [(cx-15, cy, 2.2, True), (cx+15, cy, 2.2, True)]
# SW4/SW5 GM 8.0 THT pins: NC, COM, NO (1.5mm drill)
for sx, sy in [(sw4x, sw4y), (sw5x, sw5y)]:
    upper_holes.append((sx-3.81, sy,      1.5, True))  # NC
    upper_holes.append((sx,      sy+3.81, 1.5, True))  # COM
    upper_holes.append((sx+3.81, sy,      1.5, True))  # NO
# SW6/SW7 Blue Dot SMD — no through holes needed

write_drill(f"{UPPER_OUT}/upper_pcb-PTH.drl", upper_holes)

print(f"\nUpper PCB gerbers -> {UPPER_OUT}/")
for f in sorted(os.listdir(UPPER_OUT)):
    print(f"  {f}")

print("\nDone! Zip each gerbers/ folder and upload to JLCPCB.")
