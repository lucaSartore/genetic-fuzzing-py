# necessary imports (use only the python standard libraries)
# No special imports are needed as this function uses only built-in types and operations.

# you can define other auxiliary functions

def fraction_to_recurring_decimal(numerator: int, denominator: int) -> str:
    """
    Converts a fraction (numerator/denominator) to its string representation,
    handling recurring decimals by enclosing the repeating part in parentheses.

    Args:
        numerator: The numerator of the fraction.
        denominator: The denominator of the fraction.

    Returns:
        A string representation of the fraction.

    Raises:
        ZeroDivisionError: If the denominator is 0.

    Examples:
        >>> fraction_to_recurring_decimal(1, 2)
        '0.5'
        >>> fraction_to_recurring_decimal(1, 3)
        '0.(3)'
        >>> fraction_to_recurring_decimal(1, 7)
        '0.(142857)'
        >>> fraction_to_recurring_decimal(5, 4)
        '1.25'
        >>> fraction_to_recurring_decimal(2, 1)
        '2'
        >>> fraction_to_recurring_decimal(0, 5)
        '0'
        >>> fraction_to_recurring_decimal(-1, 2)
        '-0.5'
        >>> fraction_to_recurring_decimal(1, -2)
        '-0.5'
        >>> fraction_to_recurring_decimal(-1, -3)
        '0.(3)'
    """
    if denominator == 0:
        raise ZeroDivisionError("Denominator cannot be zero.")

    if numerator == 0:
        return "0"

    # Determine the sign of the result
    sign = ""
    # If one is negative and the other is positive, the result is negative.
    if (numerator < 0) != (denominator < 0):
        sign = "-"
    
    # Work with absolute values for calculations to simplify the logic.
    abs_numerator = abs(numerator)
    abs_denominator = abs(denominator)

    # Calculate the integer part
    integer_part = abs_numerator // abs_denominator
    
    # Initialize the list to store parts of the final result string
    result_parts = [sign, str(integer_part)]

    # Calculate the initial remainder for the fractional part
    remainder = abs_numerator % abs_denominator

    # If remainder is 0, it means the fraction is an integer or terminates
    # exactly, so there's no fractional part or it's implicitly handled
    # by `integer_part`.
    if remainder == 0:
        return "".join(result_parts)

    # This dictionary will store remainders encountered during the division
    # process and their corresponding positions (index) in the `fractional_digits` list.
    # This is crucial for detecting and marking recurring decimals.
    remainder_map: dict[int, int] = {}
    
    # This list will store the digits of the fractional part as strings.
    fractional_digits: list[str] = []
    
    # Build the fractional part by performing long division
    while remainder != 0:
        # If this remainder has been seen before, we've found a repeating cycle.
        if remainder in remainder_map:
            # Get the index where the cycle starts from our map.
            start_index = remainder_map[remainder]
            # Insert an opening parenthesis at the start of the repeating cycle
            # and a closing parenthesis at the current end of the fractional digits.
            fractional_digits.insert(start_index, '(')
            fractional_digits.append(')')
            break # Exit loop as the recurrence is handled.
        
        # If the remainder is new, store it along with the current length
        # of `fractional_digits` (which is its position in the string).
        remainder_map[remainder] = len(fractional_digits)
        
        # Multiply the remainder by 10 to get the next digit in the decimal expansion.
        remainder *= 10
        
        # Get the next digit for the fractional part.
        digit = remainder // abs_denominator
        fractional_digits.append(str(digit))
        
        # Update the remainder for the next iteration.
        remainder %= abs_denominator
    
    # After the loop, if there are any fractional digits (meaning the decimal
    # part exists), add a decimal point and the collected digits.
    # We only add a decimal point if `fractional_digits` is not empty.
    if fractional_digits:
        result_parts.append('.')
        result_parts.extend(fractional_digits)
    
    return "".join(result_parts)

# add this ad the end of the file
EXPORT_FUNCTION = fraction_to_recurring_decimal