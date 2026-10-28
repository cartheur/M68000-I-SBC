# By default, use the first connected FTDI USB-serial cable we find. (macOS)
# May be overridden by setting the $FTDI_DEV environment variable in your shell
# configuration.
FTDI_DEV ?= $(firstword $(wildcard /dev/cu.usbserial-*))

# Clock frequency in Hz
F_CPU = 12000000
# Serial baud rate
BAUD  = 57600

# make         - build test program
# make load    - load test program binary using serial loader
TESTPROG  = fizzbuzz

# make rom     - build ROM image
# make burnrom - burn ROM image to EEPROMs using minipro
ROM_SRC   = rom.asm
ROM_RAW   = rom.bin
ROM_LST   = rom.lst
ROM_BIN_L = rom-l.bin
ROM_BIN_U	= rom-u.bin
ROM_DASM  = rom-dasm.lst
ROM_BIN   = $(ROM_BIN_L) $(ROM_BIN_U)
ROM_SPLITTER = ../tools/split_68k_rom.py

# Assembler and disassembler selection
VASM ?= ../tools/vasm/vasmm68k_mot
AS   = $(VASM)
DAS = vda68k
SERIALTERM = python3 -m serial.tools.miniterm --raw --eol LF

# Assembler options
# -nowarn=2028: don't warn when loading a constant >= 128 with moveq
ASFLAGS = -esc -DF_CPU=$(F_CPU) -DBAUD=$(BAUD) -m68000 -nowarn=2028
ASFLAGS_SREC = -Fsrec
ASFLAGS_BIN  = -Fbin

#-------------------------------------------------------------------------------
TESTPROG_SRC = $(TESTPROG).asm
TESTPROG_BIN = $(TESTPROG).bin
TESTPROG_LST = $(TESTPROG).lst

.PHONY: all clean rom flashrom

all: $(TESTPROG_BIN)

$(TESTPROG_BIN): $(TESTPROG_SRC)
	$(AS) $(ASFLAGS) -o $@ $(ASFLAGS_BIN) -L $(TESTPROG_LST) $<

load: $(TESTPROG_BIN)
	./serload.py $< $(FTDI_DEV)

run: load
	$(SERIALTERM) $(FTDI_DEV) $(BAUD)

rom: $(ROM_RAW) $(ROM_SPLITTER)
	python3 $(ROM_SPLITTER) $(ROM_RAW) $(ROM_BIN_L) $(ROM_BIN_U)

serial:
	$(SERIALTERM) $(FTDI_DEV) $(BAUD)

$(ROM_RAW): $(ROM_SRC)
	$(AS) $(ASFLAGS) -o $@ $(ASFLAGS_BIN) -L $(ROM_LST) $<

$(ROM_DASM): $(ROM_RAW)
	$(DAS) $< > $@

clean:
	rm -f *.bin *.srec *.lst

burnrom: rom
	@echo "Insert lower (odd) ROM and press Return:"
	@read
	@echo "Programming lower (odd) ROM"
	minipro -p AT28C256 -w $(ROM_BIN_L)
	@echo "Insert upper (even) ROM and press Return:"
	@read
	@echo "Programming upper (even) ROM"
	minipro -p AT28C256 -w $(ROM_BIN_U)
	@echo "Done"

