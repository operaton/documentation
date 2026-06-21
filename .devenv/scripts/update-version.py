#!/usr/bin/env python3
"""Update Operaton platform version references across docs.

Usage: python3 update-version.py <new-version>

Targets:
  - <operaton.version>X.Y.Z</operaton.version>
  - <operaton.external-task-client.version>X.Y.Z</...>
  - <version>X.Y.Z</version> within 5 lines of an org.operaton groupId
  - "Operaton engine vX.Y.Z" in prose
  - e.g. `X.Y.Z` in $PLATFORM_VERSION description lines

Skips: version-compatibility tables (historical), release notes.
"""
import re
import sys
from pathlib import Path

SKIP_DIRS = {"release-notes", "changelog"}
VERSION_RE = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")


def update_text(text: str, new: str) -> str:
    # 1. <operaton.version>
    text = re.sub(
        r"(<operaton\.version>)" + VERSION_RE.pattern + r"(</operaton\.version>)",
        rf"\g<1>{new}\2",
        text,
    )

    # 2. <operaton.external-task-client.version>
    text = re.sub(
        r"(<operaton\.external-task-client\.version>)" + VERSION_RE.pattern + r"(</operaton\.external-task-client\.version>)",
        rf"\g<1>{new}\2",
        text,
    )

    # 3. bare <version> within 5 lines after org.operaton groupId
    lines = text.splitlines(keepends=True)
    countdown = 0
    for i, line in enumerate(lines):
        if "org.operaton" in line and "<groupId>" in line:
            countdown = 5
        elif countdown > 0:
            m = re.search(r"(<version>)" + VERSION_RE.pattern + r"(</version>)", line)
            if m:
                lines[i] = line[: m.start()] + m.group(1) + new + m.group(2) + line[m.end() :]
                countdown = 0
                continue
            countdown -= 1
    text = "".join(lines)

    # 4. "Operaton engine vX.Y.Z" in prose
    text = re.sub(
        r"(Operaton engine v)" + VERSION_RE.pattern,
        rf"\g<1>{new}",
        text,
    )

    # 5. e.g. `X.Y.Z` on $PLATFORM_VERSION description lines
    text = re.sub(
        r"(\$PLATFORM_VERSION[^\n]+e\.g\. `)" + VERSION_RE.pattern + r"(`)",
        rf"\g<1>{new}\g<2>",
        text,
    )

    return text


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <new-version>", file=sys.stderr)
        sys.exit(1)

    new = sys.argv[1]
    if not VERSION_RE.fullmatch(new):
        print(f"error: '{new}' does not look like X.Y.Z", file=sys.stderr)
        sys.exit(1)

    docs = Path("docs")
    changed = []

    for md in sorted(docs.rglob("*.md")):
        if should_skip(md):
            continue
        original = md.read_text()
        updated = update_text(original, new)
        if updated != original:
            md.write_text(updated)
            changed.append(md)

    if changed:
        print(f"Updated {len(changed)} file(s) to {new}:")
        for f in changed:
            print(f"  {f}")
    else:
        print(f"No files needed updating (already at {new}?).")


if __name__ == "__main__":
    main()
