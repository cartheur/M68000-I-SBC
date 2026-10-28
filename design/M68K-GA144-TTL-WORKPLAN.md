# M68k–GA144–TTL MAGIC workplan

**Status:** proposed workplan

## Objective

Develop a historically informed, MAGIC-inspired video computer with three
strictly separated roles:

| Domain | Responsibility | It must not do |
| --- | --- | --- |
| M68k host | Application/game code, assets, display commands, debug monitor | Generate television timing or write live scan-out memory |
| GA144 fabric | Parallel bounded rendering, line preparation, render-memory service | Generate television timing or own buffer swaps |
| Fixed TTL video | Crystal timing, arbitration, live line-SRAM scan-out, palette and encoder feed | Depend on software for a pixel-time decision |

The first target remains a standalone, NTSC-like, non-interlaced 320 × 240,
4-bits-per-pixel system.  This is a new machine inspired by MAGIC, not a
register- or cycle-compatible reconstruction.

## Architecture contract

```text
            commands, assets, completion/status
 +----------------------------+
 |          M68k host         |
 | program RAM, ROM, UART     |
 +--------------+-------------+
                | 5 V host bus
                v
 +----------------------------+
 | host/GA144 bridge          |
 | decoded registers, FIFO,   |
 | CDC, direction-controlled  |
 | 5 V <-> 1.8 V translation  |
 +--------------+-------------+
                | narrow, asynchronous mailbox protocol
                v
 +----------------------------+       free / grant / ready
 | GA144 render fabric        |<----------------------------+
 | jobs, composition, assets  |                             |
 +--------------+-------------+                             |
                | translated line-write interface           |
                v                                            |
 +-----------------------------------------------------------+--+
 | fixed TTL timing, ownership arbiter, paired line SRAM,       |
 | word latch, pixel selector/palette, DAC/composite encoder    |
 +---------------------------------------------------------------+
```

The bridge is essential: the M68k bus is 5 V and synchronous to its own clock;
the GA144 is a 1.8 V asynchronous multicore part.  Do not connect the raw M68k
bus to GA144 pins, and do not make GA144 a direct master of the M68k bus in
revision one.

## Liaison contracts

### M68k ↔ GA144: command and completion plane

The M68k submits work through memory-mapped bridge registers and a bounded
command FIFO (or descriptor ring in host-owned RAM).  GA144 returns completion
records and counters through a separate bridge-visible FIFO/register bank.

Initial command types:

- set frame state: display-list base, scroll, palette-bank, and frame tag;
- update tile-map or asset references;
- submit object rows and composition attributes;
- request a diagnostic/test pattern; and
- fence: report all work accepted before a frame/raster boundary.

Every command must contain a sequence number and bounded payload length.
Status must expose FIFO space, FIFO overflow, last accepted/completed sequence,
GA144 reset/fault state, and deadline-miss counts.  The host may poll these
registers and may receive a completion or fault interrupt; neither is a timing
source for scan-out.

### GA144 ↔ TTL: render and line-buffer plane

TTL alone owns the state transition of each line buffer:

```text
FREE -> GRANTED -> WRITING -> READY -> DISPLAYING -> FREE
```

- TTL asserts a synchronized `grant` only for a free, off-screen buffer.
- GA144 may drive line-SRAM write controls/data only while `grant` is active.
- GA144 asserts `ready` only after the entire requested line is committed.
- TTL samples `ready` at its defined boundary and selects a ready buffer.
- A missing `ready` causes a defined safe result (repeat or blank) and bumps a
  TTL-visible underflow counter.

GA144 receives frame and raster events only through synchronizers.  It cannot
select the displayed buffer, alter the pixel clock, or drive SRAM output enable.

### M68k ↔ TTL: control, observation, and interrupts

The host accesses a fully decoded TTL/video register block.  It can configure
mode, palette shadow values, raster compare, interrupt enables, and diagnostic
patterns.  It can read frame/line counters, ownership state, underflows, and
fault latches.

Writes that change scan-out state take effect only at a TTL-defined safe
boundary.  VBlank and raster interrupts are acknowledged through this block.

## Electrical rules

1. Use qualified 1.8 V ↔ 5 V translators with direction control for every
   GA144/TTL and GA144/bridge signal.  A 74HCT input is not a valid 1.8 V
   receiver.
2. Keep all GA144-facing outputs disabled during reset.  Provide pull states
   that leave line-SRAM writes and external bus drivers inactive.
3. Synchronize every single-bit control crossing; use an acknowledged FIFO or
   toggle/acknowledge protocol for multi-bit transfers.
4. Keep crystal, TTL timing counters, line SRAM, pixel path, DAC/encoder, and
   analogue return physically local.  Do not route them through the host/video
   connector.
