"""site-audit crawler: robots rules for AI crawlers, sitemap parsing, page extraction,
findings, content signals and a tiny crawl of a local fixture site. No outside network."""
import functools
import gzip
import http.server
import importlib.util
import io
import json
import os
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "site-audit" / "scripts" / "crawl_audit.py"
SITE = ROOT / "tests" / "fixtures" / "site-audit" / "site"

_spec = importlib.util.spec_from_file_location("crawl_audit", SCRIPT)
ca = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ca)


def fixture(rel):
    return (SITE / rel).read_text(encoding="utf-8")


def fake_response(url, html, status=200, headers=None, chain=None):
    hdrs = {"content-type": "text/html; charset=utf-8"}
    hdrs.update(headers or {})
    return {"url": url, "requested_url": url, "final_url": url, "status": status, "headers": hdrs,
            "body": html.encode("utf-8"), "chain": chain or [], "first_ttfb_ms": 20, "ttfb_ms": 20,
            "total_ms": 25, "error": None, "truncated": False}


def make_audit():
    args = SimpleNamespace(mode="full", max_pages=None, timeout=5.0, delay=0.0, concurrency=1, max_minutes=1.0,
                           quiet=True, no_psi=True, psi_templates=0, psi_timeout=1.0, no_bot_check=True,
                           compare=None, rendered=None, render=None, render_limit=0, url="https://hartline.test/")
    return ca.Audit(args)


ROBOTS = """# sample
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /*.pdf$

User-agent: GPTBot
User-agent: CCBot
Disallow: /

user-agent: perplexitybot
sitemap: https://hartline.test/sitemap.xml
disallow: /blog/
Allow: /blog/public-

User-agent: ClaudeBot
Disallow: /
Allow: /
"""


class RobotsForAiBots(unittest.TestCase):
    def setUp(self):
        self.robots = ca.Robots(ROBOTS)

    def test_named_group_blocks_gptbot_and_shared_group_blocks_ccbot(self):
        pol = self.robots.policy("GPTBot", ["/", "/services/"])
        self.assertEqual(pol["state"], "blocked")
        self.assertTrue(pol["named_group"])
        self.assertEqual(pol["root_rule"], "Disallow: /")
        self.assertEqual(self.robots.policy("CCBot")["state"], "blocked")

    def test_unnamed_bot_follows_the_star_group(self):
        pol = self.robots.policy("OAI-SearchBot", ["/", "/services/"])
        self.assertEqual(pol["state"], "allowed")
        self.assertFalse(pol["named_group"])
        self.assertIn("/wp-admin/", pol["disallowed_paths"])
        self.assertFalse(self.robots.check("OAI-SearchBot", "/wp-admin/options.php")[0])
        self.assertTrue(self.robots.check("OAI-SearchBot", "/wp-admin/admin-ajax.php")[0], "longest match wins")

    def test_case_insensitive_agent_and_sitemap_line_inside_a_group(self):
        self.assertFalse(self.robots.check("PerplexityBot", "/blog/how-to")[0])
        self.assertTrue(self.robots.check("PerplexityBot", "/blog/public-notes")[0])
        self.assertEqual(self.robots.policy("PerplexityBot", ["/", "/blog/a"])["state"], "partial")
        self.assertIn("https://hartline.test/sitemap.xml", self.robots.sitemaps)

    def test_tie_goes_to_allow(self):
        self.assertTrue(self.robots.check("ClaudeBot", "/anything")[0])

    def test_wildcard_and_end_anchor(self):
        self.assertFalse(self.robots.check("Googlebot", "/files/menu.pdf")[0])
        self.assertTrue(self.robots.check("Googlebot", "/files/menu.pdf?v=2")[0])

    def test_no_robots_means_everything_allowed(self):
        empty = ca.Robots("")
        self.assertEqual(empty.policy("GPTBot")["state"], "allowed")
        self.assertEqual(empty.policy("GPTBot")["follows"], "no rules")

    def test_cloudflare_managed_block_and_content_signals(self):
        text = ("# BEGIN Cloudflare Managed content\nUser-Agent: *\nContent-signal: search=yes, ai-train=no\nAllow: /\n\n"
                "User-agent: ClaudeBot\nDisallow: /\n# END Cloudflare Managed Content\n")
        r = ca.Robots(text)
        self.assertTrue(r.cloudflare_managed)
        self.assertEqual(r.content_signals, ["search=yes, ai-train=no"])
        self.assertEqual(r.policy("ClaudeBot")["state"], "blocked")
        self.assertEqual(r.policy("Claude-SearchBot")["state"], "allowed")


SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://hartline.test/</loc><lastmod>2026-10-01</lastmod></url>
  <url><loc>https://hartline.test/services/</loc><lastmod>2026-10-02</lastmod></url>
  <url><loc>/old-offer/</loc></url>
</urlset>"""


class SitemapParse(unittest.TestCase):
    def test_urlset(self):
        out = ca.parse_sitemap(SITEMAP.encode(), "https://hartline.test/sitemap.xml")
        self.assertEqual(out["kind"], "urlset")
        self.assertEqual(out["url_count"], 3)
        self.assertEqual(out["lastmod"], 2)
        self.assertEqual([u["loc"] for u in out["urls"]][-1], "https://hartline.test/old-offer/")
        self.assertEqual(out["errors"], [])

    def test_index_and_gzip(self):
        index = ('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                 "<sitemap><loc>https://hartline.test/pages.xml.gz</loc></sitemap></sitemapindex>")
        out = ca.parse_sitemap(gzip.compress(index.encode()), "https://hartline.test/sitemap.xml")
        self.assertEqual(out["kind"], "sitemapindex")
        self.assertEqual(out["children"], ["https://hartline.test/pages.xml.gz"])

    def test_html_and_entities_are_refused(self):
        html = ca.parse_sitemap(b"<!doctype html><html><body>Not found</body></html>", "https://hartline.test/sitemap.xml")
        self.assertIsNone(html["kind"])
        self.assertIn("HTML", html["errors"][0])
        evil = ca.parse_sitemap(b'<?xml version="1.0"?><!DOCTYPE x [<!ENTITY a "b">]><urlset/>', "https://hartline.test/s.xml")
        self.assertIsNone(evil["kind"])
        self.assertIn("DOCTYPE", evil["errors"][0])


class PageExtraction(unittest.TestCase):
    def test_title_meta_and_canonical(self):
        page = ca.extract_page("https://hartline.test/", fixture("index.html"))
        self.assertEqual(page["title"], "Hartline Plumbing (sample) | Dallas Plumber, Same-Day Service")
        self.assertTrue(page["description"].startswith("A sample plumbing site"))
        self.assertEqual(page["canonical_html"], ["/"])
        self.assertTrue(page["viewport"])
        self.assertEqual(page["lang"], "en")
        self.assertEqual(page["h1_count"], 1)
        self.assertFalse(page["noindex"])
        self.assertIn("2145550100", page["tel"])
        self.assertEqual(page["schema"]["orgs"][0]["name"], "Hartline Plumbing (sample)")
        nav = [l for l in page["links_internal"] if l["pos"] == "nav"]
        self.assertEqual(len(nav), 4)
        self.assertEqual(sum(1 for i in page["images"] if i["alt"] is None), 1)

    def test_noindex_from_meta_and_scoped_header(self):
        old = ca.extract_page("https://hartline.test/old-offer/", fixture("old-offer/index.html"))
        self.assertTrue(old["noindex"])
        self.assertEqual(old["robots_meta"], ["noindex", "follow"])
        html = "<html><head><title>x</title></head><body><p>hi</p></body></html>"
        self.assertTrue(ca.extract_page("https://h.test/a", html, {"x-robots-tag": "googlebot: noindex"})["noindex"])
        self.assertFalse(ca.extract_page("https://h.test/a", html, {"x-robots-tag": "otherbot: noindex, nofollow"})["noindex"])
        self.assertTrue(ca.extract_page("https://h.test/a", html, {"x-robots-tag": "noindex"})["noindex"])

    def test_challenge_markers_ignore_normal_pages_with_recaptcha(self):
        normal = {"status": 200, "headers": {}, "body": b"<html>" + b"x" * 5000 + b"<script src='https://www.google.com/recaptcha/api.js'></script></html>"}
        self.assertIsNone(ca.challenge_markers(normal))
        blocked = {"status": 403, "headers": {}, "body": b"<html><body>Please complete the captcha</body></html>"}
        self.assertTrue(ca.challenge_markers(blocked))
        cf = {"status": 403, "headers": {"cf-mitigated": "challenge"}, "body": b""}
        self.assertIn("Cloudflare", ca.challenge_markers(cf))

    def test_js_shell_is_detected_but_a_small_static_page_is_not(self):
        shell = ('<html><head><title>App</title></head><body><div id="root"></div>'
                 '<script src="/static/app.js"></script></body></html>')
        self.assertTrue(ca.extract_page("https://h.test/", shell)["js_shell"])
        small = "<html><head><title>Tiny</title></head><body><h1>Hello</h1><p>A short static page.</p></body></html>"
        self.assertFalse(ca.extract_page("https://h.test/", small)["js_shell"])


class ContentSignals(unittest.TestCase):
    def test_article_signals(self):
        page = ca.extract_page("https://hartline.test/blog/water-heater-cost/", fixture("blog/water-heater-cost/index.html"))
        sig = page["signals"]
        self.assertEqual(sig["question_headings"], 3)
        self.assertEqual(sig["answer_capsules"], 1, "only the first answer is short, self-contained and link-light")
        self.assertGreaterEqual(sig["stats"], 4)
        self.assertGreaterEqual(sig["quotations"], 1)
        self.assertEqual(sig["cited_sources"], 1)
        self.assertEqual(sig["visible_date"], "October 20, 2026")
        self.assertEqual(sig["newest_date"], "2026-10-20")
        self.assertEqual(sig["author"], "Dana Reyes")
        self.assertEqual(len(page["schema"]["parse_errors"]), 1)
        self.assertIn("BlogPosting", page["schema"]["types"])

    def test_dates_parse_without_guessing(self):
        self.assertEqual(str(ca.parse_date("Sept 3, 2026")), "2026-09-03")
        self.assertEqual(str(ca.parse_date("3 March 2025")), "2025-03-03")
        self.assertIsNone(ca.parse_date("03/04/2025"))


class Findings(unittest.TestCase):
    def build(self):
        audit = make_audit()
        audit.host = "hartline.test"
        audit.origin = "https://hartline.test"
        audit.home_url = "https://hartline.test/"
        audit.robots_by_host = {"hartline.test": ca.Robots("User-agent: *\nDisallow: /wp-admin/\n")}
        pages = {
            "https://hartline.test/": fixture("index.html"),
            "https://hartline.test/services/": fixture("services/index.html"),
            "https://hartline.test/old-offer/": fixture("old-offer/index.html"),
            "https://hartline.test/blog/water-heater-cost/": fixture("blog/water-heater-cost/index.html"),
        }
        for url, html in pages.items():
            audit.record_page(url, fake_response(url, html), 0 if url.endswith(".test/") else 1, "link")
        audit.record_page("https://hartline.test/contact/", fake_response("https://hartline.test/contact/", "Not found", status=404), 1, "link")
        audit.sitemap_urls = {"https://hartline.test/", "https://hartline.test/services/", "https://hartline.test/old-offer/"}
        audit.site = {"robots": {"state": "present", "url": "https://hartline.test/robots.txt", "sitemaps_declared": ["x"]},
                      "sitemap": {"state": "present", "files": [], "url_count": 3, "truncated": False}}
        audit.prepare()
        return audit

    def test_noindex_in_sitemap_is_reported_with_its_evidence(self):
        findings, fine = self.build().analyze()
        by_id = {f["id"]: f for f in findings}
        self.assertIn("noindex_in_sitemap", by_id)
        f = by_id["noindex_in_sitemap"]
        self.assertEqual(f["urls"], ["https://hartline.test/old-offer/"])
        self.assertEqual(f["severity"], "high")
        self.assertIn("meta robots: noindex, follow", f["examples"][0]["detail"])
        self.assertNotIn("noindex_pages", by_id, "a page reported in the sitemap finding isn't reported twice")

    def test_broken_nav_link_and_fine_list(self):
        findings, fine = self.build().analyze()
        by_id = {f["id"]: f for f in findings}
        self.assertEqual(by_id["broken_internal_links"]["severity"], "critical", "linked from the homepage menu")
        self.assertIn("https://hartline.test/contact/", by_id["broken_internal_links"]["urls"])
        fine_ids = {x["id"] for x in fine}
        self.assertIn("robots_blocks_google", fine_ids)
        self.assertNotIn("robots_blocks_google", by_id)
        for f in findings:
            self.assertTrue(f["observation"], f["id"])
            self.assertIn(f["severity"], ca.SEVERITY_ORDER)

    def test_calibrated_severities(self):
        self.assertEqual(ca.CHECKS["llms_txt_missing"]["severity"], "info")
        self.assertEqual(ca.CHECKS["no_structured_data"]["severity"], "info")
        self.assertEqual(ca.CHECKS["title_length"]["severity"], "low")
        self.assertEqual(ca.CHECKS["robots_blocks_google"]["severity"], "critical")
        self.assertEqual(ca.CHECKS["noindex_key_pages"]["severity"], "critical")

    def test_cwv_ratings_and_compare(self):
        self.assertEqual(ca.Audit.rate("lcp_ms", 2600), "needs improvement")
        self.assertEqual(ca.Audit.rate("cls", 0.3), "poor")
        old = {"generated_at": "a", "findings": [{"id": "x", "severity": "high", "title": "X", "count": 3},
                                               {"id": "y", "severity": "low", "title": "Y", "count": 1}]}
        new = {"findings": [{"id": "x", "severity": "high", "title": "X", "count": 1},
                            {"id": "z", "severity": "critical", "title": "Z", "count": 1}]}
        ch = ca.compare(old, new)
        self.assertEqual([c["id"] for c in ch["new"]], ["z"])
        self.assertEqual([c["id"] for c in ch["resolved"]], ["y"])
        self.assertEqual(ch["changed"][0]["count"], [3, 1])


class AutoCompare(unittest.TestCase):
    def test_auto_compare_picks_the_same_site_only(self):
        root = Path(tempfile.mkdtemp())
        for folder, url in (("site-audit-hartline-test-2026-11-01", "https://www.hartline.test/"),
                            ("site-audit-other-test-2026-11-10", "https://other.test/")):
            (root / "campaigns" / folder).mkdir(parents=True)
            (root / "campaigns" / folder / "findings.json").write_text(json.dumps({"final_url": url, "findings": []}))
        cwd = os.getcwd()
        os.chdir(root)
        try:
            found = ca.find_previous(Path("campaigns/site-audit-hartline-test-2026-11-16"), "hartline.test")
        finally:
            os.chdir(cwd)
        self.assertEqual(found.parent.name, "site-audit-hartline-test-2026-11-01")


class _FixtureHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        path = self.path.split("?")[0]
        if path.endswith((".txt", ".xml")) and (SITE / path.lstrip("/")).is_file():
            body = (SITE / path.lstrip("/")).read_text(encoding="utf-8").replace("{{BASE}}", f"http://{self.headers['Host']}").encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain" if path.endswith(".txt") else "application/xml")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_HEAD(self):
        super().do_HEAD()


class TinyCrawl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = functools.partial(_FixtureHandler, directory=str(SITE))
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def run_crawl(self, out, *extra):
        with redirect_stdout(io.StringIO()):
            code = ca.main([self.base + "/", "--out", out, "--no-psi", "--delay", "0", "--quiet", "--max-minutes", "1", *extra])
        self.assertEqual(code, 0)
        return json.loads((Path(out) / "findings.json").read_text())

    def test_crawl_finds_the_planted_problems(self):
        out = tempfile.mkdtemp()
        data = self.run_crawl(out)
        by_id = {f["id"]: f for f in data["findings"]}
        self.assertIn(self.base + "/old-offer/", by_id["noindex_in_sitemap"]["urls"])
        self.assertTrue({self.base + "/contact/", self.base + "/gone/"} <= set(by_id["broken_internal_links"]["urls"]))
        self.assertIn(self.base + "/services/drain-cleaning", by_id["internal_links_to_redirects"]["urls"])
        self.assertEqual(data["site"]["sitemap"]["state"], "present")
        self.assertEqual(data["site"]["sitemap"]["url_count"], 6)
        self.assertEqual(data["site"]["ai_crawlers"]["GPTBot"]["state"], "blocked")
        self.assertEqual(data["site"]["ai_crawlers"]["OAI-SearchBot"]["state"], "allowed")
        self.assertEqual(data["site"]["edge_check"]["bots"]["OAI-SearchBot"]["verdict"], "allowed")
        self.assertIn("Core Web Vitals", [n["what"] for n in data["not_checked"]])
        self.assertTrue((Path(out) / "pages.jsonl").is_file())
        # a re-audit against the first run reports what changed
        again = self.run_crawl(tempfile.mkdtemp(), "--compare", str(Path(out) / "findings.json"))
        self.assertIn("changes", again)
        self.assertEqual(again["changes"]["new"], [])
        self.assertEqual(again["changes"]["resolved"], [])


if __name__ == "__main__":
    unittest.main()
