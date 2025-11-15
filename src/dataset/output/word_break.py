# necessary imports (use only the python standard libraries)
# No specific imports are needed for this problem as it uses built-in types.

# you can define other auxiliary functions

def word_break(s: str, word_dict: list[str]) -> bool:
    """
    Checks if 's' can be segmented into a space-separated sequence of words from 'word_dict'.
    This function uses dynamic programming (DP) to solve the Word Break problem.

    Args:
        s: The input string to be segmented.
        word_dict: A list of words that can be used for segmentation.

    Returns:
        True if 's' can be segmented, False otherwise.
    """
    
    # Convert the word_dict to a set for O(1) average time complexity lookups.
    # This significantly improves performance, especially with large dictionaries.
    word_set = set(word_dict)

    n = len(s)
    
    # dp[i] will be True if the substring s[0...i-1] (of length i) can be segmented
    # using words from word_set.
    # The array size is n + 1 because dp[n] will represent the entire string s.
    dp = [False] * (n + 1)

    # Base case: An empty string (s[0...0-1]) can always be segmented.
    # This allows us to build up solutions from the beginning of the string.
    dp[0] = True

    # Iterate through each possible end position `i` for a substring s[0...i-1].
    # `i` goes from 1 to n (inclusive).
    for i in range(1, n + 1):
        # Iterate through each possible start position `j` for the last word
        # in the segmentation of s[0...i-1].
        # The substring s[j...i-1] (i.e., s[j:i]) is the potential last word.
        # `j` goes from 0 to i-1 (inclusive).
        for j in range(i):
            # If s[0...j-1] can be segmented (dp[j] is True)
            # AND the current substring s[j:i] is a valid word in our dictionary,
            # then s[0...i-1] can also be segmented.
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                # Once we find a valid segmentation for s[0...i-1],
                # we don't need to check other `j` values for this `i`.
                break
    
    # The final result is whether the entire string s (s[0...n-1]) can be segmented.
    return dp[n]

# add this ad the end of the file
EXPORT_FUNCTION = word_break