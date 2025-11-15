# necessary imports (use only the python standard libraries)
from typing import List

# you can define other auxiliary functions

def search_in_rotated_sorted_array(nums: List[int], target: int) -> int:
    """
    Searches for a target value in a sorted array that has been rotated.
    This function uses a modified binary search algorithm.

    Args:
        nums: A list of integers representing the rotated sorted array.
              The array is sorted but might have been rotated at an unknown pivot.
              Example: [4, 5, 6, 7, 0, 1, 2]
        target: The integer value to search for in the array.

    Returns:
        The index of the target in the array if found, otherwise -1.
    """
    if not nums:
        return -1

    low, high = 0, len(nums) - 1

    while low <= high:
        mid = (low + high) // 2

        if nums[mid] == target:
            return mid

        # Determine which half is sorted
        # Case 1: Left half is sorted (nums[low] <= nums[mid])
        if nums[low] <= nums[mid]:
            # Check if target is within the sorted left half
            if nums[low] <= target < nums[mid]:
                high = mid - 1  # Target is in the left half, so narrow search to left
            else:
                low = mid + 1   # Target is in the right (unsorted or rotated) half, so narrow search to right
        # Case 2: Right half is sorted (nums[mid] < nums[high])
        else:
            # Check if target is within the sorted right half
            if nums[mid] < target <= nums[high]:
                low = mid + 1   # Target is in the right half, so narrow search to right
            else:
                high = mid - 1  # Target is in the left (unsorted or rotated) half, so narrow search to left
    
    # If the loop finishes, the target was not found
    return -1

# add this ad the end of the file
EXPORT_FUNCTION = search_in_rotated_sorted_array