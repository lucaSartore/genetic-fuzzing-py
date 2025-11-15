from typing import Dict, List, Tuple, Hashable, Union
import heapq

def dijkstra_shortest_path(
    graph: Dict[Hashable, Dict[Hashable, int]],
    start_node: Hashable,
    end_node: Hashable
) -> Tuple[List[Hashable], float]:
    """
    Finds the shortest path in a weighted graph using Dijkstra's algorithm.

    The graph is represented as a dictionary of dictionaries, where the outer dictionary
    keys are nodes, and the inner dictionaries represent neighbors and the weights
    of the edges to those neighbors. Edge weights are assumed to be non-negative.

    Args:
        graph: A dictionary representing the weighted graph.
               Example: {'A': {'B': 1, 'C': 4}, 'B': {'A': 1, 'C': 2}, 'C': {'B': 2}}
               Nodes can be any hashable type (e.g., str, int, tuple).
               Weights must be non-negative integers.
        start_node: The starting node for the path.
        end_node: The target node for the path.

    Returns:
        A tuple containing:
            - A list of nodes representing the shortest path from start_node to end_node.
              If no path exists, an empty list is returned.
            - The total weight (cost) of the shortest path. If no path exists,
              float('inf') is returned for the weight.

    Raises:
        ValueError: If the start_node or end_node is not found in the graph.
    """

    if start_node not in graph:
        raise ValueError(f"Start node '{start_node}' not found in the graph.")
    if end_node not in graph:
        raise ValueError(f"End node '{end_node}' not found in the graph.")

    # Initialize distances: store the shortest distance found so far from start_node to each node
    # All distances are initially infinity, except for the start_node which is 0.
    distances: Dict[Hashable, float] = {node: float('inf') for node in graph}
    distances[start_node] = 0.0

    # Initialize predecessors: store the predecessor of each node in the shortest path found so far.
    # This is used to reconstruct the path later.
    predecessors: Dict[Hashable, Union[Hashable, None]] = {node: None for node in graph}

    # Priority queue: a min-heap to store tuples of (distance, node).
    # The heap automatically orders elements by the first item (distance), ensuring we always
    # process the node with the smallest known distance first.
    priority_queue: List[Tuple[float, Hashable]] = [(0.0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we have already found a shorter path to current_node than this entry, skip.
        # This handles "stale" entries in the priority queue.
        if current_distance > distances[current_node]:
            continue

        # Optimization: If we've found the shortest path to the end_node, we can stop.
        # Dijkstra's guarantees that when a node is popped from the priority queue,
        # its distance is the shortest possible distance from the start_node.
        if current_node == end_node:
            break

        # Explore neighbors of the current_node
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # If a shorter path to the neighbor is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruct the path from end_node back to start_node using the predecessors dictionary.
    path: List[Hashable] = []
    current_path_node = end_node

    # If the end_node was not reachable from the start_node, its distance will remain infinity.
    if distances[end_node] == float('inf'):
        return [], float('inf')

    # Trace back the path from the end_node to the start_node
    while current_path_node is not None:
        path.append(current_path_node)
        if current_path_node == start_node:
            break
        current_path_node = predecessors[current_path_node]
    
    # The path was built in reverse, so reverse it to get the correct order.
    path.reverse()

    return path, distances[end_node]

EXPORT_FUNCTION = dijkstra_shortest_path