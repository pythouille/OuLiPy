import unittest

from src.utils import *



class TestIsPalindrom(unittest.TestCase):
    def test_remove(self):
        self.assertEqual(remove_non_word("fenouil"), "fenouil")
        self.assertEqual(remove_non_word("À-côtés"), "Àcôtés") # Accents
        self.assertEqual(remove_non_word("!:;,Ahah,;:!"), "Ahah") # Punctuation
        self.assertEqual(remove_non_word(" Ah  ah\t\tah\nah  "), "Ahahahah") # White space
        self.assertEqual(remove_non_word("Parfois, ou peut-être pas (!) ?"), "Parfoisoupeutêtrepas") # Both

    def test_is_palindrom(self):
        self.assertFalse(is_palindrom("fenouil"))
        self.assertTrue(is_palindrom("kayak"))
        #TODO
        #self.assertTrue(is_palindrom("XxXx")) # Not case sensitive
        #self.assertTrue(is_palindrom("x\nx x\tx   ")) # Not sensitive to white space
        #self.assertTrue(is_palindrom("x..x!x?!!x")) # Not sensitive to punctuation
        #self.assertTrue(is_palindrom("Ésope reste ici et se repose."))



if __name__ == '__main__':
    unittest.main()
