# DaPao Space Mouse — Full Bill of Materials

**Lower PCB rev 1.3** (dia88mm) + **Upper PCB rev 1.3** (dia54mm)  
**Branch:** `feat/split-3d-parts`  

---

## LOWER PCB Components

### U1 — XIAO ESP32-S3 (Main MCU)
**Location:** North half of board, USB-C end facing north/forward board edge  
**Description:** Seeed Studio castellated module. Brain of the device — reads joystick, buttons, runs BLE/WiFi, handles USB HID.  
| | |
|---|---|
| **Buy** | <https://www.seeedstudio.com/XIAO-ESP32S3-p-5627.html> |
| **LCSC** | C5439723 |
| **Datasheet** | <https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/esp32-s3_datasheet.pdf> |
| **Schematic** | <https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_SCH_v1.1.pdf> |
| **Price** | ~$7.99 ea |
| **Qty** | 1 |
| **PCB Label** | `U1` |

---

### U2 — TP4056 (LiPo Charger IC)
**Location:** NE quadrant, between XIAO and board edge  
**Description:** Single-cell LiPo charger. Receives power from USB-C (VBUS), charges battery at 500mA (set by R7). Has charge (RED) and standby (GREEN) LED outputs.  
| | |
|---|---|
| **Buy** | <https://www.lcsc.com/product-detail/Battery-Management_TPTEK-TP4056_C382139.html> |
| **LCSC** | C382139 |
| **Datasheet** | <https://www.lcsc.com/datasheet/lcsc_datasheet_TP4056_C382139.pdf> |
| **Price** | ~$0.08 ea |
| **Qty** | 1 |
| **Package** | SOP-8 |
| **PCB Label** | `U2` |

---

### U3 — AP2112K-3.3V (LDO Voltage Regulator)
**Location:** East side of board, between joystick center and board edge  
**Description:** Low-dropout regulator. Converts battery voltage (3.7V nominal) to clean 3.3V for the XIAO and all other logic. Only powered when SW1 (master power switch) is ON.  
| | |
|---|---|
| **Buy** | <https://www.lcsc.com/product-detail/LDO-Voltage-Regulators_Diodes-Incorporated-AP2112K-3-3TRG1_C51118.html> |
| **LCSC** | C51118 |
| **Datasheet** | <https://www.diodes.com/assets/Datasheets/AP2112.pdf> |
| **Price** | ~$0.09 ea |
| **Qty** | 1 |
| **Package** | SOT-23-5 |
| **PCB Label** | `U3` |

---

### U4 — USBLC6-2SC6 (USB ESD Protection)
**Location:** NE quadrant, directly adjacent to J1 USB-C connector  
**Description:** Bidirectional ESD protection on USB D+/D- lines. Clamps voltage spikes to protect the XIAO from static discharge through the USB port.  
| | |
|---|---|
| **Buy** | <https://www.lcsc.com/product-detail/TVS-ESD-Protection_ST-USBLC6-2SC6_C7519.html> |
| **LCSC** | C7519 |
| **Datasheet** | <https://www.st.com/resource/en/datasheet/usblc6-2.pdf> |
| **Price** | ~$0.05 ea |
| **Qty** | 1 |
| **Package** | SOT-23-6 |
| **PCB Label** | `U4` |

---

### J1 — USB-C Receptacle (Charging + Data)
**Location:** North board edge, pointing forward (flush with case front)  
**Description:** Mid-mount USB-C port. Used for LiPo charging (via U2) and USB HID data to computer. CC resistors R10/R11 set it to 5V/900mA device mode.  
| | |
|---|---|
| **Buy** | <https://www.lcsc.com/product-detail/USB-Connectors_Korean-Hroparts-Elec-TYPE-C-31-M-12_C165948.html> |
| **LCSC** | C165948 |
| **Datasheet** | <https://datasheet.lcsc.com/lcsc/1811141125_Korean-Hroparts-Elec-TYPE-C-31-M-12_C165948.pdf> |
| **Price** | ~$0.14 ea |
| **Qty** | 1 |
| **PCB Label** | `J1` |

---

### J2 — JST-PH 2-pin (Battery Connector)
**Location:** SW quadrant, near board edge  
**Description:** Right-angle connector for the LiPo battery. Pin 1 = BAT+, Pin 2 = GND. Mates with standard JST-PH pigtail on most 3.7V LiPo cells.  
| | |
|---|---|
| **Buy** | <https://www.lcsc.com/product-detail/Wire-To-Board-Connector_JST-B2B-PH-K-S-LF-SN_C131337.html> |
| **LCSC** | C131337 |
| **Datasheet** | <https://datasheet.lcsc.com/lcsc/1811191652_JST-B2B-PH-K-S-LF-SN_C131337.pdf> |
| **Battery** | <https://www.amazon.com/s?k=lipo+battery+3.7v+400mah+jst-ph> |
| **Price** | ~$0.05 ea |
| **Qty** | 1 |
| **PCB Label** | `J2` |

