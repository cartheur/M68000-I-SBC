# Tiny68K-derived 68k-nano — production draft

Generated on 2026-10-28 with KiCad 10.0.7 from
`project/68000sbc.kicad_pcb`.

## Fabrication status: HOLD

This is a complete **draft** Gerber/Excellon package for review, not an
approved order package. The accompanying `drc.json` reports 283 violations,
including one unconnected item, seven shorts, five track crossings, five
dangling tracks, four copper-clearance violations, and one dangling via.

Resolve and review all electrical violations before ordering boards. In
particular, DRC reports an open/short conflict between U2 pad 5 and R3 pad 1.
The remaining text, courtyard, and footprint-library messages should then be
triaged separately.

Regenerate the DRC report with `make drc`; it checks both PCB rules and
schematic/PCB parity, then refreshes the KiCad JSON and readable
[`DRC.md`](DRC.md). Use `make fabrication` to refresh the DRC report and all
manufacturing files together.

## Files

| File | Purpose |
| --- | --- |
| `gerbers/68000sbc-F_Cu.gtl` | Front copper |
| `gerbers/68000sbc-B_Cu.gbl` | Back copper |
| `gerbers/68000sbc-F_Mask.gts`, `*-B_Mask.gbs` | Solder mask |
| `gerbers/68000sbc-F_Silkscreen.gto`, `*-B_Silkscreen.gbo` | Silkscreen |
| `gerbers/68000sbc-F_Paste.gtp`, `*-B_Paste.gbp` | Paste/stencil layers |
| `gerbers/68000sbc-Edge_Cuts.gm1` | Board profile |
| `gerbers/68000sbc-PTH.drl` | Plated through-hole drill file |
| `gerbers/68000sbc-NPTH.drl` | Non-plated drill file (contains no holes in this revision) |
| `gerbers/*-drl_map.gbr` | Drill maps |
| `drill-report.txt` | Drill sizes and hole counts |
| `drc.json` | Full KiCad DRC report |

The board is a two-layer stackup. `drill-report.txt` records 666 plated holes
and no non-plated holes. The Gerbers use 6-place precision and the project
plot/drill origin.

## Before release

1. Repair every electrical DRC finding and rerun DRC with no unconnected,
   short, crossing, dangling, or clearance violations.
2. Open the Gerbers in an independent viewer and check board outline,
   copper pours, text, drill alignment, and connector orientation.
3. Confirm the PCB dimensions, finish, stackup, copper weight, mask colour,
   silkscreen, and panelization requirements with the fabricator.
4. Regenerate this directory and create a new dated archive only after the
   board source is committed and DRC-clean.
