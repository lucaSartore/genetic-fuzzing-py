import re

def reverse_words(text: str) -> str:
    """
    Reverses the order of words in a string, handling whitespace.

    This function preserves the original leading, trailing, and
    inter-word whitespace structure. For example, "  hello   world  "
    becomes "  world   hello  ".

    Args:
        text (str): The input string containing words and whitespace.

    Returns:
        str: A new string with the order of words reversed,
             while preserving the original whitespace structure.

    Examples:
        >>> reverse_words("hello world")
        'world hello'
        >>> reverse_words("  Python   is    fun!  ")
        '  fun!   is    Python  '
        >>> reverse_words("singleword")
        'singleword'
        >>> reverse_words("   ")
        '   '
        >>> reverse_words("")
        ''
    """
    if not text:
        return ""

    # Split the string by one or more whitespace characters,
    # but keep the delimiters in the result list.
    # The result list will alternate between 'words' (or empty strings for leading/trailing)
    # and whitespace delimiters.
    # Example: "  hello   world  " -> ['', '  ', 'hello', '   ', 'world', '  ', '']
    original_parts = re.split(r'(\s+)', text)

    # Extract only the actual words (non-empty strings at even indices)
    words_only = [part for i, part in enumerate(original_parts) if i % 2 == 0 and part]

    # Reverse the order of these extracted words
    reversed_words = words_only[::-1]

    # Reconstruct the string using the reversed words and original whitespace
    result_parts = []
    word_idx = 0
    for i, part in enumerate(original_parts):
        if i % 2 == 0:
            # This is a 'word slot'.
            # If the original part was a non-empty word, place the next reversed word.
            if part:
                result_parts.append(reversed_words[word_idx])
                word_idx += 1
            # If it was an empty string (due to leading/trailing whitespace), keep it empty.
            else:
                result_parts.append('')
        else:
            # This is a whitespace delimiter, keep it as is.
            result_parts.append(part)

    return "".join(result_parts)

# add this ad the end of the file
EXPORT_FUNCTION = reverse_words