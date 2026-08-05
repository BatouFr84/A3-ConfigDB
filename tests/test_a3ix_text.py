import unittest
from pathlib import Path

from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3ix_text import A3IXTextIndex, TEXT_INDEXED_FIELDS
from tools.a3qe import A3QEEngine, A3QEFilter, A3QEQuery


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "a3dm_v0_1_example.json"


class A3IXTextIndexTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = A3DMSnapshot.from_file(FIXTURE)
        self.index = A3IXTextIndex(self.snapshot)

    def test_fields_are_explicit_and_stable(self):
        self.assertEqual(
            TEXT_INDEXED_FIELDS,
            ("classname", "displayName", "author", "faction", "dlc"),
        )
        self.assertEqual(self.index.fields, TEXT_INDEXED_FIELDS)

    def test_classname_substring_search_is_case_insensitive(self):
        results = self.index.contains("classname", "rif")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].root, "CfgWeapons")
        self.assertEqual(results[0].classname, "A3CDB_Test_Rifle")

    def test_display_name_substring_search_is_case_insensitive(self):
        results = self.index.contains("displayName", "test rifle")
        self.assertEqual(
            [item.classname for item in results],
            ["A3CDB_Test_Soldier", "A3CDB_Test_Rifle"],
        )

    def test_root_filter_is_applied_without_partial_results(self):
        self.assertEqual(self.index.contains("classname", "test", root="CfgMagazines"), ())

    def test_unknown_field_is_rejected(self):
        with self.assertRaisesRegex(KeyError, "field is not text indexed"):
            self.index.contains("scope", "2")

    def test_a3qe_routes_text_contains_to_text_index(self):
        engine = A3QEEngine(self.snapshot)
        results = engine.execute(A3QEQuery(
            root="CfgWeapons",
            filters=(A3QEFilter("classname", "contains", "rif"),),
            limit=10,
        ))
        self.assertEqual([item.classname for item in results], ["A3CDB_Test_Rifle"])


if __name__ == "__main__":
    unittest.main()
