from typing import List
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

def parse_xml_and_find_elements(xml_string: str, tag_name: str) -> List[Element]:
    """
    Parses an XML string and finds all elements with a given tag.

    Args:
        xml_string: The XML content as a string.
        tag_name: The name of the tag to search for.

    Returns:
        A list of xml.etree.ElementTree.Element objects matching the given tag_name.
        Returns an empty list if no elements are found or if the XML string is invalid.
    """
    try:
        # Parse the XML string into an ElementTree object
        root = ET.fromstring(xml_string)

        # Find all elements with the specified tag name
        # The findall() method returns a list of all subelements matching the tag name.
        # It searches the entire subtree, not just immediate children.
        found_elements = root.findall(f".//{tag_name}")

        return found_elements
    except ET.ParseError:
        # Handle cases where the XML string is malformed or invalid
        print("Error: Invalid XML string provided.")
        return []
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return []

EXPORT_FUNCTION = parse_xml_and_find_elements