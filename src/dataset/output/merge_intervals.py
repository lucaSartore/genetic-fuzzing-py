# necessary imports (use only the python standard libraries)
from typing import List

# you can define other auxiliary functions

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merges a list of overlapping intervals.

    Args:
        intervals: A list of intervals, where each interval is a list of two
                   integers [start, end].
                   Example: [[1,3],[2,6],[8,10],[15,18]]

    Returns:
        A new list of non-overlapping intervals, merged where necessary.
        The intervals are sorted by their start times.
        Example: [[1,6],[8,10],[15,18]]
    """
    if not intervals:
        return []

    # Sort the intervals based on their start times.
    # This is crucial for the merging logic to work correctly.
    intervals.sort(key=lambda x: x[0])

    merged = []
    # Add the first interval to the merged list to start comparison
    merged.append(intervals[0])

    for current_interval in intervals[1:]:
        # Get the last interval added to our merged list
        last_merged_interval = merged[-1]

        # Check for overlap:
        # If the current interval's start time is less than or equal to the
        # end time of the last merged interval, then there's an overlap.
        if current_interval[0] <= last_merged_interval[1]:
            # Merge by updating the end time of the last merged interval
            # to be the maximum of its current end and the current interval's end.
            last_merged_interval[1] = max(last_merged_interval[1], current_interval[1])
        else:
            # No overlap, so add the current interval as a new distinct interval
            merged.append(current_interval)
            
    return merged

# add this ad the end of the file
EXPORT_FUNCTION = merge_intervals