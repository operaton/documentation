import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))
from linkcheck import lychee
from linkcheck.lychee import LycheeError, build_input_html, normalize_url, parse_report

# Shape taken from lychee-bin/src/formatters/stats/response.rs and lychee-lib Status serializer.
REPORT = {
    "total": 4, "successful": 1, "errors": 2, "timeouts": 1,
    "success_map": {}, "excluded_map": {}, "suggestion_map": {}, "redirect_map": {},
    "error_map": {
        "/tmp/x/links.html": [
            {"url": "https://a.org/missing", "status": {"text": "404 Not Found", "code": 404}},
            {"url": "https://b.org/#nope", "status": {"text": "Cannot find fragment", "details": "nope"}},
        ]
    },
    "timeout_map": {
        "/tmp/x/links.html": [{"url": "https://slow.org/", "status": {"text": "Timeout", "details": None}}]
    },
}


class TestHelpers(unittest.TestCase):
    def test_parse_report(self):
        self.assertEqual(parse_report(REPORT), {
            "https://a.org/missing": "404 Not Found",
            "https://b.org/#nope": "Cannot find fragment",
            "https://slow.org/": "Timeout",
        })

    def test_parse_report_adds_code_when_missing_from_text(self):
        data = {"error_map": {"f": [{"url": "https://a.org/", "status": {"text": "Rejected", "code": 403}}]}}
        self.assertEqual(parse_report(data), {"https://a.org/": "403 Rejected"})

    def test_parse_report_accepts_legacy_fail_map(self):
        data = {"fail_map": {"f": [{"url": "https://a.org/", "status": {"text": "404 Not Found", "code": 404}}]}}
        self.assertEqual(parse_report(data), {"https://a.org/": "404 Not Found"})

    def test_normalize_url(self):
        self.assertEqual(normalize_url("https://a.org"), normalize_url("https://a.org/"))
        self.assertEqual(normalize_url("https://a.org/my%20page"), normalize_url("https://a.org/my page"))
        self.assertNotEqual(normalize_url("https://a.org/x#a"), normalize_url("https://a.org/x#b"))

    def test_input_html_escapes(self):
        html = build_input_html(['https://a.org/?q=1&r="2"'])
        self.assertIn('href="https://a.org/?q=1&amp;r=&quot;2&quot;"', html)


class TestRunLychee(unittest.TestCase):
    def fake_run(self, returncode, report=None):
        def run(cmd, **kwargs):
            if report is not None:
                out = Path(cmd[cmd.index("--output") + 1])
                out.write_text(json.dumps(report), encoding="utf-8")
            return subprocess.CompletedProcess(cmd, returncode, "", "boom")
        return run

    def call(self, **kw):
        with tempfile.TemporaryDirectory() as tmp:
            return lychee.run_lychee(["https://a.org/"], Path(tmp) / "w", config=None, cache=False,
                                     cwd=Path(tmp), **kw)

    @patch("linkcheck.lychee.shutil.which", return_value="/usr/bin/lychee")
    def test_exit_2_is_broken_links(self, _):
        with patch("linkcheck.lychee.subprocess.run", side_effect=self.fake_run(2, REPORT)):
            self.assertEqual(len(self.call()), 3)

    @patch("linkcheck.lychee.shutil.which", return_value="/usr/bin/lychee")
    def test_other_exit_raises(self, _):
        with patch("linkcheck.lychee.subprocess.run", side_effect=self.fake_run(1)):
            with self.assertRaises(LycheeError) as ctx:
                self.call()
            self.assertIn("boom", str(ctx.exception))

    @patch("linkcheck.lychee.shutil.which", return_value="/usr/bin/lychee")
    def test_unparsable_output_raises(self, _):
        with patch("linkcheck.lychee.subprocess.run", side_effect=self.fake_run(0)):
            with self.assertRaises(LycheeError):
                self.call()

    @patch("linkcheck.lychee.shutil.which", return_value=None)
    def test_missing_binary(self, _):
        with self.assertRaises(LycheeError) as ctx:
            self.call()
        self.assertIn("brew install lychee", str(ctx.exception))

    def test_no_urls_no_call(self):
        with patch("linkcheck.lychee.subprocess.run") as run:
            self.assertEqual(lychee.run_lychee([], Path("/nonexistent"), config=None, cache=False,
                                               cwd=Path(".")), {})
            run.assert_not_called()

    @patch("linkcheck.lychee.shutil.which", return_value="/usr/bin/lychee")
    def test_flags(self, _):
        seen = {}

        def run(cmd, **kwargs):
            seen["cmd"] = cmd
            return self.fake_run(0, {})(cmd, **kwargs)

        with tempfile.TemporaryDirectory() as tmp, patch("linkcheck.lychee.subprocess.run", side_effect=run):
            lychee.run_lychee(["https://a.org/"], Path(tmp), config=Path("lychee.toml"), cache=True, cwd=Path(tmp))
        cmd = seen["cmd"]
        for flag in ("--format", "json", "--no-progress", "--include-fragments", "--cache",
                     "--config", "lychee.toml"):
            self.assertIn(flag, cmd)
        self.assertTrue(cmd[-1].endswith("links.html"))


if __name__ == "__main__":
    unittest.main()
