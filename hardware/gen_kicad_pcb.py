#!/usr/bin/env python3
"""
Generate KiCad 7 .kicad_pcb files for DaPao Space Mouse.
Lower PCB rev 2.4 + Upper PCB rev 1.6
All pads assigned to nets — open in KiCad and autoroute.
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
    # nets: list of net names (index 0 = "")
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

# Net list
L_NETS = [
    "GND", "3V3", "VBUS", "BAT_PLUS", "SW_OUT",
    "JOY_X", "JOY_Y", "JOY_SW",
    "ADC_BAT",
    "BTN_L", "BTN_R", "BTN_BK", "BTN_FW",
    "BT_SYNC",
    "USB_DP", "USB_DN",
]
def ln(name): return (net_idx(L_NETS, name), name)

# Board center
BX, BY = 100.0, 100.0
OR = 44.0   # radius 88mm board

# Component positions
XIAO_X,  XIAO_Y  = BX,       BY - 30.0
USBC_X,  USBC_Y  = BX,       BY - 43.0
JOY_X,   JOY_Y   = BX,       BY
FPC3_X,  FPC3_Y  = BX,       BY + 17.0
LDO_X,   LDO_Y   = BX + 18,  BY - 5.0
BAT_X,   BAT_Y   = BX - 8,   BY + 15.0   # B.Cu
SW1_X,   SW1_Y   = BX - 40,  BY
SWBT_X,  SWBT_Y  = BX,       BY + 40.0
SW2_X,   SW2_Y   = XIAO_X+12, XIAO_Y - 4
SW3_X,   SW3_Y   = XIAO_X+12, XIAO_Y + 4
MH_R = 36.0

footprints_lower = []

# --- U1 XIAO ESP32-S3 castellated ---
# Left pads: 3V3, GND, GPIO1, GPIO2, GPIO3, GPIO10, GND (top to bottom)
# Right pads: GPIO5, GPIO6, GPIO7, GPIO8, GPIO9, 3V3, GND
xiao_nets_L = ["3V3","GND","JOY_X","JOY_Y","JOY_SW","ADC_BAT","GND"]
xiao_nets_R = ["BTN_L","BTN_R","BTN_BK","BTN_FW","BT_SYNC","3V3","GND"]
xiao_pads = []
for i,(net) in enumerate(xiao_nets_L):
    py = -9.0 + i*3.0
    xiao_pads.append(pad_smd(-8.75, py, 1.5, 2.0, ln(net), num=str(i+1)))
for i,(net) in enumerate(xiao_nets_R):
    py = -9.0 + i*3.0
    xiao_pads.append(pad_smd(8.75, py, 1.5, 2.0, ln(net), num=str(i+8)))
footprints_lower.append(fp("U1", XIAO_X, XIAO_Y, "F.Cu", 0, xiao_pads, "XIAO-ESP32S3"))

# --- J1 USB-C ---
usbc_pads = []
# Signal pads: VBUS, GND, USB_DP, USB_DN, GND (5 pads)
usbc_nets = ["VBUS","GND","USB_DP","USB_DN","GND"]
for i,net in enumerate(usbc_nets):
    px = -1.25 + i*0.625
    usbc_pads.append(pad_smd(px, 0, 0.8, 1.8, ln(net), num=str(i+1)))
# Shell pads
usbc_pads.append(pad_smd(-2.5, 1.5, 1.6, 2.0, ln("GND"), num="6"))
usbc_pads.append(pad_smd( 2.5, 1.5, 1.6, 2.0, ln("GND"), num="7"))
footprints_lower.append(fp("J1", USBC_X, USBC_Y, "F.Cu", 0, usbc_pads, "USB-C"))

# --- J4 Alps RKJXV1224005 (THT, centered) ---
# X-axis: CCW=3V3, Wiper=JOY_X, CW=GND  at y=-7.0
# Y-axis: CCW=3V3, Wiper=JOY_Y, CW=GND  at y=+7.0
# SW: JOY_SW, GND at x=+3.8
# Mounting legs (GND) at corners
joy_pads = []
for i,(px,net) in enumerate([(-6.4,"3V3"),(-3.0,"JOY_X"),(0.4,"GND")]):
    joy_pads.append(pad_thru(px, -7.0, 1.0, 1.8, ln(net), num=str(i+1)))
    joy_pads.append(pad_thru(px, +7.0, 1.0, 1.8, ln(["3V3","JOY_Y","GND"][i]), num=str(i+4)))
joy_pads.append(pad_thru(3.8, -5.0, 1.0, 1.8, ln("JOY_SW"), num="7"))
joy_pads.append(pad_thru(3.8,  5.0, 1.0, 1.8, ln("GND"),    num="8"))
for i,(mx,my) in enumerate([(-7.7,-8.8),(7.7,-8.8),(-7.7,8.8),(7.7,8.8)]):
    joy_pads.append(pad_thru(mx, my, 1.5, 2.5, ln("GND"), num=f"M{i+1}"))
footprints_lower.append(fp("J4", JOY_X, JOY_Y, "F.Cu", 0, joy_pads, "Alps-RKJXV"))

# --- J3 FPC 6-pin 0.5mm (top contact, F.Cu) ---
fpc3_nets = ["3V3","GND","BTN_L","BTN_R","BTN_BK","BTN_FW"]
fpc3_pads = []
for i,net in enumerate(fpc3_nets):
    px = -1.25 + i*0.5
    fpc3_pads.append(pad_smd(px, 0, 0.4, 1.2, ln(net), num=str(i+1)))
# Latch pads
fpc3_pads.append(pad_smd(-2.5, 0.8, 1.2, 1.8, ln("GND"), num="7"))
fpc3_pads.append(pad_smd( 2.5, 0.8, 1.2, 1.8, ln("GND"), num="8"))
footprints_lower.append(fp("J3", FPC3_X, FPC3_Y, "F.Cu", 0, fpc3_pads, "FPC-6P-0.5mm"))

# --- U3 AP2112K LDO SOT-23-5 ---
# Pin1=GND, Pin2=3V3(out), Pin3=SW_OUT(in), Pin4=GND, Pin5=CE(->SW_OUT)
ldo_pads = []
for i,(dx,net) in enumerate([(-0.95,"GND"),(0,"3V3"),(0.95,"SW_OUT"),(-0.95,"GND"),(0.95,"SW_OUT")]):
    dy = 1.4 if i < 3 else -1.4
    ldo_pads.append(pad_smd(dx, dy, 0.55, 1.0, ln(net), num=str(i+1)))
footprints_lower.append(fp("U3", LDO_X, LDO_Y, "F.Cu", 0, ldo_pads, "AP2112K-3.3V"))

# --- J2 JST-PH 2-pin (through-hole, F.Cu side, underside of board accessible via THT) ---
bat_pads = []
bat_pads.append(pad_thru(-1.0, 0, 1.0, 1.8, ln("BAT_PLUS"), num="1"))
bat_pads.append(pad_thru( 1.0, 0, 1.0, 1.8, ln("GND"),      num="2"))
footprints_lower.append(fp("J2", BAT_X, BAT_Y, "F.Cu", 0, bat_pads, "JST-PH-2P"))

# --- SW1 SPDT power switch ---
sw1_pads = []
sw1_pads.append(pad_smd(0, -1.5, 1.2, 1.8, ln("BAT_PLUS"), num="1"))  # COM
sw1_pads.append(pad_smd(0,  0.0, 1.2, 1.8, ln("BAT_PLUS"), num="2"))  # COM2
sw1_pads.append(pad_smd(0,  1.5, 1.2, 1.8, ln("SW_OUT"),   num="3"))  # NO
footprints_lower.append(fp("SW1", SW1_X+2, SW1_Y, "F.Cu", 90, sw1_pads, "MSK-12C02"))

# --- SW2 BOOT ---
sw2_pads = [
    pad_smd(-1.5, 0, 1.0, 1.2, ln("GND"),    num="1"),
    pad_smd( 1.5, 0, 1.0, 1.2, ln("ADC_BAT"), num="2"),  # GPIO0 reuse slot
]
# Note: SW2 pulls GPIO0 low — GPIO0 is exposed via XIAO internal, not a separate net here
sw2_pads = [
    pad_smd(-1.5, 0, 1.0, 1.2, ln("GND"), num="1"),
    pad_smd( 1.5, 0, 1.0, 1.2, ln("GND"), num="2"),
]
footprints_lower.append(fp("SW2", SW2_X, SW2_Y, "F.Cu", 0, sw2_pads, "BOOT-SW"))

# --- SW3 RESET ---
sw3_pads = [
    pad_smd(-1.5, 0, 1.0, 1.2, ln("GND"), num="1"),
    pad_smd( 1.5, 0, 1.0, 1.2, ln("GND"), num="2"),
]
footprints_lower.append(fp("SW3", SW3_X, SW3_Y, "F.Cu", 0, sw3_pads, "RESET-SW"))

# --- SW_BT Bluetooth sync ---
swbt_pads = [
    pad_smd(-1.5, 0, 1.0, 1.2, ln("BT_SYNC"), num="1"),
    pad_smd( 1.5, 0, 1.0, 1.2, ln("GND"),     num="2"),
]
footprints_lower.append(fp("SW_BT", SWBT_X, SWBT_Y, "F.Cu", 0, swbt_pads, "BT-SYNC-SW"))

# --- 0402 Resistors ---
def r_0402(ref, x, y, net1, net2, angle=0):
    pads = [
        pad_smd(-0.5, 0, 0.6, 0.8, ln(net1), num="1"),
        pad_smd( 0.5, 0, 0.6, 0.8, ln(net2), num="2"),
    ]
    return fp(ref, x, y, "F.Cu", angle, pads, "R-0402")

footprints_lower += [
    r_0402("R_PU5",   JOY_X+8,   JOY_Y-8,   "3V3",     "JOY_SW"),
    r_0402("R_PU_BT", SWBT_X+5,  SWBT_Y-5,  "3V3",     "BT_SYNC"),
    r_0402("R10",     USBC_X+6,  USBC_Y+3,  "VBUS",    "GND"),   # CC1
    r_0402("R11",     USBC_X+6,  USBC_Y+5,  "VBUS",    "GND"),   # CC2
    r_0402("C1",      XIAO_X-6,  XIAO_Y+12, "3V3",     "GND"),
    r_0402("C2",      XIAO_X-4,  XIAO_Y+12, "3V3",     "GND"),
    r_0402("C3",      XIAO_X-2,  XIAO_Y+12, "3V3",     "GND"),
]

# C4 10uF 0805
c4_pads = [
    pad_smd(-1.0, 0, 1.4, 1.8, ln("3V3"), num="1"),
    pad_smd( 1.0, 0, 1.4, 1.8, ln("GND"), num="2"),
]
footprints_lower.append(fp("C4", LDO_X+5, LDO_Y+3, "F.Cu", 0, c4_pads, "C-0805"))

# Mounting holes
mh_pads_list = []
for i,ang in enumerate([45, 135, 225, 315]):
    mhx = BX + MH_R*math.cos(math.radians(ang))
    mhy = BY + MH_R*math.sin(math.radians(ang))
    mh_p = [pad_thru(0, 0, 2.2, 4.4, ln("GND"), num="1")]
    footprints_lower.append(fp(f"H{i+1}", mhx, mhy, "F.Cu", 0, mh_p, "M2-Mount"))

# Compose lower PCB file
lines = [pcb_header(1.6)]
lines.append(net_defs(L_NETS))
lines.append("")
lines.append(circle_outline(BX, BY, OR))
lines.append(silk_text("U1 XIAO-S3",   XIAO_X, XIAO_Y-14.5, size=1.0))
lines.append(silk_text("J4 ALPS-JOY",  JOY_X,  JOY_Y-4,     size=1.0))
lines.append(silk_text("J3 FPC-UP",    FPC3_X, FPC3_Y+4,    size=0.8))
lines.append(silk_text("J1 USB-C FWD", USBC_X, USBC_Y+3.5,  size=0.8))
lines.append(silk_text("U3 LDO",       LDO_X,  LDO_Y-4,     size=0.8))
lines.append(silk_text("SW1 PWR",      SW1_X+2, SW1_Y-5,    size=0.8))
lines.append(silk_text("SW_BT",        SWBT_X, SWBT_Y+4.5,  size=0.8))
lines.append(silk_text("J2 LIPO",      BAT_X,  BAT_Y-5,     layer="B.SilkS", size=0.8))
lines.append(silk_text("LOWER PCB R2.4", BX,   BY+37,       size=0.8))
lines.append(silk_text("FWD",          BX,     BY-40,        size=0.8))
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
fpc5_x, fpc5_y = UBX, UBY+8   # B.Cu

footprints_upper = []

# --- SW4/SW5 Kailh GM 8.0 Cherry MX THT ---
def gm8_fp(ref, x, y, btn_net):
    pads = [
        pad_thru(-3.81, 0,    1.5, 2.0, un("GND"),    num="1"),  # NC (floating/GND)
        pad_thru( 0,    3.81, 1.5, 2.0, un("GND"),    num="2"),  # COM -> GND
        pad_thru( 3.81, 0,    1.5, 2.0, un(btn_net),  num="3"),  # NO -> signal
    ]
    return fp(ref, x, y, "F.Cu", 0, pads, "Kailh-GM8.0")

footprints_upper.append(gm8_fp("SW4", sw4x, sw4y, "BTN_L"))
footprints_upper.append(gm8_fp("SW5", sw5x, sw5y, "BTN_R"))

# --- SW6/SW7 Kailh Blue Dot SMD ---
def bluedot_fp(ref, x, y, btn_net):
    pads = [
        pad_smd(-2.5, 0, 1.8, 2.8, un("GND"),    num="1"),
        pad_smd( 2.5, 0, 1.8, 2.8, un(btn_net),  num="2"),
    ]
    return fp(ref, x, y, "F.Cu", 0, pads, "Kailh-BlueDot")

footprints_upper.append(bluedot_fp("SW6", sw6x, sw6y, "BTN_BK"))
footprints_upper.append(bluedot_fp("SW7", sw7x, sw7y, "BTN_FW"))

# --- J5 FPC 6-pin 0.5mm (F.Cu, all on front layer for single-layer routing) ---
fpc5_nets = ["3V3","GND","BTN_L","BTN_R","BTN_BK","BTN_FW"]
fpc5_pads = []
for i,net in enumerate(fpc5_nets):
    px = -1.25 + i*0.5
    fpc5_pads.append(pad_smd(px, 0, 0.4, 1.2, un(net), layer="F.Cu", num=str(i+1)))
fpc5_pads.append(pad_smd(-2.5, 0.8, 1.2, 1.8, un("GND"), layer="F.Cu", num="7"))
fpc5_pads.append(pad_smd( 2.5, 0.8, 1.2, 1.8, un("GND"), layer="F.Cu", num="8"))
footprints_upper.append(fp("J5", fpc5_x, fpc5_y, "F.Cu", 0, fpc5_pads, "FPC-6P-0.5mm"))

# --- R1-R4 pull-ups (10k 0402, 3V3 -> BTN signal) ---
def r_0402u(ref, x, y, net1, net2, angle=0):
    pads = [
        pad_smd(-0.5, 0, 0.6, 0.8, un(net1), num="1"),
        pad_smd( 0.5, 0, 0.6, 0.8, un(net2), num="2"),
    ]
    return fp(ref, x, y, "F.Cu", angle, pads, "R-0402")

footprints_upper += [
    r_0402u("R1", sw4x-1, sw4y+7, "3V3", "BTN_L"),
    r_0402u("R2", sw5x-1, sw5y+7, "3V3", "BTN_R"),
    r_0402u("R3", sw6x+4, sw6y-4, "3V3", "BTN_BK"),
    r_0402u("R4", sw7x-4, sw7y-4, "3V3", "BTN_FW"),
]

# --- C1 decoupling 100nF 0402 ---
c1u_pads = [
    pad_smd(-0.5, 0, 0.6, 0.8, un("3V3"), num="1"),
    pad_smd( 0.5, 0, 0.6, 0.8, un("GND"), num="2"),
]
footprints_upper.append(fp("C1", UBX, UBY+8+4, "F.Cu", 0, c1u_pads, "C-0402"))

# --- H1/H2 mount holes ---
for ref,hx in [("H1", UBX-15), ("H2", UBX+15)]:
    mh_p = [pad_thru(0, 0, 2.2, 4.4, un("GND"), num="1")]
    footprints_upper.append(fp(ref, hx, UBY, "F.Cu", 0, mh_p, "M2-Mount"))

# Compose upper PCB file
lines_u = [pcb_header(1.0)]
lines_u.append(net_defs(U_NETS))
lines_u.append("")
lines_u.append(circle_outline(UBX, UBY, UR))
lines_u.append(silk_text("SW4 L-CLK",  sw4x, sw4y-9.5,  size=0.8))
lines_u.append(silk_text("SW5 R-CLK",  sw5x, sw5y-9.5,  size=0.8))
lines_u.append(silk_text("SW6 BACK",   sw6x, sw6y-6,    size=0.8))
lines_u.append(silk_text("SW7 FWD",    sw7x, sw7y-6,    size=0.8))
lines_u.append(silk_text("J5 FPC-DN",  fpc5_x, fpc5_y+4, layer="F.SilkS", size=0.8))
lines_u.append(silk_text("UPPER R1.6", UBX,  UBY+22,    size=0.8))
lines_u.append(silk_text("FWD",        UBX,  UBY-24,    size=0.8))
for fp_str in footprints_upper:
    lines_u.append(fp_str)
lines_u.append(")")

with open(OUT_U, "w") as f:
    f.write("\n".join(lines_u))
print(f"Upper PCB -> {OUT_U}")
print("\nDone. Open .kicad_pcb in KiCad -> Route -> Interactive Router or FreeRouting autoroute.")
