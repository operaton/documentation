#!/usr/bin/env python3
"""Update the Quarkus version compatibility table in the documentation.

Fetches all final releases from https://github.com/operaton/operaton,
looks up the Quarkus version from each release's root pom.xml
(property ``version.quarkus``), and rewrites the compatibility table in:

    docs/documentation/user-guide/quarkus-integration/version-compatibility.md

LTS information is read at runtime from the Quarkus release planning wiki:
    https://github.com/quarkusio/quarkus/wiki/Release-Planning

Rules applied:
  - One row per Operaton release (no grouping of patch versions).
  - Rows whose exact Operaton version cannot be found in any GitHub release
    are removed ("unknown versions").
  - Rows whose exact Operaton version is already listed are preserved as-is
    ("already listed versions are skipped").
  - Rows for new releases are added with the Quarkus version read from
    that release's root pom.xml.
  - All rows are sorted by Operaton semantic version (ascending).
  - Quarkus versions whose minor stream is marked as LTS in the wiki get
    " (LTS)" appended.

Usage:
    python3 .devenv/scripts/update-quarkus-version-table.py [--dry-run]

Environment variables:
    GITHUB_TOKEN   Optional GitHub personal-access token.  Without it the
                   GitHub API is still usable but at a lower rate limit.
"""

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from typing import Optional

# ── Configuration ─────────────────────────────────────────────────────────────

REPO = "operaton/operaton"
DOCS_FILE = "docs/documentation/user-guide/quarkus-integration/version-compatibility.md"
GITHUB_API_BASE = "https://api.github.com"
QUARKUS_WIKI_URL = (
    "https://raw.githubusercontent.com/wiki/quarkusio/quarkus/Release-Planning.md"
)

# ── GitHub API helpers ────────────────────────────────────────────────────────


def _github_get(path: str) -> object:
    token = os.environ.get("GITHUB_TOKEN", "")
    url = f"{GITHUB_API_BASE}{path}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        print(f"GitHub API error for {url}: {exc.code} {exc.reason}", file=sys.stderr)
        raise


def _parse_version(tag: str) -> Optional[tuple[int, int, int]]:
    """Parse vX.Y.Z tag format; return (major, minor, patch) or None."""
    m = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", tag)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def get_final_releases() -> list[tuple[int, int, int]]:
    """Return all final (vX.Y.Z) releases as sorted (major, minor, patch) tuples.

    A "final" release is one whose tag matches exactly ``vX.Y.Z`` with no
    additional suffix (no -alpha, -beta, -M*, -SNAPSHOT, …).
    The prerelease/draft flags in the GitHub API are *not* used because some
    milestone releases are incorrectly flagged as non-prerelease.
    """
    releases: list[tuple[int, int, int]] = []
    page = 1
    while True:
        data = _github_get(f"/repos/{REPO}/releases?per_page=100&page={page}")
        if not data:
            break
        for release in data:
            ver = _parse_version(release["tag_name"])
            if ver:
                releases.append(ver)
        if len(data) < 100:
            break
        page += 1
    return sorted(releases)


def get_quarkus_version(tag: str) -> Optional[str]:
    """Return the value of the ``version.quarkus`` property in pom.xml at *tag*."""
    try:
        data = _github_get(f"/repos/{REPO}/contents/pom.xml?ref={tag}")
        content = base64.b64decode(data["content"]).decode()
        start = content.find("<version.quarkus>")
        if start != -1:
            start += len("<version.quarkus>")
            end = content.find("</version.quarkus>", start)
            if end != -1:
                return content[start:end].strip()
        print(f"  Warning: <version.quarkus> not found in pom.xml at {tag}", file=sys.stderr)
    except Exception as exc:
        print(f"  Warning: could not fetch pom.xml for {tag}: {exc}", file=sys.stderr)
    return None


# ── Quarkus LTS detection ─────────────────────────────────────────────────────

# Matches headings like "## 3.33 LTS", "## 3.8 **LTS**", "## 3.20 LTS - …"
# but NOT "## 3.21 - … same time as 3.20 LTS" (LTS does not follow the version directly).
_WIKI_LTS_RE = re.compile(r"^## (\d+)\.(\d+)\s+\*{0,2}LTS\b", re.MULTILINE)


def get_quarkus_lts_versions() -> frozenset[tuple[int, int]]:
    """Fetch the Quarkus release-planning wiki and return LTS minor versions.

    Returns a frozenset of (major, minor) tuples, e.g. {(3, 8), (3, 15), …}.
    """
    print("Fetching Quarkus LTS versions from wiki…")
    try:
        req = urllib.request.Request(QUARKUS_WIKI_URL)
        req.add_header("User-Agent", "operaton-docs-update-script")
        with urllib.request.urlopen(req) as resp:
            wiki_text = resp.read().decode()
    except Exception as exc:
        print(f"  Warning: could not fetch Quarkus wiki: {exc}", file=sys.stderr)
        return frozenset()

    lts: set[tuple[int, int]] = set()
    for m in _WIKI_LTS_RE.finditer(wiki_text):
        lts.add((int(m.group(1)), int(m.group(2))))

    print(f"  Found LTS streams: {sorted(lts)}")
    return frozenset(lts)


