# No specific imports are needed for this function as it primarily uses
# built-in data structures like strings and sets, which are part of 
# the Python standard library by default.

def longest_substring_without_repeating(s: str) -> int:
    """
    Finds the length of the longest substring without repeating characters using a sliding window.

    The function uses a sliding window approach with two pointers, 'left' and 'right',
    and a set to keep track of characters within the current window.
    As the 'right' pointer expands the window, if a character is encountered that
    is already in the set, the 'left' pointer shrinks the window from the left
    until the repeating character is removed from the set.
    The maximum length of the substring without repeating characters is updated
    at each step.

    Args:
        s (str): The input string to find the longest substring in.

    Returns:
        int: The length of the longest substring without repeating characters.

    Examples:
        >>> longest_substring_without_repeating("abcabcbb")
        3
        >>> longest_substring_without_repeating("bbbbb")
        1
        >>> longest_substring_without_repeating("pwwkew")
        3
        >>> longest_substring_without_repeating("")
        0
        >>> longest_substring_without_repeating("a")
        1
    """
    char_set = set()  # Stores characters in the current window
    left = 0          # Left pointer of the sliding window
    max_length = 0    # Stores the maximum length found so far

    # Iterate with the 'right' pointer to expand the window
    for right in range(len(s)):
        # If the current character s[right] is already in the set,
        # it means we have a repeating character.
        # We need to shrink the window from the left until the repeating character
        # is no longer in the set.
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add the current character to the set
        char_set.add(s[right])
        
        # Update the maximum length found so far
        # The current window length is (right - left + 1)
        max_length = max(max_length, right - left + 1)
        
    return max_length

# add this at the end of the file
EXPORT_FUNCTION = longest_substring_without_repeating