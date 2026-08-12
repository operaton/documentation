# Automated Version Updates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a master Python script and updated GitHub Actions workflow that automatically updates all version references in active documentation when a new Operaton release is published.

**Architecture:** A single master script (`.devenv/scripts/update-versions.py`) fetches the latest Operaton release from GitHub, parses its SBOM for third-party versions (falling back to Maven Central), performs regex-based replacements across all active docs, then delegates compatibility table updates to the two existing scripts (refactored to expose a `run()` function). The existing `maintenance.yml` workflow is updated to call only the master script.

**Tech Stack:** Python 3.11, GitHub API (urllib), Maven Central Search API (solrsearch), `unittest` + `unittest.mock` for tests.

---

## File Map

| Action | Path | Responsibility |
|---|---|---|
| Create | `.devenv/scripts/update-versions.py` | Master orchestration script |
| Modify | `.devenv/scripts/update-spring-boot-version-table.py` | Expose `run()`, keep standalone entrypoint |
| Modify | `.devenv/scripts/update-quarkus-version-table.py` | Expose `run()`, keep standalone entrypoint |
| Modify | `.github/workflows/maintenance.yml` | Call only master script |
| Create | `.devenv/scripts/tests/test_update_versions.py` | Unit tests for master script |

---

## Task 1: Verify SBOM asset format in Operaton releases

Before writing any SBOM parsing code, confirm what asset is actually present.

**Files:** none (read-only investigation)

- [ ] **Step 1: List release assets for the latest Operaton release**

```bash
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/operaton/operaton/releases/latest" \
  | python3 -c "import json,sys; r=json.load(sys.stdin); [print(a['name'], a['content_type'], a['browser_download_url']) for a in r.get('assets',[])]"
```

Expected: a list of asset filenames. Look for any file ending in `.json` with `cyclonedx` or `spdx` in the name, or with content type `application/vnd.cyclonedx+json`.

- [ ] **Step 2: Download the SBOM and inspect its structure**

Replace `<SBOM_URL>` with the download URL found above:

```bash
curl -sL "<SBOM_URL>" | python3 -m json.tool | head -60
```

Expected output: JSON with either a `components` array (CycloneDX) or a `packages` array (SPDX).

- [ ] **Step 3: Confirm the `purl` / coordinate format for a known artifact**

```bash
curl -sL "<SBOM_URL>" | python3 -c "
import json, sys
data = json.load(sys.stdin)
# CycloneDX
for c in data.get('components', []):
    if 'slf4j' in c.get('purl','') or 'slf4j' in c.get('name',''):
        print(json.dumps(c, indent=2))
        break
"
```

Expected: a component entry showing how `groupId` and `artifactId` are encoded (likely as `purl` in the form `pkg:maven/org.slf4j/slf4j-simple@1.x.x`).

- [ ] **Step 4: Record findings**

Note in a comment at the top of `update-versions.py` (Task 2) what SBOM format and asset name pattern to use. If no SBOM is present, the implementation falls back to Maven Central only — note this too.

---

## Task 2: Refactor `update-spring-boot-version-table.py`

**Files:**
- Modify: `.devenv/scripts/update-spring-boot-version-table.py`

- [ ] **Step 1: Rename `main` to `run` and add a new `main` entrypoint**

Open `.devenv/scripts/update-spring-boot-version-table.py`. Find the existing `main` function (currently the last function, ~line 198). Rename it to `run`:

```python
def run(dry_run: bool = False) -> None:
    # ... existing body unchanged ...
```

Then at the bottom of the file, update the entrypoint:

```python
def main() -> None:
    run(dry_run="--dry-run" in sys.argv)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify standalone still works**

```bash
python3 .devenv/scripts/update-spring-boot-version-table.py --dry-run
```

Expected: prints the existing table or "already up to date" — no traceback.

- [ ] **Step 3: Commit**

```bash
git add .devenv/scripts/update-spring-boot-version-table.py
git commit -m "refactor: expose run() in update-spring-boot-version-table for import"
```

---

## Task 3: Refactor `update-quarkus-version-table.py`

**Files:**
- Modify: `.devenv/scripts/update-quarkus-version-table.py`

- [ ] **Step 1: Rename `main` to `run` and add a new `main` entrypoint**

Apply the same pattern as Task 2 to `.devenv/scripts/update-quarkus-version-table.py`.

Find the existing `main` function and rename it `run`:

```python
def run(dry_run: bool = False) -> None:
    # ... existing body unchanged ...
```

Add at the bottom:

```python
def main() -> None:
    run(dry_run="--dry-run" in sys.argv)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify standalone still works**

