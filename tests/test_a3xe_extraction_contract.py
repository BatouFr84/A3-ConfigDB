import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "a3xe_extraction_contract_v0_1.schema.json"
FIXTURE = ROOT / "data" / "fixtures" / "a3xe_extraction_contract_v0_1_example.json"
SPEC = ROOT / "docs" / "spec" / "A3XE_EXTRACTION_CONTRACT_V0_1.md"


class A3XEExtractionContractTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.spec = SPEC.read_text(encoding="utf-8")

    def test_contract_has_required_top_level_sections(self):
        expected = {"contractVersion", "run", "environment", "selection", "progress", "integrity", "diagnostics"}
        self.assertEqual(set(self.schema["required"]), expected)
        self.assertTrue(expected.issubset(self.fixture))
        self.assertEqual(self.fixture["contractVersion"], "0.1")

    def test_loaded_addon_order_is_explicit_and_deterministic(self):
        addons = self.fixture["environment"]["loadedAddons"]
        self.assertEqual([item["order"] for item in addons], list(range(len(addons))))
        self.assertIn("loadedAddons[].order", self.spec)
        self.assertIn("authoritative provenance", self.spec)

    def test_completion_requires_integrity_and_no_errors(self):
        self.assertEqual(self.fixture["run"]["status"], "complete")
        self.assertTrue(self.fixture["integrity"]["complete"])
        self.assertEqual(self.fixture["integrity"]["algorithm"], "sha256")
        self.assertEqual(self.fixture["diagnostics"]["errors"], [])
        self.assertEqual(len(self.fixture["integrity"]["snapshotDigest"]), 64)

    def test_resume_and_atomic_commit_rules_are_documented(self):
        for marker in ("resumeOf", "last atomically committed class", "atomically renamed", "no silent partial success"):
            self.assertIn(marker, self.spec)

    def test_public_boundary_excludes_personal_identifiers(self):
        for marker in ("Steam identifiers", "machine names", "profile paths"):
            self.assertIn(marker, self.spec)


if __name__ == "__main__":
    unittest.main()
