# necessary imports (use only the python standard libraries)
# No special imports beyond built-in types and string methods are needed.

def tokenize_with_context(text: str) -> list[str]:
    """
    Tokenizes text with context-aware rules including nested delimiters,
    escape sequences, and quote handling.

    Args:
        text: The input string to be tokenized.

    Returns:
        A list of strings, where each string is a token.
    """
    tokens: list[str] = []
    current_token: list[str] = []  # Use a list for efficient character appending
    
    # States: NORMAL, IN_SINGLE_QUOTE, IN_DOUBLE_QUOTE, ESCAPING
    # ESCAPING is a transient state, indicating the *next* character is escaped.
    # We need to remember the state *before* ESCAPING to restore it.
    state: str = 'NORMAL'
    state_before_escape: str = 'NORMAL' # Stores the state before entering 'ESCAPING'

    # Delimiter handling configuration
    OPEN_DELIMITERS: str = '([{'
    CLOSE_DELIMITERS: str = ')]}'
    DELIMITER_PAIRS: dict[str, str] = {'(': ')', '[': ']', '{': '}'}
    delimiter_stack: list[str] = []

    def _flush_current_token():
        """Helper function to append current_token to tokens list if not empty."""
        if current_token:
            tokens.append("".join(current_token))
            current_token.clear()

    i = 0
    while i < len(text):
        char = text[i]

        # Handle ESCAPING state (the character *after* a backslash)
        if state == 'ESCAPING':
            # If the text ends with a backslash, treat the backslash itself as literal.
            if i >= len(text):
                current_token.append('\\')
            else:
                # Append the escaped character literally
                current_token.append(char)
            
            # Restore the state that was active before the escape
            state = state_before_escape
            state_before_escape = 'NORMAL' # Reset for future escapes
            i += 1
            continue # Move to the next character after processing the escaped one

        # Handle characters when inside a single-quoted string
        if state == 'IN_SINGLE_QUOTE':
            if char == '\\':
                state_before_escape = 'IN_SINGLE_QUOTE'
                state = 'ESCAPING'
            elif char == '\'':
                current_token.append(char) # Include the closing quote in the token
                _flush_current_token()
                state = 'NORMAL'
            else:
                current_token.append(char)
            i += 1
            continue

        # Handle characters when inside a double-quoted string
        if state == 'IN_DOUBLE_QUOTE':
            if char == '\\':
                state_before_escape = 'IN_DOUBLE_QUOTE'
                state = 'ESCAPING'
            elif char == '"':
                current_token.append(char) # Include the closing quote in the token
                _flush_current_token()
                state = 'NORMAL'
            else:
                current_token.append(char)
            i += 1
            continue

        # Handle characters when in NORMAL state (outside of quotes)
        if char.isspace():
            _flush_current_token() # Whitespace separates tokens
        elif char == '\\':
            # A backslash in NORMAL state initiates an escape sequence for the next character.
            state_before_escape = 'NORMAL'
            state = 'ESCAPING'
        elif char == '\'':
            _flush_current_token() # Flush any accumulated token before starting a new string
            current_token.append(char) # Include the opening quote in the token
            state = 'IN_SINGLE_QUOTE'
        elif char == '"':
            _flush_current_token() # Flush any accumulated token before starting a new string
            current_token.append(char) # Include the opening quote in the token
            state = 'IN_DOUBLE_QUOTE'
        elif char in OPEN_DELIMITERS:
            _flush_current_token() # Delimiters are separate tokens, so flush current_token
            tokens.append(char)
            delimiter_stack.append(char)
        elif char in CLOSE_DELIMITERS:
            _flush_current_token() # Delimiters are separate tokens, so flush current_token
            if delimiter_stack and DELIMITER_PAIRS.get(delimiter_stack[-1]) == char:
                delimiter_stack.pop() # Matched closing delimiter
            # If not matched, it's still treated as a token, but doesn't pop the stack.
            tokens.append(char)
        else:
            current_token.append(char) # Accumulate regular characters into current_token
        
        i += 1

    # After the loop, flush any remaining characters in current_token
    _flush_current_token()

    # Optional: If you need to handle unclosed delimiters as an error or special token.
    # For this tokenizer, they are implicitly handled as the tokens are generated.
    # For example, in "(foo", '(' and "foo" would be tokens, and the stack would remain non-empty.

    return tokens

# add this at the end of the file
EXPORT_FUNCTION = tokenize_with_context