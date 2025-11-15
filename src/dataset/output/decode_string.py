# necessary imports (use only the python standard libraries)
# No special imports are needed beyond basic types like list for the stack.

def decode_string(s: str) -> str:
    """
    Decodes a string encoded like '3[a]2[bc]' into 'aaabcbc'.
    The decoding uses a stack-based approach to handle nested repetitions.

    Args:
        s: The encoded string. E.g., "3[a]2[bc]", "2[abc]", "3[a2[c]]".

    Returns:
        The decoded string. E.g., "aaabcbc", "abcabc", "accaccacc".
    """
    current_string = ""  # Stores the string segment being built for the current level
    current_num = 0      # Stores the repetition count for the next bracketed segment
    
    # The stack will store tuples of (string_built_so_far, repetition_count_for_next_block).
    # This captures the state of the outer scope before descending into a nested bracket.
    stack = []

    for char in s:
        if char.isdigit():
            # Build the number (can be multi-digit)
            current_num = current_num * 10 + int(char)
        elif char == '[':
            # When an opening bracket is encountered, it means we are starting a new
            # nested segment. We push the current progress onto the stack:
            # 1. The `current_string` that has been accumulated *before* this bracket.
            # 2. The `current_num` which is the repetition count for the *content*
            #    inside this new bracket.
            stack.append((current_string, current_num))
            
            # Reset `current_string` and `current_num` to start fresh for the
            # content inside the new bracket.
            current_string = ""
            current_num = 0
        elif char == ']':
            # When a closing bracket is encountered, we have finished decoding
            # the content of the current nested segment (`current_string`).
            # We pop the state of the parent scope from the stack.
            prev_string, num_repeats = stack.pop()
            
            # Append the decoded `current_string` (repeated `num_repeats` times)
            # to the `prev_string` from the parent scope. This result becomes
            # the new `current_string` for the parent scope.
            current_string = prev_string + (current_string * num_repeats)
        else: # It's a letter (or any non-digit, non-bracket character)
            # Append the character to the current string segment.
            current_string += char
    
    # After iterating through the entire string, `current_string` will hold
    # the fully decoded result.
    return current_string

# add this ad the end of the file
EXPORT_FUNCTION = decode_string