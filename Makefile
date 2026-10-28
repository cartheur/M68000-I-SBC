.PHONY: tools firmware rom drc fabrication clean

KICAD_CLI ?= flatpak run --command=kicad-cli org.kicad.KiCad
PCB       := project/68000sbc.kicad_pcb
FAB_DIR   := fabrication/production-draft

tools:
	$(MAKE) -C tools/vasm CPU=m68k SYNTAX=mot

firmware: tools
	$(MAKE) -C code

rom: tools
	$(MAKE) -C code rom

drc:
	mkdir -p $(FAB_DIR)
	$(KICAD_CLI) pcb drc $(PCB) --output $(FAB_DIR)/drc.json --format json --severity-all --all-track-errors --schematic-parity
	python3 tools/publish_drc_report.py $(FAB_DIR)/drc.json $(FAB_DIR)/DRC.md

fabrication: drc
	mkdir -p $(FAB_DIR)/gerbers
	$(KICAD_CLI) pcb export gerbers --output $(FAB_DIR)/gerbers --layers F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,F.Paste,B.Paste,Edge.Cuts --use-drill-file-origin --precision 6 $(PCB)
	$(KICAD_CLI) pcb export drill --output $(FAB_DIR)/gerbers --format excellon --drill-origin plot --excellon-units mm --excellon-zeros-format decimal --excellon-separate-th --generate-map --map-format gerberx2 --generate-report --report-path $(FAB_DIR)/drill-report.txt $(PCB)

clean:
	$(MAKE) -C code clean
