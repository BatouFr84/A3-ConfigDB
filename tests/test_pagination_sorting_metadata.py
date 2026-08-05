import unittest
from pathlib import Path

from tools.a3_browser_backend import A3BrowserBackend
from tools.a3dm_snapshot import A3DMSnapshot


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "fixtures" / "a3dm_v0_1_example.json"


class PaginationSortingMetadataTests(unittest.TestCase):
    def setUp(self):
        self.backend = A3BrowserBackend(A3DMSnapshot.from_file(FIXTURE))

    def test_basic_response_distinguishes_total_and_page_count(self):
        response = self.backend.execute_basic({"limit": 1, "offset": 1, "sort": "classname", "direction": "asc"})
        self.assertEqual(response.status, 200)
        data = response.body["data"]
        self.assertEqual(data["total"], 3)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["offset"], 1)
        self.assertEqual(data["limit"], 1)

    def test_sort_metadata_and_duration_are_exposed(self):
        response = self.backend.execute_basic({"limit": 10, "sort": "displayName", "direction": "desc"})
        data = response.body["data"]
        self.assertEqual(data["sort"], {"field": "displayName", "direction": "desc"})
        self.assertGreaterEqual(data["execution"]["durationMs"], 0)
        self.assertIn("indexesUsed", data["execution"])

    def test_invalid_offset_is_rejected(self):
        response = self.backend.execute_basic({"offset": -1})
        self.assertEqual(response.status, 400)
        self.assertEqual(response.body["error"]["code"], "QUERY_VALIDATION_ERROR")


if __name__ == "__main__":
    unittest.main()
