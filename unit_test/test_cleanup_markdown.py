import unittest
from nttt import cleanup_markdown


class TestCleanupMarkdown(unittest.TestCase):
    logging = "off"

    def test_all_spaces(self):
        c_initial = 'asd _ fgh _ asd ` ghj ` asd ** hjk ** asd * uio * asd'
        c_target = 'asd _fgh_ asd `ghj` asd **hjk** asd *uio* asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_left_spaces(self):
        c_initial = 'asd _ fgh_ asd ` ghj` asd ** hjk** asd * uio* asd'
        c_target = 'asd _fgh_ asd `ghj` asd **hjk** asd *uio* asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_right_spaces(self):
        c_initial = 'asd _fgh _ asd `ghj ` asd **hjk ** asd *uio * asd'
        c_target = 'asd _fgh_ asd `ghj` asd **hjk** asd *uio* asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_multiple_spaces(self):
        c_initial = 'asd _    fgh _ asd ` ghj    ` asd **    hjk ** asd * uio    * asd'
        c_target = 'asd _fgh_ asd `ghj` asd **hjk** asd *uio* asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_a_case_of_one(self):
        c_initial = 'asd _    fgh _ asd'
        c_target = 'asd _fgh_ asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_a_case_of_two(self):
        c_initial = 'asd _    fgh _ asd ` ghj    ` asd'
        c_target = 'asd _fgh_ asd `ghj` asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_a_case_of_three(self):
        c_initial = 'asd _    fgh _ asd ` ghj    ` asd * uio    * asd'
        c_target = 'asd _fgh_ asd `ghj` asd *uio* asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_two_underscores(self):
        c_initial = 'asd _    fgh _ asd _ ghj    _ asd'
        c_target = 'asd _fgh_ asd _ghj_ asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_two_asterisks(self):
        c_initial = 'asd *    fgh * asd * ghj    * asd'
        c_target = 'asd *fgh* asd *ghj* asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_two_double_asterisks(self):
        c_initial = 'asd **    fgh ** asd ** ghj    ** asd'
        c_target = 'asd **fgh** asd **ghj** asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_capital_letters(self):
        c_initial = 'asd **    fGh ** asd ** ghJ    ** asd'
        c_target = 'asd **fGh** asd **ghJ** asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_numbers(self):
        c_initial = 'asd **    fGh76 ** asd ** g23hJ    ** asd'
        c_target = 'asd **fGh76** asd **g23hJ** asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_double_triple_asterisks(self):
        c_initial = 'asd **    fGh76 ** asd *** g23hJ    *** asd'
        c_target = 'asd **fGh76** asd ***g23hJ*** asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_double_triple_underscores(self):
        c_initial = 'asd __    fGh76 __ asd ___ g23hJ    ___ asd'
        c_target = 'asd __fGh76__ asd ___g23hJ___ asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_underscore_in_asterisks(self):
        c_initial = 'asd **    _fGh76 ** asd *** g23_hJ    *** asd'
        c_target = 'asd **_fGh76** asd ***g23_hJ*** asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_underscore_in_underscores(self):
        c_initial = 'asd __    f_Gh76 __ asd ___ g23_hJ    ___ asd'
        c_target = 'asd __f_Gh76__ asd ___g23_hJ___ asd'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_md_inside_backquotes(self):
        c_initial = '`foo ** bar ** baz`'
        c_target = '`foo ** bar ** baz`'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_list_item(self):
        c_initial = '* list item 1'
        c_target = '* list item 1'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_list_item_italic(self):
        c_initial = '* list item * 1 *'
        c_target = '* list item *1*'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_list_item_italic_multiline(self):
        c_initial = '* list item * 1 *\n* list item * 2 *'
        c_target = '* list item *1*\n* list item *2*'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_list_item_italic_with_whitespaces(self):
        c_initial = ' \t* list item * 1 *'
        c_target = ' \t* list item *1*'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_italic_start(self):
        c_initial = '* not a list item *'
        c_target = '*not a list item*'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_tripple_backtick(self):
        c_initial = '* some text * \n' \
                    '```\n' \
                    ' 3! = 3 * 2 * 1 \n' \
                    '```\n ' \
                    '_ some other text _'
        c_target = '*some text* \n' \
                   '```\n' \
                   ' 3! = 3 * 2 * 1 \n' \
                   '```\n' \
                   ' _some other text_'
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)

    def test_misc(self):
        c_initial = "`de hele tijd` en `bij opstarten`"
        c_target = "`de hele tijd` en `bij opstarten`"
        self.assertEqual(cleanup_markdown.trim_md_tags(c_initial, self.logging), c_target)


if __name__ == '__main__':
    unittest.main()
