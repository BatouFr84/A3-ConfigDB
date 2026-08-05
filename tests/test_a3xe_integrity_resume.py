import json
import tempfile
import unittest
from pathlib import Path

from tools.a3xe_artificial_exporter import export_artificial
from tools.a3xe_integrity_resume import (
    A3XEIntegrityError,
    A3XEResumeError,
    checkpoint,
    complete_state,
    context_fingerprint,
    load_state,
    new_resume_state,
    validate_resume_context,
    verify_snapshot_integrity,
    write_state_atomic,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "fixtures" / "a3xe_artificial_source_v0_1.json"


def context():
    return {
        "gameVersion": "A3CDB-Test-Game-1.0",
        "gameBuild": "test",
        "loadedAddons": [
            {"order": 0, "id": "A3CDB_Test_Core"},
            {"order": 1, "id": "A3CDB_Test_Expansion"},
        ],
        "activeDlc": ["A3CDB_TEST_DLC"],
        "roots": ["CfgAmmo", "CfgMagazines", "CfgVehicles", "CfgWeapons"],
        "propertyMode": "local_and_resolved",
        "inheritanceMode": "explicit_parent",
        "relationMode": "known_fields",
    }


class A3XEIntegrityResumeTests(unittest.TestCase):
    def setUp(self):
        source = json.loads(SOURCE.read_text(encoding="utf-8"))
        self.package, _ = export_artificial(source)
        self.class_count = sum(
            len(classes) for classes in self.package["snapshot"]["roots"].values()
        )

    def test_context_fingerprint_is_deterministic(self):
        self.assertEqual(context_fingerprint(context()), context_fingerprint(context()))

    def test_resume_rejects_changed_game_build(self):
        state = new_resume_state(run_id="RUN_1", context=context())
        changed = context()
        changed["gameBuild"] = "other"
        with self.assertRaisesRegex(A3XEResumeError, "gameBuild"):
            validate_resume_context(state, changed)

    def test_resume_rejects_changed_addon_order(self):
        state = new_resume_state(run_id="RUN_1", context=context())
        changed = context()
        changed["loadedAddons"] = list(reversed(changed["loadedAddons"]))
        with self.assertRaisesRegex(A3XEResumeError, "loadedAddons"):
            validate_resume_context(state, changed)

    def test_checkpoint_is_monotonic(self):
        state = new_resume_state(run_id="RUN_1", context=context())
        state = checkpoint(
            state,
            root="CfgWeapons",
            classname="A3CDB_Test_Rifle",
            classes_discovered=3,
            classes_serialized=2,
            roots_complete=1,
        )
        with self.assertRaisesRegex(A3XEResumeError, "move backwards"):
            checkpoint(
                state,
                root="CfgWeapons",
                classname="A3CDB_Test_Rifle",
                classes_discovered=3,
                classes_serialized=1,
                roots_complete=1,
            )

    def test_state_roundtrip_is_atomic_and_loadable(self):
        state = new_resume_state(run_id="RUN_1", context=context())
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "a3xe-resume.json"
            write_state_atomic(path, state)
            self.assertTrue(path.exists())
            self.assertFalse(path.with_suffix(".json.tmp").exists())
            self.assertEqual(load_state(path)["contextFingerprint"], state["contextFingerprint"])

    def test_snapshot_integrity_returns_sha256(self):
        integrity = verify_snapshot_integrity(self.package, self.class_count)
        self.assertTrue(integrity["complete"])
        self.assertEqual(len(integrity["snapshotDigest"]), 64)
        self.assertEqual(integrity["classesValidated"], self.class_count)

    def test_integrity_rejects_wrong_class_count(self):
        with self.assertRaisesRegex(A3XEIntegrityError, "class count mismatch"):
            verify_snapshot_integrity(self.package, self.class_count + 1)

    def test_complete_state_disables_resume(self):
        state = new_resume_state(run_id="RUN_1", context=context())
        state = checkpoint(
            state,
            root="CfgWeapons",
            classname="A3CDB_Test_Rifle",
            classes_discovered=self.class_count,
            classes_serialized=self.class_count,
            roots_complete=4,
        )
        completed = complete_state(state, self.package)
        self.assertEqual(completed["status"], "complete")
        self.assertFalse(completed["resumePossible"])
        self.assertEqual(completed["integrityState"], "verified")
        with self.assertRaisesRegex(A3XEResumeError, "completed"):
            validate_resume_context(completed, context())


if __name__ == "__main__":
    unittest.main()
