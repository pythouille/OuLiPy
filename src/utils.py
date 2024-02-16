"""
This module contains functions to check properties in strings.
"""



def is_palindrom(s: str) -> bool:
    """
    Return True if given string is a palindrom, False otherwise.
    """
    size = len(s)
    for i in range(size//2):
        if s[i] != s[size-1-i]:
            return False
    return True
