#!/usr/bin/env python3
"""Generate an inspectable, unrouted two-layer SDIP64-to-DIP64 board."""

from pathlib import Path


HERE = Path(__file__).resolve().parent
PITCH_SDIP = 1.778
PITCH_DIP = 2.54
SDIP_ROW = 19.05
DIP_ROW = 22.86


def position(pin: int, sdip: bool) -> tuple[float, float]:
    pitch = PITCH_SDIP if sdip else PITCH_DIP
    row = SDIP_ROW if sdip else DIP_ROW
    x0 = (DIP_ROW - SDIP_ROW) / 2 if sdip else 0.0
    return (x0, (pin - 1) * pitch) if pin <= 32 else (x0 + row, (64 - pin) * pitch)


def make_pad(pin: int, x: float, y: float, size: float, drill: float) -> str:
    shape = "rect" if pin == 1 else "circle"
    return f'''\t(pad "{pin}" thru_hole {shape}
\t\t(at {x:.3f} {y:.3f})
\t\t(size {size:.3f} {size:.3f})
\t\t(drill {drill:.3f})
\t\t(layers "*.Cu" "*.Mask")
\t\t(net {pin} "P{pin:02d}")
\t)'''


def make_footprint(name: str, reference: str, value: str, sdip: bool) -> str:
    layer = "F.Cu" if sdip else "B.Cu"
    silk = "F.SilkS" if sdip else "B.SilkS"
    mirror = "" if sdip else " (justify mirror)"
    out = [f'''\t(footprint "{name}"
\t\t(layer "{layer}")
\t\t(at 100 100)
\t\t(property "Reference" "{reference}" (at 11.43 -2.7) (layer "{silk}") (effects (font (size 1.2 1.2) (thickness 0.18)){mirror}))
\t\t(property "Value" "{value}" (at 11.43 81.5) (layer "{silk}") (effects (font (size 1 1) (thickness 0.15)){mirror}))''']
    for pin in range(1, 65):
        x, y = position(pin, sdip)
        out.append(make_pad(pin, x, y, 1.40 if sdip else 1.60, 0.80 if sdip else 0.90))
    out.append("\t)\n")
    return "\n".join(out)


def make_board() -> str:
    out = ['''(kicad_pcb
\t(version 20260206)
\t(generator "pcbnew")
\t(generator_version "10.0")
\t(general (thickness 1.6))
\t(paper "A4")
\t(layers
\t\t(0 "F.Cu" signal)
\t\t(31 "B.Cu" signal)
\t\t(36 "B.SilkS" user "b.Silkscreen")
\t\t(37 "F.SilkS" user "f.Silkscreen")
\t\t(44 "Edge.Cuts" user)
\t)
\t(setup (pad_to_mask_clearance 0))''']
    out.extend(f'\t(net {pin} "P{pin:02d}")' for pin in range(1, 65))
    out.extend((
        make_footprint("SDIP64-P-750-1.78", "U1", "TMP68HC000N / SDIP SOCKET", True),
        make_footprint("DIP-64_W22.86mm", "J1", "TO SBC U3", False),
        '''\t(gr_rect (start 98.5 98.5) (end 124.36 180.24) (stroke (width 0.25) (type default)) (fill none) (layer "Edge.Cuts"))
\t(gr_text "SDIP64 (1.778 mm) to DIP64 (2.54 mm)\\nTWO-LAYER ROUTING BASELINE — UNROUTED — DO NOT FABRICATE" (at 111.43 96.3) (layer "F.SilkS") (effects (font (size 1.0 1.0) (thickness 0.17)) (justify)))
)\n''',
    ))
    return "\n".join(out)


(HERE / "SDIP64-to-DIP64-two-layer.kicad_pcb").write_text(make_board())
