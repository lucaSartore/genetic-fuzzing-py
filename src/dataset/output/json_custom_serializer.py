import json
import datetime
from typing import Any

def _custom_json_default_handler(obj: Any) -> Any:
    """
    Custom JSON serializer for objects not serializable by default json encoder.
    Handles datetime objects by converting them to ISO 8601 strings,
    and set objects by converting them to lists.

    Args:
        obj: The object to be serialized.

    Returns:
        A JSON-serializable representation of the object.

    Raises:
        TypeError: If the object type is not handled by this function
                   and is not JSON serializable by default.
    """
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    elif isinstance(obj, set):
        return list(obj)
    # Let the default JSON encoder's error handling take over for other types
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def json_custom_serializer(obj: Any) -> str:
    """
    Serializes a complex Python object (e.g., containing 'datetime' or 'set') to a JSON string.

    This function extends the default JSON serialization to handle `datetime` objects
    (converted to ISO 8601 strings) and `set` objects (converted to lists).

    Args:
        obj: The complex Python object to serialize. It can be of any type.

    Returns:
        A JSON string representation of the object.

    Raises:
        TypeError: If an object type encountered during serialization is not
                   JSON serializable by default, or by this custom serializer.
        OverflowError: If `list` (or other data structures) are too deep.
    """
    return json.dumps(obj, default=_custom_json_default_handler)

EXPORT_FUNCTION = json_custom_serializer