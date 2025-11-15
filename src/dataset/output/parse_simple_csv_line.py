# necessary imports (use only the python standard libraries)
# No specific imports are needed for this function, as it uses only built-in types and operations.

def parse_simple_csv_line(line: str) -> list[str]:
    """
    Parses a single CSV line, handling quoted fields and commas inside quotes.
    Simulates basic behavior of Python's 'csv' module for a single line,
    including handling of escaped double quotes within quoted fields.

    Args:
        line: The single CSV line string to parse.

    Returns:
        A list of strings, where each string is a field from the CSV line.
    """
    fields: list[str] = []
    current_field_chars: list[str] = []
    in_quote: bool = False
    i: int = 0
    n: int = len(line)

    while i < n:
        char = line[i]

        if in_quote:
            if char == '"':
                # Check for an escaped double quote ("")
                if i + 1 < n and line[i+1] == '"':
                    current_field_chars.append('"')
                    i += 1  # Skip the second quote character
                else:
                    # This is a closing quote for the field
                    in_quote = False
            else:
                # Any character inside quotes is part of the current field
                current_field_chars.append(char)
        else:
            # Not currently in a quoted field
            if char == ',':
                # Comma is a delimiter, so save the current field and reset
                fields.append("".join(current_field_chars))
                current_field_chars = []
            elif char == '"':
                # This character might start a quoted field.
                # According to CSV standards, a quote should only start a field
                # if it's the very first character of that field's content.
                # If current_field_chars is not empty, it means we're in an unquoted
                # field, and encountering a '"' character is usually treated literally
                # or as an error in strict CSV. For this "simple" simulation,
                # we'll start a quote only if the field is currently empty.
                if not current_field_chars:
                    in_quote = True
                else:
                    # If the field is not empty, treat the quote as a literal character
                    # within an unquoted field (non-standard but robust for simpler cases).
                    current_field_chars.append(char)
            else:
                # Any other character outside quotes is part of the current field
                current_field_chars.append(char)
        
        i += 1

    # After the loop, add the last accumulated field to the list
    fields.append("".join(current_field_chars))

    return fields

# add this ad the end of the file
EXPORT_FUNCTION = parse_simple_csv_line