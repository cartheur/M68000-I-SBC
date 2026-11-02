# M68k MAGIC host — design recommendation

## Decision

Use the M68k-I-SBC as a **reference and firmware starting point** for a new
M68k MAGIC-host project.  It is a substantially better conceptual match for a
MAGIC-inspired machine than a 6309 SBC: MAGIC's draft material assumes a
68000-style, 16-bit CPU interface.

Do **not** adopt the existing SBC unmodified as the final video machine.  Its
12 MHz 68HC000 is a capable host for game/application logic, command creation,
asset management, and bounded rendering work, but it must not be responsible
for pixel timing or directly contend for live display memory.

The architecture rule is simple:

> TTL owns deterministic scan-out. The 68k prepares work and communicates
> through a bounded video interface.

## Proposed system boundary

```text
M68k MAGIC Host
  68000 + ROM + CPU RAM + UART/storage
  memory-mapped video command/status interface
                 |
                 v
TTL MAGIC Video Board
  crystal timing + arbitration + line SRAM + pixel/palette + encoder
```

The video board remains responsible for pixel clock, sync, blanking, composite
timing, line-buffer ownership, and scan-out.  CPU software may miss a render
deadline, but that must at worst repeat or blank a line; it must never disturb
sync or cause memory-bus contention.

## Recommended improvements

### 1. Fully decode the address map

The source SBC deliberately uses minimal decoding, so it has mirrored and
forbidden regions.  That is practical for a small standalone computer but is
not appropriate for a video bus.  Create explicitly decoded, non-overlapping
regions.  One possible starting map is:

| Address range | Function |
| --- | --- |
| `000000-00FFFF` | ROM / boot monitor |
| `010000-0FFFFF` | CPU RAM |
| `100000-10FFFF` | Video registers, palette, status |
| `110000-11FFFF` | Video command or display-list RAM |
| `120000-12FFFF` | Optional shared render-memory aperture |
| `200000+` | UART, storage, and future I/O |

The exact allocation can change, but no unintended device should respond to an
address access.

### 2. Make video a memory-mapped peripheral

Define a stable programmer-visible interface instead of exposing an informal
raw expansion bus.  Initial registers should cover:

- command FIFO or display-list base and control;
- palette writes and video-mode selection;
- raster compare and enable bits;
- frame and line counters;
- line-buffer ownership (`free`, `writing`, `ready`, `displaying`);
- vblank/raster/underflow status and interrupt acknowledgement; and
- diagnostic and deadline-failure counters.

Provide VBlank and programmable raster interrupts to the 68k.  Those are
software notifications, not timing sources.

### 3. Keep memory domains separate

Use three distinct classes of memory:

| Memory | Owner / access rule |
| --- | --- |
| CPU RAM | Private 68k program and data memory |
| Render/asset RAM | Shared only through bounded arbitration or a controlled aperture |
| Line SRAM | Double- or triple-buffered; TTL reads the active line at pixel rate |

The CPU/renderer may write only a buffer granted by the TTL ownership logic.
It marks a buffer ready only after the complete line is valid.  A not-ready
buffer is never selected for display.

For early boards, paired asynchronous 8-bit SRAMs giving a 16-bit path are
preferable to SDRAM: they are simpler, easier to probe, and more deterministic.

### 4. Strengthen the 68k memory and bus implementation

Use matched 8-bit memory devices as a real 16-bit bank and correctly support
the 68000's `/UDS` and `/LDS` byte strobes.  Add registered transceivers or
buffers where the CPU bus leaves the host board, with explicit direction
control and reset-safe output enables.

Do not put a raw high-rate pixel or live-SRAM bus on a general-purpose cable.
Keep the timing chain, line SRAM, pixel path, and encoder local to the video
board.

### 5. Design for a qualified faster CPU option

The existing 12 MHz 68HC000 is sufficient for bring-up and a first functional
host.  A new board should be designed and timed for a socketed, qualified
16-20 MHz 68HC000/68000-class option if the selected parts and board signal
integrity allow it.  This improves command processing and software rendering;
it does not move deterministic scan-out out of TTL.

### 6. Define the timing and interrupt contract

Synchronize the following crossings between TTL video and the host:

- frame start and VBlank;
- optional raster/scan-line compare;
- buffer free, write grant, ready, and display select;
- video fault or renderer-deadline failure; and
- reset and safe-output state.

Logic-analyser and scope captures should show sync, blanking, pixel clock,
buffer select/free/ready, and SRAM output/write enables together.

### 7. Specify a documented host/video connector

Replace informal expansion pads with a documented 5 V parallel bus connector.
At minimum it should carry:

- `D0-D15`, the selected address lines, `/AS`, `/UDS`, `/LDS`, `R/W`, and
  `/DTACK`;
- reset, clock, interrupt, power, and ground; and
- dedicated video handshake signals.

The connector and protocol should be specified before PCB layout, including
voltage levels, signal direction, reset states, and maximum operating rate.

### 8. Put diagnostics in revision one

Retain serial-monitor support and add:

- a hardware test-pattern generator;
- readable timing and frame counters;
- register loopback/self-test support;
- line-buffer underflow and missed-deadline indicators; and
- labelled test points for sync, blanking, pixel clock, and ownership signals.

These facilities are especially important before composite encoding and
external-video work begin.

## Source-SBC caveat

The inspected M68k-I-SBC is a useful small 68k computer, but its current
fabrication draft is on hold because its published DRC identifies electrical
and schematic/PCB parity blockers.  Preserve it as a reference.  Repair it
only if a standalone SBC is desired; create a distinct derivative repository
or board revision for the M68k MAGIC host.

## Suggested project scope

Name the project **M68k-MAGIC Host** and stage it as follows:

1. Bring up the repaired/new 68k host with ROM monitor, RAM, and serial I/O.
2. Implement the memory-mapped video-register block and VBlank interrupt.
3. Bring up the independent TTL timing fixture and line-buffer ownership
   state machine.
4. Join host and video board through the documented handshake interface.
5. Demonstrate test patterns, tile backgrounds, then sprites and later
   MAGIC-inspired display features.

## Relationship to the existing MAGIC-II proposal

This recommendation changes the host processor option, not the deterministic
video principles.  The existing TTL-video direction still applies: a
crystal-derived TTL chain owns sync, blanking, pixel launch, and the moment at
which line buffers change ownership.  The M68k replaces neither that chain nor
the need for measured analogue video work.

## References

- [`MAGIC-computer-notes-summary.md`](MAGIC-computer-notes-summary.md)
- [`GA144-TTL-MAGIC-II-PROPOSAL.md`](GA144-TTL-MAGIC-II-PROPOSAL.md)
- M68k-I-SBC: `/home/cartheur/ame/aiventure/aiventure-github/cartheur/M68k-I-SBC/`
- M68k-I-SBC manufacturing gate:
  `/home/cartheur/ame/aiventure/aiventure-github/cartheur/M68k-I-SBC/fabrication/production-draft/MFG-READINESS.md`
