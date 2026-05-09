#!/usr/bin/env python3
"""Invoca o script de delivery do WAR Hub."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_SCRIPT = Path(r"D:\dev\caracore-hub\scripts\delivery_war_hub_to_releases.py")


def main() -> int:
    if not _SCRIPT.is_file():
        print(f"Script não encontrado: {_SCRIPT}", file=sys.stderr)
        return 2
    args = [sys.executable, str(_SCRIPT), *sys.argv[1:]]
    return subprocess.call(args)


if __name__ == "__main__":
    raise SystemExit(main())
