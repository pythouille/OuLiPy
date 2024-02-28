"""
This module contains functions to check properties in strings.
"""
from collections import Counter
import string
from typing import List



####
# Global variables
####

vowels_char = "aeiouy"
consonants_char = "bcdfghjklmnpqrstvwxz"

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
ligatures_char = ''.join(['æ', 'œ', 'Æ', 'Œ'])

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

def remove_non_word(s: str) -> str:
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
            s_copy = s_copy.replace(c, '')
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

def to_lines(s: str, letters_only=False) -> list[str]:
    """
    Return a list of lines in given text.
    """
    # Get non-blank lines
    lines = [line for line in s.split('\n') if line]
    # Clean lines
    if letters_only:
        lines = [remove_accent(remove_non_word(line)) for line in lines]

    return lines

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
    if letters_only:
        s_copy = remove_accent(s_copy)
    # Get words (ignore empty strings)
    words = [w for w in s_copy.split(' ') if w]
    return words

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
    s_copy = s.lower()
    s_copy = remove_non_word(s_copy)
    s_copy = remove_accent(s_copy)
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
    return Counter(remove_non_word(remove_accent(s.upper())))

def word_counter(s: str) -> Counter:
    """
    Return a Counter of words of in the text.
    """
    return Counter(to_words(s))

def count_common(s1: str, s2: str) -> int:
    """
    Return the number of letters that are
    present in both words.
    """
    s1_letters = remove_accent(s1.lower())
    s2_letters = remove_accent(s2.lower())
    count = 0
    for c in s1_letters:
        if c in s2_letters:
            count += 1
    return count


####
# Constraint checker
####

