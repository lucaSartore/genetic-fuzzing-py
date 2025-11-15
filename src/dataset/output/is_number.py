# necessary imports (use only the python standard libraries)
# No specific imports are needed for this function from the standard library.

# you can define other auxiliary functions
# No auxiliary functions are needed for this implementation.

def is_number(s: str) -> bool:
    """
    Validates if a string represents a valid number, including complex edge cases
    like scientific notation (e.g., '-1.2e+5').

    This function implements a robust state-machine-like parser to handle various
    forms of valid numbers and reject invalid formats.

    A string is considered a valid number if it adheres to the following structure:
    1. An optional leading sign ('+' or '-').
    2. A mantissa part, which can be:
       a. Digits (integer part).
       b. Digits followed by a decimal point ('.').
       c. A decimal point ('.') followed by digits (fractional part).
       d. Digits, a decimal point ('.'), and more digits.
       Crucially, there must be at least one digit either before or after the decimal point
       if a decimal point is present (e.g., "1.", ".1", "1.2" are valid, but "." is not).
       The mantissa itself must contain at least one digit.
    3. An optional exponent part, which starts with 'e' or 'E':
       a. Followed by an optional sign ('+' or '-').
       b. Followed by one or more digits.
       The exponent part is invalid if 'e'/'E' is not followed by at least one digit
       (e.g., "1e", "1e+", "1e-" are invalid).

    Examples of valid numbers:
    "0", "123", "-123", "+123", "0.0", "123.45", "-123.45", "+123.45"
    ".123", "-.123", "123.", "+123.", "-123."
    "1e0", "1e10", "1e-10", "1e+10", "1.2e3", "-1.2e+3", "+1.2e-3"
    ".1e5", "-.1e5", "1.e-5", "-1.e+5", "123e4"

    Examples of invalid numbers:
    "", " ", "abc", "1a", "e1", ".", "+.", "-.", "1e", "1e+", "1e-"
    "-.e1", "1.2.3", "++1", "1--", "1e-e2", "e", "E"
    Special values like "inf", "-inf", "nan" are not considered valid numbers by this function.
    No leading/trailing whitespace or whitespace within the number is allowed.

    Args:
        s: The input string to validate.

    Returns:
        True if the string represents a valid number according to the rules, False otherwise.
    """
    if not s:
        return False

    i = 0  # Current index in the string
    n = len(s) # Length of the string

    # 1. Handle optional leading sign ('+' or '-')
    if i < n and (s[i] == '+' or s[i] == '-'):
        i += 1

    # Flag to track if we've seen any digits in the mantissa part (before 'e'/'E').
    # This is crucial for validating cases like ".", "e1", "+.e1".
    num_digits_mantissa = 0

    # 2. Parse the integer part of the mantissa
    while i < n and s[i].isdigit():
        num_digits_mantissa += 1
        i += 1

    # 3. Handle optional decimal point and fractional part
    if i < n and s[i] == '.':
        # Consume the decimal point
        i += 1
        # Parse the fractional part digits
        while i < n and s[i].isdigit():
            num_digits_mantissa += 1
            i += 1

    # A valid number must have at least one digit in its mantissa.
    # This check correctly catches cases like ".", "+.", "-.", "e1", "+e1", "-e1"
    # which are invalid because no digits were found in the integer or fractional parts.
    if num_digits_mantissa == 0:
        return False

    # 4. Handle optional exponent part ('e' or 'E')
    if i < n and (s[i] == 'e' or s[i] == 'E'):
        # Consume 'e' or 'E'
        i += 1

        # Optional sign for the exponent part
        if i < n and (s[i] == '+' or s[i] == '-'):
            i += 1

        # The exponent part must have at least one digit following 'e'/'E' and optional sign.
        num_digits_exponent = 0
        while i < n and s[i].isdigit():
            num_digits_exponent += 1
            i += 1

        # If no digits were found after 'e'/'E' (and optional sign), it's invalid.
        # E.g., "1e", "1e+", "1e-" are caught here.
        if num_digits_exponent == 0:
            return False

    # 5. After parsing, the entire string must have been consumed for it to be a valid number.
    # If `i` is less than `n`, it means there are unparsed, invalid characters remaining
    # (e.g., "123a", "1.2.3", "123 e", "1e2.3").
    return i == n

# add this ad the end of the file
EXPORT_FUNCTION = is_number