#!/usr/bin/env python3
"""Sincroniza delivery/ink da matriz para caracore-ink-releases/docs."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_SYNC = Path(__file__).resolve().parent / "sync_delivery_site_to_releases_docs.py"


def main() -> int:
    dry = "--dry-run" in sys.argv
    no_push = "--no-push" in sys.argv
    cmd = [
        sys.executable,
        str(_SYNC),
        "--delivery",
        r"D:\dev\caracore-site\delivery\ink",
        "--releases-repo",
        r"D:\dev\caracore-ink-releases",
        "--message",
        "site: sync delivery/ink para docs/",
    ]
    if dry:
        cmd.append("--dry-run")
    if no_push:
        cmd.append("--no-push")
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
