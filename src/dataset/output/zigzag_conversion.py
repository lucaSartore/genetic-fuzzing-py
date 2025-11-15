# no necessary imports for this problem (uses built-in types and operations)

def zigzag_conversion(s: str, num_rows: int) -> str:
    """
    Converts a string into a zigzag pattern based on the given number of rows
    and reads it line by line to form a new string.

    For example, given s = "PAYPALISHIRING" and num_rows = 3:
    P   A   H   N
    A P L S I I G
    Y   I   R
    The output would be "PAHNAPLSIIGYIR".

    Args:
        s: The input string to convert.
        num_rows: The number of rows to use for the zigzag pattern.

    Returns:
        The string read line by line after forming the zigzag pattern.
    """
    if num_rows == 1 or len(s) <= num_rows:
        return s

    # Create a list of strings, one for each row.
    # Each row will collect characters that belong to it.
    rows: list[str] = [""] * num_rows

    current_row: int = 0
    # direction: 1 means moving down, -1 means moving up
    direction: int = -1 

    for char in s:
        rows[current_row] += char

        # Change direction when we hit the top or bottom row
        if current_row == 0 or current_row == num_rows - 1:
            direction *= -1
        
        current_row += direction

    # Join all the strings in the rows list to get the final zigzag pattern string.
    return "".join(rows)

# add this at the end of the file
EXPORT_FUNCTION = zigzag_conversion