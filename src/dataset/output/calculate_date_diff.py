import datetime

def calculate_date_diff(date_str1: str, date_str2: str, date_format: str) -> int:
    """
    Parses two dates in a given format and finds the difference in days.

    Args:
        date_str1: The first date string.
        date_str2: The second date string.
        date_format: The format string specifying how the date strings should be parsed
                     (e.g., "%Y-%m-%d" for "2023-10-27").

    Returns:
        The difference in days between the two dates (date_str1 - date_str2).
        A positive value means date_str1 is later than date_str2.
        A negative value means date_str1 is earlier than date_str2.

    Raises:
        ValueError: If the date strings do not match the specified format.
    """
    try:
        # Parse the date strings into datetime objects
        date1 = datetime.datetime.strptime(date_str1, date_format)
        date2 = datetime.datetime.strptime(date_str2, date_format)

        # Calculate the difference
        time_difference = date1 - date2

        # Return the difference in days
        return time_difference.days
    except ValueError as e:
        raise ValueError(f"Error parsing dates with format '{date_format}': {e}") from e

EXPORT_FUNCTION = calculate_date_diff