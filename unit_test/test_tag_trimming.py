import unittest
from nttt import tag_trimming


class TestTagTrimming(unittest.TestCase):
    def test_inside_spaces(self):
        init = "<p>   foo     </p>"

        out = "<p>foo</p>"

        self.assertEqual(tag_trimming.trim_tags(init), out)

    def test_asymmetric_spaces(self):
        init_a = "<0>foo  </0>"
        init_b = "<0>   foo</0>"

        out = "<0>foo</0>"

        self.assertEqual(tag_trimming.trim_tags(init_a), out)
        self.assertEqual(tag_trimming.trim_tags(init_b), out)

    def test_spaced_tag_content(self):
        init = "<foo>  I'm spaced   </foo>"

        out = "<foo>I'm spaced</foo>"

        self.assertEqual(tag_trimming.trim_tags(init), out)

    def test_trailing_hypen(self):
        init = "<faa>something</faa>-x"

        out = "<faa>something</faa>-x"

        self.assertEqual(tag_trimming.trim_tags(init), out)

    def test_large_example(self):
        init = "something<p>   hey there     </p>-dutch foo faa<0>   fii</0>fii fuu <code>correct content</code>"

        out = "something<p>hey there</p>-dutch foo faa<0>fii</0>fii fuu <code>correct content</code>"

        self.assertEqual(tag_trimming.trim_tags(init), out)

    def test_multiline(self):
        """
        Assume that if matching tags are located in different lines then the content should not be modified
        """
        init = "In XML there are 2 types of tags:\n " \
               "opening <foo>\n " \
               "and closing </foo>"

        out = init

        self.assertEqual(tag_trimming.trim_tags(init), out)

    def test_non_matching(self):
        """
        Assume that content inside non-matching tags should not be corrected
        """
        init = "<0>   foo     </1>"

        out = init

        self.assertEqual(tag_trimming.trim_tags(init), out)

    def test_curly_tags(self):
        init = '<0>foo</0>{:target="_blank"}'

        out = init

        self.assertEqual(tag_trimming.trim_tags(init), out)


if __name__ == '__main__':
    unittest.main()
