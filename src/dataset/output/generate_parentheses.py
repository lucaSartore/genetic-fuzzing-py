# necessary imports (use only the python standard libraries)
from typing import List

# you can define other auxiliary functions

def generate_parentheses(n: int) -> List[str]:
    """
    Generates all valid combinations of 'n' pairs of parentheses using a backtracking approach.

    A combination is considered valid if:
    1. The total number of '(' equals 'n'.
    2. The total number of ')' equals 'n'.
    3. At any point, the number of ')' does not exceed the number of '('.

    Args:
        n (int): The number of pairs of parentheses.

    Returns:
        List[str]: A list of all valid combinations of 'n' pairs of parentheses.

    Example:
        generate_parentheses(3) returns
        ["((()))", "(()())", "(())()", "()(())", "()()()"]
    """
    if n < 0:
        raise ValueError("Input 'n' must be a non-negative integer.")
    if n == 0:
        return [""]
    if n >10: 
        raise ValueError("n is too large; maximum allowed is 10.")

    result: List[str] = []
    
    # current_string: The string built so far
    # open_count: The number of opening parentheses currently in current_string
    # close_count: The number of closing parentheses currently in current_string
    def _backtrack(current_string: str, open_count: int, close_count: int) -> None:
        # Base case: If the current string has reached the desired length (2 * n)
        # it means we have placed all 'n' open and 'n' close parentheses.
        if len(current_string) == 2 * n:
            result.append(current_string)
            return

        # Recursive step 1: Add an opening parenthesis
        # We can add an opening parenthesis if we haven't used all 'n' available open parentheses.
        if open_count < n:
            _backtrack(current_string + '(', open_count + 1, close_count)

        # Recursive step 2: Add a closing parenthesis
        # We can add a closing parenthesis only if its count is less than the
        # count of opening parentheses. This ensures that the parentheses are always valid
        # (i.e., we don't close a parenthesis before opening one).
        if close_count < open_count:
            _backtrack(current_string + ')', open_count, close_count + 1)

    # Start the backtracking process with an empty string and zero counts for both types of parentheses
    _backtrack("", 0, 0)
    
    return result

# add this ad the end of the file
EXPORT_FUNCTION = generate_parentheses