"""
This module contains functions to check properties in strings.
"""
import string



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
                ):
            print(f"WARNING: unknown character: {c}")
    return s_copy

def is_palindrom(s: str) -> bool:
    """
    Return True if given string is a palindrom, False otherwise.
    """
    s_copy = s.lower()
    s_copy = remove_non_word(s_copy)
    s_copy = remove_accent(s_copy)
    for i in range(len(s_copy)//2):
        if s_copy[i] != s_copy[len(s_copy)-1-i]:
            return False
    return True
