"""
This module contains functions to check properties in strings.
"""
import string



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

def is_palindrom(s: str) -> bool:
    """
    Return True if given string is a palindrom, False otherwise.
    """
    size = len(s)
    for i in range(size//2):
        if s[i] != s[size-1-i]:
            return False
    return True
