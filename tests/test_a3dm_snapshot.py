import unittest
from pathlib import Path

from tools.a3dm_snapshot import A3DMSnapshot, A3DMSnapshotError


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "a3dm_v0_1_example.json"


class A3DMSnapshotTests(unittest.TestCase):
    def load_snapshot(self):
        return A3DMSnapshot.from_file(FIXTURE)

    def test_metadata_and_root_access(self):
        snapshot = self.load_snapshot()
        self.assertEqual(snapshot.snapshot_id, "A3CDB_Test_Snapshot_01")
        self.assertEqual(snapshot.game_version, "A3CDB-Test-Game-1.0")
        self.assertIn("CfgVehicles", snapshot.roots)
        self.assertIn("A3CDB_Test_Soldier", snapshot.class_names("CfgVehicles"))

    def test_resolved_properties_follow_class_inheritance(self):
        snapshot = self.load_snapshot()
        properties = snapshot.resolved_properties("CfgVehicles", "A3CDB_Test_Soldier")
        self.assertEqual(properties["armor"], 20)
        self.assertEqual(properties["scope"], 2)
        self.assertEqual(properties["simulation"], "soldier")

    def test_data_is_immutable(self):
        snapshot = self.load_snapshot()
        class_data = snapshot.get_class("CfgVehicles", "A3CDB_Test_Soldier")
        with self.assertRaises(TypeError):
            class_data["parent"] = None
        with self.assertRaises(TypeError):
            class_data["properties"]["armor"] = 99

    def test_unknown_root_and_class_fail_closed(self):
        snapshot = self.load_snapshot()
        with self.assertRaises(A3DMSnapshotError):
            snapshot.class_names("CfgMissing")
        with self.assertRaises(A3DMSnapshotError):
            snapshot.get_class("CfgVehicles", "A3CDB_Test_Missing")


if __name__ == "__main__":
    unittest.main()