```bash
python3 .devenv/scripts/update-quarkus-version-table.py --dry-run
```

Expected: prints the existing table or "already up to date" — no traceback.

- [ ] **Step 3: Commit**

```bash
git add .devenv/scripts/update-quarkus-version-table.py
git commit -m "refactor: expose run() in update-quarkus-version-table for import"
```

---

## Task 4: Create master script skeleton and GitHub/SBOM helpers

**Files:**
- Create: `.devenv/scripts/update-versions.py`
- Create: `.devenv/scripts/tests/__init__.py`
- Create: `.devenv/scripts/tests/test_update_versions.py`

- [ ] **Step 1: Write failing tests for `get_latest_operaton_release` and SBOM helpers**

Create `.devenv/scripts/tests/__init__.py` (empty):

```python
```

Create `.devenv/scripts/tests/test_update_versions.py`:

```python
import json
import sys
import unittest
from io import BytesIO
from unittest.mock import MagicMock, patch

sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), ".."))
import update_versions as uv


FAKE_RELEASE = {"tag_name": "v2.2.0", "assets": [
    {"name": "operaton-2.2.0-cyclonedx.json",
     "content_type": "application/json",
     "browser_download_url": "https://example.com/sbom.json"},
]}

FAKE_SBOM = {"components": [
    {"purl": "pkg:maven/org.slf4j/slf4j-simple@2.0.9", "name": "slf4j-simple", "version": "2.0.9"},
    {"purl": "pkg:maven/jakarta.xml.bind/jakarta.xml.bind-api@4.0.2", "name": "jakarta.xml.bind-api", "version": "4.0.2"},
]}


class TestGetLatestRelease(unittest.TestCase):
    @patch("update_versions._github_get")
    def test_strips_v_prefix(self, mock_get):
        mock_get.return_value = FAKE_RELEASE
        self.assertEqual(uv.get_latest_operaton_release(), "2.2.0")

    @patch("update_versions._github_get")
    def test_returns_tag_version(self, mock_get):
        mock_get.return_value = {"tag_name": "v1.5.3", "assets": []}
        self.assertEqual(uv.get_latest_operaton_release(), "1.5.3")


class TestGetVersionFromSbom(unittest.TestCase):
    def test_finds_existing_component(self):
        version = uv.get_version_from_sbom(FAKE_SBOM, "org.slf4j", "slf4j-simple")
        self.assertEqual(version, "2.0.9")

    def test_returns_none_for_missing_component(self):
        version = uv.get_version_from_sbom(FAKE_SBOM, "com.example", "missing")
        self.assertIsNone(version)


class TestResolveVersion(unittest.TestCase):
    def test_prefers_sbom_over_maven_central(self):
        version = uv.resolve_version(FAKE_SBOM, "org.slf4j", "slf4j-simple")
        self.assertEqual(version, "2.0.9")

    @patch("update_versions.get_version_from_maven_central")
    def test_falls_back_to_maven_central_when_not_in_sbom(self, mock_mc):
        mock_mc.return_value = "3.5.0"
        version = uv.resolve_version(FAKE_SBOM, "com.example", "missing")
        self.assertEqual(version, "3.5.0")
        mock_mc.assert_called_once_with("com.example", "missing")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd .devenv/scripts && python3 -m pytest tests/test_update_versions.py -v 2>&1 | head -30
```

Expected: `ModuleNotFoundError: No module named 'update_versions'` — confirms tests are wired correctly.

- [ ] **Step 3: Create the master script with GitHub and SBOM helpers**

Create `.devenv/scripts/update-versions.py`:

