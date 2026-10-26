"""Find links in Markdown/MDX sources, with line numbers."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

from .models import Link

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
# A definition is the destination plus an optional title, nothing else on the line.
REF_DEF_RE = re.compile(
    r"""^\s{0,3}\[([^\]]+)\]:\s*(<[^<>]*>|[^<\s]\S*)\s*("[^"]*"|'[^']*'|\([^)]*\))?\s*$""")
ATTR_RE = re.compile(r"""\b(?:href|src)\s*=\s*(["'])(.*?)\1""")
AUTOLINK_RE = re.compile(r"(?<!\]\()<(https?://[^>\s]+)>")
INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
COMMENT_RE = re.compile(r"<!--.*?-->")
DOC_SUFFIXES = (".md", ".mdx")


def _blank(match: re.Match) -> str:
    return " " * len(match.group(0))


def parse_destination(text: str, start: int) -> str:
    """Return the link destination starting at text[start], i.e. right after '](' ."""
    n = len(text)
    i = start
    while i < n and text[i] in " \t":
        i += 1
    if i < n and text[i] == "<":
        end = text.find(">", i + 1)
        return text[i + 1:end] if end != -1 else ""
    depth = 0
    j = i
    while j < n:
        c = text[j]
        if c == "\\" and j + 1 < n:
            j += 2
            continue
        if c in " \t":
            break
        if c == "(":
            depth += 1
        elif c == ")":
            if depth == 0:
                break
            depth -= 1
        j += 1
    return text[i:j]


def _links_in_line(line: str) -> List[Tuple[str, bool]]:
    """(destination, is_html_attribute) pairs in order of appearance."""
    ref = REF_DEF_RE.match(line)
    if ref and not ref.group(1).startswith("^"):
        dest = ref.group(2)
        return [(dest[1:-1] if dest.startswith("<") else dest, False)]
    found: List[Tuple[int, str, bool]] = []
    for m in re.finditer(r"\]\(", line):
        raw = parse_destination(line, m.end())
        if raw:
            found.append((m.start(), raw, False))
    for m in ATTR_RE.finditer(line):
        if m.group(2):
            found.append((m.start(), m.group(2), True))
    for m in AUTOLINK_RE.finditer(line):
        found.append((m.start(), m.group(1), False))
    return [(raw, html) for _, raw, html in sorted(found, key=lambda item: item[0])]


def extract_text(text: str, rel_path: str) -> List[Link]:
    """Return all links in a Markdown/MDX text, skipping frontmatter, code and comments."""
    lines = text.splitlines()
    links: List[Link] = []
    in_frontmatter = bool(lines) and lines[0].strip() == "---"
    fence: Optional[Tuple[str, int]] = None
    in_comment = False
    for lineno, line in enumerate(lines, start=1):
        if in_frontmatter:
            if lineno > 1 and line.strip() == "---":
                in_frontmatter = False
            continue
        if fence:
            stripped = line.strip()
            if stripped and set(stripped) == {fence[0]} and len(stripped) >= fence[1]:
                fence = None
            continue
        if not in_comment:
            opening = FENCE_RE.match(line)
            if opening:
                fence = (opening.group(1)[0], len(opening.group(1)))
                continue
        if in_comment:
            end = line.find("-->")
            if end == -1:
                continue
            line = " " * (end + 3) + line[end + 3:]
            in_comment = False
        line = COMMENT_RE.sub(_blank, line)
        start = line.find("<!--")
        if start != -1:
            line = line[:start]
            in_comment = True
        line = INLINE_CODE_RE.sub(_blank, line)
        links.extend(Link(rel_path, lineno, raw, html) for raw, html in _links_in_line(line))
    return links


def iter_doc_files(docs_dir: Path) -> List[Path]:
    """All .md/.mdx files below docs_dir, sorted."""
    return sorted(p for p in docs_dir.rglob("*") if p.suffix in DOC_SUFFIXES and p.is_file())


def extract_files(repo_root: Path, files: Iterable[Path]) -> List[Link]:
    """Extract links from files; Link.file is relative to repo_root."""
    root = repo_root.resolve()
    links: List[Link] = []
    for path in files:
        rel = path.resolve().relative_to(root).as_posix()
        links.extend(extract_text(path.read_text(encoding="utf-8"), rel))
    return links
