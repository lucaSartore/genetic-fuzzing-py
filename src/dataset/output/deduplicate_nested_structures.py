import collections.abc
from typing import Any, Callable, Iterable, Literal, TypeVar, Union, cast

# A type variable to represent the original collection type, allowing for precise type hints.
_T = TypeVar('_T')

def _deduplicate_single_collection_generic(
    items: Iterable[Any],
    equality_func: Callable[[Any, Any], bool] | None,
    preservation_strategy: Literal['first', 'last']
) -> list[Any]:
    """
    An auxiliary function to deduplicate a flat iterable of items based on a
    custom equality function and preservation strategy.

    Args:
        items: An iterable of elements to deduplicate.
        equality_func: An optional callable `(a: Any, b: Any) -> bool`. If `None`,
                       standard `==` is used for comparison.
        preservation_strategy: 'first' to keep the first encountered item,
                               'last' to keep the last encountered item.

    Returns:
        A new list containing the deduplicated items, preserving their relative order
        based on the chosen strategy.
    """
    result = []
    seen_elements = []  # Stores elements that have been added to 'result'

    # Convert to a list to allow reversal if 'last' strategy is used and
    # to handle single-pass iterators.
    items_list = list(items)

    if preservation_strategy == 'last':
        # To keep the last occurrence, iterate in reverse. The first item encountered
        # in reverse order is effectively the last in original order.
        items_list.reverse()

    for item in items_list:
        is_duplicate = False
        for seen_item in seen_elements:
            if equality_func:
                if equality_func(item, seen_item):
                    is_duplicate = True
                    break
            else:
                if item == seen_item:
                    is_duplicate = True
                    break
        
        if not is_duplicate:
            result.append(item)
            seen_elements.append(item)
    
    if preservation_strategy == 'last':
        # Reverse the result back to maintain the original relative order of the kept items.
        result.reverse()
    
    return result

