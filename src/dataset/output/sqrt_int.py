# necessary imports (use only the python standard libraries)

def sqrt_int(x: int) -> int:
    """
    Finds the integer square root of 'x' using binary search.

    The integer square root of x is the largest integer k such that k*k <= x.
    This function handles non-negative integers only.

    Args:
        x: A non-negative integer for which to find the integer square root.

    Returns:
        The integer square root of x.

    Raises:
        ValueError: If x is a negative integer.
    """
    if x < 0:
        raise ValueError("Cannot compute integer square root for negative numbers.")

    if x == 0 or x == 1:
        return x

    low = 1  # The square root of x will be at least 1 for x >= 1
    high = x # The square root of x will be at most x

    ans = 0 # Stores the potential answer (largest k such that k*k <= x)

    while low <= high:
        mid = low + (high - low) // 2
        mid_squared = mid * mid

        if mid_squared == x:
            return mid
        elif mid_squared < x:
            # mid is a potential answer, but we try to find a larger one
            ans = mid
            low = mid + 1
        else:
            # mid_squared is too large, search in the lower half
            high = mid - 1
            
    return ans

# add this ad the end of the file
EXPORT_FUNCTION = sqrt_int