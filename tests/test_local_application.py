import unittest
from pathlib import Path

from tools.a3cdb_query.local_application import A3ConfigDBApplication


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "a3dm_v0_1_example.json"


class LocalApplicationTests(unittest.TestCase):
    def setUp(self):
        self.application = A3ConfigDBApplication.from_dataset(FIXTURE)

    def test_health_identifies_loaded_snapshot(self):
        response = self.application.health()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body["status"], "ok")
        self.assertEqual(response.body["dataset"], "A3CDB_Test_Snapshot_01")

    def test_basic_search_is_enriched_for_browser(self):
        response = self.application.execute_basic({
            "root": "CfgVehicles",
            "filters": [{"field": "scope", "operator": "eq", "value": 2}],
            "limit": 10,
        })
        self.assertEqual(response.status, 200)
        result = response.body["data"]["results"][0]
        self.assertEqual(result["classname"], "A3CDB_Test_Soldier")
        self.assertEqual(result["displayName"], "A3CDB Test Rifleman")
        self.assertEqual(result["parent"], "A3CDB_Test_Man")

    def test_advanced_search_uses_same_result_contract(self):
        response = self.application.execute_advanced("FROM CfgWeapons WHERE scope EQ 2 LIMIT 10")
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body["data"]["results"][0]["classname"], "A3CDB_Test_Rifle")

    def test_class_not_found_is_stable_404(self):
        response = self.application.get_class("CfgVehicles", "Missing")
        self.assertEqual(response.status, 404)
        self.assertEqual(response.body["error"]["code"], "CLASS_NOT_FOUND")


if __name__ == "__main__":
    unittest.main()
