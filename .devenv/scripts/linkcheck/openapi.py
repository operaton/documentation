"""Find links in the OpenAPI spec behind the REST API reference (Redoc page)."""
from __future__ import annotations

import json
import urllib.request
from typing import Any, List, Optional
from urllib.parse import urljoin

from .extract import extract_text
from .models import Link

DEFAULT_PAGE_URL = "https://docs.operaton.org/reference/latest/rest-api/"
DEFAULT_SPEC_URL = DEFAULT_PAGE_URL + "operaton-rest-api.json"
HTTP_METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace")
SAMPLE_KEYS = ("example", "examples")  # sample payloads, not rendered as links
URL_PARENTS = ("externalDocs", "license", "contact")
LABEL = "REST API"


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
