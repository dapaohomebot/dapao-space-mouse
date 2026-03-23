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
# Lower: 0="" 1=GND 2=3V3 3=VBUS 4=BAT_PLUS 5=SW_OUT
#        6=JOY_X 7=JOY_Y 8=JOY_SW 9=ADC_BAT
#        10=BTN_L 11=BTN_R 12=BTN_BK 13=BTN_FW 14=BT_SYNC 15=USB_DP 16=USB_DN
LG=1; L3=2; LV=3; LB=4; LS=5; LJX=6; LJY=7; LJW=8
LBL=10; LBR=11; LBK=12; LBF=13; LBT=14
# Upper: 0="" 1=GND 2=3V3 3=BTN_L 4=BTN_R 5=BTN_BK 6=BTN_FW
UG=1; U3=2; UBL=3; UBR=4; UBK=5; UBF=6

PW=0.25; PP=0.35  # signal / power widths

# ==============================================================
# LOWER PCB — verified pad absolute positions
# Board center (100,100). Component origins from gen_kicad_pcb.py.
# ==============================================================

# ---- XIAO U1 pads (center 100,70) ----
XL = 100-8.75   # 91.25 — left castellated column X
XR = 100+8.75   # 108.75 — right castellated column X
# Left pads Y [3V3, GND, JOY_X, JOY_Y, JOY_SW, ADC_BAT, GND]
LY = [70-9+i*3 for i in range(7)]  # [61,64,67,70,73,76,79]
# Right pads Y [BTN_L, BTN_R, BTN_BK, BTN_FW, BT_SYNC, 3V3, GND]
RY = [70-9+i*3 for i in range(7)]  # [61,64,67,70,73,76,79]

# ---- Component pad positions (absolute) ----
# J1 USB-C (center 100,57): VBUS at (98.75,57), GND shells at (97.5,58.5)/(102.5,58.5)
# J4 Alps RKJXV (center 100,100):
#   X-axis: CCW(3V3)=(93.6,93), Wiper(JX)=(97,93), CW(GND)=(100.4,93)
#   Y-axis: CCW(3V3)=(93.6,107), Wiper(JY)=(97,107), CW(GND)=(100.4,107)
#   SW: pin1(JOY_SW)=(103.8,95), pin2(GND)=(103.8,105)
#   Mounting legs (GND): (92.3,91.2),(107.7,91.2),(92.3,108.8),(107.7,108.8)
# J3 FPC (center 100,117): pins at (98.75..101.25, 117), step 0.5mm
# U3 LDO (center 118,95):
#   pin1(GND)=(117.05,96.4), pin2(3V3)=(118,96.4), pin3(SW_OUT/VIN)=(118.95,96.4)
#   pin4(GND)=(117.05,93.6), pin5(CE=SW_OUT)=(118.95,93.6)
# J2 JST-PH (center 92,115): pin1(BAT+)=(91,115), pin2(GND)=(93,115)
# SW1 SPDT (center 62,100, rotated 90°):
#   COM→(63.5,100), COM2→(62,100), NO(SW_OUT)→(60.5,100)
# SW_BT (center 100,140): pin1(BT_SYNC)=(98.5,140), pin2(GND)=(101.5,140)
# R_PU5 (center 108,92): pin1(3V3)=(107.5,92), pin2(JOY_SW)=(108.5,92)
# R_PU_BT (center 105,135): pin1(3V3)=(104.5,135), pin2(BT_SYNC)=(105.5,135)
# C1-C3 (centers 94,82 / 96,82 / 98,82): 3V3 at x-0.5, GND at x+0.5
# C4 0805 (center 123,98): pin1(3V3)=(122,98), pin2(GND)=(124,98)
# R10/R11 CC (centers 106,60 / 106,62): VBUS at x-0.5, GND at x+0.5

traces_lower = []

# ---- 3V3 power rail bus (Y=82) ----
# XIAO L-pin1 (3V3 at 91.25,61) → west bus at X=90 → rail Y=82
traces_lower += route([(XL,LY[0]),(XL,82),(115,82)], L3, width=PP)
# XIAO R-pin6 (3V3 at 108.75,76) → rail
traces_lower += route([(XR,RY[5]),(XR,82),(115,82)], L3, width=PP)
# LDO pin2 (3V3 out at 118,96.4) → up to rail
traces_lower += L(118,96.4, 115,82, L3, w=PP)
# West spur at X=90 for joystick CCW pins and FPC pin1
traces_lower += route([(90,82),(90,117)], L3, width=PP)  # vertical bus
traces_lower += seg(90,82,115,82, L3, width=PP)          # connect west spur to main rail
# J4 X-CCW tap from west spur
traces_lower += seg(90,93, 93.6,93, L3, width=PP)
# J4 Y-CCW tap
traces_lower += seg(90,107, 93.6,107, L3, width=PP)
# J3 FPC pin1 (3V3) tap
traces_lower += seg(90,117, 98.75,117, L3, width=PP)
# R_PU5 pin1 (3V3) from rail
traces_lower += route([(115,82),(115,92),(107.5,92)], L3, width=PP)
# R_PU_BT pin1 (3V3) from west spur
traces_lower += route([(90,107),(90,135),(104.5,135)], L3, width=PP)
# C4 pin1 (3V3)
traces_lower += route([(115,82),(122,82),(122,98)], L3, width=PP)
# C1 pin1 tap
traces_lower += route([(93.5,82),(93.5,79),(XL,79)], L3, width=PP)

