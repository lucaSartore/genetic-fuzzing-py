import re
from typing import List, Tuple

def find_all_markdown_links(markdown_text: str) -> List[Tuple[str, str]]:
    """
    Uses 're.findall' to extract '(text, url)' tuples from markdown links '[text](url)'.

    Args:
        markdown_text: A string potentially containing markdown links.

    Returns:
        A list of (text, url) tuples found in the markdown text.
        Returns an empty list if no links are found.
    """
    # The regular expression pattern to find markdown links:
    # \[          - Matches the literal opening square bracket
    # (.*?)       - Captures any character (except newline) non-greedily for the link text
    # \]          - Matches the literal closing square bracket
    # \(          - Matches the literal opening parenthesis
    # (.*?)       - Captures any character (except newline) non-greedily for the URL
    # \)          - Matches the literal closing parenthesis
    pattern = r'\[(.*?)\]\((.*?)\)'

    # Use re.findall to find all non-overlapping matches of the pattern.
    # Since there are two capturing groups, re.findall will return a list of tuples,
    # where each tuple contains the captured text and URL.
    return re.findall(pattern, markdown_text)

# add this ad the end of the file
EXPORT_FUNCTION = find_all_markdown_links