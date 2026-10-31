# SDIP64-to-DIP64 adapter

This design adapts the through-hole Toshiba `TMP68HC000N` shrink-DIP package
to the 64-pin, 900-mil DIP socket already present on the production SBC.
It is a direct electrical translation: CPU pin *n* connects only to host pin
*n*.

## Design basis

The upper footprint implements Toshiba `SDIP64-P-750-1.78` geometry:

| Item | Value |
|---|---:|
| Pins | 64 (32 per side) |
| Upper lead pitch | 1.778 mm (0.070 in) |
| Upper lead-row spacing | 19.05 mm (0.750 in) |
| Package body length | 57.5 ±0.2 mm |
| Package body width | 17.8 ±0.2 mm |
| Maximum body height | 4.7 ±0.3 mm |
| Upper pad / hole | 1.40 / 0.80 mm |

### Procured CPU socket

The intended CPU-side part is a 64-pin, through-hole SDIP socket ordered from
an eBay listing.  Its seller-supplied specifications are recorded here as a
useful procurement reference; they are **not** a substitute for measuring the
actual part before releasing the PCB.

| Seller specification | Stated value | Design use |
|---|---:|---|
| Pins / ports | 64 | Matches the CPU pin count |
| Nominal pitch | 1.778 mm | Matches the SDIP footprint pitch |
| Item length | 56.90 mm | Consistent with the approximately 57.5 mm CPU package length |
| Item width | 21.54 mm | Socket outside width; do not use as the lead-row spacing |
| Item height | 8.1 mm | Clearance requirement above the SBC |
| Mounting / termination | Through-hole / solder | Suitable for the adapter's upper side |

Before fabrication, measure the socket tail pitch over multiple positions,
tail-row centre spacing, tail width/thickness and tail length, outside-body
dimensions, and the pin-1/notch orientation.  In particular, confirm the
tail rows are 19.05 mm apart; the listing does not state this dimension. Use
the measurements to adjust the upper drill/pad dimensions and complete a 1:1
printed overlay check.

The lower footprint matches `Package_DIP:DIP-64_W22.86mm_Socket` on the
production board:

| Item | Value |
|---|---:|
| Lower lead pitch | 2.54 mm (0.100 in) |
| Lower lead-row spacing | 22.86 mm (0.900 in) |
| Lower pad / hole | 1.60 / 0.90 mm |

### Host-socket and header-pin interface

The production U3 pattern is two 32-pin rows at 2.54 mm (0.100 in) pitch and
22.86 mm (0.900 in) row centres. There are two validated socket options:

1. **One-piece DIP socket:** Preci-Dip `110-PP-964-41-001101` is listed as
   64 poles, `A = 81.2 mm`, `B = 22.86 mm`, and `C = 25.3 mm`. It is a direct
   mechanical match for U3.
2. **Two separate row sockets (preferred for this adapter):** Mill-Max
   `311-93-164-41-001000` is a 64-position, single-row, 2.54 mm-pitch socket
   strip. Cut it into two 32-position sections and install one section in
   each U3 row. Because each section is single-row, the board establishes the
   required 22.86 mm separation. Its long solder tails are suitable for the
   SBC's through holes.

The Mill-Max contact accepts **0.38–0.635 mm** round leads; Preci-Dip accepts
**0.40–0.56 mm**. Use male header or turned pins in their common range—e.g.
0.50 mm round—on the adapter. That is the contact-size limit, irrespective
of the larger 0.90 mm adapter PCB drill.

The supplied Adam Tech `ICS-6XX-T` drawing instead specifies **0.600 in
(15.24 mm) row spacing**. It cannot mate with U3, even if two 32-position
parts are used: splitting the length does not change the 15.24 mm row spacing.

The SDIP pin-1 / pin-64 end is aligned with the DIP pin-1 / pin-64 end. The
unused 23.622 mm of DIP length is therefore at the pin-32 / pin-33 end. Each
signal escapes into the interior with two 0.80/0.40 mm vias before the pitch
transition, avoiding the neighbouring through-holes that a direct diagonal
trace would cross.

