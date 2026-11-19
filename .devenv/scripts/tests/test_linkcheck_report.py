import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from linkcheck.models import EXTERNAL, INTERNAL, SKIPPED, UNRESOLVED, Failure, Link, ResolvedLink
from linkcheck.report import (collect_failures, format_annotations, format_console, format_markdown,
                              format_text, link_type)

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


    def test_dot_segments_match(self):
        # lychee resolves "a/../b" to "b"
        link = rl(INTERNAL, "docs/a.md", 1, "../b", "http://localhost:3000/docs/a/../b/")
        self.assertEqual(len(collect_failures([link], {"http://localhost:3000/docs/b": "404"})), 1)

    def test_unmatched_status_still_fails(self):
        failures = collect_failures([OK], {"https://xn--bcher-kva.example/": "404"})
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0].resolved.link.line, 0)
        self.assertEqual(failures[0].resolved.url, "https://xn--bcher-kva.example/")


class TestUnmatchedFormat(unittest.TestCase):
    def setUp(self):
        self.failure = collect_failures([], {"https://x.org/": "404"})[0]

    def test_annotation_without_file(self):
        self.assertEqual(format_annotations([self.failure]),
                         "::error::Broken link https://x.org/ (source line unknown): 404")

    def test_markdown_without_blob_link(self):
        md = format_markdown([self.failure], checked={"internal": 0, "external": 1}, repo="o/d",
                             sha="s", run_url=None, now=NOW)
        self.assertNotIn("blob/s/", md)
        self.assertIn("| (source unknown) |  | https://x.org/ | 404 |", md)


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
        self.assertIn("Check links", md)
        self.assertNotIn("run summary", md)

    def test_truncation_keeps_every_section(self):
        internal = [Failure(rl(UNRESOLVED, "docs/a.md", i, f"x{i}.md", f"docs/x{i}.md", "unresolved-md"),
                            "unresolved-md") for i in range(1, 2001)]
        external = [Failure(rl(EXTERNAL, "docs/b.md", i, f"https://b.org/{i}", f"https://b.org/{i}"), "404")
                    for i in range(1, 6)]
        md = format_markdown(internal + external, checked={"internal": 2000, "external": 5}, repo="o/d",
                             sha="s", run_url=None, now=NOW, limit=8000)
        self.assertIn("### External", md)
        self.assertIn("https://b.org/5", md)
        self.assertLessEqual(len(md), 8200)


REST_PAGE = "https://docs.operaton.org/reference/latest/rest-api/#operation/getTask"
REST = ResolvedLink(Link("REST API GET /task", 0, "https://docs.operaton.org/manual/x/", source_url=REST_PAGE),
                    INTERNAL, "http://localhost:3000/manual/x/")


class TestRestApiSource(unittest.TestCase):
    def setUp(self):
        self.failure = Failure(REST, "404 Not Found")

    def test_markdown_links_to_rest_api_page(self):
        md = format_markdown([self.failure], checked={"internal": 1, "external": 0}, repo="o/d",
                             sha="s", run_url=None, now=NOW)
        self.assertIn(f"| [REST API GET /task]({REST_PAGE}) |  | https://docs.operaton.org/manual/x/ |", md)

    def test_annotation_without_file(self):
        self.assertEqual(format_annotations([self.failure]),
                         "::error::Broken link https://docs.operaton.org/manual/x/ in REST API GET /task: "
                         "404 Not Found")

    def test_console_without_line(self):
        self.assertTrue(format_console([self.failure]).startswith(
            "REST API GET /task  https://docs.operaton.org/manual/x/  404 Not Found"))


class TestLinkType(unittest.TestCase):
    def test_types(self):
        cases = [
            (Failure(UNR, "unresolved-md"), "Docs, internal: missing page"),
            (Failure(INT, "Cannot find fragment"), "Docs, internal: missing anchor"),
            (Failure(EXT, "Rejected status code: 404 Not Found"), "Docs, external: not found (404/410)"),
            (Failure(EXT, "Rejected status code: 410 Gone"), "Docs, external: not found (404/410)"),
            (Failure(EXT, "Rejected status code: 403 Forbidden"), "Docs, external: access denied (401/403)"),
            (Failure(EXT, "Timeout"), "Docs, external: timeout"),
            (Failure(EXT, "Network error: Connection failed"), "Docs, external: network error"),
            (Failure(EXT, "Rejected status code: 500 Internal Server Error"), "Docs, external: other error"),
            (Failure(REST, "404 Not Found"), "REST API, internal: not found (404/410)"),
        ]
        for failure, expected in cases:
            self.assertEqual(link_type(failure), expected, failure.status)


class TestFormatText(unittest.TestCase):
    def test_grouped_by_type(self):
        failures = [Failure(EXT, "Rejected status code: 404 Not Found"), Failure(UNR, "unresolved-md"),
                    Failure(REST, "Rejected status code: 404 Not Found"),
                    Failure(rl(EXTERNAL, "docs/z.md", 8, "https://z.org", "https://z.org"),
                            "Rejected status code: 404 Not Found")]
        text = format_text(failures, sha="abc123def4567", run_url="https://run", now=NOW)
        self.assertIn("4 broken links in 3 types", text)
        self.assertIn("2026-10-30 04:00 UTC, commit abc123def456, https://run", text)
        self.assertLess(text.index("== Docs, internal: missing page (1) =="),
                        text.index("== Docs, external: not found (404/410) (2) =="))
        self.assertLess(text.index("== Docs, external: not found (404/410) (2) =="),
                        text.index("== REST API, internal: not found (404/410) (1) =="))
        self.assertIn("docs/a.md:5  gone.md  [unresolved-md]", text)
        self.assertIn("docs/b.md:3  https://a.org  [Rejected status code: 404 Not Found]", text)
        self.assertIn(f"REST API GET /task  https://docs.operaton.org/manual/x/  "
                      f"[Rejected status code: 404 Not Found]  ({REST_PAGE})", text)

    def test_no_failures(self):
        self.assertIn("No broken links.", format_text([], sha="s", run_url=None, now=NOW))


if __name__ == "__main__":
    unittest.main()
