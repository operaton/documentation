"""Map doc source files to their published permalinks via Docusaurus build metadata."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

METADATA_DIR = ".docusaurus/docusaurus-plugin-content-docs/default"


class RoutesError(Exception):
    pass


def load_routes(repo_root: Path) -> Dict[str, str]:
    """Return {"docs/...md": "/docs/..."} from the metadata written by `npm run build`."""
    meta_dir = repo_root / METADATA_DIR
    files = sorted(meta_dir.glob("site-docs-*.json"))
    if not files:
        raise RoutesError(f"No Docusaurus doc metadata in {meta_dir}. Run `npm run build` first.")
    routes: Dict[str, str] = {}
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        source = data.get("source", "")
        if source.startswith("@site/") and "permalink" in data:
            routes[source[len("@site/"):]] = data["permalink"]
    return routes
