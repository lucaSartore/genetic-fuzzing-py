# necessary imports (use only the python standard libraries)

# you can define other auxiliary functions

def coin_change(coins: list[int], amount: int) -> int:
    """
    Finds the fewest number of coins needed to make 'amount'.

    This function uses dynamic programming to solve the coin change problem.
    Given a list of coin denominations and a target amount, it calculates
    the minimum number of coins required to reach that amount.

    Args:
        coins: A list of integers representing the available coin denominations.
               Assume coin denominations are positive integers.
        amount: An integer representing the target amount. Assume amount is
                a non-negative integer.

    Returns:
        An integer representing the minimum number of coins needed.
        Returns -1 if the amount cannot be made by any combination of the given coins.
    """
    # dp[i] will store the minimum number of coins needed to make amount i
    # Initialize dp array with float('inf') for all amounts from 1 to 'amount'
    # dp[0] is 0 because 0 coins are needed to make amount 0
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    # Iterate through each possible amount from 1 up to the target amount
    for i in range(1, amount + 1):
        # For each amount i, iterate through all available coin denominations
        for coin in coins:
            # If the current coin can be used (i.e., i - coin is not negative)
            if i - coin >= 0:
                # Update dp[i] with the minimum of its current value
                # and (dp[i - coin] + 1)
                # dp[i - coin] + 1 means using one 'coin' and then
                # finding the minimum coins for the remaining amount (i - coin)
                dp[i] = min(dp[i], dp[i - coin] + 1)

    # After filling the dp array, dp[amount] will contain the minimum coins
    # needed for the target amount.
    # If dp[amount] is still float('inf'), it means the amount cannot be made.
    return dp[amount] if dp[amount] != float('inf') else -1

# add this ad the end of the file
EXPORT_FUNCTION = coin_change