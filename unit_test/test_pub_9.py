import sys
sys.path.insert(1, '../nttt/')

import unittest
#import nttt
import utilities


class TestPub9(unittest.TestCase):
    def test_pub_9(self):
    
        c_initial = 'asd _ fgh _ asd ` ghj ` asd ** hjk ** asd * uio * asd'
        c_target = 'asd _fgh_ asd `ghj` asd **hjk** asd *uio* asd'
        
        self.assertEqual(utilities.trim_pub_9(c_initial), c_target)
    


if __name__ == '__main__':
    unittest.main()
