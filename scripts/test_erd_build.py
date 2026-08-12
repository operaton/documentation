import unittest
from pathlib import Path
from erd_schema import parse_schema
from erd_build import build_subdiagram, extract_header

SCHEMA_PATH = Path(__file__).parent.parent / "docs/documentation/reference/db-schema/schema.mermaid"


class TestExtractHeader(unittest.TestCase):
    def test_extract_header(self):
        text = SCHEMA_PATH.read_text()
        init_line, classdefs = extract_header(text)
        self.assertTrue(init_line.startswith("%%{init:"))
        self.assertEqual(len(classdefs), 6)
        self.assertTrue(all(l.strip().startswith("classDef") for l in classdefs))


class TestBuildSubdiagram(unittest.TestCase):
    def test_identity_subdiagram_contains_only_identity_tables(self):
        text = SCHEMA_PATH.read_text()
        entities, rels, classes = parse_schema(text)
        init_line, classdefs = extract_header(text)
        identity_tables = sorted(n for n in entities if n.startswith("ACT_ID_"))

        mmd = build_subdiagram(identity_tables, entities, rels, classes, init_line, classdefs)

        self.assertTrue(mmd.startswith("%%{init:"))
        self.assertIn("erDiagram", mmd)
        for t in identity_tables:
            self.assertIn(f"{t} {{", mmd)
        self.assertNotIn("ACT_RU_EXECUTION", mmd)
        # relationship internal to identity group must be present
        self.assertIn('ACT_ID_MEMBERSHIP }o--|| ACT_ID_GROUP : "GROUP_ID_"', mmd)
        # relationship crossing group boundary must be absent
        self.assertNotIn("ACT_RE_PROCDEF", mmd)

    def test_no_cross_group_relationship_leaks(self):
        text = SCHEMA_PATH.read_text()
        entities, rels, classes = parse_schema(text)
        init_line, classdefs = extract_header(text)
        dmn_tables = ["ACT_RE_DECISION_DEF", "ACT_RE_DECISION_REQ_DEF"]

        mmd = build_subdiagram(dmn_tables, entities, rels, classes, init_line, classdefs)
        # DEC_REQ_ID_ relationship is internal to DMN tables, must be present
        self.assertIn("ACT_RE_DECISION_DEF", mmd)
        self.assertIn("ACT_RE_DECISION_REQ_DEF", mmd)
        # no other tables leak in
        self.assertNotIn("ACT_HI_", mmd)


if __name__ == "__main__":
    unittest.main()
