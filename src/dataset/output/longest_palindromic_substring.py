# necessary imports (use only the python standard libraries)
# No specific imports are required from the Python standard library for this solution.

def _expand_around_center(s: str, left: int, right: int) -> tuple[int, int]:
    """
    Helper function to expand around a given center (or pair of centers)
    to find the longest palindrome.

    Args:
        s (str): The input string.
        left (int): The left boundary of the potential center.
        right (int): The right boundary of the potential center.

    Returns:
        tuple[int, int]: A tuple containing the start and end indices
                         (inclusive) of the longest palindrome found
                         centered at `left` and `right`.
    """
    # While the boundaries are valid and characters match, expand outwards
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    # After the loop, `left` and `right` are one step beyond the actual
    # palindrome boundaries. The palindrome is s[left + 1 ... right - 1].
    return left + 1, right - 1

def longest_palindromic_substring(s: str) -> str:
    """
    Finds the longest substring that is a palindrome using the
    expand-around-center approach.

    Args:
        s (str): The input string.

    Returns:
        str: The longest palindromic substring found in s.
             If multiple longest palindromes exist, any one of them is returned.
             Returns an empty string if the input string is empty.
    """
    n = len(s)

    # Base cases:
    # An empty string has an empty string as its longest palindrome.
    if n == 0:
        return ""
    # A single character string is itself a palindrome.
    if n < 2:
        return s

    # Initialize variables to keep track of the longest palindrome found so far.
    # `start` is the starting index (inclusive)
    # `end` is the ending index (inclusive)
    start = 0
    end = 0

    # Iterate through each character to consider it as a potential center
    for i in range(n):
        # Case 1: Palindromes with odd length (e.g., "aba", centered at 'b')
        # Here, the center is a single character at index `i`.
        left1, right1 = _expand_around_center(s, i, i)
        
        # Case 2: Palindromes with even length (e.g., "abba", centered between 'b' and 'b')
        # Here, the center is between characters at index `i` and `i+1`.
        left2, right2 = _expand_around_center(s, i, i + 1)

        # Determine which of the two (odd or even) resulted in a longer palindrome
        # centered at or around `i`.
        len1 = right1 - left1 + 1
        len2 = right2 - left2 + 1

        current_max_len = end - start + 1

        if len1 > current_max_len:
            start = left1
            end = right1
            current_max_len = len1 # Update for the next comparison
        
        if len2 > current_max_len:
            start = left2
            end = right2
            # current_max_len = len2 # Not strictly needed as loop finishes

    # Return the substring from the `start` index to the `end` index (inclusive).
    return s[start : end + 1]

# add this at the end of the file
EXPORT_FUNCTION = longest_palindromic_substring