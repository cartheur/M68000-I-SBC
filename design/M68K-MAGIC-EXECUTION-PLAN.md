# M68k MAGIC — execution plan

**Status:** active planning baseline

## Decision and order of work

Repair and release the existing M68k-I-SBC **before** designing or ordering
MAGIC-specific hardware.  It is a reusable 12 MHz 68HC000 firmware and
command-host platform, but it is currently under a fabrication hold.  It must
not become the final video or GA144 board: the final machine retains separate
host, TTL-video, and GA144-render domains.

Work proceeds only in this order:

```text
E0 SBC electrical release -> E1 assembled-host proof -> A0 interface freeze
    -> V1 independent TTL fixture -> G1 GA144/bridge bring-up
    -> I1 safe line writer -> R1 bounded renderer -> O1 composite output
```

A later stage may start its design documentation while its predecessor is
being measured, but no later board may be ordered or integrated before the
preceding gate passes.

## E0 — repair the existing SBC

**Purpose:** make `project/68000sbc.kicad_sch` and
`project/68000sbc.kicad_pcb` a single electrically correct, fabrication-ready
source of truth.

### E0.1 Preserve and establish a reproducible baseline

1. Keep the published production draft as evidence; do not overwrite it by
   hand.
2. Open the schematic and PCB together in KiCad 10, run *Update PCB from
   Schematic*, and save the resulting intentional changes.
3. Run `make drc` and record the resulting report before changing electrical
   routing.

**Exit evidence:** committed KiCad source changes plus a regenerated
`fabrication/production-draft/drc.json` and `DRC.md`.

### E0.2 Reconcile schematic and PCB identity

The current report names ten schematic/PCB parity findings.  Resolve their
root cause in the source—not by excluding them from DRC:

1. Synchronize the PCB footprints for `U3`, `C11`, and `C12` with their
   schematic symbols, preserving their intended values and footprints.
2. Add the four mounting holes to the schematic as explicitly excluded
   mechanical items, or configure them as intentional board-only mechanics in
   a way KiCad's parity check accepts.  They must no longer be anonymous
   `REF**` footprints.
3. Model `X1` and `X2` as mutually exclusive oscillator options, with one
   documented assembly choice.  The BOM and placement output must not imply
   that both are fitted.
4. Re-run parity checks after every synchronization step; do not mix parity
   fixes with copper edits.

**Exit gate:** zero `schematic_parity` findings.

### E0.3 Repair the known electrical fault

The current DRC identifies a physical short and an open connection involving
`Net-(C11-Pad1)` and `Net-(R3-Pad1)`, including tracks at U2 pad 5 and R3 pad
1.  Determine the intended net from the schematic, then:

1. Remove or reroute only the offending PCB copper.
2. Restore the intended R3-to-U2 connection with the board's configured hole
   clearance.
3. Verify in KiCad that the two nets remain distinct and that the intended net
   is continuous.
4. Run DRC; inspect the three `shorting_items`, three `hole_clearance`, and
   one `unconnected_items` findings explicitly rather than relying only on a
   count reduction.

**Exit gate:** zero shorts, zero hole-clearance violations, and zero
unconnected items.

### E0.4 Clear release blockers and publish fabrication inputs

1. Resolve every remaining electrical blocker reported by `make drc`.
2. Review non-blocking findings; correct defects that affect assembly,
   mechanical fit, or legibility, and document any deliberately accepted
   cosmetic items.
3. Regenerate BOM, complete placement export, socket CPL, Gerbers, drills,
   and drill report from the reconciled source.
4. Independently inspect the Gerbers and verify the oscillator assembly option
   and every socket footprint against the selected parts.

**E0 completion gate:** `make fabrication` succeeds; DRC has zero electrical
release blockers and zero schematic/PCB parity findings.  Only then may an SBC
revision be ordered.

## E1 — prove the repaired SBC as a host

1. Assemble one board with the chosen oscillator option.
2. Capture power-on reset, 12 MHz clock, ROM chip select, RAM chip select, and
   UART traffic.
3. Run the existing ROM RAM test and serial monitor; record the banner,
   memory-test result, and a serial upload/run cycle.
4. Exercise the documented open expansion window at `0x800000–0x8FFFFF` with
   a passive or fully decoded test peripheral.  Do not attach GA144 or live
   video SRAM.

**Exit gate:** repeatable cold boot, RAM test, serial upload/run, and a
contention-free peripheral read/write capture.

## A0 — freeze the new-machine interfaces

