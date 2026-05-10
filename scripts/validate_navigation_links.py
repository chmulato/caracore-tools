#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path


IGNORE_TEMPLATE_MARKER = "template-placeholders"
DEFAULT_USER_AGENT = "caracore-tools-navigation-validator/1.0"


@dataclass(frozen=True)
class LinkRef:
    href: str
    text: str
    line: int


@dataclass
class HtmlPage:
    path: Path
    links: list[LinkRef] = field(default_factory=list)
    ids: set[str] = field(default_factory=set)
    ignore_validation: bool = False


@dataclass
class ValidationIssue:
    kind: str
    file: Path
    href: str
    detail: str
    line: int


class NavigationHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[LinkRef] = []
        self.ids: set[str] = set()
        self.ignore_validation = False
        self._anchor_stack: list[dict[str, object]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        identifier = attr_map.get("id")
        if identifier:
            self.ids.add(identifier)

        if tag == "meta" and attr_map.get("name") == "caracore-audit":
            content = (attr_map.get("content") or "").lower()
            if IGNORE_TEMPLATE_MARKER in content:
                self.ignore_validation = True

        if tag == "a":
            href = attr_map.get("href")
            if href:
                self._anchor_stack.append({"href": href, "line": self.getpos()[0], "text": []})

    def handle_data(self, data: str) -> None:
        if self._anchor_stack:
            self._anchor_stack[-1]["text"].append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._anchor_stack:
            anchor = self._anchor_stack.pop()
            text = " ".join("".join(anchor["text"]).split())
            self.links.append(LinkRef(href=str(anchor["href"]), text=text, line=int(anchor["line"])))


def parse_page(path: Path) -> HtmlPage:
    parser = NavigationHtmlParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return HtmlPage(path=path, links=parser.links, ids=parser.ids, ignore_validation=parser.ignore_validation)


def is_external_http(href: str) -> bool:
    return href.startswith("https://") or href.startswith("http://")


def is_ignorable(href: str) -> bool:
    return href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:")


def normalize_local_target(source: Path, href: str) -> tuple[Path, str | None]:
    parsed = urllib.parse.urlsplit(href)
    fragment = parsed.fragment or None
    path_part = parsed.path
    if not path_part:
        return source, fragment
    if path_part.startswith("/"):
        raise ValueError("absolute local paths are not allowed in portal docs validation")
    target = (source.parent / urllib.parse.unquote(path_part)).resolve()
    return target, fragment


def collect_pages(docs_path: Path, include_templates: bool) -> dict[Path, HtmlPage]:
    pages: dict[Path, HtmlPage] = {}
    for html_path in sorted(docs_path.rglob("*.html")):
        page = parse_page(html_path)
        if page.ignore_validation and not include_templates:
            continue
        pages[html_path.resolve()] = page
    return pages


def validate_local_links(pages: dict[Path, HtmlPage]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    known_pages = set(pages.keys())
    extra_pages: dict[Path, HtmlPage] = {}

    for page in list(pages.values()):
        for link in page.links:
            href = link.href.strip()
            if is_ignorable(href) or is_external_http(href):
                continue
            try:
                target, fragment = normalize_local_target(page.path, href)
            except ValueError as exc:
                issues.append(ValidationIssue("local", page.path, href, str(exc), link.line))
                continue

            if not target.exists():
                issues.append(ValidationIssue("local", page.path, href, f"target not found: {target}", link.line))
                continue

            if target.suffix.lower() == ".html" and target.resolve() not in known_pages and target.is_file():
                parsed_target = parse_page(target)
                if not parsed_target.ignore_validation:
                    extra_pages[target.resolve()] = parsed_target
                    known_pages.add(target.resolve())

            if fragment:
                target_page = pages.get(target.resolve()) or extra_pages.get(target.resolve())
                if target_page and fragment not in target_page.ids:
                    issues.append(
                        ValidationIssue("fragment", page.path, href, f"fragment '#{fragment}' not found in {target.name}", link.line)
                    )

    pages.update(extra_pages)
    return issues


def fetch_external(url: str, timeout: int, user_agent: str) -> tuple[bool, str]:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    context = ssl.create_default_context()
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            status = getattr(response, "status", None) or response.getcode()
            final_url = response.geturl()
            if 200 <= status < 400:
                return True, f"status={status}; final={final_url}"
            return False, f"status={status}; final={final_url}"
    except urllib.error.HTTPError as exc:
        return False, f"status={exc.code}; error={exc.reason}"
    except Exception as exc:  # noqa: BLE001
        return False, f"error={exc}"


def validate_external_links(pages: dict[Path, HtmlPage], timeout: int, user_agent: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    cache: dict[str, tuple[bool, str]] = {}
    for page in pages.values():
        for link in page.links:
            href = link.href.strip()
            if not href.startswith("https://"):
                continue
            if href not in cache:
                cache[href] = fetch_external(href, timeout=timeout, user_agent=user_agent)
            ok, detail = cache[href]
            if not ok:
                issues.append(ValidationIssue("external", page.path, href, detail, link.line))
    return issues


def print_report(issues: list[ValidationIssue], docs_path: Path, checked_pages: int, external_checked: bool) -> None:
    print(f"DOCS_PATH={docs_path}")
    print(f"PAGES_CHECKED={checked_pages}")
    print(f"EXTERNAL_CHECKED={'yes' if external_checked else 'no'}")
    print(f"ISSUES_TOTAL={len(issues)}")
    if not issues:
        print("STATUS=PASS")
        return
    print("STATUS=FAIL")
    for issue in sorted(issues, key=lambda item: (str(item.file), item.line, item.href)):
        rel = issue.file.relative_to(docs_path)
        print(f"- [{issue.kind}] {rel}:{issue.line} -> {issue.href} :: {issue.detail}")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Valida links de navegação do portal tools.")
    parser.add_argument("--docs-path", type=Path, default=root / "docs", help="Pasta docs a validar.")
    parser.add_argument("--skip-external", action="store_true", help="Pula a checagem HTTP dos links https://.")
    parser.add_argument("--include-templates", action="store_true", help="Inclui templates marcados com placeholder na auditoria.")
    parser.add_argument("--external-timeout", type=int, default=15, help="Timeout por link externo em segundos.")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="User-Agent para a checagem HTTP externa.")
    args = parser.parse_args()

    docs_path = args.docs_path.resolve()
    if not docs_path.is_dir():
        print(f"ERRO: docs path não encontrado: {docs_path}", file=sys.stderr)
        return 2

    pages = collect_pages(docs_path, include_templates=args.include_templates)
    issues = validate_local_links(pages)
    if not args.skip_external:
        issues.extend(validate_external_links(pages, timeout=args.external_timeout, user_agent=args.user_agent))

    print_report(issues, docs_path=docs_path, checked_pages=len(pages), external_checked=not args.skip_external)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
