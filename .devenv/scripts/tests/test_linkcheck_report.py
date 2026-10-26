import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from linkcheck.models import EXTERNAL, INTERNAL, SKIPPED, UNRESOLVED, Failure, Link, ResolvedLink
from linkcheck.report import collect_failures, format_annotations, format_console, format_markdown

NOW = datetime(2026, 10, 30, 4, 0, tzinfo=timezone.utc)


def rl(kind, file, line, raw, url, reason=""):
    return ResolvedLink(Link(file, line, raw), kind, url, reason)


EXT = rl(EXTERNAL, "docs/b.md", 3, "https://a.org", "https://a.org")
INT = rl(INTERNAL, "docs/c.md", 9, "x.md#y", "http://localhost:3000/docs/x#y")
OK = rl(EXTERNAL, "docs/a.md", 1, "https://ok.org/", "https://ok.org/")
UNR = rl(UNRESOLVED, "docs/a.md", 5, "gone.md", "docs/gone.md", "unresolved-md")
SKIP = rl(SKIPPED, "docs/a.md", 2, "mailto:x@y.z", "", "scheme")


class TestCollect(unittest.TestCase):
    def test_collect_sorts_and_matches_normalized(self):
        # lychee reports "https://a.org/" for our "https://a.org"
        statuses = {"https://a.org/": "404 Not Found", "http://localhost:3000/docs/x#y": "Cannot find fragment"}
        failures = collect_failures([EXT, INT, OK, UNR, SKIP], statuses)
        self.assertEqual([(f.resolved.link.file, f.status) for f in failures], [
            ("docs/a.md", "unresolved-md"),
            ("docs/c.md", "Cannot find fragment"),
            ("docs/b.md", "404 Not Found"),
        ])

    def test_same_url_reported_per_occurrence(self):
        other = rl(EXTERNAL, "docs/z.md", 4, "https://a.org", "https://a.org")
        failures = collect_failures([EXT, other], {"https://a.org": "404"})
        self.assertEqual(len(failures), 2)

    def test_percent_encoding_matches(self):
        link = rl(EXTERNAL, "docs/a.md", 1, "https://a.org/my page", "https://a.org/my page")
        self.assertEqual(len(collect_failures([link], {"https://a.org/my%20page": "404"})), 1)


class TestFormat(unittest.TestCase):
    def setUp(self):
        self.failures = [Failure(UNR, "unresolved-md"), Failure(EXT, "404 Not Found")]

    def test_console(self):
        out = format_console(self.failures)
        self.assertIn("docs/a.md:5  gone.md  unresolved-md", out)
        self.assertIn("docs/b.md:3  https://a.org  404 Not Found", out)

    def test_annotations_escape(self):
        f = Failure(rl(EXTERNAL, "docs/a,b.md", 2, "https://a.org/x", "https://a.org/x"), "50%\nfail")
        self.assertEqual(format_annotations([f]),
                         "::error file=docs/a%2Cb.md,line=2::Broken link https://a.org/x: 50%25%0Afail")

    def test_markdown(self):
        md = format_markdown(self.failures, checked={"internal": 10, "external": 5},
                             repo="operaton/documentation", sha="abc123",
                             run_url="https://github.com/operaton/documentation/actions/runs/1", now=NOW)
        self.assertIn("**2 broken links**", md)
        self.assertIn("### Internal", md)
        self.assertIn("### External", md)
        self.assertIn("| [docs/a.md](https://github.com/operaton/documentation/blob/abc123/docs/a.md#L5) | 5 | gone.md | unresolved-md |", md)
        self.assertIn("https://github.com/operaton/documentation/actions/runs/1", md)
        self.assertIn("2026-10-30 04:00 UTC", md)

    def test_markdown_escapes_pipe(self):
        f = Failure(rl(EXTERNAL, "docs/a.md", 1, "https://a.org/?x=a|b", "https://a.org/?x=a|b"), "404")
        md = format_markdown([f], checked={"internal": 0, "external": 1}, repo="o/d", sha="s",
                             run_url=None, now=NOW)
        self.assertIn("https://a.org/?x=a\\|b", md)

    def test_markdown_all_ok(self):
        md = format_markdown([], checked={"internal": 10, "external": 5}, repo="o/d", sha="s",
                             run_url=None, now=NOW)
        self.assertIn("No broken links", md)
        self.assertNotIn("###", md)

    def test_markdown_truncates(self):
        many = [Failure(rl(EXTERNAL, "docs/a.md", i, f"https://a.org/{i}", f"https://a.org/{i}"), "404")
                for i in range(1, 2001)]
        md = format_markdown(many, checked={"internal": 0, "external": 2000}, repo="o/d", sha="s",
                             run_url=None, now=NOW, limit=5000)
        self.assertLessEqual(len(md), 5200)
        self.assertRegex(md, r"\+\d+ more broken links")


if __name__ == "__main__":
    unittest.main()