```python
#!/usr/bin/env python3
"""Update all version references in the documentation.

Fetches the latest Operaton release from GitHub, resolves third-party
dependency versions via the release SBOM (CycloneDX JSON) or Maven Central,
then performs regex-based replacements across all active docs.

SBOM asset: looks for the first release asset whose name contains
'cyclonedx' and ends with '.json'. Falls back to Maven Central only if no
such asset is found.

Usage:
    python3 .devenv/scripts/update-versions.py [--dry-run]

Environment variables:
    GITHUB_TOKEN   Optional GitHub personal-access token.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

REPO = "operaton/operaton"
GITHUB_API_BASE = "https://api.github.com"
MAVEN_CENTRAL_SEARCH = "https://search.maven.org/solrsearch/select"

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = (SCRIPT_DIR / ".." / "..").resolve()
DOCS_DIR = REPO_ROOT / "docs"
ARCHIVE_DIR = DOCS_DIR / "get-started" / "archive"


# ── GitHub API ────────────────────────────────────────────────────────────────

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


def get_latest_operaton_release() -> str:
    """Return latest release version string without 'v' prefix, e.g. '2.2.0'."""
    data = _github_get(f"/repos/{REPO}/releases/latest")
    tag = data["tag_name"]
    return tag.lstrip("v")


# ── SBOM ──────────────────────────────────────────────────────────────────────

def _download_url(url: str) -> bytes:
    token = os.environ.get("GITHUB_TOKEN", "")
    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def get_sbom(release_data: dict) -> Optional[dict]:
    """Download and return the CycloneDX SBOM from a release asset dict.

    Returns None if no CycloneDX JSON asset is found.
    """
    for asset in release_data.get("assets", []):
        name = asset.get("name", "").lower()
        if "cyclonedx" in name and name.endswith(".json"):
            print(f"Downloading SBOM: {asset['name']}")
            raw = _download_url(asset["browser_download_url"])
            return json.loads(raw.decode())
    print("No CycloneDX SBOM asset found in release — will use Maven Central only.")
    return None


def get_version_from_sbom(sbom: dict, group_id: str, artifact_id: str) -> Optional[str]:
    """Look up a component version in a CycloneDX SBOM by groupId:artifactId.

    Matches on purl prefix 'pkg:maven/<group_id>/<artifact_id>@'.
    """
    if not sbom:
        return None
    purl_prefix = f"pkg:maven/{group_id}/{artifact_id}@"
    for component in sbom.get("components", []):
        purl = component.get("purl", "")
        if purl.startswith(purl_prefix):
            return component.get("version")
    return None


# ── Maven Central ─────────────────────────────────────────────────────────────

def get_version_from_maven_central(group_id: str, artifact_id: str) -> str:
    """Return the latest release version for a Maven artifact from Maven Central."""
    params = f"q=g:{group_id}+AND+a:{artifact_id}&rows=1&wt=json&core=gav"
    url = f"{MAVEN_CENTRAL_SEARCH}?{params}"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        docs = data["response"]["docs"]
        if not docs:
            raise RuntimeError(f"No results from Maven Central for {group_id}:{artifact_id}")
        return docs[0]["v"]
    except urllib.error.HTTPError as exc:
        print(f"Maven Central error for {group_id}:{artifact_id}: {exc.code}", file=sys.stderr)
        raise


def resolve_version(sbom: Optional[dict], group_id: str, artifact_id: str) -> str:
    """Return version from SBOM if present, else from Maven Central."""
    v = get_version_from_sbom(sbom, group_id, artifact_id)
    if v:
        return v
    return get_version_from_maven_central(group_id, artifact_id)


# ── Doc replacement ───────────────────────────────────────────────────────────

@dataclass
class Replacement:
    description: str
    pattern: re.Pattern
    replacement: Callable[[str], str]  # receives new_version, returns substitution string


def _make_replacements(operaton_version: str, sbom: Optional[dict]) -> list[Replacement]:
    def third_party(group_id: str, artifact_id: str) -> str:
        return resolve_version(sbom, group_id, artifact_id)

    return [
        Replacement(
            description="<operaton.version> property",
            pattern=re.compile(r"(<operaton\.version>)\d+\.\d+\.\d+(</operaton\.version>)"),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="operaton-bom <version>",
            pattern=re.compile(
                r"(<artifactId>operaton-bom</artifactId>\s*<version>)\d+\.\d+\.\d+(</version>)",
                re.DOTALL,
            ),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="operaton-engine-dmn-bom <version>",
            pattern=re.compile(
                r"(<artifactId>operaton-engine-dmn-bom</artifactId>\s*<version>)\d+\.\d+\.\d+(</version>)",
                re.DOTALL,
            ),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="operaton-bpm-junit5 <version>",
            pattern=re.compile(
                r"(<artifactId>operaton-bpm-junit5</artifactId>\s*<version>)\d+\.\d+\.\d+(</version>)",
                re.DOTALL,
            ),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="<operaton.external-task-client.version> property",
            pattern=re.compile(
                r"(<operaton\.external-task-client\.version>)\d+\.\d+\.\d+(</operaton\.external-task-client\.version>)"
            ),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="GitHub tree link /tree/vX.Y.Z/",
            pattern=re.compile(r"(github\.com/operaton/operaton/tree/v)\d+\.\d+\.\d+(/)"),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="slf4j-simple <version>",
            pattern=re.compile(
                r"(<artifactId>slf4j-simple</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)",
                re.DOTALL,
            ),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="jakarta.xml.bind-api <version>",
            pattern=re.compile(
                r"(<artifactId>jakarta\.xml\.bind-api</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)",
                re.DOTALL,
            ),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="javax.servlet-api <version>",
            pattern=re.compile(
                r"(<artifactId>javax\.servlet-api</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)",
                re.DOTALL,
            ),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="maven-compiler-plugin <version>",
            pattern=re.compile(
                r"(<artifactId>maven-compiler-plugin</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)",
                re.DOTALL,
            ),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="maven-war-plugin <version>",
            pattern=re.compile(
                r"(<artifactId>maven-war-plugin</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)",
                re.DOTALL,
            ),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="bootstrap webjars <version>",
            pattern=re.compile(
                r"(<artifactId>bootstrap</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)",
                re.DOTALL,
            ),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="uuid-creator <version>",
            pattern=re.compile(
                r"(<artifactId>uuid-creator</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)",
                re.DOTALL,
            ),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="logback-classic <version>",
            pattern=re.compile(
                r"(<artifactId>logback-classic</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)",
                re.DOTALL,
            ),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
        Replacement(
            description="<spring-boot.version> property",
            pattern=re.compile(
                r"(<spring-boot\.version>)\d+[\d.]+\d+(</spring-boot\.version>)"
            ),
            replacement=lambda v: lambda m: m.group(1) + v + m.group(2),
        ),
    ]


def _apply_replacements_to_text(text: str, replacements: list[Replacement],
                                 versions: dict[str, str]) -> tuple[str, list[str]]:
    """Apply all replacements to text. Returns (new_text, list_of_change_descriptions)."""
    changes = []
    for rep in replacements:
        new_text = rep.pattern.sub(rep.replacement(versions[rep.description]), text)
        if new_text != text:
            changes.append(rep.description)
            text = new_text
    return text, changes


def update_docs(replacements: list[Replacement], versions: dict[str, str],
                dry_run: bool = False) -> int:
    """Walk active docs, apply replacements. Returns count of changed files."""
    changed = 0
    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        if md_file.is_relative_to(ARCHIVE_DIR):
            continue
        original = md_file.read_text(encoding="utf-8")
        updated, changes = _apply_replacements_to_text(original, replacements, versions)
        if updated != original:
            changed += 1
            rel = md_file.relative_to(REPO_ROOT)
            if dry_run:
                print(f"  [dry-run] Would update {rel}: {', '.join(changes)}")
            else:
                md_file.write_text(updated, encoding="utf-8")
                print(f"  Updated {rel}: {', '.join(changes)}")
    return changed


# ── Orchestration ─────────────────────────────────────────────────────────────

def main(dry_run: bool = False) -> None:
    print("Fetching latest Operaton release…")
    release_data = _github_get(f"/repos/{REPO}/releases/latest")
    operaton_version = release_data["tag_name"].lstrip("v")
    print(f"Latest Operaton release: {operaton_version}")

    print("Fetching SBOM…")
    sbom = get_sbom(release_data)

    print("Resolving third-party versions…")
    replacements = _make_replacements(operaton_version, sbom)

    # Pre-resolve all versions so we can report them upfront
    versions: dict[str, str] = {}
    for rep in replacements:
        # Operaton-version replacements use operaton_version directly
        if rep.description in (
            "<operaton.version> property",
            "operaton-bom <version>",
            "operaton-engine-dmn-bom <version>",
            "operaton-bpm-junit5 <version>",
            "<operaton.external-task-client.version> property",
            "GitHub tree link /tree/vX.Y.Z/",
        ):
            versions[rep.description] = operaton_version
        else:
            # third-party: call resolve_version once and cache
            pass  # already embedded in replacement lambda via closure

    # Re-build replacements with pre-resolved versions for caching
    # (Simpler: call resolve_version eagerly here and pass versions dict)
    THIRD_PARTY = [
        ("slf4j-simple <version>", "org.slf4j", "slf4j-simple"),
        ("jakarta.xml.bind-api <version>", "jakarta.xml.bind", "jakarta.xml.bind-api"),
        ("javax.servlet-api <version>", "javax.servlet", "javax.servlet-api"),
        ("maven-compiler-plugin <version>", "org.apache.maven.plugins", "maven-compiler-plugin"),
        ("maven-war-plugin <version>", "org.apache.maven.plugins", "maven-war-plugin"),
        ("bootstrap webjars <version>", "org.webjars", "bootstrap"),
        ("uuid-creator <version>", "com.github.f4b6a3", "uuid-creator"),
        ("logback-classic <version>", "ch.qos.logback", "logback-classic"),
        ("<spring-boot.version> property", "org.springframework.boot", "spring-boot-dependencies"),
    ]
    for desc, gid, aid in THIRD_PARTY:
        v = resolve_version(sbom, gid, aid)
        print(f"  {desc}: {v}")
        versions[desc] = v

    OPERATON_DESCS = [
        "<operaton.version> property",
        "operaton-bom <version>",
        "operaton-engine-dmn-bom <version>",
        "operaton-bpm-junit5 <version>",
        "<operaton.external-task-client.version> property",
        "GitHub tree link /tree/vX.Y.Z/",
    ]
    for desc in OPERATON_DESCS:
        versions[desc] = operaton_version

    print(f"\nUpdating docs (dry_run={dry_run})…")
    changed = update_docs(replacements, versions, dry_run=dry_run)
    print(f"\n{changed} file(s) {'would be ' if dry_run else ''}updated.")

    print("\nUpdating Spring Boot compatibility table…")
    sys.path.insert(0, str(SCRIPT_DIR))
    import update_spring_boot_version_table as sb
    sb.run(dry_run=dry_run)

    print("\nUpdating Quarkus compatibility table…")
    import update_quarkus_version_table as qk
    qk.run(dry_run=dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
```

