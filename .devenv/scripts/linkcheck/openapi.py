"""Find links in the OpenAPI spec behind the REST API reference (Redoc page)."""
from __future__ import annotations

import json
import re
import urllib.request
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit

from .extract import extract_text
from .models import Link

DEFAULT_PAGE_URL = "https://docs.operaton.org/reference/latest/rest-api/"
DEFAULT_SPEC_URL = DEFAULT_PAGE_URL + "operaton-rest-api.json"
HTTP_METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace")
SAMPLE_KEYS = ("example", "examples")  # sample payloads, not rendered as links
URL_PARENTS = ("externalDocs", "license", "contact")
LABEL = "REST API"
MISSING_FRAGMENT = "Cannot find fragment"
# Redoc anchors the spec does not define (description sections, schemas) cannot be validated.
CHECKED_ANCHOR_PREFIXES = ("tag/", "operation/")


class SpecError(Exception):
    pass


def load_spec(location: str) -> dict:
    """Read the spec from a URL or a local file."""
    try:
        if location.startswith(("http://", "https://")):
            with urllib.request.urlopen(location, timeout=60) as response:
                text = response.read().decode("utf-8")
        else:
            with open(location, encoding="utf-8") as f:
                text = f.read()
        return json.loads(text)
    except (OSError, ValueError) as exc:
        raise SpecError(f"cannot load REST API spec {location}: {exc}") from exc


def _location(path: List[str], page_url: str, spec: dict) -> tuple:
    """(label, page URL) for a link found at JSON path `path`."""
    if len(path) >= 3 and path[0] == "paths" and path[2] in HTTP_METHODS:
        label = f"{LABEL} {path[2].upper()} {path[1]}"
        rest = path[3:]
        if rest:
            label += f" ({'/'.join(rest)})"
        operation_id = spec["paths"][path[1]][path[2]].get("operationId")
        return label, page_url + (f"#operation/{operation_id}" if operation_id else "")
    return f"{LABEL} {'/'.join(path)}", page_url


def extract_spec(spec: dict, page_url: str = DEFAULT_PAGE_URL) -> List[Link]:
    """Links in descriptions and documentation URLs, resolved against the Redoc page URL."""
    links: List[Link] = []

    def add(raw: str, path: List[str]) -> None:
        label, source = _location(path, page_url, spec)
        links.append(Link(label, 0, urljoin(page_url, raw), source_url=source))

    def walk(node: Any, path: List[str], parent: Optional[str]) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key in SAMPLE_KEYS:
                    continue
                if key == "description" and isinstance(value, str):
                    for link in extract_text(value, ""):
                        add(link.raw, path)
                elif key == "url" and parent in URL_PARENTS and isinstance(value, str):
                    add(value, path)
                else:
                    walk(value, path + [str(key)], str(key))
        elif isinstance(node, list):
            for i, value in enumerate(node):
                walk(value, path + [str(i)], parent)

    walk(spec, [], None)
    return links


def _slug(name: str) -> str:
    """Redoc's anchor form of a tag name."""
    return re.sub(r"\s+", "-", name.strip())


def redoc_anchors(spec: dict) -> Set[str]:
    """Fragments the Redoc page renders for the tags and operations in the spec."""
    anchors = {f"tag/{_slug(t['name'])}" for t in spec.get("tags") or [] if t.get("name")}
    for methods in (spec.get("paths") or {}).values():
        for method, operation in methods.items():
            if method not in HTTP_METHODS or not operation.get("operationId"):
                continue
            op = f"operation/{operation['operationId']}"
            anchors.add(op)
            for tag in operation.get("tags") or []:
                anchors.add(f"tag/{_slug(tag)}")
                anchors.add(f"tag/{_slug(tag)}/{op}")
    return anchors


def _split_redoc(url: str, page_url: str) -> Optional[Tuple[str, str]]:
    """(page URL, fragment) when `url` points into the Redoc page, else None."""
    parts = urlsplit(url)
    page = urlsplit(page_url)
    if not parts.fragment or (parts.netloc, parts.path.rstrip("/")) != (page.netloc, page.path.rstrip("/")):
        return None
    return urlunsplit(parts._replace(fragment="")), unquote(parts.fragment)


def strip_redoc_fragments(urls: Iterable[str], anchors: Optional[Set[str]],
                          page_url: str = DEFAULT_PAGE_URL) -> Tuple[List[str], Dict[str, str], Dict[str, str]]:
    """Redoc renders its anchors in the browser, so lychee never finds them in the HTML.

    Returns the URLs to give lychee (Redoc fragments removed), statuses for fragments the spec
    does not define (unchecked when `anchors` is None), and {URL with fragment: page URL}.
    """
    to_check: Set[str] = set()
    statuses: Dict[str, str] = {}
    pages: Dict[str, str] = {}
    for url in urls:
        split = _split_redoc(url, page_url)
        if split is None:
            to_check.add(url)
            continue
        page, fragment = split
        to_check.add(page)
        pages[url] = page
        if anchors is not None and fragment.startswith(CHECKED_ANCHOR_PREFIXES) and fragment not in anchors:
            statuses[url] = MISSING_FRAGMENT
    return sorted(to_check), statuses, pages


def apply_page_statuses(statuses: Dict[str, str], pages: Dict[str, str], checked: Iterable[str]) -> None:
    """Report a failing Redoc page under the links that point into it."""
    for url, page in pages.items():
        if page in statuses:
            statuses.setdefault(url, statuses[page])
    linked = set(checked)
    for page in set(pages.values()) - linked:
        statuses.pop(page, None)
