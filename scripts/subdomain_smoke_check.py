#!/usr/bin/env python3
"""Verificações HTTP básicas nos subdomínios Cara Core (saída PASS/FAIL)."""
from __future__ import annotations

import argparse
import re
import ssl
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse


@dataclass
class PageResult:
    ok: bool
    status: Any
    final_url: str | None
    html: str | None
    error: str | None = None


def fetch(url: str, timeout: int) -> PageResult:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "caracore-tools-smoke/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return PageResult(True, resp.getcode(), resp.geturl(), body, None)
    except urllib.error.HTTPError as e:
        return PageResult(False, e.code, getattr(e, "url", None) or url, e.read().decode("utf-8", errors="replace") if e.fp else None, str(e))
    except Exception as e:  # noqa: BLE001
        return PageResult(False, "ERR", None, None, str(e))


def first_group(text: str | None, pattern: str) -> str | None:
    if not text:
        return None
    m = re.search(pattern, text, re.I)
    if m and m.lastindex:
        return m.group(1)
    return None


def add_store_checks(target: list[dict], name: str, host: str, has_download: bool, has_base: bool) -> None:
    root = f"https://{host}/"
    if has_base:
        target.append({"name": f"{name} root base host", "type": "base-host", "url": root, "expected_host": host})
    if has_download:
        du = f"https://{host}/download.html"
        target.append({"name": f"{name} download 200", "type": "status", "url": du, "expected_status": 200})
        if has_base:
            target.append({"name": f"{name} download base host", "type": "base-host", "url": du, "expected_host": host})
    fu = f"https://{host}/canal-feedback.html"
    target.append({"name": f"{name} feedback 200", "type": "status", "url": fu, "expected_status": 200})
    if has_base:
        target.append({"name": f"{name} feedback base host", "type": "base-host", "url": fu, "expected_host": host})
    wu = f"https://{host}/wiki/index.html"
    target.append({"name": f"{name} wiki 200", "type": "status", "url": wu, "expected_status": 200})
    target.append(
        {
            "name": f"{name} wiki links canonical wiki",
            "type": "contains",
            "url": wu,
            "expected_needle": "https://wiki.caracore.com.br/index.html",
        }
    )


def build_checks() -> list[dict]:
    checks: list[dict] = [
        {"name": "matrix root 200", "type": "status", "url": "https://www.caracore.com.br/", "expected_status": 200},
        {"name": "tools root 200", "type": "status", "url": "https://tools.caracore.com.br/", "expected_status": 200},
        {"name": "retro root 200", "type": "status", "url": "https://retro.caracore.com.br/", "expected_status": 200},
        {"name": "personal root 200", "type": "status", "url": "https://personal.caracore.com.br/", "expected_status": 200},
        {"name": "wiki root 200", "type": "status", "url": "https://wiki.caracore.com.br/", "expected_status": 200},
        {"name": "pdv root 200", "type": "status", "url": "https://pdv.caracore.com.br/", "expected_status": 200},
        {"name": "cso root 200", "type": "status", "url": "https://cso.caracore.com.br/", "expected_status": 200},
        {"name": "hub root 200", "type": "status", "url": "https://hub.caracore.com.br/", "expected_status": 200},
        {"name": "seed root 200", "type": "status", "url": "https://seed.caracore.com.br/", "expected_status": 200},
        {"name": "oidc root 200", "type": "status", "url": "https://oidc.caracore.com.br/", "expected_status": 200},
        {"name": "area51 root 200", "type": "status", "url": "https://area51.caracore.com.br/", "expected_status": 200},
        {"name": "ru root 200", "type": "status", "url": "https://ru.caracore.com.br/", "expected_status": 200},
        {"name": "ete root 200", "type": "status", "url": "https://ete.caracore.com.br/", "expected_status": 200},
        {"name": "circuito root 200", "type": "status", "url": "https://circuito.caracore.com.br/", "expected_status": 200},
        {"name": "ink root 200", "type": "status", "url": "https://ink.caracore.com.br/", "expected_status": 200},
        {"name": "mkt root 200", "type": "status", "url": "https://mkt.caracore.com.br/", "expected_status": 200},
        {
            "name": "retro articles redirect",
            "type": "redirect",
            "url": "https://retro.caracore.com.br/articles.html",
            "expected_prefix": "https://retro.caracore.com.br/",
        },
        {
            "name": "personal articles redirect",
            "type": "redirect",
            "url": "https://personal.caracore.com.br/articles.html",
            "expected_prefix": "https://personal.caracore.com.br/",
        },
        {
            "name": "retro article canonical/og host",
            "type": "meta-host",
            "url": "https://retro.caracore.com.br/articles/2026_04_04_article_79.html",
            "expected_host": "retro.caracore.com.br",
        },
        {
            "name": "personal article canonical/og host",
            "type": "meta-host",
            "url": "https://personal.caracore.com.br/articles/2026_04_03_alem_da_lente_os_limites_da_automacao_visual.html",
            "expected_host": "personal.caracore.com.br",
        },
        {
            "name": "wiki root og:url host",
            "type": "meta-host-og-only",
            "url": "https://wiki.caracore.com.br/",
            "expected_host": "wiki.caracore.com.br",
        },
    ]
    add_store_checks(checks, "pdv", "pdv.caracore.com.br", True, True)
    add_store_checks(checks, "cso", "cso.caracore.com.br", True, True)
    add_store_checks(checks, "hub", "hub.caracore.com.br", True, True)
    add_store_checks(checks, "seed", "seed.caracore.com.br", True, True)
    add_store_checks(checks, "oidc", "oidc.caracore.com.br", True, True)
    add_store_checks(checks, "area51", "area51.caracore.com.br", True, True)
    add_store_checks(checks, "ru", "ru.caracore.com.br", True, True)
    add_store_checks(checks, "ete", "ete.caracore.com.br", True, True)
    add_store_checks(checks, "circuito", "circuito.caracore.com.br", True, True)
    add_store_checks(checks, "ink", "ink.caracore.com.br", True, True)
    add_store_checks(checks, "mkt", "mkt.caracore.com.br", False, False)
    return checks


