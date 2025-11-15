# necessary imports (use only the python standard libraries)
# No special imports are required for this problem as it uses only basic arithmetic and list operations.

# you can define other auxiliary functions

def house_robber(houses: list[int]) -> int:
    """
    Finds the maximum amount you can rob from houses in a line without robbing adjacent ones.
    This problem is solved using dynamic programming with O(1) space complexity.

    Args:
        houses: A list of integers where houses[i] represents the amount of money
                in the i-th house.

    Returns:
        The maximum amount of money you can rob from the given houses
        following the rule of not robbing adjacent houses.
    """
    n = len(houses)

    # Base cases:
    # If there are no houses, no money can be robbed.
    if n == 0:
        return 0
    # If there is only one house, rob that house.
    if n == 1:
        return houses[0]

    # Dynamic Programming Approach (O(1) space optimization):
    # We only need to keep track of the maximum amounts from the previous two houses.
    # rob_prev_prev: Represents the maximum amount robbed up to house (i-2).
    # rob_prev: Represents the maximum amount robbed up to house (i-1).
    
    # Initialize for the first two houses effectively (before loop starts,
    # imagine we've processed '0' houses, then 1st house).
    # 'rob_prev_prev' stores max_money up to 'current_house - 2'
    # 'rob_prev' stores max_money up to 'current_house - 1'

    # When considering the first house in the loop, rob_prev_prev and rob_prev
    # effectively represent the max money from 0 houses (which is 0).
    rob_prev_prev = 0
    rob_prev = 0

    # Iterate through each house to calculate the maximum amount
    for current_house_money in houses:
        # Calculate the maximum amount for the current house.
        # There are two choices:
        # 1. Rob the current house: In this case, we cannot rob the previous house.
        #    So, the total would be current_house_money + rob_prev_prev (max from houses up to i-2).
        # 2. Don't rob the current house: In this case, the maximum amount is
        #    the same as the maximum amount robbed up to the previous house (rob_prev).
        # We take the maximum of these two options.
        current_max = max(rob_prev, current_house_money + rob_prev_prev)

        # Update rob_prev_prev and rob_prev for the next iteration:
        # The old rob_prev becomes the new rob_prev_prev.
        # The current_max becomes the new rob_prev.
        rob_prev_prev = rob_prev
        rob_prev = current_max

    # After iterating through all houses, rob_prev will hold the maximum amount
    # that can be robbed from all houses.
    return rob_prev

# add this at the end of the file
EXPORT_FUNCTION = house_robber