import unittest
from nttt import cleanup_html


class TestCleanupHtml(unittest.TestCase):
    logging = "off"

    def test_inside_spaces(self):
        init = "<p>   foo     </p>"

        out = "<p>foo</p>"

        self.assertEqual(cleanup_html.trim_html_tags(init, self.logging), out)

    def test_asymmetric_spaces(self):
        init_a = "<0>foo  </0>"
        init_b = "<0>   foo</0>"

        out = "<0>foo</0>"

        self.assertEqual(cleanup_html.trim_html_tags(init_a, self.logging), out)
        self.assertEqual(cleanup_html.trim_html_tags(init_b, self.logging), out)

    def test_spaced_tag_content(self):
        init = "<foo>  I'm spaced   </foo>"

        out = "<foo>I'm spaced</foo>"

        self.assertEqual(cleanup_html.trim_html_tags(init, self.logging), out)

    def test_trailing_hypen(self):
        init = "<faa>something</faa>-x"

        out = "<faa>something</faa>-x"

        self.assertEqual(cleanup_html.trim_html_tags(init, self.logging), out)

    def test_large_example(self):
        init = "something<p>   hey there     </p>-dutch foo faa<0>   fii</0>fii fuu <code>correct content</code>"

        out = "something<p>hey there</p>-dutch foo faa<0>fii</0>fii fuu <code>correct content</code>"

        self.assertEqual(cleanup_html.trim_html_tags(init, self.logging), out)

    def test_multiline(self):
        """
        Assume that if matching tags are located in different lines then the content should not be modified
        """
        init = "In XML there are 2 types of tags:\n " \
               "opening <foo>\n " \
               "and closing </foo>"

        out = init

        self.assertEqual(cleanup_html.trim_html_tags(init, self.logging), out)

    def test_non_matching(self):
        """
        Assume that content inside non-matching tags should not be corrected
        """
        init = "<0>   foo     </1>"

        out = init

        self.assertEqual(cleanup_html.trim_html_tags(init, self.logging), out)

    def test_curly_tags(self):
        init = '<0>foo</0>{:target="_blank"}'

        out = init

        self.assertEqual(cleanup_html.trim_html_tags(init, self.logging), out)

    def test_inside_backquotes(self):
        init = "`<table> </table>`"

        out = init

        self.assertEqual(cleanup_html.trim_html_tags(init, self.logging), out)

    def test_inside_backquotes2(self):
        init = "<h1> 1 </h1> `<h2> 2 </h2>` <h3> 3 </h3>"

        out = "<h1>1</h1> `<h2> 2 </h2>` <h3>3</h3>"

        self.assertEqual(cleanup_html.trim_html_tags(init, self.logging), out)

    def test_tripple_backtick(self):
        init = '<h1> some text </h1> \n' \
               '```\n' \
               ' <h3> some text </h3> \n' \
               '```\n ' \
               '<h2> some other text </h2>'
        out = '<h1>some text</h1> \n' \
              '```\n' \
              ' <h3> some text </h3> \n' \
              '```\n ' \
              '<h2>some other text</h2>'
        self.assertEqual(cleanup_html.trim_html_tags(init, self.logging), out)


if __name__ == '__main__':
    unittest.main()
