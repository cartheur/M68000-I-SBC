#!/usr/bin/env python3
"""Generate the SDIP64-to-DIP64 KiCad footprint and adapter PCB.

Geometry is derived from Toshiba package SDIP64-P-750-1.78 and the production
board's Package_DIP:DIP-64_W22.86mm_Socket footprint.  The generated board
is intentionally net-labelled P01..P64: each net joins identically numbered
top and bottom pins, making the adapter electrically 1:1.
"""

from pathlib import Path


HERE = Path(__file__).resolve().parent
PITCH_TOP = 1.778
PITCH_BOTTOM = 2.54
TOP_ROW = 19.05
BOTTOM_ROW = 22.86
TOP_START = 0.000  # align pin 1; the unused length is at the pin-32/33 end
BOTTOM_SPAN = 31 * PITCH_BOTTOM


def pin_position(pin: int, top: bool) -> tuple[float, float]:
    """Return position relative to the lower-left DIP pin 1."""
    pitch = PITCH_TOP if top else PITCH_BOTTOM
    row = TOP_ROW if top else BOTTOM_ROW
    if pin <= 32:
        return ((BOTTOM_ROW - TOP_ROW) / 2 if top else 0, TOP_START + (pin - 1) * pitch if top else (pin - 1) * pitch)
    return ((BOTTOM_ROW - TOP_ROW) / 2 + row if top else row, TOP_START + (64 - pin) * pitch if top else (64 - pin) * pitch)


def pad(number: int, x: float, y: float, size: float, drill: float, net: int | None = None) -> str:
    shape = "rect" if number == 1 else "circle"
    network = "" if net is None else f'\n\t\t(net {net} "P{number:02d}")'
    return f'''\t(pad "{number}" thru_hole {shape}
\t\t(at {x:.3f} {y:.3f})
\t\t(size {size:.3f} {size:.3f})
\t\t(drill {drill:.3f})
\t\t(layers "*.Cu" "*.Mask"){network}
\t)'''


def make_footprint() -> str:
    out = ['''(footprint "SDIP64-P-750-1.78"
\t(version 20260206)
\t(generator "pcbnew")
\t(generator_version "10.0")
\t(layer "F.Cu")
\t(descr "Toshiba SDIP64-P-750-1.78, 64-pin shrink DIP, 1.778 mm pitch, 19.05 mm row spacing")
\t(tags "THT SDIP SPDIP 64 1.778mm 750mil")
\t(property "Reference" "U" (at 9.525 -3.0) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))
\t(property "Value" "SDIP64-P-750-1.78" (at 9.525 58.2) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))
\t(fp_rect (start 0.625 -1.25) (end 18.425 56.368) (stroke (width 0.12) (type default)) (fill none) (layer "F.SilkS"))
\t(fp_arc (start 7.525 -1.25) (mid 9.525 0.75) (end 11.525 -1.25) (stroke (width 0.12) (type default)) (fill none) (layer "F.SilkS"))
\t(fp_rect (start 0.625 -1.25) (end 18.425 56.368) (stroke (width 0.1) (type default)) (fill none) (layer "F.Fab"))''']
    for n in range(1, 65):
        x, y = pin_position(n, True)
        out.append(pad(n, x, y - TOP_START, 1.40, 0.80))
    out.append(")\n")
    return "\n".join(out)


def footprint_in_board(name: str, reference: str, value: str, top: bool) -> str:
    layer = "F.Cu" if top else "B.Cu"
    side = "F.SilkS" if top else "B.SilkS"
    description = "CPU, SDIP64-P-750-1.78" if top else "Host board, DIP-64 W22.86mm"
    out = [f'''\t(footprint "Custom:{name}"
\t\t(layer "{layer}")
\t\t(at 100 100)
\t\t(descr "{description}")
\t\t(property "Reference" "{reference}" (at 11.43 -2.7) (layer "{side}") (effects (font (size 1.2 1.2) (thickness 0.18))))
\t\t(property "Value" "{value}" (at 11.43 81.5) (layer "{side}") (effects (font (size 1 1) (thickness 0.15))))
\t\t(fp_rect (start -0.9 -1.3) (end 23.76 80.04) (stroke (width 0.25) (type default)) (fill none) (layer "{side}"))
\t\t(fp_text user "PIN 1" (at 1.8 2.2) (layer "{side}") (effects (font (size 0.9 0.9) (thickness 0.14))))''']
    for n in range(1, 65):
        x, y = pin_position(n, top)
        out.append(pad(n, x, y, 1.40 if top else 1.60, 0.80 if top else 0.90, n))
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
\t\t(2 "In1.Cu" signal)
\t\t(4 "In2.Cu" signal)
\t\t(31 "B.Cu" signal)
\t\t(36 "B.SilkS" user "b.Silkscreen")
\t\t(37 "F.SilkS" user "f.Silkscreen")
\t\t(44 "Edge.Cuts" user)
\t)
\t(setup (pad_to_mask_clearance 0))''']
    for n in range(1, 65):
        out.append(f'\t(net {n} "P{n:02d}")')
    out += [footprint_in_board("SDIP64-P-750-1.78", "U1", "TMP68HC000N", True), footprint_in_board("DIP-64_W22.86mm", "J1", "TO HOST DIP-64", False)]
    # Keep this as a safe, mechanically accurate routing template. The
    # published two- and four-layer auto-route attempts both failed DRC; no
    # known-bad copper is retained in the draft board.
    out += ['''\t(gr_rect (start 98.5 98.5) (end 124.36 180.24) (stroke (width 0.25) (type default)) (fill none) (layer "Edge.Cuts"))
\t(gr_text "SDIP64 (1.778 mm) to DIP64 (2.54 mm)\\n1:1 ADAPTER — PIN 1 THIS END" (at 111.43 96.3) (layer "F.SilkS") (effects (font (size 1.1 1.1) (thickness 0.18)) (justify)))
\t(gr_text "CPU SIDE" (at 111.43 104) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))
\t(gr_text "4-LAYER ROUTING REQUIRED — DO NOT FABRICATE" (at 111.43 108) (layer "F.SilkS") (effects (font (size 0.9 0.9) (thickness 0.15))))
\t(gr_text "HOST SIDE: FIT MALE PINS" (at 111.43 176) (layer "B.SilkS") (effects (font (size 1 1) (thickness 0.15)) (justify mirror)))
)\n''']
    return "\n".join(out)


(HERE / "SDIP64-P-750-1.78.kicad_mod").write_text(make_footprint())
(HERE / "SDIP64-to-DIP64-adapter.kicad_pcb").write_text(make_board())
