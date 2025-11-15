# necessary imports (use only the python standard libraries)
# No special imports are needed as basic list operations suffice for a stack.

# you can define other auxiliary functions
# (None are strictly necessary for this specific implementation,
# but the template allows for them if a more complex helper structure were desired.)

def is_valid_parentheses(s: str) -> bool:
    """
    Checks if a string of '()[]{}' is balanced and properly nested.
    Uses a stack to keep track of opening brackets.

    Args:
        s: The input string containing parentheses, brackets, and curly braces.

    Returns:
        True if the string is balanced and properly nested, False otherwise.
    """
    stack: list[str] = []
    
    # Define mappings for opening and closing brackets
    # This dictionary maps closing brackets to their corresponding opening brackets
    matching_bracket: dict[str, str] = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    
    # A set for quick lookup of opening brackets
    opening_brackets: set[str] = {'(', '[', '{'}

    for char in s:
        if char in opening_brackets:
            # If it's an opening bracket, push it onto the stack
            stack.append(char)
        elif char in matching_bracket:
            # If it's a closing bracket
            # Check if the stack is empty. If so, there's no opening bracket
            # to match this closing bracket.
            if not stack:
                return False
            
            # Pop the top element from the stack
            top_element = stack.pop()
            
            # Check if the popped opening bracket matches the current closing bracket
            if matching_bracket[char] != top_element:
                return False
        # If the character is not a bracket, it's ignored or considered invalid
        # For this problem, we assume the string only contains '()[]{}' or similar,
        # but if other characters were allowed, this part would need refinement.
        # For strictness, if any other characters are present and not explicitly allowed,
        # one might return False here:
        # else:
        #    return False

    # After iterating through the entire string, if the stack is empty,
    # all opening brackets have been matched.
    return not stack

# add this at the end of the file
EXPORT_FUNCTION = is_valid_parentheses