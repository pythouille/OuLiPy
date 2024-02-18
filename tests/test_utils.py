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
        self.assertTrue(check_monovocalism("Être et n'être, tel est le Cerbère.", 'e'))
        self.assertTrue(check_monovocalism("Être et n'être, tel est le Cerbère.")) # Find E
        self.assertFalse(check_monovocalism("Être et n'être, tel est le Cerbère.", 'a'))
        self.assertFalse(check_monovocalism("fenouil"))
        self.assertFalse(check_monovocalism("kayak"))

    def test_turkish(self):
        self.assertTrue(check_turkish(""))
        self.assertTrue(check_turkish("kayak"))
        self.assertTrue(check_turkish("Il était une noix..."))
        self.assertFalse(check_turkish("fenouil")) # forbidden F
        self.assertFalse(check_turkish("Il était une fois...")) # F 
        self.assertFalse(check_turkish("Il était un pois...")) # P
        self.assertFalse(check_turkish("Il était un mois...")) # M
        self.assertFalse(check_turkish("Il était un bois...")) # B
        self.assertFalse(check_turkish("Il était une voix...")) # V
        # Silent letters: not handled in current version:
        #self.assertTrue(check_turkish("compte")) # Silent M and P

    def test_prisoner(self):
        self.assertTrue(check_prisoner(""))
        self.assertTrue(check_prisoner("sans un son, sans un sou"))
        self.assertTrue(check_prisoner("un réseau")) # 'é' allowed by default
        self.assertFalse(check_prisoner("fenouil"))
        self.assertFalse(check_prisoner("fenouil", allow_accent=False))
        self.assertFalse(check_prisoner("Xxxx.")) # uppercase
        self.assertFalse(check_prisoner("cinq")) # descender
        self.assertFalse(check_prisoner("j")) # descender
        self.assertFalse(check_prisoner("un réseau", allow_accent=False)) # 'é'
        self.assertFalse(check_prisoner("sans un son, sans un sou", allow_accent=False)) # ','

    def test_tautogram(self):
        self.assertTrue(check_tautogram(""))
        self.assertTrue(check_tautogram("fenouil"))
        self.assertTrue(check_tautogram("Fenouil furibond faisant finement fi !"))
        self.assertTrue(check_tautogram("Fenouil furibond faisant finement fi !", "f"))
        self.assertFalse(check_tautogram("Fenouil furibond faisant finement fi !", "a"))
        self.assertFalse(check_tautogram("Fenouil furibond faisant gras !")) # F != G

    def test_abecedaire(self):
        self.assertTrue(check_abecedaire(
            "Axxx. Bxxx, cxéxxx dxx exxxx, fxxx gxxxxxx. "\
            "Hxxxèx, ixxx jxxxx Kxx, lx Mx nxxxxxxxx... "\
            "Oxxxx pxxxxx ! Qxxx Rxxx sx txxxxxxx : "\
            "uxxx vxxxx wxxxxx xxxxxx y zxxxxxxxx."\
        ))
        self.assertFalse(check_abecedaire("")) # Empty case
        self.assertFalse(check_abecedaire("fenouil"))
        self.assertFalse(check_abecedaire(
            "Axxx. Bxxx, cxéxxx dxx exxxx, fxxx gxxxxxx. "\
            "Hxxxèx, ixxx jxxxx Kxx, lx Mx nxxxxxxxx... "\
            "Oxxxx qxxxxx ! Qxxx Rxxx sx txxxxxxx : "\
            "uxxx vxxxx wxxxxx xxxxxx y zxxxxxxxx."\
        )) # Q after O, instead of P
    
    def test_kyrielle(self):
        self.assertTrue(check_kyrielle("")) # Empty case
        self.assertTrue(check_kyrielle("fenouil"))
        self.assertTrue(check_kyrielle("fenouil luisant")) # l-l
        self.assertTrue(check_kyrielle("toujours si inépuisable")) # s-s i-i
        self.assertTrue(check_kyrielle("Touché. En naissant !")) # e-e n-n
        self.assertFalse(check_kyrielle("fenouil enragé")) # L != E

    def test_anagram(self):
        self.assertTrue(check_anagram("", "")) # Empty case
        self.assertTrue(check_anagram("abcd", "dbca"))
        self.assertTrue(check_anagram("Sourient:", "Routines !"))
        self.assertTrue(check_anagram("eee", "Éeê"))
        self.assertFalse(check_anagram("abc", "aabc")) # Missing letter
        self.assertFalse(check_anagram("abc", "abd")) # Changing letter



if __name__ == '__main__':
    unittest.main()
