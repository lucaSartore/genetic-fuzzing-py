# necessary imports (use only the python standard libraries)
# No special imports are required beyond built-in types for this implementation.

# you can define other auxiliary functions

def parse_simple_ini(ini_string: str) -> dict[str, dict[str, str]]:
    """
    Parses a simple .ini format string into a dictionary of dictionaries.

    The parser handles:
    - Sections defined by `[section_name]`.
    - Key-value pairs in the format `key = value`.
    - Whitespace trimming around section names, keys, and values.
    - Lines starting with '#' or ';' are treated as comments and ignored.
    - Empty lines are ignored.
    - Keys appearing before any explicit section header are placed into a
      default section named "DEFAULT".
    - If a key is duplicated within a section, the last value encountered wins.
    - If a section is duplicated, its entries are merged, with later keys
      for the same name overriding earlier ones within that section.

    Args:
        ini_string: A string containing the INI formatted content.

    Returns:
        A dictionary where top-level keys are section names (strings) and
        their values are dictionaries containing key-value pairs (both strings).
        An empty or only-comment INI string will result in `{"DEFAULT": {}}`.

    Raises:
        ValueError: If an empty section name is encountered (e.g., `[]` or `[ ]`).
        ValueError: If an empty key is encountered within a section (e.g., `=value`).
    """
    result: dict[str, dict[str, str]] = {}
    current_section = "DEFAULT"
    # Initialize the "DEFAULT" section, where keys defined before any explicit
    # section header or in an empty INI string will reside.
    result[current_section] = {}

    lines = ini_string.splitlines()

    for line in lines:
        line = line.strip()

        # Ignore empty lines and lines starting with comment characters
        if not line or line.startswith('#') or line.startswith(';'):
            continue

        # Check for section header: [section_name]
        if line.startswith('[') and line.endswith(']'):
            section_name = line[1:-1].strip()
            if not section_name:
                # Disallow empty section names like "[]" or "[ ]" for clarity
                raise ValueError("Empty section name found in INI string.")
            current_section = section_name
            # If the section doesn't exist yet, initialize it.
            # If it already exists (duplicate section), we continue to merge into it.
            if current_section not in result:
                result[current_section] = {}
            continue

        # Otherwise, the line is expected to be a key-value pair
        if '=' in line:
            # Split only on the first '=' to allow '=' characters within the value
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if not key:
                # Disallow empty keys for robustness
                raise ValueError(f"Empty key found in section '{current_section}' for line: '{line}'")
            result[current_section][key] = value
        else:
            # If a line is not a section, not a comment, not empty, and not a key-value pair,
            # this simple parser will ignore it. A more strict parser might raise an error.
            pass

    return result

# add this ad the end of the file
EXPORT_FUNCTION = parse_simple_ini