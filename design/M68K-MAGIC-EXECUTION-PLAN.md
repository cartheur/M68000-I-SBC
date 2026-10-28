# M68k MAGIC — execution plan

**Status:** source-recovery active

## Decision and order of work

Recover a trustworthy KiCad 10 project from the preserved KiCad 5.1.5 source,
then repair and release the existing M68k-I-SBC **before** designing or ordering
MAGIC-specific hardware.  It is a reusable 12 MHz 68HC000 firmware and
command-host platform, but it is currently under a fabrication hold.  It must
not become the final video or GA144 board: the final machine retains separate
host, TTL-video, and GA144-render domains.

Work proceeds only in this order:

```text
S0 KiCad source recovery -> E0 SBC electrical release -> E1 assembled-host proof -> A0 interface freeze
    -> V1 independent TTL fixture -> G1 GA144/bridge bring-up
    -> I1 safe line writer -> R1 bounded renderer -> O1 composite output
```

A later stage may start its design documentation while its predecessor is
being measured, but no later board may be ordered or integrated before the
preceding gate passes.

## S0 — recover the KiCad 5 design as a valid KiCad 10 project

**Purpose:** establish one openable, reproducible KiCad 10 source before
altering electrical connectivity or board copper.

`project-5/` is the preserved authority.  It contains the original KiCad 5.1.5
`.pro`, `.sch`, and `.kicad_pcb` files.  Do not edit, resave, or use it as a
KiCad 10 working directory.  Ignore per-user files such as `.kicad_prl`.

The native KiCad 5 outputs in `project-5/` are the electrical baseline:

| Evidence | Result | Required treatment |
| --- | --- | --- |
| `68000sbc.rpt` PCB DRC | 13 courtyard overlaps; zero unconnected pads | Preserve; the overlaps require later mechanical review, not copper repair. |
| `68000sbc.erc` schematic ERC | 1 error, 6 warnings | Reproduce after migration, then resolve deliberately in E0. |

The ERC error connects the outputs of both overlapping oscillator alternatives
(`X1` and `X2`) as though both were fitted.  This is a real schematic defect,
even though the physical board is intended to accept one oscillator package at
a time.  It must not be suppressed as a generic ERC exception.

The KiCad 5 PCB report disproves using the current KiCad 10 report's apparent
shorts/open connection as the reason to alter original copper.

### S0.1 Prepare the recovery workspace

1. Record SHA-256 checksums for the three authority files in `project-5/` and
   the KiCad 5 DRC report.
2. Create a new, otherwise empty `project-10-recovery/` directory from copies
   of the three authority files.  Never convert in place.
3. Use a known-working KiCad installation.  It must open a blank schematic,
   place a standard symbol, save, close, and reopen without hanging before it
   is used for this project.

### S0.2 Convert and validate the schematic

1. Open the copied legacy `.sch` in the graphical Schematic Editor and let
   KiCad create a new `.kicad_sch` file in `project-10-recovery/`.
2. Resolve legacy symbols only through the standard libraries named by the
   original schematic.  Confirm each remapped symbol's reference, value,
   footprint, pin count, and pin-number mapping; do not accept a similarly
   named symbol with different pins.
3. Save, close the application, reopen the new `.kicad_sch`, and run ERC.
4. Publish the ERC report and record all intentional warnings separately from
   errors.

**Exit gate:** the new schematic opens and reopens without a symbol-cache,
instance-ID, or missing-symbol failure; every placed symbol is resolved and
ERC output is reproducible.

### S0.3 Convert/link the PCB and compare the baseline

1. Open the copied legacy PCB in the same recovery project and save it as the
   new KiCad 10 PCB.
2. Use *Update PCB from Schematic* only after S0.2 passes.  Review each
   proposed footprint/link change; reject any unexplained net, pad, or
   footprint substitution.
