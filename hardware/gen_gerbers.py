#!/usr/bin/env python3
"""
Generate Gerber + drill files for DaPao Space Mouse PCBs.
Rev 1.3 Lower PCB layout:
  - Joystick centered on board
  - XIAO ESP32-S3 at north, USB-C facing north (board edge)
  - FPC J3 between joystick and south edge
  - Circular dia88mm board
  - Mounting holes adjusted around components
  - Silkscreen labels on all connections

Coordinate system:
  Board center: (100, 100) mm
  North = lower Y (toward top of page / forward)
  South = higher Y (toward bottom / back)
  East  = higher X (right)
  West  = lower X (left)

Component placement:
  U1 XIAO:    center (100, 70)  -- north, USB-C at (100, 57) facing north
  J1 USB-C:   (100, 57)         -- north board edge, forward-facing
  J4 Joystick: (100, 100)       -- board center
  J3 FPC:     (100, 120)        -- south of joystick, north of south edge
  U2 TP4056:  (118, 82)         -- NE quadrant
  U3 LDO:     (118, 95)         -- east
  U4 ESD:     (118, 68)         -- NE near USB-C
  J2 Battery: (82, 115)         -- SW quadrant
  SW1 Power:  (58, 100)         -- west board edge (180 deg)
  SW_BT:      (100, 140)        -- south board edge (270 deg / south)
  M2 holes:   45/135/225/315 deg at R=36mm (diagonal, clear of all components)
"""
import os, math

BASE = os.path.dirname(os.path.abspath(__file__))

def circle_poly(cx, cy, r, n=120):
    return [(cx + r*math.cos(math.radians(360*i/n)),
             cy + r*math.sin(math.radians(360*i/n))) for i in range(n)]

def write_gerber(path, layers):
    with open(path, 'w') as f:
        f.write("%FSLAX46Y46*%\n%MOMM*%\n%LPD*%\n")
        f.write("G04 DaPao Space Mouse rev1.3*\n")
        for name, cmds in layers:
            f.write(f"G04 {name}*\n")
            for c in cmds: f.write(c+"\n")
        f.write("M02*\n")

def write_drill(path, holes):
    with open(path, 'w') as f:
        f.write("M48\nMETRIC,TZ\nFMAT,2\n")
        by = {}
        for x,y,d,p in holes: by.setdefault((d,p),[]).append((x,y))
        for t,(k,v) in enumerate(by.items(),1): f.write(f"T{t:02d}C{k[0]:.3f}\n")
        f.write("%\nG90\nG05\n")
        for t,(k,v) in enumerate(by.items(),1):
            f.write(f"T{t:02d}\n")
            for x,y in v: f.write(f"X{int(x*1e4):+08d}Y{int(y*1e4):+08d}\n")
        f.write("T00\nM30\n")

def outline(cx, cy, r, n=120, apt=10, apt_size=0.10):
    pts = circle_poly(cx, cy, r, n)
    c = [f"%ADD{apt}C,{apt_size:.3f}*%", f"D{apt}*"]
    x0,y0 = pts[0]
    c.append(f"X{int(x0*1e6):+010d}Y{int(y0*1e6):+010d}D02*")
    for x,y in pts[1:]: c.append(f"X{int(x*1e6):+010d}Y{int(y*1e6):+010d}D01*")
    c.append(f"X{int(x0*1e6):+010d}Y{int(y0*1e6):+010d}D01*")
    return c

def smd(cx, cy, w, h, apt):
    return [f"%ADD{apt}R,{w:.4f}X{h:.4f}*%", f"D{apt}*",
            f"X{int(cx*1e6):+010d}Y{int(cy*1e6):+010d}D03*"]

def circ_pad(cx, cy, d, apt):
    return [f"%ADD{apt}C,{d:.4f}*%", f"D{apt}*",
            f"X{int(cx*1e6):+010d}Y{int(cy*1e6):+010d}D03*"]

