# necessary imports (use only the python standard libraries)

# no auxiliary functions needed

def transpose_jagged_matrix(matrix: list[list], padding_strategy: str = "none") -> list[list]:
    """
    Transposes a list of lists with varying lengths, with padding strategies.

    Args:
        matrix: The input list of lists (jagged matrix).
                Each inner list represents a row.
        padding_strategy: The strategy to use for handling varying row lengths.
                          Must be one of "none", "repeat", or "truncate" (case-insensitive).

                          - "none": Missing elements in shorter rows are not filled in the
                                    transposed columns. The output will have `max_row_length`
                                    columns, and each column list will only contain elements
                                    that actually existed in the original rows.
                                    Example: [[1, 2], [3, 4, 5]] -> [[1, 3], [2, 4], [5]]

                          - "repeat": Shorter rows are conceptually padded by repeating their
                                      last element to match the maximum row length. If a row
                                      is empty, it's padded with `None`.
                                      Example: [[1, 2], [3, 4, 5]] -> [[1, 3], [2, 4], [2, 5]]
                                      Example: [[1], [], [2, 3]] -> [[1, None, 2], [1, None, 3], [1, None, 3]]
                                      (assuming max length 3)

                          - "truncate": All rows are effectively truncated to the length of
                                        the shortest row before transposing.
                                        Example: [[1, 2, 3], [4, 5]] -> [[1, 4], [2, 5]]

    Returns:
        A new list of lists representing the transposed matrix.
        The outer list represents columns, and inner lists contain elements from original rows.

    Raises:
        TypeError: If 'matrix' is not a list or contains non-list elements.
        ValueError: If an invalid 'padding_strategy' is provided.
    """
    if not isinstance(matrix, list):
        raise TypeError("Input 'matrix' must be a list.")
    for row in matrix:
        if not isinstance(row, list):
            raise TypeError("All elements in 'matrix' must be lists (rows).")

    num_rows = len(matrix)
    if num_rows == 0:
        return []

    processed_strategy = padding_strategy.lower()
    if processed_strategy not in ["none", "repeat", "truncate"]:
        raise ValueError(f"Invalid padding_strategy: '{padding_strategy}'. "
                         "Must be 'none', 'repeat', or 'truncate'.")

    # Determine max and min row lengths
    max_len = 0
    min_len = float('inf')
    
    for row in matrix:
        row_len = len(row)
        max_len = max(max_len, row_len)
        min_len = min(min_len, row_len)
    
    # Handle cases where all rows are empty, or the matrix itself is empty
    if max_len == 0: # This implies min_len is also 0 and num_rows > 0 (e.g., matrix = [[]])
        return []

    if processed_strategy == "truncate":
        # If the shortest row is empty, truncating everything results in an empty matrix.
        if min_len == 0:
            return []
        
        # In truncate, the number of columns in the transposed matrix will be `min_len`.
        target_cols = min_len
        transposed: list[list] = [[] for _ in range(target_cols)]
        
        for i in range(num_rows):
            for j in range(target_cols):
                transposed[j].append(matrix[i][j])
        
        return transposed

    elif processed_strategy == "none":
        # The number of columns in the transposed matrix will be `max_len`.
        target_cols = max_len
        transposed: list[list] = [[] for _ in range(target_cols)]
        
        for i in range(num_rows):
            current_row = matrix[i]
            # Only append elements that exist in the current row
            for j in range(len(current_row)):
                transposed[j].append(current_row[j])
        
        return transposed

    elif processed_strategy == "repeat":
        # The number of columns in the transposed matrix will be `max_len`.
        target_cols = max_len
        transposed: list[list] = [[] for _ in range(target_cols)]
        
        for i in range(num_rows):
            current_row = matrix[i]
            current_row_len = len(current_row)
            
            for j in range(target_cols):
                if j < current_row_len:
                    transposed[j].append(current_row[j])
                else:
                    # Pad with the last element of the row, or None if the row was empty
                    if current_row_len > 0:
                        transposed[j].append(current_row[current_row_len - 1])
                    else:
                        transposed[j].append(None) # Pad empty rows with None
        
        return transposed

EXPORT_FUNCTION = transpose_jagged_matrix