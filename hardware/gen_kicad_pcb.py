#!/usr/bin/env python3
"""
Generate KiCad 7 .kicad_pcb files for DaPao Space Mouse.
Lower PCB rev 3.0 + Upper PCB rev 1.9
Using Seeed XIAO ESP32-S3 (Sense) module.

KEY DESIGN DECISIONS (Seeed XIAO ESP32-S3):
  - Built-in USB-C, 3.3V LDO (1A), LiPo charger (SGM40567), BOOT+RESET buttons
  - NO external USB-C, LDO, or power switch needed on this board
  - LiPo connects directly to XIAO VBAT back pad via JST-PH J2
  - XIAO 3V3 output (right pad 7) powers joystick and pull-ups
  - 7 castellated pads per side, 2.54mm pitch

XIAO ESP32-S3 PINOUT (USB-C at top/north):
  Left L1-L7 (top→bot): VBUS, GND, D0/A0, D1/A1, D2/A2, D3/A3, D4/SDA
  Right R1-R7 (top→bot): D5/SCL, D6/TX, D7/RX, D8/SCK, D9/MISO, D10/MOSI, 3V3
  Back pads: GND, VBAT (LiPo positive)

GPIO ASSIGNMENTS:
  D0/A0 (GPIO1)  → JOY_X  (analog)
  D1/A1 (GPIO2)  → JOY_Y  (analog)
  D2/A2 (GPIO3)  → JOY_SW (digital, pull-up)
  D3/A3 (GPIO4)  → ADC_BAT (analog, battery voltage divider)
  D4/SDA (GPIO5) → BTN_L
  D5/SCL (GPIO6) → BTN_R
  D6/TX  (GPIO43)→ BTN_BK
  D7/RX  (GPIO44)→ BTN_FW
  D8/SCK (GPIO7) → BT_SYNC
"""
import math, os

BASE = os.path.dirname(os.path.abspath(__file__))

# ================================================================
# KiCad S-expression helpers
# ================================================================
def pcb_header(thickness=1.6):
    return f"""(kicad_pcb
  (version 20221018)
  (generator pcbnew)
  (general (thickness {thickness}))
  (paper "A3")
  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (36 "B.SilkS" user "B.Silkscreen")
    (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (44 "Edge.Cuts" user)
    (46 "B.CrtYd" user "B.Courtyard")
    (47 "F.CrtYd" user "F.Courtyard")
  )
  (setup
    (pad_to_mask_clearance 0.05)
    (pcbplotparams (layerselection 0x00010fc_ffffffff))
  )"""

def net_defs(nets):
    out = ['  (net 0 "")']
    for i, n in enumerate(nets, 1):
        out.append(f'  (net {i} "{n}")')
    return "\n".join(out)

def net_idx(nets, name):
    if not name:
        return 0
    return nets.index(name) + 1

def pad_smd(x, y, w, h, net_n, layer="F.Cu", num="1"):
    mask = layer.replace("Cu", "Mask")
    return f"""    (pad "{num}" smd rect (at {x:.4f} {y:.4f}) (size {w:.4f} {h:.4f})
      (layers "{layer}" "{mask}") (net {net_n[0]} "{net_n[1]}"))"""

def pad_thru(x, y, drill, pad_d, net_n, num="1", shape="circle"):
    return f"""    (pad "{num}" thru_hole {shape} (at {x:.4f} {y:.4f}) (size {pad_d:.4f} {pad_d:.4f})
      (drill {drill:.4f}) (layers "*.Cu" "*.Mask") (net {net_n[0]} "{net_n[1]}"))"""

def pad_np(x, y, drill):
    return f"""    (pad "" np_thru_hole circle (at {x:.4f} {y:.4f}) (size {drill:.4f} {drill:.4f})
      (drill {drill:.4f}) (layers "*.Cu"))"""

def fp(ref, x, y, layer, angle, pads, fab_text=""):
    pstr = "\n".join(pads)
    ref_layer = "F.SilkS" if "F" in layer else "B.SilkS"
    return f"""  (footprint "{ref}" (layer "{layer}") (at {x:.4f} {y:.4f} {angle})
    (fp_text reference "{ref}" (at 0 -3) (layer "{ref_layer}") (effects (font (size 0.8 0.8) (thickness 0.15))))
    (fp_text value "{fab_text}" (at 0 3) (layer "F.Fab") hide)
{pstr}
  )"""

def circle_outline(cx, cy, r, layer="Edge.Cuts", width=0.05):
    return f'  (gr_circle (center {cx:.4f} {cy:.4f}) (end {cx+r:.4f} {cy:.4f}) (layer "{layer}") (width {width:.3f}))'