- [ ] **Step 4: Run the failing tests**

```bash
cd .devenv/scripts && python3 -m pytest tests/test_update_versions.py -v 2>&1 | head -40
```

Expected: tests run but some fail — `_make_replacements` closure pattern needs adjustment (see Task 5).

- [ ] **Step 5: Commit skeleton**

```bash
git add .devenv/scripts/update-versions.py .devenv/scripts/tests/
git commit -m "feat: add update-versions.py skeleton with GitHub/SBOM helpers"
```

---

## Task 5: Fix `_make_replacements` closure and version dispatch — make tests pass

The `_make_replacements` function as written in Task 4 has a closure/lambda structure that embeds version resolution inside the factory. `update_docs` receives a flat `versions` dict keyed by `description`. This task aligns the implementation so tests pass.

**Files:**
- Modify: `.devenv/scripts/update-versions.py`
- Modify: `.devenv/scripts/tests/test_update_versions.py`

- [ ] **Step 1: Simplify `_make_replacements` to take a pre-resolved `versions` dict**

Replace the `_make_replacements` function and `_apply_replacements_to_text` in `update-versions.py` with this simpler approach where `Replacement` stores the resolved version directly:

```python
@dataclass
class Replacement:
    description: str
    pattern: re.Pattern
    new_version: str  # resolved value to substitute


def _build_replacements(operaton_version: str, versions: dict[str, str]) -> list["Replacement"]:
    """Build replacement list from pre-resolved version dict."""
    ov = operaton_version
    return [
        Replacement("<operaton.version> property",
            re.compile(r"(<operaton\.version>)\d+\.\d+\.\d+(</operaton\.version>)"), ov),
        Replacement("operaton-bom <version>",
            re.compile(r"(<artifactId>operaton-bom</artifactId>\s*<version>)\d+\.\d+\.\d+(</version>)", re.DOTALL), ov),
        Replacement("operaton-engine-dmn-bom <version>",
            re.compile(r"(<artifactId>operaton-engine-dmn-bom</artifactId>\s*<version>)\d+\.\d+\.\d+(</version>)", re.DOTALL), ov),
        Replacement("operaton-bpm-junit5 <version>",
            re.compile(r"(<artifactId>operaton-bpm-junit5</artifactId>\s*<version>)\d+\.\d+\.\d+(</version>)", re.DOTALL), ov),
        Replacement("<operaton.external-task-client.version> property",
            re.compile(r"(<operaton\.external-task-client\.version>)\d+\.\d+\.\d+(</operaton\.external-task-client\.version>)"), ov),
        Replacement("GitHub tree link /tree/vX.Y.Z/",
            re.compile(r"(github\.com/operaton/operaton/tree/v)\d+\.\d+\.\d+(/)"), ov),
        Replacement("slf4j-simple <version>",
            re.compile(r"(<artifactId>slf4j-simple</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)", re.DOTALL),
            versions["slf4j-simple"]),
        Replacement("jakarta.xml.bind-api <version>",
            re.compile(r"(<artifactId>jakarta\.xml\.bind-api</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)", re.DOTALL),
            versions["jakarta.xml.bind-api"]),
        Replacement("javax.servlet-api <version>",
            re.compile(r"(<artifactId>javax\.servlet-api</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)", re.DOTALL),
            versions["javax.servlet-api"]),
        Replacement("maven-compiler-plugin <version>",
            re.compile(r"(<artifactId>maven-compiler-plugin</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)", re.DOTALL),
            versions["maven-compiler-plugin"]),
        Replacement("maven-war-plugin <version>",
            re.compile(r"(<artifactId>maven-war-plugin</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)", re.DOTALL),
            versions["maven-war-plugin"]),
        Replacement("bootstrap webjars <version>",
            re.compile(r"(<artifactId>bootstrap</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)", re.DOTALL),
            versions["bootstrap"]),
        Replacement("uuid-creator <version>",
            re.compile(r"(<artifactId>uuid-creator</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)", re.DOTALL),
            versions["uuid-creator"]),
        Replacement("logback-classic <version>",
            re.compile(r"(<artifactId>logback-classic</artifactId>\s*<version>)\d+[\d.]+\d+(</version>)", re.DOTALL),
            versions["logback-classic"]),
        Replacement("<spring-boot.version> property",
            re.compile(r"(<spring-boot\.version>)\d+[\d.]+\d+(</spring-boot\.version>)"),
            versions["spring-boot"]),
    ]


def _apply_replacements_to_text(text: str, replacements: list["Replacement"]) -> tuple[str, list[str]]:
    changes = []
    for rep in replacements:
        new_text = rep.pattern.sub(lambda m, v=rep.new_version: m.group(1) + v + m.group(2), text)
        if new_text != text:
            changes.append(rep.description)
            text = new_text
    return text, changes


def update_docs(replacements: list["Replacement"], dry_run: bool = False) -> int:
    changed = 0
    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        if md_file.is_relative_to(ARCHIVE_DIR):
            continue
        original = md_file.read_text(encoding="utf-8")
        updated, changes = _apply_replacements_to_text(original, replacements)
        if updated != original:
            changed += 1
            rel = md_file.relative_to(REPO_ROOT)
            if dry_run:
                print(f"  [dry-run] Would update {rel}: {', '.join(changes)}")
            else:
                md_file.write_text(updated, encoding="utf-8")
                print(f"  Updated {rel}: {', '.join(changes)}")
    return changed
```

