from typing import List, Any

def rotate_image(matrix: List[List[Any]]) -> None:
    """
    Rotates an N_N matrix 90 degrees in place.

    This function performs an in-place 90-degree clockwise rotation of a square matrix.
    It iterates through the layers of the matrix, from the outermost to the innermost,
    and for each layer, it performs a 4-way swap of elements along its perimeter.

    Args:
        matrix: A list of lists representing the N_N matrix.
                The matrix must be square (N x N), and its elements can be of any type.
                The rotation is performed in-place, meaning the input matrix is modified directly.
    """
    n = len(matrix)

    # Handle edge cases for non-square matrices or empty matrices.
    # While the problem states "N_N matrix" implying it's always square,
    # this check adds robustness. If N=0 (empty matrix) or rows are not N, do nothing.
    if n == 0 or (n > 0 and len(matrix[0]) != n):
        return

    # Iterate through each layer of the matrix.
    # We only need to process up to n // 2 layers (from the outside in).
    for i in range(n // 2):
        # For each layer 'i', iterate through the elements on the top side of that layer.
        # The 'j' index defines the specific element offset within the current layer's side.
        # The loop range goes from 'i' up to 'n - 1 - i - 1'.
        # This ensures that for each cycle, we pick a unique set of four elements
        # without double-processing or going out of bounds.
        for j in range(i, n - 1 - i):
            # Perform a 4-way swap for the elements involved in the current cycle.
            # The four points (coordinates) for a clockwise rotation are:
            # 1. (i, j)                   - Top-Left element of the current cycle
            # 2. (j, n - 1 - i)           - Top-Right element
            # 3. (n - 1 - i, n - 1 - j)   - Bottom-Right element
            # 4. (n - 1 - j, i)           - Bottom-Left element

            # Store the original value of the Top-Left element.
            temp = matrix[i][j]

            # Move the value from Bottom-Left to Top-Left.
            matrix[i][j] = matrix[n - 1 - j][i]

            # Move the value from Bottom-Right to Bottom-Left.
            matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j]

            # Move the value from Top-Right to Bottom-Right.
            matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i]

            # Move the stored original Top-Left value to Top-Right.
            matrix[j][n - 1 - i] = temp

# add this at the end of the file
EXPORT_FUNCTION = rotate_image