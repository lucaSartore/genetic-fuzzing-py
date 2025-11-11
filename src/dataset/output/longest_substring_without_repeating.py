# necessary inputs (use only the python standard libraries)

# you can define other auxiliary functions

def longest_substring_without_repeating(s: str) -> int:
    """
    Finds the length of the longest substring without repeating characters using the sliding window technique.

    Args:
        s: The input string.

    Returns:
        The length of the longest substring without repeating characters.
    """
    if not s:
        return 0

    char_set = set()
    max_length = 0
    left = 0

    for right in range(len(s)):
        # While the character at the right pointer is already in our set,
        # it means we have a repeating character.
        # We need to shrink the window from the left.
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add the current character at the right pointer to our set.
        char_set.add(s[right])
        
        # Update the maximum length found so far.
        # The current window length is right - left + 1.
        max_length = max(max_length, right - left + 1)
        
    return max_length

# add this ad the end of the file
EXPORT_FUNCTION = longest_substring_without_repeating