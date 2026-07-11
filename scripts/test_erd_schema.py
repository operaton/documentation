import unittest
from pathlib import Path
from erd_schema import parse_schema

SCHEMA_PATH = Path(__file__).parent.parent / "docs/documentation/reference/db-schema/schema.mermaid"


class TestParseSchema(unittest.TestCase):
    def test_parses_all_entities(self):
        text = SCHEMA_PATH.read_text()
        entities, rels, classes = parse_schema(text)
        self.assertEqual(len(entities), 49)
        self.assertIn("ACT_ID_GROUP", entities)
        self.assertIn("varchar NAME_", entities["ACT_ID_GROUP"])

    def test_parses_relationships(self):
        text = SCHEMA_PATH.read_text()
        entities, rels, classes = parse_schema(text)
        self.assertEqual(len(rels), 50)
        self.assertIn(
            ("ACT_ID_MEMBERSHIP", "}o--||", "ACT_ID_GROUP", "GROUP_ID_"),
            rels,
        )

    def test_parses_classes(self):
        text = SCHEMA_PATH.read_text()
        entities, rels, classes = parse_schema(text)
        self.assertEqual(classes["ACT_ID_GROUP"], "id")
        self.assertEqual(classes["ACT_RU_EXECUTION"], "ru")


if __name__ == "__main__":
    unittest.main()
