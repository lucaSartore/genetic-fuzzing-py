# necessary imports (use only the python standard libraries)
from typing import List, Dict

def find_duplicate_files(file_strings: List[str]) -> List[List[str]]:
    """
    Parses a list of strings like 'root/a 1.txt(content)' and finds groups
    of duplicate file content.

    Each input string is expected to be in the format 'path/filename.ext(content)'.
    The function extracts the full file path and its content. It then groups
    together all file paths that share identical content.

    Args:
        file_strings: A list of strings, where each string represents a file
                      with its path and content. E.g., ['root/a 1.txt(hello)',
                      'root/b 2.txt(world)', 'root/c 3.txt(hello)'].

    Returns:
        A list of lists of strings. Each inner list contains the full paths
        of files that have duplicate content. Files with unique content are
        not included in the output. The order of inner lists and paths within
        them may not be guaranteed.

    Example:
        >>> find_duplicate_files(['root/a 1.txt(content1)', 'root/b 2.txt(content2)', 'root/c 3.txt(content1)'])
        [['root/a 1.txt', 'root/c 3.txt']]
    """
    content_to_paths: Dict[str, List[str]] = {}

    for file_string in file_strings:
        # Find the last occurrence of '(' to separate path from content
        last_paren_idx = file_string.rfind('(')

        # Basic validation: ensure the string has the expected format
        if last_paren_idx == -1 or not file_string.endswith(')'):
            # If the format is invalid, we can choose to skip it,
            # raise an error, or log a warning. For this problem,
            # we'll assume valid format and skip malformed ones to be robust.
            # print(f"Warning: Malformed file string skipped: {file_string}")
            continue

        # Extract the full path (e.g., 'root/a 1.txt')
        full_path = file_string[:last_paren_idx]

        # Extract the content (e.g., 'content')
        # The +1 skips the '(', and the -1 removes the trailing ')'
        content = file_string[last_paren_idx + 1:-1]

        # Add the path to the list associated with its content
        if content in content_to_paths:
            content_to_paths[content].append(full_path)
        else:
            content_to_paths[content] = [full_path]

    # Collect all groups that have more than one file (i.e., duplicates)
    duplicate_groups: List[List[str]] = []
    for paths in content_to_paths.values():
        if len(paths) > 1:
            duplicate_groups.append(paths)

    return duplicate_groups

# add this ad the end of the file
EXPORT_FUNCTION = find_duplicate_files