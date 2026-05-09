#!/usr/bin/env python3
"""
Copia conteúdo de delivery/<app> para <releases>/docs, git add/commit/push.
Uso: python scripts/sync_delivery_site_to_releases_docs.py --delivery ... --releases-repo ... [--message ...] [--dry-run] [--no-push]
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run_git(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        check=check,
        text=True,
        capture_output=False,
    )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--delivery", type=Path, required=True, help="Pasta fonte (ex.: .../delivery/ink)")
    p.add_argument("--releases-repo", type=Path, required=True, help="Raiz do repo *-releases com pasta docs/")
    p.add_argument("--message", default="", help="Mensagem de commit")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--no-push", action="store_true")
    args = p.parse_args()

    delivery = args.delivery.resolve()
    releases = args.releases_repo.resolve()
    docs = releases / "docs"

    if not (releases / ".git").exists():
        print(f"ERRO: repositório sem .git: {releases}", file=sys.stderr)
        return 2
    if not delivery.exists():
        print(f"ERRO: pasta de delivery não encontrada: {delivery}", file=sys.stderr)
        return 2

    leaf = delivery.name
    message = args.message.strip() or f"site: sync delivery/{leaf} para docs/"

    docs.mkdir(parents=True, exist_ok=True)

    print(f"Fonte: {delivery}")
    print(f"Destino: {docs}")
    print(f"Dry-run: {args.dry_run}")

    for entry in delivery.iterdir():
        if entry.name == ".git":
            continue
        dest = docs / entry.name
        if args.dry_run:
            print(f"[dry-run] Copiar {entry} -> {dest}")
            continue
        if entry.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(entry, dest)
        else:
            shutil.copy2(entry, dest)

    if args.dry_run:
        run_git(["status", "--short"], cwd=releases, check=False)
        return 0

    run_git(["add", "docs"], cwd=releases)
    st = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=str(releases),
        capture_output=True,
    )
    if st.returncode == 0:
        print(f"Nenhuma alteração para commit em {releases}")
        return 0

    run_git(["commit", "-m", message], cwd=releases)
    if args.no_push:
        print("Commit criado com --no-push.")
        return 0
    run_git(["push", "origin", "HEAD"], cwd=releases)
    print("Sync concluído e enviado para origin.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as e:
        print(f"Erro git: {e}", file=sys.stderr)
        sys.exit(e.returncode or 1)
