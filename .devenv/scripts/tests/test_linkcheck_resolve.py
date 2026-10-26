import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from linkcheck.models import EXTERNAL, INTERNAL, SKIPPED, UNRESOLVED, Link
from linkcheck.resolve import resolve_link
from linkcheck.routes import METADATA_DIR, RoutesError, load_routes

BASE = "http://localhost:3000"
ROUTES = {
    "docs/documentation/webapps/admin/index.md": "/docs/documentation/webapps/admin/",
    "docs/documentation/webapps/admin/users.md": "/docs/documentation/webapps/admin/users",
    "docs/documentation/user-guide/history.md": "/docs/documentation/user-guide/history",
    "docs/documentation/reference/cmmn11/migration/10-to-11.md":
        "/docs/documentation/reference/cmmn11/migration/to-11",
    "docs/get-started/index.md": "/docs/get-started/",
    "docs/get-started/apache-maven.md": "/docs/get-started/apache-maven",
}
SRC = "docs/documentation/webapps/admin/users.md"


def res(raw, file=SRC):
    r = resolve_link(Link(file, 7, raw), ROUTES, BASE)
    return r.kind, r.url


class TestLoadRoutes(unittest.TestCase):
    def test_reads_source_and_permalink(self):
        with tempfile.TemporaryDirectory() as tmp:
            meta = Path(tmp) / METADATA_DIR
            meta.mkdir(parents=True)
            (meta / "site-docs-a-md-123.json").write_text(json.dumps(
                {"source": "@site/docs/a.md", "permalink": "/docs/a"}), encoding="utf-8")
            (meta / "__plugin.json").write_text("{}", encoding="utf-8")
            self.assertEqual(load_routes(Path(tmp)), {"docs/a.md": "/docs/a"})

    def test_missing_metadata_raises_with_hint(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RoutesError) as ctx:
                load_routes(Path(tmp))
            self.assertIn("npm run build", str(ctx.exception))


class TestResolve(unittest.TestCase):
    def test_external(self):
        self.assertEqual(res("https://github.com/operaton"), (EXTERNAL, "https://github.com/operaton"))

    def test_prod_docs_url_becomes_internal(self):
        self.assertEqual(res("https://docs.operaton.org/docs/documentation/webapps/admin/#x"),
                         (INTERNAL, BASE + "/docs/documentation/webapps/admin/#x"))

    def test_prod_docs_url_host_case_insensitive(self):
        self.assertEqual(res("https://Docs.Operaton.org/docs/get-started/?q=1#x"),
                         (INTERNAL, BASE + "/docs/get-started/?q=1#x"))

    def test_prod_docs_url_with_explicit_port(self):
        self.assertEqual(res("https://docs.operaton.org:443/docs/get-started/"),
                         (INTERNAL, BASE + "/docs/get-started/"))

    def test_prod_docs_bare_host(self):
        self.assertEqual(res("https://docs.operaton.org"), (INTERNAL, BASE + "/"))

    def test_prod_reference_stays_external(self):
        url = "https://docs.operaton.org/reference/latest/javadoc/A.html"
        self.assertEqual(res(url), (EXTERNAL, url))

    def test_root_relative_reference_goes_to_prod(self):
        self.assertEqual(res("/reference/latest/rest-api"),
                         (EXTERNAL, "https://docs.operaton.org/reference/latest/rest-api"))

    def test_relative_md_with_fragment(self):
        self.assertEqual(res("../../user-guide/history.md#access-the-log"),
                         (INTERNAL, BASE + "/docs/documentation/user-guide/history#access-the-log"))

    def test_number_prefix_route(self):
        self.assertEqual(res("../../reference/cmmn11/migration/10-to-11.md"),
                         (INTERNAL, BASE + "/docs/documentation/reference/cmmn11/migration/to-11"))

    def test_sibling_index_md(self):
        self.assertEqual(res("./index.md"), (INTERNAL, BASE + "/docs/documentation/webapps/admin/"))

    def test_unknown_md_is_unresolved(self):
        r = resolve_link(Link(SRC, 7, "missing.md#a"), ROUTES, BASE)
        self.assertEqual((r.kind, r.url, r.reason),
                         (UNRESOLVED, "docs/documentation/webapps/admin/missing.md", "unresolved-md"))

    def test_root_relative_md_against_docs_dir(self):
        self.assertEqual(res("/get-started/apache-maven.md#operaton-dmn"),
                         (INTERNAL, BASE + "/docs/get-started/apache-maven#operaton-dmn"))

    def test_root_relative_md_against_site_root(self):
        self.assertEqual(res("/docs/get-started/index.md"), (INTERNAL, BASE + "/docs/get-started/"))

    def test_root_relative_unknown_md_is_unresolved(self):
        r = resolve_link(Link(SRC, 7, "/get-started/nope.md"), ROUTES, BASE)
        self.assertEqual((r.kind, r.url, r.reason), (UNRESOLVED, "docs/get-started/nope.md", "unresolved-md"))

    def test_root_relative_image(self):
        self.assertEqual(res("/img/a.png"), (INTERNAL, BASE + "/img/a.png"))

    def test_fragment_only(self):
        self.assertEqual(res("#section"), (INTERNAL, BASE + "/docs/documentation/webapps/admin/users#section"))

    def test_relative_non_md_uses_browser_semantics(self):
        self.assertEqual(res("../../user-guide/history/#glossary"),
                         (INTERNAL, BASE + "/docs/documentation/user-guide/history/#glossary"))

    def test_base_url_trailing_slash(self):
        r = resolve_link(Link(SRC, 1, "/img/a.png"), ROUTES, BASE + "/")
        self.assertEqual(r.url, BASE + "/img/a.png")

    def test_skipped_schemes(self):
        for raw in ("mailto:a@b.org", "tel:123", "javascript:void(0)", "ftp://x.org/f"):
            self.assertEqual(res(raw)[0], SKIPPED, raw)

    def test_fragment_in_unrouted_partial_skipped(self):
        r = resolve_link(Link("docs/documentation/_partial.md", 1, "#a"), ROUTES, BASE)
        self.assertEqual(r.kind, SKIPPED)

    def test_md_link_from_partial_resolves_against_partial_dir(self):
        r = resolve_link(Link("docs/documentation/user-guide/_p.md", 1, "history.md"), ROUTES, BASE)
        self.assertEqual((r.kind, r.url), (INTERNAL, BASE + "/docs/documentation/user-guide/history"))


if __name__ == "__main__":
    unittest.main()
