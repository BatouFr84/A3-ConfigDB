import unittest
from pathlib import Path

from tools.a3_browser_backend import A3BrowserBackend
from tools.a3dm_snapshot import A3DMSnapshot


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "a3dm_v0_1_example.json"


class A3BrowserBackendTests(unittest.TestCase):
    def setUp(self):
        self.backend = A3BrowserBackend(A3DMSnapshot.from_file(FIXTURE))

    def test_capabilities_are_stable(self):
        response = self.backend.capabilities()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body["status"], "ok")
        self.assertEqual(response.body["data"]["maxLimit"], 500)
        self.assertIn("basic", response.body["data"]["queryModes"])
        self.assertIn("advanced", response.body["data"]["queryModes"])
        self.assertEqual(
            response.body["data"]["textIndexedFields"],
            ["classname", "displayName", "author", "faction", "dlc"],
        )

    def test_basic_query_returns_json_ready_results(self):
        response = self.backend.execute_basic({
            "root": "CfgVehicles",
            "filters": [{"field": "scope", "operator": "eq", "value": 2}],
            "limit": 100,
        })
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body["data"]["mode"], "basic")
        self.assertEqual(response.body["data"]["count"], 1)
        self.assertEqual(
            response.body["data"]["results"][0],
            {"root": "CfgVehicles", "classname": "A3CDB_Test_Soldier"},
        )

    def test_basic_text_query_uses_substring_index(self):
        response = self.backend.execute_basic({
            "root": "CfgWeapons",
            "filters": [{"field": "classname", "operator": "contains", "value": "rif"}],
            "limit": 10,
        })
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body["data"]["count"], 1)
        self.assertEqual(response.body["data"]["results"][0]["classname"], "A3CDB_Test_Rifle")

    def test_advanced_query_uses_same_result_contract(self):
        response = self.backend.execute_advanced(
            "FROM CfgVehicles WHERE linkedItems CONTAINS \"A3CDB_Test_Helmet\" LIMIT 10"
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body["data"]["mode"], "advanced")
        self.assertEqual(response.body["data"]["count"], 1)
        self.assertEqual(response.body["data"]["limit"], 10)

    def test_advanced_text_query_uses_same_text_index_contract(self):
        response = self.backend.execute_advanced(
            "FROM CfgWeapons WHERE displayName CONTAINS \"rifle\" LIMIT 10"
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body["data"]["count"], 1)

    def test_validation_and_syntax_errors_are_distinct(self):
        basic = self.backend.execute_basic({"limit": 0})
        advanced = self.backend.execute_advanced("FROM")
        self.assertEqual(basic.status, 400)
        self.assertEqual(basic.body["error"]["code"], "QUERY_VALIDATION_ERROR")
        self.assertEqual(advanced.status, 400)
        self.assertEqual(advanced.body["error"]["code"], "A3QL_SYNTAX_ERROR")

    def test_execution_error_is_not_reported_as_syntax(self):
        response = self.backend.execute_advanced(
            "FROM CfgVehicles WHERE armor EQ 20 LIMIT 10"
        )
        self.assertEqual(response.status, 422)
        self.assertEqual(response.body["error"]["code"], "A3QL_EXECUTION_ERROR")


if __name__ == "__main__":
    unittest.main()
