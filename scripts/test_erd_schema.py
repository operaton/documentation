import unittest
from pathlib import Path
from erd_schema import parse_schema, resolve_groups

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


class TestResolveGroups(unittest.TestCase):
    def test_every_table_assigned_exactly_once(self):
        text = SCHEMA_PATH.read_text()
        entities, _, _ = parse_schema(text)
        groups = resolve_groups(entities)
        grouped = [t for tables in groups.values() for t in tables]
        self.assertEqual(len(grouped), len(set(grouped)), "table in multiple groups")
        self.assertEqual(set(grouped), set(entities.keys()))

    def test_group_sizes(self):
        text = SCHEMA_PATH.read_text()
        entities, _, _ = parse_schema(text)
        groups = resolve_groups(entities)
        self.assertEqual(len(groups["bpmn"]), 20)
        self.assertEqual(len(groups["dmn"]), 2)
        self.assertEqual(len(groups["cmmn"]), 3)
        self.assertEqual(len(groups["history"]), 18)
        self.assertEqual(len(groups["identity"]), 6)

    def test_raises_on_unassigned_table(self):
        entities = {"ACT_XX_UNKNOWN": "", "ACT_ID_GROUP": ""}
        with self.assertRaises(ValueError):
            resolve_groups(entities)


if __name__ == "__main__":
    unittest.main()
