# necessary imports (use only the python standard libraries)
# No special imports are needed for this problem, as we only use built-in string, list, and integer operations.

def multiply_strings(num1: str, num2: str) -> str:
    """
    Multiplies two large numbers represented as strings.

    Handles positive and negative numbers, as well as zero.
    The algorithm simulates manual long multiplication.
    """

    # 1. Handle signs and convert numbers to their absolute string values
    s1_is_negative = False
    s2_is_negative = False

    if num1.startswith('-'):
        s1_is_negative = True
        num1 = num1[1:]
    if num2.startswith('-'):
        s2_is_negative = True
        num2 = num2[1:]

    # Remove leading zeros from the absolute values
    num1 = num1.lstrip('0')
    num2 = num2.lstrip('0')

    # 2. Handle cases where one or both numbers are '0'
    # After stripping leading zeros, if a number was "0" or "000", it becomes an empty string.
    # If it was "0", it remains "0" if we don't strip it. Let's make sure '0' itself is covered.
    if not num1 or not num2 or num1 == "0" or num2 == "0":
        return "0"
    
    # 3. Determine the final sign of the result
    # If signs are different, result is negative. Otherwise, positive.
    final_sign = '-' if s1_is_negative != s2_is_negative else ''

    # 4. Initialize result array for multiplication
    # The maximum length of the product of two numbers of length m and n is m + n.
    m = len(num1)
    n = len(num2)
    result = [0] * (m + n)

    # Reverse numbers for easier digit-by-digit processing (least significant digit first)
    num1_rev = num1[::-1]
    num2_rev = num2[::-1]

    # 5. Perform digit-by-digit multiplication
    # For each digit in num1_rev
    for i in range(m):
        d1 = int(num1_rev[i])
        # For each digit in num2_rev
        for j in range(n):
            d2 = int(num2_rev[j])
            # The product of digits d1 and d2 contributes to the position i + j in the result
            result[i + j] += d1 * d2

    # 6. Propagate carries through the result array
    # Iterate from left to right (least significant to most significant digit)
    for k in range(len(result)):
        # Calculate the carry and the digit at the current position
        carry = result[k] // 10
        result[k] %= 10 # Keep only the unit digit
        
        # Add the carry to the next position, if it exists
        if k + 1 < len(result):
            result[k + 1] += carry
        # Note: If there's a carry at the last position (result[m+n-1]), it will be handled
        # and if it results in a value > 9, result[m+n-1] will store the unit digit and the
        # carry part would normally extend the array. However, our array size m+n is sufficient
        # to hold any carry because max product (9*9) results in 81 (2 digits), max sum in one position
        # is N*81 for N multiplications, then carries will propagate. The (m+n) length is enough.

    # 7. Convert the digit array to a string
    # Reverse the result array to get digits in correct order (most significant first)
    # and convert to string.
    result_str_list = [str(digit) for digit in result]
    
    # The result array is [least significant, ..., most significant], so we need to reverse it.
    final_num_str = "".join(result_str_list[::-1])

    # 8. Remove any leading zeros from the final number string (e.g., "05535" -> "5535")
    # This also handles cases where multiplication result might be "0" but stored as "000".
    final_num_str = final_num_str.lstrip('0')

    # If after stripping leading zeros, the string is empty, it means the result was "0".
    if not final_num_str:
        return "0"

    # 9. Apply the determined sign
    return final_sign + final_num_str

# add this ad the end of the file
EXPORT_FUNCTION = multiply_strings