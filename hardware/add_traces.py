#!/usr/bin/env python3
"""
Add copper traces to DaPao Space Mouse KiCad PCB files.
2-layer simplified: ALL traces on F.Cu only.
B.Cu = solid GND pour (no routed traces, no vias).
"""
import os, math

BASE = os.path.dirname(os.path.abspath(__file__))

def seg(x1, y1, x2, y2, net, layer="F.Cu", width=0.25):
    return f'  (segment (start {x1:.4f} {y1:.4f}) (end {x2:.4f} {y2:.4f}) (width {width:.4f}) (layer "{layer}") (net {net}))'

def route(pts, net, layer="F.Cu", width=0.25):
    out = []
    for i in range(len(pts)-1):
        x1,y1 = pts[i]; x2,y2 = pts[i+1]
        out.append(seg(x1,y1,x2,y2,net,layer,width))
    return out

def L(x1,y1,x2,y2,net,width=0.25):
    """L-route: horizontal then vertical, F.Cu only."""
    return route([(x1,y1),(x2,y1),(x2,y2)], net, "F.Cu", width)

def append_traces(pcb_path, traces):
    with open(pcb_path, "r") as f:
        content = f.read()
    content = content.rstrip()
    if content.endswith(")"):
        content = content[:-1].rstrip()
    content += "\n\n# ===== COPPER TRACES (F.Cu only) =====\n"
    content += "\n".join(traces)
    content += "\n)\n"
    with open(pcb_path, "w") as f:
        f.write(content)

# ================================================================
# NET INDICES
# Lower: 1=GND 2=3V3 3=VBUS 4=BAT_PLUS 5=SW_OUT
#        6=JOY_X 7=JOY_Y 8=JOY_SW 9=ADC_BAT
#        10=BTN_L 11=BTN_R 12=BTN_BK 13=BTN_FW 14=BT_SYNC
# Upper: 1=GND 2=3V3 3=BTN_L 4=BTN_R 5=BTN_BK 6=BTN_FW
# ================================================================
L_GND=1; L_3V3=2; L_VBUS=3; L_BAT=4; L_SWOUT=5
L_JX=6;  L_JY=7;  L_JSW=8;  L_ADC=9
L_BL=10; L_BR=11; L_BBK=12; L_BFW=13; L_BTSYNC=14
U_GND=1; U_3V3=2; U_BL=3; U_BR=4; U_BBK=5; U_BFW=6

PW = 0.25  # signal width
PP = 0.35  # power width

# ================================================================
# LOWER PCB — all F.Cu
# ================================================================
BX, BY = 100.0, 100.0
XIAO_X, XIAO_Y = 100.0, 70.0
XIAO_L = XIAO_X - 8.75   # 91.25
XIAO_R = XIAO_X + 8.75   # 108.75

# Left pad Y positions: 3V3 GND JX JY JSW ADC GND
XLY = [XIAO_Y - 9.0 + i*3.0 for i in range(7)]
# Right pad Y positions: BTN_L BTN_R BTN_BK BTN_FW BT_SYNC 3V3 GND
XRY = [XIAO_Y - 9.0 + i*3.0 for i in range(7)]

USBC_X, USBC_Y = 100.0, 57.0
JOY_X,  JOY_Y  = 100.0, 100.0
FPC3_X, FPC3_Y = 100.0, 117.0
LDO_X,  LDO_Y  = 118.0, 95.0
BAT_X,  BAT_Y  = 92.0,  115.0
SW1_X,  SW1_Y  = 62.0,  100.0
SWBT_X, SWBT_Y = 100.0, 140.0

traces_lower = []

# ---- 3V3 rail (horizontal bus at Y=82) ----
traces_lower += route([(XIAO_L, XLY[0]), (XIAO_L, 82.0), (115.0, 82.0)], L_3V3, width=PP)
traces_lower += route([(XIAO_R, XRY[5]), (XIAO_R, 82.0), (115.0, 82.0)], L_3V3, width=PP)
# LDO 3V3 out → bus
traces_lower += L(118.0, 96.4, 115.0, 82.0, L_3V3, width=PP)
# FPC J3 pin1
traces_lower += route([(90.0, 82.0), (90.0, 117.0), (98.75, 117.0)], L_3V3, width=PP)
# J4 X CCW
traces_lower += route([(90.0, 82.0), (90.0, 93.0), (93.6, 93.0)], L_3V3, width=PP)
# J4 Y CCW
traces_lower += route([(90.0, 93.0), (90.0, 107.0), (93.6, 107.0)], L_3V3, width=PP)
# R_PU5 pin1
traces_lower += route([(115.0, 82.0), (115.0, 92.0), (107.5, 92.0)], L_3V3, width=PP)
# R_PU_BT pin1
traces_lower += route([(90.0, 107.0), (90.0, 135.0), (104.5, 135.0)], L_3V3, width=PP)
# C4 pin1
traces_lower += L(115.0, 82.0, 122.0, 98.0, L_3V3, width=PP)

