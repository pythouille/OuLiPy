"""
This module contains functions to check properties in strings.
"""
from collections import Counter
import string
from typing import List



####
# Global variables
####

vowels_char = "AEIOUY"
consonants_char = "BCDFGHJKLMNPQRSTVWXZ"

accent_to_letter = { # Non exhaustive list
    # Lower case
    'â': 'a', 'ä': 'a', 'á': 'a', 'à': 'a', 'ã': 'a',
    'ê': 'e', 'ë': 'e', 'é': 'e', 'è': 'e',
    'î': 'i', 'ï': 'i', 'í': 'i', 'ì': 'i',
    'ô': 'o', 'ö': 'o', 'ó': 'o', 'ò': 'o', 'õ': 'o',
    'û': 'u', 'ü': 'u', 'ú': 'u', 'ù': 'u',
              'ÿ': 'y', 'ý': 'y',           'ñ': 'n',
    'ç': 'c',
    # Upper case
    'Â': 'A', 'Ä': 'A', 'Á': 'A', 'À': 'A', 'Ã': 'A',
    'Ê': 'E', 'Ë': 'E', 'É': 'E', 'È': 'E',
    'Î': 'I', 'Ï': 'I', 'Í': 'I', 'Ì': 'I',
    'Ô': 'O', 'Ö': 'O', 'Ó': 'O', 'Ò': 'O', 'Õ': 'O',
    'Û': 'U', 'Ü': 'U', 'Ú': 'U', 'Ù': 'U',
              'Ÿ': 'Y', 'Ý': 'Y',           'Ñ': 'N',
    'Ç': 'C',
}
accents_char = ''.join(accent_to_letter.keys())
ligature_to_letter = {'æ':'ae', 'œ':'oe', 'Æ':'AE', 'Œ': 'OE'}
ligatures_char = ''.join(ligature_to_letter.keys())

low_ascender_char = ''.join([ # Accent outside the mean line
    'â', 'ä', 'á', 'à', 'ã',
    'ê', 'ë', 'é', 'è',
    'î', 'ï', 'í', 'ì',
    'ô', 'ö', 'ó', 'ò', 'õ',
    'û', 'ü', 'ú', 'ù', 
    'ç', 'ñ',
])
ascender_char = (
    "bdfklt"
    + "'!\"&\'()*/?[\\]^`{|}'" # Punctuation
    + string.ascii_uppercase # Uppercase
    + low_ascender_char.upper() # Uppercase with accent
)
low_descender_char = ",;"
descender_char = "gjpqy"


####
# Utils
####

def remove_punctuation(s: str, replace_char='') -> str:
    """
    Return a copy of given string without
    its punctuation.
    """
    s_copy = s
    for c in string.punctuation:
        if c in s_copy:
            s_copy = s_copy.replace(c, replace_char)
    return s_copy

def remove_non_word(s: str, replace_char='') -> str:
    """
    Return a copy of given string without
    its punctuation and white space (which
    are non-word character).
    """
    s_copy = s
    for c in string.punctuation:
        if c in s_copy:
            # (whitespace to ensure separation)
            s_copy = s_copy.replace(c, ' ')
    for c in string.whitespace:
        # Replace all whitespace, and erased punctuation
        if c in s_copy:
            s_copy = s_copy.replace(c, replace_char)
    return s_copy

def remove_accent(s: str) -> str:
    """
    Return a copy of given string without
    any accents.
    """
    s_copy = s
    for c in s_copy:
        if c in accents_char:
            s_copy = s_copy.replace(c, accent_to_letter[c])
        elif c not in (
                string.ascii_letters
                + string.punctuation
                + string.whitespace
                + ligatures_char
                ):
            print(f"WARNING: unknown character: {c}")
    return s_copy

def remove_ligature(s: str) -> str:
    """
    Return a copy of given string with ligature
    replaced by separated letters.
    """
    s_copy = s
    for c in ligatures_char:
        s_copy = s_copy.replace(c, ligature_to_letter[c])
    return s_copy

