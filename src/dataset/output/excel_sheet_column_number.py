# necessary imports (use only the python standard libraries)
# No specific imports are needed for this problem, as it only involves string iteration and arithmetic.

# you can define other auxiliary functions

def excel_sheet_column_number(column_title: str) -> int:
    """
    Converts an Excel column title (e.g., "A", "AB", "ZY") to its corresponding
    integer representation (e.g., 1, 28, 701).

    Excel column titles are similar to a base-26 number system, but with a key difference:
    'A' corresponds to 1, 'B' to 2, ..., 'Z' to 26. There is no '0' equivalent.
    This means 'AA' is 27 (1*26 + 1), not 26.

    The conversion works by iterating through the column title from left to right.
    For each character, it updates a running total:
    `result = result * 26 + (value_of_current_character)`

    For example, for the column title "AB":
    1. Initialize `result = 0`.
    2. Process 'A':
       `char_value` for 'A' is `ord('A') - ord('A') + 1 = 1`.
       `result = 0 * 26 + 1 = 1`.
    3. Process 'B':
       `char_value` for 'B' is `ord('B') - ord('A') + 1 = 2`.
       `result = 1 * 26 + 2 = 26 + 2 = 28`.

    Args:
        column_title: A string representing the Excel column title (e.g., "A", "AA", "ABC").
                      Assumes the input consists only of uppercase English letters.
                      Example: "A" -> 1, "Z" -> 26, "AA" -> 27, "AB" -> 28.

    Returns:
        An integer representing the column number.
    """
    result = 0
    # Iterate through each character in the column title string
    for char in column_title:
        # Calculate the numeric value of the current character.
        # 'A' corresponds to 1, 'B' to 2, ..., 'Z' to 26.
        # `ord(char)` gives the ASCII value of the character.
        # Subtracting `ord('A')` makes 'A' equivalent to 0, 'B' to 1, etc.
        # Adding 1 makes 'A' equivalent to 1, 'B' to 2, etc.
        char_value = ord(char) - ord('A') + 1
        
        # Update the total result.
        # For each new character, we effectively shift the previous result one "place"
        # in base-26 (by multiplying by 26) and then add the value of the current character.
        result = result * 26 + char_value
        
    return result

# add this ad the end of the file
EXPORT_FUNCTION = excel_sheet_column_number