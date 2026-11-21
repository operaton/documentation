#!/usr/bin/env python3
"""Update all version references in the documentation.

Fetches the latest Operaton release from GitHub, resolves third-party
dependency versions via the release SBOM (CycloneDX JSON) or Maven Central,
then performs regex-based replacements across all active docs.

Supported Tomcat/WildFly versions and links to the Tomcat, WildFly, Spring Boot
and Quarkus documentation on the pages in CONTAINER_DOC_FILES follow the
container versions of the release,
read from the version.* properties of its pom.xml and parent/pom.xml.
The supported databases list names at least the database versions the
release's CI tests with (database/pom.xml profiles).

SBOM: The distribution zip (operaton-bpm-X.Y.Z.zip) contains sbom.cdx.json
at its root. This file is extracted and parsed. Falls back to Maven Central
only if the zip or sbom.cdx.json cannot be found.

purl format in SBOM: pkg:maven/<groupId>/<artifactId>@<version>?type=jar
Matching uses prefix: pkg:maven/<groupId>/<artifactId>@

Usage:
    python3 .devenv/scripts/update_versions.py [--dry-run]

Environment variables:
    GITHUB_TOKEN   Optional GitHub personal-access token.
"""

import base64
import importlib.util
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
SUPERPOWERS_DIR = DOCS_DIR / "superpowers"


# ── GitHub API ────────────────────────────────────────────────────────────────

def _get_github_token() -> str:
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        return token
    try:
        import subprocess
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return ""


def _github_get(path: str) -> object:
    token = _get_github_token()
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


def get_latest_operaton_release() -> tuple[str, dict]:
    """Return (version_string, release_data) for the latest release.

    version_string has no 'v' prefix, e.g. '2.2.0'.
    release_data is the full GitHub API response (includes assets for SBOM).
    """
    data = _github_get(f"/repos/{REPO}/releases/latest")
    tag = data["tag_name"]
    version = tag.lstrip("v")
    return version, data


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

# The qualifier and its digits may be separated by another "-" (e.g.
# "4.0.0-beta-4", as seen on maven-compiler-plugin), not just attached
# directly (e.g. "2.1.0-alpha1") - both forms show up on Maven Central.
_PRE_RELEASE_RE = re.compile(
    r"(?i)[.-](alpha|beta|rc|m)[-.]?\d*(\..*)?$"
)


def _is_release_version(version: str) -> bool:
    return _PRE_RELEASE_RE.search(version) is None


def get_version_from_maven_central(group_id: str, artifact_id: str) -> str:
    """Return the latest stable release version for a Maven artifact from Maven Central."""
    params = f"q=g:{group_id}+AND+a:{artifact_id}&core=gav&rows=20&wt=json"
    url = f"{MAVEN_CENTRAL_SEARCH}?{params}"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        docs = data["response"]["docs"]
        if not docs:
            raise RuntimeError(f"No results from Maven Central for {group_id}:{artifact_id}")
        release_versions = [d["v"] for d in docs if _is_release_version(d["v"])]
        if not release_versions:
            raise RuntimeError(f"No stable release found on Maven Central for {group_id}:{artifact_id}")
        return release_versions[0]
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
    files = [f for f in sorted(DOCS_DIR.rglob("*.md"))
             if not f.is_relative_to(ARCHIVE_DIR) and not f.is_relative_to(SUPERPOWERS_DIR)]
    return update_files(files, replacements, dry_run=dry_run)


def update_files(files: list[Path], replacements: list["Replacement"], dry_run: bool = False) -> int:
    """Apply replacements to the given files. Returns count of changed files."""
    changed = 0
    for md_file in files:
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


# ── Container documentation links ─────────────────────────────────────────────

# Pages whose container versions and links to the Tomcat, WildFly, Spring Boot and Quarkus
# documentation follow the latest Operaton release. Other pages may name a version on purpose.
CONTAINER_DOC_FILES = [
    DOCS_DIR / "documentation" / "introduction" / "supported-environments.md",
    DOCS_DIR / "documentation" / "user-guide" / "security.md",
]

# (key, property in the Operaton root or parent pom.xml)
CONTAINER_POM_PROPERTIES = [
    ("tomcat",      "version.tomcat"),
    ("wildfly",     "version.wildfly"),
    ("spring-boot", "version.spring-boot"),
    ("quarkus",     "version.quarkus"),
]
OPERATON_POM_FILES = ("pom.xml", "parent/pom.xml")
_POM_PROPERTY_RE = re.compile(r"<(version\.[\w.-]+)>\s*([^<\s]+)\s*</\1>")


