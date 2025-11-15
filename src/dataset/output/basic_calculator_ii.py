# necessary imports (use only the python standard libraries)
# No special imports are needed for this solution as list operations are built-in.

# you can define other auxiliary functions
# No auxiliary functions are strictly necessary for this problem's solution using the described stack-based approach.

def basic_calculator_ii(s: str) -> int:
    """
    Evaluates a string expression with '+', '-', '*', '/' and no parentheses.
    Uses a single-pass, stack-based approach to handle operator precedence.
    Multiplication and division operations are performed immediately due to higher precedence.
    Addition and subtraction are deferred and processed by summing the final stack elements.
    Integer division truncates towards zero (e.g., 3/2 = 1, -3/2 = -1).

    Args:
        s (str): The input string expression containing digits, '+', '-', '*', '/', and spaces.
                 Assumes valid expressions with non-negative numbers being operands,
                 or unary minus at the start being implicitly handled as '0 - number'.

    Returns:
        int: The integer result of the expression evaluation.
    """
    if not s:
        return 0

    stack: list[int] = []
    current_number: int = 0
    # Initialize with a '+' operator. This effectively treats the expression as if it starts
    # with a '0 +' prefix, ensuring the first number is correctly pushed onto the stack
    # (e.g., "3+2" is treated as "0+3+2"). This also correctly handles expressions
    # that might implicitly start with a unary minus like "-3+2" as "0-3+2", evaluating to -1.
    operator: str = '+' 

    # Iterate through the string, including an implicit "end-of-string" check at `i == len(s) - 1`.
    # This ensures that the last number and its preceding operation are processed.
    for i in range(len(s)):
        char = s[i]

        # If the character is a digit, build the current number
        if '0' <= char <= '9':
            current_number = current_number * 10 + int(char)
        
        # If the character is an operator OR it's the last character of the string:
        # This condition triggers the processing of the `current_number` using the `operator`.
        # Spaces are effectively ignored because they are neither digits nor operators,
        # and they do not trigger this processing logic.
        if (char in "+-*/" or i == len(s) - 1):
            if operator == '+':
                stack.append(current_number)
            elif operator == '-':
                stack.append(-current_number)
            elif operator == '*':
                # Pop the last number from the stack, perform multiplication, and push the result back.
                prev_num = stack.pop()
                stack.append(prev_num * current_number)
            elif operator == '/':
                # Pop the last number, perform division, and push the result back.
                # We use int(prev_num / current_number) to achieve integer division
                # that truncates towards zero (e.g., int(-3 / 2) == -1, not -2 like Python's //).
                prev_num = stack.pop()
                stack.append(int(prev_num / current_number))
            
            # After processing the `current_number` with its `operator`:
            # Update the `operator` to the new character (if it's an actual operator)
            # and reset `current_number` for parsing the next operand.
            if char in "+-*/":
                operator = char
            current_number = 0
            
    # After iterating through the entire string, the stack will contain numbers that
    # represent the results of multiplications/divisions, and numbers for additions/subtractions.
    # Summing all elements in the stack gives the final result.
    return sum(stack)

# add this ad the end of the file
EXPORT_FUNCTION = basic_calculator_ii