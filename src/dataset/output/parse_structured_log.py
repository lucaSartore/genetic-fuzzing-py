import json
import re
import logging
from typing import Optional, Dict, List, Literal, Union, Any

# Auxiliary functions to handle specific parsing formats

def _parse_json_internal(text: str) -> Optional[Dict[str, Any]]:
    """Tries to parse a string as a JSON object.
    
    If the JSON is not an object (e.g., array, string, number), it wraps the 
    value in a dictionary with a special key '_value'.
    """
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
        # If JSON is not a dictionary (e.g., list, string, number),
        # wrap it in a dictionary as the main function expects a dictionary return.
        return {'_value': parsed}
    except json.JSONDecodeError:
        return None

def _parse_key_value_internal(text: str, kv_delimiters: tuple[str, ...]) -> Optional[Dict[str, str]]:
    """Tries to parse a string as key-value pairs.
    
    It splits the string into tokens, handling quoted strings correctly,
    then attempts to parse each token as a key-value pair.
    """
    parsed_data = {}
    
    # This regex splits the string into tokens by space, but not within double quotes.
    # E.g., 'user=john id="123 abc" status=active' -> ['user=john', 'id="123 abc"', 'status=active']
    parts = re.findall(r'"[^"]*"|\S+', text)

    for part in parts:
        if not part:
            continue
        found = False
        for kv_delim in kv_delimiters:
            if kv_delim in part:
                key, value = part.split(kv_delim, 1)
                key = key.strip()
                value = value.strip()
                # Remove surrounding quotes from the value if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                parsed_data[key] = value
                found = True
                break
        # If a part isn't a key-value pair, it's ignored for this parser
    
    return parsed_data if parsed_data else None # Return None if no key-value pairs were successfully parsed

def _parse_delimited_internal(text: str, delimiter: str, field_names: Optional[list[str]]) -> Optional[Dict[str, str]]:
    """
    Tries to parse a string as delimited values.
    
    If `field_names` are provided, they are used as keys for the dictionary.
    Otherwise, fields will be mapped to numeric string keys (e.g., '0', '1', '2').
    """
    if not text.strip(): # Consider empty or whitespace-only strings as unparseable
        return None

    values = [part.strip() for part in text.split(delimiter)]

    if field_names:
        if len(field_names) != len(values):
            # Mismatch in number of field names and values is considered a parsing failure
            return None
        return dict(zip(field_names, values))
    else:
        # If no explicit field names are provided, use numeric keys for consistency
        return {str(i): value for i, value in enumerate(values)}

