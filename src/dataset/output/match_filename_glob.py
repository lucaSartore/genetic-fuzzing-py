# necessary imports (use only the python standard libraries)
import fnmatch

# you can define other auxiliary functions

def match_filename_glob(filename: str, glob_pattern: str) -> bool:
    """
    Uses 'fnmatch.fnmatch' to check if a filename matches a glob pattern.

    Args:
        filename (str): The name of the file to check.
        glob_pattern (str): The glob-style pattern (e.g., '*.txt', 'doc?', 'report[0-9].pdf').

    Returns:
        bool: True if the filename matches the glob pattern, False otherwise.
    """
    return fnmatch.fnmatch(filename, glob_pattern)

# add this ad the end of the file
EXPORT_FUNCTION = match_filename_glob