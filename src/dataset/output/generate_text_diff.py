# necessary imports (use only the python standard libraries)
import difflib

# you can define other auxiliary functions

def generate_text_diff(text1: str, text2: str, fromfile: str = 'string1', tofile: str = 'string2') -> str:
    """
    Generates a unified diff between two strings using 'difflib'.

    Args:
        text1: The first string to compare.
        text2: The second string to compare.
        fromfile: Optional label for the first string, used in the diff header.
                  Defaults to 'string1'.
        tofile: Optional label for the second string, used in the diff header.
                Defaults to 'string2'.

    Returns:
        A string representing the unified diff. Each line in the diff will
        end with a newline character, including the header lines.
    """
    # Split the input strings into lists of lines.
    # keepends=True ensures that newlines are part of the lines, which difflib
    # handles correctly when generating the diff output.
    lines1 = text1.splitlines(keepends=True)
    lines2 = text2.splitlines(keepends=True)

    # Generate the unified diff.
    # The result is an iterator yielding diff lines.
    diff_generator = difflib.unified_diff(
        lines1,
        lines2,
        fromfile=fromfile,
        tofile=tofile
    )

    # Join the diff lines into a single string.
    # Each line returned by unified_diff already contains its newline character.
    return ''.join(diff_generator)

# add this ad the end of the file
EXPORT_FUNCTION = generate_text_diff