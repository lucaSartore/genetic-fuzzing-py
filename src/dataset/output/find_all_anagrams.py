# necessary imports (use only the python standard libraries)
from collections import Counter
from typing import List

# you can define other auxiliary functions

def find_all_anagrams(s: str, p: str) -> List[int]:
    """
    Finds all starting indices of 'p's anagrams in 's' using a sliding window
    with character counts.

    Args:
        s: The main string to search within.
        p: The pattern string whose anagrams are to be found.

    Returns:
        A list of integers, where each integer is the starting index in 's'
        of an anagram of 'p'.
    """
    result: List[int] = []
    len_s = len(s)
    len_p = len(p)

    # Edge cases
    # If p is an empty string, it's considered an anagram of itself and can be
    # "found" at every possible position (before any character, between characters,
    # and after all characters).
    if len_p == 0:
        return [i for i in range(len_s + 1)]
    
    # If s is shorter than p, no anagram of p can exist in s.
    if len_s < len_p:
        return []

    # Initialize character counts for p
    p_counts = Counter(p)
    
    # Initialize character counts for the first window of s (of length len_p)
    s_window_counts = Counter(s[:len_p])

    # Check the first window (starting at index 0)
    if s_window_counts == p_counts:
        result.append(0)

    # Slide the window across the rest of the string s
    # The loop variable 'i' represents the rightmost character's index of the
    # current window that is being *added*.
    # The window slides from index 1 up to (len_s - len_p).
    # The window itself covers characters from (i - len_p + 1) to i.
    for i in range(len_p, len_s):
        # Add the new character at the right end of the window
        s_window_counts[s[i]] += 1

        # Remove the character at the left end of the window
        # The character being removed is at index (i - len_p)
        char_to_remove = s[i - len_p]
        s_window_counts[char_to_remove] -= 1

        # If the count of a character becomes 0, remove its entry from the Counter.
        # This is important for correct comparison with p_counts, especially if
        # p_counts doesn't contain that character or has a count of 0 for it.
        # For example, Counter({'a': 1, 'b': 0}) is not equal to Counter({'a': 1}),
        # but for anagram purposes, they should be equivalent if 'b' is not relevant
        # to p_counts or has a 0 count in p_counts.
        if s_window_counts[char_to_remove] == 0:
            del s_window_counts[char_to_remove]

        # Check if the character counts in the current window match p's counts.
        # The current window starts at index (i - len_p + 1).
        if s_window_counts == p_counts:
            result.append(i - len_p + 1)

    return result

# add this ad the end of the file
EXPORT_FUNCTION = find_all_anagrams