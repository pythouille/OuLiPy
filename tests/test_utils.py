import unittest

from src.utils import *



class TestConstraintChecker(unittest.TestCase):
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

    def test_to_vowels(self):
        self.assertEqual(to_vowels(""), "")
        self.assertEqual(to_vowels("fenouil"), "eoui")
        self.assertEqual(to_vowels("Oiseau"), "oieau")
        self.assertEqual(to_vowels("Être hébété, oui."), "eeeeeoui")

    def test_to_consonants(self):
        self.assertEqual(to_consonants(""), "")
        self.assertEqual(to_consonants("fenouil"), "fnl")
        self.assertEqual(to_consonants("Un joli jalapeño."), "njljlpn")

    def test_to_words(self):
        self.assertEqual(to_words(""), [])
        self.assertEqual(to_words("fenouil"), ["fenouil"])
        self.assertEqual(to_words("Il était une fois,"), ["Il", "était", "une", "fois"])
        #NOTE: need for treating separate cases for "'" or "-"?
        #self.assertEqual(to_words("Aujourd'hui, c'est lundi ! Eh."), ["Aujourd'hui", "c", "est", "lundi", "Eh"])

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

    def test_beaupresent(self):
        self.assertTrue(check_beaupresent("", "Gilles Esposito-Farèse"))
        self.assertTrue(check_beaupresent("Le positif était effaré.", "Gilles Esposito-Farèse"))
        self.assertFalse(check_beaupresent("fenouil", "Gilles Esposito-Farèse"))

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

    def test_heteroconsonantism(self):
        self.assertTrue(check_heteroconsonantism("Ab. Cdf; ghjkl emnpqrstvwxz !"))
        self.assertFalse(check_heteroconsonantism(""))
        self.assertFalse(check_heteroconsonantism("fenouil"))

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

    def test_okapi(self):
        self.assertTrue(check_okapi(""))
        self.assertTrue(check_okapi("E"))
        self.assertTrue(check_okapi("okapi"))
        self.assertTrue(check_okapi("Je me dis à mi-mot..."))
        self.assertFalse(check_okapi("fenouil"))
        self.assertFalse(check_okapi("Patatra !"))

    def test_tautogram(self):
        self.assertTrue(check_tautogram(""))
        self.assertTrue(check_tautogram("fenouil"))
        self.assertTrue(check_tautogram("Fenouil furibond faisant finement fi !"))
        self.assertTrue(check_tautogram("Fenouil furibond faisant finement fi !", "f"))
        self.assertFalse(check_tautogram("Fenouil furibond faisant finement fi !", "a"))
        self.assertFalse(check_tautogram("Fenouil furibond faisant gras !")) # F != G

    def test_acrostic(self):
        self.assertTrue(check_acrostic("", ""))
        self.assertTrue(check_acrostic("fenouil", "f"))
        self.assertTrue(check_acrostic("fenouil", "f", by_words=True))
        self.assertTrue(check_acrostic("Il était une fois...", "ieuf", by_words=True))
        self.assertTrue(check_acrostic("Il \nétait \nune \nfois...", "ieuf"))
        self.assertFalse(check_acrostic("Il était une fois...", "ieu", by_words=True))
        self.assertFalse(check_acrostic("Il était une xxxx...", "ieuf", by_words=True))
        self.assertFalse(check_acrostic("Il était une...", "ieuf", by_words=True))

    def test_universal_acrostic(self):
        self.assertTrue(check_universal_acrostic(
            "A\nb\nc\nd\ne\nf\ng\nh\ni\nj\n"\
            "k\nl\nm\nn\no\np\nq\nr\ns\nt\n"\
            "u\nv\nw\nx\ny\nz"
        ))
        self.assertFalse(check_universal_acrostic(""))
        self.assertFalse(check_universal_acrostic("fenouil"))
        self.assertFalse(check_universal_acrostic(
            "A\nb\nc\nd\ne\nf\ng\nh\ni\nj\n"\
            "k\nl\nm\nn\no\np\nq\nr\ns\nt\n"\
            "X\nv\nw\nx\ny\nz"
        )) # X instead of U

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

    def test_sympathetic(self):
        self.assertTrue(check_sympathetic(""))
        self.assertTrue(check_sympathetic("fenouil"))
        self.assertTrue(check_sympathetic("Un fenouil cuit")) # nu, ui
        self.assertTrue(check_sympathetic("Un fenouil cuit", min=2)) # nu, ui
        self.assertFalse(check_sympathetic("Un fenouil cuit", min=3)) # nu, ui
        self.assertFalse(check_sympathetic("Fenouil, ahah !"))
    
    def test_snob(self):
        self.assertTrue(check_snob(""))
        self.assertTrue(check_snob("fenouil"))
        self.assertTrue(check_snob("Ça ! Quel gras fenouil !"))
        self.assertFalse(check_snob("Un fenouil cuit"))

    def test_ngram(self):
        self.assertTrue(check_ngram("", 7))
        self.assertTrue(check_ngram("fenouil", 7))
        self.assertTrue(check_ngram("Halte au fenouil !", [2, 5, 7]))
        self.assertTrue(check_ngram("Ab bc cd, de, fg."))
        self.assertTrue(check_ngram("Ab bc cd, de, fg.", 2))
        self.assertFalse(check_ngram("Ab bc cd, de, fg.", 3))
        self.assertFalse(check_ngram("Ab bc cd, de, fgh.", 2))
        self.assertFalse(check_ngram("Halte au fenouil !", [5, 7]))

    def test_maxgram(self):
        self.assertTrue(check_maxgram("", 1))
        self.assertTrue(check_maxgram("fenouil", 8))
        self.assertTrue(check_maxgram("fenouil", 7))
        self.assertTrue(check_maxgram("Il y a un pb d'as.", 2))
        self.assertFalse(check_maxgram("Il y a un pb d'as.", 1))
        self.assertFalse(check_maxgram("fenouil", 6))

    def test_mingram(self):
        self.assertTrue(check_mingram("", 1))
        self.assertTrue(check_mingram("fenouil", 6))
        self.assertTrue(check_mingram("fenouil", 7))
        self.assertTrue(check_mingram("Quand trois gamins disent bonjour...", 5))
        self.assertFalse(check_mingram("Quand trois gamins disent bonjour...", 6))
        self.assertFalse(check_mingram("fenouil", 8))

    def test_anagram(self):
        self.assertTrue(check_anagram("", "")) # Empty case
        self.assertTrue(check_anagram("abcd", "dbca"))
        self.assertTrue(check_anagram("Sourient:", "Routines !"))
        self.assertTrue(check_anagram("eee", "Éeê"))
        self.assertFalse(check_anagram("abc", "aabc")) # Missing letter
        self.assertFalse(check_anagram("abc", "abd")) # Changing letter

    def test_subanagram(self):
        self.assertTrue(check_subanagram("", "")) # Empty case
        self.assertTrue(check_subanagram("a", "abc"))
        self.assertTrue(check_subanagram("abc", "aaabc"))
        self.assertTrue(check_subanagram("abbccc", "aaabbbccc"))
        self.assertTrue(check_subanagram("Sourient:", "Routines !")) # Anagram
        self.assertTrue(check_subanagram("Routines !", "Sourient:")) # and vice-versa
        self.assertTrue(check_subanagram("eee", "Éeêè")) # All letters included
        self.assertFalse(check_subanagram("eeee", "Éeê")) # Not enough letters
        self.assertFalse(check_subanagram("abc", "abd")) # Missing C in reference

    def test_heterogram(self):
        self.assertTrue(check_heterogram("", "ULCERATIONS")) # Empty case
        self.assertTrue(check_heterogram("ulcerations", "ULCERATIONS"))
        self.assertTrue(check_heterogram("Taclé, ou rins", "ULCERATIONS"))
        self.assertTrue(check_heterogram("Taclé, ou rinsul cé ra tison.", "ULCERATIONS"))
        self.assertFalse(check_heterogram("fenouil", "ULCERATIONS"))
        self.assertFalse(check_heterogram("lcerations", "ULCERATIONS"))
        self.assertFalse(check_heterogram("ulcerations, et...", "ULCERATIONS"))

    def test_pangram(self):
        self.assertTrue(check_pangram("Portez ce whisky au vieux juge blond qui fume."))
        self.assertFalse(check_pangram("Portez ce whisky au vieux juge blond qui gambade."))
        self.assertFalse(check_pangram(""))
        self.assertFalse(check_pangram("fenouil"))

    def test_panscrabblogram(self):
        self.assertTrue(check_panscrabblogram("YRLKFBUEEDSOOHOIEAEARUEIESUEECNOALEALIRTEFWENDAVTMEUMIQRANRIRTBTUHLECNNPAMPDJTOSEVAGXIZIENSTGUISLOAS", lang='fr'))
        self.assertTrue(check_panscrabblogram("YEHFEOQGDDAARLKIVTEEENFYTADTIOSIVUIRWLUGOSIMWCIPSOOLOETBNCEOIEUDAPNXGOAAERRTIZIASNRTRHLJMEEBUEAANN", lang='en'))
        self.assertFalse(check_panscrabblogram("YEHFEOQGDDAARLKIVTEEENFYTADTIOSIVUIRWLUGOSIMWCIPSOOLOETBNCEOIEUDAPNXGOAAERRTIZIASNRTRHLJMEEBUEAANN", lang='fr'))
        self.assertFalse(check_panscrabblogram(""))
        self.assertFalse(check_panscrabblogram("fenouil"))
        # Check Error for unknown language
        with self.assertRaises(ValueError):
            check_panscrabblogram("fenouil", lang='es')

    def test_asupposer(self):
        self.assertTrue(check_asupposer(
            "À supposer qu'on me demande ici de rédiger un à-supposer qui "\
            "soit à la fois une illustration plausible de ce qu'est un "\
            "à-supposer, mais qui soit aussi rigoureusement exact, "\
            "c'est-à-dire que le texte du présent test ne s'arrêtera que "\
            "lorsqu'il sera suffisamment long, non pas d'ailleurs pour le "\
            "simple plaisir de faire un texte long mais plutôt pour en faire "\
            "un sérieux, ceci n'empêchant pas de le faire avec plaisir, car "\
            "le sérieux dont on parle est le terme employé par Jacques Jouet,"\
            "inventeur de la contrainte, ladite contrainte qu'on retrouve à "\
            "sa bonne place expliquée sur le site de l'Oulipo, et toujours "\
            "habilement complété par l'excellent site de Zazipo également - "\
            "ou Zazie Mode d'Emploi peut-on dire également - qui ne manque "\
            "pas de rappeler le lien vers le premier site que nous évoquions, "\
            "et qui évoque, lui, sérieux d'un à-supposer comme dépendant d'un "\
            "nombre minimal de caractères, arbitrairement choisi ou peut-être "\
            "l'est-il pour des raisons plus métaphysiques dont j'ignorerais "\
            "la teneur... un minimum fixé à 1000."
        ))
        self.assertFalse(check_asupposer(
            "À supposer qu'on me demande ici de rédiger un à-supposer qui "\
            "soit à la fois une illustration plausible de ce qu'est un "\
            "à-supposer, MAIS QUI TERMINE UNE PHRASE EN PLEIN MILIEU ! "\
            "HÉLAS... alors que je préférerais promettre que "\
            "le texte du présent test ne s'arrêtera que "\
            "lorsqu'il sera suffisamment long, non pas d'ailleurs pour le "\
            "simple plaisir de faire un texte long mais plutôt pour en faire "\
            "un sérieux, ceci n'empêchant pas de le faire avec plaisir, car "\
            "le sérieux dont on parle est le terme employé par Jacques Jouet,"\
            "inventeur de la contrainte, ladite contrainte qu'on retrouve à "\
            "sa bonne place expliquée sur le site de l'Oulipo, et toujours "\
            "habilement complété par l'excellent site de Zazipo également - "\
            "ou Zazie Mode d'Emploi peut-on dire également - qui ne manque "\
            "pas de rappeler le lien vers le premier site que nous évoquions, "\
            "et qui évoque, lui, sérieux d'un à-supposer comme dépendant d'un "\
            "nombre minimal de caractères, arbitrairement choisi ou peut-être "\
            "l'est-il pour des raisons plus métaphysiques dont j'ignorerais "\
            "la teneur... un minimum fixé à 1000."
        ))
        self.assertFalse(check_asupposer(""))
        self.assertFalse(check_asupposer("fenouil"))



if __name__ == '__main__':
    unittest.main()
