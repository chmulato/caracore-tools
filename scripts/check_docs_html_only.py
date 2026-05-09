#!/usr/bin/env python3
"""
Auditoria HTML-only: lista ficheiros em docs/ fora das extensões permitidas.
Uso: python scripts/check_docs_html_only.py [--docs-path CAMINHO] [--report-only]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ALLOWED_EXTENSIONS = frozenset({
    ".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico",
    ".avif", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".map",
})
ALLOWED_NAMES = frozenset({"CNAME", ".gitkeep", "feed.xml"})


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser(description="Auditoria HTML-only em docs/")
    p.add_argument(
        "--docs-path",
        type=Path,
        default=root / "docs",
        help="Pasta a auditar (predefinição: <raiz>/docs)",
    )
    p.add_argument(
        "--report-only",
        action="store_true",
        help="Só reporta violações; não falha com código de saída 1",
    )
    args = p.parse_args()
    docs_path: Path = args.docs_path.resolve()
    if not docs_path.is_dir():
        print(f"ERRO: pasta não encontrada: {docs_path}", file=sys.stderr)
        return 2

    files = [f for f in docs_path.rglob("*") if f.is_file()]
    violations: list[Path] = []
    for f in files:
        name = f.name
        ext = f.suffix.lower()
        if name in ALLOWED_NAMES:
            continue
        if ext in ALLOWED_EXTENSIONS:
            continue
        violations.append(f)

    print(f"DOCS_PATH={docs_path}")
    print(f"FILES_TOTAL={len(files)}")
    print(f"VIOLATIONS_TOTAL={len(violations)}")

    if violations:
        print()
        by_ext: dict[str, int] = {}
        for v in violations:
            key = "[sem-extensão]" if not v.suffix else v.suffix.lower()
            by_ext[key] = by_ext.get(key, 0) + 1
        print("Violações por extensão:")
        for ext, n in sorted(by_ext.items(), key=lambda x: (-x[1], x[0])):
            print(f"  {n:4}  {ext}")
        print()
        by_dir: dict[str, int] = {}
        for v in violations:
            d = str(v.parent)
            by_dir[d] = by_dir.get(d, 0) + 1
        print("Diretórios com mais violações:")
        for d, n in sorted(by_dir.items(), key=lambda x: (-x[1], x[0]))[:15]:
            print(f"  {n:4}  {d}")
        print()
        print("Ficheiros bloqueados:")
        for v in sorted(violations, key=lambda x: str(x)):
            print(f"  - {v}")
        if not args.report_only:
            print("\nDocs contêm artefactos publicados fora do padrão HTML-only.", file=sys.stderr)
            return 1
    print()
    print("Auditoria concluída.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
