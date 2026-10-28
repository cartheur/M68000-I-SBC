# PCB design-rule report

**Status:** HOLD — electrical DRC blockers present

- Source: `68000sbc.kicad_pcb`
- KiCad: `10.0.7`
- Report time: `2026-10-28T14:54:08`
- Violations: **246**
- Unconnected items: **1**
- Schematic/PCB parity findings: **10**
- Electrical release blockers: **7**

Do not release fabrication files while electrical release blockers remain.

## Counts by rule

| Count | Rule | Release gate |
| ---: | --- | --- |
| 66 | `text_height` | Review |
| 50 | `copper_edge_clearance` | Review |
| 39 | `lib_footprint_mismatch` | Review |
| 34 | `silk_overlap` | Review |
| 16 | `pth_inside_courtyard` | Review |
| 13 | `courtyards_overlap` | Review |
| 7 | `starved_thermal` | Review |
| 7 | `solder_mask_bridge` | Review |
| 4 | `holes_co_located` | Review |
| 3 | `shorting_items` | Blocker |
| 3 | `hole_clearance` | Blocker |
| 2 | `silk_edge_clearance` | Review |
| 1 | `text_thickness` | Review |
| 1 | `silk_over_copper` | Review |
| 1 | `unconnected_items` | Blocker |
| 10 | `schematic_parity` | Blocker |

## Electrical release blockers

### `hole_clearance` (3)

- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - Track [Net-(C11-Pad1)] on F.Cu, length 5.3882 mm at (52.07, 107.95)
    - PTH pad 5 [Net-(R3-Pad1)] of U2 at (48.26, 104.14)
- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - Track [Net-(C11-Pad1)] on B.Cu, length 2.5400 mm at (137.16, 97.79)
    - PTH pad 1 [Net-(R3-Pad1)] of R3 at (134.62, 97.79)
- Hole clearance violation (board setup constraints hole clearance 0.2500 mm; actual 0.0000 mm)
    - Track [Net-(C11-Pad1)] on B.Cu, length 3.5921 mm at (134.62, 97.79)
    - PTH pad 1 [Net-(R3-Pad1)] of R3 at (134.62, 97.79)

### `schematic_parity` (10)

- Duplicate footprints
    - Footprint REF** at (167.64, 41.275)
    - Footprint REF** at (167.64, 127.0)
- Duplicate footprints
    - Footprint REF** at (45.72, 41.275)
    - Footprint REF** at (167.64, 127.0)
- Duplicate footprints
    - Footprint REF** at (45.72, 127.0)
    - Footprint REF** at (167.64, 127.0)
- Extra footprint
    - Footprint U3 at (60.96, 45.72)
- Extra footprint
    - Footprint C11 at (146.685, 100.33)
- Extra footprint
    - Footprint C12 at (153.035, 100.33)
- Extra footprint
    - Footprint REF** at (167.64, 127.0)
- Extra footprint
    - Footprint REF** at (167.64, 41.275)
- Extra footprint
    - Footprint REF** at (45.72, 41.275)
- Extra footprint
    - Footprint REF** at (45.72, 127.0)

### `shorting_items` (3)

- Items shorting two nets (nets Net-(C11-Pad1) and Net-(R3-Pad1))
    - Track [Net-(C11-Pad1)] on F.Cu, length 5.3882 mm at (52.07, 107.95)
    - PTH pad 5 [Net-(R3-Pad1)] of U2 at (48.26, 104.14)
- Items shorting two nets (nets Net-(R3-Pad1) and Net-(C11-Pad1))
    - PTH pad 1 [Net-(R3-Pad1)] of R3 at (134.62, 97.79)
    - Track [Net-(C11-Pad1)] on B.Cu, length 2.5400 mm at (137.16, 97.79)
- Items shorting two nets (nets Net-(R3-Pad1) and Net-(C11-Pad1))
    - PTH pad 1 [Net-(R3-Pad1)] of R3 at (134.62, 97.79)
    - Track [Net-(C11-Pad1)] on B.Cu, length 3.5921 mm at (134.62, 97.79)

### `unconnected_items` (1)

- Missing connection between items
    - PTH pad 5 [Net-(R3-Pad1)] of U2 at (48.26, 104.14)
    - PTH pad 1 [Net-(R3-Pad1)] of R3 at (134.62, 97.79)