Also replace the `main()` function's `update_docs` call and `_make_replacements` call to use `_build_replacements(operaton_version, third_party_versions)` where `third_party_versions` is the dict built from THIRD_PARTY resolution. Remove the now-stale `_make_replacements` function.

- [ ] **Step 2: Update tests to match the new API**

Replace the test file content with:

```python
import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))
import update_versions as uv


FAKE_SBOM = {"components": [
    {"purl": "pkg:maven/org.slf4j/slf4j-simple@2.0.9", "version": "2.0.9"},
    {"purl": "pkg:maven/jakarta.xml.bind/jakarta.xml.bind-api@4.0.2", "version": "4.0.2"},
]}


class TestGetLatestRelease(unittest.TestCase):
    @patch("update_versions._github_get")
    def test_strips_v_prefix(self, mock_get):
        mock_get.return_value = {"tag_name": "v2.2.0", "assets": []}
        self.assertEqual(uv.get_latest_operaton_release(), "2.2.0")

    @patch("update_versions._github_get")
    def test_strips_v_prefix_single_digit(self, mock_get):
        mock_get.return_value = {"tag_name": "v1.5.3", "assets": []}
        self.assertEqual(uv.get_latest_operaton_release(), "1.5.3")


class TestGetVersionFromSbom(unittest.TestCase):
    def test_finds_existing_component(self):
        self.assertEqual(uv.get_version_from_sbom(FAKE_SBOM, "org.slf4j", "slf4j-simple"), "2.0.9")

    def test_returns_none_for_missing(self):
        self.assertIsNone(uv.get_version_from_sbom(FAKE_SBOM, "com.example", "missing"))

    def test_returns_none_for_none_sbom(self):
        self.assertIsNone(uv.get_version_from_sbom(None, "org.slf4j", "slf4j-simple"))


class TestResolveVersion(unittest.TestCase):
    def test_prefers_sbom(self):
        self.assertEqual(uv.resolve_version(FAKE_SBOM, "org.slf4j", "slf4j-simple"), "2.0.9")

    @patch("update_versions.get_version_from_maven_central")
    def test_falls_back_to_maven_central(self, mock_mc):
        mock_mc.return_value = "3.5.0"
        self.assertEqual(uv.resolve_version(FAKE_SBOM, "com.example", "missing"), "3.5.0")
        mock_mc.assert_called_once_with("com.example", "missing")


class TestApplyReplacements(unittest.TestCase):
    def _make_rep(self, desc, pattern, version):
        import re
        return uv.Replacement(desc, re.compile(pattern), version)

    def test_replaces_operaton_version(self):
        text = "<operaton.version>1.0.0</operaton.version>"
        rep = self._make_rep(
            "test",
            r"(<operaton\.version>)\d+\.\d+\.\d+(</operaton\.version>)",
            "2.2.0",
        )
        result, changes = uv._apply_replacements_to_text(text, [rep])
        self.assertEqual(result, "<operaton.version>2.2.0</operaton.version>")
        self.assertEqual(changes, ["test"])

    def test_no_change_when_already_current(self):
        text = "<operaton.version>2.2.0</operaton.version>"
        rep = self._make_rep(
            "test",
            r"(<operaton\.version>)\d+\.\d+\.\d+(</operaton\.version>)",
            "2.2.0",
        )
        result, changes = uv._apply_replacements_to_text(text, [rep])
        self.assertEqual(result, text)
        self.assertEqual(changes, [])

    def test_skips_archive_directory(self):
        """update_docs must not touch files under docs/get-started/archive/."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive = tmp_path / "docs" / "get-started" / "archive"
            archive.mkdir(parents=True)
            active = tmp_path / "docs" / "get-started"
            active.mkdir(parents=True, exist_ok=True)

            archive_file = archive / "old.md"
            archive_file.write_text("<operaton.version>1.0.0</operaton.version>")
            active_file = active / "index.md"
            active_file.write_text("<operaton.version>1.0.0</operaton.version>")

            import re
            reps = [uv.Replacement(
                "test",
                re.compile(r"(<operaton\.version>)\d+\.\d+\.\d+(</operaton\.version>)"),
                "2.2.0",
            )]

            # Temporarily patch DOCS_DIR and ARCHIVE_DIR
            orig_docs = uv.DOCS_DIR
            orig_archive = uv.ARCHIVE_DIR
            uv.DOCS_DIR = tmp_path / "docs"
            uv.ARCHIVE_DIR = tmp_path / "docs" / "get-started" / "archive"
            try:
                uv.update_docs(reps, dry_run=False)
            finally:
                uv.DOCS_DIR = orig_docs
                uv.ARCHIVE_DIR = orig_archive

            self.assertEqual(archive_file.read_text(), "<operaton.version>1.0.0</operaton.version>")
            self.assertEqual(active_file.read_text(), "<operaton.version>2.2.0</operaton.version>")
```

