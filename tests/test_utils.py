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

    def test_lipogram(self):
        self.assertFalse(is_lipogram("fenouil", "e"))
        self.assertTrue(is_lipogram("kayak", "e"))
        self.assertFalse(is_lipogram("E", "e")) # Case insensitive
        self.assertFalse(is_lipogram("ê", "e")) # Not sensitive to accents

    def test_prisoner(self):
        self.assertFalse(check_prisoner("fenouil"))
        self.assertFalse(check_prisoner("fenouil", allow_accent=False))
        self.assertFalse(check_prisoner("Xxxx."))
        self.assertFalse(check_prisoner("cinq"))
        self.assertFalse(check_prisoner("j"))
        self.assertTrue(check_prisoner("un réseau"))
        self.assertFalse(check_prisoner("un réseau", allow_accent=False)) # 'é'
        self.assertTrue(check_prisoner("sans un son, sans un sou"))
        self.assertFalse(check_prisoner("sans un son, sans un sou", allow_accent=False)) # ','

    def test_abecedaire(self):
        self.assertFalse(check_abecedaire("fenouil"))
        self.assertTrue(check_abecedaire(
            "Axxx. Bxxx, cxéxxx dxx exxxx, fxxx gxxxxxx. "\
            "Hxxxèx, ixxx jxxxx Kxx, lx Mx nxxxxxxxx... "\
            "Oxxxx pxxxxx ! Qxxx Rxxx sx txxxxxxx : "\
            "uxxx vxxxx wxxxxx xxxxxx y zxxxxxxxx."\
        ))
    
    def test_kyrielle(self):
        self.assertTrue(check_kyrielle(""))
        self.assertTrue(check_kyrielle("fenouil"))
        self.assertTrue(check_kyrielle("fenouil luisant"))
        self.assertFalse(check_kyrielle("fenouil enragé"))
        self.assertTrue(check_kyrielle("toujours si inépuisable"))
        self.assertTrue(check_kyrielle("Touché. En naissant !"))


if __name__ == '__main__':
    unittest.main()
