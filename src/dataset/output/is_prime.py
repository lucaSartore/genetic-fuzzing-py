import math

def is_prime(n: int) -> bool:
    """
    Checks if an integer 'n' is a prime number.

    Args:
        n (int): The integer to check.

    Returns:
        bool: True if 'n' is a prime number, False otherwise.

    Edge cases handled:
    - 0, 1, negative numbers (not prime).
    - 2, 3 (are prime).
    - Even numbers > 2 (not prime).
    - Multiples of 3 > 3 (not prime).
    - Efficiently handles larger numbers by checking divisors up to sqrt(n)
      using an optimized step.
    """
    # Edge cases: 0, 1, and negative numbers are not prime
    if n <= 1:
        return False
    # 2 and 3 are prime numbers
    if n == 2 or n == 3:
        return True
    # Any even number greater than 2 is not prime
    # Any multiple of 3 greater than 3 is not prime
    if n % 2 == 0 or n % 3 == 0:
        return False

    # All prime numbers greater than 3 can be expressed in the form 6k ± 1.
    # We only need to check divisors up to the square root of n.
    # math.isqrt(n) is equivalent to int(math.sqrt(n)) but often more efficient for integers.
    i = 5
    while i * i <= n:
        # Check for divisibility by i (6k - 1 form)
        if n % i == 0:
            return False
        # Check for divisibility by i + 2 (6k + 1 form)
        if n % (i + 2) == 0:
            return False
        # Increment by 6 to check the next pair (6k+5 and 6k+7)
        i += 6

    # If no divisors were found, the number is prime
    return True

# add this at the end of the file
EXPORT_FUNCTION = is_prime