def silk_text(text, x, y, layer="F.SilkS", size=0.8, thickness=0.15, angle=0):
    return f'  (gr_text "{text}" (at {x:.4f} {y:.4f} {angle}) (layer "{layer}") (effects (font (size {size} {size}) (thickness {thickness}))))'

def seg(x1, y1, x2, y2, net_n, layer="F.Cu", width=0.25):
    return f'  (segment (start {x1:.4f} {y1:.4f}) (end {x2:.4f} {y2:.4f}) (width {width:.4f}) (layer "{layer}") (net {net_n}))'

# ================================================================
# LOWER PCB
# ================================================================
OUT_L = os.path.join(BASE, "lower_pcb/lower_pcb.kicad_pcb")

# Net list — XIAO handles USB-C, LDO (3V3), and LiPo charging internally
L_NETS = [
    "GND", "3V3", "VBAT",
    "JOY_X", "JOY_Y", "JOY_SW",
    "ADC_BAT",
    "BTN_L", "BTN_R", "BTN_BK", "BTN_FW",
    "BT_SYNC",
]
def ln(name): return (net_idx(L_NETS, name), name)

# Board center
BX, BY = 100.0, 100.0
OR = 44.0  # 88mm diameter board

# Component positions (all in mm)
XIAO_X, XIAO_Y = BX, BY - 30.0          # XIAO module centre (USB-C at top/north)
JOY_X,  JOY_Y  = BX, BY                 # Alps RKJXV joystick
FPC3_X, FPC3_Y = BX, BY + 17.0          # FPC connector to upper PCB
BAT_X,  BAT_Y  = BX - 8, BY + 15.0     # JST-PH LiPo connector
SWBT_X, SWBT_Y = BX, BY + 40.0         # BT sync button
MH_R = 36.0                              # mounting hole radius

footprints_lower = []

# ---------------------------------------------------------------
# U1  Seeed XIAO ESP32-S3 (Sense) castellated module
# ---------------------------------------------------------------
# 7 pads left + 7 pads right, 2.54 mm pitch
# Origin at module centre; USB-C end points NORTH (negative Y in KiCad)
# Pad pitch 2.54 mm; half-span = 3 * 2.54 = 7.62 → y_top = -7.62 (pin 1 = northernmost)
#
# L1 (y=-7.62): VBUS   — USB 5V (from XIAO USB-C)
# L2 (y=-5.08): GND
# L3 (y=-2.54): D0/A0  → JOY_X
# L4 (y= 0.00): D1/A1  → JOY_Y
# L5 (y=+2.54): D2/A2  → JOY_SW
# L6 (y=+5.08): D3/A3  → ADC_BAT
# L7 (y=+7.62): D4/SDA → BTN_L
#
# R1 (y=-7.62): D5/SCL → BTN_R
# R2 (y=-5.08): D6/TX  → BTN_BK
# R3 (y=-2.54): D7/RX  → BTN_FW
# R4 (y= 0.00): D8/SCK → BT_SYNC
# R5 (y=+2.54): D9/MISO → GND (unused)
# R6 (y=+5.08): D10/MOSI→ GND (unused)
# R7 (y=+7.62): 3V3    — 3.3V output (up to 1A)
#
# Back pad BP1: VBAT (LiPo +, connected to onboard charger)
# Back pad BP2: GND
xiao_nets_L = ["GND","GND","JOY_X","JOY_Y","JOY_SW","ADC_BAT","BTN_L"]
xiao_nets_R = ["BTN_R","BTN_BK","BTN_FW","BT_SYNC","GND","GND","3V3"]

xiao_pads = []
for i, net in enumerate(xiao_nets_L):
    py = -7.62 + i * 2.54
    xiao_pads.append(pad_smd(-8.75, py, 1.5, 2.0, ln(net), num=str(i + 1)))
for i, net in enumerate(xiao_nets_R):
    py = -7.62 + i * 2.54
    xiao_pads.append(pad_smd(8.75, py, 1.5, 2.0, ln(net), num=str(i + 8)))
# Back pads (on B.Cu face of the XIAO, accessible from underside)
xiao_pads.append(pad_smd(-2.5, 9.0, 2.5, 2.0, ln("VBAT"), layer="B.Cu", num="15"))
xiao_pads.append(pad_smd( 2.5, 9.0, 2.5, 2.0, ln("GND"),  layer="B.Cu", num="16"))

footprints_lower.append(fp("U1", XIAO_X, XIAO_Y, "F.Cu", 0, xiao_pads, "Seeed-XIAO-ESP32S3"))

