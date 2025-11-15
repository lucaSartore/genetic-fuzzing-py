import re
from typing import Dict, Optional, Union

# Regular expression pattern for the Apache Combined Log Format.
# This pattern uses named capture groups for easy extraction of log components.
#
# Log format example:
# 127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "http://www.example.com/start.html" "Mozilla/4.08 [en] (Win98; I ;Nav)"
#
# Breakdown of the pattern:
# ^                                       # Start of the line
# (?P<ip_address>\S+)                     # Client IP address (non-whitespace characters)
# \s+                                     # One or more spaces
# (?P<remote_logname>\S+)                 # Remote log name (often '-')
# \s+
# (?P<remote_user>\S+)                    # Remote user (authentication; often '-')
# \s+
# \[                                      # Literal '['
# (?P<timestamp>\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4}) # Timestamp format: DD/Mon/YYYY:HH:MM:SS ZZZZ
# \]                                      # Literal ']'
# \s+
# \"                                      # Literal '"'
# (?P<method>[A-Z]+)                      # HTTP Method (GET, POST, PUT, DELETE, etc.)
# \s+
# (?P<path>\S+)                           # Requested path
# \s+
# HTTP/(?P<protocol>\d\.\d)               # HTTP Protocol version (e.g., 1.0, 1.1)
# \"                                      # Literal '"'
# \s+
# (?P<status>\d{3})                       # HTTP Status code (e.g., 200, 404, 500)
# \s+
# (?P<bytes_sent>\d+|-)\s+                # Bytes sent to the client, or '-' if no content
# \"                                      # Literal '"'
# (?P<referrer>[^"]*)                     # Referrer URL (any characters except '"', allowing empty)
# \"                                      # Literal '"'
# \s+
# \"                                      # Literal '"'
# (?P<user_agent>[^"]*)                   # User Agent string (any characters except '"', allowing empty)
# \"                                      # Literal '"'
# $                                       # End of the line
APACHE_COMBINED_LOG_PATTERN = re.compile(
    r'^(?P<ip_address>\S+) '
    r'(?P<remote_logname>\S+) '
    r'(?P<remote_user>\S+) '
    r'\[(?P<timestamp>\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\] '
    r'"(?P<method>[A-Z]+) '
    r'(?P<path>\S+) '
    r'HTTP/(?P<protocol>\d\.\d)" '
    r'(?P<status>\d{3}) '
    r'(?P<bytes_sent>\d+|-)\s+'
    r'"(?P<referrer>[^"]*)" '
    r'"(?P<user_agent>[^"]*)"$'
)

def parse_apache_log_line(log_line: str) -> Optional[Dict[str, Union[str, int, None]]]:
    """
    Uses 're.match' with a complex pattern to parse a single Apache log line into a dict.

    This function parses a single Apache log line, specifically adhering to the
    "Combined Log Format", into a dictionary. It extracts various components
    like IP address, timestamp, request method, path, status code, bytes sent,
    referrer, and user agent. Numerical fields ('status', 'bytes_sent') are
    converted to integers where possible, with 'bytes_sent' becoming None if
    represented by a hyphen ('-').

    Args:
        log_line: A single string representing an Apache log line in Combined Log Format.

    Returns:
        An Optional dictionary containing the parsed components if the log_line
        matches the expected format. The dictionary keys and their types are:
        - 'ip_address': str
        - 'remote_logname': str
        - 'remote_user': str
        - 'timestamp': str
        - 'method': str
        - 'path': str
        - 'protocol': str
        - 'status': int
        - 'bytes_sent': Optional[int] (int if a number, None if '-')
        - 'referrer': str
        - 'user_agent': str
        Returns None if the log_line does not match the Apache Combined Log Format pattern.
    """
    match = APACHE_COMBINED_LOG_PATTERN.match(log_line)

    if match:
        parsed_data = match.groupdict()

        # Convert status code to integer
        try:
            parsed_data['status'] = int(parsed_data['status'])
        except ValueError:
            # Should not happen if regex guarantees digits, but good for robustness
            parsed_data['status'] = None 

        # Convert bytes_sent to integer, or None if it's '-'
        bytes_sent_str = parsed_data['bytes_sent']
        parsed_data['bytes_sent'] = int(bytes_sent_str) if bytes_sent_str != '-' else None

        return parsed_data
    else:
        return None

# add this ad the end of the file
EXPORT_FUNCTION = parse_apache_log_line