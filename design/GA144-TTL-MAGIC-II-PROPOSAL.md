# MAGIC-II: GA144-assisted TTL video computer

**Status:** pre-architecture proposal
**Scope:** a new, historically informed machine; not a reconstruction of a
released Mattel product or an undocumented MAGIC ASIC.

MAGIC-II adapts the ideas in the [MAGIC notes summary](MAGIC-computer-notes-summary.md)
to a build using a GreenArrays GA144A12 multicomputer array for parallel
software work and fixed-function TTL for video timing and scan-out. It is
inspired by the original goals of layered graphics, raster events, shared
memory, and external-video capability; it makes no register-, pin-, or
cycle-level compatibility claim.

## Non-negotiable boundaries

- No FPGA, CPLD, GAL, or programmable-logic replacement. GA144 is a
  programmable processor array, not a configurable logic fabric. Counters,
  latches, arbitration, shift registers, and video emission remain
  fixed-function logic.
- The first machine is standalone, with local memory and video output. No
  connection to an Intellivision or ECS bus is authorized by this proposal.
- The preserved MAGIC material is a draft dossier, not proof that this or any
  other implementation was fabricated.
- GA144 software must not generate television timing. Its asynchronous nodes
  vary with voltage, temperature, and silicon variation; a crystal-derived
  TTL path owns sync, blanking, pixel launch, and colour-reference timing.

## Why GA144 is a candidate

The supplied [GA144A12 datasheet](../../datasheets/GA144A12-Rev-A.pdf)
describes an 18-by-8 array of 144 F18A computers with exposed 18-bit data
and address buses, GPIO, analog-capable nodes, and ROM support for external
SDRAM. It is therefore a plausible programmable rendering/control plane
without introducing programmable logic.

| Capability | Intended use |
| --- | --- |
| 144 independent nodes | Tile, object, composition, memory, diagnostic, and host-service jobs |
| Parallel bus and SDRAM-support nodes | Asset, tile-map, object-list, and render-state memory |
| GPIO and boot options | Reset, diagnostics, handshakes, and a later narrow host interface |
| Analog nodes | Experimental control or audio only; not initial video generation |
| 1.62–2.0 V, QFN-88 | Dedicated power, translation, layout, and assembly work |

Actual GA144 code must be benchmarked at the installed voltage and temperature.
The aggregate performance claim in the datasheet is not a scanline guarantee.

## TTL-video design lineage

The sibling repository contains a [16-bit TTL video-controller proposal](../../../intellivision-4182/doc/TTL-16BIT-VIDEO-CONTROLLER.md).
MAGIC-II adopts its core principles:

1. A crystal and synchronous TTL counters generate horizontal and vertical timing.
2. Display fetch owns its memory slot; no other writer drives live video RAM.
3. Two 8-bit SRAMs form one 16-bit video word, latched before pixel selection.
4. Raster/frame events are hardware signals, never software-timed approximations.
5. Composite encoding is a measured analogue subsystem; a video amplifier does
   not create missing sync, burst, black level, luminance, or chrominance.

The difference is the writer. GA144 prepares a later scanline; it does not
directly clock pixels or replace the fixed-function timing chain.

## First architecture

    SPI flash / serial diagnostic
                |
                v
       GA144A12 render fabric
      /          |           \
asset memory  job/control  line-buffer writer
    |            |            | translated interface
    +------------+------------+
                              v
crystal -> TTL timing -> ownership arbiter -> paired 5 V SRAM line buffers
              |                                      |
              +-- sync, blanking, pixel clock        v
                                                  word latch
                                                      |
                                             pixel selector/palette
                                                      |
                                            DAC and composite encoder
                                                      |
                                               75-ohm video output

### Buffer ownership

Use at least two line buffers, preferably three. Fixed TTL reads one buffer
at the crystal-derived pixel rate while GA144 writes a different future line.
Only the TTL arbiter changes ownership at a defined blanking boundary. GA144
may write only after a synchronized buffer-free handshake, and it signals ready
only after every word is valid.

This is a deliberate deterministic boundary. A missed render deadline may
repeat or blank a line in development, but it must never damage sync or create
RAM-bus contention.

## Revision-one display target

