"""Join check results with the link map and render reports."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, Iterable, List, Optional

from .lychee import normalize_url
from .models import EXTERNAL, INTERNAL, UNRESOLVED, Failure, ResolvedLink

SECTIONS = (("Internal", (INTERNAL, UNRESOLVED)), ("External", (EXTERNAL,)))
SECTION_ORDER = {INTERNAL: 0, UNRESOLVED: 0, EXTERNAL: 1}


def collect_failures(resolved: Iterable[ResolvedLink], statuses: Dict[str, str]) -> List[Failure]:
    by_key = {normalize_url(url): status for url, status in statuses.items()}
    failures: List[Failure] = []
    for r in resolved:
        if r.kind == UNRESOLVED:
            failures.append(Failure(r, r.reason))
        elif r.kind in (INTERNAL, EXTERNAL):
            status = by_key.get(normalize_url(r.url))
            if status is not None:
                failures.append(Failure(r, status))
    failures.sort(key=lambda f: (SECTION_ORDER[f.resolved.kind], f.resolved.link.file, f.resolved.link.line))
    return failures


def format_console(failures: List[Failure]) -> str:
    lines = []
    for f in failures:
        link = f.resolved.link
        target = f"  -> {f.resolved.url}" if f.resolved.kind == INTERNAL else ""
        lines.append(f"{link.file}:{link.line}  {link.raw}  {f.status}{target}")
    return "\n".join(lines)


def _escape_data(text: str) -> str:
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def _escape_property(text: str) -> str:
    return _escape_data(text).replace(":", "%3A").replace(",", "%2C")


def format_annotations(failures: List[Failure]) -> str:
    return "\n".join(
        f"::error file={_escape_property(f.resolved.link.file)},line={f.resolved.link.line}"
        f"::{_escape_data(f'Broken link {f.resolved.link.raw}: {f.status}')}"
        for f in failures
    )


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


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
    shown = 0
    for title, kinds in SECTIONS:
        section = [f for f in failures if f.resolved.kind in kinds]
        if not section:
            continue
        block = f"\n### {title}\n\n| Page | Line | URL | Status |\n|---|---|---|---|\n"
        if len(out) + len(block) > limit:
            break
        out += block
        for f in section:
            link = f.resolved.link
            row = (f"| [{link.file}](https://github.com/{repo}/blob/{sha}/{link.file}#L{link.line}) "
                   f"| {link.line} | {_cell(link.raw)} | {_cell(f.status)} |\n")
            if len(out) + len(row) > limit:
                break
            out += row
            shown += 1
    if shown < len(failures):
        out += f"\n+{len(failures) - shown} more broken links, see the workflow run summary or run the check locally.\n"
    return out