# Silkscreen helpers: draw box outline + cross at center for each component
def silk_box(cx, cy, w, h, apt=10):
    """Draw a rectangular outline on silkscreen."""
    x1,y1 = cx-w/2, cy-h/2
    x2,y2 = cx+w/2, cy+h/2
    pts = [(x1,y1),(x2,y1),(x2,y2),(x1,y2),(x1,y1)]
    c = [f"D{apt}*"]
    c.append(f"X{int(pts[0][0]*1e6):+010d}Y{int(pts[0][1]*1e6):+010d}D02*")
    for px,py in pts[1:]: c.append(f"X{int(px*1e6):+010d}Y{int(py*1e6):+010d}D01*")
    return c

def silk_cross(cx, cy, size=1.0, apt=10):
    s = size/2
    return [f"D{apt}*",
            f"X{int((cx-s)*1e6):+010d}Y{int(cy*1e6):+010d}D02*",
            f"X{int((cx+s)*1e6):+010d}Y{int(cy*1e6):+010d}D01*",
            f"X{int(cx*1e6):+010d}Y{int((cy-s)*1e6):+010d}D02*",
            f"X{int(cx*1e6):+010d}Y{int((cy+s)*1e6):+010d}D01*"]

def silk_line(x1,y1,x2,y2,apt=10):
    return [f"D{apt}*",
            f"X{int(x1*1e6):+010d}Y{int(y1*1e6):+010d}D02*",
            f"X{int(x2*1e6):+010d}Y{int(y2*1e6):+010d}D01*"]

def silk_pin1(cx, cy, apt=10):
    """Small triangle marker for pin 1."""
    s = 0.8
    return [f"D{apt}*",
            f"X{int((cx-s)*1e6):+010d}Y{int((cy-s)*1e6):+010d}D02*",
            f"X{int((cx+s)*1e6):+010d}Y{int((cy-s)*1e6):+010d}D01*",
            f"X{int(cx*1e6):+010d}Y{int((cy+s)*1e6):+010d}D01*",
            f"X{int((cx-s)*1e6):+010d}Y{int((cy-s)*1e6):+010d}D01*"]

# ================================================================
# LOWER PCB  dia88mm  rev 1.3 layout
# ================================================================
LOWER_OUT = os.path.join(BASE, "lower_pcb/gerbers")
os.makedirs(LOWER_OUT, exist_ok=True)

BX, BY = 100.0, 100.0   # board center
OR = 44.0                # outer radius
IR = 13.5                # center cutout radius (for joystick shaft)

# ---- Key component centers ----
# North = lower Y
XIAO_X,  XIAO_Y  = BX,       BY - 30.0   # U1 XIAO center (100, 70)
USBC_X,  USBC_Y  = BX,       BY - 43.0   # J1 USB-C at north edge (100, 57)
JOY_X,   JOY_Y   = BX,       BY          # J4 Joystick at center (100, 100)
FPC_X,   FPC_Y   = BX,       BY + 20.0   # J3 FPC (100, 120)
TP_X,    TP_Y    = BX + 18,  BY - 18.0   # U2 TP4056 (118, 82)
LDO_X,   LDO_Y   = BX + 18,  BY -  5.0   # U3 LDO    (118, 95)
ESD_X,   ESD_Y   = BX + 18,  BY - 32.0   # U4 ESD    (118, 68)
BAT_X,   BAT_Y   = BX - 18,  BY + 15.0   # J2 Battery (82, 115)
SW1_X,   SW1_Y   = BX - 42,  BY          # SW1 Power west edge (58, 100)
SWBT_X,  SWBT_Y  = BX,       BY + 40.0   # SW_BT south edge (100, 140)

# M2 mounting holes at 45/135/225/315 deg, R=36mm
MH_R = 36.0
MH_ANGLES = [45, 135, 225, 315]
mount_holes = [(BX + MH_R*math.cos(math.radians(a)),
                BY + MH_R*math.sin(math.radians(a))) for a in MH_ANGLES]

# ================================================================
#  Edge.Cuts
# ================================================================
edge = outline(BX, BY, OR, apt=10) + outline(BX, BY, IR, apt=10)
write_gerber(f"{LOWER_OUT}/lower_pcb-Edge_Cuts.gbr", [("Edge_Cuts", edge)])

# ================================================================
#  F.Cu
# ================================================================
fcu = []
fcu += outline(BX, BY, OR-0.3, apt=10)