| Item | First target |
| --- | --- |
| Video | NTSC-like non-interlaced composite |
| Master clock | 14.31818 MHz crystal source |
| Logical surface | 320 × 240 at 4 bits per pixel |
| Video word | Four 4-bit pixels in a 16-bit paired-SRAM word |
| Palette | 16 digital-RGB entries, feeding a separately validated DAC/encoder |
| Render store | External SDRAM or qualified local RAM, separate from line buffers |
| Content sequence | Test patterns, tile background, then sprites |

The source dossier's 40-by-24 cards, 6-by-8 pixels, high-resolution cards,
alpha, split output, and moving-object reuse are later feature goals, not
revision-one acceptance criteria.

## GA144 work allocation

| Group | Responsibility |
| --- | --- |
| Supervisor and boot | Load code, diagnostics, reset/fault state |
| Memory service | Bounded asset fetches and render-memory transactions |
| Background workers | Tile-map resolution and tile-row expansion |
| Object workers | Clipping, scale/mirror, and object-row preparation |
| Composer | Transparency, priority, palette-index, and alpha rules |
| Line writer | Store a complete 16-bit line and issue ready |
| Event service | Consume frame/raster events and later narrow host commands |

Jobs are bounded by scanline and dispatched to available workers. Do not
permanently bind one node to one screen object; uneven object distribution
would otherwise silently defeat the line deadline.

## Timing and electrical contract

1. TTL alone creates pixel clock, sync, blanking, burst gate, line count, and
   the buffer-change instant.
2. Frame-start and raster events cross to GA144 through synchronizers and are
   advisory renderer events, never timing sources.
3. A not-ready buffer is never selected for display.
4. Renderer deadline failures increment a diagnostic counter.
5. Scope and logic-analyser captures must show sync, blanking, pixel clock,
   buffer select/free/ready, SRAM output-enable, and write-enable together.

GA144 is a 1.8 V-class part. It requires qualified, direction-controlled level
translation for every interface to 5 V SRAM or 74AC/74HCT logic. A 74HCT input
alone is not a valid 1.8 V logic-high receiver. External output enables must
remain disabled through reset: the GA144 datasheet documents output-oriented
reset states on its parallel-bus nodes.

Keep the oscillator, timing counters, line SRAM, pixel path, DAC/encoder, and
their returns physically local. GA144 memory/debug traffic must not share the
analogue-video return path.

## Implementation stages

1. Extract only legible MAGIC register diagrams into evidence tables; mark every
   uncertain field as uncertain.
2. Build a standalone TTL timing fixture with stable sync, blanking, frame and
   raster events, plus hardwired test patterns.
3. Add paired SRAM, word latch, pixel selector, and buffer ownership checks.
4. Bring up GA144 power, reset, boot, serial diagnostics, and translated
   handshakes before attaching its line-buffer data path.
5. Transfer known GA144-generated patterns into an off-screen buffer; capture
   missed-line counts and ownership transitions.
6. Add tile rendering, then object rows, transparency, priority, palette
   changes, and raster state changes one measured feature at a time.
7. Validate a baseband composite encoder into 75 ohms before external-video
   mixing, PAL/SECAM, or host-machine experiments.

## Acceptance gates

| Gate | Required evidence |
| --- | --- |
| Timing | Long-soak scope captures of stable sync, blanking, and pixel timing |
| Arbitration | Capture proving no simultaneous SRAM drivers and legal buffer swaps |
| GA144 link | Reset-safe translation and repeatable boot/diagnostic exchange |
| Rendering | GA144-produced patterns and visible missed-line counter |
| Composite | 75-ohm waveform measurements and stable lock on a named scaler/display |
| Graphics | Tile/object demo with a recorded worst-case per-line budget |

## Open questions

1. Can the selected GA144 memory and transfer routines meet the measured
   worst-case line budget with voltage and temperature margin?
2. Which translators meet the required direction control, delay, and routing
   requirements at the actual bus width?
3. Should render SDRAM and 5 V TTL line SRAM remain separate, or can a common
   store be safely arbitrated after measurement?
4. Which DAC/encoder produces a conformant initial NTSC waveform from the
   selected palette representation?

## References

- [MAGIC computer notes summary](MAGIC-computer-notes-summary.md)
- [MAGIC source PDF](CCF10272011_00005.pdf)
- [GA144A12 datasheet](../../datasheets/GA144A12-Rev-A.pdf)
- Sibling [16-bit TTL video controller](../../../intellivision-4182/doc/TTL-16BIT-VIDEO-CONTROLLER.md)
- Sibling [TTL-video workplan](../../../intellivision-4182/modules/ttl-video/WORKPLAN.md)
