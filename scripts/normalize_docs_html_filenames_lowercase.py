#!/usr/bin/env python3
"""
Renomeia ficheiros .html em docs/ para nomes em caixa baixa e atualiza referências
em ficheiros de texto do repositório. Idempotente: ignora ficheiros já normalizados.

Uso: python scripts/normalize_docs_html_filenames_lowercase.py [--dry-run]
"""
from __future__ import annotations

import argparse
import random
import string
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"

TEXT_SUFFIXES = frozenset({
    ".html", ".htm", ".js", ".css", ".md", ".json", ".yml", ".yaml",
    ".py", ".ps1", ".txt", ".svg", ".xml",
})


def collect_mappings() -> list[tuple[str, str, str, str]]:
    """Lista (old_rel, new_rel, old_base, new_base) relativos a docs/."""
    rows: list[tuple[str, str, str, str]] = []
    seen_lower_parent: dict[tuple[str, str], str] = {}
    for p in sorted(DOCS.rglob("*.html")):
        name = p.name
        low = name.lower()
        if name == low:
            continue
        rel = p.relative_to(DOCS)
        parent = str(rel.parent).replace("\\", "/")
        key = (parent, low)
        if key in seen_lower_parent:
            raise SystemExit(
                f"Colisão: {rel.as_posix()} e {seen_lower_parent[key]} → {low} na mesma pasta"
            )
        seen_lower_parent[key] = rel.as_posix()
        new_rel = (rel.parent / low).as_posix()
        rows.append((rel.as_posix(), new_rel, name, low))
    return rows


def win_safe_rename(path: Path, dest: Path) -> None:
    """No Windows, só mudar maiúsculas exige nome temporário intermédio."""
    same_inode = path.resolve() == dest.resolve()
    if same_inode:
        if path.name == dest.name:
            return
        tmp = path.parent / f".__lc_{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}.html"
        path.rename(tmp)
        tmp.rename(dest)
        return
    if dest.exists():
        raise FileExistsError(f"Destino já existe: {dest}")
    path.rename(dest)


def iter_text_files() -> list[Path]:
    out: list[Path] = []
    for base in (REPO / "docs", REPO / "scripts", REPO / "sources", REPO / ".github"):
        if not base.is_dir():
            continue
        for p in base.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() in TEXT_SUFFIXES:
                out.append(p)
    for name in ("README.md", "LICENSE"):
        p = REPO / name
        if p.is_file():
            out.append(p)
    return out


def apply_content_replacements(mappings: list[tuple[str, str, str, str]], dry: bool) -> int:
    # Ordenar pelo comprimento do basename antigo (desc) para evitar substituições parciais raras
    by_base = sorted(mappings, key=lambda m: len(m[2]), reverse=True)
    changed_files = 0
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        orig = text
        for old_rel, new_rel, old_base, new_base in by_base:
            old_bs = old_rel.replace("/", "\\")
            new_bs = new_rel.replace("/", "\\")
            text = text.replace(f"docs/{old_bs}", f"docs/{new_bs}")
            text = text.replace(f"docs/{old_rel}", f"docs/{new_rel}")
            text = text.replace(old_bs, new_bs)
            text = text.replace(old_rel, new_rel)
            text = text.replace(old_base, new_base)
        if text != orig:
            changed_files += 1
            if not dry:
                path.write_text(text, encoding="utf-8", newline="\n")
    return changed_files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not DOCS.is_dir():
        print(f"ERRO: {DOCS} não existe", file=sys.stderr)
        return 2

    mappings = collect_mappings()
    if not mappings:
        print("Nada a fazer: todos os .html em docs/ já têm nome em caixa baixa.")
        return 0

    print(f"Mapeamentos: {len(mappings)} ficheiros")
    for old_rel, new_rel, _, _ in mappings[:8]:
        print(f"  {old_rel} -> {new_rel}")
    if len(mappings) > 8:
        print(f"  ... e mais {len(mappings) - 8}")

    if not args.dry_run:
        for old_rel, new_rel, _, _ in mappings:
            src = DOCS / old_rel
            dst = DOCS / new_rel
            win_safe_rename(src, dst)

    n = apply_content_replacements(mappings, args.dry_run)
    print(f"Ficheiros de texto {'que seriam ' if args.dry_run else ''}atualizados: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