def parse_structured_log(
    log_entry: str,
    *, # Enforce keyword-only arguments for clarity and extensibility
    format_hint: Optional[Literal['json', 'kv', 'delimited']] = None,
    delimiter: str = ',',
    kv_delimiters: tuple[str, ...] = ('=', ':'),
    field_names_for_delimited: Optional[list[str]] = None,
    field_extraction_rules: Optional[Dict[str, str]] = None,
    error_handling_mode: Literal['raise', 'ignore', 'log', 'return_empty'] = 'return_empty',
    logger: Optional[logging.Logger] = None
) -> Dict[str, Any]:
    """
    Parses multi-format log entries (JSON/key-value/delimited) with field extraction rules and error handling modes.

    Args:
        log_entry: The raw log string to parse.
        format_hint: An optional hint for the log format ('json', 'kv', 'delimited').
                     If None, the function attempts to auto-detect the format by trying JSON,
                     then key-value, then delimited.
        delimiter: The delimiter character(s) used for 'delimited' format. Defaults to ','.
        kv_delimiters: A tuple of strings representing potential key-value delimiters.
                       Defaults to ('=', ':').
        field_names_for_delimited: An optional list of field names to use when parsing
                                   'delimited' log entries. The order must match the log entry's fields.
                                   If not provided for 'delimited' format, fields will be mapped to
                                   numeric string keys (e.g., '0', '1').
        field_extraction_rules: An optional dictionary mapping original field names to desired
                                new field names. Only fields present in this dictionary will be
                                included in the final output, and they will be renamed.
        error_handling_mode: Specifies how parsing errors are handled:
                             - 'raise': Re-raises a ValueError containing details about the parsing failure.
                             - 'ignore': Returns an empty dictionary ({}) on any parsing error.
                             - 'log': Logs the error details and returns an empty dictionary ({}).
                             - 'return_empty': (Default) Returns an empty dictionary ({}) on error.
        logger: An optional `logging.Logger` instance to use when `error_handling_mode` is 'log'.
                If None, a basic logger is created for this purpose.

    Returns:
        A dictionary representing the parsed log entry. If parsing fails (and not 'raise' mode),
        an empty dictionary is returned. The values in the dictionary can be of any type
        as determined by the parsing process (e.g., from JSON).
    """
    _logger = logger
    if error_handling_mode == 'log' and _logger is None:
        _logger = logging.getLogger(__name__)
        # Ensure a handler is present to prevent "No handlers could be found for logger" messages
        if not _logger.handlers:
            _logger.addHandler(logging.NullHandler())

    parsed_data: Optional[Dict[str, Any]] = None
    all_parse_errors: List[str] = []

    # Helper function to centralize error handling during individual parsing attempts
    def _attempt_parse(parser_func: Any, *args: Any) -> Optional[Dict[str, Any]]:
        nonlocal all_parse_errors
        try:
            result = parser_func(*args)
            if result is not None:
                if isinstance(result, dict):
                    return result
                else:
                    # This case should ideally not happen if internal parsers are correctly implemented
                    all_parse_errors.append(f"Parser {parser_func.__name__} returned non-dictionary type.")
                    return None
            return None # Parser returned None, indicating it couldn't parse successfully
        except Exception as e:
            all_parse_errors.append(f"Failed with {parser_func.__name__}: {type(e).__name__} - {e}")
            return None

    # Define the order of parsing attempts based on hint or auto-detection
    parser_attempts = []
    if format_hint == 'json':
        parser_attempts.append((_parse_json_internal, (log_entry,)))
    elif format_hint == 'kv':
        parser_attempts.append((_parse_key_value_internal, (log_entry, kv_delimiters)))
    elif format_hint == 'delimited':
        parser_attempts.append((_parse_delimited_internal, (log_entry, delimiter, field_names_for_delimited)))
    else: # Auto-detection order: try JSON first, then Key-Value, then Delimited
        parser_attempts.append((_parse_json_internal, (log_entry,)))
        parser_attempts.append((_parse_key_value_internal, (log_entry, kv_delimiters)))
        # For delimited in autodetection, `field_names_for_delimited` is crucial for meaningful output.
        # If not provided, it will map to numeric keys.
        parser_attempts.append((_parse_delimited_internal, (log_entry, delimiter, field_names_for_delimited)))

    # Iterate through parsing attempts until one succeeds
    for parser_func, func_args in parser_attempts:
        parsed_data = _attempt_parse(parser_func, *func_args)
        if parsed_data is not None:
            break # Successfully parsed

    # --- Handle overall parsing failure based on error_handling_mode ---
    if parsed_data is None:
        error_message = (
            f"Could not parse log entry: '{log_entry}'. "
            f"Attempted formats (in order): {', '.join([f.__name__.replace('_internal', '') for f, _ in parser_attempts])}. "
            f"Detailed errors: {'; '.join(all_parse_errors)}"
        )
        if error_handling_mode == 'raise':
            raise ValueError(error_message)
        elif error_handling_mode == 'log':
            if _logger:
                _logger.error(error_message)
            return {}
        elif error_handling_mode in ('ignore', 'return_empty'):
            return {}
        else:
            # This case should be prevented by Literal type checking but serves as a defensive fallback
            raise ValueError(f"Invalid error_handling_mode specified: {error_handling_mode}")

    # --- Apply field extraction rules if provided ---
    if field_extraction_rules:
        extracted_data: Dict[str, Any] = {}
        for original_key, new_key in field_extraction_rules.items():
            if original_key in parsed_data:
                extracted_data[new_key] = parsed_data[original_key]
        return extracted_data
    else:
        # If no extraction rules, return the fully parsed data
        return parsed_data

# add this ad the end of the file
EXPORT_FUNCTION = parse_structured_log