## SPDIP-64

“Shrink DIP64” usually refers to a 64-lead shrink plastic dual-in-line package (SPDIP). Its defining feature is 0.070 in (1.778 mm) lead pitch, rather than the standard DIP’s 0.100 in (2.54 mm). It has 32 leads per row. 
Wikipedia

There isn’t one universal body size or complete dimensional drawing for every shrink DIP64: dimensions such as body width and length, lead-row spacing, height, and lead shape depend on the manufacturer and specific part. For a PCB footprint, use the exact component’s package drawing; don’t assume standard DIP64 dimensions. 

### Specifications

| Specification | TMP68HC000N-16 |
|---|---|
| Processor | 16-bit microprocessor |
| Maximum clock frequency | 16.67 MHz |
| Address bus | 23-bit |
| External data bus | 16-bit |
| Package | 64-pin plastic SDIP, through-hole |
| Package width | 19.05 mm |
| Package length | 57.5 mm |
| Terminal pitch | 1.778 mm |
| Maximum seated height | 5 mm |
| Supply voltage | 4.75–5.25 V; nominal 5 V |
| Maximum supply current | 50 mA |
| Status | Discontinued / obsolete |

Package dimensions and electrical figures are listed for the TMP68HC000N-16; check the Toshiba [datasheet](/datasheets/TMP68HC000X.pdf) before designing a footprint or setting operating limits. The reusable SDIP footprint and the DIP-64 adapter board are documented in [four-layer/ADAPTER-DESIGN.md](four-layer/ADAPTER-DESIGN.md).

### Comparatives

The standard-package counterpart is **TMP68HC000P-16**. It shares the same 68HC000 processor and 16.67 MHz rating as the **TMP68HC000N-16**; the main difference is the package. <citation src="3,4"></citation>

| Feature | TMP68HC000N-16 | TMP68HC000P-16 |
|---|---|---|
| Package type | Shrink DIP (SDIP-64) | Standard plastic DIP (PDIP-64) |
| Pin count | 64 | 64 |
| Processor | Toshiba 68HC000 | Toshiba 68HC000 |
| Maximum clock | 16.67 MHz | 16.67 MHz |
| Data width | 16-bit | 16-bit |
| Address bus | 23-bit | 23-bit |
| Lead pitch | 1.778 mm (0.070 in) for shrink DIP | 2.54 mm (0.100 in) for standard DIP |
| PCB/socket compatibility | Requires SDIP-64 footprint or socket | Requires standard DIP-64 footprint or socket |

The **P and N packages are not drop-in replacements for each other**: their lead pitch differs, so they need different footprints or sockets. Check the Toshiba package [drawings](/datasheets/TMP68HC000X.pdf) before laying out a board; reseller listings can use “DIP64” loosely for either package.

### Advice

I need footprint for 68000 (Shrink DIP). Any idea where to find?

this is trivial to make. open footprint editor. set grid to 0.050". set pads in right places - they auto increment.
go to properties make that part THT (through hole). oh and if pads are not though hole, edit one to make it correct., then set is as default and apply default to all other pads. done.

I couldn’t find a ready-made KiCad project specifically for an **SDIP-64-to-DIP-64 socket adapter**. The closest useful resource is a KiCad forum thread discussing **1.778 mm-pitch high-density DIP footprints**; it explains using KiCad’s Footprint Wizard to make the footprint from the socket’s dimensions. [Read the discussion](https://forum.kicad.info/t/high-density-dip-footprints/21154).

For your adapter, make a small PCB with:

- A **64-pin SDIP socket footprint** matching the TMP68HC000N-16 socket’s datasheet drawing.
- A **64-pin standard DIP footprint** with 2.54 mm pitch for the target socket or breadboard.
- One-to-one connections between corresponding pins, preserving pin 1 orientation.

KiCad’s built-in DIP library may help with the standard-DIP side, but the shrink-DIP socket footprint will likely need to be custom. Verify the actual socket dimensions and pin numbering before ordering the board; the component’s package drawing and the socket drawing are what determine the footprint.

## Adapter implementation

The project now includes a generated, direct 1:1 `SDIP64-P-750-1.78` to
`DIP-64_W22.86mm` adapter board. It is designed for the production board's
22.86 mm row-spacing DIP-64 socket. Start with [four-layer/ADAPTER-DESIGN.md](four-layer/ADAPTER-DESIGN.md)
for the dimensions, assembly method, and mandatory 1:1 print/DRC checks.
The constrained production-board envelope requires a compact four-layer
routing strategy, documented in [four-layer/FOUR-LAYER-ROUTING.md](four-layer/FOUR-LAYER-ROUTING.md).

## Adapter design status

The adapter work is organized by routing approach:

| Directory | Status | Contents |
|---|---|---|
| [`two-layer/`](two-layer/) | Rejected | DRC evidence for the compact two-layer fan-out attempt. It has 591 violations, including shorts, and must not be fabricated. |
| [`four-layer/`](four-layer/) | Active routing template | Mechanically accurate SDIP64 footprint, compact adapter PCB, generator, four-layer routing plan, and published DRC reports. |

The four-layer PCB is intentionally marked **ROUTING REQUIRED — DO NOT
FABRICATE**. Its current DRC report records the expected 64 unconnected nets.
The associated two-layer and four-layer auto-route reports are retained for
review; both attempts were rejected because their copper created shorts around
the overlapping plated-through footprints. A production release requires an
interactive route with zero DRC errors and zero unconnected nets, followed by
a 1:1 mechanical overlay and continuity testing.
