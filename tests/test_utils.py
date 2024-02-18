import unittest

from src.utils import *



class TestIsPalindrom(unittest.TestCase):
    def test_remove_non_word(self):
        self.assertEqual(remove_non_word(""), "")
        self.assertEqual(remove_non_word("fenouil"), "fenouil")
        self.assertEqual(remove_non_word("À-côtés"), "Àcôtés") # Accents
        self.assertEqual(remove_non_word("!:;,Ahah,;:!"), "Ahah") # Punctuation
        self.assertEqual(remove_non_word(" Ah  ah\t\tah\nah  "), "Ahahahah") # White space
        self.assertEqual(remove_non_word("Parfois, ou peut-être pas (!) ?"), "Parfoisoupeutêtrepas") # Both

    def test_remove_accent(self):
        self.assertEqual(remove_accent(""), "")
        self.assertEqual(remove_accent("fenouil"), "fenouil")
        self.assertEqual(remove_accent("À-côtés"), "A-cotes")
        self.assertEqual(remove_accent("Deçà delà"), "Deca dela")

    def test_split_words(self):
        self.assertEqual(split_words(""), [])
        self.assertEqual(split_words("fenouil"), ["fenouil"])
        self.assertEqual(split_words("Il était une fois,"), ["Il", "était", "une", "fois"])
        #NOTE: need for treating separate cases for "'" or "-"?
        #self.assertEqual(split_words("Aujourd'hui, c'est lundi ! Eh."), ["Aujourd'hui", "c", "est", "lundi", "Eh"])

    def test_palindrom(self):
        self.assertTrue(check_palindrom(""))
        self.assertTrue(check_palindrom("kayak"))
        self.assertTrue(check_palindrom("Ésope reste ici et se repose."))
        self.assertTrue(check_palindrom("XxXx")) # Not case sensitive
        self.assertTrue(check_palindrom("x\nx x\tx   ")) # Not sensitive to white space
        self.assertTrue(check_palindrom("x..x!x?!!x")) # Not sensitive to punctuation
        self.assertFalse(check_palindrom("Xsope este ici et se repose."))
        self.assertFalse(check_palindrom("fenouil"))

    def test_antipalindrom(self):
        self.assertTrue(check_antipalindrom(""))
        self.assertTrue(check_antipalindrom("fenouil")) # F!=L, E!=I, N!=U
        self.assertFalse(check_antipalindrom("kayak")) # Palindrom
        self.assertFalse(check_antipalindrom("blabla")) # L = L
        self.assertFalse(check_antipalindrom("Êxxxe")) # E = E, with accents
        self.assertFalse(check_antipalindrom("Hourrah !")) # H = H, with punctuation

    def test_lipogram(self):
        self.assertTrue(check_lipogram("", "e"))
        self.assertTrue(check_lipogram("kayak", "e"))
        self.assertTrue(check_lipogram("Parfois, j'ai froid.", "e"))
        self.assertFalse(check_lipogram("fenouil", "e"))
        self.assertFalse(check_lipogram("E", "e")) # Case insensitive
        self.assertFalse(check_lipogram("ê", "e")) # Not sensitive to accents

    def test_monovocalism(self):
        self.assertTrue(check_monovocalism(""))
        self.assertTrue(check_monovocalism("Étre et n'être, tel est le Cerbère."))
        self.assertTrue(check_monovocalism("Étre et n'être, tel est le Cerbère.", 'e'))
        self.assertFalse(check_monovocalism("Étre et n'être, tel est le Cerbère.", 'a'))
        self.assertFalse(check_monovocalism("fenouil"))
        self.assertFalse(check_monovocalism("kayak"))

    def test_prisoner(self):
        self.assertTrue(check_prisoner(""))
        self.assertFalse(check_prisoner("fenouil"))
        self.assertFalse(check_prisoner("fenouil", allow_accent=False))
        self.assertFalse(check_prisoner("Xxxx.")) # uppercase
        self.assertFalse(check_prisoner("cinq")) # descender
        self.assertFalse(check_prisoner("j")) # descender
        self.assertTrue(check_prisoner("un réseau")) # 'é' allowed by default
        self.assertFalse(check_prisoner("un réseau", allow_accent=False)) # 'é'
        self.assertTrue(check_prisoner("sans un son, sans un sou"))
        self.assertFalse(check_prisoner("sans un son, sans un sou", allow_accent=False)) # ','

    def test_abecedaire(self):
        self.assertFalse(check_abecedaire("")) # Empty case
        self.assertFalse(check_abecedaire("fenouil"))
        self.assertTrue(check_abecedaire(
            "Axxx. Bxxx, cxéxxx dxx exxxx, fxxx gxxxxxx. "\
            "Hxxxèx, ixxx jxxxx Kxx, lx Mx nxxxxxxxx... "\
            "Oxxxx pxxxxx ! Qxxx Rxxx sx txxxxxxx : "\
            "uxxx vxxxx wxxxxx xxxxxx y zxxxxxxxx."\
        ))
    
    def test_kyrielle(self):
        self.assertTrue(check_kyrielle("")) # Empty case
        self.assertTrue(check_kyrielle("fenouil"))
        self.assertTrue(check_kyrielle("fenouil luisant")) # l-l
        self.assertTrue(check_kyrielle("toujours si inépuisable")) # s-s i-i
        self.assertTrue(check_kyrielle("Touché. En naissant !")) # e-e n-n
        self.assertFalse(check_kyrielle("fenouil enragé")) # L != E



if __name__ == '__main__':
    unittest.main()
