# necessary imports (use only the python standard libraries)
import xml.etree.ElementTree as ET
from typing import List

# you can define other auxiliary functions

def xpath_search_xml(xml_string: str, xpath_expression: str) -> List[ET.Element]:
    """
    Parses an XML string and performs a simple XPath search using ElementTree.

    ElementTree's XPath support is a subset of the full XPath 1.0 specification.
    It generally supports:
    - Tag names (e.g., "tag")
    - Child paths (e.g., "parent/child")
    - Relative paths (e.g., "./child")
    - Descendant paths (e.g., ".//grandchild", "//tag")
    - Attribute filtering (e.g., "tag[@attribute='value']", "tag[@attribute]")
    - Position filtering (e.g., "tag[1]", "tag[last()]")
    - 'or' and 'and' conditions within attribute predicates (e.g., "tag[@a='x' or @b='y']")

    It does NOT support more advanced XPath features like:
    - Axes (following-sibling, preceding-sibling, ancestor, etc.) beyond child and descendant.
    - Text node selection with `text()`
    - Complex boolean logic outside of attribute predicates.
    - XPath functions beyond basic position() and last().

    Args:
        xml_string: The XML content as a string.
        xpath_expression: The XPath expression to search for.

    Returns:
        A list of `xml.etree.ElementTree.Element` objects that match the
        XPath expression. Returns an empty list if no elements match.

    Raises:
        xml.etree.ElementTree.ParseError: If the `xml_string` is not well-formed XML.
        TypeError: If `xml_string` or `xpath_expression` are not strings.
    """
    if not isinstance(xml_string, str):
        raise TypeError("xml_string must be a string.")
    if not isinstance(xpath_expression, str):
        raise TypeError("xpath_expression must be a string.")

    # Parse the XML string into an ElementTree root element
    # This will raise ParseError if the XML is malformed
    root: ET.Element = ET.fromstring(xml_string)

    # Perform the XPath search using ElementTree's findall method
    # findall returns a list of all matching subelements, in document order.
    results: List[ET.Element] = root.findall(xpath_expression)

    return results

# add this ad the end of the file
EXPORT_FUNCTION = xpath_search_xml