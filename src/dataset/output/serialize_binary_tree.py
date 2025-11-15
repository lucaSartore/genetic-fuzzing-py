# necessary imports (use only the python standard libraries)
from typing import Any, List, Union, Dict, Optional

# Define markers for serialization
# NODE_NULL_MARKER represents a non-existent node (e.g., a null child reference).
NODE_NULL_MARKER = "#"
# VALUE_NONE_MARKER represents a node whose actual value is None.
VALUE_NONE_MARKER = "None_Val"


def _get_node_components(node: Any) -> tuple[Any, Any, Any]:
    """
    Auxiliary function to extract value, left child, and right child from a node.

    This function handles nodes represented as dictionaries or arbitrary objects.
    - If a node is `None`, it signifies a null node.
    - If a node is a dictionary, it expects 'value', 'left', 'right' keys.
      Missing 'left' or 'right' keys are treated as `None` children.
      Missing 'value' is treated as `None`.
    - If a node is an object, it attempts to access 'value', 'left', 'right' attributes.
      Missing 'left' or 'right' attributes are treated as `None` children.
      If the 'value' attribute is missing, the object itself is considered the node's value.

    Args:
        node (Any): The node from which to extract components.

    Returns:
        tuple[Any, Any, Any]: A tuple containing (value, left_child, right_child).
                              If the node is None, returns (None, None, None).
    """
    if node is None:
        return None, None, None

    value: Any
    left_child: Any = None
    right_child: Any = None

    if isinstance(node, dict):
        value = node.get('value')
        left_child = node.get('left')
        right_child = node.get('right')
    else:
        # Assume it's an object. Check for standard tree node attributes.
        if hasattr(node, 'value'):
            value = getattr(node, 'value')
        else:
            # If no 'value' attribute, the object itself is considered the value.
            # This covers simple objects like integers, strings, etc., acting as nodes.
            value = node

        left_child = getattr(node, 'left', None)
        right_child = getattr(node, 'right', None)

    return value, left_child, right_child


def serialize_binary_tree(root: Any) -> str:
    """
    Serializes a (simulated) binary tree to a string using pre-order traversal.

    Nodes can be dictionaries or objects.
    - If a node is `None`, it signifies a null child and is serialized as
      `NODE_NULL_MARKER` ("#").
    - If a node is a dictionary, it expects 'value', 'left', 'right' keys.
      Missing 'left' or 'right' keys are treated as `None` children.
      Missing 'value' is treated as `None`.
    - If a node is an object, it expects 'value', 'left', 'right' attributes.
      Missing 'left' or 'right' attributes are treated as `None` children.
      If the 'value' attribute is missing, the object itself is considered
      the node's value.

    The serialized string represents a pre-order traversal, with values
    separated by commas. A node whose value is explicitly `None` is
    serialized as `VALUE_NONE_MARKER` ("None_Val") to distinguish it from
    a non-existent node.

    Args:
        root (Any): The root of the binary tree. This can be a dict, an object
                    representing a node, or `None` if the tree is empty.

    Returns:
        str: The serialized string representation of the binary tree.

    Example:
        # Define a simple class for demonstration purposes
        class TreeNode:
            def __init__(self, val: Any, left: Any = None, right: Any = None):
                self.value = val
                self.left = left
                self.right = right
            def __repr__(self) -> str:
                return f"TreeNode({self.value})"

        # Example 1: Tree using TreeNode objects
        # Tree structure:
        #        1
        #       / \
        #      2   3
        #     /   / \
        #    4   5   6
        tree_obj = TreeNode(1,
                            TreeNode(2, TreeNode(4)),
                            TreeNode(3, TreeNode(5), TreeNode(6)))
        # Expected output: "1,2,4,#,#,#,3,5,#,#,6,#,#"
        # print(serialize_binary_tree(tree_obj))

        # Example 2: Tree using dictionaries
        tree_dict = {
            'value': 1,
            'left': {
                'value': 2,
                'left': {'value': 4},
                'right': None
            },
            'right': {
                'value': 3,
                'left': {'value': 5},
                'right': {'value': 6}
            }
        }
        # Expected output: "1,2,4,#,#,#,3,5,#,#,6,#,#"
        # print(serialize_binary_tree(tree_dict))

        # Example 3: Tree with a None value and a simple integer node
        # Tree structure:
        #         'A'
        #         / \
        #   (Node with value None)  100 (simple int node)
        tree_mixed_none_val = {
            'value': 'A',
            'left': {'value': None}, # Node with value None
            'right': 100            # Simple integer treated as a leaf node
        }
        # Expected output: "A,None_Val,#,#,100,#,#"
        # print(serialize_binary_tree(tree_mixed_none_val))

        # Example 4: Empty tree
        # Expected output: "#"
        # print(serialize_binary_tree(None))

        # Example 5: Single node tree (simple object)
        # Expected output: "hello,#,#"
        # print(serialize_binary_tree("hello"))
    """
    serialized_parts: List[str] = []

    def _traverse(node: Any) -> None:
        """
        Performs a recursive pre-order traversal to build the serialized string parts.
        """
        if node is None:
            serialized_parts.append(NODE_NULL_MARKER)
            return

        value, left_child, right_child = _get_node_components(node)

        # Convert value to string. Use VALUE_NONE_MARKER if the actual value is None.
        if value is None:
            serialized_parts.append(VALUE_NONE_MARKER)
        else:
            serialized_parts.append(str(value))

        _traverse(left_child)
        _traverse(right_child)

    _traverse(root)
    return ",".join(serialized_parts)

# add this ad the end of the file
EXPORT_FUNCTION = serialize_binary_tree