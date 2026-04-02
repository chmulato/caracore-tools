#!/usr/bin/env python3
"""
Desbloqueia domínios de telemetria Microsoft / VS Code / Cursor no arquivo hosts do Windows.
Remove as entradas de bloqueio para reabilitar a telemetria.
Soberania do Código — Cara Core Informática.

Uso: Executar como Administrador (ex.: python unblock-telemetry-hosts.py).
      Opção --dry-run ou -n: simula sem escrever e sem exigir admin (para testar).
Depois: ipconfig /flushdns
"""

import os
import re
import sys

HOSTS_PATH = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32", "drivers", "etc", "hosts")
MARKER_START = "# BLOCK TELEMETRIA - INICIO (Cara Core Black-Box)"
MARKER_END = "# BLOCK TELEMETRIA - FIM"


def is_admin() -> bool:
    """Retorna True se o processo está rodando com privilégios de administrador (Windows)."""
    if sys.platform != "win32":
        return os.geteuid() == 0
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def main() -> None:
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    if not dry_run and not is_admin():
        print("ERRO: Execute como Administrador (clique direito no terminal -> Executar como administrador).", file=sys.stderr)
        sys.exit(1)

    try:
        with open(HOSTS_PATH, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except OSError as e:
        print(f"ERRO ao ler {HOSTS_PATH}: {e}", file=sys.stderr)
        sys.exit(1)

    if MARKER_START in content:
        # Remove o bloco de bloqueio
        new_content = re.sub(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END) + r"\r?\n?",
            "",
            content,
            flags=re.DOTALL,
        )
        new_content = new_content.rstrip() + "\n"
    else:
        print("Nenhum bloco de bloqueio encontrado. Telemetria já está habilitada.")
        return

    if dry_run:
        print("[DRY-RUN] O bloco de bloqueio seria removido de {HOSTS_PATH}.")
        print("[DRY-RUN] Simulação concluída. Para aplicar, execute como Administrador sem --dry-run.")
        return

    try:
        with open(HOSTS_PATH, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)
    except OSError as e:
        print(f"ERRO ao escrever {HOSTS_PATH}: {e}", file=sys.stderr)
        sys.exit(1)

    print("Hosts atualizado. Entradas de telemetria removidas (telemetria reabilitada).")
    print("Execute: ipconfig /flushdns")


if __name__ == "__main__":
    main()