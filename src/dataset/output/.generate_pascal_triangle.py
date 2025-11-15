# necessary imports (use only the python standard libraries)
from typing import List

# you can define other auxiliary functions

def generate_pascal_triangle(num_rows: int) -> List[List[int]]:
    """
    Generates Pascal's triangle up to 'num_rows'.

    Args:
        num_rows (int): The number of rows to generate in Pascal's triangle.

    Returns:
        List[List[int]]: A list of lists representing Pascal's triangle.
                          Each inner list is a row of the triangle.
                          Returns an empty list if num_rows is less than or equal to 0.
    """
    triangle: List[List[int]] = []

    if num_rows <= 0:
        return triangle

    # First row is always [1]
    triangle.append([1])

    for r in range(1, num_rows):
        prev_row = triangle[r - 1]
        current_row: List[int] = [1]  # Each row starts with 1

        # Calculate the intermediate elements
        # Each element is the sum of the two numbers directly above it
        for i in range(1, len(prev_row)):
            current_row.append(prev_row[i - 1] + prev_row[i])
        
        current_row.append(1)  # Each row ends with 1
        triangle.append(current_row)

    return triangle

# add this ad the end of the file
EXPORT_FUNCTION = generate_pascal_triangle