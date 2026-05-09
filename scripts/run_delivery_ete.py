#!/usr/bin/env python3
"""Invoca o script de delivery do Minerador 4.0 (repo caracore-ete)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_SCRIPT = Path(r"D:\dev\caracore-ete\scripts\script_delivery_minerador_to_ETE_Releases_Releases.py")


def main() -> int:
    if not _SCRIPT.is_file():
        print(f"Script não encontrado: {_SCRIPT}", file=sys.stderr)
        return 2
    args = [sys.executable, str(_SCRIPT)]
    i = 1
    while i < len(sys.argv):
        args.append(sys.argv[i])
        i += 1
    return subprocess.call(args)


if __name__ == "__main__":
    raise SystemExit(main())