- [ ] **Step 3: Run tests and verify they pass**

```bash
cd .devenv/scripts && python3 -m pytest tests/test_update_versions.py -v
```

Expected output:
```
PASSED tests/test_update_versions.py::TestGetLatestRelease::test_strips_v_prefix
PASSED tests/test_update_versions.py::TestGetLatestRelease::test_strips_v_prefix_single_digit
PASSED tests/test_update_versions.py::TestGetVersionFromSbom::test_finds_existing_component
PASSED tests/test_update_versions.py::TestGetVersionFromSbom::test_returns_none_for_missing
PASSED tests/test_update_versions.py::TestGetVersionFromSbom::test_returns_none_for_none_sbom
PASSED tests/test_update_versions.py::TestResolveVersion::test_prefers_sbom
PASSED tests/test_update_versions.py::TestResolveVersion::test_falls_back_to_maven_central
PASSED tests/test_update_versions.py::TestApplyReplacements::test_replaces_operaton_version
PASSED tests/test_update_versions.py::TestApplyReplacements::test_no_change_when_already_current
PASSED tests/test_update_versions.py::TestApplyReplacements::test_skips_archive_directory
```

- [ ] **Step 4: Commit**

```bash
git add .devenv/scripts/update-versions.py .devenv/scripts/tests/test_update_versions.py
git commit -m "feat: implement Replacement dataclass and update_docs with archive exclusion"
```

