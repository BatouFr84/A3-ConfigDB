import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ExportUITests(unittest.TestCase):
    def test_export_controls_exist(self):
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        for marker in ("export-results", "results-export-format", "export-class", "class-export-format"):
            self.assertIn(marker, html)
        for label in ("JSON", "CSV", "Markdown", "SQF Array", "C++ config"):
            self.assertIn(label, html)

    def test_export_runtime_is_deterministic_and_rejects_truncation(self):
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        for marker in ("downloadText", "resultExport", "classExport", "safeName", "Export refused"):
            self.assertIn(marker, script)
        self.assertIn("data.total!==items.length", script)
        self.assertIn("a3configdb_", script)

    def test_existing_navigation_and_a3ql_contracts_remain(self):
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        for marker in ("/api/advanced", "example-query", "history.pushState", "history.replaceState", "popstate"):
            self.assertIn(marker, script)


if __name__ == "__main__":
    unittest.main()
