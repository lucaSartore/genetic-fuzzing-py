# necessary imports (use only the python standard libraries)
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Any, Dict, List, Union

# you can define other auxiliary functions

def _build_element(parent_element: ET.Element, data: Any, tag: str = None):
    """
    Recursively builds XML elements from dictionary or list data.

    Args:
        parent_element: The current parent ElementTree element to attach new elements to.
        data: The dictionary, list, or primitive value to convert into XML.
        tag: The XML tag name to use for the current `data` if it represents an element.
             If `data` is a dictionary and `tag` is None, its keys will be direct children
             of `parent_element`.
    """
    if isinstance(data, dict):
        # Determine the current element. If a tag is provided, it's a sub-element.
        # Otherwise, the parent_element itself is the current element (for the root call
        # when processing the top-level dict's content).
        current_element = ET.SubElement(parent_element, tag) if tag else parent_element
        
        for key, value in data.items():
            _build_element(current_element, value, key)
    
    elif isinstance(data, list):
        # If it's a list, we create a wrapper element with the list's key (tag).
        # Then, each item in the list becomes a child of this wrapper.
        # This assumes 'tag' is provided and is the name for the list container.
        if tag is None:
            # This case should ideally not happen if lists are always values of dict keys.
            # If it does, we raise an error as it implies a malformed structure for this converter.
            raise ValueError("A list must be associated with a dictionary key to form an XML element.")
            
        # Create a single wrapper element for the list
        list_wrapper_element = ET.SubElement(parent_element, tag)
        
        # Iterate through the list items
        for item in data:
            if isinstance(item, dict):
                # If item is a dict, its keys become child elements of the list_wrapper_element.
                # No tag is passed for the dict itself, so its keys will be direct children.
                _build_element(list_wrapper_element, item)
            elif isinstance(item, list):
                # Nested list - treat as a list within the current wrapper.
                # Create a generic 'item' tag for inner lists of primitives.
                _build_element(list_wrapper_element, item, tag="item")
            else:
                # Primitive type in a list. Create an element with a generic tag (e.g., "item")
                # and set its text.
                ET.SubElement(list_wrapper_element, "item").text = str(item) if item is not None else ""
    
    else:
        # Primitive type (str, int, float, bool, None).
        # If a tag is provided, create a sub-element and set its text.
        # If no tag (e.g., top-level primitive or root dict content), set parent_element's text.
        if tag:
            ET.SubElement(parent_element, tag).text = str(data) if data is not None else ""
        else:
            parent_element.text = str(data) if data is not None else ""

def _prettify_xml(element: ET.Element) -> str:
    """
    Helper function to pretty-print an ElementTree element.
    """
    rough_string = ET.tostring(element, 'utf-8')
    reparsed_document = minidom.parseString(rough_string)
    return reparsed_document.toprettyxml(indent="  ")


def build_xml_from_dict(data: Dict[str, Any], root_element_name: str = "root") -> str:
    """
    Converts a nested dictionary into an XML string.

    This function transforms a Python dictionary structure into a well-formed XML string.
    Keys in the dictionary become XML element tags, and values become either
    text content or nested elements.

    Rules for conversion:
    - Dictionary keys become XML element tags.
    - String, number, boolean, or None values become text content of their respective tags.
    - Nested dictionaries become nested XML elements.
    - Lists of dictionaries or primitives under a key will create a single wrapper element
      named after the key, and each item in the list will be a child of this wrapper.
      - For dictionaries within a list, their keys will be direct children of the wrapper.
      - For primitives within a list, each will be wrapped in a generic `<item>` tag.

    Args:
        data: The nested dictionary to convert.
              If the dictionary has a single top-level key whose value is
              another dictionary or a list, that key will be used as the
              root XML element name, overriding `root_element_name`.
              Otherwise (e.g., multiple top-level keys, or a single primitive
              value for the only key), `root_element_name` will be used
              as the enclosing root, and the dictionary's top-level keys
              will be its children.
        root_element_name: The default name for the root XML element. This is used
                           if the input dictionary doesn't naturally provide a single
                           top-level key to serve as the root. Defaults to "root".

    Returns:
        An XML string representing the dictionary structure, pretty-printed with 2-space indentation.

    Raises:
        TypeError: If the input 'data' is not a dictionary.
        ValueError: If a list is encountered without an associated dictionary key (should not
                    happen with typical dictionary inputs following the expected structure).
    """
    if not isinstance(data, dict):
        raise TypeError("Input 'data' must be a dictionary.")

    root: ET.Element
    
    if len(data) == 1:
        single_key = list(data.keys())[0]
        single_value = list(data.values())[0]
        
        # If the dictionary has only one key and its value is a complex type (dict or list),
        # use that key as the root element name directly, and build XML from its value.
        if isinstance(single_value, (dict, list)):
            root = ET.Element(single_key)
            _build_element(root, single_value)
        else:
            # Handle cases like `{"user": "Alice"}` where the single key has a primitive value.
            # In this scenario, `root_element_name` wraps the single key-value pair.
            root = ET.Element(root_element_name)
            _build_element(root, data)
    else:
        # Handle cases with multiple top-level keys (e.g., `{"name": "Bob", "age": 30}`).
        # `root_element_name` wraps all top-level key-value pairs.
        root = ET.Element(root_element_name)
        _build_element(root, data)
    
    return _prettify_xml(root)

# add this ad the end of the file
EXPORT_FUNCTION = build_xml_from_dict