import unittest
from nttt import cleanup_formatting


class TestCleanupFormatting(unittest.TestCase):
    logging = "off"

    def test_multiple_tags(self):
        init = '`point up`{ : class = "block3motion"} and `go to the start position`{: class="block3motion" }.'
        out = '`point up`{:class="block3motion"} and `go to the start position`{:class="block3motion"}.'

        self.assertEqual(cleanup_formatting.trim_formatting_tags(init, self.logging), out)

    def test_space_between_md_content_and_tag(self):
        init = '`point up` {:class="block3motion"}'
        out = '`point up`{:class="block3motion"}'

        self.assertEqual(cleanup_formatting.trim_formatting_tags(init, self.logging), out)

    def test_space_between_word_and_tag(self):
        init = 'time  {:class="block3variables"}'
        out = 'time{:class="block3variables"}'

        self.assertEqual(cleanup_formatting.trim_formatting_tags(init, self.logging), out)

    def test_printer_friendly_link(self):
        init = '[ printvriendelijke versie ]' \
               '(https://projects.raspberrypi.org/en/projects/boat-race/print) {:target="_blank"}.'
        out = '[ printvriendelijke versie ]' \
              '(https://projects.raspberrypi.org/en/projects/boat-race/print){:target="_blank"}.'

        self.assertEqual(cleanup_formatting.trim_formatting_tags(init, self.logging), out)

    def test_fix_value(self):
        init = 'link{: target = " blank"}'
        out = 'link{:target="blank"}'

        self.assertEqual(cleanup_formatting.trim_formatting_tags(init, self.logging), out)


if __name__ == '__main__':
    unittest.main()