This stage creates documents, not a combined PCB.  It reconciles the host
workplan with the GA144/TTL proposal.

1. Publish `MAGIC-HOST-SPEC.md`, `VIDEO-REGISTER-ABI.md`,
   `HOST-VIDEO-CONNECTOR.md`, and `MEMORY-MAP.md` as called for by the host
   workplan.
2. Define one narrow M68k-to-GA144 command/completion transport: sequence
   number, payload limit, FIFO depth, reset behavior, overflow behavior, and
   interrupt semantics.
3. Define the GA144-to-TTL line protocol exactly: `FREE -> GRANTED ->
   WRITING -> READY -> DISPLAYING -> FREE`, synchronizers, timeout behavior,
   and the safe repeat/blank result.
4. Make a crossing table listing every signal's owner, voltage domain,
   direction, pull/reset state, clock domain, translator, and test point.
5. Select the initial physical target: 320 x 240, 4 bpp, 14.31818 MHz source,
   three line buffers, and a local asynchronous-SRAM render store for the
   first revision.  SDRAM is deferred until separately demonstrated.

**Exit gate:** reviewed interface pack; no unnamed crossing, raw 1.8 V/5 V
connection, or shared live-scan-out store remains.

## V1 — independent TTL video fixture

1. Create a separate video-board schematic and build crystal timing, counters,
   sync/blanking, raster/frame events, and hardwired patterns.
2. Add three paired-SRAM line buffers, word latch, pixel selector, and fixed
   TTL ownership arbiter.
3. Probe pixel clock, sync, blanking, buffer select, SRAM OE/WE, and ownership
   signals together during normal operation and injected missing-ready cases.

**Exit gate:** long-soak stable timing and legal swaps, with repeat/blank on
underflow and no sync disturbance.

## G1 — GA144 and bridge bring-up

1. Build or obtain a dedicated GA144 bring-up board with correct 1.8 V power,
   reset, boot/diagnostic access, decoupling, and no enabled 5 V outputs at
   reset.
2. Validate cold boot, diagnostic exchange, thermal behavior, and all selected
   translators before connecting line-SRAM data pins.
3. Implement host-command echo and completion/status FIFO; deliberately test
   overflow, reset during transfer, and fault recovery.

**Exit gate:** repeatable boot and fault-safe bidirectional command/status
exchange, with no unsafe external drive state.

## I1 — controlled line writer

1. Connect only the synchronized `grant`/`ready` controls and a translated
   line-write path to an off-screen line buffer.
2. Write known patterns; inject late and absent `ready`; capture ownership and
   SRAM enables.

**Exit gate:** no simultaneous SRAM drivers and no timing-chain disturbance
during normal, late, absent-ready, reset, and recovery cases.

## R1 — bounded renderer

1. Add tile-row rendering, then object-row composition, transparency, priority,
   and palette-index output one feature at a time.
2. Record worst-case per-line execution and transfer budget at the installed
   voltage and temperature.

**Exit gate:** a measured worst-case scene meets the line deadline with margin.
Misses are visibly counted and safely repeat or blank only the affected line.

## O1 — analogue output and later features

1. Validate DAC/composite encoder into 75 ohms with captured waveforms and a
   named display/scaler.
2. Integrate the host command API and diagnostic UI only after the renderer
   passes I1.
3. Consider alpha, high-resolution card modes, external-video work, PAL, and
   SECAM as separate gated projects.

**Completion gate:** stable demonstrated system with published captures for
timing, ownership, GA144 link, host link, rendering deadline, and video output.

## Immediate checklist

- [ ] Run and archive a fresh KiCad DRC baseline.
- [ ] Reconcile `U3`, `C11`, `C12`, mounting holes, and oscillator options.
- [ ] Repair the `C11`/`R3`/`U2` copper conflict and open connection.
- [ ] Regenerate DRC; repeat until all electrical and parity gates pass.
- [ ] Regenerate and review the fabrication package.
- [ ] Assemble and prove one SBC before beginning A0/V1 hardware work.

## Related documents

- [SBC manufacturing gate](../fabrication/production-draft/MFG-READINESS.md)
- [Published DRC report](../fabrication/production-draft/DRC.md)
- [M68k MAGIC host work plan](M68K-MAGIC-HOST-WORKPLAN.md)
- [M68k-GA144-TTL workplan](M68K-GA144-TTL-WORKPLAN.md)
- [GA144-assisted TTL MAGIC-II proposal](GA144-TTL-MAGIC-II-PROPOSAL.md)
