# M68k MAGIC Host work plan

## Objective

Build a purpose-designed 68000 host for the MAGIC TTL video system.  The host
submits bounded rendering work; it does not generate display timing or access
the active line buffer.  No FPGA or CPLD is permitted.

The existing `project/` board remains a reference and firmware bring-up
platform.  New host design files will live in `magic-host/` after the
architecture gate is passed.

## Non-negotiable design rules

- TTL owns pixel clock, sync, blanking, scan-out, and line-buffer ownership.
- The host/video boundary is a documented 5 V peripheral bus, not a raw video
  or live-SRAM bus.
- All host address decoding is explicit and non-overlapping.
- CPU RAM, shared render/asset RAM, and line SRAM are distinct memory domains.
- A missed render deadline may repeat or blank a line; it must not affect sync.
- Every board release must have zero electrical DRC blockers and a published
  DRC report.

## Phase 0 — freeze the architecture contract

Deliverables:

1. `MAGIC-HOST-SPEC.md`: CPU clock target, reset behaviour, power budget,
   connectors, and bring-up sequence.
2. `VIDEO-REGISTER-ABI.md`: register offsets, widths, reset values, access
   semantics, interrupt acknowledgement, and reserved space.
3. `HOST-VIDEO-CONNECTOR.md`: pinout, direction, pull states, timing budget,
   ground allocation, and cable/rate limits.
4. `MEMORY-MAP.md`: final decoded map and chip-select equations.

Exit gate: the host/video boundary, ownership state machine, and interrupt
contract are reviewed before selecting footprints or drawing a schematic.

Initial address-map reservation:

| Range | Function |
| --- | --- |
| `000000-00FFFF` | ROM / monitor |
| `010000-0FFFFF` | private CPU RAM |
| `100000-10FFFF` | video registers, palette, status |
| `110000-11FFFF` | command/display-list RAM |
| `120000-12FFFF` | optional controlled shared aperture |
| `200000+` | UART, storage, future I/O |

## Phase 1 — host electrical architecture

1. Choose qualified, socketed CPU and oscillator options: 12 MHz bring-up;
   16–20 MHz only after timing validation.
2. Select paired 8-bit asynchronous SRAMs for a genuine 16-bit CPU path.
3. Implement `/UDS`, `/LDS`, `/AS`, `R/W`, `/DTACK`, reset, and bus-error
   behaviour deliberately; record the timing budget.
4. Design 74xx-family decode, arbitration, and registered bus-buffer logic.
5. Define reset-safe states so the connector cannot drive an unpowered or
   resetting video board.
6. Retain serial monitor support and make storage optional, not a bring-up
   dependency.

Exit gate: reviewed schematic block diagram, chip-select truth table, and
   timing worksheet.  No unresolved multi-device select or mirrored address.

## Phase 2 — video peripheral contract

Implement the smallest useful revision-one register set:

- identification/version and feature bits;
- command/display-list base and doorbell/control;
- palette/mode control;
- frame and line counters;
- `free`, `write-grant`, `ready`, and `displaying` ownership status;
- VBlank, raster, underflow, and deadline-failure status/acknowledgement; and
- diagnostic/test-pattern controls and counters.

Exit gate: a register-level test plan proves every register's reset state,
read/write behaviour, interrupt behaviour, and safe response to invalid work.

## Phase 3 — independent TTL video fixture

1. Build the crystal-derived timing, sync, blanking, and test-pattern chain.
2. Implement double or triple line-SRAM buffers and ownership logic.
3. Scope pixel clock, sync, blanking, buffer select, SRAM OE/WE, and ownership
   handshakes together.
4. Prove that missing host work repeats/blanks a line without disturbing sync.

Exit gate: repeatable waveform captures and a documented underflow result.

## Phase 4 — schematic and PCB capture

1. Create `magic-host/` KiCad project from a new schematic; do not mutate the
   held production draft into this design.
2. Place CPU, memory, decode, connector, UART, and labelled test points.
3. Keep high-rate video timing and line SRAM physically on the video board.
4. Add decoupling, reset/enable pull states, power-entry protection, and test
   pads before routing.
5. Generate BOM and socket-only assembly placement data from the schematic.

Exit gate: ERC reviewed, board DRC has zero electrical blockers, fabrication
outputs and DRC report are regenerated, and connector pinout matches Phase 0.

## Phase 5 — firmware and integration

1. Port the monitor to the final decoded map; test ROM, RAM, serial, and
   interrupts without the video board attached.
2. Add video-register probe, counter readout, loopback, and fault reporting.
3. Demonstrate VBlank interrupt, a test pattern, one tile background, then
   sprites/display-list work.
4. Record logic-analyser captures for normal operation, reset, and deliberate
   renderer underflow.

Exit gate: host reset or software stalls cannot perturb video sync; integration
tests demonstrate bounded ownership transfers and visible diagnostics.

## Immediate next actions

1. Write the Phase 0 register ABI and connector specification.
2. Decide the initial video mode, pixel clock, line-buffer width/depth, and
   whether the first output is RGB, composite, or both.
3. Choose the physical connector family only after the required signal count,
   ground returns, and clock-rate budget are known.
4. Create the clean `magic-host/` KiCad project and architecture block diagram.
