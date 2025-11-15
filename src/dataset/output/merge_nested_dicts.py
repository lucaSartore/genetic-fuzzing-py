# necessary imports (use only the python standard libraries)
import enum
from typing import Any, Dict

# you can define other auxiliary functions
class ConflictStrategy(enum.Enum):
    """
    Defines strategies for handling key conflicts during dictionary merging.
    """
    OVERWRITE = "overwrite"  # New value replaces existing value.
    MERGE = "merge"          # If both values are dicts, they are recursively merged.
                             # Otherwise, new value overwrites existing.
    KEEP = "keep"            # Existing value is kept; new value is ignored.

def merge_nested_dicts(
    *dicts: Dict[Any, Any],
    conflict_strategy: ConflictStrategy
) -> Dict[Any, Any]:
    """
    Recursively merges multiple dictionaries with nested structures,
    handling conflicts via a strategy enum (overwrite/merge/keep).

    Args:
        *dicts: One or more dictionaries to merge. They are processed in order.
                Later dictionaries can overwrite/merge with earlier ones
                based on the conflict_strategy. Non-dictionary inputs at the
                top level will be skipped.
        conflict_strategy: The strategy to use when a key exists in multiple
                           dictionaries being merged.
                           - ConflictStrategy.OVERWRITE: The value from the later
                                 dictionary in the *dicts sequence takes precedence,
                                 replacing any existing value for that key.
                           - ConflictStrategy.MERGE: If both the existing value and
                                 the new value are dictionaries, they are recursively
                                 merged using the same conflict strategy. Otherwise,
                                 the new value overwrites the existing one.
                           - ConflictStrategy.KEEP: The value from the earlier
                                 dictionary in the *dicts sequence takes precedence,
                                 and the new value for that key is ignored.

    Returns:
        A new dictionary representing the merged result.

    Raises:
        ValueError: If an unknown conflict strategy is provided (should not happen
                    if `ConflictStrategy` enum is strictly used).

    Examples:
        >>> d1 = {'a': 1, 'b': {'x': 10}}
        >>> d2 = {'b': {'y': 20}, 'c': 3}
        >>> d3 = {'b': {'x': 11, 'z': 30}, 'a': 2}

        >>> # Overwrite strategy: latest value wins
        >>> merge_nested_dicts(d1, d2, conflict_strategy=ConflictStrategy.OVERWRITE)
        {'a': 1, 'b': {'y': 20}, 'c': 3}
        >>> merge_nested_dicts(d1, d2, d3, conflict_strategy=ConflictStrategy.OVERWRITE)
        {'a': 2, 'b': {'x': 11, 'z': 30}, 'c': 3}

        >>> # Merge strategy: nested dictionaries are merged, others overwritten
        >>> merge_nested_dicts(d1, d2, conflict_strategy=ConflictStrategy.MERGE)
        {'a': 1, 'b': {'x': 10, 'y': 20}, 'c': 3}
        >>> merge_nested_dicts(d1, d2, d3, conflict_strategy=ConflictStrategy.MERGE)
        {'a': 2, 'b': {'x': 11, 'y': 20, 'z': 30}, 'c': 3}
        >>> # Merge with type conflict - new non-dict overwrites existing dict
        >>> merge_nested_dicts({'k': {'a': 1}}, {'k': 2}, conflict_strategy=ConflictStrategy.MERGE)
        {'k': 2}
        >>> # Merge with type conflict - existing non-dict is overwritten by new dict
        >>> merge_nested_dicts({'k': 1}, {'k': {'a': 2}}, conflict_strategy=ConflictStrategy.MERGE)
        {'k': {'a': 2}}

        >>> # Keep strategy: first value encountered wins
        >>> merge_nested_dicts(d1, d2, conflict_strategy=ConflictStrategy.KEEP)
        {'a': 1, 'b': {'x': 10}, 'c': 3}
        >>> merge_nested_dicts(d1, d2, d3, conflict_strategy=ConflictStrategy.KEEP)
        {'a': 1, 'b': {'x': 10}, 'c': 3}

        >>> # Handling non-dict input (skipped)
        >>> merge_nested_dicts(d1, None, {'k': 5}, conflict_strategy=ConflictStrategy.OVERWRITE)
        {'a': 1, 'b': {'x': 10}, 'k': 5}
    """
    result: Dict[Any, Any] = {}

    for d in dicts:
        # Skip non-dictionary inputs at the top level to avoid errors
        # and provide robust merging.
        if not isinstance(d, dict):
            continue 

        for key, value in d.items():
            if key not in result:
                # No conflict, simply add the key-value pair
                result[key] = value
            else:
                # Conflict detected, apply the specified strategy
                existing_value = result[key]

                if conflict_strategy == ConflictStrategy.OVERWRITE:
                    result[key] = value
                elif conflict_strategy == ConflictStrategy.KEEP:
                    # Do nothing, the existing_value is already in result[key]
                    pass
                elif conflict_strategy == ConflictStrategy.MERGE:
                    # Check if both values are dictionaries for a recursive merge
                    if isinstance(existing_value, dict) and isinstance(value, dict):
                        # Recursively merge the nested dictionaries, passing
                        # the same conflict strategy down
                        result[key] = merge_nested_dicts(
                            existing_value, value, conflict_strategy=conflict_strategy
                        )
                    else:
                        # If types are different or not both dicts, overwrite
                        # with the new value (similar to OVERWRITE strategy)
                        result[key] = value
                else:
                    # This case should theoretically not be reachable if
                    # `conflict_strategy` is strictly an instance of `ConflictStrategy`.
                    raise ValueError(f"Unknown conflict strategy: {conflict_strategy}")

    return result

# add this ad the end of the file
EXPORT_FUNCTION = merge_nested_dicts