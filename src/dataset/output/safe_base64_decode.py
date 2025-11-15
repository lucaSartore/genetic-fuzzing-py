# necessary imports (use only the python standard libraries)
import base64
import binascii
from typing import Union

# you can define other auxiliary functions

def safe_base64_decode(encoded_string: str) -> Union[bytes, None]:
    """
    Decodes a base64 string, handling padding errors and invalid characters.

    Attempts to decode a base64 string. If decoding fails due to incorrect
    padding, it attempts to fix the padding by adding '=' characters and retries.
    If decoding still fails (e.g., due to invalid base64 characters or
    other structural issues), it returns None, indicating that the string
    could not be safely decoded.

    Args:
        encoded_string: The base64 string to decode.

    Returns:
        The decoded bytes if the string can be successfully decoded,
        otherwise None if it's an invalid base64 string or has unresolvable
        padding issues.

    Raises:
        TypeError: If the input `encoded_string` is not a string.
    """
    if not isinstance(encoded_string, str):
        raise TypeError("Input 'encoded_string' must be a string.")

    # Attempt to decode the string directly first. This covers cases where
    # the padding is already correct or explicitly included.
    try:
        # Base64 strings are typically ASCII. Attempt to encode to ASCII bytes.
        # This will raise UnicodeEncodeError if the string contains non-ASCII
        # characters, which are invalid for standard base64 encoding.
        return base64.b64decode(encoded_string.encode('ascii'))
    except binascii.Error:
        # If direct decoding fails, it could be due to missing/incorrect padding
        # or invalid base64 characters. We will try to adjust padding next.
        pass
    except UnicodeEncodeError:
        # The input string contains non-ASCII characters, which cannot be
        # part of a standard base64 encoded string. Treat this as an undecodable string.
        return None

    # If the first attempt failed, try adjusting the padding.
    # Base64 encoded strings must have a length that is a multiple of 4.
    # If not, missing '=' padding characters are implied.
    missing_padding = len(encoded_string) % 4
    if missing_padding != 0:
        # Add the necessary number of '=' characters to make the length a multiple of 4.
        padded_encoded_string = encoded_string + '=' * (4 - missing_padding)
    else:
        # If the length is already a multiple of 4, no padding adjustment is needed
        # (or implies correctly padded, or already invalid for other reasons).
        padded_encoded_string = encoded_string

    try:
        # Try decoding with the (potentially) adjusted padding.
        return base64.b64decode(padded_encoded_string.encode('ascii'))
    except binascii.Error:
        # If decoding still fails after padding adjustment, it means the string
        # contains invalid base64 characters or has other structural issues
        # that prevent it from being a valid base64 encoding.
        return None
    except UnicodeEncodeError:
        # This case should ideally be caught by the first try-except block,
        # as adding '=' characters won't introduce non-ASCII issues if the original
        # string was already checked. Included for robustness.
        return None

# add this ad the end of the file
EXPORT_FUNCTION = safe_base64_decode