import unittest
from nttt import cleanup_formatting


class TestCleanupFormatting(unittest.TestCase):
    def test_basic_space_removal(self):
        init = "{ : xxx = \"yyy\" }"
        out = "{:xxx=\"yyy\"}"

        self.assertEqual(cleanup_formatting.trim_formatting_tags(init, "off"), out)

    def test_multiple_tags(self):
        init = "`point up`{ : class = \"block3motion\"} and `go to the start position`{: class=\"block3motion\" }."
        out = "`point up`{:class=\"block3motion\"} and `go to the start position`{:class=\"block3motion\"}."

        self.assertEqual(cleanup_formatting.trim_formatting_tags(init, "off"), out)

    # TODO test removal of space before the entire formatting tag


if __name__ == '__main__':
    unittest.main()