def evaluate(check: dict, page: PageResult) -> tuple[bool, str]:
    t = check["type"]
    if t == "status":
        ok = page.status == check["expected_status"]
        return ok, f"expected={check['expected_status']}; got={page.status}"
    if t == "redirect":
        html = page.html or ""
        meta = first_group(
            html,
            r'<meta[^>]+http-equiv=["\']refresh["\'][^>]+content=["\'][^"\']*url\s*=\s*([^"\']+)["\']',
        )
        http_ok = page.final_url and page.final_url != check["url"] and page.final_url.startswith(check["expected_prefix"])
        meta_ok = bool(meta) and (meta.startswith("/") or meta.startswith(check["expected_prefix"]))
        ok = page.status == 200 and (http_ok or meta_ok)
        return ok, f"prefix={check['expected_prefix']}; final={page.final_url}; meta={meta}; status={page.status}"
    if t == "meta-host":
        html = page.html or ""
        canon = first_group(html, r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']')
        og = first_group(html, r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']')
        ch = urlparse(canon).hostname if canon else None
        oh = urlparse(og).hostname if og else None
        exp = check["expected_host"]
        ok = ch == exp and oh == exp
        return ok, f"expected={exp}; canonical-host={ch}; og-host={oh}"
    if t == "meta-host-og-only":
        html = page.html or ""
        og = first_group(html, r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']')
        oh = urlparse(og).hostname if og else None
        exp = check["expected_host"]
        ok = oh == exp
        return ok, f"expected={exp}; og-host={oh}"
    if t == "base-host":
        html = page.html or ""
        bh = first_group(html, r'<base[^>]+href=["\']([^"\']+)["\']')
        h = urlparse(bh).hostname if bh else None
        exp = check["expected_host"]
        ok = h == exp
        return ok, f"expected={exp}; base-host={h}"
    if t == "contains":
        ok = bool(page.html) and check["expected_needle"] in page.html
        return ok, f"needle={check['expected_needle']}"
    raise ValueError(f"tipo desconhecido: {t}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--timeout", type=int, default=20)
    args = p.parse_args()

    checks = build_checks()
    cache: dict[str, PageResult] = {}
    report: list[tuple[str, str, str, Any, str | None, str]] = []

    for ch in checks:
        url = ch["url"]
        if url not in cache:
            cache[url] = fetch(url, args.timeout)
        page = cache[url]
        ok, detail = evaluate(ch, page)
        if not ok and page.error:
            detail = f"{detail}; error={page.error}"
        report.append(("PASS" if ok else "FAIL", ch["name"], url, page.status, page.final_url, detail))

    for result, name, url, status, final, detail in sorted(report, key=lambda x: (x[0], x[1])):
        print(f"{result:4}  {name:45}  {status!s:>5}  {detail[:120]}")

    total = len(report)
    passed = sum(1 for r, *_ in report if r == "PASS")
    failed = total - passed
    print(f"\nResumo: total={total}; pass={passed}; fail={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
