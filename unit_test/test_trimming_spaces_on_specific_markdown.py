import unittest
import nttt


class TestTrimSpaces(unittest.TestCase):
    def test_all_spaces(self):
        c_initial = 'asd _ fgh _ asd ` ghj ` asd ** hjk ** asd * uio * asd'
        c_target = 'asd _fgh_ asd `ghj` asd **hjk** asd *uio* asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test_left_spaces(self):
        c_initial = 'asd _ fgh_ asd ` ghj` asd ** hjk** asd * uio* asd'
        c_target = 'asd _fgh_ asd `ghj` asd **hjk** asd *uio* asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test_right_spaces(self):
        c_initial = 'asd _fgh _ asd `ghj ` asd **hjk ** asd *uio * asd'
        c_target = 'asd _fgh_ asd `ghj` asd **hjk** asd *uio* asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__multiple_spaces(self):
        c_initial = 'asd _    fgh _ asd ` ghj    ` asd **    hjk ** asd * uio    * asd'
        c_target = 'asd _fgh_ asd `ghj` asd **hjk** asd *uio* asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test_a_case_of_one(self):
        c_initial = 'asd _    fgh _ asd'
        c_target = 'asd _fgh_ asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test_a_case_of_two(self):
        c_initial = 'asd _    fgh _ asd ` ghj    ` asd'
        c_target = 'asd _fgh_ asd `ghj` asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__a_case_of_three(self):
        c_initial = 'asd _    fgh _ asd ` ghj    ` asd * uio    * asd'
        c_target = 'asd _fgh_ asd `ghj` asd *uio* asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__two_underscores(self):
        c_initial = 'asd _    fgh _ asd _ ghj    _ asd'
        c_target = 'asd _fgh_ asd _ghj_ asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__two_asterisks(self):
        c_initial = 'asd *    fgh * asd * ghj    * asd'
        c_target = 'asd *fgh* asd *ghj* asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__two_double_asterisks(self):
        c_initial = 'asd **    fgh ** asd ** ghj    ** asd'
        c_target = 'asd **fgh** asd **ghj** asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__capital_letters(self):
        c_initial = 'asd **    fGh ** asd ** ghJ    ** asd'
        c_target = 'asd **fGh** asd **ghJ** asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__numbers(self):
        c_initial = 'asd **    fGh76 ** asd ** g23hJ    ** asd'
        c_target = 'asd **fGh76** asd **g23hJ** asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__double_triple_asterisks(self):
        c_initial = 'asd **    fGh76 ** asd *** g23hJ    *** asd'
        c_target = 'asd **fGh76** asd ***g23hJ*** asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__double_triple_underscores(self):
        c_initial = 'asd __    fGh76 __ asd ___ g23hJ    ___ asd'
        c_target = 'asd __fGh76__ asd ___g23hJ___ asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__underscore_in_asterisks(self):
        c_initial = 'asd **    _fGh76 ** asd *** g23_hJ    *** asd'
        c_target = 'asd **_fGh76** asd ***g23_hJ*** asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__underscore_in_underscores(self):
        c_initial = 'asd __    f_Gh76 __ asd ___ g23_hJ    ___ asd'
        c_target = 'asd __f_Gh76__ asd ___g23_hJ___ asd'
        self.assertEqual(nttt.cleanup_markdown.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__cleanup_markdown_dictionaries_same_length(self):
        self.assertEqual(len(nttt.cleanup_markdown.regular_expressions_matrix_for_trimming_spaces), len(nttt.cleanup_markdown.corrections_for_trimming_spaces))



if __name__ == '__main__':
    unittest.main()
