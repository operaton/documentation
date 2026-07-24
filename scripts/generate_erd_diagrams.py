#!/usr/bin/env python3
"""Generate grouped 7.24 ER diagram SVGs from schema.mermaid.

Usage: python3 scripts/generate_erd_diagrams.py
Requires: npx (Node.js) available on PATH; @mermaid-js/mermaid-cli is
fetched on demand via `npx -y`, no separate install step needed.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from erd_schema import parse_schema, resolve_groups
from erd_build import extract_header, build_subdiagram

REPO_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "docs/documentation/reference/db-schema/schema.mermaid"
OUT_DIR = REPO_ROOT / "static/img/documentation/user-guide/process-engine/database"


def main():
    text = SCHEMA_PATH.read_text()
    entities, rels, classes = parse_schema(text)
    groups = resolve_groups(entities)
    init_line, classdef_lines = extract_header(text)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for group, tables in groups.items():
            mmd_content = build_subdiagram(tables, entities, rels, classes, init_line, classdef_lines)
            mmd_path = tmp_path / f"{group}.mmd"
            mmd_path.write_text(mmd_content)

            svg_path = OUT_DIR / f"erd_724_{group}.svg"
            result = subprocess.run(
                [
                    "npx", "-y", "@mermaid-js/mermaid-cli",
                    "-i", str(mmd_path),
                    "-o", str(svg_path),
                    "-b", "transparent",
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print(f"FAILED rendering group '{group}':\n{result.stderr}", file=sys.stderr)
                sys.exit(1)
            print(f"Generated {svg_path} ({len(tables)} tables)")


if __name__ == "__main__":
    main()
