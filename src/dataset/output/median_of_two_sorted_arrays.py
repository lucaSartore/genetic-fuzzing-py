# necessary imports (use only the python standard libraries)
# No specific imports are needed for this solution,
# as float('inf') and float('-inf') are built-in.

# you can define other auxiliary functions

def median_of_two_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    """
    Finds the median of two sorted arrays.

    This function implements a binary search approach to find the median
    of two sorted arrays, achieving an optimal O(log(min(m, n))) time complexity,
    where m and n are the lengths of nums1 and nums2 respectively.

    The core idea is to find a "partition" in both arrays such that:
    1. The total number of elements in the left halves of both arrays
       combined is equal to (or one more than, for odd total length)
       the total number of elements in the right halves.
    2. All elements in the combined left half are less than or equal to
       all elements in the combined right half.

    Args:
        nums1: The first sorted list of integers.
        nums2: The second sorted list of integers.

    Returns:
        The median of the two sorted arrays as a float.
    """
    # Ensure nums1 is the shorter array. This optimization reduces the search space
    # for the binary search to the length of the shorter array, ensuring O(log(min(m, n)))
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    
    # 'low' and 'high' define the search space for 'partitionX'
    # 'partitionX' is the number of elements taken from nums1's left part.
    # It can range from 0 (no elements from nums1) to m (all elements from nums1).
    low, high = 0, m

    # 'total_left_elements' is the required count of elements in the combined
    # left partition. For an odd total length, it makes the left partition
    # one element larger, simplifying median calculation.
    total_left_elements = (m + n + 1) // 2

    while low <= high:
        # 'partitionX' is the cut point for nums1.
        # It represents that `partitionX` elements are on the left of the cut
        # and `m - partitionX` elements are on the right.
        partitionX = (low + high) // 2
        
        # 'partitionY' is the corresponding cut point for nums2.
        # It's calculated to ensure 'total_left_elements' elements are in the combined left partition.
        partitionY = total_left_elements - partitionX

        # Determine the elements around the partitions.
        # For edge cases where a partition is at the beginning (0) or end (length),
        # use negative/positive infinity to ensure comparison logic holds.
        max_left_x = float('-inf') if partitionX == 0 else nums1[partitionX - 1]
        min_right_x = float('inf') if partitionX == m else nums1[partitionX]

        max_left_y = float('-inf') if partitionY == 0 else nums2[partitionY - 1]
        min_right_y = float('inf') if partitionY == n else nums2[partitionY]

        # Check if the partitions are valid.
        # A valid partition satisfies two conditions:
        # 1. The largest element on the left side of nums1's partition
        #    must be less than or equal to the smallest element on the
        #    right side of nums2's partition.
        # 2. The largest element on the left side of nums2's partition
        #    must be less than or equal to the smallest element on the
        #    right side of nums1's partition.
        if max_left_x <= min_right_y and max_left_y <= min_right_x:
            # We found the correct partitions!
            # Now, calculate the median based on the total length.

            if (m + n) % 2 == 1:  # Total length is odd
                # The median is simply the largest element in the combined left half.
                return float(max(max_left_x, max_left_y))
            else:  # Total length is even
                # The median is the average of the largest element in the combined left half
                # and the smallest element in the combined right half.
                return (float(max(max_left_x, max_left_y)) + float(min(min_right_x, min_right_y))) / 2.0
        elif max_left_x > min_right_y:
            # 'partitionX' is too far to the right, meaning 'max_left_x' is too large.
            # We need to shift 'partitionX' to the left to find a smaller 'max_left_x'.
            high = partitionX - 1
        else:  # max_left_y > min_right_x
            # 'partitionX' is too far to the left, meaning 'max_left_y' is too large.
            # (Because 'partitionY' is derived from 'partitionX', if 'max_left_y' is too large,
            # it implies 'partitionY' is too large, which means 'partitionX' is too small).
            # We need to shift 'partitionX' to the right to find a larger 'min_right_x'.
            low = partitionX + 1

    # This line should theoretically not be reached as the binary search
    # guarantees a solution will be found within the loop for valid inputs.
    # It's included for static analysis tools.
    return 0.0

# add this ad the end of the file
EXPORT_FUNCTION = median_of_two_sorted_arrays