# --- Mounting hole annular rings (4x M2, 4.4mm pad, 2.2mm drill) ---
apt = 20
for hx,hy in mount_holes:
    fcu += circ_pad(hx, hy, 4.4, apt); apt+=1

# --- U1 XIAO ESP32-S3 castellated module ---
# 21mm long x 17.5mm wide, castellated pads on left/right (3 top, 8 each side, 1 bottom)
# 14 pads per side, 1.27mm pitch
# Left pads at XIAO_X - 8.75, Right pads at XIAO_X + 8.75
# Pads run from XIAO_Y - 8.89 to XIAO_Y + 8.89 (7 pads, 2.54mm pitch)
apt = 30
fcu.append(f"%ADD{apt}R,1.50X2.00*%")
fcu.append(f"D{apt}*")
for i in range(7):
    py = XIAO_Y - 9.0 + i*3.0
    # Left side pads
    fcu.append(f"X{int((XIAO_X-8.75)*1e6):+010d}Y{int(py*1e6):+010d}D03*")
    # Right side pads
    fcu.append(f"X{int((XIAO_X+8.75)*1e6):+010d}Y{int(py*1e6):+010d}D03*")

# --- J1 USB-C (north edge, forward-facing) ---
# Mid-mount receptacle, 5 signal + 4 GND/shell pads
apt = 31
fcu.append(f"%ADD{apt}R,0.80X1.80*%")
fcu.append(f"D{apt}*")
for i in range(5):
    px = USBC_X - 1.25 + i*0.625
    fcu.append(f"X{int(px*1e6):+010d}Y{int(USBC_Y*1e6):+010d}D03*")
# Shell/mounting pads
apt = 32
fcu.append(f"%ADD{apt}R,1.60X2.00*%")
fcu.append(f"D{apt}*")
for dx in [-2.5, 2.5]:
    fcu.append(f"X{int((USBC_X+dx)*1e6):+010d}Y{int((USBC_Y+1.5)*1e6):+010d}D03*")

# --- J4 Joystick module (centered on board) ---
# 5-pin right-angle header, 2.54mm pitch, module center at JOY_X/Y
# Header pins on south edge of module, spanning X=-5.08 to +5.08 from center
apt = 33
fcu.append(f"%ADD{apt}C,2.00*%")
fcu.append(f"D{apt}*")
for i in range(5):
    px = JOY_X - 5.08 + i*2.54
    fcu.append(f"X{int(px*1e6):+010d}Y{int((JOY_Y+12.5)*1e6):+010d}D03*")

# --- J3 FPC 6-pin 0.5mm (south of joystick) ---
apt = 34
fcu.append(f"%ADD{apt}R,0.40X1.20*%")
fcu.append(f"D{apt}*")
for i in range(6):
    px = FPC_X - 1.25 + i*0.5
    fcu.append(f"X{int(px*1e6):+010d}Y{int(FPC_Y*1e6):+010d}D03*")
# FPC mounting/latch pads
apt = 35
fcu.append(f"%ADD{apt}R,1.20X1.80*%")
fcu.append(f"D{apt}*")
for dx in [-2.5, 2.5]:
    fcu.append(f"X{int((FPC_X+dx)*1e6):+010d}Y{int((FPC_Y+0.8)*1e6):+010d}D03*")

# --- U2 TP4056 SOP-8 (NE quadrant) ---
apt = 36
fcu.append(f"%ADD{apt}R,0.60X1.60*%")
fcu.append(f"D{apt}*")
for i in range(4):
    py = TP_Y - 1.905 + i*1.27
    fcu.append(f"X{int((TP_X-1.905)*1e6):+010d}Y{int(py*1e6):+010d}D03*")
    fcu.append(f"X{int((TP_X+1.905)*1e6):+010d}Y{int(py*1e6):+010d}D03*")

# --- U3 AP2112K LDO SOT-23-5 (east) ---
apt = 37
fcu.append(f"%ADD{apt}R,0.55X1.00*%")
fcu.append(f"D{apt}*")
for i,dx in enumerate([-0.95, 0, 0.95]):
    fcu.append(f"X{int((LDO_X+dx)*1e6):+010d}Y{int((LDO_Y+1.4)*1e6):+010d}D03*")
