#!/usr/bin/env python3
"""
Governança do ecossistema: painel, roadmap, gate e relatório (Markdown).

  python scripts/ecosystem_governance.py dashboard
  python scripts/ecosystem_governance.py roadmap [--window-days 120]
  python scripts/ecosystem_governance.py gate --app pdv [--strict]
  python scripts/ecosystem_governance.py report --app pdv [--strict]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path


def scripts_dir() -> Path:
    return Path(__file__).resolve().parent


def repo_root() -> Path:
    return scripts_dir().parent


def load_json(name: str) -> list[dict]:
    return json.loads((scripts_dir() / name).read_text(encoding="utf-8"))


def delivery_by_app(app: str) -> dict | None:
    for d in load_json("ecosystem-delivery-map.json"):
        if str(d.get("app", "")).lower() == app.lower():
            return d
    return None


def token_status(delivery: dict | None) -> str:
    if not delivery:
        return "n/a"
    tokens = delivery.get("requiredTokens") or []
    if not tokens:
        return "n/a"
    for name in tokens:
        if os.environ.get(name):
            return f"ok:{name}"
    return "missing"


def git_repo_state(path: str) -> dict:
    p = Path(path)
    if not p.is_dir():
        return {"exists": False, "is_git": False, "dirty": None, "branch": "", "path": path}
    if not (p / ".git").exists():
        return {"exists": True, "is_git": False, "dirty": None, "branch": "", "path": path}
    br = subprocess.run(
        ["git", "-C", str(p), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
    )
    branch = (br.stdout or "").strip() if br.returncode == 0 else ""
    st = subprocess.run(
        ["git", "-C", str(p), "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    dirty = len([x for x in (st.stdout or "").splitlines() if x.strip()]) if st.returncode == 0 else 0
    return {"exists": True, "is_git": True, "dirty": dirty, "branch": branch, "path": path}


def find_git_root(start: Path) -> Path | None:
    cur = start.resolve()
    if start.is_file():
        cur = start.parent
    while cur:
        if (cur / ".git").exists():
            return cur
        parent = cur.parent
        if parent == cur:
            break
        cur = parent
    return None


def forbidden_matrix_changes(item: dict) -> list[str]:
    if not item.get("forbidBinaryDeliveryInMatrix") or not item.get("matrixForbiddenPaths"):
        return []
    base = Path(item["matrixDeliveryPath"])
    git_root = find_git_root(base)
    if not git_root:
        return []
    out: list[str] = []
    for rel in item["matrixForbiddenPaths"]:
        rel_norm = rel.replace("/", os.sep)
        st = subprocess.run(
            ["git", "-C", str(git_root), "status", "--porcelain", "--", rel_norm],
            capture_output=True,
            text=True,
        )
        if st.returncode == 0 and (st.stdout or "").strip():
            out.append(rel)
    return out


def app_snapshot(item: dict, today: date) -> dict:
    delivery = delivery_by_app(item["app"])
    tok = token_status(delivery)
    rd = (item.get("roadmapDate") or "").strip()
    days_to = None
    roadmap_date = None
    if rd:
        try:
            roadmap_date = datetime.strptime(rd, "%Y-%m-%d").date()
            days_to = (roadmap_date - today).days
        except ValueError:
            pass

    src = git_repo_state(item["sourceRepoPath"])
    rel = git_repo_state(item["releaseRepoPath"])
    matrix_exists = Path(item["matrixDeliveryPath"]).exists()
    release_docs = Path(item["releaseRepoPath"]) / item.get("releaseDocsPath", "docs")
    release_docs_exists = release_docs.is_dir()
    forbidden = forbidden_matrix_changes(item)
    release_leaf = Path(item["releaseRepoPath"]).name
    dedicated = release_leaf.endswith("-releases")

    cmd_exists = False
    if delivery and delivery.get("commandPath") and delivery.get("repoPath"):
        cmd_exists = (Path(delivery["repoPath"]) / delivery["commandPath"]).is_file()

    return {
        "app": item.get("app"),
        "displayName": item.get("displayName"),
        "category": item.get("category"),
        "roadmapStatus": item.get("roadmapStatus"),
        "roadmapDate": item.get("roadmapDate"),
        "daysToRoadmap": days_to,
        "commandExists": cmd_exists,
        "token": tok,
        "matrixExists": matrix_exists,
        "releaseDocsExists": release_docs_exists,
        "releaseRepoLeaf": release_leaf,
        "usesDedicatedReleasesRepo": dedicated,
        "releaseChannelPolicy": item.get("releaseChannelPolicy"),
        "forbiddenMatrixChanges": forbidden,
        "officialReleaseRepo": item.get("officialReleaseRepo"),
        "sourceDirty": src.get("dirty") or 0,
        "releaseDirty": rel.get("dirty") or 0,
        "sourceBranch": src.get("branch") or "",
        "releaseBranch": rel.get("branch") or "",
    }


def build_gate(snap: dict) -> dict:
    checks: list[dict] = []
    checks.append(
        {
            "name": "Segurança",
            "status": "BLOQUEADO" if snap["token"] == "missing" else "APROVADO",
            "detail": (
                "Token de delivery ausente para comando configurado."
                if snap["token"] == "missing"
                else "Token disponível ou não aplicável."
            ),
            "critical": True,
        }
    )
    ok_paths = snap["matrixExists"] and snap["releaseDocsExists"]
    checks.append(
        {
            "name": "Consistência Delivery-Matriz-Loja",
            "status": "APROVADO" if ok_paths else "BLOQUEADO",
            "detail": "Paths de matriz e docs da loja encontrados."
            if ok_paths
            else "Path ausente em matriz ou docs da loja.",
            "critical": True,
        }
    )
    checks.append(
        {
            "name": "Automação",
            "status": "APROVADO" if snap["commandExists"] else "BLOQUEADO",
            "detail": "Comando de delivery encontrado no ecossistema."
            if snap["commandExists"]
            else "Comando de delivery não encontrado.",
            "critical": True,
        }
    )
    checks.append(
        {
            "name": "Canal oficial de release",
            "status": "APROVADO" if snap["usesDedicatedReleasesRepo"] else "BLOQUEADO",
            "detail": f"Repositório dedicado: {snap['releaseRepoLeaf']}"
            if snap["usesDedicatedReleasesRepo"]
            else f"Repositório fora do padrão *-releases: {snap['releaseRepoLeaf']}",
            "critical": True,
        }
    )
    fb = snap["forbiddenMatrixChanges"] or []
    checks.append(
        {
            "name": "Política de artefato na matriz",
            "status": "BLOQUEADO" if fb else "APROVADO",
            "detail": (
                "Arquivos de artefato alterados na matriz: "
                + ", ".join(fb)
                + ". Publique binários apenas na loja oficial: "
                + str(snap.get("officialReleaseRepo") or "")
                if fb
                else "Matriz sem alterações de artefatos proibidos para este app."
            ),
            "critical": True,
        }
    )
    dirty_ok = (snap["sourceDirty"] == 0) and (snap["releaseDirty"] == 0)
    checks.append(
        {
            "name": "Integridade Git",
            "status": "APROVADO" if dirty_ok else "APROVADO COM RESSALVAS",
            "detail": "Repositórios fonte e release limpos."
            if dirty_ok
            else "Alterações locais detectadas em fonte ou release.",
            "critical": False,
        }
    )

    crit_fail = sum(1 for c in checks if c["critical"] and c["status"] == "BLOQUEADO")
    warn = sum(1 for c in checks if not c["critical"] and c["status"] != "APROVADO")
    overall = "APROVADO"
    if crit_fail > 0:
        overall = "BLOQUEADO"
    elif warn > 0:
        overall = "APROVADO COM RESSALVAS"

    return {"app": snap["app"], "displayName": snap["displayName"], "overall": overall, "checks": checks, "snapshot": snap}


def write_gate_md(gate: dict) -> Path:
    out_dir = repo_root() / "reports" / "governance"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = out_dir / f"GATE_{gate['app']}_{ts}.md"
    snap = gate["snapshot"]
    lines = [
        f"# Gate de governança — {gate['displayName']}",
        "",
        f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Status final: **{gate['overall']}**",
        "",
        "## Snapshot",
        f"- App: {snap['app']}",
        f"- Roadmap status: {snap['roadmapStatus']}",
        f"- Roadmap date: {snap['roadmapDate']}",
        f"- Token: {snap['token']}",
        f"- Command exists: {snap['commandExists']}",
        f"- Matrix exists: {snap['matrixExists']}",
        f"- Release docs exists: {snap['releaseDocsExists']}",
        f"- Release channel policy: {snap['releaseChannelPolicy']}",
        f"- Release repo leaf: {snap['releaseRepoLeaf']}",
        f"- Uses dedicated -releases repo: {snap['usesDedicatedReleasesRepo']}",
        "- Forbidden matrix changes: " + (", ".join(snap["forbiddenMatrixChanges"]) if snap["forbiddenMatrixChanges"] else "none"),
    ]
    if snap.get("officialReleaseRepo"):
        lines.append(f"- Official release repo: {snap['officialReleaseRepo']}")
    lines += [
        f"- Source dirty files: {snap['sourceDirty']}",
        f"- Release dirty files: {snap['releaseDirty']}",
        "",
        "## Checks",
    ]
    for c in gate["checks"]:
        lines.append(f"- {c['name']}: {c['status']} — {c['detail']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("dashboard")
    rp = sub.add_parser("roadmap")
    rp.add_argument("--window-days", type=int, default=120)
    gp = sub.add_parser("gate")
    gp.add_argument("--app", required=True)
    gp.add_argument("--strict", action="store_true")
    rep = sub.add_parser("report")
    rep.add_argument("--app", required=True)
    rep.add_argument("--strict", action="store_true")

    args = p.parse_args()
    catalog = load_json("ecosystem-governance-catalog.json")
    today = date.today()

    if args.cmd == "dashboard":
        snaps = [app_snapshot(it, today) for it in catalog]
        snaps.sort(key=lambda s: (99999 if s["daysToRoadmap"] is None else s["daysToRoadmap"], s["app"]))
        for s in snaps:
            print(
                f"{s['app']:10}  {str(s['roadmapStatus']):14}  {str(s['roadmapDate']):12}  "
                f"{str(s['daysToRoadmap']):>5}  tok={s['token']:12}  cmd={s['commandExists']}  "
                f"mat={s['matrixExists']}  docs={s['releaseDocsExists']}  "
                f"sd={s['sourceDirty']} rd={s['releaseDirty']}"
            )
        return 0

    if args.cmd == "roadmap":
        snaps = [app_snapshot(it, today) for it in catalog]
        win = [s for s in snaps if s["roadmapDate"] and s["daysToRoadmap"] is not None and s["daysToRoadmap"] <= args.window_days]
        if not win:
            print(f"Nenhum marco de roadmap nos próximos {args.window_days} dias.")
            return 0
        win.sort(key=lambda s: s["daysToRoadmap"] or 99999)
        for s in win:
            print(
                f"{s['app']:10}  {str(s['displayName'])[:32]:32}  {str(s['roadmapStatus']):14}  "
                f"{s['roadmapDate']}  ({s['daysToRoadmap']} dias)"
            )
        return 0

    if args.cmd in ("gate", "report"):
        snap = next((app_snapshot(it, today) for it in catalog if str(it.get("app", "")).lower() == args.app.lower()), None)
        if not snap:
            print(f"App '{args.app}' não encontrada no catálogo.", file=sys.stderr)
            return 2
        gate = build_gate(snap)
        for c in gate["checks"]:
            print(f"{c['name']:40}  {c['status']:22}  {c['detail']}")
        print(f"\nStatus final: {gate['overall']}")
        if args.cmd == "report":
            fpath = write_gate_md(gate)
            print(f"Relatório gerado: {fpath}")
        if args.strict and gate["overall"] != "APROVADO":
            print("Gate em modo estrito bloqueou a publicação.", file=sys.stderr)
            return 1
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
