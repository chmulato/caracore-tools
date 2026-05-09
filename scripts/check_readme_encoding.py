#!/usr/bin/env python3
"""
Deteta marcas típicas de mojibake (UTF-8 lido como CP1252) em README.md de repos caracore-*.
Uso: python scripts/check_readme_encoding.py [--root CAMINHO] [--fix]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MOJIBAKE = re.compile(
    r"\u00C3[\u0080-\u00BF]|\u00C2[\u0080-\u00BF]|\u00E2[\u0080-\u00BF]{1,2}|\uFFFD"
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path(r"d:\dev"), help="Pasta que contém os repositórios")
    p.add_argument("--fix", action="store_true", help="Tenta corrigir reescrevendo em UTF-8")
    args = p.parse_args()
    root: Path = args.root
    if not root.is_dir():
        print(f"Pasta não encontrada: {root}", file=sys.stderr)
        return 2

    readmes: list[Path] = []
    own = root / "README.md"
    if own.is_file():
        readmes.append(own)
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        if not (child.name.startswith("caracore-") or child.name.startswith("circuito")):
            continue
        readme = child / "README.md"
        if readme.is_file() and readme not in readmes:
            readmes.append(readme)

    if not readmes:
        print("Nenhum README.md encontrado nos repositórios alvo.")
        return 0

    issues: list[tuple[Path, int, int, bool]] = []
    for path in readmes:
        raw = path.read_text(encoding="utf-8")
        before = len(MOJIBAKE.findall(raw))
        if before <= 0:
            continue
        try:
            fixed = raw.encode("cp1252").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            issues.append((path, before, before, False))
            continue
        after = len(MOJIBAKE.findall(fixed))
        changed = False
        if args.fix and after < before:
            path.write_text(fixed, encoding="utf-8", newline="\n")
            changed = True
        issues.append((path, before, after, changed))

    if not issues:
        print("Encoding: nenhum marcador suspeito encontrado.")
        return 0

    print("Possíveis problemas de codificação:")
    for path, b, a, ch in sorted(issues, key=lambda x: str(x[0])):
        print(f"  {path}  marcadores={b}->{a}  fix={'sim' if ch else 'não'}")

    if not args.fix:
        print(f"\nFalha: {len(issues)} ficheiro(s) com marcadores (use --fix para tentar corrigir).", file=sys.stderr)
        return 1
    if any(after > 0 for _, _, after, _ in issues):
        print(f"\nFalha: ainda há marcadores após --fix.", file=sys.stderr)
        return 1
    print("\nEncoding OK após correção.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
