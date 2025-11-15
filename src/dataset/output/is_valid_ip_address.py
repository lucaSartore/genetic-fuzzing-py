# necessary imports (use only the python standard libraries)
# No specific imports are needed from the standard library beyond built-in types and functions.

# you can define other auxiliary functions

def _is_valid_ipv4_segment(segment: str) -> bool:
    """
    Checks if a string segment is a valid part of an IPv4 address.
    A valid segment is a decimal number from 0 to 255, with no leading zeros
    (unless the segment itself is '0').
    """
    if not segment:
        return False
    
    # Check if the segment consists only of digits.
    if not segment.isdigit():
        return False
    
    # Check for leading zeros: '01' is invalid, but '0' is valid.
    if len(segment) > 1 and segment.startswith('0'):
        return False
    
    # Convert to integer and check the range (0-255).
    try:
        num = int(segment)
    except ValueError:
        # This case should ideally not be reached if segment.isdigit() is true,
        # but it's a safeguard against extremely malformed strings.
        return False
    
    return 0 <= num <= 255

def _is_valid_ipv6_segment(segment: str) -> bool:
    """
    Checks if a string segment is a valid part of an IPv6 address.
    A valid segment is 1 to 4 hexadecimal characters.
    """
    if not segment:
        return False
    
    # Segment length must be between 1 and 4 hexadecimal characters.
    if not (1 <= len(segment) <= 4):
        return False
    
    # Check if all characters are valid hexadecimal digits (0-9, a-f, A-F).
    # Trying to convert to an int with base 16 will raise a ValueError
    # if the segment contains non-hexadecimal characters.
    try:
        int(segment, 16)
    except ValueError:
        return False
    
    return True

def is_valid_ip_address(ip_string: str) -> bool:
    """
    Checks if a given string is a valid IPv4 or IPv6 address.

    Args:
        ip_string (str): The string to be validated.

    Returns:
        bool: True if the string is a valid IPv4 or IPv6 address, False otherwise.
    """
    if not isinstance(ip_string, str):
        return False
    if not ip_string:
        return False

    # --- Attempt IPv4 validation ---
    # An IPv4 address must contain at least one dot.
    if '.' in ip_string:
        parts = ip_string.split('.')
        # A valid IPv4 address has exactly 4 parts separated by dots.
        if len(parts) == 4:
            # All parts must be valid IPv4 segments.
            if all(_is_valid_ipv4_segment(part) for part in parts):
                return True
    
    # --- Attempt IPv6 validation ---
    # An IPv6 address must contain at least one colon.
    if ':' in ip_string:
        # IPv6 addresses can use '::' for compression, but only once.
        if ip_string.count('::') > 1:
            return False
        
        if '::' in ip_string:
            # Handle IPv6 addresses with '::' (zero compression).
            # The string is split into two parts around '::'.
            # E.g., "1::2" -> ["1", "2"]
            # E.g., "::1" -> ["", "1"]
            # E.g., "1::" -> ["1", ""]
            # E.g., "::" -> ["", ""]
            parts = ip_string.split('::')
            # If the address contains '::', there should always be exactly two parts after splitting.
            # (e.g. '1::2' splits into ['1', '2'], '::1' splits into ['', '1'], '1::' splits into ['1', ''])
            # The `ip_string.count('::') > 1` check above handles cases like '1::2::3',
            # so `len(parts)` will always be 2 here.

            # Get segments from the part before '::'
            # If parts[0] is empty (e.g., '::1'), split(':') would return [''],
            # so we explicitly handle it to get an empty list.
            part1_segments = parts[0].split(':') if parts[0] else []
            # Get segments from the part after '::'
            part2_segments = parts[1].split(':') if parts[1] else []

            # Validate all segments in both parts.
            # An empty segment like '' within '1:::' (resulting in part1_segments = ['1', ''])
            # would be caught by _is_valid_ipv6_segment('') returning False.
            if not all(_is_valid_ipv6_segment(s) for s in part1_segments):
                return False
            if not all(_is_valid_ipv6_segment(s) for s in part2_segments):
                return False
            
            total_non_compressed_segments = len(part1_segments) + len(part2_segments)
            
            # If '::' is used for compression, the total number of visible segments
            # must be less than 8, leaving room for the compressed zero groups.
            # The full address has 8 groups. If `total_non_compressed_segments` is 8,
            # there's no room for `::` to represent missing groups, making it invalid.
            # The '::' address itself has 0 segments, which is < 8.
            if not (0 <= total_non_compressed_segments <= 7):
                return False
            
            return True # If all checks pass for the '::' case
            
        else:
            # No '::' present, so the IPv6 address must have exactly 8 segments.
            segments = ip_string.split(':')
            if len(segments) == 8:
                # All segments must be valid IPv6 segments.
                if all(_is_valid_ipv6_segment(segment) for segment in segments):
                    return True
    
    # If it's neither a valid IPv4 nor a valid IPv6 address.
    return False

# add this ad the end of the file
EXPORT_FUNCTION = is_valid_ip_address