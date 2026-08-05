import json
import unittest
from pathlib import Path

from tools.a3xe_resolved_properties import (
    A3XEResolvedPropertyError,
    resolve_properties,
)
from tools.a3xe_sqf_resolved_converter import (
    convert_capture_with_resolved_properties,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "fixtures" / "a3xe_sqf_capture_v0_1.json"


class A3XEResolvedPropertyTests(unittest.TestCase):
    def test_local_and_resolved_values_are_separate(self):
        classes = {
            "Base": {
                "parent": None,
                "properties": {"scope": 1, "author": "Base Author"},
            },
            "Child": {
                "parent": "Base",
                "properties": {"scope": 2, "displayName": "Child"},
            },
        }
        result = resolve_properties(classes)
        self.assertEqual(result["Child"]["local"], {
            "displayName": "Child",
            "scope": 2,
        })
        self.assertEqual(result["Child"]["resolved"], {
            "author": "Base Author",
            "displayName": "Child",
            "scope": 2,
        })
        self.assertEqual(result["Child"]["sources"]["author"], "Base")
        self.assertEqual(result["Child"]["sources"]["scope"], "Child")

    def test_json_types_are_preserved(self):
        classes = {
            "Base": {
                "parent": None,
                "properties": {
                    "number": 3.5,
                    "flag": True,
                    "items": ["a", 2, False],
                    "nested": {"x": 1},
                    "empty": None,
                },
            }
        }
        resolved = resolve_properties(classes)["Base"]["resolved"]
        self.assertEqual(resolved["number"], 3.5)
        self.assertIs(resolved["flag"], True)
        self.assertEqual(resolved["items"], ["a", 2, False])
        self.assertEqual(resolved["nested"], {"x": 1})
        self.assertIsNone(resolved["empty"])

    def test_unsupported_value_is_rejected(self):
        with self.assertRaisesRegex(A3XEResolvedPropertyError, "unsupported property value"):
            resolve_properties({
                "Base": {"parent": None, "properties": {"bad": {1, 2}}}
            })

    def test_sqf_converter_exposes_resolved_properties(self):
        capture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        package, envelope = convert_capture_with_resolved_properties(capture)
        root = capture["root"]
        classes = package["snapshot"]["roots"][root]
        self.assertEqual(envelope["selection"]["propertyMode"], "local_and_resolved")
        self.assertTrue(envelope["resolvedProperties"]["complete"])
        self.assertEqual(
            set(envelope["resolvedProperties"]["classes"]),
            set(classes),
        )


if __name__ == "__main__":
    unittest.main()
