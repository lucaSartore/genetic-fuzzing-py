import json
from typing import Any, List, Union

def find_nested_key_in_json(
    json_data: Union[str, dict, list, int, float, bool, None],
    target_key: str
) -> List[Any]:
    """
    Parses JSON (if the input is a string) and recursively searches for all
    values associated with a specific key within the JSON structure.

    Args:
        json_data: The JSON data to search. This can be:
                   - A JSON string (which will be parsed internally).
                   - A Python dictionary representing a JSON object.
                   - A Python list representing a JSON array.
                   - Any other JSON-compatible primitive type (int, float, bool, None),
                     in which case no nested search will occur.
        target_key: The string key whose values are to be found.

    Returns:
        A list of all values found for the target_key. The order of values
        is not guaranteed to be consistent across different executions, but
        all instances will be collected.
    """
    parsed_data: Any

    # If the input is a JSON string, parse it first
    if isinstance(json_data, str):
        try:
            parsed_data = json.loads(json_data)
        except json.JSONDecodeError:
            # If it's a string but not valid JSON, it cannot contain nested structures.
            # Return an empty list as no nested keys can be found.
            return []
    else:
        # If it's already a Python object, use it directly
        parsed_data = json_data

    found_values: List[Any] = []

    # Recursively search in the parsed data
    if isinstance(parsed_data, dict):
        # Check if the target_key exists at the current dictionary level
        if target_key in parsed_data:
            found_values.append(parsed_data[target_key])
        
        # Recursively search in all values of the dictionary
        for value in parsed_data.values():
            found_values.extend(find_nested_key_in_json(value, target_key))
            
    elif isinstance(parsed_data, list):
        # Recursively search in each item of the list
        for item in parsed_data:
            found_values.extend(find_nested_key_in_json(item, target_key))
            
    # For other types (int, float, bool, None), there are no nested structures
    # or keys to search within them, so nothing is added to found_values here.

    return found_values

EXPORT_FUNCTION = find_nested_key_in_json