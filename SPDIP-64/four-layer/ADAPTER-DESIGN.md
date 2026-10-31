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

The lower footprint matches `Package_DIP:DIP-64_W22.86mm_Socket` on the
production board:

| Item | Value |
|---|---:|
| Lower lead pitch | 2.54 mm (0.100 in) |
| Lower lead-row spacing | 22.86 mm (0.900 in) |
| Lower pad / hole | 1.60 / 0.90 mm |

The SDIP pin-1 / pin-64 end is aligned with the DIP pin-1 / pin-64 end. The
unused 23.622 mm of DIP length is therefore at the pin-32 / pin-33 end. Each
signal escapes into the interior with two 0.80/0.40 mm vias before the pitch
transition, avoiding the neighbouring through-holes that a direct diagonal
trace would cross.

## Files

- `SDIP64-P-750-1.78.kicad_mod` is the reusable, upper-side CPU footprint.
- `SDIP64-to-DIP64-adapter.kicad_pcb` is the compact four-layer adapter board.
- `generate_adapter.py` regenerates both files from the dimensional constants.

## Assembly

1. Fit 64 turned male pins from the **B.Cu / HOST SIDE**. Their tails must
   suit the socket fitted to the production SBC; 0.46–0.64 mm square or round
   pins are appropriate for the 0.90 mm finished holes.
2. Insert the CPU on the **F.Cu / CPU SIDE**, aligned with the pin-1 legend.
   Solder it directly. Do not bend its leads to fit the host socket.
3. Inspect for bridges, then verify continuity from every upper pin *n* to
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
