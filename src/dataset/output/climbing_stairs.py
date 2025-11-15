# necessary imports (use only the python standard libraries)
# No specific imports are required for this problem, as it uses basic arithmetic and data types.

def climbing_stairs(n: int) -> int:
    """
    Finds the number of distinct ways to climb 'n' stairs, taking 1 or 2 steps at a time.
    This is a classic dynamic programming problem, which boils down to the Fibonacci sequence.

    Args:
        n (int): The total number of stairs to climb.
                 Must be a non-negative integer.

    Returns:
        int: The number of distinct ways to climb 'n' stairs.

    Examples:
        climbing_stairs(0) == 1  (There's one way to climb 0 stairs: do nothing)
        climbing_stairs(1) == 1  (1 way: [1])
        climbing_stairs(2) == 2  (2 ways: [1, 1], [2])
        climbing_stairs(3) == 3  (3 ways: [1, 1, 1], [1, 2], [2, 1])
        climbing_stairs(4) == 5  (5 ways: [1, 1, 1, 1], [1, 1, 2], [1, 2, 1], [2, 1, 1], [2, 2])
    """
    if n < 0:
        raise ValueError("Number of stairs cannot be negative.")
    
    # Base cases
    # If n = 0, there is 1 way (do nothing).
    # If n = 1, there is 1 way (take 1 step).
    if n <= 1:
        return 1

    # For n > 1, the number of ways to reach stair 'n' is the sum of:
    # 1. Ways to reach stair 'n-1' and then take a 1-step.
    # 2. Ways to reach stair 'n-2' and then take a 2-step.
    # This is effectively the Fibonacci sequence: F(n) = F(n-1) + F(n-2)
    # with a slight shift in indexing if we consider F(0)=1, F(1)=1.

    # We use a space-optimized dynamic programming approach,
    # keeping track of only the last two results.
    ways_to_n_minus_2 = 1  # Represents ways to climb (i-2) stairs, initially ways to climb 0 stairs
    ways_to_n_minus_1 = 1  # Represents ways to climb (i-1) stairs, initially ways to climb 1 stair

    for _ in range(2, n + 1):
        # Calculate ways to climb current stair 'i'
        current_ways = ways_to_n_minus_1 + ways_to_n_minus_2
        
        # Update for the next iteration
        ways_to_n_minus_2 = ways_to_n_minus_1
        ways_to_n_minus_1 = current_ways

    return ways_to_n_minus_1

# add this at the end of the file
EXPORT_FUNCTION = climbing_stairs