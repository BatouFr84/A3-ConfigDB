import copy
import json
import unittest
from pathlib import Path

from tools.a3xe_multi_root_converter import A3XEMultiRootError, convert_multi_root_capture

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "fixtures" / "a3xe_multi_root_capture_v0_1.json"


class A3XEMultiRootConverterTests(unittest.TestCase):
    def load_capture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_four_roots_are_emitted_in_one_snapshot(self):
        package, envelope = convert_multi_root_capture(self.load_capture())
        self.assertEqual(
            list(package["snapshot"]["roots"]),
            ["CfgAmmo", "CfgMagazines", "CfgVehicles", "CfgWeapons"],
        )
        self.assertEqual(envelope["progress"]["rootsTotal"], 4)
        self.assertEqual(envelope["progress"]["rootsComplete"], 4)
        self.assertEqual(envelope["progress"]["classesSerialized"], 6)

    def test_inheritance_and_resolved_properties_are_per_root(self):
        _, envelope = convert_multi_root_capture(self.load_capture())
        chain = envelope["inheritance"]["roots"]["CfgWeapons"]["A3CDB_Test_Weapon"]
        self.assertEqual(chain, ["A3CDB_Test_Weapon_Base", "A3CDB_Test_Weapon"])
        resolved = envelope["resolvedProperties"]["roots"]["CfgWeapons"]["A3CDB_Test_Weapon"]
        self.assertEqual(resolved["resolved"]["author"], "A3CDB")
        self.assertEqual(resolved["sources"]["author"], "A3CDB_Test_Weapon_Base")

    def test_cross_root_relations_are_complete(self):
        _, envelope = convert_multi_root_capture(self.load_capture())
        self.assertTrue(envelope["nativeRelations"]["complete"])
        self.assertEqual(envelope["nativeRelations"]["missingTargets"], [])
        weapon_rel = envelope["nativeRelations"]["roots"]["CfgWeapons"]["A3CDB_Test_Weapon"]
        self.assertTrue(weapon_rel["outbound"]["magazines"][0]["exists"])

    def test_missing_cross_root_target_is_reported_not_hidden(self):
        capture = copy.deepcopy(self.load_capture())
        capture["roots"]["CfgMagazines"][0]["properties"]["ammo"] = "Missing_Ammo"
        _, envelope = convert_multi_root_capture(capture)
        self.assertFalse(envelope["nativeRelations"]["complete"])
        self.assertEqual(
            envelope["nativeRelations"]["missingTargets"][0]["targetClass"],
            "Missing_Ammo",
        )

    def test_invalid_root_and_missing_parent_are_rejected(self):
        capture = copy.deepcopy(self.load_capture())
        capture["roots"]["CfgUnknown"] = []
        with self.assertRaisesRegex(A3XEMultiRootError, "unsupported root"):
            convert_multi_root_capture(capture)

        capture = copy.deepcopy(self.load_capture())
        capture["roots"]["CfgWeapons"][1]["parent"] = "Missing_Base"
        with self.assertRaisesRegex(A3XEMultiRootError, "missing parent"):
            convert_multi_root_capture(capture)


if __name__ == "__main__":
    unittest.main()
