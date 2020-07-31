import unittest
import nttt


class TestPub9(unittest.TestCase):
    def test_all_spaces(self):
        c_initial = 'asd _ fgh _ asd ` ghj ` asd ** hjk ** asd * uio * asd'
        c_target = 'asd _fgh_ asd `ghj` asd **hjk** asd *uio* asd'
        self.assertEqual(nttt.utilities.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test_left_spaces(self):
        c_initial = 'asd _ fgh_ asd ` ghj` asd ** hjk** asd * uio* asd'
        c_target = 'asd _fgh_ asd `ghj` asd **hjk** asd *uio* asd'
        self.assertEqual(nttt.utilities.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test_right_spaces(self):
        c_initial = 'asd _fgh _ asd `ghj ` asd **hjk ** asd *uio * asd'
        c_target = 'asd _fgh_ asd `ghj` asd **hjk** asd *uio* asd'
        self.assertEqual(nttt.utilities.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__multiple_spaces(self):
        c_initial = 'asd _    fgh _ asd ` ghj    ` asd **    hjk ** asd * uio    * asd'
        c_target = 'asd _fgh_ asd `ghj` asd **hjk** asd *uio* asd'
        self.assertEqual(nttt.utilities.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test_a_case_of_one(self):
        c_initial = 'asd _    fgh _ asd'
        c_target = 'asd _fgh_ asd'
        self.assertEqual(nttt.utilities.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test_a_case_of_two(self):
        c_initial = 'asd _    fgh _ asd ` ghj    ` asd'
        c_target = 'asd _fgh_ asd `ghj` asd'
        self.assertEqual(nttt.utilities.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__a_case_of_three(self):
        c_initial = 'asd _    fgh _ asd ` ghj    ` asd * uio    * asd'
        c_target = 'asd _fgh_ asd `ghj` asd *uio* asd'
        self.assertEqual(nttt.utilities.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__two_underscores(self):
        c_initial = 'asd _    fgh _ asd _ ghj    _ asd'
        c_target = 'asd _fgh_ asd _ghj_ asd'
        self.assertEqual(nttt.utilities.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__two_asterisks(self):
        c_initial = 'asd *    fgh * asd * ghj    * asd'
        c_target = 'asd *fgh* asd *ghj* asd'
        self.assertEqual(nttt.utilities.trim_spaces_on_specific_markdown(c_initial), c_target)
    def test__two_double_asterisks(self):
        c_initial = 'asd **    fgh ** asd ** ghj    ** asd'
        c_target = 'asd **fgh** asd **ghj** asd'
        self.assertEqual(nttt.utilities.trim_spaces_on_specific_markdown(c_initial), c_target)
    


if __name__ == '__main__':
    unittest.main()
