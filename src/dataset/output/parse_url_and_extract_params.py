# necessary imports (use only the python standard libraries)
from urllib.parse import urlparse, parse_qs
from typing import Dict, List

# you can define other auxiliary functions

def parse_url_and_extract_params(url: str) -> Dict[str, List[str]]:
    """
    Uses 'urlparse' and 'parse_qs' to extract query parameters from a URL.

    This function takes a URL string, parses it using urlparse to separate
    its components, then extracts the query string. Finally, it uses parse_qs
    to parse the query string into a dictionary of parameters.

    Args:
        url (str): The URL string from which to extract query parameters.

    Returns:
        Dict[str, List[str]]: A dictionary where keys are parameter names
                               (str) and values are lists of strings (List[str])
                               representing the values for each parameter.
                               If a parameter appears multiple times, its values
                               will all be included in the corresponding list.
                               Returns an empty dictionary if no query
                               parameters are found in the URL.
    """
    # Parse the URL into its components
    parsed_url = urlparse(url)

    # Extract the query string part
    query_string = parsed_url.query

    # Parse the query string into a dictionary of parameters
    # parse_qs returns a dictionary where values are lists of strings,
    # even if there's only one value for a parameter.
    query_parameters = parse_qs(query_string)

    return query_parameters

# add this ad the end of the file
EXPORT_FUNCTION = parse_url_and_extract_params