# Two-layer routing baseline

`SDIP64-to-DIP64-two-layer.kicad_pcb` is an inspectable two-copper-layer
KiCad board for the direct 1:1 TMP68HC000N SDIP-64 to the SBC's U3 DIP-64
adapter. It contains the verified geometry but **no copper tracks**, so it is
not a fabrication candidate.

The generator is the authoritative source for the board. Regenerate it with:

```sh
python3 generate_adapter.py
```

The board has only `F.Cu` and `B.Cu`, 64 separate nets (`P01` through `P64`),
and a complete netlist joining upper pin *n* only to lower pin *n*. It is the
reproducible starting point for a two-layer routing trial: make a copy, route
it, and retain that PCB alongside its KiCad DRC report.

The SDIP rows are centred along the 32-position host rows. The board is 34.86
mm wide by 90.74 mm long, providing a 6 mm perimeter routing margin around
the host-pad envelope. Every host pin is identified on `F.SilkS`, outside its
respective row: pins 1–32 on the left and pins 64–33 on the right.

## SBC mounting and clearance

Mount the adapter through two 1×32, 2.54 mm-pitch tall female header strips
at the SBC U3 row spacing of 22.86 mm. Fit matching 2.54 mm male header strips
to the adapter underside. The selected female headers are 8 mm tall, placing
the adapter underside at least approximately 8 mm above the SBC (and normally
slightly higher when the male-header carrier is included). This permits the
adapter to overfly the nearby C2, C3, and C4 capacitors despite the enlarged
34.86 × 90.74 mm outline.

Confirm the actual mating height, solder-joint clearance, and the height of
the fitted capacitors with a dry assembly before ordering the adapter.

## Timing and routing length

Centreing the SDIP rows makes the middle pins almost longitudinally aligned
with their respective host pads: the residual offset is approximately 0.381
mm. The largest longitudinal offset occurs at the row ends and is 11.811 mm.
An approximately 12 mm FR-4 trace adds only about 70–90 ps of propagation
delay, compared with the 62.5 ns clock period of the selected 16 MHz
oscillator. No trace-length matching is required for this adapter.

Route the clock and asynchronous control signals directly where practical,
avoid unnecessary loops and lengthy parallel runs, and retain effective local
decoupling and signal-return paths. These signal- and power-integrity concerns
matter more than the small pin-to-pin delay differences on this board.

## Geometry under test

| Interface | Lead pitch | Row spacing |
|---|---:|---:|
| U1, SDIP socket / TMP68HC000N | 1.778 mm | 19.05 mm |
| J1, male pins to SBC U3 | 2.540 mm | 22.86 mm |

The earlier DRC report was removed because its matching source PCB was not
retained, so it could not be used as evidence for or against a two-layer
route. `two-layer-baseline-drc.rpt` was generated from this board with Flatpak
KiCad 10.0.8: it records zero physical DRC violations and the expected 64
unconnected nets. Run a fresh DRC after creating a routing candidate.