# ---- GND rail (bus at Y=84, east column at X=120) ----
traces_lower += route([(XIAO_L, XLY[1]), (XIAO_L, 84.0), (120.0, 84.0)], L_GND, width=PP)
traces_lower += route([(XIAO_R, XRY[6]), (XIAO_R, 84.0), (120.0, 84.0)], L_GND, width=PP)
# J1 USB-C GND
traces_lower += L(100.625, 57.0, 120.0, 84.0, L_GND, width=PP)
# J4 GND pads
traces_lower += route([(100.4, 93.0), (120.0, 93.0), (120.0, 84.0)], L_GND, width=PP)
traces_lower += route([(100.4, 107.0), (120.0, 107.0), (120.0, 84.0)], L_GND, width=PP)
traces_lower += route([(103.8, 105.0), (120.0, 105.0), (120.0, 107.0)], L_GND, width=PP)
# J3 FPC pin2
traces_lower += route([(99.25, 117.0), (85.0, 117.0), (85.0, 84.0), (XIAO_L, 84.0)], L_GND, width=PP)
# LDO GND
traces_lower += route([(117.05, 96.4), (120.0, 96.4), (120.0, 84.0)], L_GND, width=PP)
traces_lower += L(117.05, 93.6, 120.0, 84.0, L_GND, width=PP)
# C4 pin2
traces_lower += L(124.0, 98.0, 120.0, 96.4, L_GND, width=PP)
# J2 battery GND (F.Cu — THT pin goes through to B.Cu)
traces_lower += route([(93.0, 115.0), (85.0, 115.0), (85.0, 117.0)], L_GND, width=PP)
# SW_BT GND
traces_lower += L(101.5, 140.0, 120.0, 107.0, L_GND, width=PP)

# ---- VBUS ----
traces_lower += L(98.75, 57.0, XIAO_X-2, 62.0, L_VBUS, width=PP)

# ---- BAT_PLUS (F.Cu — route around south side) ----
# J2 pin1 → around south → SW1 COM
traces_lower += route([(91.0, 115.0), (75.0, 115.0), (75.0, 105.0), (65.0, 105.0), (65.0, 101.5)], L_BAT, width=PP)

# ---- SW_OUT ----
# SW1 NO → north → LDO VIN
traces_lower += route([(60.5, 100.0), (56.0, 100.0), (56.0, 90.0), (120.0, 90.0), (118.95, 93.6)], L_SWOUT, width=PP)
traces_lower += L(118.95, 96.4, 118.95, 93.6, L_SWOUT, width=PP)  # CE pin

# ---- JOY_X → XIAO GPIO1 ----
traces_lower += route([(XIAO_L, XLY[2]), (88.0, XLY[2]), (88.0, 93.0), (97.0, 93.0)], L_JX, width=PW)

# ---- JOY_Y → XIAO GPIO2 ----
traces_lower += route([(XIAO_L, XLY[3]), (86.0, XLY[3]), (86.0, 107.0), (97.0, 107.0)], L_JY, width=PW)

# ---- JOY_SW → R_PU5 → XIAO GPIO3 ----
traces_lower += route([(103.8, 95.0), (107.5, 95.0), (107.5, 92.0)], L_JSW, width=PW)  # SW → R_PU5
traces_lower += route([(107.5, 92.0), (107.5, 88.0), (XIAO_L, 88.0), (XIAO_L, XLY[4])], L_JSW, width=PW)

# ---- BTN_L → FPC J3 pin3 ----
traces_lower += route([(XIAO_R, XRY[0]), (112.0, XRY[0]), (112.0, 117.5), (99.75, 117.5), (99.75, 117.0)], L_BL, width=PW)

# ---- BTN_R → FPC J3 pin4 ----
traces_lower += route([(XIAO_R, XRY[1]), (113.0, XRY[1]), (113.0, 118.5), (100.25, 118.5), (100.25, 117.0)], L_BR, width=PW)

# ---- BTN_BK → FPC J3 pin5 ----
traces_lower += route([(XIAO_R, XRY[2]), (114.0, XRY[2]), (114.0, 119.5), (100.75, 119.5), (100.75, 117.0)], L_BBK, width=PW)

# ---- BTN_FW → FPC J3 pin6 ----
traces_lower += route([(XIAO_R, XRY[3]), (115.0, XRY[3]), (115.0, 120.5), (101.25, 120.5), (101.25, 117.0)], L_BFW, width=PW)

# ---- BT_SYNC → R_PU_BT → SW_BT ----
traces_lower += route([(XIAO_R, XRY[4]), (116.0, XRY[4]), (116.0, 130.0), (105.5, 130.0), (105.5, 135.0)], L_BTSYNC, width=PW)
traces_lower += L(104.5, 135.0, SWBT_X-1.5, SWBT_Y, L_BTSYNC, width=PW)

pcb_lower = os.path.join(BASE, "lower_pcb/lower_pcb.kicad_pcb")
append_traces(pcb_lower, traces_lower)
print(f"Lower PCB: {len(traces_lower)} segments — all F.Cu, no vias -> {pcb_lower}")

