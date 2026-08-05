import unittest
from pathlib import Path

from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3ix_exact import A3IXAssetRef, A3IXExactIndex


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "a3dm_v0_1_example.json"


class A3IXExactIndexTests(unittest.TestCase):
    def load_index(self):
        snapshot = A3DMSnapshot.from_file(FIXTURE)
        return A3IXExactIndex(snapshot)

    def test_indexes_classname_and_root(self):
        index = self.load_index()
        self.assertEqual(
            index.exact("classname", "a3cdb_test_soldier"),
            (A3IXAssetRef("CfgVehicles", "A3CDB_Test_Soldier"),),
        )
        self.assertEqual(len(index.exact("root", "CfgVehicles")), 2)

    def test_indexes_resolved_inherited_properties(self):
        index = self.load_index()
        soldier = A3IXAssetRef("CfgVehicles", "A3CDB_Test_Soldier")
        self.assertTrue(index.contains_ref("author", "A3CDB Test Team", soldier))
        self.assertTrue(index.contains_ref("dlc", "a3cdb_test_dlc", soldier))
        self.assertTrue(index.contains_ref("faction", "A3CDB_TEST_FACTION", soldier))

    def test_indexes_display_name_parent_and_scope(self):
        index = self.load_index()
        self.assertEqual(
            index.exact("displayName", "A3CDB Test Rifleman"),
            (A3IXAssetRef("CfgVehicles", "A3CDB_Test_Soldier"),),
        )
        self.assertEqual(
            index.exact("parent", "A3CDB_Test_Man"),
            (A3IXAssetRef("CfgVehicles", "A3CDB_Test_Soldier"),),
        )
        self.assertEqual(len(index.exact("scope", 2)), 2)

    def test_root_filter_and_missing_values(self):
        index = self.load_index()
        self.assertEqual(len(index.exact("scope", 2, root="CfgWeapons")), 1)
        self.assertEqual(index.exact("displayName", "missing"), ())
        with self.assertRaises(KeyError):
            index.exact("armor", 20)

    def test_index_metadata_is_stable(self):
        index = self.load_index()
        self.assertEqual(index.snapshot_id, "A3CDB_Test_Snapshot_01")
        self.assertIn("classname", index.fields)
        self.assertGreater(index.count_keys("displayName"), 0)


if __name__ == "__main__":
    unittest.main()
