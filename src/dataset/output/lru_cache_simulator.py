import collections
from typing import Any, List, Tuple, Union, Optional

def lru_cache_simulator(capacity: int, operations: List[Union[Tuple[str, Any, Any], Tuple[str, Any]]]) -> List[Optional[Any]]:
    """
    Simulates an LRU (Least Recently Used) cache's 'get' and 'put' operations.
    Uses 'collections.OrderedDict' to maintain key order, where the most recently
    used items are at the end (right) and the least recently used are at the
    beginning (left).

    Args:
        capacity: The maximum number of key-value pairs the cache can hold.
                  Must be a positive integer.
        operations: A list of operations to perform on the cache.
                    Each operation is a tuple:
                    - For 'put' operation: ('put', key: Any, value: Any)
                    - For 'get' operation: ('get', key: Any)

    Returns:
        A list of results from 'get' operations. For each 'get' operation:
        - If the key is found, its corresponding value is returned.
        - If the key is not found, None is returned.
    """
    if not isinstance(capacity, int) or capacity <= 0:
        raise ValueError("Capacity must be a positive integer.")

    # OrderedDict stores items in insertion order.
    # We use it to simulate LRU:
    # - The start (left) of the OrderedDict holds LRU items.
    # - The end (right) of the OrderedDict holds MRU items.
    cache: collections.OrderedDict[Any, Any] = collections.OrderedDict()
    results: List[Optional[Any]] = []

    for op in operations:
        op_type = op[0]
        key = op[1]

        if op_type == 'put':
            value = op[2] # type: ignore (mypy might complain about op[2] for get ops, but we handle it by type)

            if key in cache:
                # Update existing key's value and mark as most recently used (MRU)
                cache[key] = value
                cache.move_to_end(key)
            else:
                # New key
                if len(cache) >= capacity:
                    # Cache is full, remove the least recently used (LRU) item
                    cache.popitem(last=False) # last=False removes the first (LRU) item
                cache[key] = value # Add new item, it's automatically at the end (MRU)

        elif op_type == 'get':
            if key in cache:
                # Retrieve value and mark as most recently used (MRU)
                value = cache[key]
                cache.move_to_end(key)
                results.append(value)
            else:
                # Key not found in cache
                results.append(None)
        else:
            raise ValueError(f"Unknown operation type: {op_type}. Expected 'get' or 'put'.")

    return results

# add this ad the end of the file
EXPORT_FUNCTION = lru_cache_simulator