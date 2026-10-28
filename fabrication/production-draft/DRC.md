# PCB design-rule report

**Status:** HOLD — electrical DRC blockers present

- Source: `68000sbc.kicad_pcb`
- KiCad: `10.0.7`
- Report time: `2026-10-28T14:24:48`
- Violations: **283**
- Unconnected items: **1**
- Electrical release blockers: **34**

Do not release fabrication files while electrical release blockers remain.

## Counts by rule

| Count | Rule | Release gate |
| ---: | --- | --- |
| 66 | `text_height` | Review |
| 50 | `copper_edge_clearance` | Review |
| 39 | `lib_footprint_mismatch` | Review |
| 34 | `silk_overlap` | Review |
| 16 | `pth_inside_courtyard` | Review |
| 15 | `solder_mask_bridge` | Review |
| 13 | `courtyards_overlap` | Review |
| 11 | `hole_clearance` | Blocker |
| 9 | `starved_thermal` | Review |
| 7 | `shorting_items` | Blocker |
| 5 | `tracks_crossing` | Blocker |
| 5 | `track_dangling` | Blocker |
| 4 | `clearance` | Blocker |
| 4 | `holes_co_located` | Review |
| 2 | `silk_edge_clearance` | Review |
| 1 | `via_dangling` | Blocker |
| 1 | `text_thickness` | Review |
| 1 | `silk_over_copper` | Review |
| 1 | `unconnected_items` | Blocker |

## Electrical release blockers

### `clearance` (4)

- Clearance violation ( clearance 0.1524 mm; actual 0.0000 mm)
    - PTH pad 5 [<no net>] of J1 at (166.37, 110.49)
    - Zone [GND] on F.Cu, priority 0 at (170.18, 129.54)
- Clearance violation ( clearance 0.1524 mm; actual 0.0000 mm)
    - PTH pad 5 [<no net>] of J1 at (166.37, 110.49)
    - Zone [GND] on B.Cu, priority 0 at (170.18, 129.54)
- Clearance violation ( clearance 0.1524 mm; actual 0.0000 mm)
    - PTH pad 5 [<no net>] of J1 at (166.37, 122.53)
    - Zone [GND] on F.Cu, priority 0 at (170.18, 129.54)
- Clearance violation ( clearance 0.1524 mm; actual 0.0000 mm)
    - PTH pad 5 [<no net>] of J1 at (166.37, 122.53)
    - Zone [GND] on B.Cu, priority 0 at (170.18, 129.54)

### `hole_clearance` (11)

- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - Track [<no net>] on B.Cu, length 5.0800 mm at (152.4, 108.585)
    - PTH pad 3 [unconnected-(JP1-B-Pad3)] of JP1 at (152.4, 108.585)
- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - Track [<no net>] on B.Cu, length 3.5921 mm at (161.925, 100.965)
    - PTH pad 3 [unconnected-(J2-Pin_3-Pad3)] of J2 at (159.385, 98.425)
- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - Track [<no net>] on B.Cu, length 2.4950 mm at (161.66, 112.765)
    - PTH pad 1 [unconnected-(J1-VBUS-Pad1)] of J1 at (161.66, 115.26)
- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - Track [<no net>] on B.Cu, length 2.6941 mm at (147.32, 108.585)
    - PTH pad 1 [unconnected-(JP1-A-Pad1)] of JP1 at (147.32, 108.585)
- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - Track [Net-(C11-Pad1)] on F.Cu, length 5.3882 mm at (52.07, 107.95)
    - PTH pad 5 [Net-(R3-Pad1)] of U2 at (48.26, 104.14)
- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - Track [Net-(C11-Pad1)] on B.Cu, length 2.5400 mm at (137.16, 97.79)
    - PTH pad 1 [Net-(R3-Pad1)] of R3 at (134.62, 97.79)
- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - Track [Net-(C11-Pad1)] on B.Cu, length 3.5921 mm at (134.62, 97.79)
    - PTH pad 1 [Net-(R3-Pad1)] of R3 at (134.62, 97.79)
- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - PTH pad 5 [<no net>] of J1 at (166.37, 110.49)
    - Zone [GND] on F.Cu, priority 0 at (170.18, 129.54)
- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - PTH pad 5 [<no net>] of J1 at (166.37, 110.49)
    - Zone [GND] on B.Cu, priority 0 at (170.18, 129.54)
- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - PTH pad 5 [<no net>] of J1 at (166.37, 122.53)
    - Zone [GND] on F.Cu, priority 0 at (170.18, 129.54)
- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - PTH pad 5 [<no net>] of J1 at (166.37, 122.53)
    - Zone [GND] on B.Cu, priority 0 at (170.18, 129.54)

### `shorting_items` (7)

- Items shorting two nets (nets <no net> and unconnected-(J2-Pin_3-Pad3))
    - Track [<no net>] on B.Cu, length 3.5921 mm at (161.925, 100.965)
    - PTH pad 3 [unconnected-(J2-Pin_3-Pad3)] of J2 at (159.385, 98.425)
- Items shorting two nets (nets unconnected-(JP1-B-Pad3) and <no net>)
    - PTH pad 3 [unconnected-(JP1-B-Pad3)] of JP1 at (152.4, 108.585)
    - Track [<no net>] on B.Cu, length 5.0800 mm at (152.4, 108.585)
- Items shorting two nets (nets <no net> and unconnected-(J1-VBUS-Pad1))
    - Track [<no net>] on B.Cu, length 2.4950 mm at (161.66, 112.765)
    - PTH pad 1 [unconnected-(J1-VBUS-Pad1)] of J1 at (161.66, 115.26)
- Items shorting two nets (nets unconnected-(JP1-A-Pad1) and <no net>)
    - PTH pad 1 [unconnected-(JP1-A-Pad1)] of JP1 at (147.32, 108.585)
    - Track [<no net>] on B.Cu, length 2.6941 mm at (147.32, 108.585)
- Items shorting two nets (nets Net-(C11-Pad1) and Net-(R3-Pad1))
    - Track [Net-(C11-Pad1)] on F.Cu, length 5.3882 mm at (52.07, 107.95)
    - PTH pad 5 [Net-(R3-Pad1)] of U2 at (48.26, 104.14)
- Items shorting two nets (nets Net-(R3-Pad1) and Net-(C11-Pad1))
    - PTH pad 1 [Net-(R3-Pad1)] of R3 at (134.62, 97.79)
    - Track [Net-(C11-Pad1)] on B.Cu, length 2.5400 mm at (137.16, 97.79)
- Items shorting two nets (nets Net-(R3-Pad1) and Net-(C11-Pad1))
    - PTH pad 1 [Net-(R3-Pad1)] of R3 at (134.62, 97.79)
    - Track [Net-(C11-Pad1)] on B.Cu, length 3.5921 mm at (134.62, 97.79)

### `track_dangling` (5)

- Track has unconnected end
    - Track [/~{A22}] on F.Cu, length 0.0000 mm at (94.615, 70.485)
- Track has unconnected end
    - Track [/A1] on F.Cu, length 0.0000 mm at (120.015, 73.66)
- Track has unconnected end
    - Track [/A1] on F.Cu, length 0.0000 mm at (111.125, 114.3)
- Track has unconnected end
    - Track [/A3] on F.Cu, length 0.0000 mm at (109.855, 110.49)
- Track has unconnected end
    - Track [/D7] on F.Cu, length 0.0000 mm at (156.21, 72.39)

### `tracks_crossing` (5)

- Tracks crossing
    - Track [/~{A20}] on F.Cu, length 0.0000 mm at (160.655, 46.355)
    - Track [VCC] on F.Cu, length 4.6386 mm at (162.03, 49.0)
- Tracks crossing
    - Track [/A9] on F.Cu, length 0.0000 mm at (112.395, 97.79)
    - Track [/A8] on F.Cu, length 1.7961 mm at (111.125, 97.79)
- Tracks crossing
    - Track [/A15] on F.Cu, length 0.0000 mm at (87.63, 99.06)
    - Track [/A14] on F.Cu, length 3.5921 mm at (86.36, 101.6)
- Tracks crossing
    - Track [/D14] on F.Cu, length 0.0000 mm at (98.425, 69.85)
    - Track [/A3] on F.Cu, length 1.7961 mm at (98.425, 68.58)
- Tracks crossing
    - Track [/RTC_CLK] on F.Cu, length 0.0000 mm at (144.78, 60.96)
    - Track [/D14] on F.Cu, length 1.7961 mm at (143.51, 60.96)

### `unconnected_items` (1)

- Missing connection between items
    - PTH pad 5 [Net-(R3-Pad1)] of U2 at (48.26, 104.14)
    - PTH pad 1 [Net-(R3-Pad1)] of R3 at (134.62, 97.79)

### `via_dangling` (1)

- Via is not connected or connected on only one layer
    - Via [/~{RDU}] on F.Cu - B.Cu at (143.51, 92.71)

