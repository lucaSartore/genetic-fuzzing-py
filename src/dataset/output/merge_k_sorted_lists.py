import heapq
from typing import List

def merge_k_sorted_lists(lists: List[List[int]]) -> List[int]:
    """
    Merges 'k' sorted lists into one sorted list using a min-heap (priority queue).

    This function efficiently combines multiple sorted lists into a single sorted list.
    It leverages the `heapq` module to maintain a min-heap of the smallest elements
    currently available from all input lists.

    Args:
        lists: A list of 'k' sorted lists. Each inner list is assumed to be
               sorted in non-decreasing order.

    Returns:
        A single sorted list containing all elements from the input lists
        in non-decreasing order.

    Example:
        >>> merge_k_sorted_lists([[1, 4, 5], [1, 3, 4], [2, 6]])
        [1, 1, 2, 3, 4, 4, 5, 6]
        >>> merge_k_sorted_lists([[], [1], [2, 3]])
        [1, 2, 3]
        >>> merge_k_sorted_lists([])
        []
    """
    min_heap: List[tuple[int, int, int]] = []  # Stores (value, list_index, element_index_in_list)
    result: List[int] = []

    # Initialize the min-heap with the first element from each non-empty list
    for i, lst in enumerate(lists):
        if lst:  # Only add if the list is not empty
            heapq.heappush(min_heap, (lst[0], i, 0))

    # While the heap is not empty, extract the smallest element and add the next
    # element from its respective list
    while min_heap:
        val, list_idx, elem_idx = heapq.heappop(min_heap)
        result.append(val)

        # If there are more elements in the list from which 'val' was taken,
        # add the next element to the heap
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, list_idx, elem_idx + 1))

    return result

EXPORT_FUNCTION = merge_k_sorted_lists