def to_letters(s: str) -> str:
    """
    Return a copy of given text with only its letters,
    standardized to uppercase, without accent or
    ligature, remove all non-word characters and spaces.
    """
    return remove_non_word(
        remove_accent(
            remove_ligature(
                s.upper()
            )
        )
    )

def to_words(s: str, letters_only=False) -> list[str]:
    """
    Return a list of the words in given text.

    White space and punctuation are discarded.
    """
    # Remove punctuation and standardize white space
    s_copy = remove_punctuation(s, replace_char=' ')
    for w in string.whitespace:
        if w in s_copy:
            s_copy = s_copy.replace(w, ' ')
    # Get words (ignore empty strings)
    words = [w for w in s_copy.split(' ') if w]
    if letters_only:
        words = [to_letters(w) for w in words]
    return words

def to_lines(s: str, letters_only=False) -> list[str]:
    """
    Return a list of lines in given text.
    """
    # Get non-blank lines
    lines = [line for line in s.split('\n') if line]
    # Clean lines
    if letters_only:
        lines = [to_letters(line) for line in lines]

    return lines

def filter_letters(s: str, filter: str) -> str:
    """
    Return a string that contains only the letters
    in source text.

    White space, punctuation and accents are discarded.

    Parameters
    ----------
    s : str
        Target text.
    filter : str
        All the letters that are preserved in output string.
        Other letters are removed.
    """
    # Clean data
    s_copy = to_letters(s)
    filter = to_letters(filter)
    # Get target letters only
    s_filtered = []
    for char in s_copy:
        if char in filter:
            s_filtered.append(char)

    return ''.join(s_filtered)

def to_vowels(s: str) -> str:
    """
    Return a string that contains only the vowels
    in source text.

    White space, punctuation and accents are discarded.
    """
    return filter_letters(s, vowels_char)

def to_consonants(s: str) -> str:
    """
    Return a string that contains only the consonants
    in source text.

    White space, punctuation and accents are discarded.
    """
    return filter_letters(s, consonants_char)

def letter_counter(s: str) -> Counter:
    """
    Return a Counter of letters in the text.

    Spaces, punctuation, accents are discarded.
    """
    return Counter(to_letters(s))

def word_counter(s: str, letters_only=False) -> Counter:
    """
    Return a Counter of words of in the text.
    """
    return Counter(to_words(s, letters_only=letters_only))

def chunk(s: str, n: int) -> list[str]:
    """
    Return a list of string of size n, extracted
    from successive letters in given string 's'.
    """
    s_copy = to_letters(s)

    chunk_list = []
    char_pointer = 0
    while char_pointer < len(s_copy):
        chunk_list.append(s_copy[char_pointer:char_pointer+n])
        char_pointer += n

    return chunk_list

def count_common(s1: str, s2: str) -> int:
    """
    Return the number of letters that are
    present in both words.
    """
    s1_letters = to_letters(s1)
    s2_letters = to_letters(s2)
    count = 0
    for c in s1_letters:
        if c in s2_letters:
            count += 1
    return count


####
# Constraint checker
####

def check_isosceles(s: str) -> bool:
    """
    Return True if all the lines in given
    text share the same number of characters
    (whitespace included); False otherwise.
    """
    # Get distinct strictly positive lengths
    line_lengths = set([len(line) for line in to_lines(s) if line])
    # Check the number of distinct line lengths
    return len(line_lengths) <= 1

