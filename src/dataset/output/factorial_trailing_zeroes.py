# necessary imports (use only the python standard libraries)

def factorial_trailing_zeroes(n: int) -> int:
    """
    Finds the number of trailing zeroes in 'n!'.

    A trailing zero in a factorial number is produced by a factor of 10.
    Since 10 = 2 * 5, we need to count how many pairs of (2, 5) exist
    in the prime factorization of n!.
    Because there are always more factors of 2 than factors of 5,
    the number of trailing zeroes is determined by the number of factors of 5.

    The number of factors of 5 in n! can be found by summing up
    the number of multiples of 5, 25, 125, etc., up to n.
    This is based on Legendre's formula: n! = sum(n / 5^k) for k >= 1.

    Args:
        n (int): The non-negative integer for which to calculate the
                 number of trailing zeroes in its factorial.

    Returns:
        int: The number of trailing zeroes in n!.

    Raises:
        ValueError: If n is a negative integer.

    Examples:
        >>> factorial_trailing_zeroes(0)
        0
        >>> factorial_trailing_zeroes(4)
        0
        >>> factorial_trailing_zeroes(5)
        1
        >>> factorial_trailing_zeroes(10)
        2
        >>> factorial_trailing_zeroes(25)
        6
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")

    count = 0
    i = 5
    while n // i >= 1:
        count += n // i
        i *= 5  # Go to the next power of 5 (25, 125, etc.)
    return count

# add this ad the end of the file
EXPORT_FUNCTION = factorial_trailing_zeroes