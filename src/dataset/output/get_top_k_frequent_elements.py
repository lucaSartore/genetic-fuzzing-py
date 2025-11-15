import collections
import heapq
from typing import List, Any, Hashable

def get_top_k_frequent_elements(items: List[Hashable], k: int) -> List[Hashable]:
    """
    Returns the 'k' most frequent elements from a list.

    This function utilizes 'collections.Counter' to efficiently count the frequency
    of each element and 'heapq.nlargest' to retrieve the 'k' elements with the
    highest frequencies.

    Args:
        items: A list of hashable elements from which to find the most frequent ones.
               Elements must be hashable because collections.Counter requires them
               as dictionary keys.
        k: The number of most frequent elements to return. Must be a non-negative integer.

    Returns:
        A list containing the 'k' most frequent elements. The order of elements with
        the same frequency is stable but not strictly defined by frequency alone.
        If 'k' is greater than the number of unique elements, all unique elements
        will be returned. If 'k' is 0, an empty list is returned.

    Raises:
        ValueError: If 'k' is a negative integer.
        TypeError: If 'k' is not an integer.
    """
    if not isinstance(k, int):
        raise TypeError("k must be an integer.")
    if k < 0:
        raise ValueError("k must be a non-negative integer.")

    # 1. Count the frequency of each element in the list
    # collections.Counter returns a dictionary-like object mapping elements to their counts.
    item_counts = collections.Counter(items)

    # 2. Use heapq.nlargest to find the 'k' elements with the highest frequencies.
    #    item_counts.items() yields (element, count) pairs.
    #    The 'key' argument tells nlargest to compare based on the count (the second item in the pair).
    #    This returns a list of (element, count) tuples for the k most frequent items.
    top_k_pairs = heapq.nlargest(k, item_counts.items(), key=lambda item_pair: item_pair[1])

    # 3. Extract just the elements from the (element, count) pairs
    #    We iterate through the top_k_pairs and take only the element part (the first item).
    result_elements = [element for element, _ in top_k_pairs]

    return result_elements

EXPORT_FUNCTION = get_top_k_frequent_elements