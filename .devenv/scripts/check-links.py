#!/usr/bin/env python3
"""Check internal and external links in the Operaton documentation.

Phase 1 (`map`) collects every link in docs/**/*.md(x) with file and line and resolves internal
links to site URLs. Phase 2 (`check`) checks the URLs with lychee: internal ones against a static
docs server (`npm run serve`, or --serve to start one), external ones on the web.

Examples:
  .devenv/scripts/check-links.py map --out links.json
  .devenv/scripts/check-links.py check --serve
  .devenv/scripts/check-links.py check --scope internal --base-url http://localhost:3000
  .devenv/scripts/check-links.py check --scope external --files docs/documentation/index.md

Exit codes: 0 no broken links, 1 broken links, 2 setup or tool error.
"""
from __future__ import annotations

import argparse
import contextlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Set

sys.path.insert(0, str(Path(__file__).resolve().parent))
from linkcheck import extract, lychee, report, resolve, routes, server  # noqa: E402
from linkcheck.models import EXTERNAL, INTERNAL, SKIPPED, UNRESOLVED, ResolvedLink  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASE_URL = "http://localhost:3000"


def build_map(repo_root: Path, base_url: str) -> List[ResolvedLink]:
    links = extract.extract_files(repo_root, extract.iter_doc_files(repo_root / "docs"))
    return resolve.resolve_all(links, routes.load_routes(repo_root), base_url)


def select(resolved: List[ResolvedLink], scope: str, files: Optional[Set[str]]) -> List[ResolvedLink]:
    picked = []
    for r in resolved:
        if r.kind in (INTERNAL, UNRESOLVED) and scope in ("internal", "all"):
            picked.append(r)
        elif r.kind == EXTERNAL and scope in ("external", "all"):
            if files is None or r.link.file in files:
                picked.append(r)
    return picked


def _rel_files(repo_root: Path, paths: Optional[List[str]]) -> Optional[Set[str]]:
    if paths is None:
        return None
    root = repo_root.resolve()
    result = set()
    for p in paths:
        path = Path(p)
        path = path if path.is_absolute() else (Path.cwd() / path)
        try:
            result.add(path.resolve().relative_to(root).as_posix())
        except ValueError:
            result.add(Path(p).as_posix())
    return result


def _entry(r: ResolvedLink) -> dict:
    entry = {"file": r.link.file, "line": r.link.line, "raw": r.link.raw, "url": r.url}
    if r.reason:
        entry["reason"] = r.reason
    return entry


def cmd_map(args: argparse.Namespace) -> int:
    resolved = build_map(REPO_ROOT, args.base_url)
    groups = {kind: [_entry(r) for r in resolved if r.kind == kind]
              for kind in (INTERNAL, EXTERNAL, UNRESOLVED, SKIPPED)}
    text = json.dumps(groups, indent=2) + "\n"
    if args.out == "-":
        sys.stdout.write(text)
    else:
        Path(args.out).write_text(text, encoding="utf-8")
        print(", ".join(f"{k}: {len(v)}" for k, v in groups.items()), file=sys.stderr)
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    needs_server = args.scope in ("internal", "all")
    config = REPO_ROOT / "lychee.toml"
    with contextlib.ExitStack() as stack:
        base_url = args.base_url
        if needs_server and args.serve:
            base_url = stack.enter_context(server.docusaurus_server(REPO_ROOT, args.port, args.rebuild))
        resolved = build_map(REPO_ROOT, base_url)
        selected = select(resolved, args.scope, _rel_files(REPO_ROOT, args.files))
        internal_urls = sorted({r.url for r in selected if r.kind == INTERNAL})
        external_urls = sorted({r.url for r in selected if r.kind == EXTERNAL})
        if internal_urls and not args.serve:
            server.assert_static_server(base_url)
        tmp = Path(stack.enter_context(tempfile.TemporaryDirectory()))
        statuses = {}
        print(f"Checking {len(internal_urls)} internal URLs against {base_url} ...", file=sys.stderr)
        statuses.update(lychee.run_lychee(internal_urls, tmp / "internal", config=config,
                                          cache=False, cwd=REPO_ROOT))
        print(f"Checking {len(external_urls)} external URLs ...", file=sys.stderr)
        statuses.update(lychee.run_lychee(external_urls, tmp / "external", config=config,
                                          cache=True, cwd=REPO_ROOT))

    failures = report.collect_failures(selected, statuses)
    if failures:
        print(report.format_console(failures))
    if args.annotations and failures:
        print(report.format_annotations(failures))
    if args.report_md:
        md = report.format_markdown(
            failures, checked={"internal": len(internal_urls), "external": len(external_urls)},
            repo=args.repo, sha=args.sha, run_url=args.run_url, now=datetime.now(timezone.utc))
        Path(args.report_md).write_text(md, encoding="utf-8")
    print(f"{len(failures)} broken links.", file=sys.stderr)
    return 1 if failures else 0


def _default_run_url() -> Optional[str]:
    if os.environ.get("GITHUB_RUN_ID") and os.environ.get("GITHUB_REPOSITORY"):
        server_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
        return f"{server_url}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}"
    return None


def parse_args(argv: Optional[List[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_map = sub.add_parser("map", help="write the link map as JSON")
    p_map.add_argument("--out", default="-", help="output file, '-' for stdout (default)")
    p_map.add_argument("--base-url", default=DEFAULT_BASE_URL)
    p_map.set_defaults(func=cmd_map)

    p_check = sub.add_parser("check", help="check links and report broken ones")
    p_check.add_argument("--scope", choices=("internal", "external", "all"), default="all")
    p_check.add_argument("--files", nargs="*", default=None,
                         help="limit external links to these doc files (internal links stay complete)")
    p_check.add_argument("--base-url", default=DEFAULT_BASE_URL,
                         help="running static docs server (`npm run serve`), default %(default)s")
    p_check.add_argument("--serve", action="store_true", help="build if needed and start `npm run serve`")
    p_check.add_argument("--port", type=int, default=3000, help="port for --serve (default %(default)s)")
    p_check.add_argument("--rebuild", action="store_true", help="with --serve: always run `npm run build`")
    p_check.add_argument("--report-md", help="write a markdown report to this file")
    p_check.add_argument("--annotations", action="store_true", help="print GitHub ::error annotations")
    p_check.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", "operaton/documentation"))
    p_check.add_argument("--sha", default=os.environ.get("GITHUB_SHA", "main"))
    p_check.add_argument("--run-url", default=_default_run_url())
    p_check.set_defaults(func=cmd_check)
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    try:
        return args.func(args)
    except (routes.RoutesError, lychee.LycheeError, server.ServerError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
