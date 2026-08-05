import copy
import json
import unittest
from pathlib import Path

from tools.a3xe_inheritance import A3XEInheritanceError, build_inheritance_chains
from tools.a3xe_sqf_capture_converter import A3XESQFCaptureError
from tools.a3xe_sqf_inheritance_converter import convert_capture_with_inheritance

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "fixtures" / "a3xe_sqf_capture_v0_1.json"


class A3XEInheritanceTests(unittest.TestCase):
    def test_root_to_class_chains_are_deterministic(self):
        classes = {
            "C": {"parent": "B"},
            "A": {"parent": None},
            "B": {"parent": "A"},
        }
        self.assertEqual(build_inheritance_chains(classes), {
            "A": ["A"],
            "B": ["A", "B"],
            "C": ["A", "B", "C"],
        })

    def test_missing_parent_is_rejected(self):
        with self.assertRaisesRegex(A3XEInheritanceError, "missing parent"):
            build_inheritance_chains({"Child": {"parent": "Missing"}})

    def test_cycle_is_rejected(self):
        with self.assertRaisesRegex(A3XEInheritanceError, "inheritance cycle"):
            build_inheritance_chains({"A": {"parent": "B"}, "B": {"parent": "A"}})

    def test_sqf_converter_exposes_complete_inheritance(self):
        capture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        package, envelope = convert_capture_with_inheritance(capture)
        root = capture["root"]
        classes = package["snapshot"]["roots"][root]
        self.assertTrue(envelope["inheritance"]["complete"])
        self.assertEqual(set(envelope["inheritance"]["chains"]), set(classes))
        self.assertGreaterEqual(envelope["inheritance"]["maxDepth"], 1)

    def test_sqf_converter_propagates_cycle_failure(self):
        capture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        capture = copy.deepcopy(capture)
        capture["classes"][0]["parent"] = capture["classes"][1]["classname"]
        capture["classes"][1]["parent"] = capture["classes"][0]["classname"]
        with self.assertRaises(A3XESQFCaptureError):
            convert_capture_with_inheritance(capture)


if __name__ == "__main__":
    unittest.main()
