import re
import copy
from typing import Any, Dict, List, Optional, Tuple, Union, Callable

class ValidationErrors:
    """Helper class to collect validation errors and manage stopping on the first error."""
    def __init__(self, stop_on_first_error: bool):
        self.errors: List[Dict[str, str]] = []
        self.stop_on_first_error = stop_on_first_error

    def add_error(self, path: str, message: str) -> bool:
        """
        Adds an error and returns True if validation should stop according to `stop_on_first_error`.
        """
        error = {"path": path, "message": message}
        self.errors.append(error)
        return self.stop_on_first_error

    def has_errors(self) -> bool:
        """Checks if any errors have been collected."""
        return len(self.errors) > 0

    def get_errors(self) -> List[Dict[str, str]]:
        """Returns the list of collected errors."""
        return self.errors

def _coerce_value(value: Any, expected_type: str) -> Tuple[Any, bool]:
    """
    Attempts to coerce a value to the expected type.

    Args:
        value: The value to coerce.
        expected_type: The target type (e.g., "string", "integer", "boolean").

    Returns:
        A tuple (coerced_value, success_status).
        success_status is True if coercion was successful, False otherwise.
    """
    if expected_type == "string":
        if isinstance(value, (str, int, float, bool)):
            return str(value), True
    elif expected_type == "integer":
        if isinstance(value, str):
            try:
                # Handle string floats like "1.0" that represent integers
                if '.' in value:
                    float_val = float(value)
                    if float_val == int(float_val):
                        return int(float_val), True
                else: # Handle integer strings like "123"
                    return int(value), True
            except ValueError:
                pass
        elif isinstance(value, float):
            if value == int(value): # Check if float is an exact integer
                return int(value), True
        elif isinstance(value, bool):
            return int(value), True # True -> 1, False -> 0
        elif isinstance(value, int):
            return value, True # Already correct type
    elif expected_type == "number": # Includes integers and floats
        if isinstance(value, str):
            try:
                return float(value), True
            except ValueError:
                pass
        elif isinstance(value, (int, float, bool)):
            return float(value), True # Convert int/bool to float
    elif expected_type == "boolean":
        if isinstance(value, str):
            if value.lower() in ("true", "1"):
                return True, True
            if value.lower() in ("false", "0"):
                return False, True
        elif isinstance(value, (int, float)):
            if value == 1:
                return True, True
            if value == 0:
                return False, True
        elif isinstance(value, bool):
            return value, True # Already correct type
    elif expected_type == "array":
        if isinstance(value, (list, tuple)):
            return list(value), True
    elif expected_type == "object":
        if isinstance(value, dict):
            return value, True

    return value, False

