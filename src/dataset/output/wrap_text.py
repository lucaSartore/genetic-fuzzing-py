import textwrap

def wrap_text(text: str, width: int) -> str:
    """
    Wraps text to a specified width using 'textwrap', handling long words and newlines.

    This function utilizes `textwrap.fill` which automatically handles:
    - Breaking long words to fit the specified width.
    - Preserving paragraph breaks indicated by newlines in the input text,
      wrapping each paragraph independently.
    - Indenting subsequent lines within a paragraph (though not explicitly
      requested, `textwrap.fill` handles this naturally for simple wrapping).

    Args:
        text: The input string to be wrapped.
        width: The maximum width for each line of the wrapped text.

    Returns:
        A new string with the text wrapped to the specified width, with
        newlines inserted where wraps occur and paragraphs preserved.
    """
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string.")
    if not isinstance(width, int):
        raise TypeError("Input 'width' must be an integer.")
    if width <= 0:
        raise ValueError("Input 'width' must be a positive integer.")

    # textwrap.fill automatically handles newlines by processing text paragraph by paragraph.
    # It also handles long words by breaking them by default.
    wrapped_text = textwrap.fill(text, width=width)

    return wrapped_text

EXPORT_FUNCTION = wrap_text