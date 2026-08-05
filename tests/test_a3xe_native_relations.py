import json
import unittest
from pathlib import Path

from tools.a3xe_native_relations import A3XENativeRelationError, build_native_relations
from tools.a3xe_sqf_relations_converter import convert_capture_with_relations

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "fixtures" / "a3xe_sqf_capture_v0_1.json"


class A3XENativeRelationTests(unittest.TestCase):
    def test_known_relations_are_typed_and_sources_are_preserved(self):
        roots = {
            "CfgVehicles": {
                "VehicleBase": {"parent": None, "properties": {"weapons": ["Rifle"]}},
                "VehicleChild": {"parent": "VehicleBase", "properties": {}},
            },
            "CfgWeapons": {
                "Rifle": {"parent": None, "properties": {"magazines": ["Magazine"]}},
            },
            "CfgMagazines": {
                "Magazine": {"parent": None, "properties": {"ammo": "Bullet"}},
            },
            "CfgAmmo": {
                "Bullet": {"parent": None, "properties": {}},
            },
        }
        resolved = {
            "CfgVehicles": {
                "VehicleBase": {
                    "resolved": {"weapons": ["Rifle"]},
                    "sources": {"weapons": "VehicleBase"},
                },
                "VehicleChild": {
                    "resolved": {"weapons": ["Rifle"]},
                    "sources": {"weapons": "VehicleBase"},
                },
            },
            "CfgWeapons": {
                "Rifle": {
                    "resolved": {"magazines": ["Magazine"]},
                    "sources": {"magazines": "Rifle"},
                },
            },
            "CfgMagazines": {
                "Magazine": {
                    "resolved": {"ammo": "Bullet"},
                    "sources": {"ammo": "Magazine"},
                },
            },
            "CfgAmmo": {
                "Bullet": {"resolved": {}, "sources": {}},
            },
        }
        result = build_native_relations(roots, resolved)
        self.assertTrue(result["complete"])
        child = result["roots"]["CfgVehicles"]["VehicleChild"]
        self.assertEqual(child["parent"], "VehicleBase")
        self.assertEqual(
            result["roots"]["CfgVehicles"]["VehicleBase"]["children"],
            ["VehicleChild"],
        )
        weapon = child["outbound"]["weapons"][0]
        self.assertEqual(weapon["root"], "CfgWeapons")
        self.assertTrue(weapon["exists"])
        self.assertEqual(weapon["sourceClass"], "VehicleBase")

    def test_missing_target_is_reported_and_marks_result_incomplete(self):
        roots = {
            "CfgWeapons": {
                "Rifle": {"parent": None, "properties": {"magazines": ["Missing"]}},
            }
        }
        resolved = {
            "CfgWeapons": {
                "Rifle": {
                    "resolved": {"magazines": ["Missing"]},
                    "sources": {"magazines": "Rifle"},
                }
            }
        }
        result = build_native_relations(roots, resolved)
        self.assertFalse(result["complete"])
        self.assertEqual(result["missingTargets"][0]["targetRoot"], "CfgMagazines")
        self.assertFalse(
            result["roots"]["CfgWeapons"]["Rifle"]["outbound"]["magazines"][0]["exists"]
        )

    def test_invalid_relation_value_is_rejected(self):
        roots = {"CfgWeapons": {"Rifle": {"parent": None, "properties": {}}}}
        resolved = {
            "CfgWeapons": {
                "Rifle": {
                    "resolved": {"magazines": "not-an-array"},
                    "sources": {"magazines": "Rifle"},
                }
            }
        }
        with self.assertRaisesRegex(A3XENativeRelationError, "must be an array"):
            build_native_relations(roots, resolved)

    def test_sqf_converter_exposes_known_fields_contract(self):
        capture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        _, envelope = convert_capture_with_relations(capture)
        self.assertEqual(envelope["selection"]["relationMode"], "known_fields")
        self.assertTrue(envelope["nativeRelations"]["complete"])
        self.assertIn(capture["root"], envelope["nativeRelations"]["roots"])


if __name__ == "__main__":
    unittest.main()