def deduplicate_nested_structures(
    collection: _T,
    equality_func: Callable[[Any, Any], bool] | None = None,
    preservation_strategy: Literal['first', 'last'] = 'first',
    _recursion_memo: dict[int, Any] | None = None # Internal parameter for handling cyclic structures
) -> _T:
    """
    Removes duplicates from nested collections using custom equality functions
    and preservation strategies.

    This function recursively traverses nested lists, tuples, sets, and dictionaries,
    de-duplicating their elements based on the provided `equality_func` and
    `preservation_strategy`. It produces a new collection structure, leaving the
    original untouched.

    For lists and tuples, duplicates among their direct elements are removed.
    For sets, elements are de-duplicated *before* being added to the new set. Note that
    the final set conversion will enforce Python's default uniqueness rules based on
    `__hash__` and `__eq__`, which might interact with `equality_func` if they differ.
    For dictionaries, keys are de-duplicated based on `equality_func` and
    `preservation_strategy` (e.g., if 'first', the first key encountered is kept;
    if 'last', the last one is kept). Values are processed recursively.

    Args:
        collection: The nested collection (e.g., `list`, `tuple`, `set`, `dict`) or
                    a base type (e.g., `str`, `int`, `float`) to process.
        equality_func: An optional callable `(a: Any, b: Any) -> bool` that
                       returns `True` if `a` and `b` are considered equal for
                       de-duplication purposes. If `None`, standard `==` is used.
        preservation_strategy: A string indicating which duplicate to keep:
                               'first' (default) keeps the first encountered item,
                               'last' keeps the last encountered item.
        _recursion_memo: Internal parameter used by the function to detect and handle
                         cyclic data structures, preventing infinite recursion.
                         Users should not pass this argument directly.

    Returns:
        A new collection of the same type as the input, with duplicates removed
        according to the specified strategy and equality function. Base types
        (like numbers, strings) are returned as is.

    Raises:
        TypeError: If a processed element intended for a set, or a processed key
                   for a dictionary, becomes unhashable during recursion.
                   Python sets and dictionary keys require their elements/keys to be hashable.
    """
    if _recursion_memo is None:
        _recursion_memo = {}

    # Base case: If the item is not a known collection type, return it as is.
    # This handles primitive types (int, str, float, None, etc.).
    if not isinstance(collection, (list, tuple, set, dict)):
        return collection

    # Check for cyclic structures or already processed collection objects.
    # We use the object's identity (id) to uniquely identify it in the memo.
    collection_id = id(collection)
    if collection_id in _recursion_memo:
        return _recursion_memo[collection_id]

    # Initialize a variable to hold the processed collection before memoization.
    processed_collection: Any

    if isinstance(collection, (list, tuple)):
        # For lists and tuples, first recursively process each element.
        processed_elements_recursive = []
        for item in collection:
            processed_elements_recursive.append(
                deduplicate_nested_structures(item, equality_func, preservation_strategy, _recursion_memo)
            )
        
        # Then, apply de-duplication to the flat list of processed elements.
        deduplicated_flat_list = _deduplicate_single_collection_generic(
            processed_elements_recursive, equality_func, preservation_strategy
        )

        # Reconstruct the collection to its original type (list or tuple).
        if isinstance(collection, list):
            processed_collection = deduplicated_flat_list
        else:  # tuple
            processed_collection = tuple(deduplicated_flat_list)

    elif isinstance(collection, set):
        # For sets, recursively process each element first.
        processed_elements_recursive = []
        for item in collection:
            processed_elements_recursive.append(
                deduplicate_nested_structures(item, equality_func, preservation_strategy, _recursion_memo)
            )
        
        # Apply de-duplication to the collected elements based on `equality_func`.
        # Note: The final conversion to `set()` will perform its own uniqueness check
        # based on Python's default `__hash__` and `__eq__`. If `equality_func` differs
        # significantly from `__eq__`, this might lead to further (unintended)
        # de-duplication or retention of items `equality_func` deems identical.
        deduplicated_flat_list = _deduplicate_single_collection_generic(
            processed_elements_recursive, equality_func, preservation_strategy
        )

        # Attempt to convert the de-duplicated list to a set.
        # This step requires all elements to be hashable.
        try:
            processed_collection = set(deduplicated_flat_list)
        except TypeError as e:
            raise TypeError(
                f"Processed element for set is unhashable: {e}. "
                "Cannot convert to set if elements become unhashable after de-duplication recursion. "
                "Consider ensuring elements remain hashable or changing the target collection type."
            ) from e

    elif isinstance(collection, dict):
        # For dictionaries, we want to de-duplicate based on keys using the custom
        # equality function and preservation strategy, while recursively processing values.
        temp_items_for_deduplication = []
        for k, v in collection.items():
            # Recursively process both keys and values.
            processed_k = deduplicate_nested_structures(k, equality_func, preservation_strategy, _recursion_memo)
            processed_v = deduplicate_nested_structures(v, equality_func, preservation_strategy, _recursion_memo)
            temp_items_for_deduplication.append((processed_k, processed_v))

        deduplicated_dict_items: list[tuple[Any, Any]] = []
        # Stores keys (or key-value pairs) that have been added to `deduplicated_dict_items`
        seen_keys_for_dict_deduplication = []

        # Prepare the list of items for de-duplication based on keys, respecting strategy.
        items_list_for_dict_processing = list(temp_items_for_deduplication)
        if preservation_strategy == 'last':
            items_list_for_dict_processing.reverse()

        for k, v in items_list_for_dict_processing:
            is_key_duplicate = False
            for seen_k, _ in seen_keys_for_dict_deduplication: # Compare 'k' with 'seen_k'
                if equality_func:
                    if equality_func(k, seen_k):
                        is_key_duplicate = True
                        break
                else:
                    if k == seen_k:
                        is_key_duplicate = True
                        break
            
            if not is_key_duplicate:
                deduplicated_dict_items.append((k, v))
                seen_keys_for_dict_deduplication.append((k, v)) # Store the (k,v) pair, but comparison is on k
        
        if preservation_strategy == 'last':
            # Reverse back to maintain the original relative order of the kept items.
            deduplicated_dict_items.reverse()

        # Reconstruct the dictionary. All keys in `deduplicated_dict_items` must be hashable.
        new_dict_result = {}
        for k, v in deduplicated_dict_items:
            try:
                new_dict_result[k] = v
            except TypeError as e:
                raise TypeError(
                    f"Processed key for dictionary is unhashable: {e}. "
                    "Cannot use as a dictionary key if it becomes unhashable after de-duplication recursion. "
                    "Consider ensuring keys remain hashable or changing the key type."
                ) from e
        processed_collection = new_dict_result

    # Memoize the result of processing this specific collection object (by its id).
    # This is crucial for handling cyclic references and for efficiency if the same
    # collection object appears multiple times in the nested structure.
    _recursion_memo[collection_id] = processed_collection
    
    # Cast the result to the input type variable `_T` for accurate type hinting.
    return cast(_T, processed_collection)

EXPORT_FUNCTION = deduplicate_nested_structures