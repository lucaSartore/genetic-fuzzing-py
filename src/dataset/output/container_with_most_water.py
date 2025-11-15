# necessary imports (use only the python standard libraries)
# No specific imports are needed for this algorithm as it uses basic list operations and arithmetic.

def container_with_most_water(heights: list[int]) -> int:
    """
    Finds the two lines that, with the x-axis, form a container holding the most water.

    Given n non-negative integers a1, a2, ..., an, where each represents a point at
    coordinate (i, ai). n vertical lines are drawn such that the two endpoints
    of line i is at (i, ai) and (i, 0). Find two lines, which, together with the
    x-axis, forms a container, such that the container contains the most water.

    You may not slant the container.

    Args:
        heights: A list of non-negative integers representing the heights of the
                 vertical lines. Each index i corresponds to the x-coordinate.

    Returns:
        The maximum amount of water that can be contained.
    """
    if not heights or len(heights) < 2:
        return 0  # Cannot form a container with less than two lines

    max_area = 0
    left_pointer = 0
    right_pointer = len(heights) - 1

    while left_pointer < right_pointer:
        # Calculate the current height of the container (limited by the shorter line)
        current_height = min(heights[left_pointer], heights[right_pointer])

        # Calculate the current width of the container
        current_width = right_pointer - left_pointer

        # Calculate the area for the current pair of lines
        current_area = current_height * current_width

        # Update the maximum area found so far
        max_area = max(max_area, current_area)

        # Move the pointer of the shorter line inward.
        # The intuition here is that moving the taller line inward will definitely
        # decrease or keep the same min_height (as the new height will be compared
        # to the shorter line), and also decrease the width. So we move the shorter
        # line hoping to find a taller line to increase the min_height.
        if heights[left_pointer] < heights[right_pointer]:
            left_pointer += 1
        else:
            right_pointer -= 1

    return max_area

# add this ad the end of the file
EXPORT_FUNCTION = container_with_most_water