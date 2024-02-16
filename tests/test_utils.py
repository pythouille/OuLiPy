import unittest

from src.utils import *



class TestIsPalindrom(unittest.TestCase):
    def test_remove_non_word(self):
        self.assertEqual(remove_non_word("fenouil"), "fenouil")
        self.assertEqual(remove_non_word("À-côtés"), "Àcôtés") # Accents
        self.assertEqual(remove_non_word("!:;,Ahah,;:!"), "Ahah") # Punctuation
        self.assertEqual(remove_non_word(" Ah  ah\t\tah\nah  "), "Ahahahah") # White space
        self.assertEqual(remove_non_word("Parfois, ou peut-être pas (!) ?"), "Parfoisoupeutêtrepas") # Both

    def test_remove_accent(self):
        self.assertEqual(remove_accent("fenouil"), "fenouil")
        self.assertEqual(remove_accent("À-côtés"), "A-cotes")
        self.assertEqual(remove_accent("Deçà delà"), "Deca dela")

    def test_is_palindrom(self):
        self.assertFalse(is_palindrom("fenouil"))
        self.assertTrue(is_palindrom("kayak"))
        self.assertTrue(is_palindrom("XxXx")) # Not case sensitive
        self.assertTrue(is_palindrom("x\nx x\tx   ")) # Not sensitive to white space
        self.assertTrue(is_palindrom("x..x!x?!!x")) # Not sensitive to punctuation
        self.assertTrue(is_palindrom("Ésope reste ici et se repose."))
        self.assertFalse(is_palindrom("Xsope este ici et se repose."))
    
    def test_prisoner(self):
        self.assertFalse(check_prisoner("fenouil"))
        self.assertFalse(check_prisoner("Xxxx."))
        self.assertFalse(check_prisoner("j"))
        self.assertTrue(check_prisoner("un réseau"))
        self.assertFalse(check_prisoner("un réseau", allow_accent=False))



if __name__ == '__main__':
    unittest.main()