for dx in [-0.95, 0.95]:
    fcu.append(f"X{int((LDO_X+dx)*1e6):+010d}Y{int((LDO_Y-1.4)*1e6):+010d}D03*")

# --- U4 USBLC6 ESD SOT-23-6 (NE near USB-C) ---
apt = 38
fcu.append(f"%ADD{apt}R,0.55X1.00*%")
fcu.append(f"D{apt}*")
for i,dx in enumerate([-0.95, 0, 0.95]):
    fcu.append(f"X{int((ESD_X+dx)*1e6):+010d}Y{int((ESD_Y+1.4)*1e6):+010d}D03*")
    fcu.append(f"X{int((ESD_X+dx)*1e6):+010d}Y{int((ESD_Y-1.4)*1e6):+010d}D03*")

# --- J2 JST-PH 2-pin battery (SW quadrant) ---
apt = 39
fcu.append(f"%ADD{apt}C,2.00*%")
fcu.append(f"D{apt}*")
for dx in [-1.0, 1.0]:
    fcu.append(f"X{int((BAT_X+dx)*1e6):+010d}Y{int(BAT_Y*1e6):+010d}D03*")

# --- SW1 SPDT power switch (west board edge) ---
apt = 40
fcu.append(f"%ADD{apt}R,1.20X1.80*%")
fcu.append(f"D{apt}*")
for dy in [-1.5, 0.0, 1.5]:
    fcu.append(f"X{int((SW1_X+2.0)*1e6):+010d}Y{int((SW1_Y+dy)*1e6):+010d}D03*")

# --- SW_BT Bluetooth sync (south board edge) ---
apt = 41
fcu.append(f"%ADD{apt}R,1.00X1.20*%")
fcu.append(f"D{apt}*")
for dx in [-1.5, 1.5]:
    fcu.append(f"X{int((SWBT_X+dx)*1e6):+010d}Y{int(SWBT_Y*1e6):+010d}D03*")

# --- SW2 BOOT + SW3 RESET (east of XIAO, 3x4mm SMD tactile) ---
apt = 42
fcu.append(f"%ADD{apt}R,1.00X1.20*%")
fcu.append(f"D{apt}*")
for bx,by in [(XIAO_X+12, XIAO_Y-4), (XIAO_X+12, XIAO_Y+4)]:
    for dx in [-1.5, 1.5]:
        fcu.append(f"X{int((bx+dx)*1e6):+010d}Y{int(by*1e6):+010d}D03*")

# --- 0402 Passives ---
apt = 50
fcu.append(f"%ADD{apt}R,0.60X0.80*%")
fcu.append(f"D{apt}*")
passives_0402 = [
    # R_PU5: JOY_SW pull-up near joystick NE
    (JOY_X+8, JOY_Y-8), (JOY_X+10, JOY_Y-8),
    # R_PU_BT: BT sync pull-up near SW_BT
    (SWBT_X+4, SWBT_Y-4), (SWBT_X+6, SWBT_Y-4),
    # R5/R6: VBAT divider near XIAO GPIO4
    (XIAO_X-12, XIAO_Y+6), (XIAO_X-12, XIAO_Y+8),
    # R7: TP4056 PROG
    (TP_X-5, TP_Y+5), (TP_X-5, TP_Y+7),
    # R8/R9: LED resistors
    (TP_X+5, TP_Y+2), (TP_X+5, TP_Y+4),
    # R10/R11: CC1/CC2 for USB-C
    (USBC_X+5, USBC_Y+3), (USBC_X+5, USBC_Y+5),
    # C1-C5: decoupling on 3V3 rail near XIAO
    (XIAO_X-6, XIAO_Y+12),(XIAO_X-4,XIAO_Y+12),
    (XIAO_X-2, XIAO_Y+12),(XIAO_X,   XIAO_Y+12),
    (XIAO_X+2, XIAO_Y+12),
    # C6/C7: bulk caps on VBUS and BAT+
    (TP_X-5, TP_Y-4), (TP_X-5, TP_Y-6),
]
for px,py in passives_0402:
    fcu.append(f"X{int(px*1e6):+010d}Y{int(py*1e6):+010d}D03*")

