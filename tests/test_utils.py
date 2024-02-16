import unittest

from src.utils import *



class TestIsPalindrom(unittest.TestCase):
    def test_is_palindrom(self):
        self.assertTrue(is_palindrom("kayak"))
        self.assertFalse(is_palindrom("fenouil"))



if __name__ == '__main__':
    unittest.main()
