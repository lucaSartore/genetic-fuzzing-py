# no specific imports are necessary from the python standard libraries for this implementation

def _pow_positive_integer(base: int, exp: int) -> int:
    """
    Calculates base raised to a non-negative integer exponent using exponentiation by squaring.
    This helper function is designed for integer results where exp >= 0.

    Args:
        base: The integer base.
        exp: The non-negative integer exponent.

    Returns:
        The integer result of base raised to the power of exp.
    """
    if exp < 0:
        raise ValueError("Exponent must be non-negative for this helper function.")

    # Special case: x^0 = 1 for any x (including 0^0 in Python's behavior)
    if exp == 0:
        return 1
    
    # Special case: 0^positive_n = 0
    if base == 0:
        return 0

    result = 1
    current_base = base
    current_exp = exp

    while current_exp > 0:
        # If current_exp is odd, multiply result by current_base
        if current_exp % 2 == 1:
            result *= current_base
        
        # Square the current_base for the next iteration
        current_base *= current_base
        
        # Halve the exponent
        current_exp //= 2
    
    return result

def pow_int(x: int, n: int) -> int | float:
    """
    Implements 'pow(x, n)' for integers, handling negative exponents.

    This function calculates x raised to the power of n.
    - If n is non-negative, the result is an integer.
    - If n is negative, the result is a float (1.0 / (x**|n|)).

    Args:
        x: The base integer.
        n: The exponent integer.

    Returns:
        The result of x raised to the power of n.
        Returns an int if n >= 0, a float if n < 0.

    Raises:
        ZeroDivisionError: If x is 0 and n is negative, as division by zero would occur.
    """
    if n < 0:
        # Handle negative exponents
        if x == 0:
            raise ZeroDivisionError("0.0 cannot be raised to a negative power")
        
        # Calculate x raised to the positive absolute value of n
        positive_n_result = _pow_positive_integer(x, -n)
        
        # The final result is 1.0 divided by the positive result
        return 1.0 / positive_n_result
    else:
        # Handle non-negative exponents directly using the helper
        return _pow_positive_integer(x, n)

# add this ad the end of the file
EXPORT_FUNCTION = pow_int