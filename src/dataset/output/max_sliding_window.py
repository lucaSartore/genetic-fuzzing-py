# necessary imports (use only the python standard libraries)
import collections
from typing import List

# you can define other auxiliary functions

def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """
    Finds the maximum of each sliding window of size 'k' in a list of numbers.

    This function uses a double-ended queue (deque) to store indices of elements
    in the current window in decreasing order of their values. The front of
    the deque always holds the index of the maximum element in the current window.

    Args:
        nums: A list of integers.
        k: The size of the sliding window.

    Returns:
        A list of integers, where each element is the maximum of the
        corresponding sliding window.

    Examples:
        >>> max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3)
        [3, 3, 5, 5, 6, 7]
        >>> max_sliding_window([1], 1)
        [1]
        >>> max_sliding_window([1, -1], 1)
        [1, -1]
        >>> max_sliding_window([9, 11], 2)
        [11]
    """
    if not nums:
        return []
    if k <= 0:
        raise ValueError("Window size 'k' must be a positive integer.")
    if k > len(nums):
        # If k is larger than the list, there's only one window, which is the entire list
        return [max(nums)]

    result = []
    # dq stores indices of elements, maintaining them in decreasing order of their values
    # The front of the deque always holds the index of the maximum element in the current window
    dq = collections.deque() 

    for i in range(len(nums)):
        # 1. Remove elements from the front of the deque that are out of the current window
        # The window starts at i - k + 1 and ends at i.
        # If the index at the front of dq is less than or equal to i - k, it's out of bounds.
        if dq and dq[0] <= i - k:
            dq.popleft()

        # 2. Remove elements from the back of the deque that are smaller than the current element
        # This ensures that elements in dq are in decreasing order of their values.
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()

        # 3. Add the current element's index to the back of the deque
        dq.append(i)

        # 4. If the window is fully formed (i.e., we have processed at least k elements),
        #    the maximum element for the current window is at the front of the deque.
        if i >= k - 1:
            result.append(nums[dq[0]])
            
    return result

# add this ad the end of the file
EXPORT_FUNCTION = max_sliding_window