# necessary imports (use only the python standard libraries)
from typing import List

# you can define other auxiliary functions

def longest_increasing_subsequence(nums: List[int]) -> int:
    """
    Finds the length of the Longest Increasing Subsequence (LIS) in a given list of numbers
    using dynamic programming.

    The LIS is a subsequence where all elements are in increasing order,
    and its length is as long as possible.

    This implementation has a time complexity of O(n^2) and a space complexity of O(n),
    where n is the number of elements in the input list.

    Args:
        nums: A list of integers.

    Returns:
        The length of the Longest Increasing Subsequence.

    Examples:
        >>> longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])
        4
        >>> longest_increasing_subsequence([0, 1, 0, 3, 2, 3])
        4
        >>> longest_increasing_subsequence([7, 7, 7, 7, 7, 7, 7])
        1
        >>> longest_increasing_subsequence([])
        0
        >>> longest_increasing_subsequence([1])
        1
        >>> longest_increasing_subsequence([3, 2, 1])
        1
        >>> longest_increasing_subsequence([1, 2, 3, 4, 5])
        5
    """
    n = len(nums)

    # Base case: if the list is empty, the LIS length is 0
    if n == 0:
        return 0

    # dp[i] will store the length of the LIS ending at index i
    # Initialize all dp values to 1, as each element itself forms an LIS of length 1
    dp = [1] * n

    # Fill the dp array
    for i in range(n):
        # For each element nums[i], iterate through previous elements nums[j]
        for j in range(i):
            # If nums[i] is greater than nums[j], it means nums[i] can extend
            # the LIS ending at nums[j].
            # We take the maximum of the current dp[i] and (dp[j] + 1).
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    # The length of the overall LIS is the maximum value in the dp array
    return max(dp)

# add this ad the end of the file
EXPORT_FUNCTION = longest_increasing_subsequence