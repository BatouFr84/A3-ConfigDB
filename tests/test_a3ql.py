import unittest

from tools.a3ql import A3QLSyntaxError, parse_a3ql


class A3QLTests(unittest.TestCase):
    def test_minimal_query(self):
        query = parse_a3ql("FROM CfgVehicles")
        self.assertEqual(query.root, "CfgVehicles")
        self.assertEqual(query.filters, ())
        self.assertEqual(query.limit, 100)

    def test_where_and_limit(self):
        query = parse_a3ql(
            'FROM CfgVehicles WHERE scope EQ 2 '
            'AND linkedItems CONTAINS "A3CDB_Test_Helmet" LIMIT 50'
        )
        self.assertEqual(query.root, "CfgVehicles")
        self.assertEqual(query.limit, 50)
        self.assertEqual(len(query.filters), 2)
        self.assertEqual(query.filters[0].field, "scope")
        self.assertEqual(query.filters[0].operator, "eq")
        self.assertEqual(query.filters[0].value, 2)
        self.assertEqual(query.filters[1].operator, "contains")
        self.assertEqual(query.filters[1].value, "A3CDB_Test_Helmet")

    def test_keywords_are_case_insensitive(self):
        query = parse_a3ql('from CfgWeapons where scope eq 2 limit 10')
        self.assertEqual(query.root, "CfgWeapons")
        self.assertEqual(query.limit, 10)

    def test_boolean_and_float_values(self):
        boolean_query = parse_a3ql("FROM CfgVehicles WHERE enabled EQ true")
        float_query = parse_a3ql("FROM CfgVehicles WHERE armor EQ 12.5")
        self.assertIs(boolean_query.filters[0].value, True)
        self.assertEqual(float_query.filters[0].value, 12.5)

    def test_rejects_unquoted_bare_string_value(self):
        with self.assertRaises(A3QLSyntaxError):
            parse_a3ql("FROM CfgVehicles WHERE faction EQ BLU_F")

    def test_rejects_unknown_operator(self):
        with self.assertRaises(A3QLSyntaxError):
            parse_a3ql("FROM CfgVehicles WHERE scope GT 1")

    def test_rejects_invalid_limit(self):
        with self.assertRaises(A3QLSyntaxError):
            parse_a3ql("FROM CfgVehicles LIMIT 0")
        with self.assertRaises(A3QLSyntaxError):
            parse_a3ql("FROM CfgVehicles LIMIT 2.5")

    def test_rejects_trailing_tokens(self):
        with self.assertRaises(A3QLSyntaxError):
            parse_a3ql("FROM CfgVehicles GARBAGE")

    def test_rejects_empty_query(self):
        with self.assertRaises(A3QLSyntaxError):
            parse_a3ql("   ")


if __name__ == "__main__":
    unittest.main()
