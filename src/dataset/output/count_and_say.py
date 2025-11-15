# necessary imports (use only the python standard libraries)
# No specific imports are needed for this function as it uses only built-in types and string operations.

# you can define other auxiliary functions
# No auxiliary functions are required for this implementation.

def count_and_say(n: int) -> str:
    """
    Generates the n-th term of the 'count-and-say' sequence.

    The count-and-say sequence is a sequence of digit strings defined by the
    recursive rule:
    1. The first term is "1".
    2. To generate the next term, read aloud the previous term, then count the
       number of consecutive identical digits and say the digit itself.
       For example:
       - "1" is read as "one 1", which becomes "11".
       - "11" is read as "two 1s", which becomes "21".
       - "21" is read as "one 2, one 1", which becomes "1211".

    Args:
        n: A positive integer representing the term number to generate (n >= 1).

    Returns:
        A string representing the n-th term of the count-and-say sequence.

    Raises:
        ValueError: If n is less than 1.
    """
    if n < 1:
        raise ValueError("n must be a positive integer.")

    # The first term of the sequence is "1".
    current_term = "1"

    # Generate terms from the 2nd up to the n-th term.
    # The loop runs n-1 times.
    for _ in range(1, n):
        # Use a list to build the next term efficiently, then join at the end.
        next_term_builder = []
        i = 0  # Pointer to the current character group's start

        while i < len(current_term):
            count = 1  # Start count for the current digit
            j = i + 1  # Pointer to check subsequent characters

            # Count consecutive occurrences of the digit at current_term[i]
            while j < len(current_term) and current_term[j] == current_term[i]:
                count += 1
                j += 1

            # Append the count and the digit to the builder
            next_term_builder.append(str(count))
            next_term_builder.append(current_term[i])

            # Move the main pointer 'i' to the start of the next distinct digit group
            i = j
        
        # Update current_term for the next iteration
        current_term = "".join(next_term_builder)
        
    return current_term

# add this ad the end of the file
EXPORT_FUNCTION = count_and_say