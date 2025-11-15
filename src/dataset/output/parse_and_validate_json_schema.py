import json
from typing import Any, Dict, List, Tuple, Union, Type

# Auxiliary function for validating against a specific Python type
def _validate_type(data: Any, expected_type: Type, path: str = "") -> Tuple[bool, str]:
    """
    Validates if the given data is an instance of the expected Python type.

    Args:
        data: The value to validate.
        expected_type: The expected Python type (e.g., str, int, bool, float).
        path: A string representing the current path in the JSON structure for error reporting.

    Returns:
        A tuple: (True, "") on success, or (False, error_message) on failure.
    """
    if not isinstance(data, expected_type):
        return False, f"Type mismatch at '{path}'. Expected {expected_type.__name__}, got {type(data).__name__}."
    return True, ""

# Auxiliary function for validating a dictionary structure
def _validate_dict_structure(data: Any, schema_dict: Dict[str, Any], path: str = "") -> Tuple[bool, str]:
    """
    Recursively validates a dictionary's structure and types against a schema dictionary.

    Args:
        data: The dictionary to validate.
        schema_dict: The schema dictionary defining expected keys and their structures/types.
        path: A string representing the current path in the JSON structure for error reporting.

    Returns:
        A tuple: (True, "") on success, or (False, error_message) on failure.
    """
    if not isinstance(data, dict):
        return False, f"Structure mismatch at '{path}'. Expected a dictionary, got {type(data).__name__}."

    for key, expected_schema in schema_dict.items():
        current_path = f"{path}.{key}" if path else key
        
        # Check for missing required keys
        if key not in data:
            return False, f"Missing required key '{key}' at '{path}'."

        value = data[key]
        is_valid, error_msg = _validate_data(value, expected_schema, current_path)
        if not is_valid:
            return False, error_msg
    return True, ""

# Auxiliary function for validating a list structure
def _validate_list_structure(data: Any, schema_list: List[Any], path: str = "") -> Tuple[bool, str]:
    """
    Recursively validates a list's elements against its element schema.

    The `schema_list` is expected to contain exactly one element, which defines the
    schema for each item within the list. E.g., `[str]` or `[{'id': int}]`.

    Args:
        data: The list to validate.
        schema_list: A list containing the schema for its elements (must have 1 element).
        path: A string representing the current path in the JSON structure for error reporting.

    Returns:
        A tuple: (True, "") on success, or (False, error_message) on failure.
    """
    if not isinstance(data, list):
        return False, f"Structure mismatch at '{path}'. Expected a list, got {type(data).__name__}."

    # Validate the schema definition for lists itself
    if not schema_list or len(schema_list) != 1:
        return False, f"Malformed schema: List schema at '{path}' must contain exactly one element defining the element's structure/type (e.g., `[str]` or `[{'id': int}]`)."
    
    element_schema = schema_list[0]

    for i, item in enumerate(data):
        current_path = f"{path}[{i}]"
        is_valid, error_msg = _validate_data(item, element_schema, current_path)
        if not is_valid:
            return False, error_msg
    return True, ""

# The main recursive validation dispatcher function
def _validate_data(data: Any, schema_element: Any, path: str = "") -> Tuple[bool, str]:
    """
    Dispatches validation based on the type of `schema_element`.
    `schema_element` can be a Python type (for primitives), a dict (for nested objects),
    or a list (for arrays, where `schema_element[0]` defines the item schema).

    Args:
        data: The data (value) to validate.
        schema_element: The schema definition for the current `data` element.
        path: A string representing the current path in the JSON structure for error reporting.

    Returns:
        A tuple: (True, "") on success, or (False, error_message) on failure.
    """
    if isinstance(schema_element, Type):  # e.g., str, int, bool, float
        return _validate_type(data, schema_element, path)
    elif isinstance(schema_element, dict):  # e.g., {'key': str}
        return _validate_dict_structure(data, schema_element, path)
    elif isinstance(schema_element, list):  # e.g., [str] or [{'id': int}]
        return _validate_list_structure(data, schema_element, path)
    else:
        # This case indicates a malformed schema definition
        return False, f"Malformed schema: Unknown schema element type '{type(schema_element).__name__}' encountered at '{path}'. Schema element was: {schema_element}"


def parse_and_validate_json_schema(json_string: str, schema: Dict[str, Any]) -> Tuple[bool, Union[Dict[str, Any], str]]:
    """
    Parses a JSON string and validates its structure against a simple schema (dict).

    The schema dictates the expected structure and types of the JSON data.
    It should be a dictionary where:
    - Keys are strings representing expected keys in the JSON object.
    - Values can be:
        - A Python type (e.g., `str`, `int`, `float`, `bool`) for primitive values.
        - Another dictionary (for nested JSON objects), recursively defining its schema.
        - A list containing a single element, which defines the schema for the elements
          within an expected JSON array. For example:
          - `[str]` means "a list where all elements must be strings".
          - `[{'id': int, 'name': str}]` means "a list of dictionaries, each with an
            'id' (int) and 'name' (str)".

    Args:
        json_string: The JSON string to parse and validate.
        schema: A dictionary defining the expected structure and types for the JSON data.
                The top-level JSON data is expected to be a dictionary, matching this schema.

    Returns:
        A tuple:
        - (True, parsed_data) if the JSON string is valid and matches the schema.
        - (False, error_message) if parsing fails or the structure/types do not match the schema.
    """
    try:
        parsed_data = json.loads(json_string)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON string: {e}"
    
    # The top-level schema is a dictionary, so we initiate validation with _validate_dict_structure.
    # This also implicitly checks if `parsed_data` itself is a dictionary.
    is_valid, error_msg = _validate_dict_structure(parsed_data, schema, path="")

    if is_valid:
        return True, parsed_data
    else:
        return False, error_msg

# add this ad the end of the file
EXPORT_FUNCTION = parse_and_validate_json_schema