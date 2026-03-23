#!/usr/bin/env python3
"""
Generate Gerber + drill files for DaPao Space Mouse PCBs.
Rev 2.0 Lower PCB layout:
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

def silk_label(cx, cy, text, apt=10, scale=0.7):
    """
    Render a text label using a simple 5x7 dot-matrix stroke font.
    Each character is drawn as line segments; label centered on (cx, cy).
    scale: mm per unit (0.7mm gives ~1mm char height)
    """
    # Minimal stroke font: uppercase + digits + common symbols
    # Each char: list of strokes [(x0,y0,x1,y1), ...] in a 4x6 grid
    FONT = {
        'A':[(0,6,2,0),(2,0,4,6),(1,3,3,3)],
        'B':[(0,0,0,6),(0,0,3,0),(0,3,3,3),(0,6,3,6),(3,0,4,1),(3,3,4,4),(3,1,3,3),(3,4,3,6)],
        'C':[(4,1,3,0),(3,0,1,0),(1,0,0,1),(0,1,0,5),(0,5,1,6),(1,6,3,6),(3,6,4,5)],
        'D':[(0,0,0,6),(0,0,2,0),(2,0,4,2),(4,2,4,4),(4,4,2,6),(2,6,0,6)],
        'E':[(0,0,0,6),(0,0,4,0),(0,3,3,3),(0,6,4,6)],
        'F':[(0,0,0,6),(0,0,4,0),(0,3,3,3)],
        'G':[(4,1,3,0),(3,0,1,0),(1,0,0,1),(0,1,0,5),(0,5,1,6),(1,6,3,6),(3,6,4,5),(4,5,4,3),(4,3,2,3)],
        'H':[(0,0,0,6),(4,0,4,6),(0,3,4,3)],
        'I':[(1,0,3,0),(2,0,2,6),(1,6,3,6)],
        'J':[(1,0,3,0),(3,0,3,5),(3,5,2,6),(2,6,1,6),(1,6,0,5)],
        'K':[(0,0,0,6),(0,3,4,0),(0,3,4,6)],
        'L':[(0,0,0,6),(0,6,4,6)],
        'M':[(0,6,0,0),(0,0,2,3),(2,3,4,0),(4,0,4,6)],
        'N':[(0,6,0,0),(0,0,4,6),(4,6,4,0)],
        'O':[(1,0,3,0),(3,0,4,1),(4,1,4,5),(4,5,3,6),(3,6,1,6),(1,6,0,5),(0,5,0,1),(0,1,1,0)],
        'P':[(0,0,0,6),(0,0,3,0),(3,0,4,1),(4,1,4,3),(4,3,3,3),(3,3,0,3)],
        'Q':[(1,0,3,0),(3,0,4,1),(4,1,4,5),(4,5,3,6),(3,6,1,6),(1,6,0,5),(0,5,0,1),(0,1,1,0),(3,4,4,6)],
        'R':[(0,0,0,6),(0,0,3,0),(3,0,4,1),(4,1,4,3),(4,3,3,3),(3,3,0,3),(2,3,4,6)],
        'S':[(4,1,3,0),(3,0,1,0),(1,0,0,1),(0,1,0,3),(0,3,4,3),(4,3,4,5),(4,5,3,6),(3,6,1,6),(1,6,0,5)],
        'T':[(0,0,4,0),(2,0,2,6)],
        'U':[(0,0,0,5),(0,5,1,6),(1,6,3,6),(3,6,4,5),(4,5,4,0)],
        'V':[(0,0,2,6),(2,6,4,0)],
        'W':[(0,0,1,6),(1,6,2,3),(2,3,3,6),(3,6,4,0)],
        'X':[(0,0,4,6),(4,0,0,6)],
        'Y':[(0,0,2,3),(4,0,2,3),(2,3,2,6)],
        'Z':[(0,0,4,0),(4,0,0,6),(0,6,4,6)],
        '0':[(1,0,3,0),(3,0,4,1),(4,1,4,5),(4,5,3,6),(3,6,1,6),(1,6,0,5),(0,5,0,1),(0,1,1,0),(1,1,3,5)],
        '1':[(1,1,2,0),(2,0,2,6),(1,6,3,6)],
        '2':[(0,1,1,0),(1,0,3,0),(3,0,4,1),(4,1,4,3),(4,3,0,6),(0,6,4,6)],
        '3':[(0,1,1,0),(1,0,3,0),(3,0,4,1),(4,1,4,2),(4,2,2,3),(2,3,4,4),(4,4,4,5),(4,5,3,6),(3,6,1,6),(1,6,0,5)],
        '4':[(3,0,0,4),(0,4,4,4),(4,4,4,0),(4,4,4,6)],
        '5':[(4,0,0,0),(0,0,0,3),(0,3,3,3),(3,3,4,4),(4,4,4,5),(4,5,3,6),(3,6,1,6),(1,6,0,5)],
        '6':[(4,1,3,0),(3,0,1,0),(1,0,0,1),(0,1,0,5),(0,5,1,6),(1,6,3,6),(3,6,4,5),(4,5,4,3),(4,3,0,3)],
        '7':[(0,0,4,0),(4,0,2,6)],
        '8':[(1,0,3,0),(3,0,4,1),(4,1,4,2),(4,2,3,3),(3,3,4,4),(4,4,4,5),(4,5,3,6),(3,6,1,6),(1,6,0,5),(0,5,0,4),(0,4,1,3),(1,3,0,2),(0,2,0,1),(0,1,1,0)],
        '9':[(4,3,0,3),(0,3,0,1),(0,1,1,0),(1,0,3,0),(3,0,4,1),(4,1,4,5),(4,5,3,6),(3,6,1,6),(1,6,0,5)],
        '-':[(0,3,4,3)],
        '_':[(0,6,4,6)],
        '/':[(4,0,0,6)],
        '.':[(1,5,1,6),(2,5,2,6)],
        ':':[(1,1,2,1),(1,4,2,4)],
        '+':[(2,1,2,5),(0,3,4,3)],
        ' ':[], '#':[(1,0,1,6),(3,0,3,6),(0,2,4,2),(0,4,4,4)],
    }
    chars = text.upper()
    char_w = 4 * scale
    spacing = 1.2 * scale
    total_w = len(chars) * (char_w + spacing) - spacing
    start_x = cx - total_w/2
    cmds = [f"D{apt}*"]
    for ci, ch in enumerate(chars):
        ox = start_x + ci * (char_w + spacing)
        oy = cy - 3 * scale  # center vertically (char height = 6 units)
        strokes = FONT.get(ch, [])
        for x0,y0,x1,y1 in strokes:
            ax = ox + x0*scale; ay = oy + y0*scale
            bx2 = ox + x1*scale; by2 = oy + y1*scale
            cmds.append(f"X{int(ax*1e6):+010d}Y{int(ay*1e6):+010d}D02*")
            cmds.append(f"X{int(bx2*1e6):+010d}Y{int(by2*1e6):+010d}D01*")
    return cmds

# ================================================================
# LOWER PCB  dia88mm  rev 1.3 layout
# ================================================================
LOWER_OUT = os.path.join(BASE, "lower_pcb/gerbers")
os.makedirs(LOWER_OUT, exist_ok=True)

BX, BY = 100.0, 100.0   # board center
OR = 44.0                # outer radius
# NOTE: NO center cutout - joystick module mounts on PCB surface

# ---- Key component centers ----
# North = lower Y
XIAO_X,  XIAO_Y  = BX,       BY - 30.0   # U1 XIAO center (100, 70)
USBC_X,  USBC_Y  = BX,       BY - 43.0   # J1 USB-C at north edge (100, 57)
JOY_X,   JOY_Y   = BX,       BY          # J4 Joystick at center (100, 100)
FPC_X,   FPC_Y   = BX,       BY + 17.0   # J3 FPC (100, 117) - between joystick and battery row
# U2 TP4056 REMOVED - XIAO handles charging internally
# U4 USBLC6 REMOVED - XIAO handles USB ESD internally
LDO_X,   LDO_Y   = BX + 18,  BY -  5.0   # U3 LDO    (118, 95) - powers peripherals
BAT_X,   BAT_Y   = BX - 8,   BY + 15.0   # J2 Battery -- B.Cu (underside), SW quadrant
SW1_X,   SW1_Y   = BX - 42,  BY          # SW1 Power west edge (58, 100)
SWBT_X,  SWBT_Y  = BX,       BY + 40.0   # SW_BT south edge

# M2 mounting holes at 45/135/225/315 deg, R=36mm
MH_R = 36.0
MH_ANGLES = [45, 135, 225, 315]
mount_holes = [(BX + MH_R*math.cos(math.radians(a)),
                BY + MH_R*math.sin(math.radians(a))) for a in MH_ANGLES]

# ================================================================
#  Edge.Cuts  — circular board only, NO center hole
# ================================================================
edge = outline(BX, BY, OR, apt=10)
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

# --- J4 Alps RKJXV1224005 (direct THT solder, board center) ---
# Body: 18.2 x 21.7mm. 10 pins total:
# Signal pins (1.0mm drill, 1.8mm pad):
#   X-axis: CCW at (-6.4, -7.0), Wiper at (-3.0, -7.0), CW at (+0.4, -7.0)
#   Y-axis: CCW at (-6.4, +7.0), Wiper at (-3.0, +7.0), CW at (+0.4, +7.0)  [approx from Alps datasheet]
#   SW pins: (+3.8, -5.0) and (+3.8, +5.0)
# Mounting legs (1.5mm drill, 2.5mm pad, tie to GND):
#   (-7.7, -8.8), (+7.7, -8.8), (-7.7, +8.8), (+7.7, +8.8)
apt = 33
fcu.append(f"%ADD{apt}C,1.80*%")
fcu.append(f"D{apt}*")
# X-axis pins
for px in [-6.4, -3.0, 0.4]:
    fcu.append(f"X{int((JOY_X+px)*1e6):+010d}Y{int((JOY_Y-7.0)*1e6):+010d}D03*")
# Y-axis pins
for px in [-6.4, -3.0, 0.4]:
    fcu.append(f"X{int((JOY_X+px)*1e6):+010d}Y{int((JOY_Y+7.0)*1e6):+010d}D03*")
# SW pins
for py in [-5.0, 5.0]:
    fcu.append(f"X{int((JOY_X+3.8)*1e6):+010d}Y{int((JOY_Y+py)*1e6):+010d}D03*")
# Mounting legs (GND, 2.5mm pad)
apt = 34
fcu.append(f"%ADD{apt}C,2.50*%")
fcu.append(f"D{apt}*")
for mx,my in [(-7.7,-8.8),(7.7,-8.8),(-7.7,8.8),(7.7,8.8)]:
    fcu.append(f"X{int((JOY_X+mx)*1e6):+010d}Y{int((JOY_Y+my)*1e6):+010d}D03*")

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

# U2 TP4056 REMOVED

# --- U3 AP2112K LDO SOT-23-5 (east) ---
apt = 37
fcu.append(f"%ADD{apt}R,0.55X1.00*%")
fcu.append(f"D{apt}*")
for i,dx in enumerate([-0.95, 0, 0.95]):
    fcu.append(f"X{int((LDO_X+dx)*1e6):+010d}Y{int((LDO_Y+1.4)*1e6):+010d}D03*")
for dx in [-0.95, 0.95]:
    fcu.append(f"X{int((LDO_X+dx)*1e6):+010d}Y{int((LDO_Y-1.4)*1e6):+010d}D03*")

# U4 USBLC6 REMOVED

# J2 JST-PH battery -- placed on B.Cu (underside), added to bcu below

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
    # R_PU5: JOY_SW pull-up (GPIO3), near J4 joystick NE
    (JOY_X+8, JOY_Y-8), (JOY_X+10, JOY_Y-8),
    # R_PU_BT: BT sync pull-up (GPIO9), near SW_BT
    (SWBT_X+4, SWBT_Y-4), (SWBT_X+6, SWBT_Y-4),
    # R10/R11: USB-C CC1/CC2 (5.1k), near J1
    (USBC_X+5, USBC_Y+3), (USBC_X+5, USBC_Y+5),
    # C1-C3: 100nF 0402 decoupling on 3V3 near U1
    (XIAO_X-6, XIAO_Y+12),(XIAO_X-4, XIAO_Y+12),(XIAO_X-2, XIAO_Y+12),
    # REMOVED: R5/R6 VBAT divider (GPIO10/ADC_BAT onboard on XIAO)
    # REMOVED: R7/R8/R9 TP4056 resistors (U2 removed)
    # REMOVED: C6 VBUS bulk (XIAO handles internally)
]
for px,py in passives_0402:
    fcu.append(f"X{int(px*1e6):+010d}Y{int(py*1e6):+010d}D03*")

# 0805 bulk caps
apt = 51
fcu.append(f"%ADD{apt}R,2.00X1.25*%")
fcu.append(f"D{apt}*")
# C4: 10uF bulk 3V3, near U3
fcu.append(f"X{int((LDO_X+5)*1e6):+010d}Y{int((LDO_Y+2)*1e6):+010d}D03*")
# C5: 10uF bulk BAT+, near J2 (on B.Cu since J2 is on bottom)
# LEDs REMOVED (U2 TP4056 gone; XIAO has its own charge LED onboard)

write_gerber(f"{LOWER_OUT}/lower_pcb-F_Cu.gbr", [("F.Cu", fcu)])

# B.Cu — ground plane + J2 battery connector (bottom-mount)
bcu = outline(BX, BY, OR-0.3, apt=10)
# J2 JST-PH 2-pin on bottom of board (battery hangs below)
bcu.append(f"%ADD60C,2.00*%")
bcu.append(f"D60*")
for dx in [-1.0, 1.0]:
    bcu.append(f"X{int((BAT_X+dx)*1e6):+010d}Y{int(BAT_Y*1e6):+010d}D03*")
# C5: 10uF bulk BAT+ on bottom near J2
bcu.append(f"%ADD61R,2.00X1.25*%")
bcu.append(f"D61*")
bcu.append(f"X{int((BAT_X+4)*1e6):+010d}Y{int((BAT_Y-3)*1e6):+010d}D03*")

write_gerber(f"{LOWER_OUT}/lower_pcb-B_Cu.gbr", [("B.Cu", bcu)])

# Mask layers
write_gerber(f"{LOWER_OUT}/lower_pcb-F_Mask.gbr", [("F.Mask", fcu)])
write_gerber(f"{LOWER_OUT}/lower_pcb-B_Mask.gbr", [("B.Mask", bcu)])

# ================================================================
#  F.SilkS — component outlines + ref designators + net labels
# ================================================================
silk = []
# Aperture for silkscreen lines (0.15mm)
silk.append("%ADD10C,0.15*%")
silk.append("%ADD12C,0.12*%")  # thinner for small text

# Label hierarchy: REF=0.50, name=0.36, net/pin=0.22

# ---- U1 XIAO ESP32-S3 ----
silk += silk_box(XIAO_X, XIAO_Y, 17.5, 21.0)
silk += silk_cross(XIAO_X, XIAO_Y)
# Ref + name above box (north, outside)
silk += silk_label(XIAO_X, XIAO_Y-13.5, "U1", scale=0.50)
silk += silk_label(XIAO_X, XIAO_Y-11.8, "XIAO-S3", scale=0.36)
# Left side: tick + net name, compact spacing
for i, net in enumerate(["3V3","GND","JOY-X","JOY-Y","JOY-SW","ADC-BAT","GND"]):
    py = XIAO_Y - 9.0 + i*3.0
    silk += silk_line(XIAO_X-8.75, py, XIAO_X-9.8, py)
    silk += silk_label(XIAO_X-11.0, py-1.0, net, scale=0.22)
# Right side GPIO net names
for i, net in enumerate(["BTN-L","BTN-R","BTN-BK","BTN-FW","BT-SYN","3V3","GND"]):
    py = XIAO_Y - 9.0 + i*3.0
    silk += silk_line(XIAO_X+8.75, py, XIAO_X+9.8, py)
    silk += silk_label(XIAO_X+11.0, py-1.0, net, scale=0.22)

# ---- J1 USB-C ----
silk += silk_box(USBC_X, USBC_Y, 9.0, 3.5)
silk += silk_label(USBC_X, USBC_Y+2.8, "J1", scale=0.50)
silk += silk_label(USBC_X, USBC_Y+4.2, "USB-C", scale=0.36)
# Small north arrow
silk += silk_line(USBC_X, USBC_Y-2.5, USBC_X, USBC_Y-4.0)
silk += silk_line(USBC_X-0.6, USBC_Y-3.3, USBC_X, USBC_Y-4.0)
silk += silk_line(USBC_X+0.6, USBC_Y-3.3, USBC_X, USBC_Y-4.0)

# ---- J4 Alps RKJXV1224005 ----
silk += silk_box(JOY_X, JOY_Y, 18.2, 21.7)
silk += silk_cross(JOY_X, JOY_Y, 2.5)
silk += silk_label(JOY_X, JOY_Y-2.5, "J4", scale=0.50)
silk += silk_label(JOY_X, JOY_Y-0.8, "ALPS-JOY", scale=0.36)
# X-axis row (south side of component)
silk += silk_label(JOY_X-6.4, JOY_Y-9.5, "3V3", scale=0.22)
silk += silk_label(JOY_X-3.0, JOY_Y-9.5, "X", scale=0.22)
silk += silk_label(JOY_X+0.4, JOY_Y-9.5, "GND", scale=0.22)
silk += silk_label(JOY_X-3.0, JOY_Y-11.2, "X-AXIS", scale=0.22)
# Y-axis row (north side)
silk += silk_label(JOY_X-6.4, JOY_Y+9.0, "3V3", scale=0.22)
silk += silk_label(JOY_X-3.0, JOY_Y+9.0, "Y", scale=0.22)
silk += silk_label(JOY_X+0.4, JOY_Y+9.0, "GND", scale=0.22)
silk += silk_label(JOY_X-3.0, JOY_Y+10.7, "Y-AXIS", scale=0.22)
# SW pins (east side)
silk += silk_label(JOY_X+6.5, JOY_Y-5.0, "SW", scale=0.22)
silk += silk_label(JOY_X+6.5, JOY_Y+5.0, "GND", scale=0.22)
# Mounting leg markers (small cross only)
for mx,my in [(-7.7,-8.8),(7.7,-8.8),(-7.7,8.8),(7.7,8.8)]:
    silk += silk_cross(JOY_X+mx, JOY_Y+my, 0.8)

# ---- J3 FPC ----
silk += silk_box(FPC_X, FPC_Y, 5.5, 3.5)
silk += silk_pin1(FPC_X-2.75, FPC_Y-1.0)
silk += silk_label(FPC_X, FPC_Y+3.0, "J3", scale=0.50)
silk += silk_label(FPC_X, FPC_Y+4.5, "FPC UP", scale=0.36)
# Pin numbers only (too small for net names at 0.5mm pitch)
for i in range(6):
    px = FPC_X - 1.25 + i*0.5
    silk += silk_label(px, FPC_Y+2.0, str(i+1), scale=0.20)

# ---- U3 LDO ----
silk += silk_box(LDO_X, LDO_Y, 3.5, 3.5)
silk += silk_pin1(LDO_X-1.75, LDO_Y-1.75)
silk += silk_label(LDO_X, LDO_Y-3.8, "U3", scale=0.50)
silk += silk_label(LDO_X, LDO_Y-2.4, "LDO", scale=0.36)

# J2 battery is on B.Cu (underside) -- silk goes on B.SilkS, not here

# ---- SW1 Power ----
silk += silk_box(SW1_X+2.0, SW1_Y, 8.0, 5.5)
silk += silk_label(SW1_X+2.0, SW1_Y-5.5, "SW1", scale=0.50)
silk += silk_label(SW1_X+2.0, SW1_Y-3.8, "PWR", scale=0.36)

# ---- SW_BT Bluetooth ----
silk += silk_box(SWBT_X, SWBT_Y, 5.0, 4.0)
silk += silk_label(SWBT_X, SWBT_Y+3.2, "SW-BT", scale=0.50)
silk += silk_label(SWBT_X, SWBT_Y+4.8, "G9-SYNC", scale=0.36)

# ---- SW2 BOOT / SW3 RESET ----
silk += silk_box(XIAO_X+12, XIAO_Y-4, 4.5, 3.5)
silk += silk_label(XIAO_X+12, XIAO_Y-7.8, "SW2", scale=0.50)
silk += silk_label(XIAO_X+12, XIAO_Y-6.2, "BOOT", scale=0.36)
silk += silk_box(XIAO_X+12, XIAO_Y+4, 4.5, 3.5)
silk += silk_label(XIAO_X+12, XIAO_Y+6.2, "SW3", scale=0.50)
silk += silk_label(XIAO_X+12, XIAO_Y+7.8, "RST", scale=0.36)

# ---- Mounting holes ----
for hx,hy in mount_holes:
    silk += outline(hx, hy, 2.5, n=36, apt=10, apt_size=0.15)
    silk += silk_label(hx, hy+3.2, "M2", scale=0.22)

# ---- Board orientation + title ----
silk += silk_line(BX, BY-37, BX, BY-41)
silk += silk_line(BX-0.8, BY-40.2, BX, BY-41.5)
silk += silk_line(BX+0.8, BY-40.2, BX, BY-41.5)
silk += silk_label(BX, BY-43, "FWD", scale=0.36)
silk += silk_label(BX, BY+35, "DAPAO LOWER R2.4", scale=0.36)

write_gerber(f"{LOWER_OUT}/lower_pcb-F_SilkS.gbr", [("F.SilkS", silk)])

# B.SilkS — labels for bottom-mounted components
bsilk = []
bsilk.append("%ADD10C,0.15*%")
bsilk += silk_box(BAT_X, BAT_Y, 9.0, 6.0)
bsilk += silk_pin1(BAT_X-4.5, BAT_Y-3.0)
bsilk += silk_label(BAT_X, BAT_Y-5.5, "J2", scale=0.50)
bsilk += silk_label(BAT_X, BAT_Y-3.8, "LIPO", scale=0.36)
bsilk += silk_label(BAT_X-2.0, BAT_Y+0.5, "+", scale=0.40)
bsilk += silk_label(BAT_X+2.0, BAT_Y+0.5, "-", scale=0.40)
bsilk += silk_label(BAT_X, BAT_Y+5.5, "BOTTOM MOUNT", scale=0.28)
write_gerber(f"{LOWER_OUT}/lower_pcb-B_SilkS.gbr", [("B.SilkS", bsilk)])

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

# J4 Alps RKJXV THT signal pins (1.0mm drill, 8 pins)
for px in [-6.4, -3.0, 0.4]:
    lower_holes.append((JOY_X+px, JOY_Y-7.0, 1.0, True))   # X-axis
    lower_holes.append((JOY_X+px, JOY_Y+7.0, 1.0, True))   # Y-axis
for py in [-5.0, 5.0]:
    lower_holes.append((JOY_X+3.8, JOY_Y+py, 1.0, True))   # SW
# Mounting legs (1.5mm drill, 4 legs, plated)
for mx,my in [(-7.7,-8.8),(7.7,-8.8),(-7.7,8.8),(7.7,8.8)]:
    lower_holes.append((JOY_X+mx, JOY_Y+my, 1.5, True))

# J2 JST-PH through-hole (bottom mount, drilled through from B.Cu)
lower_holes += [(BAT_X-1.0, BAT_Y, 1.0, True), (BAT_X+1.0, BAT_Y, 1.0, True)]

# No center NPTH — joystick module sits on PCB surface

write_drill(f"{LOWER_OUT}/lower_pcb-PTH.drl",  [(x,y,d,p) for x,y,d,p in lower_holes if p])
# NPTH file still written but empty (JLCPCB requires it)
write_drill(f"{LOWER_OUT}/lower_pcb-NPTH.drl", [])

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
fpc2_x, fpc2_y = UBX, UBY + 8.0    # J5 FPC on B.Cu (underside), center-south area

edge2 = outline(UBX, UBY, UR, apt=10)
write_gerber(f"{UPPER_OUT}/upper_pcb-Edge_Cuts.gbr", [("Edge_Cuts", edge2)])

fcu2 = []
fcu2 += outline(UBX, UBY, UR-0.3, apt=10)

# H1/H2 mount holes
fcu2 += circ_pad(UBX-15, UBY, 4.4, 20)
fcu2 += circ_pad(UBX+15, UBY, 4.4, 21)

# SW4/SW5 Kailh GM 8.0 mouse microswitch (CORRECTED footprint)
# 3 pins horizontal row, 5.08mm pitch (matches Omron D2FC-F-7N standard)
# NO(-5.08,0) -- COM(0,0) -- NC(+5.08,0)
# Drill 1.0mm, pad 1.8mm
apt = 30
fcu2.append(f"%ADD{apt}C,1.80*%")
fcu2.append(f"D{apt}*")
for sx,sy in [(sw4x,sw4y),(sw5x,sw5y)]:
    fcu2.append(f"X{int((sx-5.08)*1e6):+010d}Y{int(sy*1e6):+010d}D03*")   # NO -> BTN signal
    fcu2.append(f"X{int(sx*1e6):+010d}Y{int(sy*1e6):+010d}D03*")           # COM -> GND
    fcu2.append(f"X{int((sx+5.08)*1e6):+010d}Y{int(sy*1e6):+010d}D03*")   # NC -> float/GND

# SW6/SW7 Kailh Blue Dot SMD (2-pad 1.8x2.8mm, 5mm pitch)
apt = 31
fcu2.append(f"%ADD{apt}R,1.80X2.80*%")
fcu2.append(f"D{apt}*")
for sx,sy in [(sw6x,sw6y),(sw7x,sw7y)]:
    fcu2.append(f"X{int((sx-2.5)*1e6):+010d}Y{int(sy*1e6):+010d}D03*")   # GND
    fcu2.append(f"X{int((sx+2.5)*1e6):+010d}Y{int(sy*1e6):+010d}D03*")   # SIG

# J5 FPC -- on B.Cu (bottom of upper PCB), added to bcu2 below

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

# B.Cu — ground plane + J5 FPC on bottom of upper PCB
bcu2 = outline(UBX, UBY, UR-0.3, apt=10)
bcu2.append(f"%ADD60R,0.40X1.20*%")
bcu2.append(f"D60*")
for i in range(6):
    bcu2.append(f"X{int((fpc2_x-1.25+i*0.5)*1e6):+010d}Y{int(fpc2_y*1e6):+010d}D03*")
# FPC latch pads
bcu2.append(f"%ADD61R,1.20X1.80*%")
bcu2.append(f"D61*")
for dx in [-2.5, 2.5]:
    bcu2.append(f"X{int((fpc2_x+dx)*1e6):+010d}Y{int((fpc2_y+0.8)*1e6):+010d}D03*")

write_gerber(f"{UPPER_OUT}/upper_pcb-B_Cu.gbr", [("B.Cu", bcu2)])
write_gerber(f"{UPPER_OUT}/upper_pcb-F_Mask.gbr", [("F.Mask", fcu2)])
write_gerber(f"{UPPER_OUT}/upper_pcb-B_Mask.gbr", [("B.Mask", bcu2)])

# Upper silk
silk2 = []
silk2.append("%ADD10C,0.15*%")

# Label hierarchy: REF=0.50, name=0.36, net/pin=0.22

# SW4/SW5 GM 8.0 (corrected: 3 pins horizontal, 5.08mm pitch)
for sx,sy,lbl,func in [(sw4x,sw4y,"SW4","L-CLK"),(sw5x,sw5y,"SW5","R-CLK")]:
    # Body outline 12.8x5.8mm, centered on COM pin at (sx,sy)
    silk2 += silk_box(sx, sy, 12.8, 5.8)
    silk2 += silk_cross(sx, sy)
    silk2 += silk_pin1(sx-5.08, sy)  # pin1 marker at NO pin
    silk2 += silk_label(sx, sy-5.5, lbl, scale=0.50)
    silk2 += silk_label(sx, sy-4.0, "GM8.0", scale=0.36)
    silk2 += silk_label(sx, sy-2.8, func, scale=0.36)
    # Pin labels: NO=BTN, COM=GND, NC=NC
    silk2 += silk_label(sx-5.08, sy+4.0, "NO-SIG", scale=0.22)
    silk2 += silk_label(sx,      sy+4.0, "COM-GND", scale=0.22)
    silk2 += silk_label(sx+5.08, sy+4.0, "NC", scale=0.22)
    silk2 += silk_label(sx+3.81, sy+8.2, "SIG", scale=0.22)

# SW6/SW7 Blue Dot SMD
for sx,sy,lbl,func,arrow_dir in [
    (sw6x, sw6y, "SW6", "BACK",  -1),
    (sw7x, sw7y, "SW7", "FWD",   +1)
]:
    silk2 += silk_box(sx, sy, 9.0, 9.0)
    silk2 += silk_label(sx, sy-6.2, lbl, scale=0.50)
    silk2 += silk_label(sx, sy-4.6, func, scale=0.36)
    # Plunger arrow (short)
    silk2 += silk_line(sx, sy, sx + arrow_dir*4, sy)
    silk2 += silk_line(sx+arrow_dir*4, sy, sx+arrow_dir*3, sy-0.6)
    silk2 += silk_line(sx+arrow_dir*4, sy, sx+arrow_dir*3, sy+0.6)
    # Pad net labels
    silk2 += silk_label(sx-2.5, sy+5.8, "GND", scale=0.22)
    silk2 += silk_label(sx+2.5, sy+5.8, "SIG", scale=0.22)

# J5 FPC is on B.Cu (underside) -- label goes on B.SilkS only

# R1-R4 + C1 — compact ref only
for ref,px2,py2 in [
    ("R1", sw4x-1, sw4y+6.5), ("R2", sw5x-1, sw5y+6.5),
    ("R3", sw6x+4, sw6y-3.5), ("R4", sw7x-4, sw7y-3.5),
    ("C1", UBX,    UBY+8.5),
]:
    silk2 += silk_label(px2, py2, ref, scale=0.28)

# H1/H2 mount holes
for hx2,hy2,lbl in [(UBX-15,UBY,"H1"),(UBX+15,UBY,"H2")]:
    silk2 += outline(hx2, hy2, 2.5, n=36, apt=10, apt_size=0.15)
    silk2 += silk_label(hx2, hy2+3.2, lbl, scale=0.28)

# North arrow + board title
silk2 += silk_line(UBX, UBY-20, UBX, UBY-23)
silk2 += silk_line(UBX-0.8, UBY-22.3, UBX, UBY-23.5)
silk2 += silk_line(UBX+0.8, UBY-22.3, UBX, UBY-23.5)
silk2 += silk_label(UBX, UBY-25, "FWD", scale=0.36)
silk2 += silk_label(UBX, UBY+18, "DAPAO UPPER R1.6", scale=0.36)

write_gerber(f"{UPPER_OUT}/upper_pcb-F_SilkS.gbr", [("F.SilkS", silk2)])

# B.SilkS — J5 FPC label on underside
bsilk2 = []
bsilk2.append("%ADD10C,0.15*%")
bsilk2 += silk_box(fpc2_x, fpc2_y, 5.5, 3.5)
bsilk2 += silk_pin1(fpc2_x-2.75, fpc2_y-1.0)
bsilk2 += silk_label(fpc2_x, fpc2_y+3.0, "J5", scale=0.50)
bsilk2 += silk_label(fpc2_x, fpc2_y+4.5, "FPC-DN", scale=0.36)
for i in range(6):
    px2 = fpc2_x - 1.25 + i*0.5
    bsilk2 += silk_label(px2, fpc2_y+2.0, str(i+1), scale=0.20)
bsilk2 += silk_label(fpc2_x, fpc2_y-3.5, "BOTTOM MOUNT", scale=0.28)
write_gerber(f"{UPPER_OUT}/upper_pcb-B_SilkS.gbr", [("B.SilkS", bsilk2)])

# Upper drill
upper_holes = [(UBX-15, UBY, 2.2, True), (UBX+15, UBY, 2.2, True)]
for sx,sy in [(sw4x,sw4y),(sw5x,sw5y)]:
    upper_holes += [(sx-5.08, sy, 1.0, True), (sx, sy, 1.0, True), (sx+5.08, sy, 1.0, True)]

write_drill(f"{UPPER_OUT}/upper_pcb-PTH.drl", upper_holes)

print(f"\nUpper PCB gerbers -> {UPPER_OUT}/")
for f in sorted(os.listdir(UPPER_OUT)):
    print(f"  {f}")
print("\nDone.")
