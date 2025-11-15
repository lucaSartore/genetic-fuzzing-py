# necessary imports (use only the python standard libraries)

# you can define other auxiliary functions

def unique_paths(target_row: int, target_col: int) -> int:
    """
    Finds the number of unique paths from (0,0) to (target_row, target_col) in a grid,
    moving only right or down.

    This problem is solved using dynamic programming.
    A robot starts at cell (0,0) and wants to reach cell (target_row, target_col).
    It can only move right or down.

    Args:
        target_row: The 0-indexed row coordinate of the destination cell (m in the problem description).
                    Must be a non-negative integer.
        target_col: The 0-indexed column coordinate of the destination cell (n in the problem description).
                    Must be a non-negative integer.

    Returns:
        The total number of unique paths from (0,0) to (target_row, target_col).

    Raises:
        ValueError: If target_row or target_col is negative.
    """
    if target_row < 0 or target_col < 0:
        raise ValueError("Grid dimensions (target_row, target_col) must be non-negative.")

    # Initialize a DP table with dimensions (target_row + 1) x (target_col + 1).
    # dp[i][j] will store the number of unique paths to reach cell (i, j).
    dp = [[0] * (target_col + 1) for _ in range(target_row + 1)]

    # Base cases:
    # 1. Cells in the first row (i=0): There's only one way to reach any cell (0, j)
    #    from (0,0) - by moving right j times.
    for j in range(target_col + 1):
        dp[0][j] = 1

    # 2. Cells in the first column (j=0): There's only one way to reach any cell (i, 0)
    #    from (0,0) - by moving down i times.
    #    Note: dp[0][0] will be set to 1 by both loops, which is correct (starting point).
    for i in range(target_row + 1):
        dp[i][0] = 1

    # Fill the DP table using the recurrence relation:
    # To reach cell (i, j), the robot must have come from either (i-1, j) (moved down)
    # or from (i, j-1) (moved right).
    # So, dp[i][j] = dp[i-1][j] + dp[i][j-1].
    for i in range(1, target_row + 1):
        for j in range(1, target_col + 1):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    # The result is the value stored at the target cell.
    return dp[target_row][target_col]

# add this ad the end of the file
EXPORT_FUNCTION = unique_paths