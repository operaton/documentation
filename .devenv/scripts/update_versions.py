#!/usr/bin/env python3
"""Update all version references in the documentation.

Fetches the latest Operaton release from GitHub, resolves third-party
dependency versions via the release SBOM (CycloneDX JSON) or Maven Central,
then performs regex-based replacements across all active docs.

SBOM: The distribution zip (operaton-bpm-X.Y.Z.zip) contains sbom.cdx.json
at its root. This file is extracted and parsed. Falls back to Maven Central
only if the zip or sbom.cdx.json cannot be found.

purl format in SBOM: pkg:maven/<groupId>/<artifactId>@<version>?type=jar
Matching uses prefix: pkg:maven/<groupId>/<artifactId>@

Usage:
    python3 .devenv/scripts/update-versions.py [--dry-run]

Environment variables:
    GITHUB_TOKEN   Optional GitHub personal-access token.
"""

import json
import os
import re
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

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

def get_sbom(release_data: dict) -> Optional[dict]:
    """Extract sbom.cdx.json from the distribution zip in release assets.

    The distribution zip is named operaton-bpm-X.Y.Z.zip. The SBOM is at
    sbom.cdx.json inside the zip root. Returns None if not found.

    Streams the zip to a temporary file to avoid loading large files into memory.
    """
    for asset in release_data.get("assets", []):
        name = asset.get("name", "")
        if name.startswith("operaton-bpm-") and name.endswith(".zip"):
            print(f"Downloading distribution zip for SBOM: {name}")
            token = os.environ.get("GITHUB_TOKEN", "")
            req = urllib.request.Request(asset["browser_download_url"])
            if token:
                req.add_header("Authorization", f"Bearer {token}")
            try:
                with urllib.request.urlopen(req) as resp, \
                     tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
                    shutil.copyfileobj(resp, tmp)
                    tmp_path = tmp.name
            except urllib.error.HTTPError as exc:
                print(f"Failed to download zip {name}: {exc.code} {exc.reason}", file=sys.stderr)
                return None
            try:
                with zipfile.ZipFile(tmp_path) as zf:
                    # sbom.cdx.json may be at root or inside a top-level directory
                    for entry in zf.namelist():
                        if entry.endswith("sbom.cdx.json"):
                            with zf.open(entry) as f:
                                return json.loads(f.read().decode())
                print("sbom.cdx.json not found inside zip — will use Maven Central only.")
            finally:
                os.unlink(tmp_path)
            return None
    print("No operaton-bpm-*.zip asset found — will use Maven Central only.")
    return None


def get_version_from_sbom(sbom: Optional[dict], group_id: str, artifact_id: str) -> Optional[str]:
    """Look up a component version in a CycloneDX SBOM by groupId:artifactId.

    Matches on purl prefix 'pkg:maven/<group_id>/<artifact_id>@'.
    The ?type=... suffix in actual purls is handled by prefix matching.
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
    params = f"q=g:{group_id}+AND+a:{artifact_id}&rows=1&wt=json"
    url = f"{MAVEN_CENTRAL_SEARCH}?{params}"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        docs = data["response"]["docs"]
        if not docs:
            raise RuntimeError(f"No results from Maven Central for {group_id}:{artifact_id}")
        return docs[0]["latestVersion"]
    except urllib.error.HTTPError as exc:
        print(f"Maven Central error for {group_id}:{artifact_id}: {exc.code}", file=sys.stderr)
        raise


def resolve_version(sbom: Optional[dict], group_id: str, artifact_id: str) -> str:
    """Return version from SBOM if present, else from Maven Central."""
    v = get_version_from_sbom(sbom, group_id, artifact_id)
    if v:
        return v
    return get_version_from_maven_central(group_id, artifact_id)


# ── Placeholder for doc replacement (Task 5) ─────────────────────────────────

@dataclass
class Replacement:
    description: str
    pattern: re.Pattern
    new_version: str


def _build_replacements(operaton_version: str, versions: dict) -> list:
    raise NotImplementedError("Implemented in Task 5")


def _apply_replacements_to_text(text: str, replacements: list) -> tuple:
    raise NotImplementedError("Implemented in Task 5")


def update_docs(replacements: list, dry_run: bool = False) -> int:
    raise NotImplementedError("Implemented in Task 5")


# ── Orchestration (Task 6) ────────────────────────────────────────────────────

def main(dry_run: bool = False) -> None:
    raise NotImplementedError("Implemented in Task 6")


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
