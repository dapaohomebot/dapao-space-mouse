#!/usr/bin/env python3
"""
Add copper traces to DaPao Space Mouse KiCad PCB files.
Routes all signal and power nets on lower + upper PCBs.
Appends trace segments before the closing ')' of each file.
"""
import os, math

BASE = os.path.dirname(os.path.abspath(__file__))

def seg(x1, y1, x2, y2, net, layer="F.Cu", width=0.25):
    return f'  (segment (start {x1:.4f} {y1:.4f}) (end {x2:.4f} {y2:.4f}) (width {width:.4f}) (layer "{layer}") (net {net}))'

def via(x, y, net, drill=0.4, size=0.8):
    return f'  (via (at {x:.4f} {y:.4f}) (size {size:.4f}) (drill {drill:.4f}) (layers "F.Cu" "B.Cu") (net {net}))'

def route(pts, net, layer="F.Cu", width=0.25):
    """Connect list of (x,y) points with trace segments."""
    out = []
    for i in range(len(pts)-1):
        x1,y1 = pts[i]; x2,y2 = pts[i+1]
        out.append(seg(x1,y1,x2,y2,net,layer,width))
    return out

def L(x1,y1,x2,y2,net,layer="F.Cu",width=0.25,via_mid=False):
    """L-shaped route: horizontal then vertical."""
    segs = route([(x1,y1),(x2,y1),(x2,y2)], net, layer, width)
    return segs

def append_traces(pcb_path, traces):
    with open(pcb_path, "r") as f:
        content = f.read()
    # Remove final closing paren, append traces, re-add
    content = content.rstrip()
    if content.endswith(")"):
        content = content[:-1].rstrip()
    content += "\n\n  ; ===== COPPER TRACES =====\n"
    content += "\n".join(traces)
    content += "\n)\n"
    with open(pcb_path, "w") as f:
        f.write(content)

# ================================================================
# NET INDEX MAPS (matches gen_kicad_pcb.py order)
# ================================================================
# Lower PCB nets (1-indexed after ""):
# 0="", 1=GND, 2=3V3, 3=VBUS, 4=BAT_PLUS, 5=SW_OUT,
# 6=JOY_X, 7=JOY_Y, 8=JOY_SW, 9=ADC_BAT,
# 10=BTN_L, 11=BTN_R, 12=BTN_BK, 13=BTN_FW, 14=BT_SYNC,
# 15=USB_DP, 16=USB_DN
L_GND=1; L_3V3=2; L_VBUS=3; L_BAT=4; L_SWOUT=5
L_JX=6; L_JY=7; L_JSW=8; L_ADCBAT=9
L_BL=10; L_BR=11; L_BBK=12; L_BFW=13; L_BTSYNC=14

# Upper PCB nets:
# 0="", 1=GND, 2=3V3, 3=BTN_L, 4=BTN_R, 5=BTN_BK, 6=BTN_FW
U_GND=1; U_3V3=2; U_BL=3; U_BR=4; U_BBK=5; U_BFW=6

# ================================================================
# LOWER PCB TRACES
# ================================================================
# Component absolute pad positions:
# XIAO center (100, 70), pads at X±8.75
BX,BY = 100.0, 100.0
XIAO_X, XIAO_Y = 100.0, 70.0
XIAO_L = XIAO_X - 8.75   # 91.25
XIAO_R = XIAO_X + 8.75   # 108.75
# Left pads Y: -9,-6,-3,0,+3,+6,+9 from XIAO_Y = 61,64,67,70,73,76,79
# Nets L: 3V3,GND,JOY_X,JOY_Y,JOY_SW,ADC_BAT,GND
XL = {n: XIAO_Y - 9.0 + i*3.0 for i,n in enumerate(["3V3","GND","JX","JY","JSW","ADC","GND2"])}
# Right pads (BTN_L...GND)
XR = {n: XIAO_Y - 9.0 + i*3.0 for i,n in enumerate(["BTN_L","BTN_R","BTN_BK","BTN_FW","BT_SYNC","3V3","GND"])}

# Key pad positions (absolute)
USBC_X, USBC_Y = 100.0, 57.0
JOY_X,  JOY_Y  = 100.0, 100.0
FPC3_X, FPC3_Y = 100.0, 117.0
LDO_X,  LDO_Y  = 118.0, 95.0
BAT_X,  BAT_Y  = 92.0,  115.0
SW1_X,  SW1_Y  = 62.0,  100.0   # after +2 offset in fp()
SWBT_X, SWBT_Y = 100.0, 140.0
RU5_X,  RU5_Y  = 108.0, 92.0
RPBT_X, RPBT_Y = 105.0, 135.0

