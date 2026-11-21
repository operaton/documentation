"""Find links in Markdown/MDX sources, with line numbers."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

from .models import Link

# A backtick fence's info string cannot contain backticks (else it is inline code).
FENCE_RE = re.compile(r"^\s*(`{3,}(?=[^`]*$)|~{3,})")
# A definition is the destination plus an optional title, nothing else on the line.
REF_DEF_RE = re.compile(
    r"""^\s{0,3}\[([^\]]+)\]:\s*(<[^<>]*>|[^<\s]\S*)\s*("[^"]*"|'[^']*'|\([^)]*\))?\s*$""")
ATTR_RE = re.compile(r"""\b(href|src)\s*=\s*(["'])(.*?)\2""")
ALT_RE = re.compile(r"""\balt\s*=\s*(["'])(.*?)\1""")
TAG_RE = re.compile(r"<[^>]*>")
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


def _clean_text(text: str) -> str:
    return " ".join(TAG_RE.sub(" ", text).split())


def bracket_text(line: str, close: int, original: str) -> str:
    """Text of the [...] that ends at line[close] (the ']'), taken from the original line.

    `line` is the scanned line (inline code blanked), `original` the line as written, same length.
    """
    depth = 0
    for i in range(close - 1, -1, -1):
        c = line[i]
        if c == "]":
            depth += 1
        elif c == "[":
            if depth == 0:
                return _clean_text(original[i + 1:close])
            depth -= 1
    return ""


def _html_text(line: str, match: re.Match, original: str) -> str:
    """Text of an <a href> (up to </a> on the same line) or the alt text of an <img src>."""
    tag_start = line.rfind("<", 0, match.start())
    tag_end = line.find(">", match.end())
    if tag_start == -1 or tag_end == -1:
        return ""
    if match.group(1) == "src":
        alt = ALT_RE.search(original, tag_start, tag_end)
        return _clean_text(alt.group(2)) if alt else ""
    close = line.lower().find("</a", tag_end)
    return _clean_text(original[tag_end + 1:close if close != -1 else len(original)])


def _links_in_line(line: str, original: Optional[str] = None) -> List[Tuple[str, bool, str]]:
    """(destination, is_html_attribute, link text) in order of appearance."""
    original = line if original is None else original
    ref = REF_DEF_RE.match(line)
    if ref and not ref.group(1).startswith("^"):
        dest = ref.group(2)
        return [(dest[1:-1] if dest.startswith("<") else dest, False, _clean_text(ref.group(1)))]
    found: List[Tuple[int, str, bool, str]] = []
    for m in re.finditer(r"\]\(", line):
        raw = parse_destination(line, m.end())
        if raw:
            found.append((m.start(), raw, False, bracket_text(line, m.start(), original)))
    for m in ATTR_RE.finditer(line):
        if m.group(3):
            found.append((m.start(), m.group(3), True, _html_text(line, m, original)))
    for m in AUTOLINK_RE.finditer(line):
        found.append((m.start(), m.group(1), False, m.group(1)))
    return [(raw, html, text) for _, raw, html, text in sorted(found, key=lambda item: item[0])]


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
        original = line
        line = INLINE_CODE_RE.sub(_blank, line)
        links.extend(Link(rel_path, lineno, raw, html, text=text)
                     for raw, html, text in _links_in_line(line, original))
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
