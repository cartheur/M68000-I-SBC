# Manufacturing-readiness gate

## Current status: HOLD

This package is not ready for fabrication or assembly release. The current
parity-inclusive DRC has 34 electrical blockers and 11 schematic/PCB parity
findings; see [DRC.md](DRC.md).

The most important parity defects are:

- U3 (the 68000), C11, and C12 exist on the PCB but are absent from the
  schematic BOM.
- Four unannotated `REF**` footprints exist on the PCB.
- J1's shield pin has no matching schematic pad.
- X1 and X2 are overlapping alternative oscillator footprints and must be
  modelled as a mutually exclusive, explicitly documented choice.

## Published draft inputs

- [KiCad BOM export](kicad-bom.csv) is the current schematic-derived source.
- [Full placement export](full-placement.csv) is retained for review.
- [Socket CPL](socket-cpl.csv) places only the eight IC sockets; it deliberately
  excludes all ICs.
- [Mouser socket BOM](mouser-socket-bom.csv) specifies compatible Omron XR2A
  sockets by manufacturer part number and links each line to a Mouser search.

## Socket-CPL import notes

The socket CPL uses KiCad's current board coordinate system in millimetres.
All placements are on the top side and rotated 0 degrees. A specific assembler
may require a translated origin, alternate rotation convention, or a
vendor-specific column order; transform only after a first-article placement
review. The file is intentionally generic until an assembly house is selected.

## Release sequence

1. Repair schematic/PCB parity and all electrical DRC violations.
2. Add validated manufacturer and Mouser fields to every schematic symbol.
3. Regenerate `kicad-bom.csv`, placement exports, and the socket CPL.
4. Validate the selected socket footprint against the manufacturer drawing and
   obtain an assembly-house-specific CPL import template.
5. Run `make fabrication`, review the Gerbers independently, and freeze a
   committed revision before ordering.