# --- LEDs (0402) ---
apt = 51
fcu.append(f"%ADD{apt}R,0.60X0.80*%")
fcu.append(f"D{apt}*")
for lx,ly in [(TP_X+7, TP_Y-2), (TP_X+7, TP_Y+1)]:
    fcu.append(f"X{int(lx*1e6):+010d}Y{int(ly*1e6):+010d}D03*")

write_gerber(f"{LOWER_OUT}/lower_pcb-F_Cu.gbr", [("F.Cu", fcu)])

# B.Cu — full ground plane
bcu = outline(BX, BY, OR-0.3, apt=10)
write_gerber(f"{LOWER_OUT}/lower_pcb-B_Cu.gbr", [("B.Cu", bcu)])

# Mask layers match copper
write_gerber(f"{LOWER_OUT}/lower_pcb-F_Mask.gbr", [("F.Mask", fcu)])
write_gerber(f"{LOWER_OUT}/lower_pcb-B_Mask.gbr", [("B.Mask", bcu)])

# ================================================================
#  F.SilkS — component outlines + connection labels
# ================================================================
silk = []
# Aperture for silkscreen lines (0.15mm)
silk.append("%ADD10C,0.15*%")

# U1 XIAO outline + label
silk += silk_box(XIAO_X, XIAO_Y, 17.5, 21.0)
silk += silk_cross(XIAO_X, XIAO_Y)
# Label: U1 XIAO ESP32-S3
silk += silk_line(XIAO_X-8, XIAO_Y-12, XIAO_X+8, XIAO_Y-12)   # top edge annotation line
# Pin labels along left side (GPIO assignments)
gpio_labels = [
    (XIAO_X-8.75, XIAO_Y-9,  "3V3"),
    (XIAO_X-8.75, XIAO_Y-6,  "GND"),
    (XIAO_X-8.75, XIAO_Y-3,  "G1-JOY_X"),
    (XIAO_X-8.75, XIAO_Y+0,  "G2-JOY_Y"),
    (XIAO_X-8.75, XIAO_Y+3,  "G3-JOY_SW"),
    (XIAO_X-8.75, XIAO_Y+6,  "G4-VBAT"),
    (XIAO_X-8.75, XIAO_Y+9,  "GND"),
]
gpio_labels_r = [
    (XIAO_X+8.75, XIAO_Y-9,  "G5-BTN_L"),
    (XIAO_X+8.75, XIAO_Y-6,  "G6-BTN_R"),
    (XIAO_X+8.75, XIAO_Y-3,  "G7-BTN_BK"),
    (XIAO_X+8.75, XIAO_Y+0,  "G8-BTN_FW"),
    (XIAO_X+8.75, XIAO_Y+3,  "G9-BT_SYNC"),
    (XIAO_X+8.75, XIAO_Y+6,  "3V3"),
    (XIAO_X+8.75, XIAO_Y+9,  "GND"),
]
# Tick marks at each pad position for left and right sides
for px,py,lbl in gpio_labels + gpio_labels_r:
    silk += silk_line(px-0.5, py, px+0.5, py)

# J1 USB-C outline
silk += silk_box(USBC_X, USBC_Y, 9.0, 3.5)
# Arrow pointing north (forward)
silk += silk_line(USBC_X, USBC_Y-3, USBC_X, USBC_Y-5)
silk += silk_line(USBC_X-1, USBC_Y-4, USBC_X, USBC_Y-5)
silk += silk_line(USBC_X+1, USBC_Y-4, USBC_X, USBC_Y-5)
# Label: J1 USB-C CHRG
silk += silk_line(USBC_X-4, USBC_Y+3, USBC_X+4, USBC_Y+3)

# J4 Joystick outline (25x25mm module)
silk += silk_box(JOY_X, JOY_Y, 25.0, 25.0)
silk += silk_cross(JOY_X, JOY_Y, 3.0)
# Pin labels: VCC GND X Y SW (south edge header)
for i,(lbl) in enumerate(["3V3","GND","JOY_X","JOY_Y","JOY_SW"]):
    px = JOY_X - 5.08 + i*2.54
    silk += silk_line(px, JOY_Y+12.5, px, JOY_Y+14.5)
