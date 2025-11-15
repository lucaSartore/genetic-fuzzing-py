import collections.abc
from typing import Union, List, Tuple, Set, Any, Iterable, Type

def _flatten_generator(
    item: Any,
    current_level: int,
    max_depth: Union[int, None]
) -> Iterable[Any]:
    """
    A recursive generator that flattens nested collections (lists, tuples, sets)
    up to a specified depth.

    Args:
        item: The current item being processed. It can be a collection (list, tuple, set)
              or any other basic type.
        current_level: The current recursion depth, starting from 0 for the initial call
                       to the top-level collection.
        max_depth: The maximum depth to flatten.
                   If `None`, flattening occurs to all possible depths (full flattening).
                   If an integer `N` (where N > 0), the function will unpack elements
                   from collections at levels 0, 1, ..., up to level `N-1`.
                   Collections found at level `N` or deeper will be yielded as-is.
                   
                   Example: `[[1, 2], [3, [4, 5]]]`
                   - `max_depth=1`: `_flatten_generator` unpacks the outer list (level 0).
                     `[1, 2]` (level 1) and `[3, [4, 5]]` (level 1) are yielded as-is because
                     their `current_level` (1) is not greater than `max_depth` (1).
                     Result: `[1, 2, [3, [4, 5]]]`
                   - `max_depth=2`: `_flatten_generator` unpacks outer list (level 0) AND
                     inner lists (level 1).
                     `[1, 2]` is unpacked, yielding `1` and `2`.
                     `[3, [4, 5]]` is unpacked, yielding `3`.
                     `[4, 5]` (level 2) is yielded as-is because its `current_level` (2)
                     is not greater than `max_depth` (2).
                     Result: `[1, 2, 3, [4, 5]]`
                   - `max_depth=None`: Full flattening.
                     Result: `[1, 2, 3, 4, 5]`
    """

    # Define what types are considered "flattenable collections" for this function.
    # Strings, bytes, dicts, etc., are iterables but usually not intended for this kind of flattening.
    is_target_collection = isinstance(item, (list, tuple, set))

    # Condition to stop flattening for the current `item` and yield it as-is:
    # 1. The `item` is not one of our target flattenable collection types.
    # 2. We have descended beyond the maximum specified flattening depth.
    #    If `max_depth` is `None`, this condition (current_level > max_depth) will never be true,
    #    allowing full flattening for target collections.
    if not is_target_collection or (max_depth is not None and current_level >= max_depth):
        yield item
        return
    
    # If the item is a flattenable collection and we haven't reached the depth limit yet,
    # iterate through its sub-items and recursively flatten them.
    for sub_item in item:
        yield from _flatten_generator(sub_item, current_level + 1, max_depth)


def flatten_heterogeneous_list(
    nested_collection: Union[List[Any], Tuple[Any, ...], Set[Any]],
    depth: Union[int, None],
    preserve_type: bool = False
) -> Union[List[Any], Tuple[Any, ...], Set[Any]]:
    """
    Flattens nested collections (lists, tuples, sets) up to a specified depth,
    with an option to preserve the original top-level collection type.

    Args:
        nested_collection: The input collection (can be a list, tuple, or set)
                           containing mixed types, including other nested collections.
        depth: The maximum depth to flatten.
               - `None`: Flattens all nested collections completely.
               - `0` (or less): Returns the `nested_collection` unchanged (or wrapped in a list
                 if `preserve_type` is `False`). No flattening occurs.
               - `N` (an integer > 0): Flattens nested collections up to `N` levels deep.
                 This means collections at level `N-1` will be unpacked, but collections
                 at level `N` will be kept as-is.
                 E.g., `depth=1` flattens only the immediate children of the top-level collection.
                 `flatten_heterogeneous_list([[1, 2], [3, [4, 5]]], depth=1)` would result in
                 `[1, 2, 3, [4, 5]]` (assuming `preserve_type=False`).
        preserve_type: If `True`, the returned collection will be of the same type
                       as the input `nested_collection` (e.g., if input is a tuple,
                       output is a tuple). If `False`, the function always returns a `list`.

    Returns:
        A flattened collection (list, tuple, or set) according to the `depth`
        and `preserve_type` parameters.

    Raises:
        TypeError: If `nested_collection` is not a list, tuple, or set,
                   or if `depth` is not an int or None, or if `preserve_type` is not a bool.
                   Also raised if `preserve_type=True` and the flattened elements cannot
                   be converted to the original set type (e.g., due to unhashable items).
    """

    # --- Input Validation ---
    if not isinstance(nested_collection, (list, tuple, set)):
        raise TypeError("Input 'nested_collection' must be a list, tuple, or set.")
    if depth is not None and not isinstance(depth, int):
        raise TypeError("Input 'depth' must be an integer or None.")
    if not isinstance(preserve_type, bool):
        raise TypeError("Input 'preserve_type' must be a boolean.")

    # --- Edge case: depth = 0 or less (no flattening) ---
    if depth is not None and depth <= 0:
        if preserve_type:
            # If depth is 0 and preserving type, return the original collection as is.
            return nested_collection
        else:
            # If depth is 0 and not preserving type, wrap the original collection in a list.
            return [nested_collection]

    # --- Perform flattening using the generator ---
    # The generator yields all elements flattened up to the specified depth.
    # `depth` for `_flatten_generator` is equivalent to `max_depth_exclusive` for iteration.
    # i.e., iterate if `current_level < max_depth`.
    flattened_elements = list(_flatten_generator(nested_collection, 0, depth))

    # --- Apply final type preservation if requested ---
    if preserve_type:
        original_type = type(nested_collection)
        
        # Special handling for sets: they cannot contain unhashable types
        # and automatically remove duplicates.
        if original_type is set:
            try:
                # Attempt to convert the flattened list back to a set.
                # This will raise TypeError if any elements are unhashable.
                return original_type(flattened_elements)
            except TypeError as e:
                raise TypeError(
                    f"Cannot convert flattened elements to a set due to unhashable types in the result. "
                    f"Original error: {e}"
                ) from e
        else:
            # For lists and tuples, direct conversion from list is straightforward.
            return original_type(flattened_elements)
    else:
        # Default behavior: always return a list.
        return flattened_elements

EXPORT_FUNCTION = flatten_heterogeneous_list