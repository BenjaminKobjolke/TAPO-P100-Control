"""Script entry: `python src/tapo.py USERNAME PASSWORD IP on|off` (also the PyInstaller target)."""

import sys

from tapo_control.cli import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
