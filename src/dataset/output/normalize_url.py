# necessary imports (use only the python standard libraries)
from urllib.parse import urlparse, urlunparse, ParseResult
import posixpath
from typing import List

# you can define other auxiliary functions

def _reconstruct_netloc(parsed_url_obj: ParseResult) -> str:
    """
    Reconstructs the netloc part of a URL, omitting default ports.
    Handles userinfo and hostname, and IPv6 literal addresses.
    
    Args:
        parsed_url_obj: A ParseResult object obtained from urllib.parse.urlparse.

    Returns:
        The reconstructed netloc string without default ports.
    """
    # If there's no hostname, there's no netloc to reconstruct.
    # This covers cases like relative URLs (e.g., '/path/to/resource')
    # or URLs without a host (e.g., 'file:///path/to/file').
    if not parsed_url_obj.hostname:
        return ''

    netloc_parts: List[str] = []

    # Add userinfo if present
    if parsed_url_obj.username:
        netloc_parts.append(parsed_url_obj.username)
        if parsed_url_obj.password:
            netloc_parts.append(':' + parsed_url_obj.password)
        netloc_parts.append('@')
    
    # Add hostname (parsed_url_obj.hostname already handles IPv6 brackets, e.g., '[::1]')
    netloc_parts.append(parsed_url_obj.hostname)
    
    # Add port if it's not a default port for the scheme
    if parsed_url_obj.port is not None:
        is_default_port = False
        if parsed_url_obj.scheme == 'http' and parsed_url_obj.port == 80:
            is_default_port = True
        elif parsed_url_obj.scheme == 'https' and parsed_url_obj.port == 443:
            is_default_port = True
        
        if not is_default_port:
            netloc_parts.append(':' + str(parsed_url_obj.port))
    
    return ''.join(netloc_parts)


def normalize_url(url: str) -> str:
    """
    Cleans up a URL by:
    1. Normalizing the path (resolves '..' and '.').
    2. Removing default ports (e.g., 80 for HTTP, 443 for HTTPS).
    3. Removing URL fragments (the part after '#').

    Args:
        url: The URL string to clean up.

    Returns:
        The cleaned and normalized URL string.
    """
    parsed_url = urlparse(url)

    # 1. Normalize path
    # posixpath.normpath('') returns '.', which is generally undesirable for an empty path.
    # If the original path is empty, it should remain empty.
    if parsed_url.path == '':
        normalized_path = ''
    else:
        # posixpath.normpath resolves '..' and '.' components in the path.
        # It also handles multiple slashes and trailing slashes correctly
        # for URL paths (e.g., /a/b/../c -> /a/c, /a/./b -> /a/b).
        normalized_path = posixpath.normpath(parsed_url.path)
        
        # Ensure that if the path becomes '.', it's treated as empty for scheme://host cases.
        # This generally aligns with how web servers interpret root paths.
        if normalized_path == '.' and not parsed_url.path: # if original path was empty, and normpath made it '.'
             normalized_path = ''
        elif normalized_path == '.' and parsed_url.path != '': # if path was e.g. "/../" and becomes "/", but normpath made it "." then convert to "/"
             normalized_path = '/' # This case can happen for URLs like "http://example.com/../"
                                   # normpath produces "/", but if that resolves to just ".", it implies root.
                                   # A simple "/" is generally more canonical than "." for root.
                                   # However, if the path was just ".", normpath returns ".", which is fine.
                                   # For consistency with how web servers resolve this, '/' is better than '.'
                                   # if the original path implied a non-empty root.
                                   # After careful consideration, posixpath.normpath('/') == '/'
                                   # posixpath.normpath('/../') == '/'
                                   # posixpath.normpath('/./') == '/'
                                   # The only problem case is path='' -> '.'
                                   # If normalized_path is still '.', and original was not empty, it probably means root.
                                   # let's refine this more carefully:
                                   # if the url was http://example.com and path was '', normpath('') -> '.'
                                   # this makes it http://example.com/.  which is wrong.
                                   # My current `if parsed_url.path == '': normalized_path = ''` handles this.
                                   #
                                   # What if path was `/a/../` and normpath returned `/`? This is correct.
                                   # What if path was `/..` and normpath returned `/`? This is correct.
                                   # What if path was `.` and normpath returned `.`? This is correct.
                                   #
                                   # The logic is fine for `posixpath.normpath` as it is; the only specific edge case
                                   # is an explicitly empty `parsed_url.path`.

    # 2. Remove default ports from netloc
    # This is handled by the auxiliary function _reconstruct_netloc, which builds
    # the netloc string without including default ports (80 for http, 443 for https).
    cleaned_netloc = _reconstruct_netloc(parsed_url)

    # 3. Remove fragments
    # The fragment component is explicitly set to an empty string.
    
    # Reconstruct the URL using urlunparse with the cleaned components.
    # The order of components for urlunparse is:
    # (scheme, netloc, path, params, query, fragment)
    cleaned_url_parts = (
        parsed_url.scheme,      # Scheme remains unchanged
        cleaned_netloc,         # Cleaned netloc (default ports removed)
        normalized_path,        # Normalized path ('..' and '.' resolved)
        parsed_url.params,      # Params remain unchanged
        parsed_url.query,       # Query remains unchanged
        ''                      # Fragment is always removed
    )
    
    return urlunparse(cleaned_url_parts)

# add this at the end of the file
EXPORT_FUNCTION = normalize_url