import json
import unittest
from pathlib import Path


class PublicFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.path = Path("data/fixtures/public_fixture.json")
        self.data = json.loads(self.path.read_text(encoding="utf-8"))

    def test_public_fixture_is_artificial_only(self) -> None:
        self.assertIs(self.data["artificialDataOnly"], True)
        self.assertIs(self.data["sourceGameDataIncluded"], False)
        self.assertEqual(
            {profile["profileId"] for profile in self.data["profiles"]},
            {"P0_TEST", "P1_TEST"},
        )
        for profile in self.data["profiles"]:
            self.assertTrue(profile["profileId"].endswith("_TEST"))
            for asset in profile["assets"]:
                self.assertTrue(asset["className"].startswith("A3CDB_Test_"))
                self.assertTrue(asset["configRoot"].startswith("Cfg"))

    def test_no_real_profile_names(self) -> None:
        text = self.path.read_text(encoding="utf-8")
        for forbidden in ("TOTAL_V2", "V008", "P0_REAL", "P5_REAL"):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
