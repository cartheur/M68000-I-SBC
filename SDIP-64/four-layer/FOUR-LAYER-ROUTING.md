# Compact four-layer routing plan

## Why four layers

The production SBC has no usable lateral clearance around its DIP-64 CPU
socket. The adapter must therefore remain inside the original DIP-64 envelope,
with the SDIP-64 footprint centered over it. A two-layer, direct pitch-change
route crosses adjacent plated-through pads and is not manufacture-safe.

Use a four-layer board with the following stackup:

| Layer | Use |
|---|---|
| F.Cu | Short escape tracks from the SDIP pads; assembly side |
| In1.Cu | Pins 1–32, odd-numbered channels |
| In2.Cu | Pins 1–32, even-numbered channels; repeat the same split for pins 33–64 |
| B.Cu | Short escape tracks to the DIP male-pin pads; host side |

No plane is assigned because all four layers are required for the 64 direct
point-to-point connections. This is acceptable only because this is a short
adapter for a low-speed 16.67 MHz processor; retain the SBC's existing local
decoupling and keep all tracks as short as possible.

## Proposed fabrication rules

These are capabilities to request explicitly from the PCB fabricator:

| Feature | Minimum design value |
|---|---:|
| Finished board thickness | 1.6 mm |
| Outer-layer trace / space | 0.20 / 0.20 mm |
| Inner-layer trace / space | 0.15 / 0.15 mm |
| Through-hole CPU pad drill | 0.80 mm |
| Through-hole DIP pin drill | 0.90 mm |
| Routing via drill / pad | 0.25 / 0.50 mm |
| Annular ring | 0.15 mm minimum |
| Copper | 1 oz outer and inner layers |

Do not order until the chosen fabricator confirms these values and KiCad DRC
has been run against that fabricator's rules.

## Routing topology

For each SDIP row:

1. Escape every upper PTH pad toward the space between the two rows on F.Cu.
2. Place a via immediately after each escape. Alternate pins between In1.Cu
   and In2.Cu, so each inner layer carries only 16 channels per side.
3. Fan the channels monotonically to corresponding escape vias beside the
   lower DIP row. Keep each pin number in order; pin *n* remains pin *n*.
4. Route the final short segment on B.Cu from each lower via into its DIP pad.

The alternating inner-layer assignment is what allows the required lanes to
fit between 19.05 mm SDIP rows without a sidecar or trace crossings.

## Acceptance criteria

- All 64 nets connect exactly `U1.n` to `J1.n`; no other pads share a net.
- KiCad DRC: zero errors and zero unconnected items.
- Gerber/drill review: no annular-ring, solder-mask, or clearance violations.
- 1:1 print of the upper footprint fits the actual CPU without force.
- First article continuity test: 64 intended connections; zero adjacent-pin
  shorts before the CPU is powered.
- Plug-in test confirms the adapter clears nearby components on the SBC.

## Status

This is the approved routing strategy, not a fabrication release. The
existing `.kicad_pcb` remains intentionally unrouted until the four-layer
tracks have passed the acceptance criteria above.

The current KiCad DRC output is retained as
[`adapter-drc.rpt`](adapter-drc.rpt). It is expected to show 64 unconnected
nets until routing is complete; it is published so review can distinguish
known template findings from new routing errors.

The rejected compact two-layer auto-route is documented in
[`../two-layer/adapter-drc.rpt`](../two-layer/adapter-drc.rpt). It has 591 DRC
violations, including shorts, and is evidence for rejecting that route rather
than a candidate fabrication result.

The corresponding automated compact four-layer attempt is retained as
[`four-layer-attempt-drc.rpt`](four-layer-attempt-drc.rpt). It has 620 DRC
violations. Its failure identifies the limiting geometry: a lower DIP-pad
escape crosses the keepout of the centred SDIP through-hole row before it can
reach an inner-layer via. An interactive route must alter the escape topology
(for example, external fan-out, blind/buried vias, or a selected commercial
adapter); merely adding In1/In2 copper does not make a straight compact
fan-out valid.
