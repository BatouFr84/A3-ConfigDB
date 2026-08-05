import unittest
from pathlib import Path

from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3_relations import A3RelationResolver
from tools.a3cdb_query.local_application import A3ConfigDBApplication


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "a3dm_v0_1_example.json"


class RelationResolverTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = A3DMSnapshot.from_file(FIXTURE)
        self.resolver = A3RelationResolver(self.snapshot)

    def test_parent_and_children_are_typed(self):
        soldier = self.resolver.relations_for("CfgVehicles", "A3CDB_Test_Soldier")
        parent = soldier["parent"]
        self.assertEqual(parent, {"root": "CfgVehicles", "classname": "A3CDB_Test_Man", "exists": True})
        base = self.resolver.relations_for("CfgVehicles", "A3CDB_Test_Man")
        self.assertEqual(base["children"][0]["classname"], "A3CDB_Test_Soldier")

    def test_absent_relation_roots_do_not_fake_targets(self):
        soldier = self.resolver.relations_for("CfgVehicles", "A3CDB_Test_Soldier")
        self.assertEqual(soldier["outbound"]["weapons"], [])
        self.assertEqual(soldier["outbound"]["magazines"], [])
        self.assertEqual(soldier["outbound"]["ammo"], [])
        self.assertTrue(soldier["complete"])

    def test_class_endpoint_exposes_relation_contract(self):
        response = A3ConfigDBApplication.from_dataset(FIXTURE).get_class("CfgVehicles", "A3CDB_Test_Soldier")
        self.assertEqual(response.status, 200)
        self.assertIn("relations", response.body["data"])
        self.assertIn("missingTargets", response.body["data"]["relations"])


if __name__ == "__main__":
    unittest.main()
