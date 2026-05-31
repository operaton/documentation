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
            re.compile(r"(<artifactId>slf4j-simple</artifactId>\s*<version>)\d+(?:\.\d+)+(</version>)", re.DOTALL),
            versions["slf4j-simple"]),
        Replacement("jakarta.xml.bind-api <version>",
            re.compile(r"(<artifactId>jakarta\.xml\.bind-api</artifactId>\s*<version>)\d+(?:\.\d+)+(</version>)", re.DOTALL),
            versions["jakarta.xml.bind-api"]),
        Replacement("javax.servlet-api <version>",
            re.compile(r"(<artifactId>javax\.servlet-api</artifactId>\s*<version>)\d+(?:\.\d+)+(</version>)", re.DOTALL),
            versions["javax.servlet-api"]),
        Replacement("maven-compiler-plugin <version>",
            re.compile(r"(<artifactId>maven-compiler-plugin</artifactId>\s*<version>)\d+(?:\.\d+)+(</version>)", re.DOTALL),
            versions["maven-compiler-plugin"]),
        Replacement("maven-war-plugin <version>",
            re.compile(r"(<artifactId>maven-war-plugin</artifactId>\s*<version>)\d+(?:\.\d+)+(</version>)", re.DOTALL),
            versions["maven-war-plugin"]),
        Replacement("bootstrap webjars <version>",
            re.compile(r"(<artifactId>bootstrap</artifactId>\s*<version>)\d+(?:\.\d+)+(</version>)", re.DOTALL),
            versions["bootstrap"]),
        Replacement("uuid-creator <version>",
            re.compile(r"(<artifactId>uuid-creator</artifactId>\s*<version>)\d+(?:\.\d+)+(</version>)", re.DOTALL),
            versions["uuid-creator"]),
        Replacement("logback-classic <version>",
            re.compile(r"(<artifactId>logback-classic</artifactId>\s*<version>)\d+(?:\.\d+)+(</version>)", re.DOTALL),
            versions["logback-classic"]),
        Replacement("<spring-boot.version> property",
            re.compile(r"(<spring-boot\.version>)\d+(?:\.\d+)+(</spring-boot\.version>)"),
            versions["spring-boot"]),
    ]


def _apply_replacements_to_text(text: str, replacements: list["Replacement"]) -> tuple[str, list[str]]:
    """Apply all replacements to text. Returns (new_text, list_of_descriptions_that_changed)."""
    changes = []
    for rep in replacements:
        new_text = rep.pattern.sub(lambda m, v=rep.new_version: m.group(1) + v + m.group(2), text)
        if new_text != text:
            changes.append(rep.description)
            text = new_text
    return text, changes


def update_docs(replacements: list["Replacement"], dry_run: bool = False) -> int:
    """Walk active docs, apply replacements. Returns count of changed files."""
    changed = 0
    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        if md_file.is_relative_to(ARCHIVE_DIR):
            continue
        original = md_file.read_text(encoding="utf-8")
        updated, changes = _apply_replacements_to_text(original, replacements)
        if updated != original:
            changed += 1
            try:
                rel = md_file.relative_to(REPO_ROOT)
            except ValueError:
                rel = md_file
            if dry_run:
                print(f"  [dry-run] Would update {rel}: {', '.join(changes)}")
            else:
                md_file.write_text(updated, encoding="utf-8")
                print(f"  Updated {rel}: {', '.join(changes)}")
    return changed


# ── Orchestration (Task 6) ────────────────────────────────────────────────────

THIRD_PARTY_ARTIFACTS = [
    ("slf4j-simple",          "org.slf4j",                "slf4j-simple"),
    ("jakarta.xml.bind-api",  "jakarta.xml.bind",         "jakarta.xml.bind-api"),
    ("javax.servlet-api",     "javax.servlet",            "javax.servlet-api"),
    ("maven-compiler-plugin", "org.apache.maven.plugins", "maven-compiler-plugin"),
    ("maven-war-plugin",      "org.apache.maven.plugins", "maven-war-plugin"),
    ("bootstrap",             "org.webjars",              "bootstrap"),
    ("uuid-creator",          "com.github.f4b6a3",        "uuid-creator"),
    ("logback-classic",       "ch.qos.logback",           "logback-classic"),
    ("spring-boot",           "org.springframework.boot", "spring-boot"),
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
