import json
import unittest
from pathlib import Path

from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3ix_property import A3IXPropertyIndex, A3IXPropertyRef

FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "a3dm_v0_1_example.json"


class A3IXPropertyIndexTests(unittest.TestCase):
    def load_index(self):
        package = json.loads(FIXTURE.read_text(encoding="utf-8"))
        props = package["snapshot"]["roots"]["CfgVehicles"]["A3CDB_Test_Soldier"]["properties"]
        props["weapons"] = ["A3CDB_Test_Rifle"]
        props["magazines"] = ["A3CDB_Test_Magazine", "A3CDB_Test_Magazine"]
        props["turrets"] = [{"weapons": ["A3CDB_Test_TurretGun"]}]
        props["transportItems"] = [{"name": "A3CDB_Test_Bandage", "count": 4}]
        return A3IXPropertyIndex(A3DMSnapshot(package))

    def test_linked_items_contains_is_case_insensitive(self):
        index = self.load_index()
        expected = (A3IXPropertyRef("CfgVehicles", "A3CDB_Test_Soldier"),)
        self.assertEqual(index.contains("linkedItems", "a3cdb_test_helmet"), expected)

    def test_arrays_are_deduplicated_per_asset(self):
        index = self.load_index()
        self.assertEqual(len(index.contains("magazines", "A3CDB_Test_Magazine")), 1)

    def test_nested_objects_and_arrays_are_indexed(self):
        index = self.load_index()
        self.assertEqual(index.contains("turrets", "A3CDB_Test_TurretGun")[0].classname, "A3CDB_Test_Soldier")
        self.assertEqual(index.contains("transportItems", "A3CDB_Test_Bandage")[0].classname, "A3CDB_Test_Soldier")
        self.assertEqual(index.contains("transportItems", 4)[0].classname, "A3CDB_Test_Soldier")

    def test_root_filter_and_missing_path(self):
        index = self.load_index()
        self.assertEqual(index.contains("weapons", "A3CDB_Test_Rifle", root="CfgWeapons"), ())
        with self.assertRaises(KeyError):
            index.contains("unindexedProperty", "x")

    def test_index_metadata(self):
        index = self.load_index()
        self.assertEqual(index.snapshot_id, "A3CDB_Test_Snapshot_01")
        self.assertIn("linkedItems", index.property_paths)


if __name__ == "__main__":
    unittest.main()