def parse_pom_properties(content: str) -> dict[str, str]:
    """Return the <version.*> properties of a pom.xml."""
    return {m.group(1): m.group(2) for m in _POM_PROPERTY_RE.finditer(content)}


def get_container_versions(tag: str) -> dict[str, str]:
    """Return the container versions of an Operaton release, read from its pom.xml files."""
    properties: dict[str, str] = {}
    for path in OPERATON_POM_FILES:
        data = _github_get(f"/repos/{REPO}/contents/{path}?ref={tag}")
        properties.update(parse_pom_properties(base64.b64decode(data["content"]).decode()))
    versions = {}
    for key, prop in CONTAINER_POM_PROPERTIES:
        if prop not in properties:
            raise RuntimeError(f"<{prop}> not found in {', '.join(OPERATON_POM_FILES)} at {tag}")
        versions[key] = properties[prop]
    return versions


def _major(version: str) -> str:
    return version.split(".")[0]


def _major_minor(version: str) -> str:
    return ".".join(version.split(".")[:2])


def _build_container_doc_replacements(versions: dict[str, str]) -> list["Replacement"]:
    """Supported container list items and version segments in documentation URLs."""
    return [
        Replacement("supported Tomcat version",
            re.compile(r"^(\* Apache Tomcat )\d+\.\d+([ \t]*)$", re.MULTILINE), _major_minor(versions["tomcat"])),
        Replacement("supported WildFly version",
            re.compile(r"^(\* WildFly Application Server )\d+([ \t]*)$", re.MULTILINE), _major(versions["wildfly"])),
        Replacement("Tomcat documentation link",
            re.compile(r"(tomcat\.apache\.org/tomcat-)\d+\.\d+(-doc/)"), _major_minor(versions["tomcat"])),
        Replacement("WildFly documentation link",
            re.compile(r"(docs\.wildfly\.org/)\d+(/)"), _major(versions["wildfly"])),
        Replacement("Spring Boot documentation link",
            re.compile(r"(docs\.spring\.io/spring-boot/)\d+\.\d+(?:\.\d+)?(/)"),
            _major_minor(versions["spring-boot"])),
        Replacement("Quarkus documentation link",
            re.compile(r"(quarkus\.io/version/)\d+\.\d+(/)"), _major_minor(versions["quarkus"])),
    ]


# ── Supported databases ───────────────────────────────────────────────────────

SUPPORTED_ENVIRONMENTS_FILE = DOCS_DIR / "documentation" / "introduction" / "supported-environments.md"
OPERATON_DATABASE_POM = "database/pom.xml"

# (key, database/pom.xml profile, list item prefix in the supported environments page).
# The list item must name the version the CI tests with; other versions listed stay.
DATABASE_PROFILES = [
    ("mysql",      "mysql",      r"MySQL"),
    ("mariadb",    "mariadb",    r"MariaDB"),
    ("oracle",     "oracle",     r"Oracle"),
    ("db2",        "db2",        r"IBM DB2"),
    ("postgresql", "postgresql", r"PostgreSQL"),
    ("sqlserver",  "sqlserver",  r"Microsoft SQL Server"),
]
# Oracle images are tagged with the internal major version; 23 is marketed as 26ai since 23.26.
ORACLE_RELEASE_NAMES = {23: "26ai"}
_PROFILE_RE = re.compile(r"<profile>\s*<id>([^<]+)</id>(.*?)</profile>", re.DOTALL)
_TC_URL_RE = re.compile(r"<database\.tc\.url>\s*operaton\w+:([^<\s]+)\s*</database\.tc\.url>")
_VERSION_LIST = r"\d[\w.]*(?: / \d[\w.]*)*"


def _database_version_label(key: str, tag: str) -> str:
    """Docs label of a testcontainers image tag, e.g. oracle 21-faststart → 21c, 23-faststart → 26ai."""
    version = re.match(r"[\d.]+", tag).group(0)
    if key == "oracle":
        major = int(_major(version))
        if major in ORACLE_RELEASE_NAMES:
            return ORACLE_RELEASE_NAMES[major]
        return f"{major}ai" if major >= 23 else f"{major}c"
    if key == "db2":
        return _major_minor(version)
    return version


