"""service-area overlap must compare Korean sentences, not only ASCII."""
import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "service-area-pages" / "scripts" / "overlap.py"
spec = importlib.util.spec_from_file_location("overlap", SCRIPT)
overlap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(overlap)

PAGE_A = """수성구 보일러 수리는 당일 출장으로 진행합니다. 출장비는 따로 받지 않고 기사님이 시간을 먼저 확인합니다. 견적은 현장에서 고장 부위를 본 뒤에 말씀드립니다.
"""
PAGE_B = PAGE_A.replace("수성구", "달서구")
PAGE_C = """중구 매장은 부품 판매만 하고 출장 수리는 하지 않습니다. 영업시간은 평일 오전 아홉 시부터 오후 여섯 시까지입니다. 주차는 건물 뒤편 두 대입니다.
"""


class OverlapKorean(unittest.TestCase):
    def test_hangul_sentences_survive_and_city_swap_matches(self):
        names = ["수성구", "달서구", "중구"]
        a = overlap.sentences(PAGE_A, names, 6)
        b = overlap.sentences(PAGE_B, names, 6)
        c = overlap.sentences(PAGE_C, names, 6)
        self.assertGreaterEqual(len(a), 2)
        self.assertTrue(any("보일러" in s for s in a))
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_cli_flags_the_swapped_pair(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "suseong.md").write_text(PAGE_A, encoding="utf-8")
            (root / "dalseo.md").write_text(PAGE_B, encoding="utf-8")
            (root / "jung.md").write_text(PAGE_C, encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                code = overlap.main([
                    str(root),
                    "--names", "수성구,달서구,중구",
                    "--format", "json",
                ])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
