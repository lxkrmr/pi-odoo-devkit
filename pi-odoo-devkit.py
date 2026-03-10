#!/usr/bin/env python3
"""Compatibility wrapper for renamed CLI.

Use: ./pi-odoo-skill-manager.py
"""

from pathlib import Path
import runpy
import sys

TARGET = Path(__file__).resolve().parent / "pi-odoo-skill-manager.py"

if __name__ == "__main__":
    print("Warning: pi-odoo-devkit.py is deprecated. Use ./pi-odoo-skill-manager.py", file=sys.stderr)
    runpy.run_path(str(TARGET), run_name="__main__")