# Label: J4 JOYSTICK
silk += silk_line(JOY_X-8, JOY_Y-14, JOY_X+8, JOY_Y-14)

# J3 FPC outline (6-pin, ~4.5mm wide x 3.5mm tall)
silk += silk_box(FPC_X, FPC_Y, 5.0, 3.5)
silk += silk_pin1(FPC_X-2.5, FPC_Y-1.0)  # Pin 1 marker
# Pin labels
for i,(lbl) in enumerate(["3V3","GND","BTN_L","BTN_R","BTN_BK","BTN_FW"]):
    px = FPC_X - 1.25 + i*0.5
    silk += silk_line(px, FPC_Y+2, px, FPC_Y+3)
# Label: J3 FPC-6P TO_UPPER_PCB
silk += silk_line(FPC_X-3, FPC_Y+4, FPC_X+3, FPC_Y+4)

# U2 TP4056 outline
silk += silk_box(TP_X, TP_Y, 5.0, 6.5)
silk += silk_pin1(TP_X-2.5, TP_Y-3.25)
# Labels: VIN BAT GND on nearby
silk += silk_line(TP_X-3, TP_Y-4, TP_X+3, TP_Y-4)

# U3 LDO outline
silk += silk_box(LDO_X, LDO_Y, 3.0, 3.0)
silk += silk_pin1(LDO_X-1.5, LDO_Y-1.5)
silk += silk_line(LDO_X-2, LDO_Y-2.5, LDO_X+2, LDO_Y-2.5)

# U4 ESD outline
silk += silk_box(ESD_X, ESD_Y, 3.0, 3.5)
silk += silk_pin1(ESD_X-1.5, ESD_Y-1.75)
silk += silk_line(ESD_X-2, ESD_Y-2.5, ESD_X+2, ESD_Y-2.5)

# J2 battery connector outline
silk += silk_box(BAT_X, BAT_Y, 9.0, 6.0)
silk += silk_pin1(BAT_X-4.5, BAT_Y-3.0)
# +/- labels
silk += silk_line(BAT_X-1.5, BAT_Y, BAT_X-1.5, BAT_Y-4)  # BAT+
silk += silk_line(BAT_X+1.5, BAT_Y, BAT_X+1.5, BAT_Y-4)  # GND
silk += silk_line(BAT_X-4.5, BAT_Y+3, BAT_X+4.5, BAT_Y+3)

# SW1 power switch outline
silk += silk_box(SW1_X+2, SW1_Y, 8.0, 5.5)
silk += silk_line(SW1_X+3, SW1_Y-4, SW1_X+8, SW1_Y-4)

# SW_BT Bluetooth sync outline + label
silk += silk_box(SWBT_X, SWBT_Y, 5.0, 4.0)
silk += silk_line(SWBT_X-3, SWBT_Y+3, SWBT_X+3, SWBT_Y+3)

# SW2/SW3 BOOT/RESET
silk += silk_box(XIAO_X+12, XIAO_Y-4, 4.0, 3.5)
silk += silk_box(XIAO_X+12, XIAO_Y+4, 4.0, 3.5)

# Mounting hole circles
silk.append("%ADD10C,0.15*%")
for hx,hy in mount_holes:
    silk += outline(hx, hy, 2.5, n=36, apt=10, apt_size=0.15)

# North/South/East/West orientation arrows at edge
# North arrow (top)
silk += silk_line(BX, BY-37, BX, BY-41)
silk += silk_line(BX-1, BY-40, BX, BY-42)
silk += silk_line(BX+1, BY-40, BX, BY-42)
# Label lines for board edge features
# USB-C at north
silk += silk_line(BX-5, BY-43.5, BX+5, BY-43.5)
# SW1 at west
silk += silk_line(BX-43, BY-2, BX-43, BY+2)
# SW_BT at south
silk += silk_line(BX-3, BY+41.5, BX+3, BY+41.5)

write_gerber(f"{LOWER_OUT}/lower_pcb-F_SilkS.gbr", [("F.SilkS", silk)])

# ================================================================
#  Drill file
# ================================================================
lower_holes = []

