import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from linkcheck.models import Link
from linkcheck.openapi import SpecError, extract_spec, load_spec

PAGE = "https://docs.operaton.org/reference/latest/rest-api/"

SPEC = {
    "openapi": "3.0.2",
    "info": {
        "description": "See [Auth](https://docs.operaton.org/docs/auth/).",
        "license": {"name": "Apache", "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
    },
    "externalDocs": {"url": "https://docs.operaton.org/docs/rest/"},
    "servers": [{"url": "http://localhost:8080/engine-rest"}],
    "tags": [{"name": "Task", "description": "Tasks, see [errors](/reference/rest/overview/#error-handling)."}],
    "paths": {
        "/task/{id}": {
            "get": {
                "operationId": "getTask",
                "description": "Get a task.\n```\n[nope](in-code.md)\n```\n<a href=\"$(docsUrl)/x/\">x</a>",
                "parameters": [{"name": "id", "description": "The [id](#operation/getTasks)."}],
                "responses": {"200": {
                    "description": "OK",
                    "content": {"application/json": {
                        "example": {"description": "[ignored](https://example.org/)"},
                        "examples": {"a": {"value": {"description": "[ignored](https://ex.org/)"}}},
                    }},
                }},
            },
        },
    },
    "components": {"schemas": {"TaskDto": {"properties": {"name": {
        "description": "Name, see <https://en.wikipedia.org/wiki/Task>."}}}}},
}


class TestExtractSpec(unittest.TestCase):
    def setUp(self):
        self.links = extract_spec(SPEC, PAGE)

    def by_raw(self, raw):
        return next(link for link in self.links if link.raw == raw)

    def test_links_from_descriptions_and_doc_urls(self):
        self.assertEqual(sorted(link.raw for link in self.links), sorted([
            "https://docs.operaton.org/docs/auth/",
            "https://www.apache.org/licenses/LICENSE-2.0.html",
            "https://docs.operaton.org/docs/rest/",
            "https://docs.operaton.org/reference/rest/overview/#error-handling",
            "https://docs.operaton.org/reference/latest/rest-api/$(docsUrl)/x/",
            "https://docs.operaton.org/reference/latest/rest-api/#operation/getTasks",
            "https://en.wikipedia.org/wiki/Task",
        ]))

    def test_relative_links_resolve_against_the_page(self):
        self.assertTrue(all(link.raw.startswith("https://") for link in self.links))

    def test_operation_location_links_to_redoc_anchor(self):
        link = self.by_raw("https://docs.operaton.org/reference/latest/rest-api/#operation/getTasks")
        self.assertEqual(link.file, "REST API GET /task/{id} (parameters/0)")
        self.assertEqual(link.line, 0)
        self.assertEqual(link.source_url, PAGE + "#operation/getTask")

    def test_operation_description_location(self):
        link = self.by_raw("https://docs.operaton.org/reference/latest/rest-api/$(docsUrl)/x/")
        self.assertEqual(link.file, "REST API GET /task/{id}")

    def test_component_location_links_to_page(self):
        link = self.by_raw("https://en.wikipedia.org/wiki/Task")
        self.assertEqual(link.file, "REST API components/schemas/TaskDto/properties/name")
        self.assertEqual(link.source_url, PAGE)

    def test_tag_location(self):
        link = self.by_raw("https://docs.operaton.org/reference/rest/overview/#error-handling")
        self.assertEqual(link.file, "REST API tags/0")


class TestLoadSpec(unittest.TestCase):
    def test_local_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spec.json"
            path.write_text(json.dumps({"paths": {}}), encoding="utf-8")
            self.assertEqual(load_spec(str(path)), {"paths": {}})

    def test_missing_file_raises(self):
        with self.assertRaises(SpecError):
            load_spec("/nonexistent/spec.json")

    def test_invalid_json_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spec.json"
            path.write_text("<html>", encoding="utf-8")
            with self.assertRaises(SpecError):
                load_spec(str(path))


class TestLinkDefault(unittest.TestCase):
    def test_doc_links_have_no_source_url(self):
        self.assertEqual(Link("docs/a.md", 1, "x").source_url, "")


if __name__ == "__main__":
    unittest.main()