## Direct-fit validation — CPU must not be fitted to U3

The Toshiba `TMP68HC000N` SDIP-64 **cannot** directly plug into the production
SBC's U3 holes. This is a mechanical non-fit, independent of the electrical
pinout:

| Geometry | TMP68HC000N SDIP-64 | Production U3 |
|---|---:|---:|
| Pin pitch along either row | 1.778 mm (0.070 in) | 2.54 mm (0.100 in) |
| Pin-row centre separation | 19.05 mm (0.750 in) | 22.86 mm (0.900 in) |
| Span from first to last pin in a 32-pin row | 55.118 mm | 78.740 mm |

If pin 1 is placed over its corresponding U3 hole, the next pin is already
0.762 mm off centre; the error grows by another 0.762 mm at every position,
reaching 23.622 mm at pin 32. The opposite lead row is also 3.81 mm too close
together. The CPU therefore must only be used through the SDIP-to-DIP adapter
and its SDIP socket. Never force it into U3 or into the board-side Mill-Max /
Preci-Dip socket arrangement.

## Files

- `SDIP64-P-750-1.78.kicad_mod` is the reusable, upper-side CPU footprint.
- `SDIP64-to-DIP64-adapter.kicad_pcb` is the compact four-layer adapter board.
- `generate_adapter.py` regenerates both files from the dimensional constants.

## Assembly

1. Fit 64 turned male pins from the **B.Cu / HOST SIDE**: two 32-pin sections
   on 2.54 mm pitch and 22.86 mm row centres. For either the Preci-Dip or
   Mill-Max socket option, use a 0.40–0.56 mm mating diameter (for example,
   0.50 mm round); the adapter's 0.90 mm finished holes are not the
   contact-size limit.
2. Fit the measured SDIP-64 socket on the **F.Cu / CPU SIDE**, aligned with
   the pin-1 legend. Insert the CPU into that socket; do not bend or solder
   the CPU leads directly to the adapter.
3. Inspect for bridges, then verify continuity from every upper socket pin *n* to
   lower pin *n*. Confirm no continuity exists between adjacent pins.
4. Only then insert the completed adapter into the host DIP-64 socket, with
   both pin-1 markers at the same end.

## Required pre-fabrication checks

- Print the F.Cu layer at 1:1 and overlay the actual CPU before ordering.
- Open the board in KiCad 10 or newer and run DRC; this environment does not
  include KiCad's command-line validator.
- Confirm the selected pin-strip or turned-pin part fits the production-board
  socket. The existing board footprint is 22.86 mm row spacing.
- Review generated Gerbers and drill data with the fabricator's viewer.
- Order a small first article and continuity-test it before applying power.

## Scope and limitations

This board is a mechanical/electrical adapter, not a voltage or logic-level
converter. It has no intentional net swaps, components, or decoupling. Keep
the adapter as short as practical and use the existing SBC's decoupling. The
footprint dimensions are based on Toshiba's `SDIP64-P-750-1.78` package
drawing; verify the actual CPU with the 1:1 overlay because obsolete parts
can have lead deformation.

## Routing status

`SDIP64-to-DIP64-adapter.kicad_pcb` is a **mechanically accurate, unrouted
template**, not a fabrication release. Its 64 named nets deliberately expose
the required 1:1 connections. A naïve two-layer diagonal fan-out shorts
against adjacent through-hole pads, so it must not be used. Route it
interactively in KiCad after choosing fabrication rules. The production SBC's
nearby components rule out a wide two-layer sidecar, so the selected approach
is a compact four-layer adapter. See [FOUR-LAYER-ROUTING.md](FOUR-LAYER-ROUTING.md)
for its stackup, design rules, routing topology, and release criteria. The
board itself is marked `ROUTING REQUIRED — DO NOT FABRICATE`.
