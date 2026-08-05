import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BrowserNavigationUITests(unittest.TestCase):
    def test_navigation_controls_and_relation_panel_exist(self):
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        for marker in ("viewer-back", "viewer-forward", "relation-groups", "relation-warning"):
            self.assertIn(marker, html)

    def test_relations_are_opened_through_class_endpoint(self):
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        self.assertIn("data.relations", script)
        self.assertIn("openClass(target.root,target.classname", script)
        self.assertIn("history.pushState", script)
        self.assertIn("history.replaceState", script)
        self.assertIn("popstate", script)

    def test_stable_viewer_url_contains_root_class_and_view(self):
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        self.assertIn("searchParams.set('root'", script)
        self.assertIn("searchParams.set('class'", script)
        self.assertIn("searchParams.set('view'", script)


if __name__ == "__main__":
    unittest.main()
