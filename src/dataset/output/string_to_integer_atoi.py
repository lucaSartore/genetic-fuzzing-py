import sys

def string_to_integer_atoi(s: str) -> int:
    """
    Implements the 'atoi' function, parsing a string to an integer with edge cases
    (whitespace, sign, overflow).

    The function first discards any leading whitespace characters until the first
    non-whitespace character is found. Then, an optional initial plus or minus sign
    is taken into account. After that, as many numerical digits as possible are
    read until a non-digit character or the end of the input is reached.
    The numerical value is then converted to an integer.

    If no valid conversion could be performed, a zero value is returned.
    If the integer value is out of the range of a 32-bit signed integer
    [−2^31, 2^31 − 1], then INT_MIN (−2^31) or INT_MAX (2^31 − 1) is returned.

    Args:
        s: The input string to be converted.

    Returns:
        The parsed integer value, or INT_MIN/INT_MAX on overflow, or 0 if no
        valid conversion can be performed.
    """
    i = 0
    n = len(s)
    
    # Define 32-bit signed integer limits
    INT_MAX = 2**31 - 1  # 2147483647
    INT_MIN = -2**31     # -2147483648

    # 1. Discard leading whitespace
    while i < n and s[i] == ' ':
        i += 1
    
    # Handle empty string or only whitespace
    if i == n:
        return 0

    # 2. Check for sign
    sign = 1  # Default to positive
    if s[i] == '-':
        sign = -1
        i += 1
    elif s[i] == '+':
        i += 1
    
    # 3. Read digits and convert to integer, checking for overflow
    result = 0
    while i < n and s[i].isdigit():
        digit = int(s[i])

        # Check for potential overflow before multiplying and adding the digit
        if sign == 1:
            # If current result is already greater than INT_MAX // 10, it will overflow
            # Or if result is equal to INT_MAX // 10 and the current digit is > 7 (since INT_MAX ends with 7)
            if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > 7):
                return INT_MAX
        else:  # sign == -1
            # For negative numbers, we build a positive result and then apply the sign.
            # We compare with abs(INT_MIN) // 10.
            # If current result is already greater than abs(INT_MIN) // 10, it will overflow
            # Or if result is equal to abs(INT_MIN) // 10 and the current digit is > 8 (since abs(INT_MIN) ends with 8)
            # abs(INT_MIN) = 2147483648, so abs(INT_MIN) // 10 = 214748364.
            # If digit is 9, then 214748364 * 10 + 9 = 2147483649, which becomes -2147483649, overflowing INT_MIN.
            if result > abs(INT_MIN) // 10 or (result == abs(INT_MIN) // 10 and digit > 8):
                return INT_MIN
        
        result = result * 10 + digit
        i += 1
    
    # 4. Apply the sign and return the final result
    return result * sign

EXPORT_FUNCTION = string_to_integer_atoi