traces_lower = []
PW = 0.25   # signal trace width
PP = 0.35   # power trace width

# ---- 3V3 power rail ----
# Horizontal bus at Y=82 (below XIAO, above joystick)
# XIAO left pad 1 (3V3) → bus
traces_lower += route([(XIAO_L, XL["3V3"]), (XIAO_L, 82.0), (97.5, 82.0)], L_3V3, width=PP)
# XIAO right pad 6 (3V3) → bus
traces_lower += route([(XIAO_R, XR["3V3"]), (XIAO_R, 82.0), (108.0, 82.0)], L_3V3, width=PP)
# Bus segment (97.5 to 108)
traces_lower += [seg(97.5, 82.0, 108.0, 82.0, L_3V3, width=PP)]
# LDO output → 3V3 bus
traces_lower += L(118.0, 96.4, 108.0, 82.0, L_3V3, width=PP)
# C1,C2,C3 taps from bus
for cx in [93.5, 95.5, 97.5]:
    traces_lower += [seg(cx, 82.0, cx, 82.0, L_3V3, width=PP)]  # junction markers
# J3 FPC pin1 (3V3) from bus
traces_lower += route([(97.5, 82.0), (90.0, 82.0), (90.0, 117.0), (98.75, 117.0)], L_3V3, width=PP)
# J4 X-axis CCW (3V3) from bus
traces_lower += route([(90.0, 82.0), (90.0, 93.0), (93.6, 93.0)], L_3V3, width=PP)
# J4 Y-axis CCW (3V3) from bus
traces_lower += route([(90.0, 93.0), (90.0, 107.0), (93.6, 107.0)], L_3V3, width=PP)
# R_PU5 pin1 (3V3) from bus
traces_lower += route([(108.0, 82.0), (108.0, 92.0), (107.5, 92.0)], L_3V3, width=PP)
# R_PU_BT pin1 (3V3) from bus down west side
traces_lower += route([(90.0, 107.0), (90.0, 135.0), (104.5, 135.0)], L_3V3, width=PP)
# C4 pin1 (3V3)
traces_lower += L(118.0, 96.4, 122.0, 98.0, L_3V3, width=PP)

# ---- GND net ----
# XIAO GND pads → horizontal bus at Y=84
traces_lower += route([(XIAO_L, XL["GND"]), (XIAO_L, 84.0), (110.0, 84.0), (XIAO_R, XR["GND"])], L_GND, width=PP)
# J1 USB-C GND shells
traces_lower += L(99.375, 57.0, XIAO_L, 84.0, L_GND, width=PP)
# J4 joystick GND pads
traces_lower += route([(100.4, 93.0), (110.0, 93.0), (110.0, 84.0)], L_GND, width=PP)
traces_lower += route([(100.4, 107.0), (110.0, 107.0), (110.0, 84.0)], L_GND, width=PP)
traces_lower += route([(103.8, 105.0), (110.0, 105.0), (110.0, 107.0)], L_GND, width=PP)
# J3 FPC pin2 (GND)
traces_lower += L(99.25, 117.0, 110.0, 107.0, L_GND, width=PP)
# U3 LDO GND pads
traces_lower += route([(117.05, 96.4), (115.0, 96.4), (115.0, 84.0)], L_GND, width=PP)
traces_lower += route([(117.05, 93.6), (115.0, 93.6), (115.0, 84.0)], L_GND, width=PP)
# C4 pin2 (GND)
traces_lower += L(124.0, 98.0, 115.0, 96.4, L_GND, width=PP)
# J2 battery GND (B.Cu) via to F.Cu GND bus
traces_lower += [via(93.0, 115.0, L_GND)]
traces_lower += [seg(93.0, 115.0, 110.0, 115.0, L_GND, "B.Cu", PP)]
# SW_BT GND
traces_lower += L(101.5, 140.0, 110.0, 107.0, L_GND, width=PP)
# Mounting hole GND pads (annular rings already on GND net, just reference)

# ---- VBUS ----
# J1 USB-C VBUS → XIAO VBUS pad (short run, XIAO handles internally)
traces_lower += L(98.75, 57.0, XIAO_X, 62.0, L_VBUS, width=PP)

# ---- BAT_PLUS (B.Cu layer) ----
# J2 pin1 → along bottom to SW1 COM
traces_lower += route([(91.0, 115.0), (65.0, 115.0), (65.0, 100.0), (63.5, 100.0)], L_BAT, "B.Cu", PP)