def _validate(
    data_node: Any,
    schema_node: Dict[str, Any],
    path: str,
    errors_collector: ValidationErrors,
    custom_validators: Dict[str, Callable[..., bool]],
    coerce_types_globally: bool,
) -> Tuple[bool, Any]:
    """
    Recursively validates a data node against a schema node.

    Args:
        data_node: The current data element being validated.
        schema_node: The schema definition for the current data_node.
        path: The JSON path to the current data_node (e.g., "root.users[0].name").
        errors_collector: An instance of ValidationErrors to collect validation issues.
        custom_validators: A dictionary of custom validation functions.
        coerce_types_globally: A boolean indicating if type coercion is globally enabled.

    Returns:
        A tuple: (is_node_valid, coerced_data_for_this_node)
        - is_node_valid (bool): True if the current node (and its children) are valid so far.
        - coerced_data_for_this_node (Any): The data node, potentially modified by coercion.
                                            If not coercing, it's a copy to ensure isolation.
    """
    current_value = data_node
    is_node_valid = True

    # Check for 'type' definition in the schema
    expected_type = schema_node.get("type")

    # If `data_node` is a mutable type (list/dict), make a copy to ensure
    # coercion modifies the copy, not the original input data.
    if isinstance(current_value, dict):
        current_value = current_value.copy()
    elif isinstance(current_value, list):
        current_value = current_value.copy()


    # 1. Type validation and coercion
    if expected_type:
        type_matches = False
        if expected_type == "string":
            type_matches = isinstance(current_value, str)
        elif expected_type == "integer":
            # bool is a subclass of int, so explicitly exclude it
            type_matches = isinstance(current_value, int) and not isinstance(current_value, bool)
        elif expected_type == "number":
            type_matches = isinstance(current_value, (int, float)) and not isinstance(current_value, bool)
        elif expected_type == "boolean":
            type_matches = isinstance(current_value, bool)
        elif expected_type == "array":
            type_matches = isinstance(current_value, list)
        elif expected_type == "object":
            type_matches = isinstance(current_value, dict)
        elif expected_type == "null":
            type_matches = current_value is None
        elif expected_type == "any":
            type_matches = True
        else: # Schema error
            is_node_valid = False
            if errors_collector.add_error(path, f"Schema error: Unknown type '{expected_type}' in schema."):
                return False, current_value

        if not type_matches:
            # Determine if coercion is enabled for this specific field
            # A 'coerce' field in schema overrides the global 'coerce_types_globally' setting.
            can_coerce_local = schema_node.get("coerce", coerce_types_globally)
            
            if can_coerce_local:
                coerced_val, success = _coerce_value(current_value, expected_type)
                if success:
                    current_value = coerced_val
                    type_matches = True # Type now matches after successful coercion
                else:
                    is_node_valid = False
                    if errors_collector.add_error(path, f"Expected type '{expected_type}', got '{type(data_node).__name__}'. Coercion failed."):
                        return False, current_value
            else:
                is_node_valid = False
                if errors_collector.add_error(path, f"Expected type '{expected_type}', got '{type(data_node).__name__}'"):
                    return False, current_value
        
        # If type still doesn't match after coercion attempt (or no coercion was attempted/enabled),
        # this node is fundamentally invalid for type.
        if not type_matches:
            # An error has already been added above. We mark is_node_valid = False but
            # continue to allow other (possibly independent) errors to be collected if
            # stop_on_first_error is False. However, be aware that subsequent type-specific
            # checks might fail or misbehave if the type is incorrect.
            # We assume current_value retains its original type in such cases.
            pass


    # 2. Schema specific validations based on the (potentially coerced) type
    if expected_type == "object" and isinstance(current_value, dict):
        new_coerced_obj = {} # Build the new dictionary based on schema
        
        # Populate defaults for missing fields first
        for field_name, sub_schema in schema_node.get("properties", {}).items():
            if field_name not in current_value and "default" in sub_schema:
                # Deep copy default values to prevent shared mutable state
                new_coerced_obj[field_name] = copy.deepcopy(sub_schema["default"])

        # Validate 'required' fields
        required_fields = schema_node.get("required", [])
        for field_name in required_fields:
            if field_name not in current_value and field_name not in new_coerced_obj:
                is_node_valid = False
                if errors_collector.add_error(f"{path}.{field_name}", f"Required field '{field_name}' is missing"):
                    return False, new_coerced_obj # Stop early

        # Process known properties
        properties_schema = schema_node.get("properties", {})
        for key, value in current_value.items():
            sub_path = f"{path}.{key}"
            if key in properties_schema:
                sub_schema = properties_schema[key]
                is_sub_valid, coerced_sub_data = _validate(
                    value, sub_schema, sub_path,
                    errors_collector, custom_validators, coerce_types_globally
                )
                if not is_sub_valid:
                    is_node_valid = False
                    if errors_collector.stop_on_first_error:
                        return False, new_coerced_obj # Propagate stop
                new_coerced_obj[key] = coerced_sub_data
            else:
                # Handle 'additionalProperties'
                additional_properties_schema = schema_node.get("additionalProperties")
                if additional_properties_schema is False:
                    is_node_valid = False
                    if errors_collector.add_error(sub_path, f"Additional property '{key}' is not allowed"):
                        if errors_collector.stop_on_first_error:
                            return False, new_coerced_obj
                elif isinstance(additional_properties_schema, dict):
                    # Validate against additionalProperties schema
                    is_sub_valid, coerced_sub_data = _validate(
                        value, additional_properties_schema, sub_path,
                        errors_collector, custom_validators, coerce_types_globally
                    )
                    if not is_sub_valid:
                        is_node_valid = False
                        if errors_collector.stop_on_first_error:
                            return False, new_coerced_obj
                    new_coerced_obj[key] = coerced_sub_data
                else: # additionalProperties is True or not specified (default True)
                    new_coerced_obj[key] = value # Just copy it

        current_value = new_coerced_obj # Update current_value to the coerced version

    elif expected_type == "array" and isinstance(current_value, list):
        new_coerced_array = [] # Build the new list based on schema
        items_schema = schema_node.get("items")
        
        if items_schema:
            for idx, item in enumerate(current_value):
                sub_path = f"{path}[{idx}]"
                is_sub_valid, coerced_sub_data = _validate(
                    item, items_schema, sub_path,
                    errors_collector, custom_validators, coerce_types_globally
                )
                if not is_sub_valid:
                    is_node_valid = False
                    if errors_collector.stop_on_first_error:
                        return False, new_coerced_array # Propagate stop
                new_coerced_array.append(coerced_sub_data)
        else: # No item schema, just copy items
            new_coerced_array = current_value.copy()

        # Array specific validations
        min_items = schema_node.get("minItems")
        if min_items is not None and len(new_coerced_array) < min_items:
            is_node_valid = False
            if errors_collector.add_error(path, f"Expected at least {min_items} items, got {len(new_coerced_array)}"):
                return False, new_coerced_array

        max_items = schema_node.get("maxItems")
        if max_items is not None and len(new_coerced_array) > max_items:
            is_node_valid = False
            if errors_collector.add_error(path, f"Expected at most {max_items} items, got {len(new_coerced_array)}"):
                return False, new_coerced_array

        unique_items = schema_node.get("uniqueItems")
        if unique_items is True:
            # Attempt to check uniqueness. If items are unhashable, catch TypeError.
            try:
                # Convert mutable objects (lists, dicts) to hashable equivalents for set comparison
                hashable_items = [
                    tuple(item) if isinstance(item, list) else 
                    frozenset(sorted(item.items())) if isinstance(item, dict) else # Sort items for consistent frozenset hash
                    item for item in new_coerced_array
                ]
                if len(set(hashable_items)) != len(new_coerced_array):
                    is_node_valid = False
                    if errors_collector.add_error(path, "Array items must be unique"):
                        return False, new_coerced_array
            except TypeError:
                is_node_valid = False
                if errors_collector.add_error(path, "Cannot check for uniqueItems with unhashable array elements (e.g., objects with unhashable keys)"):
                    return False, new_coerced_array
            except Exception as e: # Catch other potential issues with conversion for hashing
                is_node_valid = False
                if errors_collector.add_error(path, f"Error checking uniqueItems: {e}"):
                    return False, new_coerced_array

        current_value = new_coerced_array # Update current_value to the coerced version

    # Primitive type validations (string, number, integer, boolean, null, any)
    elif expected_type in ["string", "integer", "number", "boolean", "null", "any"]:
        # String validations
        if expected_type == "string" and isinstance(current_value, str):
            min_length = schema_node.get("minLength")
            if min_length is not None and len(current_value) < min_length:
                is_node_valid = False
                if errors_collector.add_error(path, f"Expected string of min length {min_length}, got {len(current_value)}"):
                    return False, current_value

            max_length = schema_node.get("maxLength")
            if max_length is not None and len(current_value) > max_length:
                is_node_valid = False
                if errors_collector.add_error(path, f"Expected string of max length {max_length}, got {len(current_value)}"):
                    return False, current_value

            pattern = schema_node.get("pattern")
            if pattern is not None:
                try:
                    if not re.fullmatch(pattern, current_value):
                        is_node_valid = False
                        if errors_collector.add_error(path, f"String does not match pattern '{pattern}'"):
                            return False, current_value
                except re.error:
                    is_node_valid = False
                    if errors_collector.add_error(path, f"Schema error: Invalid regex pattern '{pattern}'"):
                        return False, current_value

            format_type = schema_node.get("format")
            if format_type == "email":
                if not re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", current_value):
                    is_node_valid = False
                    if errors_collector.add_error(path, f"String is not a valid email format"):
                        return False, current_value
            elif format_type == "uri":
                 # A more robust regex for URI, covering common valid cases
                 if not re.fullmatch(r"^[a-zA-Z][a-zA-Z0-9+-.]*://\S+$", current_value):
                    is_node_valid = False
                    if errors_collector.add_error(path, f"String is not a valid URI format"):
                        return False, current_value
            elif format_type == "uuid":
                if not re.fullmatch(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", current_value):
                    is_node_valid = False
                    if errors_collector.add_error(path, f"String is not a valid UUID format"):
                        return False, current_value
            # Add more format checks as needed

        # Number/Integer validations
        if expected_type in ["integer", "number"] and isinstance(current_value, (int, float)):
            minimum = schema_node.get("minimum")
            if minimum is not None and current_value < minimum:
                is_node_valid = False
                if errors_collector.add_error(path, f"Expected value >= {minimum}, got {current_value}"):
                    return False, current_value

            maximum = schema_node.get("maximum")
            if maximum is not None and current_value > maximum:
                is_node_valid = False
                if errors_collector.add_error(path, f"Expected value <= {maximum}, got {current_value}"):
                    return False, current_value

            exclusive_minimum = schema_node.get("exclusiveMinimum")
            if exclusive_minimum is not None and current_value <= exclusive_minimum:
                is_node_valid = False
                if errors_collector.add_error(path, f"Expected value > {exclusive_minimum}, got {current_value}"):
                    return False, current_value

            exclusive_maximum = schema_node.get("exclusiveMaximum")
            if exclusive_maximum is not None and current_value >= exclusive_maximum:
                is_node_valid = False
                if errors_collector.add_error(path, f"Expected value < {exclusive_maximum}, got {current_value}"):
                    return False, current_value

            multiple_of = schema_node.get("multipleOf")
            if multiple_of is not None and isinstance(multiple_of, (int, float)) and multiple_of != 0:
                # Use a small epsilon for float comparisons to avoid precision issues
                if not (current_value / multiple_of).is_integer():
                    is_node_valid = False
                    if errors_collector.add_error(path, f"Expected value to be a multiple of {multiple_of}, got {current_value}"):
                        return False, current_value
            elif multiple_of is not None: # Catch non-numeric or zero multipleOf in schema
                is_node_valid = False
                if errors_collector.add_error(path, f"Schema error: 'multipleOf' must be a non-zero number, got '{multiple_of}'"):
                    return False, current_value
    
    # 3. Custom Validator
    custom_validator_name = schema_node.get("custom_validator")
    if custom_validator_name:
        validator = custom_validators.get(custom_validator_name)
        if validator:
            try:
                if not validator(current_value):
                    is_node_valid = False
                    if errors_collector.add_error(path, f"Custom validator '{custom_validator_name}' failed for value '{current_value}'"):
                        return False, current_value
            except Exception as e:
                is_node_valid = False
                if errors_collector.add_error(path, f"Custom validator '{custom_validator_name}' raised an exception: {e}"):
                    return False, current_value
        else:
            is_node_valid = False
            if errors_collector.add_error(path, f"Custom validator '{custom_validator_name}' not found in provided validators map"):
                return False, current_value
    
    # 4. Enum validation
    enum_values = schema_node.get("enum")
    if enum_values is not None:
        if current_value not in enum_values:
            is_node_valid = False
            if errors_collector.add_error(path, f"Value '{current_value}' is not one of the allowed enum values: {enum_values}"):
                return False, current_value

    return is_node_valid, current_value


def validate_json_schema(
    data: Any,
    schema: Dict[str, Any],
    custom_validators: Optional[Dict[str, Callable[..., bool]]] = None,
    coerce_types: bool = False,
    stop_on_first_error: bool = False
) -> Tuple[bool, Optional[Any], List[Dict[str, str]]]:
    """
    Validates nested JSON against a schema with custom validators, type coercion options,
    and error collection modes.

    Args:
        data: The JSON data (dict, list, or primitive) to validate.
        schema: The JSON schema (dict) to validate against.
        custom_validators: An optional dictionary mapping validator names (str) to callable functions.
                           Each function should take the field value as its first argument and return
                           True for valid or False for invalid.
        coerce_types: If True, type coercion is globally enabled. This means the validator will attempt
                      to convert data types to match the schema's 'type' if they are coercible (e.g.,
                      "123" to 123 for an integer field, or 1 to True for a boolean field).
                      This global setting can be overridden for individual fields by specifying
                      `"coerce": true` or `"coerce": false` in their respective schema nodes.
        stop_on_first_error: If True, validation stops and returns immediately upon the first error found.
                             If False, all possible errors are collected throughout the data structure.

    Returns:
        A tuple: (is_valid, coerced_data, errors)
        - is_valid (bool): True if the data is valid against the schema (and all coercions, if enabled,
                           were successful and respected schema rules), False otherwise.
        - coerced_data (Any | None): If `coerce_types` is True (or `coerce: true` in schema for a field),
                                     this will be the validated data with types coerced as per the schema.
                                     If `coerce_types` is False, `coerced_data` will be None.
                                     In case of validation failure with `coerce_types` True, it will contain
                                     partially coerced data up to the point of failure.
                                     Note: If `data` is a primitive and `coerce_types` is True, this
                                     might return the coerced primitive.
        - errors (List[Dict[str, str]]): A list of error dictionaries. Each dictionary contains
                                         "path" (string indicating the location of the error, e.g.,
                                         "root.fieldName" or "root.arrayName[index]") and "message"
                                         (string describing the validation error). The list is empty
                                         if no errors occurred. If `stop_on_first_error` is True,
                                         this list will contain at most one error.
    """
    errors_collector = ValidationErrors(stop_on_first_error)
    validators = custom_validators if custom_validators is not None else {}

    is_valid, final_coerced_data = _validate(
        data,
        schema,
        "root", # Initial path for the root of the JSON data
        errors_collector,
        validators,
        coerce_types,
    )

    result_coerced_data = final_coerced_data if coerce_types else None
    
    return not errors_collector.has_errors(), result_coerced_data, errors_collector.get_errors()

EXPORT_FUNCTION = validate_json_schema