# M2 mount holes (4x at 45/135/225/315 deg, R=36mm)
for hx,hy in mount_holes:
    lower_holes.append((hx, hy, 2.2, True))

# J1 USB-C mechanical tabs
lower_holes += [(USBC_X-2.5, USBC_Y+1.5, 0.8, True),
                (USBC_X+2.5, USBC_Y+1.5, 0.8, True)]

# J4 Joystick 5-pin header (through-hole)
for i in range(5):
    lower_holes.append((JOY_X-5.08+i*2.54, JOY_Y+12.5, 0.8, True))

# J2 JST-PH through-hole
lower_holes += [(BAT_X-1, BAT_Y, 0.8, True), (BAT_X+1, BAT_Y, 0.8, True)]

# Center cutout NPTH 27mm
lower_holes.append((BX, BY, 27.0, False))

write_drill(f"{LOWER_OUT}/lower_pcb-PTH.drl",  [(x,y,d,p) for x,y,d,p in lower_holes if p])
write_drill(f"{LOWER_OUT}/lower_pcb-NPTH.drl", [(x,y,d,p) for x,y,d,p in lower_holes if not p])

print(f"Lower PCB gerbers -> {LOWER_OUT}/")
for f in sorted(os.listdir(LOWER_OUT)):
    print(f"  {f}")


# ================================================================
# UPPER PCB — dia54mm rev 1.3 (unchanged layout, regenerated)
# ================================================================
UPPER_OUT = os.path.join(BASE, "upper_pcb/gerbers")
os.makedirs(UPPER_OUT, exist_ok=True)

UBX, UBY = 100.0, 100.0
UR = 27.0

sw4x, sw4y = UBX - 10.0, UBY - 12.0
sw5x, sw5y = UBX + 10.0, UBY - 12.0
sw6x, sw6y = UBX - 22.0, UBY
sw7x, sw7y = UBX + 22.0, UBY
fpc2_x, fpc2_y = UBX, UBY + 15.0

edge2 = outline(UBX, UBY, UR, apt=10)
write_gerber(f"{UPPER_OUT}/upper_pcb-Edge_Cuts.gbr", [("Edge_Cuts", edge2)])

fcu2 = []
fcu2 += outline(UBX, UBY, UR-0.3, apt=10)

# H1/H2 mount holes
fcu2 += circ_pad(UBX-15, UBY, 4.4, 20)
fcu2 += circ_pad(UBX+15, UBY, 4.4, 21)

# SW4/SW5 Kailh GM 8.0 THT Cherry-MX (3-pin: NC, COM, NO)
apt = 30
fcu2.append(f"%ADD{apt}C,2.00*%")
fcu2.append(f"D{apt}*")
for sx,sy in [(sw4x,sw4y),(sw5x,sw5y)]:
    fcu2.append(f"X{int((sx-3.81)*1e6):+010d}Y{int(sy*1e6):+010d}D03*")   # NC
    fcu2.append(f"X{int(sx*1e6):+010d}Y{int((sy+3.81)*1e6):+010d}D03*")   # COM->GND
    fcu2.append(f"X{int((sx+3.81)*1e6):+010d}Y{int(sy*1e6):+010d}D03*")   # NO->signal

# SW6/SW7 Kailh Blue Dot SMD (2-pad 1.8x2.8mm, 5mm pitch)
apt = 31
fcu2.append(f"%ADD{apt}R,1.80X2.80*%")
fcu2.append(f"D{apt}*")
for sx,sy in [(sw6x,sw6y),(sw7x,sw7y)]:
    fcu2.append(f"X{int((sx-2.5)*1e6):+010d}Y{int(sy*1e6):+010d}D03*")   # GND
    fcu2.append(f"X{int((sx+2.5)*1e6):+010d}Y{int(sy*1e6):+010d}D03*")   # SIG

# J5 FPC 6-pin 0.5mm
apt = 32
fcu2.append(f"%ADD{apt}R,0.40X1.20*%")
fcu2.append(f"D{apt}*")
for i in range(6):
    fcu2.append(f"X{int((fpc2_x-1.25+i*0.5)*1e6):+010d}Y{int(fpc2_y*1e6):+010d}D03*")

