# necessary imports (use only the python standard libraries)
import re

# you can define other auxiliary functions

def split_by_multiple_delimiters(text: str, delimiters: list[str]) -> list[str]:
    """
    Splits a string by a list of delimiters using 're.split'.

    This function constructs a regular expression pattern by joining the
    provided delimiters with the regex OR operator '|'. Each delimiter
    is escaped using re.escape() to ensure that special regex characters
    within the delimiters are treated literally.

    Args:
        text: The input string to be split.
        delimiters: A list of strings, where each string is a delimiter
                    by which the text should be split.

    Returns:
        A list of strings, which are the parts of the original string
        separated by any of the specified delimiters.
        Empty strings resulting from consecutive delimiters or delimiters
        at the start/end of the string are typically included by re.split.

    Examples:
        >>> split_by_multiple_delimiters("apple,banana;orange.grape", [",", ";", "."])
        ['apple', 'banana', 'orange', 'grape']
        >>> split_by_multiple_delimiters("one two;three,four", [" ", ",", ";"])
        ['one', '', 'two', 'three', 'four']
        >>> split_by_multiple_delimiters("path/to\\file.txt", ["/", "\\", "."])
        ['path', 'to', 'file', 'txt']
        >>> split_by_multiple_delimiters("data--item___value", ["--", "___"])
        ['data', 'item', 'value']
    """
    if not delimiters:
        return [text] # If no delimiters, return the original string as a single item list

    # Escape each delimiter to treat them literally in the regex pattern
    escaped_delimiters = [re.escape(d) for d in delimiters]

    # Join the escaped delimiters with '|' to create the regex pattern
    # e.g., if delimiters are [",", ";"], pattern becomes "[,]|[;]" or simpler "[;,]"
    # With re.escape, it's more like "\,|\;"
    pattern = '|'.join(escaped_delimiters)

    # Use re.split to split the text by the generated pattern
    return re.split(pattern, text)

# add this ad the end of the file
EXPORT_FUNCTION = split_by_multiple_delimiters