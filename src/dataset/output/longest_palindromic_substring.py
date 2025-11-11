# necessary inputs (use only the python standard libraries)

# you can define other auxiliary functions

def _expand(s: str, left: int, right: int) -> tuple[int, int]:
    """
    Helper function to expand around a center (or two centers for even length)
    and find the boundaries of the palindrome.

    It expands outwards from the given `left` and `right` indices as long as
    characters match and remain within the string bounds.

    Args:
        s: The input string.
        left: The initial left index for expansion.
        right: The initial right index for expansion.

    Returns:
        A tuple (actual_left, actual_right) representing the inclusive
        start and end indices of the longest palindrome found centered
        around the initial `left` and `right`.
    """
    n = len(s)
    # Expand outwards from the center(s) as long as characters match
    # and stay within string bounds.
    while left >= 0 and right < n and s[left] == s[right]:
        left -= 1
        right += 1
    # The loop exits when s[left] != s[right] or when an index goes out of bounds.
    # At this point, `left` is one position too far left and `right` is one
    # position too far right. So, the actual palindrome boundaries are
    # (left + 1) and (right - 1).
    return left + 1, right - 1


def longest_palindromic_substring(s: str) -> str:
    """
    Finds the longest substring that is a palindrome using the "expand around center" strategy.

    This implementation iterates through each character of the string,
    considering it as a potential center for an odd-length palindrome.
    It also considers each pair of adjacent characters as a potential center
    for an even-length palindrome. For each potential center, it expands
    outwards to find the longest palindrome centered there. The overall
    longest palindrome found throughout this process is then returned.

    Args:
        s: The input string.

    Returns:
        The longest palindromic substring found in 's'. If there are multiple
        substrings of the same maximum length, this implementation returns
        the first one encountered (from left to right in the original string).
    """
    if not s:
        return ""

    n = len(s)
    if n < 2:
        # A string with 0 or 1 character is a palindrome itself.
        return s

    longest_start = 0  # Stores the starting index of the longest palindrome found
    longest_len = 1    # Stores the length of the longest palindrome found (initial: 1 for any single char)

    for i in range(n):
        # Case 1: Odd length palindromes, centered at 'i'
        # e.g., "aba", where 'b' at index 1 is the center.
        start1, end1 = _expand(s, i, i)
        current_len1 = end1 - start1 + 1
        if current_len1 > longest_len:
            longest_len = current_len1
            longest_start = start1

        # Case 2: Even length palindromes, centered between 'i' and 'i+1'
        # e.g., "abba", where the center is between 'b' at index 1 and 'b' at index 2.
        # Only proceed if i+1 is a valid index to form a pair.
        if i + 1 < n:
            start2, end2 = _expand(s, i, i + 1)
            current_len2 = end2 - start2 + 1
            if current_len2 > longest_len:
                longest_len = current_len2
                longest_start = start2

    # Extract and return the longest palindromic substring using its start index and length.
    return s[longest_start : longest_start + longest_len]

# add this ad the end of the file
EXPORT_FUNCTION = longest_palindromic_substring