from typing import List

def spiral_matrix(matrix: List[List[int]]) -> List[int]:
    """
    Returns all elements of a matrix in spiral order.
    """
    if not matrix or not matrix[0]:
        return []

    rows = len(matrix)
    cols = len(matrix[0])
    result = []

    # Initialize the pointers for the boundaries of the matrix
    top = 0
    bottom = rows - 1
    left = 0
    right = cols - 1

    # Continue the spiral traversal as long as the boundaries don't cross
    while top <= bottom and left <= right:
        # Traverse right along the current top row
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1  # Move the top boundary down

        # Traverse down along the current rightmost column
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1  # Move the right boundary left

        # Traverse left along the current bottom row
        # This step is only performed if 'top' has not crossed 'bottom'
        # (e.g., for a single row matrix, this step would be skipped after 'top' increments)
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1  # Move the bottom boundary up

        # Traverse up along the current leftmost column
        # This step is only performed if 'left' has not crossed 'right'
        # (e.g., for a single column matrix, this step would be skipped after 'right' decrements)
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1  # Move the left boundary right

    return result

# add this ad the end of the file
EXPORT_FUNCTION = spiral_matrix