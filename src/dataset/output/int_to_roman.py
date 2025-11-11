# necessary inputs (use only the python standard libraries)
# No specific imports are needed from standard libraries for this function.

# you can define other auxiliary functions

def int_to_roman(num: int) -> str:
    """
    Converts an integer (1-3999) to its Roman numeral representation.

    This function handles the conversion of integers to Roman numerals,
    including the special subtractive cases (e.g., IV for 4, IX for 9).
    The conversion is done by iterating through a predefined list of Roman
    numeral values and their corresponding symbols, from largest to smallest.

    Args:
        num: An integer between 1 and 3999 (inclusive).

    Returns:
        A string representing the Roman numeral of the input integer.

    Raises:
        ValueError: If the input integer `num` is not within the valid
                    range of 1 to 3999.
    """
    if not (1 <= num <= 3999):
        raise ValueError("Input integer must be between 1 and 3999.")

    # Define the Roman numeral values and their symbols.
    # It's crucial to list them in descending order of value,
    # and include the subtractive combinations (like 900 for CM)
    # before their larger components (like 500 for D or 100 for C)
    # to ensure correct processing.
    roman_map = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I')
    ]

    roman_numeral_parts = []
    current_num = num

    # Iterate through the Roman map.
    for value, symbol in roman_map:
        # While the current number is greater than or equal to the current Roman value,
        # append the symbol and subtract the value from the number.
        while current_num >= value:
            roman_numeral_parts.append(symbol)
            current_num -= value
        # Optimization: If the number becomes 0, we have completed the conversion.
        if current_num == 0:
            break

    # Join all collected symbols to form the final Roman numeral string.
    return "".join(roman_numeral_parts)

# add this ad the end of the file
EXPORT_FUNCTION = int_to_roman