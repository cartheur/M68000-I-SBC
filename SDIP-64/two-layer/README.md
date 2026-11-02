# Two-layer SDIP64-to-DIP64 production adapter

`SDIP64-to-DIP64-two-layer.kicad_pcb` is the authoritative, fully routed
two-copper-layer TMP68HC000N SDIP-64 to SBC U3 DIP-64 adapter. It is a direct
1:1 translation: upper pin *n* connects only to host pin *n*.

The finished outline is **42.16 × 92.20 mm**. It uses only `F.Cu` and `B.Cu`,
with 0.20 mm tracks and 0.20 mm spacing. Pin numbers are on `F.SilkS` outside
both 32-pin host rows.

## Preproduction status

`final-preproduction-drc.rpt` records the final KiCad check: **0 violations,
0 unconnected pads, and 0 footprint errors**. Temporary Gerber and Excellon
drill exports were generated successfully from this exact board.

Remaining release checks require the physical parts:

- Print the upper footprint at 1:1 and overlay the actual SDIP socket and CPU.
- Confirm socket tail pitch and tail-row centres are 1.778 mm and 19.05 mm.
- Dry-fit the adapter over the SBC, including nearby capacitors.
- Order a small first article; continuity-test all 64 intended pin pairs and
  confirm no adjacent-pin shorts before applying power.
- Review Gerbers and drill data in the fabricator's viewer using its own rules.

## Geometry and mechanical fit

| Interface | Lead pitch | Row spacing | Pad / drill |
|---|---:|---:|---:|
| U1, SDIP socket / TMP68HC000N | 1.778 mm | 19.05 mm | 1.40 / 0.80 mm |
| J1, male pins to SBC U3 | 2.540 mm | 22.86 mm | 1.60 / 0.90 mm |

The TMP68HC000N SDIP-64 must **not** be plugged directly into U3: the pitch,
row spacing, and 32-pin row length do not match. Use the adapter and an SDIP
socket only.

Mount through two 1×32, 2.54 mm-pitch, 8 mm-tall female header strips at the
SBC's 22.86 mm row spacing, with matching male strips on the adapter underside.
Confirm actual mated height by dry assembly.

## Timing

At 16 MHz the clock period is 62.5 ns. The largest original pin-position
offset is about 11.8 mm, or roughly 70–90 ps in FR-4. Trace-length matching
is not required; clean routing and continuity verification matter more.

## Supporting files

- `SDIP64-P-750-1.78.kicad_mod`: reusable SDIP64 footprint.
- `final-preproduction-drc.rpt`: matching final DRC report.
- `SDIP64-to-DIP64-two-layer-drill.rpt`: generated drill summary.
- `generate_adapter.py`: unrouted geometry baseline only; do not run it on the
  production design because it removes routed copper.
