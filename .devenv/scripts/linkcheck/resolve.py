"""Classify links and resolve them to the URL that gets checked."""
from __future__ import annotations

import posixpath
from typing import Dict, Iterable, List
from urllib.parse import unquote, urljoin, urlsplit

from .models import EXTERNAL, INTERNAL, SKIPPED, UNRESOLVED, Link, ResolvedLink

PROD_HOST = "docs.operaton.org"
PROD_URL = "https://docs.operaton.org"
# Deployed next to the site, not part of the Docusaurus build: always checked on production.
PROD_ONLY_PREFIXES = ("/reference/",)
SKIP_PREFIXES = ("mailto:", "tel:", "javascript:", "data:")
DOC_SUFFIXES = (".md", ".mdx")
DOCS_DIR = "docs"


def _md_candidates(link_file: str, path: str) -> List[str]:
    """Source files a Markdown link may point to, in Docusaurus lookup order."""
    if path.startswith("/"):
        # Docusaurus tries the docs content dir first, then the site root.
        return [posixpath.normpath(DOCS_DIR + path), posixpath.normpath(path.lstrip("/"))]
    return [posixpath.normpath(posixpath.join(posixpath.dirname(link_file), path))]


def resolve_link(link: Link, routes: Dict[str, str], base_url: str) -> ResolvedLink:
    base = base_url.rstrip("/")
    raw = link.raw.strip()

    def made(kind: str, url: str = "", reason: str = "") -> ResolvedLink:
        return ResolvedLink(link, kind, url, reason)

    if not raw:
        return made(SKIPPED, reason="empty")
    if raw.lower().startswith(SKIP_PREFIXES):
        return made(SKIPPED, reason="scheme")
    parts = urlsplit(raw)
    if parts.scheme in ("http", "https"):
        if parts.hostname == PROD_HOST and not parts.path.startswith(PROD_ONLY_PREFIXES):
            rest = raw.split(PROD_HOST, 1)[1]
            return made(INTERNAL, base + (rest or "/"))
        return made(EXTERNAL, raw)
    if parts.scheme or raw.startswith("//"):
        return made(SKIPPED, reason="scheme")

    path, _, fragment = raw.partition("#")
    suffix = "#" + fragment if fragment else ""
    page = routes.get(link.file)

    if not path:
        if page is None:
            return made(SKIPPED, reason="fragment in file without route")
        return made(INTERNAL, base + page + suffix)
    plain = unquote(path.split("?", 1)[0])
    if plain.endswith(DOC_SUFFIXES):
        candidates = _md_candidates(link.file, plain)
        for target in candidates:
            if target in routes:
                return made(INTERNAL, base + routes[target] + suffix)
        return made(UNRESOLVED, candidates[0], "unresolved-md")
    if path.startswith("/"):
        if path.startswith(PROD_ONLY_PREFIXES):
            return made(EXTERNAL, PROD_URL + raw)
        return made(INTERNAL, base + raw)
    if page is None:
        return made(SKIPPED, reason="relative link in file without route")
    return made(INTERNAL, urljoin(base + page, raw))


def resolve_all(links: Iterable[Link], routes: Dict[str, str], base_url: str) -> List[ResolvedLink]:
    return [resolve_link(link, routes, base_url) for link in links]
