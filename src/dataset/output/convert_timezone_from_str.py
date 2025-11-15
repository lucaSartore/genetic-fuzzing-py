# necessary imports (use only the python standard libraries)
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# you can define other auxiliary functions

def convert_timezone_from_str(
    datetime_str: str,
    source_tz_str: str,
    target_tz_str: str,
    datetime_format: str = "%Y-%m-%d %H:%M:%S"
) -> datetime:
    """
    Parses a datetime string, interprets it within a specified source timezone,
    and then converts it to a target timezone.

    This function leverages the standard library `zoneinfo` module, which is
    available in Python 3.9 and later. For earlier Python versions, `zoneinfo`
    is not available and this function will not work as described.

    Args:
        datetime_str (str): The datetime string to parse.
        source_tz_str (str): The IANA string identifier of the timezone
                             that `datetime_str` represents or should be
                             interpreted in (e.g., 'UTC', 'America/New_York').
                             If `datetime_str` includes its own timezone
                             information and `datetime_format` parses it,
                             the `source_tz_str` specifies the timezone this
                             parsed datetime should be *converted to initially*
                             before the final conversion to `target_tz_str`.
                             If `datetime_str` is naive, `source_tz_str` is
                             used to localize it.
        target_tz_str (str): The IANA string identifier of the timezone to
                             convert the datetime to.
        datetime_format (str, optional): The format string to parse
                                         `datetime_str` with (e.g., "%Y-%m-%d %H:%M:%S").
                                         Defaults to "%Y-%m-%d %H:%M:%S".
                                         For ISO 8601 strings, `datetime.fromisoformat`
                                         is an alternative parsing method (not used here
                                         to strictly adhere to `datetime_format` argument).

    Returns:
        datetime.datetime: A timezone-aware datetime object localized
                           to the `target_tz_str`.

    Raises:
        ValueError: If `datetime_str` cannot be parsed with the given format.
        zoneinfo.ZoneInfoNotFoundError: If `source_tz_str` or `target_tz_str`
                                        are not recognized IANA timezone identifiers.
    """
    try:
        # 1. Parse the datetime string into a datetime object.
        # This object might be naive or timezone-aware, depending on datetime_str
        # and datetime_format (e.g., if format includes %z).
        dt_parsed = datetime.strptime(datetime_str, datetime_format)
    except ValueError as e:
        raise ValueError(
            f"Could not parse datetime string '{datetime_str}' "
            f"with format '{datetime_format}': {e}"
        )

    try:
        # 2. Get source timezone object.
        source_tz = ZoneInfo(source_tz_str)
    except ZoneInfoNotFoundError:
        raise ZoneInfoNotFoundError(
            f"Invalid source timezone: '{source_tz_str}'. "
            f"Please use a valid IANA timezone identifier "
            f"(e.g., 'UTC', 'America/New_York')."
        )

    # 3. Interpret/Localize the parsed datetime based on source_tz_str.
    if dt_parsed.tzinfo is None:
        # If the parsed datetime is naive, localize it directly using the source_tz.
        localized_dt = dt_parsed.replace(tzinfo=source_tz)
    else:
        # If the parsed datetime is already timezone-aware (e.g., because datetime_format
        # included %z and datetime_str had tz info), convert it to the source_tz.
        # This effectively re-bases the datetime's context to source_tz before
        # the final conversion.
        localized_dt = dt_parsed.astimezone(source_tz)

    try:
        # 4. Get target timezone object.
        target_tz = ZoneInfo(target_tz_str)
    except ZoneInfoNotFoundError:
        raise ZoneInfoNotFoundError(
            f"Invalid target timezone: '{target_tz_str}'. "
            f"Please use a valid IANA timezone identifier "
            f"(e.g., 'UTC', 'America/New_York')."
        )

    # 5. Convert the localized datetime to the target timezone.
    converted_dt = localized_dt.astimezone(target_tz)

    return converted_dt

# add this ad the end of the file
EXPORT_FUNCTION = convert_timezone_from_str