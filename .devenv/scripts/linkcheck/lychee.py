"""Run lychee on a list of URLs and parse its JSON report."""
from __future__ import annotations

import html
import json
import posixpath
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Iterable, List, Optional
from urllib.parse import unquote, urlsplit, urlunsplit

FAILURE_MAPS = ("error_map", "timeout_map", "fail_map")  # fail_map: older lychee versions
LYCHEE_OK = 0
LYCHEE_BROKEN = 2


class LycheeError(Exception):
    pass


def normalize_url(url: str) -> str:
    """Key used to match lychee's (normalized) URLs back to ours."""
    parts = urlsplit(unquote(url.strip()))
    path = posixpath.normpath(parts.path) if parts.path else ""  # lychee resolves "a/../b"
    path = path.rstrip("/")
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, parts.fragment))


def build_input_html(urls: Iterable[str]) -> str:
    """An HTML page with one anchor per URL.

    lychee crawls URLs passed as inputs, so the URLs are handed over as links inside a file.
    """
    rows = "".join(f'<a href="{html.escape(u, quote=True)}">{i}</a>\n' for i, u in enumerate(urls))
    return f"<!doctype html>\n<html><body>\n{rows}</body></html>\n"


def _status_label(status: dict) -> str:
    text = str(status.get("text") or "error")
    code = status.get("code")
    if code is not None and str(code) not in text:
        return f"{code} {text}"
    return text


def parse_report(data: dict) -> Dict[str, str]:
    failures: Dict[str, str] = {}
    for key in FAILURE_MAPS:
        for entries in (data.get(key) or {}).values():
            for entry in entries:
                failures[entry["url"]] = _status_label(entry.get("status") or {})
    return failures


def run_lychee(urls: List[str], workdir: Path, *, config: Optional[Path], cache: bool,
               cwd: Path) -> Dict[str, str]:
    """Check URLs; return {url: status} for failing ones."""
    if not urls:
        return {}
    if shutil.which("lychee") is None:
        raise LycheeError("lychee not found. Install it: `brew install lychee` "
                          "(see https://lychee.cli.rs/installation/).")
    workdir.mkdir(parents=True, exist_ok=True)
    source = workdir / "links.html"
    output = workdir / "lychee.json"
    source.write_text(build_input_html(urls), encoding="utf-8")
    cmd = ["lychee", "--format", "json", "--output", str(output), "--no-progress", "--include-fragments"]
    if config is not None:
        cmd += ["--config", str(config)]
    if cache:
        cmd += ["--cache"]
    cmd.append(str(source))
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if proc.returncode not in (LYCHEE_OK, LYCHEE_BROKEN):
        raise LycheeError(f"lychee failed (exit {proc.returncode}):\n{proc.stderr.strip()}")
    try:
        data = json.loads(output.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise LycheeError(f"Cannot read lychee report {output}: {exc}\n{proc.stderr.strip()}") from exc
    return parse_report(data)