---

### J3 — FPC Connector 6-pin 0.5mm (Ribbon Cable — Lower PCB)
**Location:** Center-south of board, between joystick module and south edge  
**Description:** Top-contact FPC connector. The 6-pin ribbon cable runs upward through the body shell to J5 on the upper PCB. Carries 3V3, GND, and 4 button signals.  
Pinout: `1=3V3  2=GND  3=BTN_L  4=BTN_R  5=BTN_BK  6=BTN_FW`  
| | |
|---|---|
| **Buy** | <https://www.lcsc.com/product-detail/FFC-FPC-Connectors_BOOMELE-Boom-Precision-Elec-C11021_C11021.html> |
| **LCSC** | C11021 |
| **Datasheet** | <https://datasheet.lcsc.com/lcsc/1809301247_BOOMELE-Boom-Precision-Elec-C11021_C11021.pdf> |
| **Cable** | <https://www.lcsc.com/product-detail/FFC-FPC-Cables_Cvilux-CF05S06VFB0R_C2683542.html> |
| **Price** | ~$0.06 ea connector, ~$0.15 cable |
| **Qty** | 1 connector + 1 cable |
| **PCB Label** | `J3` |

---

### J4 — Analog Joystick Module (Thumbstick)
**Location:** Board center (mounted on PCB surface, shaft points up through body shell)  
**Description:** 5-pin right-angle header accepts a KY-023-style analog joystick module. X/Y analog outputs go to XIAO GPIO1/GPIO2. Pushdown click goes to GPIO3. The joystick shaft pokes up through the body shell coupler.  
| | |
|---|---|
| **Buy (module)** | <https://www.amazon.com/s?k=KY-023+joystick+module> |
| **Buy (header)** | <https://www.lcsc.com/product-detail/Pin-Headers_2-54mm-5P-Straight_C124387.html> |
| **Datasheet** | <https://arduinomodules.info/ky-023-joystick-dual-axis-module/> |
| **Price** | ~$1.50 module |
| **Qty** | 1 |
| **PCB Label** | `J4` |

---

### J5 — FPC Connector 6-pin 0.5mm (Ribbon Cable — Upper PCB)
**Location:** Center-bottom of upper PCB (dia54mm board)  
**Description:** Identical to J3 — top-contact FPC, receives the ribbon cable from the lower PCB. Same pinout.  
| | |
|---|---|
| **Buy** | <https://www.lcsc.com/product-detail/FFC-FPC-Connectors_BOOMELE-Boom-Precision-Elec-C11021_C11021.html> |
| **LCSC** | C11021 |
| **Price** | ~$0.06 ea |
| **Qty** | 1 |
| **PCB Label** | `J5` |

---

### SW1 — SPDT Slide Switch (Master Power)
**Location:** West board edge, accessible through base_ring cutout  
**Description:** Master ON/OFF switch. Sits between battery BAT+ and the LDO (U3). Cutting power here shuts off the 3V3 rail and the XIAO. USB charging still works with SW1 OFF.  
| | |
|---|---|
| **Buy** | <https://www.lcsc.com/product-detail/Slide-Switches_SHOU-HAN-MSK-12C02_C431541.html> |
| **LCSC** | C431541 |
| **Datasheet** | <https://datasheet.lcsc.com/lcsc/2009041608_SHOU-HAN-MSK-12C02_C431541.pdf> |
| **Price** | ~$0.04 ea |
| **Qty** | 1 |
| **Package** | SMD, 7x3mm |
| **PCB Label** | `SW1` |

---

### SW2 — Tactile Switch (BOOT)
**Location:** East of XIAO, near top of module  
**Description:** Boot mode button for XIAO ESP32-S3. Hold while pressing SW3 (RESET) to enter download mode for firmware flashing. Pulls GPIO0 LOW when pressed.  
| | |
|---|---|
| **Buy** | <https://www.lcsc.com/product-detail/Tactile-Switches_XUNPU-TS-1101H-C_C318884.html> |
| **LCSC** | C318884 |
| **Price** | ~$0.02 ea |
| **Qty** | 1 |
| **Package** | SMD 3x4mm |
| **PCB Label** | `SW2-BOOT` |

---