def check_palindrom(s: str) -> bool:
    """
    Return True if given text is a palindrom, False otherwise.
    In a palindrom of size N, the i-th and (N-i)-th letters
    are the same for every i.

    Punctuation, spaces, accents and cases are ignored.

    Notes
    -----
    This function only check palindrom of letters.

    See also:
    - https://en.wikipedia.org/wiki/Palindrome
    - https://zazipo.net/+-Palindrome-+
    """
    s_copy =  to_letters(s)
    for i in range(len(s_copy)//2):
        if s_copy[i] != s_copy[len(s_copy)-1-i]:
            return False
    return True

def check_antipalindrom(s: str) -> bool:
    """
    Return True if given text is a anti-palindrom, False otherwise.
    In an anti-palindrom of size N, the i-th and (N-i)-th letters
    are always different.

    Punctuation, spaces, accents and cases are ignored.
    """
    s_copy = to_letters(s)
    for i in range(len(s_copy)//2):
        if s_copy[i] == s_copy[len(s_copy)-1-i]:
            return False
    return True

def check_beaupresent(s: str, ref: str) -> bool:
    """
    Return True if given text uses only letters that are
    also present in reference string, False otherwise.

    Parameters
    ----------
    s : str
        Source text.
    ref : str
        Word, or name, containing the only letters
        that can be used in source text.

    Notes
    -----
    See also:
    - https://oulipo.net/fr/contraintes/beau-present
    - https://www.zazipo.net/+-Beau-present-+
    """
    # 
    s_copy = to_letters(s)
    ref_letters = to_letters(ref)

    # Check constraint
    for c in s_copy:
        if c not in ref_letters:
            return False
    return True

def check_lipogram(s: str, forbidden: str) -> bool:
    """
    Return True if given text ('s') does not contain
    any character in 'forbidden' string, False otherwise.

    For example, a lipogram in 'E' must not use the letter
    E (with or without accent, with or without uppercase).

    Notes
    -----
    See also: https://www.oulipo.net/fr/contraintes/lipogramme
    """
    s_copy = to_letters(s)
    forbidden = to_letters(forbidden)
    for c in s_copy:
        if c in forbidden:
            return False
    return True

def check_monovocalism(s: str, vowel=None) -> bool:
    """
    Return True if there is only one vowel used in the text,
    False otherwise.

    Parameters
    ----------
    s : str
        Text to check.
    vowel : str, optional
        Single character, the only vowel that can be used in
        the text. Two or more vowel can also be given for
        bivocalism, trivocalism etc. Defaults to None
        (any vowel can be used, but only one for all the text).

    Notes
    -----
    See also:
    - https://www.zazipo.net/+-Monovocalisme-609-+
    - https://www.oulipo.net/fr/contraintes/monovocalisme
    - https://www.oulipo.net/fr/contraintes/bivocalisme
    """
    s_vowels = set(to_vowels(s))
    n_vowels = len(s_vowels)
    if n_vowels > 1:
        return False
    if vowel:
        vowel_upper = vowel.upper()
        if not (set(vowel_upper) < set(vowels_char)):
            raise ValueError(f"Please chose target voyel in {vowels_char}.")
        if vowel_upper not in s_vowels:
            return False
    return True

def check_heteroconsonantism(s: str) -> bool:
    """
    Return True if all consonants of source text are
    different, False otherwise.

    Notes
    -----
    See also: https://zazipo.net/+-Heteroconsonnantisme-+
    """
    if not s:
        return True
    s_consonants = to_consonants(s)
    # All consonants
    n_consonants = len(s_consonants)
    # All distinct consonants
    n_different_consonants = len(set(s_consonants))
    return n_consonants == n_different_consonants

def check_turkish(s: str) -> bool:
    """
    Return True if the text can be read without moving the lips
    ("vers turcs", i.e. approximatively lipogram in B, F, M, P, V).
    Return False otherwise.

    Note
    ----
    Currently, this function only checks the absence of B, F, M, P and V,
    which is an approximation. In reality, the constraint is focused on
    pronounciation. For example, the French word 'compte' has M and P
    but they are not pronounced, so it should normally verify the
    constraint. However, current implementation of the function would
    return False.
    """
    return check_lipogram(s, forbidden="BFMPV")

def check_prisoner(s: str, allow_accent=True) -> bool:
    """
    Return True if given text follow the 'prisoner's constraint',
    False otherwise. In other words, its letters must not have
    any ascenders (like in 'l', 'k', 'h'...) nor descenders
    ('y', 'j'...).

    Parameters
    ----------
    s : str
        Source text.
    allow_accent : bool, optional.
        If True, accents and small ascenders are tolerated.
        Otherwise, it follows the 'strict' prisoner's
        constraint. Defaults to True.    

    Notes
    -----
    See also:
    - https://zazipo.net/+-Prisonnier-+
    - https://fr.wikipedia.org/wiki/Contrainte_du_prisonnier
    """
    # Build list of forbidden characters
    forbidden_char = descender_char + ascender_char
    if not allow_accent:
        # Avoid accents too, if specified
        forbidden_char += low_ascender_char + low_descender_char
    # Check each character
    for c in s:
        if c in forbidden_char:
            return False
    return True

def check_released_prisoner(s: str) -> bool:
    """
    Return True if all letters given text, except vowels
    have ascenders or descenders, False otherwise.

    Notes
    -----
    See also: https://fr.wikipedia.org/wiki/Contrainte_du_prisonnier
    """
    return check_beaupresent(
        s=s,
        ref='bdfghjklpqt' + vowels_char + ligatures_char
    )

def check_okapi(s: str) -> bool:
    """
    Return True if source has is an alternation
    of vowels and consonants, False otherwise.

    Notes
    -----
    See also: https://zazipo.net/+-Okapi-+
    """
    if not s:
        return True
    # Extract letters only
    s_copy = to_letters(s)
    # Check alternation
    previous_is_vowel = s_copy[0] in vowels_char
    for c in s_copy[1:]:
        if c in vowels_char:
            if previous_is_vowel:
                # Double vowel detected
                return False
            previous_is_vowel = True
        elif c in consonants_char:
            if not previous_is_vowel:
                # Double consonant detected
                return False
            previous_is_vowel = False
        else:
            raise RuntimeError(f"Unknown vowel or consonant: {c}")

    return True

def check_tautogram(s: str, start_with=None) -> bool:
    """
    Return True if all the words in the text
    begin with the same letter, False otherwise.

    Parameters
    ----------
    s : str
        Text to check.
    start_with : str, optional
        Single character imposed at the beginning of each word.
        Default value is the first letter of the text.
    
    Notes
    -----
    See also:
    - https://www.oulipo.net/fr/contraintes/tautogramme
    - https://zazipo.net/+-Tautogramme-+
    """
    # Remove accent, uppercase, and get words only
    words = to_words(s, letters_only=True)
    if start_with is None:
        if not s:
            return True
        start_with = words[0][0].upper()
    elif len(start_with) != 1:
        raise ValueError("'start_with' must be only one character.")
    else:
        start_with = start_with.upper()
    # Check each word
    for w in words:
        if w[0] != start_with:
            return False
    return True

def check_acrostic(s: str, ref: str, by_words=False, check_length=True) -> bool:
    """
    Return True if all the lines (or words) begin by
    the letters of the reference word, in order;
    False otherwise.

    Parameters
    ----------
    s : str
        Target text.
    ref : str
        Characters to be found at the beginning of each line or words.
    by_words : bool, optional
        If False, check the beginning of each line. If True,
        check the beginning of each word. Defaults to False.
    check_length : bool, optional
        If True, target text must have exactly the same number
        of lines (or words) as the reference text. Defaults to
        True.
    
    Notes
    -----
    See also: https://zazipo.net/+-Acrostiche-+
    """
    # Remove accent, uppercase, and get words only
    if by_words:
        units = to_words(s, letters_only=True)
    else:
        units = to_lines(s, letters_only=True)
    ref = to_letters(ref)

    if check_length and (len(units) != len(ref)):
        return False
    for i, u in enumerate(units):
        if u[0] != ref[i%len(ref)]:
            return False
    return True

def check_progressive_tautogram(s: str, ref: str) -> bool:
    """
    Return True if the beginning of each successive word
    in given text follow the order of given reference
    (looping on given characters), False otherwise.

    Parameters
    ----------
    s : str
        Text to check.
    ref : str
        Characters to be found at the beginning of each words,
        successively.
    
    Notes
    -----
    See also: https://www.oulipo.net/fr/contraintes/tautogramme-progressif
    """
    return check_acrostic(
        s=s,
        ref=ref,
        by_words=True,
        check_length=False
    )

def check_universal_acrostic(s: str) -> bool:
    """
    Return True if all 26 lines in given text
    begin with the successive letters in latin
    alphabet, False otherwise.

    Notes
    -----
    See also: https://www.oulipo.net/fr/contraintes/acrostiche-universel
    """
    return check_acrostic(
        s=s,
        ref=string.ascii_uppercase,
        by_words=False
    )

def check_abecedaire(s: str) -> bool:
    """
    Return True if all 26 words in given text
    begin with the successive letters in latin
    alphabet (an 'abécédaire'), False otherwise. 

    Notes
    -----
    See also:
    - https://www.oulipo.net/fr/contraintes/abecedaire
    - https://zazipo.net/+-Abecedaire-756-+
    """
    return check_acrostic(
        s,
        ref=string.ascii_uppercase,
        by_words=True
    )

def check_kyrielle(s: str) -> bool:
    """
    Return True if the last letter of each word
    is the same letter as the first letter of the
    following word ('kyrielle').
    """
    words = to_words(s, letters_only=True)
    for i in range(len(words)-1):
        if words[i][-1] != words[i+1][0]:
            return False
    return True

def check_sympathetic(s: str, min=1) -> bool:
    """
    Return True if all successive words in given text
    share at least one (or more) letters, False otherwise.

    Parameters
    ----------
    s : str
        Text to check.
    min : int, optional
        Minimal required number of common letters
        between each successive words. Defaults to 1. 

    Notes
    -----
    See also: https://zazipo.net/+-Sympathique-+
    """
    words = to_words(s, letters_only=True)
    for i in range(len(words)-1):
        if count_common(words[i], words[i+1]) < min:
            return False
    return True

def check_snob(s: str) -> bool:
    """
    Return True if all successive words in given text
    share no common letter, False otherwise.

    Notes
    -----
    See also: https://zazipo.net/+-Snob-+
    """
    words = to_words(s, letters_only=True)
    for i in range(len(words)-1):
        if count_common(words[i], words[i+1]) != 0:
            return False
    return True

def check_ngram(s: str, n=None) -> bool:
    """
    Return True if each word in given text has the same number
    of letters, or if this number matches given value(s).

    Parameters
    ----------
    s : str
        Source text.
    n : int or list of int, optional
        Required length(s) for each word of given text.
        By default, only check that all the words have
        the same length.

    Notes
    -----
    See also: https://zazipo.net/+-X-gramme-+
    """
    # Extract word lengths
    words_lengths = [len(word) for word in to_words(s)]
    if not words_lengths:
        return True
    words_lengths.sort()

    if n is None:
        # Default case:
        # All the word must have the same length
        return len(set(words_lengths)) <= 1
    elif isinstance(n, int):
        if len(set(words_lengths)) > 1:
            # More than one possible length
            return False
        return words_lengths[0] == n
    elif isinstance(n, list):
        # Check that extracted lengths are authorized
        for l in words_lengths:
            if l not in n:
                # Forbidden value
                return False
        return True
    else:
        raise ValueError("'n' argument must be an integer, or a list of integer.")

def check_maxgram(s: str, m: int):
    """
    Return True if each word in given text is 'm' letters
    long or smaller.

    Parameters
    ----------
    s : str
        Source text.
    m : int
        If given, each word must have 'max' letters or less.
   
    Notes
    -----
    See also: https://zazipo.net/+-X-gramme-+
    """
    # Extract words length
    words_lengths = [len(word) for word in to_words(s)]
    if not words_lengths:
        return True
    words_lengths.sort()

    # Compare to highest value
    return words_lengths[-1] <= m

def check_mingram(s: str, m: int):
    """
    Return True if each word in given text is at least
    'm' letters long.

    Parameters
    ----------
    s : str
        Source text.
    m : int
        If given, each word must have 'm' letters or more.

    Notes
    -----
    See also: https://zazipo.net/+-X-gramme-+
    """
    # Extract words length
    words_lengths = [len(word) for word in to_words(s)]
    if not words_lengths:
        return True
    words_lengths.sort()

    # Compare to smallest value
    return words_lengths[0] >= m

def check_ananym(s1: str, s2: str) -> bool:
    """
    Return True if s1 and s2 use exactly the same
    words, the same amount of time, possibly with
    a different order; False otherwise.

    Notes
    -----
    See also: https://zazipo.net/+-Ananyme-+
    """
    w1 = word_counter(s1, letters_only=True)
    w2 = word_counter(s2, letters_only=True)
    return w1 == w2

def check_arithmonym(s: str, other_s: str = "") -> bool:
    """
    Return True if each line of given text has
    the same number of words, False otherwise.
    If a second string is given, return True if
    both strings have the same number of words.
    """
    if other_s:
        return len(to_words(s)) == len(to_words(other_s))
    lines = to_lines(s)

    n_words = [
        len(to_words(line))
        for line in lines
    ]
    return len(set(n_words)) <= 1

def check_anagram(s1: str, s2: str) -> bool:
    """
    Return True if s1 and s2 use exactly the same
    letters, the same amount of time; False otherwise.

    Notes
    -----
    See also:
    - https://www.oulipo.net/fr/contraintes/anagramme
    - https://zazipo.net/+-Anagramme-+
    """
    return letter_counter(s1) == letter_counter(s2)

def check_subanagram(s_sub: str, s_ref: str) -> bool:
    """
    Return True if all the letter in s_sub are contained
    in s_ref.
    """
    return letter_counter(s_sub) <= letter_counter(s_ref)

def check_heterogram(s: str, ref: str = 'ULCERATIONS') -> bool:
    """
    Return True if given text is built by successive anagrams
    of given reference text.

    Parameters
    ----------
    s : str
        Source text.
    ref : str, optional
        Reference word, or letters, to follow.
        Defaults to 'ULCERATIONS', or the 11 most used
        letters in French.
    
    Notes
    -----
    - https://www.zazipo.net/+-Heterogramme-+
    - https://www.zazipo.net/+-Ulcerations-+
    """
    ref_letters = to_letters(ref)

    chunks = chunk(s, len(ref_letters))
    for c in chunks:
        if not check_anagram(c, ref_letters):
            return False
    return True

def check_ulcerations(s: str, tone='C'):
    """
    Return True if given text is an heterogram
    based on 'Ulcerations', with possibly a
    specific letter instead of 'C'.

    Parameters
    ----------
    s : str
        Source text.
    tone : str, optional
        Reference letter to be added to the 10 most
        common letters in French. Defaults to 'C'
        ("Ul(c)érations sur ton de C").

    Notes
    -----
    - https://www.zazipo.net/+-Heterogramme-+
    - https://www.zazipo.net/+-Ulcerations-+
    """
    return check_heterogram(s, ref="UL_ERATIONS"+tone)

def check_pangram(s: str, alphabet=None) -> bool:
    """
    Return True if the text contains all letters of the
    alphabet, at least once. False otherwise.

    By default, it checks the 26 letters of latin alphabet.

    Parameters
    ----------
    s : str
        Source text.
    alphabet : str, optional
        Check a given alphabet. Defaults to None.
    
    Notes
    -----
    See also: https://zazipo.net/+-Pangramme-+
    """
    if alphabet is None:
        # By default, latin alphabet
        alphabet = string.ascii_uppercase

    return check_subanagram(alphabet, s)

def check_panscrabblogram(s: str, lang='fr') -> bool:
    """
    Return True if the text is made of (and only of)
    all the letters in a box of Scrabble.

    #TODO: add 2 jokers

    Parameters
    ----------
    s : str
        Source text.
    lang: str in {'fr', 'en'}
        Language of reference. Available languages
        are French ('fr') and English ('en').
        Defaults to French.
    
    Notes
    -----
    See also: https://zazipo.net/+-Panscrabblogramme-594-+
    """
    available_lang = {
        # French
        'fr': "AAAAAAAAABBCCDDDEEEEEEEEEEEEEEEFFGGHHIIIIIIIIJKLLLLLMMMNNNNNNOOOOOOPPQRRRRRRSSSSSSTTTTTTUUUUUUVVWXYZ",
        # English
        'en': "AAAAAAAAABBCCDDDDEEEEEEEEEEEEFFGGGHHIIIIIIIIIJKLLLLMMNNNNNNOOOOOOOOPPQRRRRRRSSSSTTTTTTUUUUVVWWXYYZ"
    }
    if lang not in available_lang:
        raise ValueError(f"'lang' argument must be in {set(available_lang.keys())}")

    return check_anagram(available_lang[lang], s)

def check_belleabsente(s: str, ref: str = None) -> bool:
    """
    Return True if the i-th line does not contain the i-th
    letter of a reference word, False otherwise. Each line
    must also contain each other letter of the alphabet
    (except K, W, X, Y and Z).

    Parameters
    ----------
    s : str
        Source text.
    ref : str, optional
        Word, or name, containing the letters
        that are forbidden in the successive
        lines of the source text.

    Notes
    -----
    See also:
    - https://zazipo.net/+-Belle-absente-505-+
    - https://oulipo.net/fr/contraintes/belle-absente
    """
    # Clean arguments
    lines = to_lines(s, letters_only=True)
    if ref:
        ref = to_letters(ref)
        if len(lines) != len(ref):
            # Must have as many lines as letters in target word
            return False
    # Check each line
    for i, line in enumerate(lines):
        letters = set(line)
        missing_letters = set(string.ascii_uppercase).difference(letters)
        if not missing_letters:
            # One letter should be missing
            return False
        if ref:
            if ref[i] not in missing_letters:
                # A forbidden letter have been found
                return False
        # Remove unnecessary K, W, X, Y and Z
        missing_letters = missing_letters.difference(set('KWXYZ'))
        if len(missing_letters) > 1:
            # Several possible letters... There should be only one
            return False
    return True

def check_asupposer(s: str) -> bool:
    """
    Return True if the text is made of one long sentence,
    False otherwise. In other wordes, this function checks
    that there is no terminal punctuation (./!/?) and that
    there are more than 1000 characters.

    Notes
    -----
    See also:
    - https://www.oulipo.net/fr/contraintes/a-supposer
    - https://zazipo.net/+-A-supposer-502-+
    """
    size = len(s)
    # Consider '...' as authorized punctuation
    s_copy = s.replace('...', '')
    # Look for sentence endings
    for p in ['.', '!', '?']:
        if p in s_copy[:-1]:
            return False
    # Check minimal length
    return size >= 1000


####
# Operations, statistics
####

gematria_dict = { # From http://www.gef.free.fr/gem.php
    # Latin par rang
    'latin_rank': {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6,
        'G': 7, 'H': 8, 'I': 9, 'J': 9, 'K': 10, 'L': 11, 'M': 12,
        'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18,
        'T': 19, 'U': 20, 'V': 20, 'X': 21, 'Y': 22, 'Z': 23
    },
    # Latin classique
    'latin_classic': {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6,
        'G': 7, 'H': 8, 'I': 9, 'J': 9, 'K': 10, 'L': 20, 'M': 30,
        'N': 40, 'O': 50, 'P': 60, 'Q': 70, 'R': 80, 'S': 90,
        'T': 100, 'U': 200, 'V': 200, 'X': 300, 'Y': 400, 'Z': 500
    },
    # Latin carré
    'latin_square': {
        'A': 1, 'B': 4, 'C': 9, 'D': 16, 'E': 25, 'F': 36,
        'G': 49, 'H': 64, 'I': 81, 'J': 81, 'K': 100, 'L': 400, 'M': 900,
        'N': 1600, 'O': 2500, 'P': 3600, 'Q': 4900, 'R': 6400, 'S': 8400,
        'T': 10000, 'U': 40000, 'V': 40000, 'X': 90000, 'Y': 160000, 'Z': 250000
    },
    # Français par rang
    'french_rank': {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6,
        'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13,
        'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19,
        'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26
    },
    # Français classique
    'french_classic': {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6,
        'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 20, 'L': 30, 'M': 40,
        'N': 50, 'O': 60, 'P': 70, 'Q': 80, 'R': 90, 'S': 100,
        'T': 200, 'U': 300, 'V': 400, 'W': 500, 'X': 600, 'Y': 700, 'Z': 800
    },
    # Français moins classique
    'french_classic': {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6,
        'G': 7, 'H': 8, 'I': 9, 'K': 10, 'L': 20, 'M': 30,
        'N': 40, 'O': 50, 'P': 60, 'Q': 70, 'R': 80, 'S': 90,
        'T': 100, 'U': 110, 'V': 120, 'W': 130, 'X': 140, 'Y': 150, 'Z': 160
    },
    # Jacob-Abraham Soubira
    'jacob_abraham_soubira': {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6,
        'G': 7, 'H': 8, 'I': 9, 'K': 10, 'L': 20, 'M': 30,
        'N': 40, 'O': 50, 'P': 60, 'Q': 70, 'R': 80, 'S': 90,
        'T': 100, 'U': 110, 'V': 120, 'W': 240, 'X': 130, 'Y': 140, 'Z': 150
    },
    # Code de Cheiro
    'cheiro_code': {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 8,
        'G': 3, 'H': 5, 'I': 1, 'J': 1, 'K': 2, 'L': 3, 'M': 4,
        'N': 5, 'O': 7, 'P': 8, 'Q': 1, 'R': 2, 'S': 3,
        'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 5, 'Y': 1, 'Z': 7
    },
    # Chiffres romains
    'roman_numeral': {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    },
    # Scrabble français
    'scrabble_fr': {
        'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4,
        'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 10, 'L': 1, 'M': 2,
        'N': 1, 'O': 1, 'P': 3, 'Q': 8, 'R': 1, 'S': 1,
        'T': 1, 'U': 1, 'V': 4, 'W': 10, 'X': 10, 'Y': 10, 'Z': 10
    },
    # Scrabble anglais
    'scrabble_en': {
        'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4,
        'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3,
        'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1,
        'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
    },
    # Nombre de lettres
    'n_letters': {
        'A': 1, 'B': 1, 'C': 1, 'D': 1, 'E': 1, 'F': 1,
        'G': 1, 'H': 1, 'I': 1, 'J': 1, 'K': 1, 'L': 1, 'M': 1,
        'N': 1, 'O': 1, 'P': 1, 'Q': 1, 'R': 1, 'S': 1,
        'T': 1, 'U': 1, 'V': 1, 'W': 1, 'X': 1, 'Y': 1, 'Z': 1
    },
}

def gematria(s: str, mapping='french_rank') -> int:
    """
    Return the gematria value for each word
    of given text. The gematria of the word is the
    sum of the value of each of its letters, following
    given mapping.
    """
    return sum(gematria_words(s=s, mapping=mapping))

def gematria_words(s: str, mapping='french_rank') -> list[int]:
    """
    Return the list of gematria value for each word
    of given text. The gematria of the word is the
    sum of the value of each of its letters, following
    given mapping.
    """
    if not isinstance(mapping, dict) and mapping not in gematria_dict:
        raise ValueError(f"'mapping' argument must be in: {set(gematria_dict.keys())}")
    letter_to_value = gematria_dict[mapping]
    words = to_words(s, letters_only=True)

    gematria_list = []
    for word in words:
        sum = 0
        for letter in word:
            sum += letter_to_value[letter]
        gematria_list.append(sum)
    return gematria_list

def gematria_lines(s: str, mapping='french_rank') -> list[int]:
    """
    Return the gematria value for each word
    of given text. The gematria of the word is the
    sum of the value of each of its letters, following
    given mapping.
    """
    lines = to_lines(s)
    gematria_list = [
        gematria(line, mapping=mapping)
        for line in lines if line
    ]
    return gematria_list


####
# Transformations
####

# ...
