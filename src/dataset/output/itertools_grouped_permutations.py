import itertools
from typing import Iterable, Dict, List, Tuple, TypeVar

# Define a generic type for the elements in 'items'
T = TypeVar('T')

def itertools_grouped_permutations(items: Iterable[T], r: int) -> Dict[T, List[Tuple[T, ...]]]:
    """
    Generates 'r'-length permutations of 'items' and groups them by their first element.

    Args:
        items: An iterable of elements from which to generate permutations.
        r: The length of the permutations to generate.

    Returns:
        A dictionary where keys are the first elements of the permutations,
        and values are lists of all 'r'-length permutations that start with that element.
        The order of permutations within each list is based on the iteration order
        of itertools.permutations and subsequent sorting.

    Raises:
        ValueError: If r is negative. (itertools.permutations handles r > len(items) by returning an empty iterator)
        IndexError: If r is 0 and items is not empty (accessing p[0] would fail).
                    However, permutations of length 0 would result in `()` tuples,
                    which cannot be indexed by `[0]`.
                    The `key=lambda p: p[0]` would fail for `r=0`.
                    A common practice is to assume r >= 1 for grouping by first element.
                    Let's add a check for r=0.
    """
    if r < 0:
        raise ValueError("r must be a non-negative integer.")
    if r == 0:
        # Permutations of length 0 result in a single empty tuple '()'.
        # Grouping by the first element of '()' is not possible.
        # Returning an empty dictionary is consistent as no element can be a key.
        return {}

    # 1. Generate all r-length permutations using itertools.permutations
    # This returns an iterator of tuples.
    all_permutations = itertools.permutations(items, r)

    # 2. Convert the permutations to a list and sort them.
    # itertools.groupby requires the input iterable to be sorted by the key
    # that will be used for grouping. In this case, the key is the first element (p[0]).
    # We materialize the iterator to a list before sorting to ensure it's iterable multiple times
    # and to provide a stable input for sorting.
    permutations_list: List[Tuple[T, ...]] = sorted(list(all_permutations), key=lambda p: p[0])

    # 3. Group the sorted permutations by their first element using itertools.groupby
    grouped_result: Dict[T, List[Tuple[T, ...]]] = {}
    for key, group_iterator in itertools.groupby(permutations_list, key=lambda p: p[0]):
        # Consume the group_iterator into a list and store it in the dictionary.
        grouped_result[key] = list(group_iterator)

    return grouped_result


EXPORT_FUNCTION = itertools_grouped_permutations