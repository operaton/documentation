Rem# Design: Automated Version Updates on Operaton Release

**Date:** 2026-05-29  
**Status:** Approved

## Overview

When `operaton/operaton` publishes a release, a workflow in this documentation repository should automatically update all version references in the active docs to reflect the latest release. This consolidates the existing Spring Boot and Quarkus compatibility table maintenance into a single script and workflow, and extends version tracking to Operaton Maven snippets and third-party dependencies.

## Architecture
3
Three parts:

1. **Master script** — `.devenv/scripts/update-versions.py` — orchestrates all version updates in a single run.
2. **Refactored modules** — existing `update-spring-boot-version-table.py` and `update-quarkus-version-table.py` gain a callable `run()` function so the master script can import them. Both remain runnable standalone.
3. **Updated workflow** — `.github/workflows/maintenance.yml` — calls only the master script. Triggered on the existing monthly schedule and via `workflow_dispatch` (no inputs).

The `operaton/operaton` release job triggers the workflow by calling the GitHub API `workflow_dispatch` endpoint targeting this repo. No inputs are passed; versions are auto-detected.

## Script Execution Order

1. Fetch latest Operaton release tag from GitHub API → derive version string (e.g. `2.2.0` from `v2.2.0`)
2. Download and parse the SBOM (CycloneDX JSON) attached to that release
3. For each tracked third-party artifact: look up version in SBOM first, fall back to Maven Central API
4. Update all active docs via targeted regex replacements (skipping `docs/get-started/archive/`)
5. Update Spring Boot compatibility table (calls refactored module)
6. Update Quarkus compatibility table (calls refactored module)

## Version Targets

### Operaton versions (sourced from latest GitHub release tag)

| Pattern in docs | Example current value |
|---|---|
| `<operaton.version>X</operaton.version>` | `1.0.0`, `2.1.0` |
| `<version>X</version>` after `operaton-bom` or `operaton-engine-dmn-bom` | `1.0.0` |
| `<version>X</version>` after `operaton-bpm-junit5` (testing doc) | `1.0.0` |
| `<operaton.external-task-client.version>X` | `2.1.0` |
| `github.com/operaton/operaton/tree/vX/` | `v2.1.0` |

### Third-party versions (SBOM-first, Maven Central fallback)

| Artifact | `groupId:artifactId` | Current value |
|---|---|---|
| SLF4J Simple | `org.slf4j:slf4j-simple` | `1.7.36` |
| Jakarta XML Bind API | `jakarta.xml.bind:jakarta.xml.bind-api` | `4.0.2` |
| Javax Servlet API | `javax.servlet:javax.servlet-api` | `3.0.1` |
| Maven Compiler Plugin | `org.apache.maven.plugins:maven-compiler-plugin` | `3.11.0` |
| Maven WAR Plugin | `org.apache.maven.plugins:maven-war-plugin` | `3.3.2` |
| Bootstrap (webjars) | `org.webjars:bootstrap` | `3.1.1` |
| UUID Creator | `com.github.f4b6a3:uuid-creator` | `3.1.2` |
| Logback Classic | `ch.qos.logback:logback-classic` | `1.1.2` |
| Spring Boot | `org.springframework.boot:spring-boot-dependencies` | `4.0.6` |

### Compatibility tables (delegated to existing modules)

- Spring Boot version compatibility table
- Quarkus version compatibility table

## Script Internals

**`update-versions.py`** key functions:

- `get_latest_operaton_release() -> str` — GitHub API `/repos/operaton/operaton/releases/latest`, strips `v` prefix from tag
- `get_sbom(tag: str) -> dict` — downloads CycloneDX JSON SBOM asset from the release (assumes CycloneDX JSON format; implementation must verify the asset name/media type in the actual release artifacts)
- `get_version_from_sbom(sbom, group_id, artifact_id) -> str | None` — looks up component by `groupId:artifactId`
- `get_version_from_maven_central(group_id, artifact_id) -> str` — queries `search.maven.org/solrsearch/select`
- `resolve_version(sbom, group_id, artifact_id) -> str` — SBOM first, Maven Central fallback
- `update_docs(replacements, dry_run)` — walks `.md` files under `docs/`, skips `docs/get-started/archive/`, applies regex substitutions
- `main(dry_run)` — orchestrates all of the above, then calls the two compatibility table modules

Each replacement is a dataclass: `(description, file_glob, pattern, replacement_fn)`.

**Dry-run mode** (`--dry-run`): prints what would change without writing files.

**Existing scripts** each gain a `run() -> None` function importable by the master script. The `if __name__ == "__main__"` block calls `run()` for standalone use.

## Updated Workflow

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
      - uses: actions/checkout@v6

      - uses: actions/setup-python@v6
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

## Exclusions

- `docs/get-started/archive/` — all version references stay pinned
- Project-internal snapshot versions (e.g. `0.0.1-SNAPSHOT`, `0.1-SNAPSHOT`) — never updated
- Namespace URIs and schema URLs (e.g. `http://operaton.org/schema/1.0/...`) — not version references