# R1-R4 pull-ups + C1
apt = 40
fcu2.append(f"%ADD{apt}R,0.60X0.80*%")
fcu2.append(f"D{apt}*")
for px,py in [
    (sw4x-1, sw4y+6),(sw4x+1, sw4y+6),
    (sw5x-1, sw5y+6),(sw5x+1, sw5y+6),
    (sw6x+3, sw6y-3),(sw6x+5, sw6y-3),
    (sw7x-5, sw7y-3),(sw7x-3, sw7y-3),
    (UBX-1,  UBY+8), (UBX+1,  UBY+8),
]:
    fcu2.append(f"X{int(px*1e6):+010d}Y{int(py*1e6):+010d}D03*")

write_gerber(f"{UPPER_OUT}/upper_pcb-F_Cu.gbr", [("F.Cu", fcu2)])
write_gerber(f"{UPPER_OUT}/upper_pcb-B_Cu.gbr", [("B.Cu", outline(UBX,UBY,UR-0.3,apt=10))])
write_gerber(f"{UPPER_OUT}/upper_pcb-F_Mask.gbr", [("F.Mask", fcu2)])
write_gerber(f"{UPPER_OUT}/upper_pcb-B_Mask.gbr", [("B.Mask", outline(UBX,UBY,UR-0.3,apt=10))])

# Upper silk
silk2 = []
silk2.append("%ADD10C,0.15*%")
silk2 += silk_box(sw4x, sw4y, 14.0, 14.0)   # SW4 GM8.0 body
silk2 += silk_box(sw5x, sw5y, 14.0, 14.0)   # SW5 GM8.0 body
silk2 += silk_cross(sw4x, sw4y); silk2 += silk_cross(sw5x, sw5y)
silk2 += silk_box(sw6x, sw6y, 9.0, 9.0)     # SW6 Blue Dot
silk2 += silk_box(sw7x, sw7y, 9.0, 9.0)     # SW7 Blue Dot
silk2 += silk_pin1(sw4x-3.81, sw4y)          # pin1 NC marker SW4
silk2 += silk_pin1(sw5x-3.81, sw5y)          # pin1 NC marker SW5
# FPC outline + pin1
silk2 += silk_box(fpc2_x, fpc2_y, 5.0, 3.5)
silk2 += silk_pin1(fpc2_x-2.5, fpc2_y-1.0)
# FPC pin labels (tick marks)
for i in range(6):
    px2 = fpc2_x - 1.25 + i*0.5
    silk2 += silk_line(px2, fpc2_y+2, px2, fpc2_y+3.5)
# Mount holes
for hx2,hy2 in [(UBX-15,UBY),(UBX+15,UBY)]:
    silk2 += outline(hx2, hy2, 2.5, n=36, apt=10, apt_size=0.15)
# Orientation mark: north arrow
silk2 += silk_line(UBX, UBY-20, UBX, UBY-24)
silk2 += silk_line(UBX-1, UBY-23, UBX, UBY-25)
silk2 += silk_line(UBX+1, UBY-23, UBX, UBY-25)
# Pin labels near FPC
for i,(lbl) in enumerate(["1:3V3","2:GND","3:BTN_L","4:BTN_R","5:BTN_BK","6:BTN_FW"]):
    px2 = fpc2_x - 1.25 + i*0.5
    silk2 += silk_line(px2-0.3, fpc2_y-1.5, px2+0.3, fpc2_y-1.5)

write_gerber(f"{UPPER_OUT}/upper_pcb-F_SilkS.gbr", [("F.SilkS", silk2)])

# Upper drill
upper_holes = [(UBX-15, UBY, 2.2, True), (UBX+15, UBY, 2.2, True)]
for sx,sy in [(sw4x,sw4y),(sw5x,sw5y)]:
    upper_holes += [(sx-3.81, sy, 1.5, True), (sx, sy+3.81, 1.5, True), (sx+3.81, sy, 1.5, True)]

write_drill(f"{UPPER_OUT}/upper_pcb-PTH.drl", upper_holes)

print(f"\nUpper PCB gerbers -> {UPPER_OUT}/")
for f in sorted(os.listdir(UPPER_OUT)):
    print(f"  {f}")
print("\nDone.")
