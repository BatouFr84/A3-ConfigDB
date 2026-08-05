import copy
import json
import unittest
from pathlib import Path

from tools.a3xe_pub046_capture_check import PUB046CaptureCheckError, check_capture

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "fixtures" / "a3xe_sqf_capture_v0_1.json"


class PUB046CaptureCheckTests(unittest.TestCase):
    def setUp(self):
        self.capture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.capture["artificial"] = False

    def test_valid_capture_passes(self):
        result = check_capture(self.capture)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["root"], "CfgWeapons")
        self.assertGreater(result["classes"], 0)

    def test_artificial_capture_is_rejected(self):
        capture = copy.deepcopy(self.capture)
        capture["artificial"] = True
        with self.assertRaisesRegex(PUB046CaptureCheckError, "artificial=false"):
            check_capture(capture)

    def test_empty_capture_is_rejected(self):
        capture = copy.deepcopy(self.capture)
        capture["classes"] = []
        with self.assertRaisesRegex(PUB046CaptureCheckError, "at least one class"):
            check_capture(capture)

    def test_wrong_root_is_rejected(self):
        capture = copy.deepcopy(self.capture)
        capture["root"] = "CfgVehicles"
        with self.assertRaisesRegex(PUB046CaptureCheckError, "CfgWeapons"):
            check_capture(capture)


if __name__ == "__main__":
    unittest.main()
