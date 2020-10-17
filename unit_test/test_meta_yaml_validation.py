import unittest
from unit_test.test_helpers import AssertHelper


class TestMetadataValidation(unittest.TestCase):
    def test_revert_redundant_translations(self):
        AssertHelper.assert_fix_meta(
            "---\n"
            "title: Про мене\n"
            "theme: оранжевий\n"  # this should not be translated
            "description: Використовуй мову програмування Python для створення зображень з тексту\n"
            "technologies: python\n"  # this should not be translated
            "steps:\n"
            "  - title: Вступ\n",

            "---\n"
            "title: About me\n"
            "theme: orange\n"
            "description: Use the Python programming language to create pictures out of text\n"
            "technologies: python\n"
            "steps:\n"
            "  - title: Introduction\n",

            "---\n"
            "title: Про мене\n"
            "theme: orange\n"
            "description: Використовуй мову програмування Python для створення зображень з тексту\n"
            "technologies: python\n"
            "steps:\n"
            "  - title: Вступ\n")

    def test_extra_fields(self):
        AssertHelper.assert_fix_meta(
            "---\n"
            "title: Про мене\n"
            "technologies: python\n",

            "---\n"
            "title: About me\n",

            "---\n"
            "title: Про мене\n"
            "technologies: python\n")

    def test_cn_steps(self):
        AssertHelper.assert_fix_meta(
            "---\n"
            "title: 剪刀、石头、布\n"
            "description: 创建你自己的“剪刀、石头、布”游戏。\n"
            "steps:\n"
            "  - title: '挑战：ASCII码图像'\n",

            "---\n"
            "title: Rock, Paper, Scissors\n"
            "description: Create your own 'Rock, Paper Scissors' game.\n"
            "steps:\n"
            "  - title: 'Challenge: ASCII Art'\n",

            "---\n"
            "title: 剪刀、石头、布\n"
            "description: 创建你自己的“剪刀、石头、布”游戏。\n"
            "steps:\n"
            "  - title: '挑战：ASCII码图像'\n")


if __name__ == '__main__':
    unittest.main()
