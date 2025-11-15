import re
from typing import Optional

def re_dos_vulnerable(regex_pattern: str, text: str) -> Optional[re.Match[str]]:
    """
    Applies a potentially vulnerable regex (e.g., '(a+)+b') to text, good for finding catastrophic backtracking.

    This function performs a regular expression search on the given text using the provided pattern.
    It is specifically designed for testing scenarios where one wants to observe or demonstrate
    catastrophic backtracking (Regex Denial of Service, ReDoS).

    When a vulnerable regex pattern (like `(a+)+b` or `(a|aa)+b`) is applied to a string
    that partially matches but ultimately fails (e.g., 'aaaaaaaaaaaaaaaaaaaaaaaa!'),
    the regex engine might explore an exponentially increasing number of paths,
    leading to extremely long execution times or resource exhaustion.

    Args:
        regex_pattern: The regular expression pattern string. This pattern is expected
                       to be potentially vulnerable to catastrophic backtracking.
                       Example vulnerable patterns: `(a+)+b`, `(a|aa)+b`, `(a*)*b`, `(ab|a)*c`
        text: The input string on which the regex search will be performed.
              To trigger catastrophic backtracking, the text typically needs to match
              the repeating part of the vulnerable pattern many times, but then
              fail to match the final part.
              Example text for `(a+)+b`: `'a' * 30 + '!'`

    Returns:
        A re.Match object if the pattern is found in the text, otherwise None.
        
    WARNING:
        Using this function with actual vulnerable regex patterns and sufficiently
        long input strings can lead to very long execution times, potentially
        freezing the calling process or consuming excessive CPU resources.
        Use with caution and in controlled environments, and consider adding
        a timeout mechanism in your calling code if integrating into a larger system.
    """
    try:
        # Perform the regex search operation.
        # This is the point where catastrophic backtracking would occur if the
        # regex_pattern and text are crafted to trigger it.
        match = re.search(regex_pattern, text)
        return match
    except re.error as e:
        # Catch errors that might arise from invalid regex patterns (e.g., malformed syntax).
        print(f"Error: Invalid regex pattern provided: {e}")
        return None

# add this ad the end of the file
EXPORT_FUNCTION = re_dos_vulnerable