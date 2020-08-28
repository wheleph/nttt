import unittest
from unit_test.test_meta_yaml_validation import AssertHelper


class TestEol(unittest.TestCase):
    def test_fix_metadata_crlf(self):
        AssertHelper.assert_fix_meta("---\r\n"
                                     "steps:\r\n"
                                     "  - \r\n"
                                     "    title: Inleiding\r\n",

                                     "---\r\n"
                                     "steps:\r\n"
                                     "  - \r\n"
                                     "    title: Introduction\r\n",

                                     "---\r\n"
                                     "steps:\r\n"
                                     "  - title: Inleiding\r\n")

    def test_fix_metadata_lf(self):
        AssertHelper.assert_fix_meta(
            "---\n"
            "steps:\n"
            "  - \n"
            "    title: Inleiding\n",

            "---\n"
            "steps:\n"
            "  - \n"
            "    title: Introduction\n",

            "---\n"
            "steps:\n"
            "  - title: Inleiding\n")

    def test_fix_collapse_block_crlf(self):
        AssertHelper.assert_fix_step("--- collapse ---\r\n"
                                     "\r\n"
                                     "## title: My title\r\n",

                                     "el-GR",

                                     "--- collapse ---\r\n"
                                     "---\r\n"
                                     "title: My title\r\n"
                                     "---\r\n")

    def test_fix_collapse_block_lf(self):
        AssertHelper.assert_fix_step("--- collapse ---\n"
                                     "\n"
                                     "## title: My title\n",

                                     "es-ES",

                                     "--- collapse ---\n"
                                     "---\n"
                                     "title: My title\n"
                                     "---\n")


if __name__ == '__main__':
    unittest.main()