### SW3 — Tactile Switch (RESET)
**Location:** East of XIAO, below SW2  
**Description:** Hardware reset for XIAO ESP32-S3. Pulls EN pin LOW when pressed. Press alone to reboot; press with SW2 held to enter firmware flash mode.  
| | |
|---|---|
| **Buy** | <https://www.lcsc.com/product-detail/Tactile-Switches_XUNPU-TS-1101H-C_C318884.html> |
| **LCSC** | C318884 |
| **Price** | ~$0.02 ea |
| **Qty** | 1 |
| **Package** | SMD 3x4mm |
| **PCB Label** | `SW3-RST` |

---

### SW_BT — Tactile Switch (Bluetooth Sync)
**Location:** South board edge, accessible through base_ring cutout  
**Description:** Bluetooth pairing/reconnect button. Tap = reconnect to last paired device. Hold 3 seconds = enter BLE pairing mode. Pulls GPIO9 LOW when pressed, 10k pull-up (R_PU_BT) to 3V3.  
| | |
|---|---|
| **Buy** | <https://www.lcsc.com/product-detail/Tactile-Switches_XUNPU-TS-1101H-C_C318884.html> |
| **LCSC** | C318884 |
| **Price** | ~$0.02 ea |
| **Qty** | 1 |
| **Package** | SMD 3x4mm |
| **PCB Label** | `SW_BT` |

---

### SW4, SW5 — Kailh GM 8.0 (L/R Click — Upper PCB)
**Location:** Upper PCB, left and right of center, under rocker buttons  
**Description:** Cherry MX-compatible 3-pin THT click switches. SW4 = Left click (BTN_L), SW5 = Right click (BTN_R). Plunger faces UP and is pressed by a nub on the underside of the rocker button cap.  
COM pin → GND, NO pin → BTN signal, NC pin left floating.  
| | |
|---|---|
| **Buy** | <https://www.lcsc.com/product-detail/Mouse-Switches_Kailh-CPG3280B11-GM8-0_C5333969.html> |
| **LCSC** | C5333969 |
| **Datasheet** | <https://datasheet.lcsc.com/lcsc/2012171437_Kailh-CPG3280B11-GM8-0_C5333969.pdf> |
| **Price** | ~$0.80 ea |
| **Qty** | 2 |
| **Package** | THT, 12.8×5.8mm, 1.5mm drill |
| **PCB Label** | `SW4`, `SW5` |

---

### SW6, SW7 — Kailh Blue Dot SMD (Back/Fwd — Upper PCB)
**Location:** Upper PCB, left and right board edges  
**Description:** Side-actuated SMD tactile switches. SW6 = Back (BTN_BK), SW7 = Forward (BTN_FW). Plunger faces outward through a cutout in the top_frame wall and is pressed by a side button cap.  
| | |
|---|---|
| **Buy** | <https://www.kailhswitch.com/Info/kailh-mini-micro-switch-for-mouse-blue-dot-4.html> |
| **Alt buy** | <https://www.aliexpress.com/item/1005004065562445.html> |
| **Datasheet** | <https://www.kailhswitch.com/uploads/202012111045162.pdf> |
| **Price** | ~$0.60 ea |
| **Qty** | 2 |
| **Package** | SMD, 2-pin, 1.8×2.8mm pads, 5mm pitch |
| **PCB Label** | `SW6-BCK`, `SW7-FWD` |

---

## Passive Components

### Resistors (all 0402 1% unless noted)
| Ref | Value | Function | Location | LCSC | Buy |
|---|---|---|---|---|---|
| R1 | 10kΩ | BTN_L pull-up | Upper PCB, near SW4 | C25804 | <https://www.lcsc.com/product-detail/Chip-Resistor-Surface-Mount_UNI-ROYAL-Uniroyal-Elec-0402WGF1002TCE_C25804.html> |
| R2 | 10kΩ | BTN_R pull-up | Upper PCB, near SW5 | C25804 | (same) |
| R3 | 10kΩ | BTN_BK pull-up | Upper PCB, near SW6 | C25804 | (same) |
| R4 | 10kΩ | BTN_FW pull-up | Upper PCB, near SW7 | C25804 | (same) |
| R_PU5 | 10kΩ | JOY_SW pull-up | Lower PCB, near J4 | C25804 | (same) |
| R_PU_BT | 10kΩ | BT_SYNC pull-up | Lower PCB, near SW_BT | C25804 | (same) |
| R5 | 100kΩ | VBAT sense divider top | Lower PCB, near XIAO | C25803 | <https://www.lcsc.com/product-detail/Chip-Resistor-Surface-Mount_UNI-ROYAL-Uniroyal-Elec-0402WGF1003TCE_C25803.html> |
| R6 | 100kΩ | VBAT sense divider bottom | Lower PCB, near XIAO | C25803 | (same) |
| R7 | 2kΩ | TP4056 PROG (500mA charge) | Lower PCB, near U2 | C25879 | <https://www.lcsc.com/product-detail/Chip-Resistor-Surface-Mount_UNI-ROYAL-Uniroyal-Elec-0402WGF2001TCE_C25879.html> |
| R8 | 1kΩ | LED1 current limit (CHG) | Lower PCB, near U2 | C11702 | <https://www.lcsc.com/product-detail/Chip-Resistor-Surface-Mount_UNI-ROYAL-Uniroyal-Elec-0402WGF1001TCE_C11702.html> |
| R9 | 1kΩ | LED2 current limit (STDBY) | Lower PCB, near U2 | C11702 | (same) |
| R10 | 5.1kΩ | USB-C CC1 | Lower PCB, near J1 | C23186 | <https://www.lcsc.com/product-detail/Chip-Resistor-Surface-Mount_UNI-ROYAL-Uniroyal-Elec-0402WGF5101TCE_C23186.html> |
| R11 | 5.1kΩ | USB-C CC2 | Lower PCB, near J1 | C23186 | (same) |