# ---------------------------------------------------------------
# J4  Alps RKJXV1224005 dual-axis joystick with push-switch (THT)
# ---------------------------------------------------------------
# X-axis: CCW=3V3 at (-6.4,-7), Wiper=JOY_X at (-3.0,-7), CW=GND at (0.4,-7)
# Y-axis: CCW=3V3 at (-6.4,+7), Wiper=JOY_Y at (-3.0,+7), CW=GND at (0.4,+7)
# SW:     JOY_SW at (3.8,-5), GND at (3.8,+5)
# Mount legs (GND) at four corners
joy_pads = []
for i, (px, xnet, ynet) in enumerate([(-6.4,"3V3","3V3"), (-3.0,"JOY_X","JOY_Y"), (0.4,"GND","GND")]):
    joy_pads.append(pad_thru(px, -7.0, 1.0, 1.8, ln(xnet), num=str(i+1)))
    joy_pads.append(pad_thru(px, +7.0, 1.0, 1.8, ln(ynet), num=str(i+4)))
joy_pads.append(pad_thru(3.8, -5.0, 1.0, 1.8, ln("JOY_SW"), num="7"))
joy_pads.append(pad_thru(3.8, +5.0, 1.0, 1.8, ln("GND"),    num="8"))
for i, (mx, my) in enumerate([(-7.7,-8.8),(7.7,-8.8),(-7.7,8.8),(7.7,8.8)]):
    joy_pads.append(pad_thru(mx, my, 1.5, 2.5, ln("GND"), num=f"M{i+1}"))
footprints_lower.append(fp("J4", JOY_X, JOY_Y, "F.Cu", 0, joy_pads, "Alps-RKJXV"))

# ---------------------------------------------------------------
# J3  FPC 6-pin 0.5mm pitch — connects to upper PCB button ring
# ---------------------------------------------------------------
# Pin1=3V3, Pin2=GND, Pin3=BTN_L, Pin4=BTN_R, Pin5=BTN_BK, Pin6=BTN_FW
fpc3_nets = ["3V3","GND","BTN_L","BTN_R","BTN_BK","BTN_FW"]
fpc3_pads = []
for i, net in enumerate(fpc3_nets):
    px = -1.25 + i * 0.5
    fpc3_pads.append(pad_smd(px, 0, 0.4, 1.2, ln(net), num=str(i+1)))
fpc3_pads.append(pad_smd(-2.5, 0.8, 1.2, 1.8, ln("GND"), num="7"))  # latch
fpc3_pads.append(pad_smd( 2.5, 0.8, 1.2, 1.8, ln("GND"), num="8"))  # latch
footprints_lower.append(fp("J3", FPC3_X, FPC3_Y, "F.Cu", 0, fpc3_pads, "FPC-6P-0.5mm"))

# ---------------------------------------------------------------
# J2  JST-PH 2-pin — LiPo battery connector
# ---------------------------------------------------------------
# Routes directly to XIAO VBAT back pad
bat_pads = [
    pad_thru(-1.0, 0, 1.0, 1.8, ln("VBAT"), num="1"),
    pad_thru( 1.0, 0, 1.0, 1.8, ln("GND"),  num="2"),
]
footprints_lower.append(fp("J2", BAT_X, BAT_Y, "F.Cu", 0, bat_pads, "JST-PH-2P"))

# ---------------------------------------------------------------
# SW_BT  Bluetooth sync / pairing button (SMD 3x4mm)
# ---------------------------------------------------------------
swbt_pads = [
    pad_smd(-1.5, 0, 1.0, 1.2, ln("BT_SYNC"), num="1"),
    pad_smd( 1.5, 0, 1.0, 1.2, ln("GND"),     num="2"),
]
footprints_lower.append(fp("SW_BT", SWBT_X, SWBT_Y, "F.Cu", 0, swbt_pads, "BT-SYNC-SW"))

# ---------------------------------------------------------------
# Passives
# ---------------------------------------------------------------
def r_0402(ref, x, y, net1, net2, angle=0):
    pads = [
        pad_smd(-0.5, 0, 0.6, 0.8, ln(net1), num="1"),
        pad_smd( 0.5, 0, 0.6, 0.8, ln(net2), num="2"),
    ]
    return fp(ref, x, y, "F.Cu", angle, pads, "R-0402")

