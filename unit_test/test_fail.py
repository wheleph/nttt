import unittest


class FailTestCase(unittest.TestCase):
    def test_fail(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
