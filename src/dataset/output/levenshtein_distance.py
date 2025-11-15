# necessary imports (use only the python standard libraries)

def levenshtein_distance(word1: str, word2: str) -> int:
    """
    Calculates the Levenshtein edit distance between two strings using dynamic programming.

    The Levenshtein distance is the minimum number of single-character edits (insertions,
    deletions, or substitutions) required to change one word into the other.

    Args:
        word1: The first string.
        word2: The second string.

    Returns:
        The Levenshtein edit distance as an integer.
    """
    len1 = len(word1)
    len2 = len(word2)

    # Create a DP table to store results of subproblems
    # dp[i][j] will be the Levenshtein distance between word1[:i] and word2[:j]
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    # Initialize the first row and column of the DP table
    # If word1 is empty, the distance to word2[:j] is j (insertions)
    for j in range(len2 + 1):
        dp[0][j] = j
    # If word2 is empty, the distance to word1[:i] is i (deletions)
    for i in range(len1 + 1):
        dp[i][0] = i

    # Fill the DP table
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            # Cost of substitution: 0 if characters match, 1 otherwise
            cost = 0 if word1[i - 1] == word2[j - 1] else 1

            # dp[i][j] is the minimum of three possibilities:
            # 1. Deletion: dp[i-1][j] + 1 (delete character from word1)
            # 2. Insertion: dp[i][j-1] + 1 (insert character into word1 to match word2)
            # 3. Substitution: dp[i-1][j-1] + cost (substitute character)
            dp[i][j] = min(dp[i - 1][j] + 1,        # Deletion
                           dp[i][j - 1] + 1,        # Insertion
                           dp[i - 1][j - 1] + cost) # Substitution/Match

    # The bottom-right cell contains the Levenshtein distance for the full strings
    return dp[len1][len2]

# add this ad the end of the file
EXPORT_FUNCTION = levenshtein_distance