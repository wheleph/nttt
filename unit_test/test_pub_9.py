import sys
sys.path.insert(1, '../')
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
    


if __name__ == '__main__':
    unittest.main()
