import unittest
from pathlib import Path

from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3qe import A3QEEngine, A3QEFilter, A3QEQuery, A3QEQueryError


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "a3dm_v0_1_example.json"


class A3QEPlannerTests(unittest.TestCase):
    def setUp(self):
        self.engine = A3QEEngine(A3DMSnapshot.from_file(FIXTURE))

    def test_mixed_query_uses_all_explicit_index_routes(self):
        query = A3QEQuery(
            root="CfgVehicles",
            filters=(
                A3QEFilter("displayName", "contains", "rifle"),
                A3QEFilter("scope", "eq", 2),
            ),
            limit=10,
        )
        results = self.engine.execute(query)
        plan = self.engine.last_plan
        self.assertEqual([item.classname for item in results], ["A3CDB_Test_Soldier"])
        self.assertIsNotNone(plan)
        self.assertTrue(plan.complete)
        self.assertIsNone(plan.fallback)
        self.assertEqual({step.index for step in plan.steps}, {"exact", "text"})
        estimates = [step.estimated_matches for step in plan.steps]
        self.assertEqual(estimates, sorted(estimates))

    def test_property_contains_is_routed_to_property_index(self):
        query = A3QEQuery(
            root="CfgVehicles",
            filters=(A3QEFilter("linkedItems", "contains", "A3CDB_Test_Helmet"),),
            limit=10,
        )
        self.engine.execute(query)
        indexes = [step.index for step in self.engine.last_plan.steps]
        self.assertIn("property", indexes)

    def test_unsupported_route_is_rejected_without_fallback(self):
        query = A3QEQuery(filters=(A3QEFilter("scope", "contains", "2"),))
        with self.assertRaisesRegex(A3QEQueryError, "no complete index route"):
            self.engine.execute(query)


if __name__ == "__main__":
    unittest.main()