# ---- SW_OUT (LDO input) ----
# SW1 NO → LDO VIN (F.Cu — need via from B.Cu SW1 side)
# SW1 pin3 (SW_OUT) at (60.5, 100) → right along west edge → LDO VIN
traces_lower += route([(60.5, 100.0), (55.0, 100.0), (55.0, 95.0), (115.0, 95.0), (118.95, 96.4)], L_SWOUT, width=PP)
# LDO CE also gets SW_OUT
traces_lower += L(118.95, 93.6, 118.95, 96.4, L_SWOUT, width=PP)

# ---- JOY_X ----
# XIAO L3 → J4 X Wiper
traces_lower += route([(XIAO_L, XL["JX"]), (88.0, XL["JX"]), (88.0, 93.0), (97.0, 93.0)], L_JX, width=PW)

# ---- JOY_Y ----
# XIAO L4 → J4 Y Wiper
traces_lower += route([(XIAO_L, XL["JY"]), (86.0, XL["JY"]), (86.0, 107.0), (97.0, 107.0)], L_JY, width=PW)

# ---- JOY_SW ----
# J4 SW pad → R_PU5 pin2 → XIAO L5
traces_lower += L(103.8, 95.0, 108.5, 92.0, L_JSW, width=PW)    # SW pad → R_PU5
traces_lower += L(107.5, 92.0, XIAO_R, XR["BT_SYNC"]+3, L_JSW, width=PW)  # via bus area
# Direct: R_PU5 → XIAO L5 (JOY_SW)
traces_lower += route([(107.5, 92.0), (107.5, 88.0), (XIAO_L, 88.0), (XIAO_L, XL["JSW"])], L_JSW, width=PW)

# ---- BTN_L → J3 FPC P3 ----
traces_lower += route([(XIAO_R, XR["BTN_L"]), (112.0, XR["BTN_L"]), (112.0, 117.0), (99.75, 117.0)], L_BL, width=PW)

# ---- BTN_R → J3 FPC P4 ----
traces_lower += route([(XIAO_R, XR["BTN_R"]), (113.0, XR["BTN_R"]), (113.0, 118.0), (100.25, 118.0), (100.25, 117.0)], L_BR, width=PW)

# ---- BTN_BK → J3 FPC P5 ----
traces_lower += route([(XIAO_R, XR["BTN_BK"]), (114.0, XR["BTN_BK"]), (114.0, 119.0), (100.75, 119.0), (100.75, 117.0)], L_BBK, width=PW)

# ---- BTN_FW → J3 FPC P6 ----
traces_lower += route([(XIAO_R, XR["BTN_FW"]), (115.0, XR["BTN_FW"]), (115.0, 120.0), (101.25, 120.0), (101.25, 117.0)], L_BFW, width=PW)

# ---- BT_SYNC ----
# XIAO R5 → R_PU_BT pin2 → SW_BT pin1
traces_lower += route([(XIAO_R, XR["BT_SYNC"]), (116.0, XR["BT_SYNC"]), (116.0, 130.0), (105.5, 130.0), (105.5, 135.0)], L_BTSYNC, width=PW)
traces_lower += L(104.5, 135.0, 98.5, 140.0, L_BTSYNC, width=PW)

# Write lower PCB traces
pcb_lower = os.path.join(BASE, "lower_pcb/lower_pcb.kicad_pcb")
append_traces(pcb_lower, traces_lower)
print(f"Lower PCB traces added -> {pcb_lower}  ({len(traces_lower)} segments/vias)")

# ================================================================
# UPPER PCB TRACES
# ================================================================
UBX, UBY = 100.0, 100.0
sw4x, sw4y = 90.0, 88.0
sw5x, sw5y = 110.0, 88.0
sw6x, sw6y = 78.0, 100.0
sw7x, sw7y = 122.0, 100.0
fpc5x, fpc5y = 100.0, 108.0   # B.Cu

# R1-R4 positions
r1x,r1y = sw4x-1, sw4y+7
r2x,r2y = sw5x-1, sw5y+7
r3x,r3y = sw6x+4, sw6y-4
r4x,r4y = sw7x-4, sw7y-4
c1x,c1y = 100.0, 116.0  # C1 is at UBX, fpc5y+8

traces_upper = []

