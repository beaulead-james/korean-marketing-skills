"""Ad Library puller: parsing, filtering and output, against pages saved from a real pull.

No network. tests/fixtures/ad-library/search.md is Firecrawl's markdown of a live US keyword
search ("Kettlewell Coffee", Nov 2026), trimmed to four cards with signed image links shortened;
search.html carries three of the same ads as the page's embedded JSON, trimmed the same way.
"""
import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "creative" / "scripts" / "ad_library.py"
FIXTURES = ROOT / "tests" / "fixtures" / "ad-library"

spec = importlib.util.spec_from_file_location("ad_library", SCRIPT)
ad_library = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ad_library)


def run(argv, env=None, fetch=None):
    """Run main() with a clean environment and captured output."""
    out = io.StringIO()
    old = dict(os.environ)
    os.environ.pop("FIRECRAWL_API_KEY", None)
    os.environ.update(env or {})
    try:
        with contextlib.redirect_stdout(out):
            kwargs = {"fetch": fetch} if fetch else {}
            code = ad_library.main(argv, **kwargs)
    finally:
        os.environ.clear()
        os.environ.update(old)
    return code, out.getvalue()


class Markdown(unittest.TestCase):
    def setUp(self):
        self.ads = ad_library.parse_markdown((FIXTURES / "search.md").read_text(encoding="utf-8"))
        self.by_id = {a["library_id"]: a for a in self.ads}

    def test_every_card_in_page_order(self):
        self.assertEqual([a["library_id"] for a in self.ads],
                         ["1000000000000001", "1000000000000002", "1000000000000003", "1000000000000004"])

    def test_start_dates_and_flags(self):
        video = self.by_id["1000000000000002"]
        self.assertEqual(video["started"].isoformat(), "2026-07-30")
        self.assertEqual(video["media_type"], "video")
        self.assertTrue(video["multiple_versions"])
        self.assertEqual(self.by_id["1000000000000003"]["multiple_versions"], False)

    def test_advertiser_text_cta_and_link(self):
        still = self.by_id["1000000000000004"]
        self.assertEqual(still["advertiser"], "Kettlewell")
        self.assertTrue(still["primary_text"].startswith("Taste your way through great coffee."))
        self.assertEqual(still["headline"], "Start Discovering")
        self.assertEqual(still["cta"], "Shop Now")
        self.assertEqual(still["link_url"], "https://www.kettlewell.example/pages/discovery-trial")
        self.assertEqual(len(still["image_urls"]), 1)
        self.assertIn("s600x600", still["image_urls"][0])  # the creative, not the 60px avatar

    def test_creator_running_a_brands_ad(self):
        ad = self.by_id["1000000000000003"]
        self.assertEqual(ad["advertiser"], "Harborline")
        self.assertEqual(ad["via"], "sample_creator")
        self.assertEqual(ad["cta"], "Book now")

    def test_video_text_stops_before_player_message(self):
        self.assertNotIn("trouble playing", self.by_id["1000000000000002"]["primary_text"])


class EmbeddedJson(unittest.TestCase):
    def setUp(self):
        self.ads = ad_library.parse_raw_html((FIXTURES / "search.html").read_text(encoding="utf-8"))
        self.by_id = {a["library_id"]: a for a in self.ads}

    def test_video_links_and_poster(self):
        ad = self.by_id["1000000000000002"]
        self.assertEqual(ad["media_type"], "video")
        self.assertEqual(ad["page_id"], "2000000000000001")
        self.assertTrue(ad["video_urls"] and ad["video_urls"][0].startswith("https://video"))
        self.assertTrue(ad["poster_urls"])
        self.assertEqual(ad["same_creative_ads"], 1)

    def test_template_fields_fall_back_to_the_card(self):
        ad = self.by_id["1000000000000002"]  # body is "{{product.brand}}" at the top level
        self.assertTrue(ad["primary_text"].startswith("Discover extraordinary coffees"))
        self.assertEqual(ad["headline"], "Discover New Coffee")

    def test_dynamic_creative_is_not_a_carousel(self):
        self.assertEqual(self.by_id["1000000000000004"]["media_type"], "image")

    def test_json_wins_over_markdown(self):
        md = (FIXTURES / "search.md").read_text(encoding="utf-8")
        raw = (FIXTURES / "search.html").read_text(encoding="utf-8")
        ads = ad_library.parse_page({"markdown": md, "rawHtml": raw})
        self.assertEqual({a["source"] for a in ads}, {"json"})
        self.assertEqual(ad_library.parse_page({"markdown": md, "rawHtml": ""})[0]["source"], "markdown")


