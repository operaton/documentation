"""Data types shared by the link checker modules."""
from __future__ import annotations

from dataclasses import dataclass

INTERNAL = "internal"
EXTERNAL = "external"
UNRESOLVED = "unresolved"
SKIPPED = "skipped"


@dataclass(frozen=True)
class Link:
    """A link as written in a source file."""
    file: str  # repo-relative POSIX path, e.g. docs/documentation/index.md
    line: int  # 1-based
    raw: str   # destination exactly as written
    html: bool = False  # from a raw HTML/JSX attribute: Docusaurus does not rewrite .md there
    source_url: str = ""  # page the link is on when it is not a repo file (REST API); line is 0 then


@dataclass(frozen=True)
class ResolvedLink:
    """A link classified and resolved to the URL that gets checked."""
    link: Link
    kind: str        # INTERNAL | EXTERNAL | UNRESOLVED | SKIPPED
    url: str         # absolute URL; target path for UNRESOLVED; "" for SKIPPED
    reason: str = ""  # why a link is UNRESOLVED or SKIPPED


@dataclass(frozen=True)
class Failure:
    """A broken link occurrence."""
    resolved: ResolvedLink
    status: str
