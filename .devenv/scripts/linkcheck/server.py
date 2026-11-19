"""Find, start and stop the static docs server used for internal link checks."""
from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

PROBE_PATH = "/__linkcheck_probe_does_not_exist__"


class ServerError(Exception):
    pass


def probe(url: str, timeout: float = 3.0) -> Optional[int]:
    """HTTP status of a GET, or None when nothing answers."""
    # Ask for HTML like a browser (and lychee) does: SPA fallbacks only answer such requests.
    request = urllib.request.Request(url, headers={"Accept": "text/html,*/*;q=0.8"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except (urllib.error.URLError, OSError):
        return None


def assert_static_server(base_url: str) -> None:
    base = base_url.rstrip("/")
    if probe(base + "/") is None:
        raise ServerError(f"No server at {base}. Start it with `npm run build && npm run serve`, "
                          f"or pass --serve.")
    if probe(base + PROBE_PATH) == 200:
        raise ServerError(f"{base} answers 200 for unknown pages, so broken links would pass. "
                          f"This is likely the dev server (`npm start`). Use `npm run serve` instead.")


def wait_until_up(url: str, timeout_s: float = 60.0, interval_s: float = 0.5) -> bool:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if probe(url, timeout=interval_s * 2) is not None:
            return True
        time.sleep(interval_s)
    return False


def _stop(proc: subprocess.Popen) -> None:
    try:
        os.killpg(proc.pid, signal.SIGTERM)
        proc.wait(timeout=10)
    except ProcessLookupError:
        pass
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()


@contextmanager
def docusaurus_server(repo_root: Path, port: int, build: bool) -> Iterator[str]:
    """Build the site (always when `build`, else only if missing), serve it on `port`, yield its
    base URL, stop it afterwards."""
    base = f"http://localhost:{port}"
    for host in ("localhost", "127.0.0.1"):
        if probe(f"http://{host}:{port}/", timeout=1.0) is not None:
            raise ServerError(f"Port {port} is already in use. Stop that server, pick --port, "
                              f"or omit --serve to check against it.")
    if build or not (repo_root / "build").is_dir():
        try:
            # stdout carries the link report; keep build chatter on stderr.
            subprocess.run(["npm", "run", "build"], cwd=repo_root, check=True, stdout=sys.stderr)
        except (subprocess.CalledProcessError, OSError) as exc:
            raise ServerError(f"`npm run build` failed: {exc}") from exc
    proc = subprocess.Popen(
        ["npm", "run", "serve", "--", "--port", str(port), "--no-open"],
        cwd=repo_root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True,
    )
    try:
        if not wait_until_up(base + "/"):
            raise ServerError(f"Docs server did not come up on {base} within 60 s.")
        assert_static_server(base)
        yield base
    finally:
        _stop(proc)
