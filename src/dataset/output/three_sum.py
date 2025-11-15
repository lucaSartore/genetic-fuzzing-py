from typing import List

def three_sum(nums: List[int]) -> List[List[int]]:
    """
    Finds all unique triplets in a list that sum to zero.

    The algorithm first sorts the input list. Then, it iterates through the
    sorted list with a single pointer `i`. For each `nums[i]`, it uses a
    two-pointer approach (`left` and `right`) on the remaining part of the
    list to find pairs `(nums[left], nums[right])` such that
    `nums[i] + nums[left] + nums[right] == 0`.
    Duplicate triplets are avoided by skipping over duplicate elements
    for `i`, `left`, and `right` pointers.

    Args:
        nums: A list of integers.

    Returns:
        A list of unique triplets, where each triplet is a list of three
        integers that sum to zero. The order of triplets in the output and
        the order of elements within each triplet are not guaranteed, but
        each triplet itself is unique.
    """
    
    # Sort the input array. This is crucial for both the two-pointer approach
    # and for efficiently handling duplicates.
    nums.sort()
    
    result: List[List[int]] = []
    
    # If the list has fewer than 3 elements, no triplets can be formed.
    if len(nums) < 3:
        return result
        
    # Iterate through the array with pointer 'i'.
    # 'i' will represent the first element of our potential triplet.
    # We iterate up to len(nums) - 2 because we need at least two more elements
    # (at 'left' and 'right' pointers) to form a triplet.
    for i in range(len(nums) - 2):
        # Skip duplicate values for 'nums[i]'.
        # This optimization ensures that we don't process the same 'first' number
        # multiple times, which would lead to duplicate triplets.
        # This condition is checked only if 'i' is not the first element (i > 0)
        # to avoid an out-of-bounds error and correctly handle the first element.
        if i > 0 and nums[i] == nums[i-1]:
            continue
            
        # Initialize two pointers: 'left' and 'right'.
        # 'left' starts just after 'i'.
        # 'right' starts at the end of the array.
        left = i + 1
        right = len(nums) - 1
        
        # Use the two-pointer approach to find pairs (nums[left], nums[right])
        # that, along with nums[i], sum to zero.
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                # Found a triplet that sums to zero.
                # Add it to our results list.
                result.append([nums[i], nums[left], nums[right]])
                
                # Move both pointers inward to search for other potential triplets.
                left += 1
                right -= 1
                
                # Skip duplicate values for 'nums[left]'.
                # This ensures that we don't include triplets that only differ
                # in their second element if that element is a duplicate.
                while left < right and nums[left] == nums[left-1]:
                    left += 1
                
                # Skip duplicate values for 'nums[right]'.
                # Similar to 'left', this avoids triplets that only differ
                # in their third element due to duplicates.
                while left < right and nums[right] == nums[right+1]:
                    right -= 1
                    
            elif current_sum < 0:
                # The current sum is too small.
                # To increase the sum, move the 'left' pointer to the right
                # to consider a larger number.
                left += 1
            else: # current_sum > 0
                # The current sum is too large.
                # To decrease the sum, move the 'right' pointer to the left
                # to consider a smaller number.
                right -= 1
                
    return result

# add this ad the end of the file
EXPORT_FUNCTION = three_sum