# necessary inputs (use only the python standard libraries)
# No external libraries are needed beyond built-in types and operations.

# you can define other auxiliary functions

def string_to_integer_atoi(s: str) -> int:
    """
    Implements the 'atoi' function, parsing a string to an integer with edge cases
    including whitespace, sign, and 32-bit signed integer overflow.

    The function processes the input string `s` in several steps:
    1.  **Discard Leading Whitespace**: It first discards any leading whitespace
        characters (' ') until the first non-whitespace character is found.
    2.  **Determine Sign**: It then checks if the next character is '-' or '+'.
        If it is, this character determines the sign of the integer (negative or
        positive, respectively). If neither, the sign is implicitly positive.
        The pointer is advanced past the sign character.
    3.  **Read Digits**: Subsequently, it reads as many numerical digits as
        possible until a non-digit character or the end of the string is reached.
        If no digits are found after the initial whitespace and optional sign,
        the integer value defaults to 0.
    4.  **Convert and Handle Overflow**: The collected digits are converted to
        an integer. During this process, it continuously checks for 32-bit
        signed integer overflow. The valid range for a 32-bit signed integer is
        [-2^31, 2^31 - 1].
        - If the number would exceed `2^31 - 1` (INT_MAX), it returns `INT_MAX`.
        - If the number would fall below `-2^31` (INT_MIN), it returns `INT_MIN`.
    5.  **Apply Sign**: The final integer is then adjusted for the sign determined
        in step 2.

    Args:
        s: The input string to be converted.

    Returns:
        The converted integer. Returns `INT_MAX` or `INT_MIN` in case of
        overflow, and `0` if no valid conversion could be performed (e.g.,
        "words and 987", "  ", "+-12").
    """
    # Define 32-bit signed integer limits
    INT_MAX = 2**31 - 1  # 2,147,483,647
    INT_MIN = -2**31     # -2,147,483,648

    n = len(s)
    i = 0
    result = 0
    sign = 1  # Default to positive

    # 1. Skip leading whitespace
    while i < n and s[i] == ' ':
        i += 1

    # If all characters were whitespace or the string is empty after skipping, return 0
    if i == n:
        return 0

    # 2. Handle sign
    if s[i] == '-':
        sign = -1
        i += 1
    elif s[i] == '+':
        # Explicitly handle '+', although sign is already 1
        i += 1

    # 3. Read digits and convert
    while i < n and s[i].isdigit():
        digit = int(s[i])

        # Check for overflow BEFORE adding the digit
        # For positive numbers:
        # If 'result' is already greater than INT_MAX // 10, then 'result * 10' will overflow.
        # If 'result' is equal to INT_MAX // 10, then adding 'digit' must not exceed INT_MAX % 10.
        if sign == 1:
            if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > INT_MAX % 10):
                return INT_MAX
        # For negative numbers:
        # We build the absolute value in `result` (which is always positive here).
        # The maximum absolute value for INT_MIN is 2**31 (i.e., |-2147483648| = 2147483648).
        # So we compare `result` against -(INT_MIN // 10) and `digit` against -(INT_MIN % 10).
        # Note: -(INT_MIN // 10) correctly gives 214748364, and -(INT_MIN % 10) gives 8.
        else: # sign == -1
            if result > -(INT_MIN // 10) or (result == -(INT_MIN // 10) and digit > -(INT_MIN % 10)):
                return INT_MIN

        result = result * 10 + digit
        i += 1

    # Apply the determined sign and return the final integer
    return result * sign

# add this ad the end of the file
EXPORT_FUNCTION = string_to_integer_atoi