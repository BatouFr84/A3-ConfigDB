import copy
import json
import unittest
from pathlib import Path

from tools.a3dm_validator import A3DMValidationError, validate_snapshot_package


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "a3dm_v0_1_example.json"


class A3DMValidatorTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_valid_snapshot_package(self):
        package = self.load_fixture()
        snapshot = validate_snapshot_package(package)
        self.assertEqual(snapshot["snapshotId"], "A3CDB_Test_Snapshot_01")
        self.assertIn("A3CDB_Test_Soldier", snapshot["roots"]["CfgVehicles"])
        self.assertEqual(package["manifest"]["loadedAddons"][1]["order"], 1)

    def test_snapshot_identity_mismatch_rejects(self):
        package = self.load_fixture()
        package["snapshot"]["snapshotId"] = "A3CDB_Test_Different"
        with self.assertRaises(A3DMValidationError):
            validate_snapshot_package(package)

    def test_non_contiguous_addon_order_rejects(self):
        package = self.load_fixture()
        package["manifest"]["loadedAddons"][1]["order"] = 3
        with self.assertRaises(A3DMValidationError):
            validate_snapshot_package(package)

    def test_missing_parent_rejects(self):
        package = self.load_fixture()
        package["snapshot"]["roots"]["CfgVehicles"]["A3CDB_Test_Soldier"]["parent"] = "A3CDB_Test_Missing"
        with self.assertRaises(A3DMValidationError):
            validate_snapshot_package(package)

    def test_inheritance_cycle_rejects(self):
        package = self.load_fixture()
        package["snapshot"]["roots"]["CfgVehicles"]["A3CDB_Test_Man"]["parent"] = "A3CDB_Test_Soldier"
        with self.assertRaises(A3DMValidationError):
            validate_snapshot_package(package)

    def test_artificial_source_flags_conflict_rejects(self):
        package = self.load_fixture()
        package["manifest"]["sourceGameDataIncluded"] = True
        with self.assertRaises(A3DMValidationError):
            validate_snapshot_package(package)


if __name__ == "__main__":
    unittest.main()