class Filters(unittest.TestCase):
    def test_advertiser_exact_name_then_contains(self):
        ads = ad_library.parse_markdown((FIXTURES / "search.md").read_text(encoding="utf-8"))
        self.assertEqual([a["library_id"] for a in ad_library.filter_advertiser(ads, "kettlewell")],
                         ["1000000000000002", "1000000000000004"])
        self.assertEqual(len(ad_library.filter_advertiser(ads, "gearbin")), 1)
        self.assertEqual(ad_library.filter_advertiser(ads, "nobody here"), [])

    def test_search_url_is_the_working_form(self):
        self.assertEqual(
            ad_library.search_url("coffee subscription"),
            "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US"
            "&q=coffee%20subscription&search_type=keyword_unordered&media_type=all"
            "&sort_data[mode]=total_impressions&sort_data[direction]=desc")


class Cli(unittest.TestCase):
    def test_no_key_prints_the_url_and_fetches_nothing(self):
        def boom(*args, **kwargs):
            raise AssertionError("no network without a key")
        code, out = run(["coffee subscription"], fetch=boom)
        self.assertEqual(code, 0)
        self.assertIn("q=coffee%20subscription", out)
        self.assertIn("FIRECRAWL_API_KEY", out)

    def test_from_file_writes_index_and_board(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run(["Kettlewell Coffee", "--from-file", str(FIXTURES / "search.md"), "--advertiser", "Kettlewell",
                             "--out", tmp, "--no-download", "--as-of", "2026-11-16"])
            self.assertEqual(code, 0)
            index = json.loads(Path(tmp, "index.json").read_text(encoding="utf-8"))
            self.assertEqual(index["count"], 2)
            first = index["ads"][0]
            self.assertEqual(first["days_running"], 109)
            self.assertEqual(first["ad_library_url"], "https://www.facebook.com/ads/library/?id=1000000000000002")
            board = Path(tmp, "board.html").read_text(encoding="utf-8")
            self.assertIn("109 days", board)
            self.assertIn("Start Discovering", board)

    def test_key_is_never_printed_or_saved(self):
        secret = "fc-test-secret-0042"
        seen = {}

        def fake_fetch(url, key, wait_ms):
            seen["key"], seen["url"] = key, url
            return {"markdown": (FIXTURES / "search.md").read_text(encoding="utf-8"),
                    "rawHtml": (FIXTURES / "search.html").read_text(encoding="utf-8")}

        with tempfile.TemporaryDirectory() as tmp:
            code, out = run(["Kettlewell Coffee", "--out", tmp, "--no-download", "--as-of", "2026-11-16"],
                            env={"FIRECRAWL_API_KEY": secret}, fetch=fake_fetch)
            self.assertEqual(code, 0)
            self.assertEqual(seen["key"], secret)
            self.assertIn("q=Kettlewell%20Coffee", seen["url"])
            self.assertNotIn(secret, out)
            for name in ("index.json", "board.html"):
                self.assertNotIn(secret, Path(tmp, name).read_text(encoding="utf-8"))

    def test_pull_failure_points_to_the_page(self):
        def failing(*args, **kwargs):
            raise ad_library.PullError("Firecrawl returned HTTP 402: out of credits")
        code, out = run(["Kettlewell Coffee"], env={"FIRECRAWL_API_KEY": "fc-x"}, fetch=failing)
        self.assertEqual(code, 1)
        self.assertIn("HTTP 402", out)
        self.assertIn("facebook.com/ads/library", out)


if __name__ == "__main__":
    unittest.main()
