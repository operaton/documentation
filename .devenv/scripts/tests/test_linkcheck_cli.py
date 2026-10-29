import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("check_links", SCRIPTS / "check-links.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)

from linkcheck.models import EXTERNAL, INTERNAL, Link, ResolvedLink  # noqa: E402
from linkcheck.routes import METADATA_DIR  # noqa: E402


def make_repo(tmp: Path):
    (tmp / "docs").mkdir()
    (tmp / "docs" / "a.md").write_text("[b](b.md)\n[x](https://x.org/)\n[g](gone.md)\n", encoding="utf-8")
    (tmp / "docs" / "b.md").write_text("[y](https://y.org/)\n", encoding="utf-8")
    meta = tmp / METADATA_DIR
    meta.mkdir(parents=True)
    for name in ("a", "b"):
        (meta / f"site-docs-{name}-md.json").write_text(
            json.dumps({"source": f"@site/docs/{name}.md", "permalink": f"/docs/{name}"}), encoding="utf-8")


class TestSelect(unittest.TestCase):
    def test_files_limit_external_only(self):
        i = ResolvedLink(Link("docs/a.md", 1, "b.md"), INTERNAL, "u1")
        e1 = ResolvedLink(Link("docs/a.md", 2, "https://x"), EXTERNAL, "https://x")
        e2 = ResolvedLink(Link("docs/b.md", 1, "https://y"), EXTERNAL, "https://y")
        self.assertEqual(cli.select([i, e1, e2], "all", {"docs/b.md"}), [i, e2])
        self.assertEqual(cli.select([i, e1, e2], "external", None), [e1, e2])
        self.assertEqual(cli.select([i, e1, e2], "internal", None), [i])


REST_SPEC = {"paths": {"/task": {"get": {
    "operationId": "getTasks",
    "description": "[docs](https://docs.operaton.org/docs/b) [old](/manual/x/) [ext](https://r.org/)"}}}}


class TestMain(unittest.TestCase):
    def run_main(self, tmp, argv, statuses, spec=None):
        out, err = io.StringIO(), io.StringIO()
        with patch.object(cli, "REPO_ROOT", tmp), \
             patch.object(cli.openapi, "load_spec", return_value=spec or {"paths": {}}) as load, \
             patch.object(cli.server, "assert_static_server"), \
             patch.object(cli.lychee, "run_lychee", side_effect=lambda urls, *a, **k: {
                 u: statuses[u] for u in urls if u in statuses}), \
             redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        self.load_spec = load
        return code, out.getvalue(), err.getvalue()

    def test_map_groups(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            code, out, _ = self.run_main(tmp, ["map"], {})
            data = json.loads(out)
            self.assertEqual(code, 0)
            self.assertEqual([e["url"] for e in data["internal"]], ["http://localhost:3000/docs/b"])
            self.assertEqual([e["line"] for e in data["external"]], [2, 1])
            self.assertEqual(data["unresolved"][0]["file"], "docs/a.md")

    def test_check_reports_and_exits_1(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            report = tmp / "report.md"
            code, out, _ = self.run_main(tmp, ["check", "--report-md", str(report), "--annotations",
                                               "--repo", "o/d", "--sha", "abc"],
                                         {"https://y.org/": "404 Not Found"})
            self.assertEqual(code, 1)
            self.assertIn("docs/a.md:3  gone.md  unresolved-md", out)
            self.assertIn("docs/b.md:1  https://y.org/  404 Not Found", out)
            self.assertIn("::error file=docs/b.md,line=1::", out)
            self.assertIn("**2 broken links**", report.read_text(encoding="utf-8"))

    def test_check_includes_rest_api_links(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            code, out, _ = self.run_main(tmp, ["check"], {
                "http://localhost:3000/manual/x/": "404 Not Found", "https://r.org/": "Timeout"}, REST_SPEC)
            self.assertEqual(code, 1)
            self.load_spec.assert_called_once_with(cli.openapi.DEFAULT_SPEC_URL)
            self.assertIn("REST API GET /task  https://docs.operaton.org/manual/x/  404 Not Found", out)
            self.assertIn("REST API GET /task  https://r.org/  Timeout", out)

    def test_rest_api_external_links_skipped_with_files(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            code, out, _ = self.run_main(tmp, ["check", "--files", "docs/b.md"],
                                         {"https://r.org/": "Timeout"}, REST_SPEC)
            self.assertNotIn("r.org", out)

    def test_no_rest_api(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            self.run_main(tmp, ["check", "--no-rest-api"], {}, REST_SPEC)
            self.load_spec.assert_not_called()

    def test_rest_api_spec_option(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            code, out, _ = self.run_main(tmp, ["map", "--rest-api-spec", "spec.json"], {}, REST_SPEC)
            self.load_spec.assert_called_once_with("spec.json")
            self.assertIn("REST API GET /task", out)

    def test_rest_api_spec_error_exits_2(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            with patch.object(cli.openapi, "load_spec", side_effect=cli.openapi.SpecError("cannot load x")), \
                 patch.object(cli, "REPO_ROOT", tmp), redirect_stdout(io.StringIO()), \
                 redirect_stderr(io.StringIO()) as err:
                code = cli.main(["check", "--scope", "internal"])
            self.assertEqual(code, 2)
            self.assertIn("cannot load x", err.getvalue())

    def test_report_txt_grouped_by_type(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            txt = tmp / "broken-links.txt"
            self.run_main(tmp, ["check", "--report-txt", str(txt)], {"https://y.org/": "404 Not Found"})
            text = txt.read_text(encoding="utf-8")
            self.assertIn("== Docs, internal: missing page (1) ==", text)
            self.assertIn("== Docs, external: not found (404/410) (1) ==", text)

    def test_report_txt_written_when_all_ok(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            (tmp / "docs" / "a.md").write_text("ok\n", encoding="utf-8")
            txt = tmp / "broken-links.txt"
            code, _, _ = self.run_main(tmp, ["check", "--report-txt", str(txt)], {})
            self.assertEqual(code, 0)
            self.assertIn("No broken links.", txt.read_text(encoding="utf-8"))

    def test_check_files_filter(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            code, out, _ = self.run_main(tmp, ["check", "--scope", "external", "--files", "docs/a.md"],
                                         {"https://y.org/": "404 Not Found"})
            self.assertEqual(code, 0)

    def test_internal_check_ignores_lychee_toml_excludes(self):
        # lychee.toml excludes sample hosts like 127.0.0.1; internal URLs must never hit those.
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            calls = []
            with patch.object(cli, "REPO_ROOT", tmp), \
                 patch.object(cli.server, "assert_static_server"), \
                 patch.object(cli.lychee, "run_lychee",
                              side_effect=lambda urls, *a, **k: calls.append((urls, k)) or {}), \
                 redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                cli.main(["check", "--base-url", "http://127.0.0.1:3000"])
            internal = [k for urls, k in calls if urls and urls[0].startswith("http://127.0.0.1")]
            external = [k for urls, k in calls if urls and not urls[0].startswith("http://127.0.0.1")]
            self.assertIsNone(internal[0]["config"])
            self.assertEqual(external[0]["config"], tmp / "lychee.toml")

    def test_unexpected_exception_exits_2(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            with patch.object(cli, "build_map", side_effect=RuntimeError("bug")):
                code, _, err = self.run_main(tmp, ["check"], {})
            self.assertEqual(code, 2)
            self.assertIn("bug", err)

    def test_summary_is_not_truncated_like_the_issue_report(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            (tmp / "docs" / "c.md").write_text("".join(f"[g](gone{i}.md)\n" for i in range(200)),
                                               encoding="utf-8")
            report, summary = tmp / "report.md", tmp / "summary.md"
            self.run_main(tmp, ["check", "--report-md", str(report), "--report-limit", "3000",
                                "--summary-md", str(summary)], {})
            self.assertIn("more broken links", report.read_text(encoding="utf-8"))
            self.assertNotIn("more broken links", summary.read_text(encoding="utf-8"))
            self.assertIn("gone199.md", summary.read_text(encoding="utf-8"))

    def test_serve_builds_unless_no_build(self):
        import contextlib

        seen = []

        @contextlib.contextmanager
        def fake_server(repo_root, port, build):
            seen.append(build)
            yield "http://localhost:3000"

        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            make_repo(tmp)
            with patch.object(cli.server, "docusaurus_server", fake_server):
                self.run_main(tmp, ["check", "--serve"], {})
                self.run_main(tmp, ["check", "--serve", "--no-build"], {})
        self.assertEqual(seen, [True, False])

    def test_setup_error_exits_2(self):
        with tempfile.TemporaryDirectory() as t:
            code, _, err = self.run_main(Path(t), ["check"], {})
            self.assertEqual(code, 2)
            self.assertIn("npm run build", err)


if __name__ == "__main__":
    unittest.main()