3. Run KiCad 10 DRC with schematic/PCB parity enabled.
4. Compare the resulting electrical findings with `project-5/68000sbc.rpt`
   and `project-5/68000sbc.erc`.
   A new short, open connection, or parity error is a migration defect until
   its difference from the KiCad 5 sources is demonstrated.

**S0 completion gate:** KiCad 10 can reopen both recovery files, schematic to
PCB linkage is valid, and DRC has no unexplained electrical finding relative
to the KiCad 5 baseline.  Only `project-10-recovery/` may proceed to E0.

## E0 — repair the existing SBC

**Purpose:** make the recovered KiCad 10 schematic and PCB a single
electrically correct, fabrication-ready source of truth.  At E0 entry, replace
the disputed migrated source only through an explicit reviewed handoff from
`project-10-recovery/`; do not repair the old migration in place.

### E0.1 Preserve and establish a reproducible baseline

1. Keep the published production draft and KiCad 5 report as evidence; do not
   overwrite either by hand.
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
2. Select one electrically connected oscillator implementation.  Model the
   other package as an assembly alternative that cannot drive `CPUCLK` at the
   same time; a DNP note alone does not remove the ERC output-driver conflict.
3. Add the four mounting holes to the schematic as explicitly excluded
   mechanical items, or configure them as intentional board-only mechanics in
   a way KiCad's parity check accepts.  They must no longer be anonymous
   `REF**` footprints.
4. Model the retained oscillator package as the documented assembly choice.
   The BOM and placement output must not imply that both are fitted.
5. Re-run parity checks after every synchronization step; do not mix parity
   fixes with copper edits.

**Exit gate:** zero `schematic_parity` findings.

### E0.3 Resolve verified electrical findings

Do not repair copper based on the disputed pre-recovery KiCad 10 report.  In
particular, its apparent `C11`/`R3`/`U2` short/open combination was absent from
the native KiCad 5 PCB DRC and is presumed to be a migration artifact unless
the recovery project reproduces it.

1. Triage every recovery DRC/ ERC error against the native KiCad 5 reports.
2. Fix the verified oscillator-output conflict first, by choosing one
   electrically active oscillator path.
3. For each newly demonstrated board fault, determine the intended net in the
   recovered schematic before changing copper; remove or reroute only the
   affected copper and verify continuity/clearance in KiCad.
4. Run DRC after each electrical correction and inspect every remaining short,
   clearance, and unconnected-item finding individually.

**Exit gate:** zero verified shorts, zero hole-clearance violations, zero
unconnected items, and no unresolved ERC errors.

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

- [ ] Preserve the `project-5/` authority files and native KiCad 5 ERC/DRC reports.
- [ ] Establish a known-working KiCad environment using a blank schematic.
- [ ] Convert into `project-10-recovery/`, then prove open/reopen and ERC.
- [ ] Link the recovery PCB and compare its DRC with the KiCad 5 baseline.
- [ ] Approve the recovery project as the sole E0 working source.
- [ ] Run and archive a fresh KiCad 10 DRC baseline.
- [ ] Reconcile `U3`, `C11`, `C12`, mounting holes, and oscillator options.
- [ ] Resolve the verified `X1`/`X2` oscillator-output ERC error.
- [ ] Regenerate DRC; repeat until all electrical and parity gates pass.
- [ ] Regenerate and review the fabrication package.
- [ ] Assemble and prove one SBC before beginning A0/V1 hardware work.

## Related documents

- [SBC manufacturing gate](../fabrication/production-draft/MFG-READINESS.md)
- [Published DRC report](../fabrication/production-draft/DRC.md)
- [M68k MAGIC host work plan](M68K-MAGIC-HOST-WORKPLAN.md)
- [M68k-GA144-TTL workplan](M68K-GA144-TTL-WORKPLAN.md)
- [GA144-assisted TTL MAGIC-II proposal](GA144-TTL-MAGIC-II-PROPOSAL.md)
