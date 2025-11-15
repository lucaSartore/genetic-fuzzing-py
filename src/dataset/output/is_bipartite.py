import collections
from typing import Dict, List, Deque, Any

def is_bipartite(graph: Dict[Any, List[Any]]) -> bool:
    """
    Checks if a graph (as an adjacency list) is bipartite.

    A graph is bipartite if its vertices can be divided into two disjoint
    and independent sets, U and V, such that every edge connects a vertex
    in U to one in V. There are no edges within U or within V.

    This function uses a Breadth-First Search (BFS) based coloring algorithm.
    It attempts to color the graph with two colors (0 and 1) such that no
    adjacent vertices have the same color. If such a coloring is possible,
    the graph is bipartite.

    Args:
        graph: An adjacency list representation of the graph.
               The keys of the dictionary are nodes, and the values are
               lists of their direct neighbors. Nodes can be of any hashable type.
               Example: {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}

    Returns:
        True if the graph is bipartite, False otherwise.
    """
    
    # Store the color assigned to each node.
    # -1: uncolored, 0: color A, 1: color B
    colors: Dict[Any, int] = {}

    # Iterate over all nodes in the graph. This handles disconnected graphs,
    # ensuring each connected component is checked.
    for node in graph:
        if node not in colors:
            # If the node hasn't been colored, start a BFS from it.
            # Assign it an initial color (e.g., 0).
            colors[node] = 0
            queue: Deque[Any] = collections.deque([node])

            while queue:
                current_node = queue.popleft()
                current_color = colors[current_node]

                # Check all neighbors of the current_node
                for neighbor in graph.get(current_node, []): # Use .get to handle nodes that might exist as keys but have empty lists
                    if neighbor not in colors:
                        # If the neighbor is uncolored, color it with the opposite color
                        colors[neighbor] = 1 - current_color
                        queue.append(neighbor)
                    elif colors[neighbor] == current_color:
                        # If the neighbor has the same color, the graph is not bipartite
                        return False
                    # If colors[neighbor] is different, it's consistent; do nothing.
    
    # If the BFS completes for all connected components without conflicts,
    # the graph is bipartite.
    return True

# add this ad the end of the file
EXPORT_FUNCTION = is_bipartite