footprints_lower += [
    # R_PU5: 10k pull-up on JOY_SW (D2) → active-low push detected
    r_0402("R_PU5",   JOY_X+8,   JOY_Y-8,  "3V3", "JOY_SW"),
    # R_PU_BT: 10k pull-up on BT_SYNC
    r_0402("R_PU_BT", SWBT_X+5,  SWBT_Y-5, "3V3", "BT_SYNC"),
    # R_DIV1/R_DIV2: voltage divider for ADC_BAT (VBAT → R_DIV1 → ADC_BAT → R_DIV2 → GND)
    # 100k / 100k → 50% of VBAT, keeps < 3.3V ADC input
    r_0402("R_DIV1", BAT_X+4, BAT_Y-2, "VBAT", "ADC_BAT"),
    r_0402("R_DIV2", BAT_X+4, BAT_Y+2, "ADC_BAT", "GND"),
    # Decoupling caps on 3V3 rail (near XIAO)
    r_0402("C1", XIAO_X-4, XIAO_Y+12, "3V3", "GND"),
    r_0402("C2", XIAO_X-2, XIAO_Y+12, "3V3", "GND"),
]

# ---------------------------------------------------------------
# Mounting holes (M2, NPTH)
# ---------------------------------------------------------------
for i, ang in enumerate([45, 135, 225, 315]):
    mhx = BX + MH_R * math.cos(math.radians(ang))
    mhy = BY + MH_R * math.sin(math.radians(ang))
    mh_p = [pad_thru(0, 0, 2.2, 4.4, ln("GND"), num="1")]
    footprints_lower.append(fp(f"H{i+1}", mhx, mhy, "F.Cu", 0, mh_p, "M2-Mount"))

# ---------------------------------------------------------------
# Compose lower PCB file
# ---------------------------------------------------------------
lines = [pcb_header(1.6)]
lines.append(net_defs(L_NETS))
lines.append("")
lines.append(circle_outline(BX, BY, OR))
lines.append(silk_text("XIAO-S3",  XIAO_X,  XIAO_Y-12.0, size=0.6))
lines.append(silk_text("J4-JOY",   JOY_X,   JOY_Y-12.0,  size=0.6))
lines.append(silk_text("J3-FPC",   FPC3_X,  FPC3_Y+3.0,  size=0.6))
lines.append(silk_text("J2-BAT",   BAT_X,   BAT_Y-3.0,   size=0.6))
lines.append(silk_text("SW-BT",    SWBT_X,  SWBT_Y+3.0,  size=0.6))
lines.append(silk_text("LWR R3.0", BX,      BY+35,       size=0.6))
lines.append(silk_text("FWD",      BX,      BY-38,       size=0.6))
for fp_str in footprints_lower:
    lines.append(fp_str)
lines.append(")")

with open(OUT_L, "w") as f:
    f.write("\n".join(lines))
print(f"Lower PCB -> {OUT_L}")


# ================================================================
# UPPER PCB
# ================================================================
OUT_U = os.path.join(BASE, "upper_pcb/upper_pcb.kicad_pcb")

U_NETS = ["GND","3V3","BTN_L","BTN_R","BTN_BK","BTN_FW"]
def un(name): return (net_idx(U_NETS, name), name)

UBX, UBY = 100.0, 100.0
UR = 27.0

sw4x, sw4y = UBX-10, UBY-12
sw5x, sw5y = UBX+10, UBY-12
sw6x, sw6y = UBX-22, UBY
sw7x, sw7y = UBX+22, UBY
fpc5_x, fpc5_y = UBX, UBY+8

footprints_upper = []

# --- SW4/SW5 Kailh GM 8.0 (THT, 3 pins horizontal, 5.08mm pitch) ---
# NO(-5.08,0) — COM(0,0) — NC(+5.08,0)
def gm8_fp(ref, x, y, btn_net):
    pads = [
        pad_thru(-5.08, 0, 1.0, 1.8, un(btn_net), num="1"),  # NO → signal
        pad_thru(  0.0, 0, 1.0, 1.8, un("GND"),   num="2"),  # COM → GND
        pad_thru(+5.08, 0, 1.0, 1.8, un("GND"),   num="3"),  # NC  → GND (safety)
    ]
    return fp(ref, x, y, "F.Cu", 0, pads, "Kailh-GM8.0")

footprints_upper.append(gm8_fp("SW4", sw4x, sw4y, "BTN_L"))
footprints_upper.append(gm8_fp("SW5", sw5x, sw5y, "BTN_R"))

