from typing import List

def plus_one(digits: List[int]) -> List[int]:
    """
    Adds one to a large integer represented as a list of digits.

    The digits are stored such that the most significant digit is at the head
    of the list, and each element in the list contains a single digit.

    For example, the integer 123 is represented as [1, 2, 3].

    Args:
        digits: A list of integers representing the digits of the non-negative integer.
                Each integer in the list is between 0 and 9, inclusive.
                The list is assumed to be non-empty.

    Returns:
        A list of integers representing the digits of the incremented integer.

    Examples:
        plus_one([1, 2, 3]) == [1, 2, 4]
        plus_one([4, 3, 2, 1]) == [4, 3, 2, 2]
        plus_one([9]) == [1, 0]
        plus_one([9, 9]) == [1, 0, 0]
        plus_one([8, 9, 9]) == [9, 0, 0]
    """
    n = len(digits)

    # Iterate from the rightmost digit (least significant) to the leftmost
    for i in range(n - 1, -1, -1):
        # If the current digit is less than 9, just increment it and return
        # as no carry-over is needed for subsequent digits.
        if digits[i] < 9:
            digits[i] += 1
            return digits
        # If the current digit is 9, set it to 0 and continue the loop
        # to carry over 1 to the next more significant digit.
        else:
            digits[i] = 0
    
    # If the loop completes, it means all digits were 9 (e.g., [9], [9, 9, 9]).
    # In this case, we need to prepend a '1' to the list.
    # For example, [9, 9] becomes [0, 0] after the loop, then [1, 0, 0].
    return [1] + digits

EXPORT_FUNCTION = plus_one