import unittest

from tools.a3qm import A3QMError, normalize_query


class A3QMTests(unittest.TestCase):
    def test_normalizes_basic_payload_and_defaults_limit(self):
        query = normalize_query({
            "root": "CfgVehicles",
            "filters": [
                {"field": "scope", "operator": "EQ", "value": 2},
                {"field": "linkedItems", "operator": "Contains", "value": "A3CDB_Test_Helmet"},
            ],
        })
        self.assertEqual(query.root, "CfgVehicles")
        self.assertEqual(query.limit, 100)
        self.assertEqual(query.filters[0].operator, "eq")
        self.assertEqual(query.filters[1].operator, "contains")

    def test_converts_to_a3qe_query(self):
        query = normalize_query({
            "root": "CfgVehicles",
            "filters": [{"field": "scope", "operator": "eq", "value": 2}],
            "limit": 25,
        }).to_a3qe()
        self.assertEqual(query.root, "CfgVehicles")
        self.assertEqual(query.limit, 25)
        self.assertEqual(query.filters[0].field, "scope")

    def test_rejects_unknown_top_level_fields(self):
        with self.assertRaises(A3QMError):
            normalize_query({"root": None, "filters": [], "limit": 100, "unexpected": True})

    def test_rejects_unknown_filter_fields(self):
        with self.assertRaises(A3QMError):
            normalize_query({
                "filters": [{"field": "scope", "operator": "eq", "value": 2, "extra": 1}]
            })

    def test_requires_filter_value_even_when_null_is_intended(self):
        query = normalize_query({
            "filters": [{"field": "parent", "operator": "eq", "value": None}]
        })
        self.assertIsNone(query.filters[0].value)
        with self.assertRaises(A3QMError):
            normalize_query({"filters": [{"field": "scope", "operator": "eq"}]})

    def test_rejects_invalid_limit_and_filter_container(self):
        for value in (0, 501, True, "100"):
            with self.subTest(value=value):
                with self.assertRaises(A3QMError):
                    normalize_query({"limit": value})
        with self.assertRaises(A3QMError):
            normalize_query({"filters": "scope=2"})


if __name__ == "__main__":
    unittest.main()