# --- SW6/SW7 Alps SKHLLBA010 (side-push snap-in THT, 4 holes 6.5x6.5mm square) ---
# Pin1=signal(-3.25,-3.25), Pin2=GND(+3.25,-3.25), Leg3(-3.25,+3.25), Leg4(+3.25,+3.25)
def skhll_fp(ref, x, y, btn_net):
    pads = [
        pad_thru(-3.25, -3.25, 1.0, 1.8, un(btn_net), num="1"),
        pad_thru(+3.25, -3.25, 1.0, 1.8, un("GND"),   num="2"),
        pad_thru(-3.25, +3.25, 1.0, 1.8, un("GND"),   num="3"),
        pad_thru(+3.25, +3.25, 1.0, 1.8, un("GND"),   num="4"),
    ]
    return fp(ref, x, y, "F.Cu", 0, pads, "Alps-SKHLLBA010")

footprints_upper.append(skhll_fp("SW6", sw6x, sw6y, "BTN_BK"))
footprints_upper.append(skhll_fp("SW7", sw7x, sw7y, "BTN_FW"))

# --- J5 FPC 6-pin 0.5mm — connects to lower PCB ---
# Pin1=3V3, Pin2=GND, Pin3=BTN_L, Pin4=BTN_R, Pin5=BTN_BK, Pin6=BTN_FW
fpc5_nets = ["3V3","GND","BTN_L","BTN_R","BTN_BK","BTN_FW"]
fpc5_pads = []
for i, net in enumerate(fpc5_nets):
    px = -1.25 + i * 0.5
    fpc5_pads.append(pad_smd(px, 0, 0.4, 1.2, un(net), layer="F.Cu", num=str(i+1)))
fpc5_pads.append(pad_smd(-2.5, 0.8, 1.2, 1.8, un("GND"), layer="F.Cu", num="7"))
fpc5_pads.append(pad_smd( 2.5, 0.8, 1.2, 1.8, un("GND"), layer="F.Cu", num="8"))
footprints_upper.append(fp("J5", fpc5_x, fpc5_y, "F.Cu", 0, fpc5_pads, "FPC-6P-0.5mm"))

# --- R1-R4 pull-ups (10k 0402, 3V3 → BTN signal) ---
def r_0402u(ref, x, y, net1, net2, angle=0):
    pads = [
        pad_smd(-0.5, 0, 0.6, 0.8, un(net1), num="1"),
        pad_smd( 0.5, 0, 0.6, 0.8, un(net2), num="2"),
    ]
    return fp(ref, x, y, "F.Cu", angle, pads, "R-0402")

footprints_upper += [
    r_0402u("R1", sw4x-1, sw4y+7, "3V3", "BTN_L"),
    r_0402u("R2", sw5x-1, sw5y+7, "3V3", "BTN_R"),
    r_0402u("R3", sw6x+5, sw6y-6, "3V3", "BTN_BK"),
    r_0402u("R4", sw7x-5, sw7y-6, "3V3", "BTN_FW"),
]

# --- C1 decoupling 100nF 0402 ---
c1u_pads = [
    pad_smd(-0.5, 0, 0.6, 0.8, un("3V3"), num="1"),
    pad_smd( 0.5, 0, 0.6, 0.8, un("GND"), num="2"),
]
footprints_upper.append(fp("C1", UBX, UBY+8+4, "F.Cu", 0, c1u_pads, "C-0402"))

# --- Mounting holes H1/H2 ---
for ref, hx in [("H1", UBX-15), ("H2", UBX+15)]:
    mh_p = [pad_thru(0, 0, 2.2, 4.4, un("GND"), num="1")]
    footprints_upper.append(fp(ref, hx, UBY, "F.Cu", 0, mh_p, "M2-Mount"))

# ---------------------------------------------------------------
# Compose upper PCB file
# ---------------------------------------------------------------
lines_u = [pcb_header(1.0)]
lines_u.append(net_defs(U_NETS))
lines_u.append("")
lines_u.append(circle_outline(UBX, UBY, UR))
lines_u.append(silk_text("SW4",      sw4x,   sw4y-8.5, size=0.5))
lines_u.append(silk_text("SW5",      sw5x,   sw5y-8.5, size=0.5))
lines_u.append(silk_text("SW6",      sw6x,   sw6y-5.5, size=0.5))
lines_u.append(silk_text("SW7",      sw7x,   sw7y-5.5, size=0.5))
lines_u.append(silk_text("J5",       fpc5_x, fpc5_y+3, size=0.5))
lines_u.append(silk_text("UPR R1.9", UBX,    UBY+21,   size=0.5))
lines_u.append(silk_text("FWD",      UBX,    UBY-23,   size=0.5))
for fp_str in footprints_upper:
    lines_u.append(fp_str)
lines_u.append(")")

with open(OUT_U, "w") as f:
    f.write("\n".join(lines_u))
print(f"Upper PCB -> {OUT_U}")
print("\nDone. Open in KiCad, run DRC, add GND fill on B.Cu.")
