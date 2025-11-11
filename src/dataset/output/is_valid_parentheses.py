# necessary inputs (use only the python standard libraries)

# you can define other auxiliary functions

def is_valid_parentheses(s: str) -> bool:
    """
    Checks if a string of '()[]{}' is balanced and properly nested using a stack.

    Args:
        s (str): The input string containing parentheses, brackets, and braces.

    Returns:
        bool: True if the string is balanced and properly nested, False otherwise.
    """
    
    stack: list[str] = []
    
    # Define sets for opening brackets and a dictionary for matching pairs
    opening_brackets: set[str] = {'(', '[', '{'}
    matching_pairs: dict[str, str] = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    
    for char in s:
        if char in opening_brackets:
            # If it's an opening bracket, push it onto the stack
            stack.append(char)
        elif char in matching_pairs:
            # If it's a closing bracket
            # 1. Check if the stack is empty (no corresponding opening bracket)
            if not stack:
                return False
            
            # 2. Pop the top element from the stack
            top_of_stack = stack.pop()
            
            # 3. Check if the popped element matches the expected opening bracket
            #    for the current closing bracket
            if matching_pairs[char] != top_of_stack:
                return False
        # If the string can contain other characters, they would be ignored here.
        # Per problem description, we assume the string only contains '()[]{}'.

    # After iterating through the string, if the stack is empty,
    # all opening brackets have been correctly closed and matched.
    return not stack

# add this ad the end of the file
EXPORT_FUNCTION = is_valid_parentheses