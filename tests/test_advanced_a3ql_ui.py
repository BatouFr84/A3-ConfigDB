import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AdvancedA3QLUITests(unittest.TestCase):
    def test_html_exposes_advanced_controls(self):
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        for marker in ("advanced-tab", "advanced-panel", "a3ql-source", "run-a3ql", "a3ql-error"):
            self.assertIn(marker, html)
        self.assertIn("FROM CfgVehicles", html)
        self.assertNotIn("SELECT className", html)

    def test_client_calls_advanced_endpoint(self):
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        self.assertIn("/api/advanced", script)
        self.assertIn("Executing A3QL", script)
        self.assertIn("example-query", script)

    def test_server_routes_advanced_queries(self):
        server = (ROOT / "tools" / "a3cdb_query" / "local_http_server.py").read_text(encoding="utf-8")
        self.assertIn('"/api/advanced"', server)
        self.assertIn("application.execute_advanced(source)", server)
        self.assertIn("INVALID_A3QL_REQUEST", server)


if __name__ == "__main__":
    unittest.main()