def check_palindrom(s: str) -> bool:
    """
    Return True if given text is a palindrom, False otherwise.
    In a palindrom of size N, the i-th and (N-i)-th letters
    are the same for every i.

    Punctuation, spaces, accents and cases are ignored.
    """
    s_copy = s.lower()
    s_copy = remove_non_word(s_copy)
    s_copy = remove_accent(s_copy)
    for i in range(len(s_copy)//2):
        if s_copy[i] != s_copy[len(s_copy)-1-i]:
            return False
    return True

def check_antipalindrom(s: str) -> bool:
    """
    Return True if given text is a anti-palindrom, False otherwise.
    In a anti-palindrom of size N, the i-th and (N-i)-th letters
    are always different.

    Punctuation, spaces, accents and cases are ignored.
    """
    s_copy = s.lower()
    s_copy = remove_non_word(s_copy)
    s_copy = remove_accent(s_copy)
    for i in range(len(s_copy)//2):
        if s_copy[i] == s_copy[len(s_copy)-1-i]:
            return False
    return True

def check_lipogram(s: str, forbidden: str) -> bool:
    """
    Return True if given text ('s') does not contain
    any character in 'forbidden' string, False otherwise.

    For example, a lipogram in 'E' must not use the letter
    E (with or without accent, with or without uppercase).
    """
    s_copy = s.lower()
    s_copy = remove_accent(s_copy)
    for c in s_copy:
        if c in forbidden:
            return False
    return True

def check_monovocalism(s: str, voyel: str = None) -> bool:
    """
    Return True if the text use only one voyel (monovocalism),
    False otherwise.
    """
    if voyel is None:
        # Find first voyel of the text
        s_copy = remove_accent(s.lower())
        for c in s_copy:
            if c in 'aeiouy':
                voyel = c
                break
        if voyel is None:
            # No voyel found
            return True
    elif voyel not in 'aeiouy':
        raise ValueError("Please chose target voyel in 'aeiuoy'.")
    forbidden_voyels = ['a', 'e', 'i', 'o', 'u', 'y']
    forbidden_voyels.remove(voyel)
    return check_lipogram(s, ''.join(forbidden_voyels))

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
    return check_lipogram(s, forbidden="bfmpv")

def check_prisoner(s: str, allow_accent=True) -> bool:
    """
    Return True if given text follow the 'prisoner's constraint',
    False otherwise.

    https://fr.wikipedia.org/wiki/Contrainte_du_prisonnier
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

def check_monovocalism(s: str, target=None) -> bool:
    """
    Return True if there is only one vowel used in the text,
    False otherwise.

    Parameters
    ----------
    s : str
        Text to check.
    target : str, optional
        Single character imposed at the beginning of each word.
        Defaults to None.
    """
    s_vowels = set(to_vowels(s))
    n_vowels = len(s_vowels)
    if n_vowels > 1:
        return False
    if target:
        if target not in s_vowels:
            return False
    return True

def check_heteroconsonantism(s: str) -> bool:
    """
    Return True if each consonant appears only once in
    the source text, False otherwise.
    """
    s_consonants = set(to_consonants(s))
    n_consonants = len(s_consonants)
    if n_consonants != len(consonants_char):
        # Missing or doubled consonants
        return False
    for c in consonants_char:
        if c not in s_consonants:
            return False
    return True

def check_okapi(s: str) -> bool:
    """
    Return True if source has is an alternation
    of vowels and consonants, False otherwise.
    """
    if not s:
        return True
    # Extract letters only
    s_copy = s.lower()
    s_copy = remove_non_word(s_copy)
    s_copy = remove_accent(s_copy)
    # Check alternation
    previous_is_vowel = s[0] in vowels_char
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
    """
    # Remove accent, uppercase, and get words only
    words = to_words(remove_accent(s.lower()))
    if start_with is None:
        if not s:
            return True
        start_with = words[0][0]
    elif len(start_with) != 1:
        raise ValueError("'start_with' must be only one character.")
    for w in words:
        if w[0] != start_with:
            return False
    return True

def check_acrostic(s: str, ref: str, by_words=False) -> bool:
    """
    Parameters
    ----------
    s : str
        Text to check.
    ref : str
        Characters to be found at the beginning of each line or words.
    by_words : bool, optional
        If False, check the beginning of each line. If True,
        check the beginning of each word. Defaults to False.
    """
    # Remove accent, uppercase, and get words only
    if by_words:
        units = to_words(s.lower(), letters_only=True)
    else:
        units = to_lines(s.lower(), letters_only=True)
    if len(units) != len(ref):
        return False
    for u, c in zip(units, ref):
        if u[0] != c:
            return False
    return True

def check_universal_acrostic(s: str) -> bool:
    """
    Return True if all 26 lines in given text
    begin with the successive letters in latin
    alphabet, False otherwise.
    """
    return check_acrostic(
        s,
        ref=string.ascii_lowercase,
        by_words=False
    )

def check_abecedaire(s: str) -> bool:
    """
    Return True if all 26 words in given text
    begin with the successive letters in latin
    alphabet (an 'abécédaire'), False otherwise. 
    """
    return check_acrostic(
        s,
        ref=string.ascii_lowercase,
        by_words=True
    )

def check_kyrielle(s: str) -> bool:
    """
    Return True if the last letter of each word
    is the same letter as the first letter of the
    following word ('kyrielle').
    """
    words = to_words(remove_accent(s.lower()))
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
    """
    words = to_words(s)
    for i in range(len(words)-1):
        if count_common(words[i], words[i+1]) < min:
            return False
    return True

def check_snob(s: str) -> bool:
    """
    Return True if all successive words in given text
    share no common letter, False otherwise.
    """
    words = to_words(s)
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
    """
    # Extract words length
    words_lengths = [len(word) for word in to_words(s)]
    if not words_lengths:
        return True
    words_lengths.sort()

    # Compare to smallest value
    return words_lengths[0] >= m

def check_anagram(s1: str, s2: str) -> bool:
    """
    Return True if s1 and s2 use exactly the same
    letters, the same amount of time; False otherwise.
    """
    return letter_counter(s1) == letter_counter(s2)

def check_subanagram(s_sub: str, s_ref: str) -> bool:
    """
    Return True if all the letter in s_sub are contained
    in s_ref.
    """
    return letter_counter(s_sub) <= letter_counter(s_ref)

def check_pangram(s: str, alphabet=None) -> bool:
    """
    Return True if the text contains all letters of the
    alphabet, at least once. False otherwise.

    By default, it checks the 26 letters of latin alphabet.

    Parameters
    ----------
    alphabet : str, optional
        Check a given alphabet. Defaults to None.
    """
    if alphabet is None:
        # By default, latin alphabet
        alphabet = string.ascii_lowercase

    return check_subanagram(alphabet, s)

def check_panscrabblogram(s: str, lang='fr') -> bool:
    """
    Return True if the text is made of (and only of)
    all the letters in a box of Scrabble.

    Parameters
    ----------
    lang: str in {'fr', 'en'}
        Language of reference. Available languages
        are French ('fr') and English ('en').
        Defaults to French.
    """
    available_lang = {
        # French
        'fr': "aaaaaaaaabbccdddeeeeeeeeeeeeeeeffgghhiiiiiiiijklllllmmmnnnnnnooooooppqrrrrrrssssssttttttuuuuuuvvwxyz",
        # English
        'en': "aaaaaaaaabbccddddeeeeeeeeeeeeffggghhiiiiiiiiijkllllmmnnnnnnooooooooppqrrrrrrssssttttttuuuuvvwwxyyz"
    }
    if lang not in available_lang:
        raise ValueError(f"'lang' argument must be in {set(available_lang.keys())}")

    return check_anagram(available_lang[lang], s)
