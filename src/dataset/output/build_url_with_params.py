# necessary imports (use only the python standard libraries)
from urllib.parse import urlencode, urlsplit, urlunsplit
from typing import Any, Mapping

# you can define other auxiliary functions

def build_url_with_params(base_url: str, params: Mapping[str, Any]) -> str:
    """
    Uses 'urlencode' to build a full URL with query parameters.

    This function takes a base URL and a dictionary of parameters,
    encodes the parameters, and appends them as a query string to the URL.
    If the base URL already contains a query string, it will be replaced
    by the new parameters. Any fragment in the base URL will be preserved.

    Args:
        base_url: The base URL string (e.g., "http://example.com/path").
                  Can include existing query parameters or a fragment,
                  but existing query parameters will be overwritten
                  by the ones provided in `params`.
        params: A dictionary of query parameters. Keys are strings, and
                values can be strings, numbers, or iterables (like lists or
                tuples) of strings/numbers. These will be URL-encoded.
                `urlencode` will convert numbers to strings and handle
                iterables by repeating the key (e.g., `{'id': [1, 2]}` becomes `id=1&id=2`).

    Returns:
        A complete URL string with the encoded query parameters.

    Examples:
        >>> build_url_with_params("http://example.com/search", {"q": "python", "page": 1})
        'http://example.com/search?q=python&page=1'

        >>> build_url_with_params("https://api.example.com/data", {"id": [101, 102], "format": "json"})
        'https://api.example.com/data?id=101&id=102&format=json'

        >>> build_url_with_params("http://example.com/path?old=value#fragment", {"new": "param"})
        'http://example.com/path?new=param#fragment'

        >>> build_url_with_params("http://example.com", {})
        'http://example.com'
    """
    # Parse the base URL to separate its components (scheme, netloc, path, query, fragment).
    # This allows us to replace just the query part while preserving other components.
    parsed_url = urlsplit(base_url)

    # Encode the parameters into a query string.
    # doseq=True ensures that if a parameter's value is an iterable (like a list),
    # it is encoded as multiple key=value pairs (e.g., 'id=1&id=2' instead of 'id=[1, 2]').
    encoded_params = urlencode(params, doseq=True)

    # Reconstruct the URL with the new query string.
    # The components are (scheme, netloc, path, query, fragment).
    # We use the original scheme, netloc, path, and fragment,
    # but replace the query with our newly encoded parameters.
    full_url = urlunsplit((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        encoded_params,  # This is the new query string
        parsed_url.fragment
    ))

    return full_url

# add this ad the end of the file
EXPORT_FUNCTION = build_url_with_params