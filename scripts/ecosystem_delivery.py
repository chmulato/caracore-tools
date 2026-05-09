#!/usr/bin/env python3
"""
Orquestra deliveries do ecossistema (ecosystem-delivery-map.json).

  python scripts/ecosystem_delivery.py list
  python scripts/ecosystem_delivery.py validate
  python scripts/ecosystem_delivery.py run --app ink-v2 [--dry-run] [-- args extras]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def scripts_dir() -> Path:
    return Path(__file__).resolve().parent


def load_items() -> list[dict]:
    p = scripts_dir() / "ecosystem-delivery-map.json"
    return json.loads(p.read_text(encoding="utf-8"))


def token_status(item: dict) -> str:
    tokens = item.get("requiredTokens") or []
    if not tokens:
        return "n/a"
    for name in tokens:
        if os.environ.get(name):
            return f"ok:{name}"
    return "missing"


def roadmap_sort_key(item: dict) -> tuple:
    d = (item.get("roadmapDate") or "").strip()
    if not d:
        return (datetime.max.date(), item.get("app", ""))
    try:
        dt = datetime.strptime(d, "%Y-%m-%d").date()
    except ValueError:
        return (datetime.max.date(), item.get("app", ""))
    return (dt, item.get("app", ""))


def cmd_list(items: list[dict]) -> None:
    rows = sorted(items, key=roadmap_sort_key)
    for it in rows:
        mode = "manual" if not (it.get("commandPath") or "").strip() else "auto"
        print(
            f"{it.get('app', ''):12}  {str(it.get('displayName', ''))[:28]:28}  "
            f"{str(it.get('category', ''))[:12]:12}  {str(it.get('roadmapStatus', ''))[:14]:14}  "
            f"{str(it.get('roadmapDate', '') or ''):12}  {mode:8}  {token_status(it)}"
        )
    print("\nDica: python scripts/ecosystem_delivery.py run --app <id> [--dry-run]")


def cmd_validate(items: list[dict]) -> int:
    code = 0
    for it in items:
        repo = Path(it.get("repoPath", ""))
        cmd_rel = it.get("commandPath") or ""
        cmd = (repo / cmd_rel) if cmd_rel else None
        exists_repo = repo.is_dir()
        exists_cmd = cmd.is_file() if cmd else False
        mode = "manual" if not cmd_rel else "auto"
        tok = token_status(it)
        print(
            f"{it.get('app')}: repo={'sim' if exists_repo else 'não'}  "
            f"cmd={'sim' if exists_cmd else 'não' if cmd_rel else 'n/a'}  mode={mode}  token={tok}"
        )
        if not exists_repo or (cmd_rel and not exists_cmd):
            code = 1
    return code


def cmd_run(item: dict, dry_run: bool, extra: list[str]) -> int:
    repo = Path(item["repoPath"])
    cmd_rel = item.get("commandPath") or ""
    if not cmd_rel:
        print("App em modo manual (sem comando).", file=sys.stderr)
        return 2
    if not repo.is_dir():
        print(f"Repositório não encontrado: {repo}", file=sys.stderr)
        return 2

    cmd_file = repo / cmd_rel
    if not cmd_file.is_file():
        print(f"Comando não encontrado: {cmd_file}", file=sys.stderr)
        return 2

    tok = token_status(item)
    if tok == "missing":
        print("Aviso: nenhum token do conjunto requerido encontrado.", file=sys.stderr)
        print("Tokens aceites:", ", ".join(item.get("requiredTokens") or []), file=sys.stderr)
        if not dry_run:
            print("Abortado (defina um token ou use --dry-run).", file=sys.stderr)
            return 1
        print("Dry-run sem token: simulação concluída sem invocar o comando.")
        return 0

    ctype = (item.get("commandType") or "python").lower()
    if ctype == "ps1":
        invocation: list[str] = ["powershell", "-NoProfile", "-File", str(cmd_file)]
    elif ctype == "python":
        invocation = [sys.executable, str(cmd_file)]
    else:
        print(f"Tipo de comando não suportado: {ctype}", file=sys.stderr)
        return 2

    args = list(extra)
    if dry_run and item.get("supportsDryRun"):
        da = (item.get("dryRunArg") or "").strip()
        if da and da not in args:
            if ctype == "python" and da in ("-DryRun", "-dry-run", "-Dryrun"):
                if "--dry-run" not in args:
                    args.append("--dry-run")
            else:
                args.append(da)

    print(f"App: {item.get('displayName')} [{item.get('app')}]")
    print(f"Repo: {repo}")
    print(f"Comando: {cmd_file}")
    print(f"Token: {tok}")
    print(f"Dry-run: {dry_run}")
    if args:
        print("Args:", " ".join(args))

    r = subprocess.run(invocation + args, cwd=str(repo))
    return int(r.returncode or 0)


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "Uso: python scripts/ecosystem_delivery.py list|calendar|validate|run --app ID [--dry-run]",
            file=sys.stderr,
        )
        return 2

    cmd = sys.argv[1].lower()
    items = load_items()

    if cmd in ("list", "calendar"):
        cmd_list(items)
        return 0
    if cmd == "validate":
        return cmd_validate(items)
    if cmd != "run":
        print(f"Ação desconhecida: {sys.argv[1]}", file=sys.stderr)
        return 2

    rest = sys.argv[2:]
    rp = argparse.ArgumentParser(add_help=False)
    rp.add_argument("--app", required=True)
    rp.add_argument("--dry-run", action="store_true")
    ns, extra = rp.parse_known_args(rest)
    if extra and extra[0] == "--":
        extra = extra[1:]

    hit = next((x for x in items if str(x.get("app", "")).lower() == ns.app.lower()), None)
    if not hit:
        print(f"App '{ns.app}' não encontrada no mapa.", file=sys.stderr)
        return 2
    return cmd_run(hit, ns.dry_run, extra)


if __name__ == "__main__":
    sys.exit(main())
