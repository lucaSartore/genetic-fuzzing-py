# necessary imports (use only the python standard libraries)
from typing import List

# you can define other auxiliary functions

def find_missing_positive(nums: List[int]) -> int:
    """
    Finds the smallest missing positive integer in an unsorted array.

    This function uses an in-place modification approach (similar to cyclic sort)
    to rearrange the numbers. It attempts to place each number `k` at index `k-1`
    if `k` is within the range [1, len(nums)]. After this rearrangement,
    it iterates through the array to find the first index `i` where `nums[i]`
    is not equal to `i + 1`. This `i + 1` is the smallest missing positive integer.

    Args:
        nums: A list of integers (can contain negatives, zeros, duplicates,
              and positives).

    Returns:
        The smallest missing positive integer.

    Examples:
        >>> find_missing_positive([1, 2, 0])
        3
        >>> find_missing_positive([3, 4, -1, 1])
        2
        >>> find_missing_positive([7, 8, 9, 11, 12])
        1
        >>> find_missing_positive([1])
        2
        >>> find_missing_positive([])
        1
        >>> find_missing_positive([-1, -5, 0, 10])
        1
    """
    n = len(nums)
    
    # Phase 1: Place positive numbers in their "correct" positions
    # A number `val` should ideally be at index `val - 1`.
    i = 0
    while i < n:
        val = nums[i]
        
        # Check if the current value `val` is:
        # 1. A positive integer.
        # 2. Within the valid range [1, n] (where n is the length of the array).
        # 3. Not already in its correct position (i.e., nums[val - 1] should not be val).
        #    This check prevents infinite loops for duplicates or numbers already in place.
        if 1 <= val <= n and nums[val - 1] != val:
            # If conditions are met, swap nums[i] with the element at its target index (val - 1).
            # This moves `val` towards its correct position.
            nums[val - 1], nums[i] = nums[i], nums[val - 1]
            
            # After the swap, the element at nums[i] is new (it was the element from val-1),
            # so we re-evaluate nums[i] without incrementing i.
        else:
            # If the current element is not a positive integer within range [1, n],
            # or if it's already in its correct place, move to the next element.
            i += 1
            
    # Phase 2: Find the first missing positive integer
    # After the rearrangement, iterate through the array.
    # The first index `i` where `nums[i]` is not equal to `i + 1`
    # indicates that `i + 1` is the smallest missing positive integer.
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
            
    # If the loop completes, it means all numbers from 1 to n are present
    # in their correct positions (e.g., [1, 2, 3]).
    # In this case, the smallest missing positive integer is n + 1.
    return n + 1

# add this ad the end of the file
EXPORT_FUNCTION = find_missing_positive