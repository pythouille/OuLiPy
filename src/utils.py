"""
This module contains functions to check properties in strings.
"""
import string
from typing import List



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
authorized_characters = ''.join(['æ', 'œ', 'Æ', 'Œ'])

def remove_punctuation(s: str) -> str:
    """
    Return a copy of given string without
    its punctuation.
    """
    s_copy = s
    for c in string.punctuation:
        if c in s_copy:
            s_copy = s_copy.replace(c, '')
    return s_copy

def remove_non_word(s: str) -> str:
    """
    Return a copy of given string without
    its punctuation and white space (which
    are non-word character).
    """
    s_copy = s
    for c in (string.punctuation + string.whitespace):
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
        if c in accent_to_letter:
            s_copy = s_copy.replace(c, accent_to_letter[c])
        elif c not in (
                string.ascii_letters
                + string.punctuation
                + string.whitespace
                + authorized_characters
                ):
            print(f"WARNING: unknown character: {c}")
    return s_copy

def is_palindrom(s: str) -> bool:
    """
    Return True if given text is a palindrom, False otherwise.
    """
    s_copy = s.lower()
    s_copy = remove_non_word(s_copy)
    s_copy = remove_accent(s_copy)
    for i in range(len(s_copy)//2):
        if s_copy[i] != s_copy[len(s_copy)-1-i]:
            return False
    return True

def is_lipogram(s: str, forbidden: str) -> bool:
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

low_ascender_char = ''.join([ # Accent outside the mean line
    'â', 'ä', 'á', 'à', 'ã',
    'ê', 'ë', 'é', 'è',
    'î', 'ï', 'í', 'ì',
    'ô', 'ö', 'ó', 'ò', 'õ',
    'û', 'ü', 'ú', 'ù', 
    'ç', 'ñ',
])
low_descender_char = ",;"
ascender_char = (
    "bdfklt"
    + "'!\"&\'()*/?[\\]^`{|}'" # Punctuation
    + string.ascii_uppercase # Uppercase
    + low_ascender_char.upper() # Uppercase with accent
)
descender_char = "gjpqy"

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

def split_words(s: str) -> list[str]:
    """
    Return a list of the words in given text.

    White space and punctuation are discarded.
    """
    # Remove punctuation and standardize white space
    s_copy = remove_punctuation(s)
    for w in string.whitespace:
        if w in s_copy:
            s_copy = s_copy.replace(w, ' ')
    return [w for w in s_copy.split(' ') if w]

def check_abecedaire(s: str) -> bool:
    """
    Return True if all 26 words in given text
    begin with the successive letters in latin
    alphabet (an 'abécédaire'), False otherwise. 
    """
    # Remove accent, uppercase, and get words only
    words = split_words(remove_accent(s.lower()))
    if len(words) != 26:
        return False
    for c, w in zip(string.ascii_lowercase, words):
        if c != w[0]:
            return False
    return True

def check_kyrielle(s: str) -> bool:
    """
    Return True if the last letter of each word
    is the same letter as the first letter of the
    following word ('kyrielle').
    """
    words = split_words(remove_accent(s.lower()))
    for i in range(len(words)-1):
        if words[i][-1] != words[i+1][0]:
            return False
    return True
