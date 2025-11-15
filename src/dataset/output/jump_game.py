# necessary imports (use only the python standard libraries)
from typing import List

# you can define other auxiliary functions

def jump_game(nums: List[int]) -> bool:
    """
    Determines if you can reach the last index of an array given jump lengths.
    This function employs a greedy approach to solve the "Jump Game" problem.
    Each element in the array represents your maximum jump length from that position.

    The algorithm works by keeping track of the farthest index `farthest_reach`
    that can be reached from any position visited so far. It iterates through
    the array, updating `farthest_reach`. If at any point the current index `i`
    exceeds `farthest_reach`, it means `i` is unreachable, and thus the last
    index cannot be reached. If `farthest_reach` ever covers or surpasses
    the last index of the array (`n - 1`), then the last index is reachable.

    Args:
        nums: A list of non-negative integers. Each nums[i] represents the maximum
              jump length from index i. It is assumed that the list will contain
              at least one element (i.e., `len(nums) >= 1`).

    Returns:
        True if the last index can be reached from the first index, False otherwise.
    """
    n = len(nums)
    
    # farthest_reach tracks the maximum index that can be reached from the start.
    # Initially, we are at index 0, so the farthest we can reach is also 0.
    farthest_reach = 0

    # Iterate through the array. We only need to iterate up to the point
    # where the last index is potentially reachable.
    # The loop condition `i < n` ensures we consider all possible jump points.
    for i in range(n):
        # If the current index `i` is beyond what we can currently reach (`farthest_reach`),
        # it means we are stuck and cannot proceed further.
        # Therefore, the last index is unreachable.
        if i > farthest_reach:
            return False

        # Update `farthest_reach`. It's the maximum of the current `farthest_reach`
        # and the maximum index we can reach by jumping from the current position `i`.
        farthest_reach = max(farthest_reach, i + nums[i])

        # If `farthest_reach` has reached or surpassed the last index of the array,
        # it means we can successfully reach the end.
        if farthest_reach >= n - 1:
            return True
            
    # This line should theoretically not be reached because the two `return` statements
    # inside the loop cover all possible scenarios. If the loop completes, it means
    # either `True` was returned (we reached the end) or `False` was returned (we got stuck).
    # For robustness and clarity (though logically redundant here), one might add a final
    # `return False` if the loop ends and no `True` was returned, but it implies a flaw
    # in the condition `if i > farthest_reach`. The current logic is complete.
    # The `if farthest_reach >= n - 1` condition ensures an early exit with True.
    # If it's not reached, and the loop finishes, then it implies `farthest_reach < n - 1`.
    # This means the last index was never reached. Thus, the implicit return is False.
    return False # Explicitly returning False if loop completes without success
                 # (which should not happen with the current robust logic).


# add this ad the end of the file
EXPORT_FUNCTION = jump_game