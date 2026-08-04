import copy
import json
import unittest
from pathlib import Path

from tools.a3dm_validator import A3DMValidationError, validate_and_reconstruct


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "a3dm_v0_1_example.json"


class A3DMValidatorTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_valid_linear_chain_and_last_definition_wins(self):
        package = self.load_fixture()
        states = validate_and_reconstruct(package)
        soldier = states["P2_TEST"]["CfgVehicles"]["A3CDB_Test_Soldier"]
        self.assertEqual(soldier["properties"]["armor"], 30)
        self.assertIn("A3CDB_Test_Scout", states["P2_TEST"]["CfgVehicles"])

    def test_unknown_operation_rejects_complete_profile(self):
        package = self.load_fixture()
        package["profiles"]["P1_TEST"]["operations"].append(
            {"op": "removeProperty", "root": "CfgVehicles", "className": "A3CDB_Test_Soldier", "property": "armor"}
        )
        with self.assertRaises(A3DMValidationError):
            validate_and_reconstruct(package)

    def test_removing_parent_with_dependent_rejects(self):
        package = self.load_fixture()
        package["profiles"]["P1_TEST"]["operations"] = [
            {"op": "removeClass", "root": "CfgVehicles", "className": "A3CDB_Test_Man"}
        ]
        with self.assertRaises(A3DMValidationError):
            validate_and_reconstruct(package)

    def test_missing_parent_rejects(self):
        package = self.load_fixture()
        package["profiles"]["P1_TEST"]["operations"] = [
            {"op": "setParent", "root": "CfgVehicles", "className": "A3CDB_Test_Soldier", "parent": "A3CDB_Test_Missing"}
        ]
        with self.assertRaises(A3DMValidationError):
            validate_and_reconstruct(package)

    def test_profile_dependency_cycle_rejects(self):
        package = self.load_fixture()
        for entry in package["manifest"]["profiles"]:
            if entry["profileId"] == "P1_TEST":
                entry["baseProfileId"] = "P2_TEST"
        package["profiles"]["P1_TEST"]["baseProfileId"] = "P2_TEST"
        with self.assertRaises(A3DMValidationError):
            validate_and_reconstruct(package)


if __name__ == "__main__":
    unittest.main()
