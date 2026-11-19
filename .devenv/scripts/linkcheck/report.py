"""Join check results with the link map and render reports."""
from __future__ import annotations

import re
from datetime import datetime
from typing import Dict, Iterable, List, Optional

from .lychee import normalize_url
from .models import EXTERNAL, INTERNAL, UNRESOLVED, Failure, Link, ResolvedLink

SECTIONS = (("Internal", (INTERNAL, UNRESOLVED)), ("External", (EXTERNAL,)))
SECTION_ORDER = {INTERNAL: 0, UNRESOLVED: 0, EXTERNAL: 1}
UNKNOWN_SOURCE = "(source unknown)"
NOTE_RESERVE = 200  # room for the "+N more" note


def collect_failures(resolved: Iterable[ResolvedLink], statuses: Dict[str, str]) -> List[Failure]:
    by_key = {normalize_url(url): (url, status) for url, status in statuses.items()}
    matched = set()
    failures: List[Failure] = []
    for r in resolved:
        if r.kind == UNRESOLVED:
            failures.append(Failure(r, r.reason))
        elif r.kind in (INTERNAL, EXTERNAL):
            key = normalize_url(r.url)
            if key in by_key:
                matched.add(key)
                failures.append(Failure(r, by_key[key][1]))
    # A failure lychee reports under a URL we cannot map back must still fail the run.
    for key, (url, status) in by_key.items():
        if key not in matched:
            failures.append(Failure(ResolvedLink(Link(UNKNOWN_SOURCE, 0, url), EXTERNAL, url), status))
    failures.sort(key=lambda f: (SECTION_ORDER[f.resolved.kind], f.resolved.link.file, f.resolved.link.line))
    return failures


def _where(link: Link) -> str:
    return f"{link.file}:{link.line}" if link.line else link.file


def format_console(failures: List[Failure]) -> str:
    lines = []
    for f in failures:
        link = f.resolved.link
        target = f"  -> {f.resolved.url}" if f.resolved.kind == INTERNAL else ""
        lines.append(f"{_where(link)}  {link.raw}  {f.status}{target}")
    return "\n".join(lines)


def _escape_data(text: str) -> str:
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def _escape_property(text: str) -> str:
    return _escape_data(text).replace(":", "%3A").replace(",", "%2C")


def _annotation(f: Failure) -> str:
    link = f.resolved.link
    if link.source_url:
        return f"::error::{_escape_data(f'Broken link {link.raw} in {link.file}: {f.status}')}"
    if link.line == 0:
        return f"::error::{_escape_data(f'Broken link {link.raw} (source line unknown): {f.status}')}"
    return (f"::error file={_escape_property(link.file)},line={link.line}"
            f"::{_escape_data(f'Broken link {link.raw}: {f.status}')}")


def format_annotations(failures: List[Failure]) -> str:
    return "\n".join(_annotation(f) for f in failures)


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def _row(f: Failure, repo: str, sha: str) -> str:
    link = f.resolved.link
    if link.source_url:
        page, line = f"[{_cell(link.file)}]({link.source_url})", ""
    elif link.line == 0:
        page, line = link.file, ""
    else:
        page = f"[{link.file}](https://github.com/{repo}/blob/{sha}/{link.file}#L{link.line})"
        line = str(link.line)
    return f"| {page} | {line} | {_cell(link.raw)} | {_cell(f.status)} |\n"


def _budgets(needs: List[int], available: int) -> List[int]:
    """Share `available` characters between sections; small sections get all they need."""
    budgets = [0] * len(needs)
    order = sorted(range(len(needs)), key=lambda i: needs[i])
    for done, i in enumerate(order):
        share = available // (len(needs) - done)
        budgets[i] = min(needs[i], share)
        available -= budgets[i]
    return budgets


