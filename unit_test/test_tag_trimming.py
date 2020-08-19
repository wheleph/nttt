import unittest, nttt

class test_tag_trimming(unittest.TestCase):
    def test_inside_spaces(self):
        init = "<p>   foo     </p>"

        out = "<p>foo</p>"

        self.assertEqual(nttt.tag_trimming.trim_tags(init, 'any_lang'), out)

    def test_asymmetric_spaces(self):
        init_a = "<0>foo  </0>"
        init_b = "<0>   foo</0>"

        out = "<0>foo</0>"

        self.assertEqual(nttt.tag_trimming.trim_tags(init_a, 'any_lang'), out)
        self.assertEqual(nttt.tag_trimming.trim_tags(init_b, 'any_lang'), out)

    def test_preceding_leading_spaces(self):
        init_a = "a<1>foo</1> b"
        init_b = "a <1>foo</1>b"

        out = "a <1>foo</1> b"

        self.assertEqual(nttt.tag_trimming.trim_tags(init_a, 'any_lang'), out)
        self.assertEqual(nttt.tag_trimming.trim_tags(init_b, 'any_lang'), out)

    def test_spaced_tag_content(self):
        init = "<foo>  I'm spaced   </foo>"

        out = "<foo>I'm spaced</foo>"

        self.assertEqual(nttt.tag_trimming.trim_tags(init, 'any_lang'), out)

    def test_trailing_hypen(self):
        init = "<faa>something</faa>-x"

        out_not_dutch = "<faa>something</faa> -x"
        out_dutch = "<faa>something</faa>-x"

        self.assertEqual(nttt.tag_trimming.trim_tags(init, 'any_lang'), out_not_dutch)
        self.assertEqual(nttt.tag_trimming.trim_tags(init, 'nl-NL'), out_dutch)

    def test_large_example(self):
        init = "something<p>   hey there     </p>-dutch foo faa<0>   fii</0>fii fuu <code>correct content</code>"

        out_not_dutch = "something <p>hey there</p> -dutch foo faa <0>fii</0> fii fuu <code>correct content</code>"
        out_dutch = "something <p>hey there</p>-dutch foo faa <0>fii</0> fii fuu <code>correct content</code>"

        self.assertEqual(nttt.tag_trimming.trim_tags(init, 'any_lang'), out_not_dutch)
        self.assertEqual(nttt.tag_trimming.trim_tags(init, 'nl-NL'), out_dutch)

    def test_spaced_tag_content_legitimate(self):
        init = "In XML every opening tag (<foo>) should have a matching closing tag (</foo>)"

        out = "In XML every opening tag (<foo>) should have a matching closing tag (</foo>)"

        self.assertEqual(nttt.tag_trimming.trim_tags(init, 'any_lang'), out)

if __name__ == '__main__':
    unittest.main()