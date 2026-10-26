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
