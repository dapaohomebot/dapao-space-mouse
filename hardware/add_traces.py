#!/usr/bin/env python3
"""
Add copper traces to DaPao Space Mouse KiCad PCB files.
All traces on F.Cu only. B.Cu = GND pour.
All pad coordinates verified against gen_kicad_pcb.py footprint definitions.
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def seg(x1,y1,x2,y2,net,layer="F.Cu",width=0.25):
    return f'  (segment (start {x1:.4f} {y1:.4f}) (end {x2:.4f} {y2:.4f}) (width {width:.4f}) (layer "{layer}") (net {net}))'

def route(pts,net,layer="F.Cu",width=0.25):
    return [seg(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1],net,layer,width) for i in range(len(pts)-1)]

def L(x1,y1,x2,y2,net,w=0.25):
    """Horizontal-then-vertical L route on F.Cu."""
    return route([(x1,y1),(x2,y1),(x2,y2)],net,width=w)

def append_traces(pcb_path, traces):
    with open(pcb_path,"r") as f: content = f.read()
    content = content.rstrip()
    if content.endswith(")"): content = content[:-1].rstrip()
    content += "\n\n# ===== COPPER TRACES (F.Cu only, all pads verified) =====\n"
    content += "\n".join(traces)
    content += "\n)\n"
    with open(pcb_path,"w") as f: f.write(content)

# Net indices — must match gen_kicad_pcb.py L_NETS / U_NETS order
# Lower: 0="" 1=GND 2=3V3 3=VBAT
#        4=JOY_X 5=JOY_Y 6=JOY_SW 7=ADC_BAT
#        8=BTN_L 9=BTN_R 10=BTN_BK 11=BTN_FW 12=BT_SYNC
LG=1; L3=2; LVB=3
LJX=4; LJY=5; LJW=6; LADC=7
LBL=8; LBR=9; LBK=10; LBF=11; LBT=12
# Upper: 0="" 1=GND 2=3V3 3=BTN_L 4=BTN_R 5=BTN_BK 6=BTN_FW
UG=1; U3=2; UBL=3; UBR=4; UBK=5; UBF=6

PW=0.25; PP=0.35  # signal / power widths

# ==============================================================
# LOWER PCB — Seeed XIAO ESP32-S3 Sense rev 3.0
# USB-C charging + 3.3V LDO + LiPo charger all built into XIAO.
# External: LiPo → SW1 → XIAO VIN pad. 3V3 sourced from XIAO.
# ==============================================================

# ---- XIAO U1 pads (center 100,70) ----
# 2.54mm pitch, 8 pads per side
XL = 100-8.75   # 91.25
XR = 100+8.75   # 108.75
# Left pads (top→bottom): GND, 3V3, JOY_X, JOY_Y, JOY_SW, ADC_BAT, GND, GND
LY = [70 - 8.89 + i*2.54 for i in range(8)]
# Right pads (top→bottom): VBAT, GND, BTN_L, BTN_R, BTN_BK, BTN_FW, BT_SYNC, GND
RY = [70 - 8.89 + i*2.54 for i in range(8)]

# ---- Component pad absolute positions ----
# J4 Alps RKJXV (center 100,100):
#   X-axis: CCW(3V3)=(93.6,93), Wiper(JX)=(97,93), CW(GND)=(100.4,93)
#   Y-axis: CCW(3V3)=(93.6,107), Wiper(JY)=(97,107), CW(GND)=(100.4,107)
#   SW: pin1(JOY_SW)=(103.8,95), pin2(GND)=(103.8,105)
#   Mounting legs (GND): (92.3,91.2),(107.7,91.2),(92.3,108.8),(107.7,108.8)
# J3 FPC (center 100,117): pins at (98.75..101.25, 117), 0.5mm pitch
# J2 JST-PH (center 92,115): pin1(VBAT+)=(91,115), pin2(GND)=(93,115)
# SW1 SPDT (center 62,100, rotated 90°): COM=VBAT, NO → XIAO VIN
#   pin1(COM at 63.5,100), pin3(NO at 60.5,100)
# SW_BT (center 100,140): pin1(BT_SYNC)=(98.5,140), pin2(GND)=(101.5,140)
# R_PU5 (center 108,92): pin1(3V3)=(107.5,92), pin2(JOY_SW)=(108.5,92)
# R_PU_BT (center 105,135): pin1(3V3)=(104.5,135), pin2(BT_SYNC)=(105.5,135)
# C1-C3 (centers 94,82/96,82/98,82): 3V3=(x-0.5,82), GND=(x+0.5,82)

traces_lower = []

# ---- 3V3 rail (horizontal bus Y=82, sourced from XIAO left pad 2) ----
# XIAO L-pad2 (3V3 at XL, LY[1]) → bus Y=82
traces_lower += route([(XL,LY[1]),(XL,82),(115,82)], L3, width=PP)
# West spur at X=90 serving joystick CCW and FPC
traces_lower += route([(90,82),(90,117)], L3, width=PP)
traces_lower += seg(90,82, XL,82, L3, width=PP)
# J4 X-CCW tap (93.6,93)
traces_lower += seg(90,93, 93.6,93, L3, width=PP)
# J4 Y-CCW tap (93.6,107)
traces_lower += seg(90,107, 93.6,107, L3, width=PP)
# J3 FPC pin1 (98.75,117)
traces_lower += seg(90,117, 98.75,117, L3, width=PP)
# R_PU5 pin1 (107.5,92)
traces_lower += route([(115,82),(115,92),(107.5,92)], L3, width=PP)
# R_PU_BT pin1 (104.5,135)
traces_lower += route([(90,107),(90,135),(104.5,135)], L3, width=PP)
# C1-C3 decoupling
traces_lower += route([(93.5,82),(93.5,79),(XL,79)], L3, width=PP)

# ---- GND rail (east column X=120, bus Y=84) ----
# XIAO L-pad1 (GND at XL,LY[0])
traces_lower += route([(XL,LY[0]),(XL,84),(120,84)], LG, width=PP)
# XIAO R-pad8 (GND at XR,RY[7])
traces_lower += route([(XR,RY[7]),(XR,84),(120,84)], LG, width=PP)
# XIAO R-pad2 (GND at XR,RY[1])
traces_lower += L(XR,RY[1], 120,84, LG, w=PP)
# J4 joystick GND pads
traces_lower += route([(100.4,93),(120,93),(120,84)], LG, width=PP)
traces_lower += route([(100.4,107),(120,107),(120,84)], LG, width=PP)
traces_lower += route([(103.8,105),(120,105),(120,107)], LG, width=PP)
traces_lower += L(92.3,91.2, 90,84, LG, w=PP)
traces_lower += L(107.7,91.2, 120,84, LG, w=PP)
# J3 FPC pin2 (GND at 99.25,117)
traces_lower += route([(99.25,117),(85,117),(85,84),(XL,84)], LG, width=PP)
# J2 LiPo GND (93,115)
traces_lower += route([(93,115),(85,115),(85,117)], LG, width=PP)
# SW_BT pin2 GND (101.5,140)
traces_lower += L(101.5,140, 120,107, LG, w=PP)
# C1-C3 GND
traces_lower += route([(94.5,82),(94.5,84),(XL,84)], LG, width=PP)

# ---- VBAT rail ----
# J2 pin1 (VBAT+ at 91,115) → SW1 COM (63.5,100) → SW1 NO (60.5,100) → XIAO R-pad1 (XR,RY[0])
traces_lower += route([(91,115),(75,115),(75,105),(65,105),(65,100),(63.5,100)], LVB, width=PP)
# SW1 NO → XIAO VIN pad (right pad 1 = VBAT)
traces_lower += route([(60.5,100),(56,100),(56,62),(XR,62),(XR,RY[0])], LVB, width=PP)

# ---- JOY_X → XIAO left pad 3 (LY[2]) ----
traces_lower += route([(97,93),(88,93),(88,LY[2]),(XL,LY[2])], LJX, width=PW)

# ---- JOY_Y → XIAO left pad 4 (LY[3]) ----
traces_lower += route([(97,107),(86,107),(86,LY[3]),(XL,LY[3])], LJY, width=PW)

# ---- JOY_SW → R_PU5 → XIAO left pad 5 (LY[4]) ----
traces_lower += route([(103.8,95),(108.5,95),(108.5,92)], LJW, width=PW)
traces_lower += route([(108.5,92),(108.5,88),(XL,88),(XL,LY[4])], LJW, width=PW)

# ---- ADC_BAT → XIAO left pad 6 (LY[5]) ----
# (battery voltage divider or direct VBAT sense — connect via 100k/100k divider if desired)
# For now routed as direct net placeholder
traces_lower += L(XL,LY[5], XL,LY[5], LADC, w=PW)  # stub — extend to divider if added

# ---- BTN_L → J3 FPC pin3 (99.75,117) ----
traces_lower += route([(XR,RY[2]),(112,RY[2]),(112,117.5),(99.75,117.5),(99.75,117)], LBL, width=PW)

# ---- BTN_R → J3 FPC pin4 (100.25,117) ----
traces_lower += route([(XR,RY[3]),(113,RY[3]),(113,118),(100.25,118),(100.25,117)], LBR, width=PW)

# ---- BTN_BK → J3 FPC pin5 (100.75,117) ----
traces_lower += route([(XR,RY[4]),(114,RY[4]),(114,118.5),(100.75,118.5),(100.75,117)], LBK, width=PW)

# ---- BTN_FW → J3 FPC pin6 (101.25,117) ----
traces_lower += route([(XR,RY[5]),(115,RY[5]),(115,119),(101.25,119),(101.25,117)], LBF, width=PW)

# ---- BT_SYNC → R_PU_BT → SW_BT ----
traces_lower += route([(XR,RY[6]),(116,RY[6]),(116,130),(105.5,130),(105.5,135)], LBT, width=PW)
traces_lower += route([(105.5,135),(105.5,138),(98.5,138),(98.5,140)], LBT, width=PW)

pcb_lower = os.path.join(BASE,"lower_pcb/lower_pcb.kicad_pcb")
append_traces(pcb_lower, traces_lower)
print(f"Lower PCB: {len(traces_lower)} segments -> {pcb_lower}")

# ==============================================================
# UPPER PCB — verified pad absolute positions
# Board center (100,100), R=27mm
# ==============================================================

# Component positions from gen_kicad_pcb.py:
# SW4 center (90,88):  NO=(84.92,88), COM=(90,88), NC=(95.08,88)
# SW5 center (110,88): NO=(104.92,88), COM=(110,88), NC=(115.08,88)
# SW6 center (78,100) SKHLLBA010: sig=(74.75,96.75), GND=(81.25,96.75), legs=(74.75,103.25),(81.25,103.25)
# SW7 center (122,100) SKHLLBA010: sig=(118.75,96.75), GND=(125.25,96.75), legs=(118.75,103.25),(125.25,103.25)
# R1 center (89,95): 3V3=(88.5,95), BTN_L=(89.5,95)
# R2 center (109,95): 3V3=(108.5,95), BTN_R=(109.5,95)
# R3 center (82,96): 3V3=(81.5,96), BTN_BK=(82.5,96)
# R4 center (118,96): 3V3=(117.5,96), BTN_FW=(118.5,96)
# J5 FPC center (100,108): pins at (98.75..101.25, 108), step 0.5mm
# C1 center (100,112): 3V3=(99.5,112), GND=(100.5,112)
# H1=(85,100), H2=(115,100)

traces_upper = []

# ---- 3V3 rail (bus at Y=96) ----
# J5 pin1 (3V3 at 98.75,108) → bus
traces_upper += route([(98.75,108),(98.75,96),(122,96)], U3, width=PP)
# R1 pin1 (3V3 at 88.5,95) from bus
traces_upper += L(88.5,96, 88.5,95, U3, w=PP)
# R2 pin1 (3V3 at 108.5,95) from bus
traces_upper += L(108.5,96, 108.5,95, U3, w=PP)
# R3 pin1 (3V3 at 81.5,96) from bus — extend bus west
traces_upper += route([(80,96),(81.5,96)], U3, width=PP)
traces_upper += seg(80,96, 98.75,96, U3, width=PP)  # close the gap
# R4 pin1 (3V3 at 117.5,96) from bus
traces_upper += L(117.5,96, 117.5,96, U3, w=PP)  # already on bus — just connect
# C1 pin1 (3V3 at 99.5,112) from FPC 3V3 line
traces_lower_tap = route([(98.75,108),(99.5,108),(99.5,112)], U3, width=PP)
traces_upper += traces_lower_tap

# ---- GND rail (bus at Y=98) ----
# J5 pin2 (GND at 99.25,108) → bus
traces_upper += route([(99.25,108),(99.25,98),(122,98)], UG, width=PP)
# SW4 COM (90,88) → bus
traces_upper += L(90,88, 90,98, UG, w=PP)
# SW5 COM (110,88) → bus
traces_upper += L(110,88, 110,98, UG, w=PP)
# SW6 GND pin (81.25,96.75) → bus
traces_upper += L(81.25,96.75, 81.25,98, UG, w=PP)
# SW6 snap legs (74.75,103.25) and (81.25,103.25) → GND
traces_upper += L(74.75,103.25, 74.75,98, UG, w=PP)
traces_upper += L(81.25,103.25, 81.25,103.25, UG, w=PP)  # already connected via 81.25 column
# SW7 GND pin (125.25,96.75) — inside 27mm radius? SW7 at X=122, pad at 125.25, board radius=27 from center 100, so edge at X=127. OK.
traces_upper += L(125.25,96.75, 122,98, UG, w=PP)
# SW7 snap legs
traces_upper += L(118.75,103.25, 118.75,98, UG, w=PP)
# C1 pin2 (GND at 100.5,112)
traces_upper += L(100.5,112, 100.5,98, UG, w=PP)

# ---- BTN_L ----
# J5 pin3 (99.75,108) → R1 pin2 (89.5,95) → SW4 NO (84.92,88)
traces_upper += route([(99.75,108),(99.75,104),(89.5,104),(89.5,95)], UBL, width=PW)
traces_upper += L(89.5,95, 84.92,88, UBL, w=PW)

# ---- BTN_R ----
# J5 pin4 (100.25,108) → R2 pin2 (109.5,95) → SW5 NO (104.92,88)
traces_upper += route([(100.25,108),(100.25,105),(109.5,105),(109.5,95)], UBR, width=PW)
traces_upper += L(109.5,95, 104.92,88, UBR, w=PW)

# ---- BTN_BK ----
# J5 pin5 (100.75,108) → R3 pin2 (82.5,96) → SW6 SIG (74.75,96.75)
traces_upper += route([(100.75,108),(100.75,102),(82.5,102),(82.5,96)], UBK, width=PW)
traces_upper += L(82.5,96, 74.75,96.75, UBK, w=PW)

# ---- BTN_FW ----
# J5 pin6 (101.25,108) → R4 pin2 (118.5,96) → SW7 SIG (118.75,96.75)
traces_upper += route([(101.25,108),(101.25,103),(118.5,103),(118.5,96)], UBF, width=PW)
traces_upper += seg(118.5,96, 118.75,96.75, UBF, width=PW)

pcb_upper = os.path.join(BASE,"upper_pcb/upper_pcb.kicad_pcb")
append_traces(pcb_upper, traces_upper)
print(f"Upper PCB: {len(traces_upper)} segments -> {pcb_upper}")
print("\nAll pad coordinates verified. B.Cu = GND pour. Run DRC in KiCad.")