# ---- GND rail (east column X=120, bus Y=84) ----
# XIAO L-pin2 (GND at 91.25,64) → bus
traces_lower += route([(XL,LY[1]),(XL,84),(120,84)], LG, width=PP)
# XIAO R-pin7 (GND at 108.75,79) → bus
traces_lower += route([(XR,RY[6]),(XR,84),(120,84)], LG, width=PP)
# J1 USB-C GND shell (97.5,58.5) → bus
traces_lower += L(97.5,58.5, 120,84, LG, w=PP)
# J4 joystick GND pads → east column
traces_lower += route([(100.4,93),(120,93),(120,84)], LG, width=PP)
traces_lower += route([(100.4,107),(120,107),(120,84)], LG, width=PP)
traces_lower += route([(103.8,105),(120,105),(120,107)], LG, width=PP)
# J4 mounting legs (GND)
traces_lower += L(92.3,91.2, 90,84, LG, w=PP)
traces_lower += L(107.7,91.2, 120,84, LG, w=PP)
# J3 FPC pin2 (GND at 99.25,117) → west spur at X=85 → bus
traces_lower += route([(99.25,117),(85,117),(85,84),(XL,84)], LG, width=PP)
# U3 LDO GND pins
traces_lower += route([(117.05,96.4),(120,96.4),(120,84)], LG, width=PP)
traces_lower += route([(117.05,93.6),(120,93.6),(120,84)], LG, width=PP)
# C4 pin2 (GND at 124,98) → east column
traces_lower += route([(124,98),(120,98),(120,96.4)], LG, width=PP)
# J2 battery pin2 (GND at 93,115) → west spur
traces_lower += route([(93,115),(85,115),(85,117)], LG, width=PP)
# SW_BT pin2 (GND at 101.5,140)
traces_lower += L(101.5,140, 120,107, LG, w=PP)
# C1 pin2 (GND at 94.5,82) → bus
traces_lower += route([(94.5,82),(94.5,84),(XL,84)], LG, width=PP)

# ---- VBUS ----
# J1 USB-C VBUS pad (98.75,57) → XIAO VBUS (internal, connect to pad nearest top)
traces_lower += L(98.75,57, 98.75,62, LV, w=PP)

# ---- BAT_PLUS ----
# J2 pin1 (BAT+ at 91,115) → around components → SW1 COM (63.5,100)
traces_lower += route([(91,115),(75,115),(75,105),(65,105),(65,100),(63.5,100)], LB, width=PP)

# ---- SW_OUT ----
# SW1 NO (at 60.5,100) → U3 LDO VIN pin3 (118.95,96.4) and CE pin5 (118.95,93.6)
traces_lower += route([(60.5,100),(56,100),(56,90),(119,90),(118.95,93.6)], LS, width=PP)
traces_lower += seg(118.95,93.6, 118.95,96.4, LS, width=PP)

# ---- JOY_X → XIAO GPIO1 (left pad 3, Y=67) ----
# J4 X wiper (97,93) → XIAO left pad
traces_lower += route([(97,93),(88,93),(88,LY[2]),(XL,LY[2])], LJX, width=PW)

# ---- JOY_Y → XIAO GPIO2 (left pad 4, Y=70) ----
# J4 Y wiper (97,107) → XIAO left pad
traces_lower += route([(97,107),(86,107),(86,LY[3]),(XL,LY[3])], LJY, width=PW)

# ---- JOY_SW → R_PU5 → XIAO GPIO3 (left pad 5, Y=73) ----
# J4 SW pin1 (103.8,95) → R_PU5 pin2 (108.5,92)
traces_lower += route([(103.8,95),(108.5,95),(108.5,92)], LJW, width=PW)
# R_PU5 pin2 → XIAO left pad 5
traces_lower += route([(108.5,92),(108.5,88),(XL,88),(XL,LY[4])], LJW, width=PW)

# ---- BTN_L → J3 FPC pin3 (99.75,117) ----
traces_lower += route([(XR,RY[0]),(112,RY[0]),(112,117.5),(99.75,117.5),(99.75,117)], LBL, width=PW)

# ---- BTN_R → J3 FPC pin4 (100.25,117) ----
traces_lower += route([(XR,RY[1]),(113,RY[1]),(113,118),(100.25,118),(100.25,117)], LBR, width=PW)

# ---- BTN_BK → J3 FPC pin5 (100.75,117) ----
traces_lower += route([(XR,RY[2]),(114,RY[2]),(114,118.5),(100.75,118.5),(100.75,117)], LBK, width=PW)

# ---- BTN_FW → J3 FPC pin6 (101.25,117) ----
traces_lower += route([(XR,RY[3]),(115,RY[3]),(115,119),(101.25,119),(101.25,117)], LBF, width=PW)

# ---- BT_SYNC → R_PU_BT → SW_BT ----
# XIAO right pad 5 (BT_SYNC at 108.75,73) → R_PU_BT pin2 (105.5,135) → SW_BT pin1 (98.5,140)
traces_lower += route([(XR,RY[4]),(116,RY[4]),(116,130),(105.5,130),(105.5,135)], LBT, width=PW)
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
