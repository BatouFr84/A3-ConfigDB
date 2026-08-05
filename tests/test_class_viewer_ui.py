import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ClassViewerUITests(unittest.TestCase):
    def test_viewer_contract_is_present(self):
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        js = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        server = (ROOT / "tools" / "a3cdb_query" / "public_fixture_server.py").read_text(encoding="utf-8")
        self.assertIn('id="class-viewer"', html)
        self.assertIn('id="viewer-basic"', html)
        self.assertIn('id="viewer-advanced"', html)
        self.assertIn("/api/class/", js)
        self.assertIn('path.startswith("/api/class/")', server)


if __name__ == "__main__":
    unittest.main()