---

## Task 6: Fix `main()` to use `_build_replacements` cleanly

**Files:**
- Modify: `.devenv/scripts/update-versions.py`

- [ ] **Step 1: Replace the `main()` function**

Replace the entire `main()` function with:

```python
THIRD_PARTY_ARTIFACTS = [
    ("slf4j-simple",          "org.slf4j",                    "slf4j-simple"),
    ("jakarta.xml.bind-api",  "jakarta.xml.bind",             "jakarta.xml.bind-api"),
    ("javax.servlet-api",     "javax.servlet",                "javax.servlet-api"),
    ("maven-compiler-plugin", "org.apache.maven.plugins",     "maven-compiler-plugin"),
    ("maven-war-plugin",      "org.apache.maven.plugins",     "maven-war-plugin"),
    ("bootstrap",             "org.webjars",                  "bootstrap"),
    ("uuid-creator",          "com.github.f4b6a3",            "uuid-creator"),
    ("logback-classic",       "ch.qos.logback",               "logback-classic"),
    ("spring-boot",           "org.springframework.boot",     "spring-boot-dependencies"),
]


def main(dry_run: bool = False) -> None:
    print("Fetching latest Operaton release…")
    release_data = _github_get(f"/repos/{REPO}/releases/latest")
    operaton_version = release_data["tag_name"].lstrip("v")
    print(f"Latest Operaton release: {operaton_version}")

    print("Fetching SBOM…")
    sbom = get_sbom(release_data)

    print("Resolving third-party versions…")
    third_party_versions: dict[str, str] = {}
    for key, group_id, artifact_id in THIRD_PARTY_ARTIFACTS:
        v = resolve_version(sbom, group_id, artifact_id)
        print(f"  {group_id}:{artifact_id} → {v}")
        third_party_versions[key] = v

    replacements = _build_replacements(operaton_version, third_party_versions)

    print(f"\nUpdating docs (dry_run={dry_run})…")
    changed = update_docs(replacements, dry_run=dry_run)
    print(f"\n{changed} file(s) {'would be ' if dry_run else ''}updated.")

    print("\nUpdating Spring Boot compatibility table…")
    sys.path.insert(0, str(SCRIPT_DIR))
    import update_spring_boot_version_table as sb
    sb.run(dry_run=dry_run)

    print("\nUpdating Quarkus compatibility table…")
    import update_quarkus_version_table as qk
    qk.run(dry_run=dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
```