def format_markdown(failures: List[Failure], *, checked: Dict[str, int], repo: str, sha: str,
                    run_url: Optional[str], now: datetime, limit: int = 60000) -> str:
    head = ["## Link check", ""]
    meta = f"{now.strftime('%Y-%m-%d %H:%M')} UTC, commit `{sha[:12]}`"
    if run_url:
        meta += f", [workflow run]({run_url})"
    head.append(meta)
    head.append("")
    scope = f"Checked {checked.get('internal', 0)} internal and {checked.get('external', 0)} external URLs."
    if not failures:
        return "\n".join(head + [f"No broken links. {scope}", ""])
    counts = {title: sum(1 for f in failures if f.resolved.kind in kinds) for title, kinds in SECTIONS}
    head.append(f"**{len(failures)} broken links** (internal: {counts['Internal']}, "
                f"external: {counts['External']}). {scope}")
    out = "\n".join(head) + "\n"

    sections = []
    for title, kinds in SECTIONS:
        rows = [_row(f, repo, sha) for f in failures if f.resolved.kind in kinds]
        if rows:
            block = f"\n### {title}\n\n| Page | Line | URL | Status |\n|---|---|---|---|\n"
            sections.append((block, rows))
    needs = [len(block) + sum(len(r) for r in rows) for block, rows in sections]
    budgets = _budgets(needs, limit - len(out) - NOTE_RESERVE)

    shown = 0
    for (block, rows), budget in zip(sections, budgets):
        if len(block) > budget:
            continue
        out += block
        used = len(block)
        for row in rows:
            if used + len(row) > budget:
                break
            out += row
            used += len(row)
            shown += 1
    if shown < len(failures):
        out += (f"\n+{len(failures) - shown} more broken links. The full list is in the log of the "
                f"\"Check links\" step of the workflow run, or run the check locally.\n")
    return out


# (pattern on the lychee status, problem), first match wins
PROBLEMS = (
    (r"^unresolved-md$", "missing page"),
    (r"fragment", "missing anchor"),
    (r"\b(404|410)\b", "not found (404/410)"),
    (r"\b(401|403)\b", "access denied (401/403)"),
    (r"timeout", "timeout"),
    (r"network error", "network error"),
)
OTHER = "other error"
PROBLEM_ORDER = [problem for _, problem in PROBLEMS] + [OTHER]


def _type_key(f: Failure) -> tuple:
    source = "REST API" if f.resolved.link.source_url else "Docs"
    scope = "external" if f.resolved.kind == EXTERNAL else "internal"
    problem = next((p for pattern, p in PROBLEMS if re.search(pattern, f.status, re.IGNORECASE)), OTHER)
    return source, scope, problem


def link_type(f: Failure) -> str:
    """Group name of a failure, e.g. "Docs, external: not found (404/410)"."""
    source, scope, problem = _type_key(f)
    return f"{source}, {scope}: {problem}"


def _type_order(f: Failure) -> tuple:
    source, scope, problem = _type_key(f)
    return source != "Docs", scope != "internal", PROBLEM_ORDER.index(problem)


def format_text(failures: List[Failure], *, sha: str, run_url: Optional[str], now: datetime) -> str:
    """Plain text list of all broken links, grouped by link type."""
    meta = f"{now.strftime('%Y-%m-%d %H:%M')} UTC, commit {sha[:12]}"
    if run_url:
        meta += f", {run_url}"
    if not failures:
        return f"Link check: No broken links.\n{meta}\n"
    groups: Dict[str, List[Failure]] = {}
    for f in sorted(failures, key=_type_order):
        groups.setdefault(link_type(f), []).append(f)
    out = [f"Link check: {len(failures)} broken links in {len(groups)} types", meta]
    for name, members in groups.items():
        out += ["", f"== {name} ({len(members)}) =="]
        for f in members:
            link = f.resolved.link
            line = f"{_where(link)}  {link.raw}  [{f.status}]"
            if link.source_url:
                line += f"  ({link.source_url})"
            out.append(line)
    return "\n".join(out) + "\n"