def parse_database_versions(pom: str) -> dict[str, str]:
    """Database versions the CI tests with: testcontainers image tags of the profiles, and H2."""
    tags = {}
    for profile_id, body in _PROFILE_RE.findall(pom):
        m = _TC_URL_RE.search(body)
        if m:
            tags[profile_id.strip()] = m.group(1)
    versions = {}
    for key, profile, _ in DATABASE_PROFILES:
        if profile not in tags:
            raise RuntimeError(f"No <database.tc.url> in profile '{profile}' of {OPERATON_DATABASE_POM}")
        versions[key] = _database_version_label(key, tags[profile])
    h2 = parse_pom_properties(pom).get("version.h2")
    if not h2:
        raise RuntimeError(f"<version.h2> not found in {OPERATON_DATABASE_POM}")
    versions["h2"] = _major_minor(h2)
    return versions


def get_database_versions(tag: str) -> dict[str, str]:
    data = _github_get(f"/repos/{REPO}/contents/{OPERATON_DATABASE_POM}?ref={tag}")
    return parse_database_versions(base64.b64decode(data["content"]).decode())


def _version_key(label: str) -> tuple:
    return tuple(int(n) for n in re.findall(r"\d+", label))


def update_database_versions_text(text: str, versions: dict[str, str]) -> tuple[str, list[str]]:
    """Add the CI-tested version to each database list item; H2 (bundled driver) is replaced."""
    changes = []

    def ensure(match: re.Match, key: str) -> str:
        listed = match.group(2).split(" / ")
        if versions[key] in listed:
            return match.group(0)
        changes.append(f"{key} {versions[key]}")
        return match.group(1) + " / ".join(sorted(listed + [versions[key]], key=_version_key))

    for key, _, prefix in DATABASE_PROFILES:
        # Only list items whose versions end the line or precede a remark in parentheses.
        pattern = re.compile(rf"^(\* {prefix} +)({_VERSION_LIST})(?=[ \t]*(?:\(|$))", re.MULTILINE)
        text = pattern.sub(lambda m, k=key: ensure(m, k), text)

    def replace_h2(match: re.Match) -> str:
        if match.group(2) != versions["h2"]:
            changes.append(f"h2 {versions['h2']}")
        return match.group(1) + versions["h2"]

    text = re.sub(r"^(\* H2 +)(\d+\.\d+)", replace_h2, text, flags=re.MULTILINE)
    return text, changes


def update_supported_databases(versions: dict[str, str], dry_run: bool = False) -> bool:
    original = SUPPORTED_ENVIRONMENTS_FILE.read_text(encoding="utf-8")
    updated, changes = update_database_versions_text(original, versions)
    if updated == original:
        return False
    rel = SUPPORTED_ENVIRONMENTS_FILE.relative_to(REPO_ROOT)
    if dry_run:
        print(f"  [dry-run] Would update {rel}: {', '.join(changes)}")
    else:
        SUPPORTED_ENVIRONMENTS_FILE.write_text(updated, encoding="utf-8")
        print(f"  Updated {rel}: {', '.join(changes)}")
    return True


# ── Script Loading ────────────────────────────────────────────────────────────

def _load_script(name: str, path: Path) -> object:
    """Load a Python script as a module by file path (supports hyphenated filenames).

    Args:
        name: Module name (identifier for the module)
        path: Path to the .py file to load

    Returns:
        The loaded module object
    """
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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
    operaton_version, release_data = get_latest_operaton_release()
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

    print("\nResolving container versions…")
    container_versions = get_container_versions(release_data["tag_name"])
    for key, v in container_versions.items():
        print(f"  {key} → {v}")
    changed = update_files(CONTAINER_DOC_FILES, _build_container_doc_replacements(container_versions),
                           dry_run=dry_run)
    print(f"{changed} file(s) with container documentation links {'would be ' if dry_run else ''}updated.")

    print("\nResolving tested database versions…")
    database_versions = get_database_versions(release_data["tag_name"])
    for key, v in database_versions.items():
        print(f"  {key} → {v}")
    if not update_supported_databases(database_versions, dry_run=dry_run):
        print("Supported databases are up to date.")

    print("\nUpdating Spring Boot compatibility table…")
    sb = _load_script("update_spring_boot_version_table",
                      SCRIPT_DIR / "update-spring-boot-version-table.py")
    sb.run(dry_run=dry_run)

    print("\nUpdating Quarkus compatibility table…")
    qk = _load_script("update_quarkus_version_table",
                      SCRIPT_DIR / "update-quarkus-version-table.py")
    qk.run(dry_run=dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
