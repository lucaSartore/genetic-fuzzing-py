from typing import List

def next_permutation(nums: List[int]) -> List[int]:
    """
    Finds the next lexicographically greater permutation of a list of numbers.
    If no greater permutation exists (i.e., the list is in descending order),
    it rearranges the list to the smallest possible order (ascending order).
    The function modifies the input list in-place and returns the modified list.

    Args:
        nums (List[int]): A list of integers.

    Returns:
        List[int]: The list after being rearranged to its next lexicographically
                   greater permutation, or the smallest permutation if it was
                   already the largest.
    """
    n = len(nums)

    # Step 1: Find the largest index `k` such that `nums[k] < nums[k + 1]`.
    # Iterate from right to left (second to last element down to the first).
    k = -1
    for i in range(n - 2, -1, -1):
        if nums[i] < nums[i + 1]:
            k = i
            break

    # Step 2: If no such index `k` exists, the list is already in descending order
    # (i.e., it is the largest permutation). In this case, reverse the entire list
    # to get the smallest permutation.
    if k == -1:
        nums.reverse()
        return nums

    # Step 3: Find the largest index `l` greater than `k` such that `nums[k] < nums[l]`.
    # Iterate from right to left, starting from the last element down to `k + 1`.
    l = -1
    for i in range(n - 1, k, -1):
        if nums[k] < nums[i]:
            l = i
            break

    # Step 4: Swap `nums[k]` and `nums[l]`.
    nums[k], nums[l] = nums[l], nums[k]

    # Step 5: Reverse the sub-list `nums[k + 1:]`.
    # This segment is currently in descending order. Reversing it puts it
    # in ascending order, which is the smallest lexicographical order possible
    # for the suffix, thus ensuring the overall permutation is the *next* one.
    left = k + 1
    right = n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1

    return nums

EXPORT_FUNCTION = next_permutation