### Capacitors
| Ref | Value | Function | Location | LCSC | Buy |
|---|---|---|---|---|---|
| C1 (lower) | 10µF 0805 | VBUS bulk decoupling | Lower PCB, near J1 | C15850 | <https://www.lcsc.com/product-detail/Multilayer-Ceramic-Capacitors-MLCC-SMD-SMT_Samsung-Electro-Mechanics-CL21A106KAYNNNE_C15850.html> |
| C2 | 10µF 0805 | BAT+ bulk decoupling | Lower PCB, near J2 | C15850 | (same) |
| C3 | 10µF 0805 | 3V3 bulk decoupling | Lower PCB, near U3 | C15850 | (same) |
| C4–C7 | 100nF 0402 | 3V3 rail decoupling | Lower PCB, near U1 | C1525 | <https://www.lcsc.com/product-detail/Multilayer-Ceramic-Capacitors-MLCC-SMD-SMT_Samsung-Electro-Mechanics-CL05B104KO5NNNC_C1525.html> |
| C1 (upper) | 100nF 0402 | 3V3 decoupling on upper PCB | Upper PCB, center | C1525 | (same) |

### LEDs
| Ref | Color | Function | Location | LCSC | Buy |
|---|---|---|---|---|---|
| LED1 | Red 0402 | Charging indicator (ON while charging) | Lower PCB, NE near U2 | C2286 | <https://www.lcsc.com/product-detail/Light-Emitting-Diodes-LED_Hubei-KENTO-Elec-C2286_C2286.html> |
| LED2 | Green 0402 | Standby indicator (ON when full/idle) | Lower PCB, NE near U2 | C2290 | <https://www.lcsc.com/product-detail/Light-Emitting-Diodes-LED_Hubei-KENTO-Elec-C2290_C2290.html> |

---

## Mechanical / Fasteners
| Item | Spec | Function | Buy |
|---|---|---|---|
| LiPo battery | 3.7V 400mAh JST-PH | Power source | <https://www.amazon.com/s?k=lipo+3.7v+400mah+JST-PH+2pin> |
| M2×6mm screws | Phillips head | Mount lower PCB to base_ring (×4) | <https://www.amazon.com/s?k=M2+6mm+screws> |
| M2×4mm screws | Phillips head | Mount upper PCB to top_frame (×2) | (same kit) |
| M2 heat-set inserts | 3.2mm OD | Press into printed posts | <https://www.amazon.com/s?k=M2+heat+set+inserts> |
| FPC cable 6-pin 0.5mm | ~80mm same-side | Lower J3 ↔ Upper J5 | <https://www.lcsc.com/product-detail/FFC-FPC-Cables_Cvilux-CF05S06VFB0R_C2683542.html> |

---

## Cost Summary (approximate per unit)
| Section | Cost |
|---|---|
| Lower PCB (JLCPCB, 5 boards) | ~$10 / 5 = $2 ea |
| Upper PCB (JLCPCB, 5 boards) | ~$8 / 5 = $1.60 ea |
| XIAO ESP32-S3 | $7.99 |
| ICs (TP4056, LDO, ESD) | ~$0.25 |
| Connectors (USB-C, JST, FPC×2) | ~$0.40 |
| Kailh GM 8.0 ×2 | $1.60 |
| Kailh Blue Dot ×2 | $1.20 |
| Passives (resistors, caps, LEDs) | ~$0.50 |
| Joystick module | $1.50 |
| LiPo battery | ~$4.00 |
| Switches (SW1, SW2, SW3, SW_BT) | ~$0.10 |
| Fasteners + misc | ~$1.00 |
| **Total per unit (excl. 3D print)** | **~$22** |
