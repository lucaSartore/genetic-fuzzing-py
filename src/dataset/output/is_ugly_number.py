# necessary imports (use only the python standard libraries)

# you can define other auxiliary functions

def is_ugly_number(num: int) -> bool:
    """
    Checks if a number's prime factors are only 2, 3, or 5.
    Such numbers are often referred to as "ugly numbers".

    Args:
        num: The integer to check.

    Returns:
        True if the number's prime factors are exclusively 2, 3, or 5,
        False otherwise.
    """
    if num <= 0:
        return False
    
    # 1 is conventionally considered an ugly number (it has no prime factors,
    # so all its prime factors are vacuously 2, 3, or 5)
    if num == 1:
        return True

    # Divide by 2 until it's no longer divisible
    while num % 2 == 0:
        num //= 2
    
    # Divide by 3 until it's no longer divisible
    while num % 3 == 0:
        num //= 3
        
    # Divide by 5 until it's no longer divisible
    while num % 5 == 0:
        num //= 5
        
    # If the number has been reduced to 1, it means all its prime factors
    # were 2, 3, or 5. Otherwise, it has other prime factors.
    return num == 1

# add this ad the end of the file
EXPORT_FUNCTION = is_ugly_number