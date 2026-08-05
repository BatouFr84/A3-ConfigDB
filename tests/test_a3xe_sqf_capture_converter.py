import json
import tempfile
import unittest
from pathlib import Path

from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3xe_sqf_capture_converter import A3XESQFCaptureError, convert_capture, write_conversion

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "fixtures" / "a3xe_sqf_capture_v0_1.json"
SQF = ROOT / "a3xe" / "sqf" / "fn_extractControlledRoot.sqf"


class A3XESQFCaptureConverterTests(unittest.TestCase):
    def test_controlled_sqf_script_contract(self):
        script = SQF.read_text(encoding="utf-8")
        for marker in (
            '"CfgWeapons"',
            "configClasses",
            "inheritsFrom",
            "displayName",
            "scope",
            "author",
            "dlc",
            "copyToClipboard",
            "A3XE_SQF_EXPORT=PASS",
        ):
            self.assertIn(marker, script)
        self.assertNotIn("profileName", script)
        self.assertNotIn("getPlayerUID", script)

    def test_fixture_converts_to_valid_a3dm(self):
        capture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        package, envelope = convert_capture(capture)
        snapshot = A3DMSnapshot(package)
        self.assertEqual(snapshot.roots, ("CfgWeapons",))
        self.assertEqual(snapshot.class_names("CfgWeapons"), (
            "A3CDB_Test_Rifle",
            "A3CDB_Test_Weapon_Base",
        ))
        self.assertEqual(snapshot.resolved_properties("CfgWeapons", "A3CDB_Test_Rifle")["author"], "A3CDB Test Team")
        self.assertEqual(envelope["run"]["status"], "complete")
        self.assertTrue(envelope["integrity"]["complete"])
        self.assertEqual(len(envelope["integrity"]["snapshotDigest"]), 64)

    def test_output_files_use_existing_runtime_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path, run_path = write_conversion(FIXTURE, directory)
            self.assertTrue(snapshot_path.is_file())
            self.assertTrue(run_path.is_file())
            A3DMSnapshot.from_file(snapshot_path)

    def test_parent_outside_capture_is_rejected(self):
        capture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        capture["classes"][1]["parent"] = "Missing_Parent"
        with self.assertRaises(A3XESQFCaptureError):
            convert_capture(capture)


if __name__ == "__main__":
    unittest.main()
