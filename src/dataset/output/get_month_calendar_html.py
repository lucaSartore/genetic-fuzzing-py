# necessary imports (use only the python standard libraries)
import calendar

# you can define other auxiliary functions

def get_month_calendar_html(year: int, month: int) -> str:
    """
    Uses the 'calendar' module to generate an HTML calendar for a given month and year.

    Args:
        year (int): The year for which to generate the calendar (e.g., 2023).
        month (int): The month for which to generate the calendar (1-12, e.g., 1 for January).

    Returns:
        str: An HTML string representing the calendar for the specified month and year.
             Returns an empty string if the month or year is invalid.
    """
    if not (1 <= month <= 12) or not (year > 0):
        # Basic validation for month and year
        return ""

    # Create an HTMLCalendar instance
    # The firstweekday parameter determines which day is the start of the week.
    # calendar.MONDAY (0) means Monday is the first day.
    # calendar.SUNDAY (6) means Sunday is the first day.
    # Default is Monday.
    cal = calendar.HTMLCalendar(firstweekday=calendar.MONDAY)

    # Format the month as an HTML table
    html_calendar_string = cal.formatmonth(year, month)

    return html_calendar_string

# add this ad the end of the file
EXPORT_FUNCTION = get_month_calendar_html