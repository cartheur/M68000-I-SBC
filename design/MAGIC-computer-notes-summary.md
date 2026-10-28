# MAGIC computer notes — summary

This is a research summary of
[`CCF10272011_00005.pdf`](CCF10272011_00005.pdf), a 79-page scanned dossier
about **MAGIC** (*Mattel Advanced Graphic Interface Circuit*). It is not a
transcription, a definitive specification, or evidence that the described
computer was manufactured. The source itself is marked *Draft / Confidential*
and includes working proposals, handwritten design notes, estimates, and test
ideas from late 1981 and 1982.

## What the dossier describes

MAGIC is proposed as one of two custom ICs for a second-generation Mattel TV
game system. The typed working specification assumes a Motorola 68000 CPU,
while explicitly saying that the CPU selection had not yet been made. MAGIC is
intended to combine:

- composite-video generation and video timing;
- dynamic-RAM arbitration, control, and refresh;
- CPU clocking, address decoding, and interrupts;
- background, character/alpha, border, and moving-object graphics; and
- miscellaneous small- and medium-scale logic to reduce chip count.

## Architecture proposed in the typed specification

The opening pages describe shared 16-bit dynamic RAM. MAGIC would access the
RAM directly, interleave its accesses with those of the CPU, pipeline graphics
data, generate RAS/CAS, multiplex RAM addresses, and manage refresh. The
minimum graphics-access requirement is stated as 16K 16-bit words; larger RAM
arrangements were being considered.

Timing is derived from a 14.32 MHz crystal for 525-line systems and 17.72 MHz
for 625-line systems. The proposal targets NTSC, PAL, and SECAM operation,
including full interlace, composite-sync generation, and provision for locking
to an external video source. A software-selectable non-interlaced mode is also
described.

The CPU interface is presented as a 68000-style 16-bit data bus with standard
control signals. Two interrupt causes share one interrupt line:

- a roughly 60 Hz timing interrupt, intended to keep game timing similar on
  525- and 625-line systems; and
- a programmable scan-line interrupt, chiefly intended to permit moving-object
  reuse during a frame.

## Display model and video features

The typed proposal calls for a 40-by-24 alpha/graphics-card display. It
describes square-ish pixels as a deliberate choice: they simplify positioning,
rotation, line/circle drawing, and anti-aliasing, while allowing an 8-bit
horizontal coordinate to cover the active area plus the hidden-left-border
positioning range.

Video circuitry would use palette registers with luminance and two color-
difference components. The proposal describes a primary and secondary output,
allowing graphics and alpha information to be split between two displays. The
suggested uses include two-player private/common information and separate
game/application displays; this mode is not available in the stated SECAM
configuration. Provision for external-video mixing is also described.

The border is treated as four independently colored corner regions with
programmable division points. The source also identifies bitmap, normal-card,
and high-resolution-card background modes, alongside alpha/character and
moving-object generators.

## Handwritten register and graphics notes

The middle of the dossier is primarily handwritten engineering material:

- block diagrams and an address-map sketch;
- a large register map, including raster-bank selection, moving-object
  parameters, palette/color information, display control, and counters;
- timing diagrams and notes for scrolling, splitting, borders, and raster
  operations;
- background-generator notes for card and bitmap-style data; and
- character-generator and moving-object notes, including scaling, zooming,
  mirroring, priority, interaction, and object reuse.

These pages are valuable design evidence, but their handwriting, diagrams, and
occasional scan degradation make exact field names, bit positions, and register
semantics unsuitable for citation from this summary. Consult the page images
before deriving an implementation.

## High-resolution cards concept

The closing technical note explains the motivation for a high-resolution cards
mode: composite television has substantially less chrominance detail than
luminance detail. Rather than allocate equal detail to both, the proposal groups
pixels for color while retaining more per-pixel luminance information.

For MAGIC, normal cards are described as 40 columns by 24 rows, with cards of
6 by 8 pixels. In the proposed high-resolution mode, each six-pixel line is
divided into two three-pixel color groups. The 16-bit word allocates color for
the groups and uses the remaining per-pixel information for luminance
adjustment. The author reports that a software/hardware simulation had given
excellent results. This is a design claim, not a preserved implementation or
performance measurement.

## Evaluation and implementation planning

The March 1982 evaluation list calls for demonstrations of high-resolution
backgrounds, user-controlled and animated objects, anti-aliasing, external
video, 16 objects on one scan line, object reuse and color changes, rotation,
RAM-bandwidth stress, 3D/shading, zoom, split alpha/graphics, and separate TV
outputs. It also calls for debug software covering normal cards, the color
spectrum, interaction, and scrolling.

A 15 June 1982 die-size estimate describes an early implementation study based
on incomplete emulator schematics and engineering meetings. It estimates about
87,600 square mils of die area and roughly 54,000 transistors, but emphasizes
that the logic design was incomplete and the estimate would be refined. The
function breakdown includes video, addressing/interrupts, 68000 and DRAM
control, timing, background and alpha generators, 16 moving objects, and I/O
buffers. These are estimates for a proposal, not measured properties of a
fabricated chip.

## Source map

| PDF pages | Material |
| --- | --- |
| 1–8 | Typed MAGIC working specification: purpose, memory/CPU interface, timing, video, and graphics introduction |
| 9–68 | Block diagrams, address/register material, and handwritten graphics-generator notes |
| 69–72 | March 1982 hardware-capability and software-evaluation notes |
| 73–76 | June 1982 MAGIC die-size and transistor-count estimate |
| 77–78 | High Resolution Cards Mode explanatory note, dated 30 October 1981 |
| 79 | Low-information scan tail; no technical conclusion drawn |

## Preservation and use

Keep the PDF unchanged. Its SHA-256 is:

```text
b26b930bbf612af70824ff2b0483b3cbde2ffe48e1ea31ae2d10354e040a3f06
```

Verify it from the repository root:

```sh
sha256sum design-stubs/MAGIC/CCF10272011_00005.pdf
```

For research citations, identify the PDF page and distinguish verbatim source
content, a legible diagram reading, and any reconstruction inference. Do not
use the draft as proof of final pinouts, register encodings, clock values, chip
process, software behavior, or released hardware.
