# necessary imports (use only the python standard libraries)
from collections import defaultdict
from typing import List, Dict

# you can define other auxiliary functions

def find_itinerary(tickets: List[List[str]]) -> List[str]:
    """
    Reconstructs a flight itinerary from a list of '[from, to]' tickets using graph traversal.

    This function implements Hierholzer's algorithm, which is suitable for finding
    an Eulerian path/circuit in a directed graph. The problem implies that:
    1. A valid itinerary exists.
    2. All tickets must be used exactly once.
    3. The itinerary should start from 'JFK' (a common assumption for this problem type).
    4. If multiple valid itineraries exist, the one with the smallest lexicographical
       order should be returned.

    Args:
        tickets: A list of flight tickets, where each ticket is a list containing
                 two strings: [from_airport_code, to_airport_code].
                 Example: [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]

    Returns:
        A list of strings representing the reconstructed itinerary in sequential order
        from the starting airport to the final destination, using all tickets.
        Example: ["JFK", "MUC", "LHR", "SFO", "SJC"]
    """
    # 1. Build the graph using an adjacency list.
    # We use a defaultdict to simplify adding new airports as keys.
    # The values are lists of destination airports reachable from the key airport.
    graph: Dict[str, List[str]] = defaultdict(list)
    for fr, to in tickets:
        graph[fr].append(to)

    # 2. Sort the destination lists in reverse lexicographical order.
    # This is crucial for satisfying the requirement of finding the
    # lexicographically smallest itinerary. By sorting in reverse,
    # `list.pop()` will retrieve the smallest airport first.
    for fr_airport in graph:
        graph[fr_airport].sort(reverse=True)

    # 3. Initialize the itinerary list and a stack for the iterative DFS traversal.
    # The stack will hold the path currently being explored.
    # The problem typically implies starting from 'JFK'.
    itinerary: List[str] = []
    stack: List[str] = ['JFK']  # Start the traversal from 'JFK'

    # 4. Perform an iterative Depth-First Search (DFS) based on Hierholzer's algorithm.
    # The algorithm works as follows:
    # - It traverses the graph, always trying to pick an available outgoing edge.
    # - When an airport (node) has no more outgoing flights (edges) to explore,
    #   it means we've reached a dead end or completed a segment of the path
    #   that must end at this airport. This airport is then "processed" by
    #   being added to our `itinerary` list.
    # - Since airports are added to `itinerary` *after* all their outgoing edges
    #   have been explored, the `itinerary` will naturally be built in reverse order.
    while stack:
        current_airport = stack[-1]

        # If there are still outgoing flights (unexplored edges) from the current airport
        if graph[current_airport]:
            # Pop the lexicographically smallest destination (due to reverse sorting)
            next_destination = graph[current_airport].pop()
            stack.append(next_destination)
        else:
            # No more outgoing flights from this airport.
            # This airport is a "sink" for the current path segment.
            # Add it to the itinerary (it will be in reverse order initially).
            itinerary.append(stack.pop())

    # 5. Reverse the itinerary to obtain the correct chronological order of flights.
    return itinerary[::-1]

# add this ad the end of the file
EXPORT_FUNCTION = find_itinerary