import unittest
from pathlib import Path

from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3qe import A3QEEngine, A3QEFilter, A3QEQuery, A3QEQueryError, A3QEResult


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "a3dm_v0_1_example.json"


class A3QEEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = A3QEEngine(A3DMSnapshot.from_file(FIXTURE))

    def test_exact_filter(self):
        query = A3QEQuery(filters=(A3QEFilter("scope", "eq", 2),))
        self.assertEqual(
            self.engine.execute(query),
            (
                A3QEResult("CfgVehicles", "A3CDB_Test_Soldier"),
                A3QEResult("CfgWeapons", "A3CDB_Test_Rifle"),
            ),
        )

    def test_property_contains_filter(self):
        query = A3QEQuery(
            root="CfgVehicles",
            filters=(A3QEFilter("linkedItems", "contains", "A3CDB_Test_Helmet"),),
        )
        self.assertEqual(
            self.engine.execute(query),
            (A3QEResult("CfgVehicles", "A3CDB_Test_Soldier"),),
        )

    def test_multiple_filters_use_and_semantics(self):
        query = A3QEQuery(
            root="CfgVehicles",
            filters=(
                A3QEFilter("scope", "eq", 2),
                A3QEFilter("faction", "eq", "A3CDB_TEST_FACTION"),
                A3QEFilter("linkedItems", "contains", "A3CDB_Test_Vest"),
            ),
        )
        self.assertEqual(
            self.engine.execute(query),
            (A3QEResult("CfgVehicles", "A3CDB_Test_Soldier"),),
        )

    def test_empty_filters_return_deterministic_root_limited_results(self):
        query = A3QEQuery(root="CfgVehicles", limit=1)
        self.assertEqual(
            self.engine.execute(query),
            (A3QEResult("CfgVehicles", "A3CDB_Test_Man"),),
        )

    def test_invalid_query_fails_closed(self):
        with self.assertRaises(A3QEQueryError):
            self.engine.execute(A3QEQuery(root="CfgMissing"))
        with self.assertRaises(A3QEQueryError):
            self.engine.execute(A3QEQuery(limit=0))
        with self.assertRaises(A3QEQueryError):
            self.engine.execute(A3QEQuery(filters=(A3QEFilter("armor", "eq", 20),)))
        with self.assertRaises(A3QEQueryError):
            self.engine.execute(A3QEQuery(filters=(A3QEFilter("scope", "gt", 1),)))


if __name__ == "__main__":
    unittest.main()
