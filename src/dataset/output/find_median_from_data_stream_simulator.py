# necessary imports (use only the python standard libraries)
import heapq
from typing import List, Union

def find_median_from_data_stream_simulator(numbers: List[Union[int, float]]) -> List[float]:
    """
    Simulates adding numbers from a data stream and finds the median after each addition.
    It uses two heaps (a min-heap and a max-heap) to maintain the two halves of the numbers
    processed so far, ensuring efficient median calculation.

    The max-heap stores the smaller half of the numbers (negated, because Python's heapq
    is a min-heap), and the min-heap stores the larger half.

    Args:
        numbers: A list of integers or floats representing the data stream.

    Returns:
        A list of floats, where each element is the median of the numbers
        processed up to that point in the stream.
    """
    max_heap: List[Union[int, float]] = []  # Stores the smaller half (as negated values to simulate max-heap)
    min_heap: List[Union[int, float]] = []  # Stores the larger half
    medians: List[float] = []

    for num in numbers:
        # Step 1: Add the number to the appropriate heap
        # If max_heap is empty or num is less than or equal to the largest element in max_heap
        # (which is -max_heap[0]), push it to max_heap.
        if not max_heap or num <= -max_heap[0]:
            heapq.heappush(max_heap, -num)
        else:
            heapq.heappush(min_heap, num)

        # Step 2: Balance the heaps
        # Ensure max_heap size is equal to or one greater than min_heap size
        # (to correctly handle odd/even number of elements, keeping the median in max_heap's root for odd count)
        if len(max_heap) > len(min_heap) + 1:
            # Move largest element from max_heap to min_heap
            heapq.heappush(min_heap, -heapq.heappop(max_heap))
        elif len(min_heap) > len(max_heap):
            # Move smallest element from min_heap to max_heap
            heapq.heappush(max_heap, -heapq.heappop(min_heap))

        # Step 3: Calculate the median
        if len(max_heap) == len(min_heap):
            # Even number of elements: median is the average of the two middle elements
            median = (-max_heap[0] + min_heap[0]) / 2.0
        else:
            # Odd number of elements: median is the largest element in max_heap
            median = -max_heap[0]
        
        medians.append(median)

    return medians

# add this ad the end of the file
EXPORT_FUNCTION = find_median_from_data_stream_simulator