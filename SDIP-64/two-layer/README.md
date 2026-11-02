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
