import json
import tempfile
import unittest
from pathlib import Path

from tools.a3_browser_backend import A3BrowserBackend
from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3xe_artificial_exporter import export_artificial, snapshot_digest, write_export


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "fixtures" / "a3xe_artificial_source_v0_1.json"


class A3XEArtificialExporterTests(unittest.TestCase):
    def test_export_is_valid_deterministic_and_complete(self):
        source = json.loads(SOURCE.read_text(encoding="utf-8"))
        package_a, run_a = export_artificial(source)
        package_b, run_b = export_artificial(source)
        self.assertEqual(package_a, package_b)
        self.assertEqual(run_a, run_b)
        snapshot = A3DMSnapshot(package_a)
        self.assertEqual(snapshot.snapshot_id, "A3CDB_Artificial_Exporter_Snapshot_01")
        self.assertEqual(run_a["progress"]["classesSerialized"], 5)
        self.assertEqual(run_a["integrity"]["snapshotDigest"], snapshot_digest(package_a))
        self.assertEqual(run_a["diagnostics"], {"errors": [], "warnings": [], "skipped": []})

    def test_generated_snapshot_loads_in_browser_backend(self):
        package, _ = export_artificial(json.loads(SOURCE.read_text(encoding="utf-8")))
        backend = A3BrowserBackend(A3DMSnapshot(package))
        response = backend.execute_basic({"root": "CfgVehicles", "filters": [], "limit": 100})
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body["data"]["total"], 2)

    def test_writer_publishes_final_files_without_temporary_residue(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path, run_path = write_export(SOURCE, directory)
            self.assertTrue(snapshot_path.is_file())
            self.assertTrue(run_path.is_file())
            self.assertFalse(list(Path(directory).glob("*.tmp")))
            A3DMSnapshot.from_file(snapshot_path)


if __name__ == "__main__":
    unittest.main()