- [ ] **Step 2: Run a dry-run to validate end-to-end wiring (requires GITHUB_TOKEN)**

```bash
GITHUB_TOKEN=$GITHUB_TOKEN python3 .devenv/scripts/update-versions.py --dry-run 2>&1 | head -60
```

Expected: prints latest Operaton version, resolved third-party versions, lists files that would be updated — no traceback.

- [ ] **Step 3: Verify tests still pass**

```bash
cd .devenv/scripts && python3 -m pytest tests/test_update_versions.py -v
```

Expected: all 10 tests PASS.

- [ ] **Step 4: Commit**

```bash
git add .devenv/scripts/update-versions.py
git commit -m "feat: wire main() with THIRD_PARTY_ARTIFACTS registry and module imports"
```

---

## Task 7: Update `maintenance.yml` workflow

**Files:**
- Modify: `.github/workflows/maintenance.yml`

- [ ] **Step 1: Replace the workflow content**

Replace the entire contents of `.github/workflows/maintenance.yml` with:

```yaml
name: Maintenance

on:
  schedule:
    - cron: '0 0 25 * *'
  workflow_dispatch:

jobs:
  update-versions:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v6

      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.11'

      - name: Update all versions
        run: python3 .devenv/scripts/update-versions.py
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Commit and push changes
        uses: EndBug/add-and-commit@v10
        with:
          message: 'docs: update version references'
          default_author: github_actions
```

- [ ] **Step 2: Validate YAML syntax**

```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/maintenance.yml'))" && echo "YAML OK"
```

Expected: `YAML OK`

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/maintenance.yml
git commit -m "chore: consolidate maintenance workflow to single update-versions script"
```

---

## Task 8: End-to-end dry-run validation

**Files:** none (read-only validation)

- [ ] **Step 1: Run full dry-run and verify all expected files appear**

```bash
GITHUB_TOKEN=$GITHUB_TOKEN python3 .devenv/scripts/update-versions.py --dry-run 2>&1
```

Expected output includes lines like:
```
Fetching latest Operaton release…
Latest Operaton release: X.Y.Z
Fetching SBOM…
Resolving third-party versions…
  org.slf4j:slf4j-simple → X.Y.Z
  ...
[dry-run] Would update docs/get-started/apache-maven.md: operaton-bom <version>
[dry-run] Would update docs/get-started/spring-boot/project-setup.md: <operaton.version> property, <spring-boot.version> property
[dry-run] Would update docs/get-started/quick-start/service-task.md: <operaton.external-task-client.version> property, slf4j-simple <version>, jakarta.xml.bind-api <version>
[dry-run] Would update docs/get-started/dmn/project-setup.md: <operaton.version> property, ...
[dry-run] Would update docs/documentation/user-guide/testing/index.md: ...
...
Updating Spring Boot compatibility table…
Updating Quarkus compatibility table…
Done.
```

- [ ] **Step 2: Verify archive directory is untouched**

```bash
GITHUB_TOKEN=$GITHUB_TOKEN python3 .devenv/scripts/update-versions.py --dry-run 2>&1 | grep "archive"
```

Expected: no output (no archive files listed).

- [ ] **Step 3: Run all tests one final time**

```bash
cd .devenv/scripts && python3 -m pytest tests/test_update_versions.py -v
```

Expected: all 10 tests PASS.

- [ ] **Step 4: Final commit if any cleanup was needed**

```bash
git status
# If clean, nothing to commit. If there are minor fixups:
git add -p
git commit -m "fix: dry-run validation corrections"
```
