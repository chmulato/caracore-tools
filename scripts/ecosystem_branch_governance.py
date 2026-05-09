#!/usr/bin/env python3
"""
Alinhamento de branches (ecosystem-governance-catalog.json).

  python scripts/ecosystem_branch_governance.py status [--app ID]
  python scripts/ecosystem_branch_governance.py align [--app ID] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def scripts_dir() -> Path:
    return Path(__file__).resolve().parent


def load_catalog() -> list[dict]:
    p = scripts_dir() / "ecosystem-governance-catalog.json"
    return json.loads(p.read_text(encoding="utf-8"))


def git_branch(repo: Path) -> tuple[bool, str, int | None]:
    if not repo.is_dir():
        return False, "", None
    if not (repo / ".git").is_dir():
        return True, "", None
    r = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
    )
    branch = (r.stdout or "").strip() if r.returncode == 0 else ""
    r2 = subprocess.run(
        ["git", "-C", str(repo), "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    dirty = len([ln for ln in (r2.stdout or "").splitlines() if ln.strip()]) if r2.returncode == 0 else None
    return True, branch, dirty


def row(item: dict) -> dict:
    src_ok, src_b, src_d = git_branch(Path(item["sourceRepoPath"]))
    rel_ok, rel_b, rel_d = git_branch(Path(item["releaseRepoPath"]))
    src_t = item.get("sourceBranchTarget") or src_b
    rel_t = item.get("releaseBranchTarget") or rel_b
    return {
        "app": item.get("app"),
        "sourceBranch": src_b,
        "sourceTarget": src_t,
        "sourceDirty": src_d,
        "sourceAligned": src_b == src_t,
        "releaseBranch": rel_b,
        "releaseTarget": rel_t,
        "releaseDirty": rel_d,
        "releaseAligned": rel_b == rel_t,
    }


def print_table(rows: list[dict]) -> None:
    for rw in rows:
        print(
            f"{rw['app']:10}  src {rw['sourceBranch']!s:12} -> {rw['sourceTarget']!s:12}  "
            f"ok={rw['sourceAligned']} dirty={rw['sourceDirty']}  |  "
            f"rel {rw['releaseBranch']!s:12} -> {rw['releaseTarget']!s:12}  "
            f"ok={rw['releaseAligned']} dirty={rw['releaseDirty']}"
        )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["status", "align"])
    p.add_argument("--app", help="Filtrar por app")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    catalog = load_catalog()
    if args.app:
        catalog = [x for x in catalog if str(x.get("app", "")).lower() == args.app.lower()]
        if not catalog:
            print(f"App '{args.app}' não encontrada no catálogo.", file=sys.stderr)
            return 2

    rows = [row(it) for it in catalog]

    if args.action == "status":
        print_table(rows)
        return 0

    for it in catalog:
        src_p = Path(it["sourceRepoPath"])
        rel_p = Path(it["releaseRepoPath"])
        _, src_b, src_d = git_branch(src_p)
        _, rel_b, rel_d = git_branch(rel_p)
        src_t = it.get("sourceBranchTarget") or src_b
        rel_t = it.get("releaseBranchTarget") or rel_b

        if src_b and src_b != src_t:
            if src_d and src_d > 0:
                print(f"[{it.get('app')}] source sujo ({src_p}); não altero branch.")
            else:
                print(f"[{it.get('app')}] source: {src_b} -> {src_t}")
                if not args.dry_run:
                    subprocess.run(["git", "-C", str(src_p), "checkout", src_t], check=False)

        if rel_b and rel_b != rel_t:
            if rel_d and rel_d > 0:
                print(f"[{it.get('app')}] release sujo ({rel_p}); não altero branch.")
            else:
                print(f"[{it.get('app')}] release: {rel_b} -> {rel_t}")
                if not args.dry_run:
                    subprocess.run(["git", "-C", str(rel_p), "checkout", rel_t], check=False)

    print("\nEstado após alinhamento:")
    print_table([row(it) for it in catalog])
    return 0


if __name__ == "__main__":
    sys.exit(main())
