import json
import unittest
from pathlib import Path

from tools.a3cdb_query.public_fixture_server import BACKEND, SNAPSHOT, WEB


class BasicSearchUITests(unittest.TestCase):
    def test_mobile_ui_assets_are_present(self):
        html = (WEB / "index.html").read_text(encoding="utf-8")
        script = (WEB / "app.js").read_text(encoding="utf-8")
        css = (WEB / "styles.css").read_text(encoding="utf-8")
        self.assertIn('id="search-form"', html)
        self.assertIn('id="filter-template"', html)
        self.assertIn('/api/basic', script)
        self.assertIn('filters:', script)
        self.assertIn('@media(max-width:720px)', css)

    def test_basic_payload_matches_a3qm_contract(self):
        response = BACKEND.execute_basic({
            "root": "CfgVehicles",
            "filters": [{"field": "scope", "operator": "eq", "value": 2}],
            "limit": 100,
        })
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body["status"], "ok")
        self.assertEqual(response.body["data"]["results"][0]["classname"], "A3CDB_Test_Soldier")

    def test_snapshot_fixture_remains_artificial(self):
        self.assertTrue(SNAPSHOT.manifest["artificialDataOnly"])
        self.assertFalse(SNAPSHOT.manifest["sourceGameDataIncluded"])


if __name__ == "__main__":
    unittest.main()