def format_quarkus_cell(raw_version: str, lts_versions: frozenset[tuple[int, int]]) -> str:
    """Format a raw Quarkus version (e.g. ``3.33.1``) as ``X.Y.Z[ (LTS)]``."""
    m = re.match(r"(\d+)\.(\d+)", raw_version)
    if not m:
        return raw_version
    is_lts = (int(m.group(1)), int(m.group(2))) in lts_versions
    return f"{raw_version} (LTS)" if is_lts else raw_version


# ── Markdown table helpers ────────────────────────────────────────────────────

_ROW_RE = re.compile(r"<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>", re.DOTALL)
_VERSION_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)")
_TABLE_RE = re.compile(r'<table class="table table-striped">.*?</table>', re.DOTALL)


def parse_table_rows(content: str) -> list[tuple[str, str]]:
    """Return list of (operaton_cell, quarkus_cell) for every data row."""
    return [(m.group(1).strip(), m.group(2).strip()) for m in _ROW_RE.finditer(content)]


def _row_sort_key(operaton_cell: str) -> tuple[int, int, int]:
    m = _VERSION_RE.search(operaton_cell)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else (999, 999, 999)


def build_table(rows: list[tuple[str, str]]) -> str:
    lines = ['<table class="table table-striped">']
    lines += [
        "  <tr>",
        "    <th>Operaton version</th>",
        "    <th>Quarkus version</th>",
        "  </tr>",
    ]
    for op_cell, q_cell in rows:
        lines += [
            "  <tr>",
            f"    <td>{op_cell}</td>",
            f"    <td>{q_cell}</td>",
            "  </tr>",
        ]
    lines.append("</table>")
    return "\n".join(lines)


# ── Orchestration helpers ────────────────────────────────────────────────────


def extract_listed_versions(
    existing_rows: list[tuple[str, str]],
) -> set[tuple[int, int, int]]:
    """Extract exact Operaton versions (X.Y.Z) from existing table rows."""
    listed: set[tuple[int, int, int]] = set()
    for op_cell, _ in existing_rows:
        m = _VERSION_RE.search(op_cell)
        if m:
            listed.add((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return listed


def classify_existing_rows(
    existing_rows: list[tuple[str, str]], release_set: set[tuple[int, int, int]]
) -> list[tuple[str, str]]:
    """Filter existing rows to keep only those matching releases; log removals."""
    kept: list[tuple[str, str]] = []
    for op_cell, q_cell in existing_rows:
        m = _VERSION_RE.search(op_cell)
        if m:
            ver = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
            if ver in release_set:
                kept.append((op_cell, q_cell))
                print(f"  Keeping  : {op_cell} (already listed, skipping API lookup)")
            else:
                print(f"  Removing : {op_cell} (no matching release found)")
        else:
            print(f"  Removing : {op_cell!r} (cannot parse version)")
    return kept


def fetch_new_rows(
    new_versions: set[tuple[int, int, int]], lts_versions: frozenset[tuple[int, int]]
) -> list[tuple[str, str]]:
    """Fetch Quarkus versions for new releases and build rows."""
    new_rows: list[tuple[str, str]] = []
    for major, minor, patch in sorted(new_versions):
        tag = f"v{major}.{minor}.{patch}"
        print(f"  Fetching : {tag}…")
        raw_q = get_quarkus_version(tag)
        if raw_q:
            q_cell = format_quarkus_cell(raw_q, lts_versions)
            op_cell = f"{major}.{minor}.{patch}"
            print(f"             {op_cell} → Quarkus {q_cell}")
            new_rows.append((op_cell, q_cell))
        else:
            print(f"  Skipping {tag}: could not determine Quarkus version", file=sys.stderr)
    return new_rows


def main(dry_run: bool = False) -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    docs_path = os.path.join(repo_root, DOCS_FILE)

    if not os.path.exists(docs_path):
        print(f"Error: {docs_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(docs_path) as f:
        content = f.read()

    if not _TABLE_RE.search(content):
        print("Error: could not find the compatibility table in the file", file=sys.stderr)
        sys.exit(1)

    lts_versions = get_quarkus_lts_versions()
    existing_rows = parse_table_rows(content)
    print(f"Existing table rows: {len(existing_rows)}")

    listed_versions = extract_listed_versions(existing_rows)

    print("Fetching releases from GitHub…")
    releases = get_final_releases()
    release_set = set(releases)
    print(f"Found {len(releases)} final release(s): {[f'v{a}.{b}.{c}' for a,b,c in releases]}")

    kept_rows = classify_existing_rows(existing_rows, release_set)
    new_rows = fetch_new_rows(release_set - listed_versions, lts_versions)

    all_rows = sorted(kept_rows + new_rows, key=lambda r: _row_sort_key(r[0]))
    new_table = build_table(all_rows)
    new_content = _TABLE_RE.sub(new_table, content)

    if new_content == content:
        print("Table is already up to date – no changes made.")
        return

    if dry_run:
        print("\n─── Dry run – proposed table ───────────────────────────────")
        print(new_table)
        print("────────────────────────────────────────────────────────────")
    else:
        with open(docs_path, "w") as f:
            f.write(new_content)
        print(f"\nUpdated {DOCS_FILE}")


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
