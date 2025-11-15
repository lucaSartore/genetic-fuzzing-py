# necessary imports (use only the python standard libraries)

def longest_common_subsequence(str1: str, str2: str) -> int:
    """
    Finds the length of the longest common subsequence (LCS) between two strings
    using dynamic programming.

    A subsequence is a sequence that can be derived from another sequence by
    deleting some or no elements without changing the order of the remaining
    elements. A common subsequence is a subsequence common to two sequences.
    The longest common subsequence is the longest such subsequence.

    Args:
        str1: The first input string.
        str2: The second input string.

    Returns:
        The length of the longest common subsequence.
    """
    m = len(str1)
    n = len(str2)

    # Create a 2D DP table to store lengths of LCS of prefixes.
    # dp[i][j] will store the length of LCS of str1[0...i-1] and str2[0...j-1].
    # The table size will be (m+1) x (n+1) to handle empty string prefixes.
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill the dp table using the recurrence relation
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                # If current characters match, they contribute to the LCS.
                # The length is 1 plus the LCS of the strings excluding these characters.
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                # If current characters don't match, we take the maximum of:
                # 1. LCS of str1[0...i-2] and str2[0...j-1] (excluding str1[i-1])
                # 2. LCS of str1[0...i-1] and str2[0...j-2] (excluding str2[j-1])
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # The bottom-right cell of the DP table contains the length of the LCS
    # of the entire str1 and str2.
    return dp[m][n]

# add this ad the end of the file
EXPORT_FUNCTION = longest_common_subsequence