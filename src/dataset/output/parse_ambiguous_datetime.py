# necessary imports (use only the python standard libraries)
from datetime import datetime
from typing import List

# you can define other auxiliary functions

def parse_ambiguous_datetime(datetime_str: str) -> datetime:
    """
    Tries to parse a datetime string that could be in one of several formats.

    This function attempts to parse the input datetime string using a predefined
    list of common datetime formats. It first tries the robust `datetime.fromisoformat()`
    and then iterates through a list of `strptime` format codes.

    Args:
        datetime_str: The string containing the datetime to parse.

    Returns:
        A datetime object if parsing is successful using any of the known formats.

    Raises:
        ValueError: If the string cannot be parsed by any of the known formats.
    """
    # List of common datetime formats to try with datetime.strptime().
    # The order is chosen to prioritize more specific formats or those that
    # might be more common, reducing ambiguity where possible.
    # Note: %f for microseconds, %z for timezone offset, %Z for timezone name.
    # We include formats with 24-hour time (%H) and 12-hour time with AM/PM (%I, %p).
    strptime_formats: List[str] = [
        # ISO 8601-like formats (without 'T' or specific timezone handling which fromisoformat covers)
        "%Y-%m-%d %H:%M:%S.%f", # e.g., "2023-10-27 15:30:00.123456"
        "%Y-%m-%d %H:%M:%S",   # e.g., "2023-10-27 15:30:00"
        "%Y-%m-%d %H:%M",      # e.g., "2023-10-27 15:30"
        "%Y-%m-%d",            # e.g., "2023-10-27"

        # US common formats (MM/DD/YYYY)
        "%m/%d/%Y %H:%M:%S.%f", # e.g., "10/27/2023 15:30:00.123456"
        "%m/%d/%Y %H:%M:%S",   # e.g., "10/27/2023 15:30:00"
        "%m/%d/%Y %H:%M",      # e.g., "10/27/2023 15:30"
        "%m/%d/%Y",            # e.g., "10/27/2023"
        "%m-%d-%Y %H:%M:%S",   # e.g., "10-27-2023 15:30:00"
        "%m-%d-%Y %H:%M",      # e.g., "10-27-2023 15:30"
        "%m-%d-%Y",            # e.g., "10-27-2023"

        # European common formats (DD/MM/YYYY)
        "%d/%m/%Y %H:%M:%S.%f", # e.g., "27/10/2023 15:30:00.123456"
        "%d/%m/%Y %H:%M:%S",   # e.g., "27/10/2023 15:30:00"
        "%d/%m/%Y %H:%M",      # e.g., "27/10/2023 15:30"
        "%d/%m/%Y",            # e.g., "27/10/2023"
        "%d-%m-%Y %H:%M:%S",   # e.g., "27-10-2023 15:30:00"
        "%d-%m-%Y %H:%M",      # e.g., "27-10-2023 15:30"
        "%d-%m-%Y",            # e.g., "27-10-2023"

        # Formats with AM/PM (12-hour clock)
        "%Y-%m-%d %I:%M:%S %p", # e.g., "2023-10-27 03:30:00 PM"
        "%Y-%m-%d %I:%M %p",    # e.g., "2023-10-27 03:30 PM"
        "%m/%d/%Y %I:%M:%S %p", # e.g., "10/27/2023 03:30:00 PM"
        "%m/%d/%Y %I:%M %p",    # e.g., "10/27/2023 03:30 PM"
        "%d/%m/%Y %I:%M:%S %p", # e.g., "27/10/2023 03:30:00 PM"
        "%d/%m/%Y %I:%M %p",    # e.g., "27/10/2023 03:30 PM"

        # Word-based month names
        "%B %d, %Y %H:%M:%S",  # e.g., "October 27, 2023 15:30:00"
        "%b %d, %Y %H:%M:%S",  # e.g., "Oct 27, 2023 15:30:00"
        "%B %d, %Y",           # e.g., "October 27, 2023"
        "%b %d, %Y",           # e.g., "Oct 27, 2023"
        "%B %d, %Y %I:%M:%S %p", # e.g., "October 27, 2023 03:30:00 PM"
        "%b %d, %Y %I:%M:%S %p", # e.g., "Oct 27, 2023 03:30:00 PM"
    ]

    # 1. Try parsing with datetime.fromisoformat() first.
    #    This method is highly robust for various ISO 8601 formats,
    #    including those with 'T', microseconds, and timezone offsets (like 'Z' or '+HH:MM').
    try:
        return datetime.fromisoformat(datetime_str)
    except ValueError:
        # If fromisoformat fails, proceed to try strptime formats.
        pass

    # 2. Iterate through the list of common strptime formats.
    for fmt in strptime_formats:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            # If parsing fails for the current format, continue to the next one.
            continue

    # If no format matched after trying all possibilities, raise an error.
    raise ValueError(f"Unable to parse datetime string: '{datetime_str}' "
                     f"with any of the known formats.")

# add this ad the end of the file
EXPORT_FUNCTION = parse_ambiguous_datetime