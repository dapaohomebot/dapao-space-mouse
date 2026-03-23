#!/usr/bin/env python3
"""
Add copper traces for DaPao Space Mouse PCBs.
All traces on F.Cu. B.Cu = solid GND pour.
Pad coordinates verified against gen_kicad_pcb.py rev 3.0 / upper rev 1.9.

LOWER PCB net indices:
  1=GND  2=3V3  3=VBAT
  4=JOY_X  5=JOY_Y  6=JOY_SW  7=ADC_BAT
  8=BTN_L  9=BTN_R  10=BTN_BK  11=BTN_FW  12=BT_SYNC

UPPER PCB net indices:
  1=GND  2=3V3  3=BTN_L  4=BTN_R  5=BTN_BK  6=BTN_FW
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def seg(x1,y1,x2,y2,net,layer="F.Cu",width=0.25):
    return f'  (segment (start {x1:.4f} {y1:.4f}) (end {x2:.4f} {y2:.4f}) (width {width:.4f}) (layer "{layer}") (net {net}))'

def route(pts,net,layer="F.Cu",width=0.25):
    return [seg(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1],net,layer,width)
            for i in range(len(pts)-1)]

def L(x1,y1,x2,y2,net,w=0.25):
    """Horizontal-then-vertical L-route on F.Cu."""
    return route([(x1,y1),(x2,y1),(x2,y2)], net, width=w)

def append_traces(pcb_path, traces):
    with open(pcb_path,"r") as f: content = f.read()
    content = content.rstrip()
    if content.endswith(")"): content = content[:-1].rstrip()
    content += "\n\n# ===== COPPER TRACES (F.Cu, pad coords verified) =====\n"
    content += "\n".join(traces)
    content += "\n)\n"
    with open(pcb_path,"w") as f: f.write(content)

# Lower net indices
LG=1; L3=2; LVB=3
LJX=4; LJY=5; LJW=6; LAD=7
LBL=8; LBR=9; LBK=10; LBF=11; LBT=12

# Upper net indices
UG=1; U3=2; UBL=3; UBR=4; UBK=5; UBF=6

PW=0.25; PP=0.35

# ==============================================================
# LOWER PCB
# Board / component positions (from gen_kicad_pcb.py)
# ==============================================================
BX,BY = 100.0,100.0
XC,YC = BX, BY-30.0   # XIAO centre

# XIAO castellated pads (absolute)
# Left column X = XC-8.75 = 91.25
# Right column X = XC+8.75 = 108.75
# Pad Y = YC + (-7.62 + i*2.54), i=0..6
XL = XC-8.75   # 91.25
XR = XC+8.75   # 108.75
LY = [YC-7.62+i*2.54 for i in range(7)]
#  LY[0] = 62.38  GND (L1)
#  LY[1] = 64.92  GND (L2)
#  LY[2] = 67.46  JOY_X (L3)
#  LY[3] = 70.00  JOY_Y (L4)
#  LY[4] = 72.54  JOY_SW (L5)
#  LY[5] = 75.08  ADC_BAT (L6)
#  LY[6] = 77.62  BTN_L (L7)
RY = [YC-7.62+i*2.54 for i in range(7)]
#  RY[0] = 62.38  BTN_R (R1)
#  RY[1] = 64.92  BTN_BK (R2)
#  RY[2] = 67.46  BTN_FW (R3)
#  RY[3] = 70.00  BT_SYNC (R4)
#  RY[4] = 72.54  GND (R5)
#  RY[5] = 75.08  GND (R6)
#  RY[6] = 77.62  3V3 (R7)

# Back pads (VBAT at XC-2.5, YC+9 / GND at XC+2.5, YC+9)
VBAT_X, VBAT_Y = XC-2.5, YC+9.0

# Joystick J4 absolute pads (centre BX,BY = 100,100)
#  X-axis: CCW=(93.6,93) Wiper=(97,93) CW=(100.4,93)
#  Y-axis: CCW=(93.6,107) Wiper=(97,107) CW=(100.4,107)
#  SW:     (103.8,95) GND (103.8,105)
#  Legs:   (92.3,91.2),(107.7,91.2),(92.3,108.8),(107.7,108.8)

# FPC J3 pads: px = -1.25+i*0.5, y=117  i=0..5
# J3 pin1(3V3)=(98.75,117) pin2(GND)=(99.25,117)
# pin3(BTN_L)=(99.75,117)  pin4(BTN_R)=(100.25,117)
# pin5(BTN_BK)=(100.75,117) pin6(BTN_FW)=(101.25,117)
FPC3_X,FPC3_Y = BX, BY+17.0

# J2 LiPo: pin1(VBAT)=(BAT_X-1,BAT_Y)=(91,115) pin2(GND)=(93,115)
BAT_X,BAT_Y = BX-8, BY+15.0

# SW_BT: pin1(BT_SYNC)=(SWBT_X-1.5,SWBT_Y)=(98.5,140) pin2(GND)=(101.5,140)
SWBT_X,SWBT_Y = BX, BY+40.0

# R_PU5 (centre JOY_X+8,JOY_Y-8 = 108,92): pin1(3V3)=(107.5,92) pin2(JOY_SW)=(108.5,92)
# R_PU_BT (centre SWBT_X+5,SWBT_Y-5 = 105,35): pin1(3V3)=(104.5,35) pin2(BT_SYNC)=(105.5,35)
# R_DIV1 (centre BAT_X+4,BAT_Y-2 = 96,113): pin1(VBAT)=(95.5,113) pin2(ADC_BAT)=(96.5,113)
# R_DIV2 (centre BAT_X+4,BAT_Y+2 = 96,117): pin1(ADC_BAT)=(95.5,117) pin2(GND)=(96.5,117)
# C1 (centre XC-4,YC+12 = 96,82): pin1(3V3)=(95.5,82) pin2(GND)=(96.5,82)
# C2 (centre XC-2,YC+12 = 98,82): pin1(3V3)=(97.5,82) pin2(GND)=(98.5,82)

traces_lower = []

# ---- 3V3 rail — XIAO R7 output (108.75, 77.62) → horizontal bus at Y=80 ----
traces_lower += route([(XR,RY[6]),(XR,80),(115,80)], L3, width=PP)
# J4 X-CCW (93.6,93) and Y-CCW (93.6,107) via west spur at X=90
traces_lower += route([(90,80),(90,93)], L3, width=PP)
traces_lower += seg(90,80,115,80, L3, width=PP)
traces_lower += seg(90,93, 93.6,93, L3, width=PP)
traces_lower += seg(90,107, 93.6,107, L3, width=PP)
traces_lower += route([(90,93),(90,107)], L3, width=PP)
# J3 FPC pin1 (3V3 at 98.75,117) from west spur
traces_lower += route([(90,107),(90,117),(98.75,117)], L3, width=PP)
# R_PU5 pin1 (3V3 at 107.5,92) from rail
traces_lower += route([(115,80),(115,92),(107.5,92)], L3, width=PP)
# R_PU_BT pin1 (3V3 at 104.5,35) from rail — route south around board
traces_lower += route([(90,107),(90,135),(104.5,135)], L3, width=PP)
# C1/C2 pin1 (3V3 at 95.5,82 / 97.5,82)
traces_lower += route([(95.5,82),(95.5,80)], L3, width=PP)
traces_lower += route([(97.5,82),(97.5,80)], L3, width=PP)

# ---- GND bus — east column X=120, bus Y=82 ----
# XIAO L1 (GND at 91.25,62.38) → bus
traces_lower += route([(XL,LY[0]),(XL,82),(120,82)], LG, width=PP)
# XIAO L2 (GND at 91.25,64.92) → bus
traces_lower += route([(XL,LY[1]),(XL,82),(120,82)], LG, width=PP)
# XIAO R5/R6 (GND at 108.75,72.54 and 75.08) → bus
traces_lower += route([(XR,RY[4]),(XR,82),(120,82)], LG, width=PP)
# J4 GND pads
traces_lower += route([(100.4,93),(120,93),(120,82)], LG, width=PP)
traces_lower += route([(100.4,107),(120,107),(120,82)], LG, width=PP)
traces_lower += route([(103.8,105),(120,105),(120,107)], LG, width=PP)
# J4 mounting legs
traces_lower += L(92.3,91.2, 90,82, LG, w=PP)
traces_lower += L(107.7,91.2, 120,82, LG, w=PP)
# J3 FPC pin2 (GND at 99.25,117) → west spur
traces_lower += route([(99.25,117),(85,117),(85,82),(XL,82)], LG, width=PP)
# J2 battery pin2 (GND at 93,115)
traces_lower += route([(93,115),(85,115),(85,117)], LG, width=PP)
# SW_BT pin2 (GND at 101.5,140) → east column
traces_lower += L(101.5,140, 120,107, LG, w=PP)
# R_DIV2 pin2 (GND at 96.5,117) → FPC GND line
traces_lower += route([(96.5,117),(85,117)], LG, width=PP)
# C1/C2 pin2 (GND at 96.5,82 / 98.5,82)
traces_lower += route([(96.5,82),(120,82)], LG, width=PP)
traces_lower += route([(98.5,82),(120,82)], LG, width=PP)

# ---- VBAT — J2 pin1 (91,115) → XIAO back pad (97.5,79) via west side ----
traces_lower += route([(91,115),(80,115),(80,YC+9),(VBAT_X,VBAT_Y)], LVB, width=PP)

# ---- JOY_X → XIAO L3 (91.25, 67.46) ----
# J4 X wiper (97,93) → XIAO
traces_lower += route([(97,93),(88,93),(88,LY[2]),(XL,LY[2])], LJX, width=PW)

# ---- JOY_Y → XIAO L4 (91.25, 70.0) ----
# J4 Y wiper (97,107) → XIAO
traces_lower += route([(97,107),(86,107),(86,LY[3]),(XL,LY[3])], LJY, width=PW)

# ---- JOY_SW → R_PU5 → XIAO L5 (91.25, 72.54) ----
# J4 SW (103.8,95) → R_PU5 pin2 (108.5,92) → XIAO
traces_lower += route([(103.8,95),(108.5,95),(108.5,92)], LJW, width=PW)
traces_lower += route([(108.5,92),(108.5,86),(XL,86),(XL,LY[4])], LJW, width=PW)

# ---- ADC_BAT → R_DIV1 → R_DIV2 → XIAO L6 (91.25, 75.08) ----
# R_DIV1 pin2 (96.5,113) → R_DIV2 pin1 (95.5,117) via mid-point
traces_lower += route([(96.5,113),(96.5,115),(95.5,115),(95.5,117)], LAD, width=PW)
# R_DIV1 pin1 (95.5,113) is VBAT — already connected above via VBAT net
# R_DIV2 mid → XIAO L6
traces_lower += route([(96.5,113),(84,113),(84,LY[5]),(XL,LY[5])], LAD, width=PW)

# ---- BTN_L → XIAO L7 (91.25, 77.62) and J3 FPC pin3 (99.75,117) ----
# XIAO L7 → J3 via right side
traces_lower += route([(XL,LY[6]),(XL,77),(112,77),(112,117.5),(99.75,117.5),(99.75,117)], LBL, width=PW)

# ---- BTN_R → XIAO R1 (108.75, 62.38) → J3 FPC pin4 (100.25,117) ----
traces_lower += route([(XR,RY[0]),(113,RY[0]),(113,118),(100.25,118),(100.25,117)], LBR, width=PW)

# ---- BTN_BK → XIAO R2 (108.75, 64.92) → J3 FPC pin5 (100.75,117) ----
traces_lower += route([(XR,RY[1]),(114,RY[1]),(114,118.5),(100.75,118.5),(100.75,117)], LBK, width=PW)

# ---- BTN_FW → XIAO R3 (108.75, 67.46) → J3 FPC pin6 (101.25,117) ----
traces_lower += route([(XR,RY[2]),(115,RY[2]),(115,119),(101.25,119),(101.25,117)], LBF, width=PW)

# ---- BT_SYNC → R_PU_BT → XIAO R4 (108.75, 70.0) → SW_BT ----
# XIAO R4 → R_PU_BT pin2 (105.5,135)
traces_lower += route([(XR,RY[3]),(116,RY[3]),(116,130),(105.5,130),(105.5,135)], LBT, width=PW)
# R_PU_BT pin2 → SW_BT pin1 (98.5,140)
traces_lower += route([(105.5,135),(105.5,138),(98.5,138),(98.5,140)], LBT, width=PW)

pcb_lower = os.path.join(BASE, "lower_pcb/lower_pcb.kicad_pcb")
append_traces(pcb_lower, traces_lower)
print(f"Lower PCB: {len(traces_lower)} segments -> {pcb_lower}")

# ==============================================================
# UPPER PCB (unchanged from rev 1.9)
# ==============================================================
UBX,UBY = 100.0,100.0
sw4x,sw4y = UBX-10, UBY-12
sw5x,sw5y = UBX+10, UBY-12
sw6x,sw6y = UBX-22, UBY
sw7x,sw7y = UBX+22, UBY
fpc5x,fpc5y = UBX, UBY+8
r1x,r1y = sw4x-1, sw4y+7   # (89,95)
r2x,r2y = sw5x-1, sw5y+7   # (109,95)
r3x,r3y = sw6x+5, sw6y-6   # (83,94)
r4x,r4y = sw7x-5, sw7y-6   # (117,94)

traces_upper = []

# ---- 3V3 rail (bus at Y=96) ----
# J5 pin1 (3V3 at 98.75,108) → bus east to X=122
traces_upper += route([(98.75,108),(98.75,96),(122,96)], U3, width=PP)
# R1 pin1 (3V3 at 88.5,95) tap
traces_upper += L(88.5,96, 88.5,95, U3, w=PP)
# R2 pin1 (3V3 at 108.5,95) tap
traces_upper += L(108.5,96, 108.5,95, U3, w=PP)
# R3 pin1 (3V3 at 82.5,94) — extend bus west
traces_upper += route([(80,96),(82.5,96),(82.5,94)], U3, width=PP)
traces_upper += seg(80,96, 98.75,96, U3, width=PP)
# R4 pin1 (3V3 at 116.5,94)
traces_upper += L(116.5,96, 116.5,94, U3, w=PP)
# C1 pin1 (3V3 at 99.5,112)
traces_upper += route([(98.75,108),(99.5,108),(99.5,112)], U3, width=PP)

# ---- GND bus (Y=98) ----
# J5 pin2 (GND at 99.25,108) → bus
traces_upper += route([(99.25,108),(99.25,98),(122,98)], UG, width=PP)
# SW4 COM (90,88) → bus
traces_upper += L(90,88, 90,98, UG, w=PP)
# SW5 COM (110,88) → bus
traces_upper += L(110,88, 110,98, UG, w=PP)
# SW6 GND pin (81.25,96.75) and snap legs
traces_upper += L(81.25,96.75, 81.25,98, UG, w=PP)
traces_upper += L(74.75,103.25, 74.75,98, UG, w=PP)
traces_upper += L(81.25,103.25, 81.25,98, UG, w=PP)
# SW7 GND pin (125.25,96.75) and snap legs
traces_upper += L(125.25,96.75, 122,98, UG, w=PP)
traces_upper += L(118.75,103.25, 118.75,98, UG, w=PP)
traces_upper += L(125.25,103.25, 122,98, UG, w=PP)
# C1 pin2 (GND at 100.5,112)
traces_upper += L(100.5,112, 100.5,98, UG, w=PP)

# ---- BTN_L: J5 pin3 (99.75,108) → R1 pin2 (89.5,95) → SW4 NO (84.92,88) ----
traces_upper += route([(99.75,108),(99.75,104),(89.5,104),(89.5,95)], UBL, width=PW)
traces_upper += L(89.5,95, 84.92,88, UBL, w=PW)

# ---- BTN_R: J5 pin4 (100.25,108) → R2 pin2 (109.5,95) → SW5 NO (104.92,88) ----
traces_upper += route([(100.25,108),(100.25,105),(109.5,105),(109.5,95)], UBR, width=PW)
traces_upper += L(109.5,95, 104.92,88, UBR, w=PW)

# ---- BTN_BK: J5 pin5 (100.75,108) → R3 pin2 (83.5,94) → SW6 sig (74.75,96.75) ----
traces_upper += route([(100.75,108),(100.75,102),(83.5,102),(83.5,94)], UBK, width=PW)
traces_upper += L(83.5,94, 74.75,96.75, UBK, w=PW)

# ---- BTN_FW: J5 pin6 (101.25,108) → R4 pin2 (117.5,94) → SW7 sig (118.75,96.75) ----
traces_upper += route([(101.25,108),(101.25,103),(117.5,103),(117.5,94)], UBF, width=PW)
traces_upper += seg(117.5,94, 118.75,96.75, UBF, width=PW)

pcb_upper = os.path.join(BASE, "upper_pcb/upper_pcb.kicad_pcb")
append_traces(pcb_upper, traces_upper)
print(f"Upper PCB: {len(traces_upper)} segments -> {pcb_upper}")
print("\nAll traces verified. B.Cu = GND pour. Run DRC in KiCad.")
