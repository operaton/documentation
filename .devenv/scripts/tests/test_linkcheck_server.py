import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from linkcheck.server import ServerError, assert_static_server, docusaurus_server, probe


def make_handler(unknown_status):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200 if self.path == "/" else unknown_status)
            self.end_headers()

        def log_message(self, *args):
            pass
    return Handler


class HtmlFallbackHandler(BaseHTTPRequestHandler):
    """Like the Docusaurus dev server: unknown paths answer 200 only to requests accepting HTML."""
    def do_GET(self):
        html = "text/html" in self.headers.get("Accept", "")
        self.send_response(200 if self.path == "/" or html else 404)
        self.end_headers()

    def log_message(self, *args):
        pass


class LocalServer:
    def __init__(self, unknown_status, handler=None):
        self.httpd = HTTPServer(("127.0.0.1", 0), handler or make_handler(unknown_status))
        self.url = f"http://127.0.0.1:{self.httpd.server_port}"
        self.port = self.httpd.server_port

    def __enter__(self):
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        return self

    def __exit__(self, *exc):
        self.httpd.shutdown()
        self.httpd.server_close()


class TestServer(unittest.TestCase):
    def test_probe_unreachable(self):
        self.assertIsNone(probe("http://127.0.0.1:9", timeout=0.5))

    def test_probe_status(self):
        with LocalServer(404) as s:
            self.assertEqual(probe(s.url + "/"), 200)
            self.assertEqual(probe(s.url + "/nope"), 404)

    def test_static_server_accepted(self):
        with LocalServer(404) as s:
            assert_static_server(s.url)

    def test_no_server_has_hint(self):
        with self.assertRaises(ServerError) as ctx:
            assert_static_server("http://127.0.0.1:9")
        self.assertIn("npm run serve", str(ctx.exception))

    def test_spa_server_rejected(self):
        with LocalServer(200) as s:
            with self.assertRaises(ServerError) as ctx:
                assert_static_server(s.url)
            self.assertIn("npm start", str(ctx.exception))

    def test_html_only_fallback_server_rejected(self):
        with LocalServer(None, HtmlFallbackHandler) as s:
            with self.assertRaises(ServerError):
                assert_static_server(s.url)

    def serve_with_fake_processes(self, build, build_dir_exists):
        with tempfile.TemporaryDirectory() as tmp, \
             patch("linkcheck.server.probe", return_value=None), \
             patch("linkcheck.server.wait_until_up", return_value=True), \
             patch("linkcheck.server.assert_static_server"), \
             patch("linkcheck.server._stop"), \
             patch("linkcheck.server.subprocess.Popen"), \
             patch("linkcheck.server.subprocess.run") as run:
            if build_dir_exists:
                (Path(tmp) / "build").mkdir()
            with docusaurus_server(Path(tmp), 3999, build=build):
                pass
        return run

    def test_build_output_goes_to_stderr(self):
        run = self.serve_with_fake_processes(build=True, build_dir_exists=False)
        self.assertIs(run.call_args.kwargs.get("stdout"), sys.stderr)

    def test_build_runs_even_when_build_dir_exists(self):
        run = self.serve_with_fake_processes(build=True, build_dir_exists=True)
        run.assert_called_once()

    def test_no_build_reuses_existing_build(self):
        run = self.serve_with_fake_processes(build=False, build_dir_exists=True)
        run.assert_not_called()

    def test_no_build_still_builds_when_missing(self):
        run = self.serve_with_fake_processes(build=False, build_dir_exists=False)
        run.assert_called_once()

    def test_serve_refuses_busy_port(self):
        with LocalServer(404) as s:
            with self.assertRaises(ServerError) as ctx:
                with docusaurus_server(Path("."), s.port, build=False):
                    pass
            self.assertIn("in use", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
