# necessary imports (use only the python standard libraries)
# No specific imports are needed for this function, as it uses built-in types and functions.

# you can define other auxiliary functions

def excel_sheet_column_title(column_number: int) -> str:
    """
    Converts a positive integer to its corresponding Excel column title.

    For example:
    1 -> A
    26 -> Z
    27 -> AA
    52 -> AZ
    703 -> AAA

    Args:
        column_number (int): A positive integer representing the column number.

    Returns:
        str: The Excel column title.

    Raises:
        ValueError: If the column_number is not a positive integer.
    """
    if not isinstance(column_number, int) or column_number <= 0:
        raise ValueError("Column number must be a positive integer.")

    result_chars = []
    while column_number > 0:
        # Excel column titles are 1-indexed (A=1, B=2, ..., Z=26)
        # To convert this to a 0-indexed system (A=0, B=1, ..., Z=25) for
        # modulo arithmetic, we subtract 1 from the column_number first.
        column_number -= 1

        # The remainder gives us the 0-indexed character for the current position
        remainder = column_number % 26

        # Convert the 0-indexed remainder to its corresponding character
        # 'A' has ASCII value ord('A'), 'B' is ord('A')+1, etc.
        char = chr(ord('A') + remainder)
        result_chars.append(char)

        # Update column_number for the next iteration by integer division
        # This effectively moves to the next "digit" position (e.g., from unit to tens)
        column_number //= 26

    # The characters are collected in reverse order (least significant first)
    # so we need to reverse the list before joining them into a string.
    return "".join(reversed(result_chars))

# add this ad the end of the file
EXPORT_FUNCTION = excel_sheet_column_title