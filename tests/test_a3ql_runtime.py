import unittest
from pathlib import Path

from tools.a3dm_snapshot import A3DMSnapshot
from tools.a3ql import A3QLSyntaxError
from tools.a3ql_runtime import A3QLExecutionError, A3QLRuntime, execute_a3ql


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "a3dm_v0_1_example.json"


class A3QLRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = A3DMSnapshot.from_file(FIXTURE)
        self.runtime = A3QLRuntime(self.snapshot)

    def test_executes_a3ql_end_to_end(self):
        execution = self.runtime.execute(
            'FROM CfgVehicles WHERE scope EQ 2 AND linkedItems CONTAINS "A3CDB_Test_Helmet" LIMIT 25'
        )
        self.assertEqual(execution.snapshot_id, "A3CDB_Test_Snapshot_01")
        self.assertEqual(execution.limit, 25)
        self.assertEqual(
            [(item.root, item.classname) for item in execution.results],
            [("CfgVehicles", "A3CDB_Test_Soldier")],
        )

    def test_convenience_helper_returns_deterministic_tuple(self):
        results = execute_a3ql(self.snapshot, "FROM CfgWeapons WHERE scope EQ 2 LIMIT 10")
        self.assertEqual(
            [(item.root, item.classname) for item in results],
            [("CfgWeapons", "A3CDB_Test_Rifle")],
        )

    def test_syntax_errors_remain_distinct(self):
        with self.assertRaises(A3QLSyntaxError):
            self.runtime.execute("FROM CfgVehicles WHERE scope")

    def test_execution_errors_are_wrapped(self):
        with self.assertRaises(A3QLExecutionError) as context:
            self.runtime.execute("FROM CfgMissing LIMIT 10")
        self.assertIn("unknown root", str(context.exception))

    def test_empty_result_is_successful(self):
        execution = self.runtime.execute(
            'FROM CfgVehicles WHERE linkedItems CONTAINS "A3CDB_Test_Missing" LIMIT 10'
        )
        self.assertEqual(execution.results, ())


if __name__ == "__main__":
    unittest.main()
