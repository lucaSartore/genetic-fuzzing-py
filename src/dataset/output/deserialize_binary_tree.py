# necessary imports (use only the python standard libraries)
# No special imports are needed for a basic tree node and string manipulation.
# For type hinting, 'typing' module is standard if Union or Optional are used.
# For Python 3.10+, 'Type | None' is sufficient without 'typing'.

# you can define other auxiliary functions

class TreeNode:
    """
    Represents a node in a binary tree.
    """
    def __init__(self, val: int = 0, left: 'TreeNode' | None = None, right: 'TreeNode' | None = None):
        """
        Initializes a new TreeNode.

        Args:
            val: The value of the node.
            left: The left child node.
            right: The right child node.
        """
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """
        Returns a string representation of the TreeNode for debugging purposes.
        """
        left_val = self.left.val if self.left else 'null'
        right_val = self.right.val if self.right else 'null'
        return f"TreeNode(val={self.val}, left={left_val}, right={right_val})"

def deserialize_binary_tree(data: str) -> TreeNode | None:
    """
    Deserializes a string back into a (simulated) binary tree.

    The input string `data` is assumed to be a comma-separated string
    representing a pre-order traversal of the binary tree.
    'null' is used to represent empty children/nodes.
    Node values are assumed to be integers.

    Example serialization format:
    For a tree:
          1
         / \
        2   3
           / \
          4   5
    The string representation would be: "1,2,null,null,3,4,null,null,5,null,null"

    An empty tree is represented as: "null"

    Args:
        data: A string representation of the binary tree.

    Returns:
        The root node of the deserialized binary tree, or None if the input
        represents an empty tree ("null").
    
    Raises:
        ValueError: If a node value in the string cannot be converted to an integer,
                    or if the input string is malformed (e.g., empty string, non-integer value).
    """
    # Helper function to recursively build the tree
    def _deserialize_helper(nodes_iter):
        """
        Recursive helper to consume values from the iterator and build tree nodes.
        It uses a pre-order traversal logic.
        """
        try:
            val_str = next(nodes_iter)
        except StopIteration:
            # This case means the iterator ran out of elements unexpectedly.
            # In a well-formed pre-order serialization with explicit 'null' markers,
            # this should ideally not be reached before an explicit 'null' is found.
            # However, if the input is truncated, this correctly signifies no node.
            return None

        if val_str == "null":
            return None
        
        try:
            node_val = int(val_str)
        except ValueError:
            # Catches cases where a non-null string cannot be converted to an integer.
            raise ValueError(f"Invalid node value: '{val_str}'. Expected 'null' or an integer.")

        # Create the current node
        node = TreeNode(node_val)
        
        # Recursively build the left child
        node.left = _deserialize_helper(nodes_iter)
        
        # Recursively build the right child
        node.right = _deserialize_helper(nodes_iter)
        
        return node

    # Split the input string into a list of values using comma as delimiter.
    # For an empty string input, data.split(',') will return [''],
    # which will then raise a ValueError for int('').
    values = data.split(',')
    
    # Create an iterator for the values list.
    # Using an iterator simplifies the recursive calls as `next()` automatically advances
    # the position in the list, avoiding manual index management.
    nodes_iterator = iter(values)
    
    # Start the recursive deserialization from the root
    return _deserialize_helper(nodes_iterator)

# add this ad the end of the file
EXPORT_FUNCTION = deserialize_binary_tree