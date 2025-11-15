# No specific imports are necessary for the extended Euclidean algorithm
# as it primarily relies on basic arithmetic operations.

def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Implements the extended Euclidean algorithm to find the greatest common divisor (GCD)
    of two integers 'a' and 'b', and also integers 'x' and 'y' such that
    ax + by = gcd(a, b).

    The algorithm works for both positive and negative integers.
    The returned GCD will always be non-negative.

    Args:
        a: The first integer.
        b: The second integer.

    Returns:
        A tuple (gcd, x, y) where:
        - gcd: The greatest common divisor of a and b.
        - x: The coefficient for 'a' in the Bezout's identity (ax + by = gcd).
        - y: The coefficient for 'b' in the Bezout's identity (ax + by = gcd).
    """
    if a == 0 and b == 0:
        return 0, 0, 0 # Or handle as an error/specific case if desired. For now, 0*0 + 0*0 = 0.

    # Current values for a and b in the Euclidean algorithm
    # coefficients for a_orig (x0, y0) and b_orig (x1, y1)
    # The current equation is a_curr * x0 + b_curr * y0
    # and a_curr * x1 + b_curr * y1
    x0, y0 = 1, 0
    x1, y1 = 0, 1

    # Keep original values to ensure the final coefficients relate to them
    # although the iterative algorithm directly computes for the initial a and b.
    # We use temporary variables `a_curr` and `b_curr` for the algorithm itself.
    a_curr, b_curr = a, b

    while b_curr != 0:
        quotient = a_curr // b_curr  # Python's floor division
        remainder = a_curr % b_curr  # Python's modulo operator

        # Update coefficients:
        # (x_new, y_new) are coefficients for the new remainder
        x_new = x0 - quotient * x1
        y_new = y0 - quotient * y1

        # Move to the next step of the Euclidean algorithm
        a_curr = b_curr
        b_curr = remainder

        # Update coefficients for the next iteration
        x0 = x1
        y0 = y1
        x1 = x_new
        y1 = y_new

    # After the loop, a_curr holds the GCD, and (x0, y0) are the coefficients.
    # The GCD should always be non-negative.
    return a_curr, x0, y0

# add this ad the end of the file
EXPORT_FUNCTION = extended_gcd