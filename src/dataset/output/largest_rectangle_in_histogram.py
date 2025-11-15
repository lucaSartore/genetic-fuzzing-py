# necessary imports (use only the python standard libraries)
from typing import List

# you can define other auxiliary functions

def largest_rectangle_in_histogram(heights: List[int]) -> int:
    """
    Finds the largest rectangle area in a histogram.

    This function calculates the maximum area of a rectangle that can be
    formed within a histogram where each bar has a width of 1.
    It uses a monotonic stack approach to achieve O(n) time complexity.

    Args:
        heights: A list of integers representing the heights of the histogram bars.
                 Each bar has a width of 1.

    Returns:
        An integer representing the maximum possible area of a rectangle
        in the histogram.

    Examples:
        >>> largest_rectangle_in_histogram([2, 1, 5, 6, 2, 3])
        10
        >>> largest_rectangle_in_histogram([2, 4])
        4
        >>> largest_rectangle_in_histogram([1])
        1
        >>> largest_rectangle_in_histogram([])
        0
        >>> largest_rectangle_in_histogram([0])
        0
        >>> largest_rectangle_in_histogram([0, 0, 0])
        0
        >>> largest_rectangle_in_histogram([6, 2, 5, 4, 5, 1, 6])
        12
    """
    if not heights:
        return 0

    max_area = 0
    # The stack will store indices of bars.
    # The invariant is that heights[stack[-1]] < heights[i] for all i on stack.
    # In other words, the stack stores indices of bars in increasing order of their heights.
    stack: List[int] = []

    # Iterate through all bars. We append an implicit bar of height 0 at the end
    # (by iterating up to len(heights) + 1) to ensure all bars in the stack are processed.
    for i in range(len(heights) + 1):
        # Determine the current height for comparison. If 'i' is beyond the last actual bar,
        # use 0 to force all remaining bars in the stack to be popped and their areas calculated.
        current_h = heights[i] if i < len(heights) else 0

        # While the stack is not empty AND the height of the bar at the top of the stack
        # is greater than or equal to the current height, we pop and calculate areas.
        # This means `current_h` is the first bar to the right (at index `i`)
        # that is smaller than `heights[stack[-1]]`.
        while stack and heights[stack[-1]] >= current_h:
            # Pop the index of the bar that defines the height of a potential rectangle.
            h_idx = stack.pop()
            h = heights[h_idx]

            # Calculate the width of the rectangle with height 'h'.
            # The right boundary (exclusive) is the current index 'i'.
            # The left boundary (exclusive) is the index of the element
            # below the popped element in the stack.
            # If the stack becomes empty after popping `h_idx`, it means `h`
            # is the smallest bar from index 0 up to `i-1`. In this case,
            # the left boundary is effectively -1.
            # So, width = i - (left_boundary_exclusive) - 1
            # If stack is empty, left_boundary_exclusive is -1, so width = i - (-1) - 1 = i.
            # If stack is not empty, left_boundary_exclusive is stack[-1], so width = i - stack[-1] - 1.
            width = i if not stack else i - stack[-1] - 1
            
            max_area = max(max_area, h * width)
        
        # Push the current bar's index onto the stack.
        # This maintains the monotonic increasing height property of the stack.
        stack.append(i)
    
    return max_area

# add this ad the end of the file
EXPORT_FUNCTION = largest_rectangle_in_histogram