# ---- 3V3 rail on upper PCB (B.Cu — FPC is on B.Cu) ----
# J5 pin1 (3V3) at B.Cu: fpc5x-1.25 = 98.75, fpc5y
# Route 3V3 from J5 up to R1,R2,R3,R4 via via to F.Cu
FPC5_3V3 = (fpc5x - 1.25, fpc5y)  # 98.75, 108
traces_upper += [via(98.75, 108.0, U_3V3)]  # B.Cu via to F.Cu
# F.Cu 3V3 rail horizontal at Y=96
traces_upper += route([(98.75, 108.0), (98.75, 96.0), (122.0, 96.0)], U_3V3, width=PP)
# Tap to R1 (sw4x-1-0.5=88.5, sw4y+7=95)
traces_upper += L(98.75, 96.0, r1x-0.5, r1y, U_3V3, width=PP)
# Tap to R2
traces_upper += L(108.0, 96.0, r2x-0.5, r2y, U_3V3, width=PP)
# Tap to R3
traces_upper += L(80.0, 96.0, r3x-0.5, r3y, U_3V3, width=PP)
# Tap to R4
traces_upper += L(118.0, 96.0, r4x-0.5, r4y, U_3V3, width=PP)

# ---- GND rail ----
# J5 pin2 (GND) at B.Cu: (99.25, 108)
traces_upper += [via(99.25, 108.0, U_GND)]
traces_upper += route([(99.25, 108.0), (99.25, 98.0), (122.0, 98.0)], U_GND, width=PP)
# SW4 COM (GND) at (sw4x, sw4y+3.81) = (90, 91.81)
traces_upper += L(99.25, 98.0, sw4x, sw4y+3.81, U_GND, width=PP)
# SW5 COM (GND) at (sw5x, sw5y+3.81) = (110, 91.81)
traces_upper += L(110.0, 98.0, sw5x, sw5y+3.81, U_GND, width=PP)
# SW6 GND pad at (sw6x-2.5, sw6y) = (75.5, 100)
traces_upper += L(80.0, 98.0, sw6x-2.5, sw6y, U_GND, width=PP)
# SW7 GND pad at (sw7x-2.5, sw7y) = (119.5, 100)
traces_upper += L(119.5, 98.0, sw7x-2.5, sw7y, U_GND, width=PP)
# C1 GND
traces_upper += L(c1x+0.5, c1y, 110.0, 98.0, U_GND, width=PP)

# ---- BTN_L ----
# J5 pin3 (BTN_L) at B.Cu: (99.75, 108) → via → F.Cu → R1 → SW4 NO
traces_upper += [via(99.75, 108.0, U_BL)]
traces_upper += route([(99.75, 108.0), (99.75, 104.0), (r1x+0.5, 104.0), (r1x+0.5, r1y)], U_BL, width=PW)
# R1 out → SW4 NO at (sw4x+3.81, sw4y) = (93.81, 88)
traces_upper += L(r1x+0.5, r1y, sw4x+3.81, sw4y, U_BL, width=PW)

# ---- BTN_R ----
traces_upper += [via(100.25, 108.0, U_BR)]
traces_upper += route([(100.25, 108.0), (100.25, 105.0), (r2x+0.5, 105.0), (r2x+0.5, r2y)], U_BR, width=PW)
traces_upper += L(r2x+0.5, r2y, sw5x+3.81, sw5y, U_BR, width=PW)

# ---- BTN_BK ----
traces_upper += [via(100.75, 108.0, U_BBK)]
traces_upper += route([(100.75, 108.0), (100.75, 102.0), (82.0, 102.0), (r3x+0.5, 102.0), (r3x+0.5, r3y)], U_BBK, width=PW)
# R3 out → SW6 SIG at (sw6x+2.5, sw6y) = (80.5, 100)
traces_upper += L(r3x+0.5, r3y, sw6x+2.5, sw6y, U_BBK, width=PW)

# ---- BTN_FW ----
traces_upper += [via(101.25, 108.0, U_BFW)]
traces_upper += route([(101.25, 108.0), (101.25, 103.0), (118.0, 103.0), (r4x+0.5, 103.0), (r4x+0.5, r4y)], U_BFW, width=PW)
# R4 out → SW7 SIG at (sw7x+2.5, sw7y) = (124.5, 100)
traces_upper += L(r4x+0.5, r4y, sw7x+2.5, sw7y, U_BFW, width=PW)

# C1 3V3 tap from rail
traces_upper += L(c1x-0.5, c1y, 99.25, 108.0, U_3V3, width=PP)

pcb_upper = os.path.join(BASE, "upper_pcb/upper_pcb.kicad_pcb")
append_traces(pcb_upper, traces_upper)
print(f"Upper PCB traces added -> {pcb_upper}  ({len(traces_upper)} segments/vias)")
print("\nOpen both .kicad_pcb files in KiCad.")
print("Run DRC to check for any conflicts, then use interactive router to fix any violations.")
