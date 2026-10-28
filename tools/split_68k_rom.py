#!/usr/bin/env python3
"""Split a 16-bit 68000 ROM image into upper- and lower-byte EEPROM images."""

from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) != 4:
        print(f"usage: {Path(sys.argv[0]).name} INPUT.BIN LOWER.BIN UPPER.BIN", file=sys.stderr)
        return 2

    source, lower_path, upper_path = map(Path, sys.argv[1:])
    image = source.read_bytes()
    if len(image) % 2:
        print(f"{source}: image length must be even, got {len(image)} bytes", file=sys.stderr)
        return 1

    # D15-D8 is stored at an even address; D7-D0 at an odd address.
    lower_path.write_bytes(image[1::2])
    upper_path.write_bytes(image[0::2])
    print(f"split {len(image)} bytes into {len(image) // 2}-byte EEPROM images")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
