import unittest
from nttt import utilities


class TestUtilities(unittest.TestCase):
    def test_apply_to_every_other_part(self):
        def f(s, param):
            return s + param

        init = "a*b*c"
        exp_result = "a1*b*c1"

        self.assertEqual(utilities.apply_to_every_other_part(init, "*", f, "1"), exp_result)