5. Establish logic-family voltage thresholds, translator delay budget, maximum
   trace length, and reset sequence before schematic capture.

## Milestones and gates

### P0 — evidence and interface freeze

Deliverables:

- extract only legible MAGIC evidence into marked evidence tables;
- publish the first host address map and register map;
- publish command, completion, and buffer-ownership protocol drafts; and
- choose connector, translator candidates, power domains, and reset order.

Gate: every crossing has a named owner, voltage domain, direction, reset state,
and clock-domain-crossing method.

### P1 — independent TTL video fixture

Deliverables:

- 14.31818 MHz-derived timing, sync, blanking, frame, and raster events;
- hardwired test patterns;
- double/triple line-SRAM buffering and ownership arbiter; and
- scope/logic-analyser test points.

Gate: long-soak captures prove stable sync and legal buffer swaps without an
M68k or GA144 attached.

### P2 — M68k host base

Deliverables:

- repaired or new, fully decoded 68k host board;
- ROM monitor, RAM test, serial diagnostic path, and documented expansion
  connector; and
- memory-mapped stub registers for the future video bridge.

Gate: host passes RAM/ROM/serial tests and can read/write every bridge stub
without mirrored selects or illegal bus contention.

### P3 — GA144 bring-up and bridge

Deliverables:

- GA144 power, reset, boot, serial diagnostics, and thermal/power checks;
- reset-safe, direction-controlled translation; and
- host-to-GA144 command FIFO and GA144-to-host completion/status path.

Gate: repeatable cold boot, sequence-numbered command echo, deliberate FIFO
overflow reporting, and fault recovery with no unsafe external drive state.

### P4 — GA144 to TTL controlled writer

Deliverables:

- synchronized `grant`/`ready` protocol;
- GA144 writes known patterns only to granted off-screen buffers; and
- TTL reports underflow/deadline events to host-visible counters.

Gate: captures prove no overlapping SRAM drivers, no change to sync timing,
and safe repeat/blank behaviour under injected late or absent `ready`.

### P5 — bounded renderer

Deliverables:

- GA144 tile-row rendering, then object-row rendering;
- transparency, priority, and palette-index composition; and
- per-line execution/bandwidth instrumentation.

Gate: a recorded worst-case scene meets the chosen line deadline with explicit
voltage and temperature margin.  Do not infer a guarantee from GA144 aggregate
performance figures.

### P6 — host/renderer software model

Deliverables:

- 68k command API and example program;
- display-list/asset upload path;
- VBlank/raster event handling; and
- diagnostic UI exposing sequence, FIFO, ownership, and miss counters.

Gate: host changes scenes using commands only; it never writes active line
SRAM or depends on software-timed video events.

### P7 — composite and feature expansion

Deliverables:

- measured DAC/composite encoder into 75 ohms;
- named-display/scaler lock test; and
- incremental later features: alpha, richer card modes, object reuse,
  external-video experiments, and PAL/SECAM only after the base path is stable.

Gate: captured waveforms and a stable displayed demonstration accompany every
new feature claim.

## First revision acceptance criteria

| Area | Required evidence |
| --- | --- |
| TTL timing | Long-soak scope captures of sync, blanking, and pixel timing |
| Buffer safety | Logic-analyser capture of legal ownership transitions and SRAM enables |
| GA144 link | Repeatable boot, reset-safe translation, command/completion exchange |
| Host link | Fully decoded registers, documented interrupts, no bus contention |
| Rendering | GA144-generated test/tile/object scenes plus visible deadline counters |
| Video output | 75-ohm waveform measurements and stable lock on a named display/scaler |

## Explicit non-goals for revision one

- Direct GA144 ownership of the M68k bus.
- Software-generated sync, blanking, colour burst, or pixel clock.
- A shared, unarbitrated store for GA144, M68k, and live scan-out.
- FPGA/CPLD/GAL replacement of the fixed TTL timing/arbitration path.
- Claims of MAGIC compatibility or reconstruction accuracy beyond documented
  evidence.

## Open decisions to resolve in P0

1. Command FIFO versus descriptor ring: which gives the clearest bounded
   latency and simplest 68k implementation?
2. Number of line buffers: begin with two or adopt three to increase renderer
   slack?
3. Render-memory choice: qualified SRAM for initial determinism, or separate
   SDRAM after its controller and margins are demonstrated?
4. Which translators meet the real direction, delay, and signal-integrity
   requirements at the selected interface width?
5. Which encoder/DAC path delivers the initial measured NTSC-like output?

## Related documents

- [M68k MAGIC host recommendation](M68K-MAGIC-HOST-RECOMMENDATION.md)
- [GA144-assisted TTL MAGIC-II proposal](GA144-TTL-MAGIC-II-PROPOSAL.md)
- [MAGIC computer notes summary](MAGIC-computer-notes-summary.md)
