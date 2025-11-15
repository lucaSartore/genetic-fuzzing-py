import collections
from typing import List, Dict, Tuple, Any, Union

def group_by_composite_key(
    data: List[Dict[str, Any]],
    group_keys: List[str],
    agg_functions: Dict[str, Tuple[str, str]]
) -> List[Dict[str, Any]]:
    """
    Groups a list of dictionaries by multiple keys, with aggregation functions
    (sum/mean/concat) for value lists.

    Args:
        data: A list of dictionaries, where each dictionary represents a record.
              Example: [{'id': 1, 'category': 'A', 'value': 10}, ...]
        group_keys: A list of strings, where each string is a key to group by.
                    The combination of values for these keys forms the composite
                    group key.
                    Example: ['category', 'sub_category']
        agg_functions: A dictionary mapping output field names to tuples
                       (source_key, agg_type).
                       - output_field_name (str): The name of the field in the
                                                  result dictionary for the
                                                  aggregated value.
                       - source_key (str): The key in the original dictionaries
                                           whose values need to be aggregated.
                       - agg_type (str): A string indicating the type of
                                         aggregation: 'sum', 'mean', or 'concat'.
                       Example: {'total_value': ('value', 'sum'),
                                 'average_quantity': ('qty', 'mean'),
                                 'combined_notes': ('notes', 'concat')}

    Returns:
        A list of dictionaries. Each dictionary in the output represents a group
        and contains the `group_keys` and their respective values, plus the
        aggregated values for each specified aggregation function.
    
    Raises:
        TypeError: If input arguments are not of the expected types.
        ValueError: If an unknown aggregation type is specified.
    """
    # Type validation for input arguments
    if not isinstance(data, list):
        raise TypeError("The 'data' argument must be a list.")
    if not all(isinstance(item, dict) for item in data):
        raise TypeError("All items in the 'data' list must be dictionaries.")
    if not isinstance(group_keys, list) or not all(isinstance(k, str) for k in group_keys):
        raise TypeError("The 'group_keys' argument must be a list of strings.")
    if not isinstance(agg_functions, dict):
        raise TypeError("The 'agg_functions' argument must be a dictionary.")
    
    for output_field, agg_spec in agg_functions.items():
        if not isinstance(output_field, str):
            raise TypeError(f"Keys in 'agg_functions' must be strings (output field names), got {type(output_field)}.")
        if not isinstance(agg_spec, tuple) or len(agg_spec) != 2:
            raise TypeError(f"Values in 'agg_functions' must be tuples of (source_key: str, agg_type: str), got {type(agg_spec)}.")
        source_key, agg_type = agg_spec
        if not isinstance(source_key, str) or not isinstance(agg_type, str):
            raise TypeError(f"Values in 'agg_functions' must be tuples of (source_key: str, agg_type: str), got ({type(source_key)}, {type(agg_type)}).")
        if agg_type not in ['sum', 'mean', 'concat']:
            raise ValueError(f"Unknown aggregation type: '{agg_type}'. Must be 'sum', 'mean', or 'concat'.")

    # Step 1: Initialize a dictionary to temporarily store grouped rows.
    # The keys of this dictionary will be the composite group keys (as tuples),
    # and the values will be lists of original dictionaries belonging to that group.
    grouped_rows: Dict[Tuple[Any, ...], List[Dict[str, Any]]] = collections.defaultdict(list)

    # Step 2: Iterate through the input data and group rows.
    for row in data:
        # Create a composite key by extracting values for the specified group_keys.
        # .get() is used to handle cases where a group_key might be missing from a row,
        # resulting in a None value for that part of the composite key.
        composite_key_values = tuple(row.get(key) for key in group_keys)
        grouped_rows[composite_key_values].append(row)

    # Step 3: Process each group and apply aggregation functions.
    result: List[Dict[str, Any]] = []
    for composite_key_values, rows_in_group in grouped_rows.items():
        output_row: Dict[str, Any] = {}

        # Add the group key values to the output row.
        for i, key in enumerate(group_keys):
            output_row[key] = composite_key_values[i]

        # Apply each specified aggregation function.
        for output_field, (source_key, agg_type) in agg_functions.items():
            # Collect all values for the current source_key from all rows within this group.
            # We collect None values as well, letting the aggregation logic decide how to handle them.
            values_to_aggregate: List[Any] = [row.get(source_key) for row in rows_in_group]

            aggregated_value: Any = None  # Default value for aggregation result

            if agg_type == 'sum':
                # Sum only numeric values (int or float), ignoring None or other non-numeric types.
                numeric_values = [v for v in values_to_aggregate if isinstance(v, (int, float))]
                aggregated_value = sum(numeric_values) # sum([]) is 0, which is desired behavior

            elif agg_type == 'mean':
                # Calculate the mean for numeric values.
                # Ignore None or non-numeric types.
                numeric_values = [v for v in values_to_aggregate if isinstance(v, (int, float))]
                if numeric_values:
                    aggregated_value = sum(numeric_values) / len(numeric_values)
                else:
                    # Mean is undefined if no numeric values are present.
                    # Return None in this case.
                    aggregated_value = None

            elif agg_type == 'concat':
                # Concatenate the string representation of all non-None values.
                # Values are converted to strings before concatenation.
                string_values = [str(v) for v in values_to_aggregate if v is not None]
                aggregated_value = "".join(string_values)

            output_row[output_field] = aggregated_value
        
        result.append(output_row)
    
    return result

EXPORT_FUNCTION = group_by_composite_key