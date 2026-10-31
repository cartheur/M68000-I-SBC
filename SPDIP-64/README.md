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

Package dimensions and electrical figures are listed for the TMP68HC000N-16; check the Toshiba [datasheet](/datasheets/TMP68HC000X.pdf) before designing a footprint or setting operating limits.

### Advice

I need footprint for 68000 (Shrink DIP). Any idea where to find?

this is trivial to make. open footprint editor. set grid to 0.050". set pads in right places - they auto increment.
go to properties make that part THT (through hole). oh and if pads are not though hole, edit one to make it correct., then set is as default and apply default to all other pads. done.