# ================================================================
# UPPER PCB — all F.Cu
# ================================================================
UBX, UBY = 100.0, 100.0
sw4x, sw4y = 90.0, 88.0
sw5x, sw5y = 110.0, 88.0
sw6x, sw6y = 78.0, 100.0
sw7x, sw7y = 122.0, 100.0
fpc5x, fpc5y = 100.0, 108.0
r1x,r1y = sw4x-1, sw4y+7
r2x,r2y = sw5x-1, sw5y+7
r3x,r3y = sw6x+5, sw6y-6   # R3 near SW6 SKHLLBA010
r4x,r4y = sw7x-5, sw7y-6   # R4 near SW7 SKHLLBA010

traces_upper = []

# ---- 3V3 rail (horizontal bus at Y=96) ----
# J5 FPC pin1 (3V3) at (98.75, fpc5y=108) → up to bus
traces_upper += route([(fpc5x-1.25, fpc5y), (fpc5x-1.25, 96.0), (122.0, 96.0)], U_3V3, width=PP)
# Branch to R1
traces_upper += L(r1x-0.5, 96.0, r1x-0.5, r1y, U_3V3, width=PP)
# Branch to R2
traces_upper += L(r2x-0.5, 96.0, r2x-0.5, r2y, U_3V3, width=PP)
# Branch west to R3
traces_upper += route([(80.0, 96.0), (r3x-0.5, 96.0), (r3x-0.5, r3y)], U_3V3, width=PP)
# Branch to R4
traces_upper += L(118.0, 96.0, r4x-0.5, r4y, U_3V3, width=PP)

# ---- GND rail (bus at Y=98) ----
# J5 FPC pin2 (GND) at (99.25, 108) → up to bus
traces_upper += route([(fpc5x-0.75, fpc5y), (fpc5x-0.75, 98.0), (122.0, 98.0)], U_GND, width=PP)
# SW4 COM (0,0 from sw4 center = sw4x, sw4y) → GND bus
traces_upper += L(sw4x, sw4y, sw4x, 98.0, U_GND, width=PP)
# SW5 COM (sw5x, sw5y) → GND bus
traces_upper += L(sw5x, sw5y, sw5x, 98.0, U_GND, width=PP)
# SW6 GND pads (SKHLLBA010: pin2 at +3.25,-3.25 and legs at +-3.25,+3.25)
traces_upper += L(sw6x+3.25, sw6y-3.25, 82.0, 98.0, U_GND, width=PP)
# SW7 GND pads
traces_upper += L(sw7x+3.25, sw7y-3.25, 119.0, 98.0, U_GND, width=PP)

# ---- BTN_L ----
# J5 pin3 (99.75, 108) → R1 → SW4 NO (at sw4x-5.08, sw4y)
traces_upper += route([(fpc5x-0.25, fpc5y), (fpc5x-0.25, 104.0), (r1x+0.5, 104.0), (r1x+0.5, r1y)], U_BL, width=PW)
traces_upper += L(r1x+0.5, r1y, sw4x-5.08, sw4y, U_BL, width=PW)

# ---- BTN_R ----
# J5 pin4 (100.25, 108) → R2 → SW5 NO (at sw5x-5.08, sw5y)
traces_upper += route([(fpc5x+0.25, fpc5y), (fpc5x+0.25, 105.0), (r2x+0.5, 105.0), (r2x+0.5, r2y)], U_BR, width=PW)
traces_upper += L(r2x+0.5, r2y, sw5x-5.08, sw5y, U_BR, width=PW)

# ---- BTN_BK ----
# J5 pin5 (100.75, 108) → R3 → SW6 SIG
traces_upper += route([(fpc5x+0.75, fpc5y), (fpc5x+0.75, 102.0), (82.0, 102.0), (r3x+0.5, 102.0), (r3x+0.5, r3y)], U_BBK, width=PW)
traces_upper += L(r3x+0.5, r3y, sw6x-3.25, sw6y-3.25, U_BBK, width=PW)  # SW6 SIG pin

# ---- BTN_FW ----
# J5 pin6 (101.25, 108) → R4 → SW7 SIG pin at (sw7x-3.25, sw7y-3.25)
traces_upper += route([(fpc5x+1.25, fpc5y), (fpc5x+1.25, 103.0), (118.0, 103.0), (r4x+0.5, 103.0), (r4x+0.5, r4y)], U_BFW, width=PW)
traces_upper += L(r4x+0.5, r4y, sw7x-3.25, sw7y-3.25, U_BFW, width=PW)  # SW7 SIG pin

pcb_upper = os.path.join(BASE, "upper_pcb/upper_pcb.kicad_pcb")
append_traces(pcb_upper, traces_upper)
print(f"Upper PCB: {len(traces_upper)} segments — all F.Cu, no vias -> {pcb_upper}")
print("\nDone. B.Cu = GND pour only. Open in KiCad, run DRC, add GND fill.")
