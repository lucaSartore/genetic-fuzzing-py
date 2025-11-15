import re

# A constant dictionary mapping Roman numeral characters to their integer values.
# This map is used for the conversion logic itself.
_ROMAN_CHAR_TO_INT_MAP = {
    'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
}

# A regular expression to enforce complex validation rules for Roman numerals.
# This regex ensures:
# 1. Valid characters are used ('I', 'V', 'X', 'L', 'C', 'D', 'M').
# 2. Correct order of magnitude groups (thousands, hundreds, tens, units).
# 3. Correct repetition limits:
#    - 'I', 'X', 'C', 'M' can be repeated up to three times (e.g., 'III', 'XXX', 'CCC', 'MMM').
#    - 'V', 'L', 'D' cannot be repeated (e.g., 'VV', 'LL', 'DD' are invalid).
# 4. Correct subtractive combinations:
#    - 'I' can only precede 'V' or 'X' (e.g., 'IV', 'IX').
#    - 'X' can only precede 'L' or 'C' (e.g., 'XL', 'XC').
#    - 'C' can only precede 'D' or 'M' (e.g., 'CD', 'CM').
#    - Invalid subtractive combinations are disallowed (e.g., 'IL', 'IC', 'XD', 'XM', 'VX', 'LC', 'DM').
# 5. No 'double subtraction' (e.g., 'IIX' for 8, which should be 'VIII').
# 6. Ensures the entire string matches the pattern from start to end (`^...$`).
_ROMAN_VALIDATION_REGEX = re.compile(
    r"^M{0,3}"               # Thousands: 0 to 3 'M's (e.g., M, MM, MMM)
    r"(CM|CD|D?C{0,3})"      # Hundreds: 'CM' (900), 'CD' (400),
                             # or 'D' (500) followed by 0-3 'C's (e.g., D, DC, DCC, DCCC),
                             # or 0-3 'C's (e.g., C, CC, CCC).
    r"(XC|XL|L?X{0,3})"      # Tens: 'XC' (90), 'XL' (40),
                             # or 'L' (50) followed by 0-3 'X's (e.g., L, LX, LXX, LXXX),
                             # or 0-3 'X's (e.g., X, XX, XXX).
    r"(IX|IV|V?I{0,3})$"     # Units: 'IX' (9), 'IV' (4),
                             # or 'V' (5) followed by 0-3 'I's (e.g., V, VI, VII, VIII),
                             # or 0-3 'I's (e.g., I, II, III).
)

def _is_valid_roman_numeral_string(s: str) -> bool:
    """
    Checks if a string is a valid Roman numeral according to standard, complex rules
    using a regular expression.

    Args:
        s: The string to validate.

    Returns:
        True if the string is a valid Roman numeral, False otherwise.
    """
    return bool(_ROMAN_VALIDATION_REGEX.fullmatch(s))


def roman_to_int(roman_numeral: str) -> int:
    """
    Converts a Roman numeral string (e.g., 'MCMXCIV') to its integer equivalent.

    This function incorporates complex validation rules to ensure the input
    string is a syntactically correct Roman numeral before conversion.

    Validation rules include:
    1.  Only allowed Roman numeral characters ('I', 'V', 'X', 'L', 'C', 'D', 'M')
        are present.
    2.  Characters 'I', 'X', 'C', 'M' can be repeated consecutively up to three times.
        (e.g., 'III' is valid, 'IIII' is not).
    3.  Characters 'V', 'L', 'D' cannot be repeated.
        (e.g., 'V' is valid, 'VV' is not).
    4.  Subtraction is only permitted for specific pairs:
        - 'I' can only precede 'V' or 'X' (resulting in 4 or 9).
        - 'X' can only precede 'L' or 'C' (resulting in 40 or 90).
        - 'C' can only precede 'D' or 'M' (resulting in 400 or 900).
    5.  Invalid subtractive combinations are disallowed (e.g., 'IL', 'IC', 'XD', 'XM', 'VX', 'LC', 'DM').
    6.  The numeral must follow the correct general order of magnitudes
        (thousands, then hundreds, then tens, then units).
    7.  A smaller numeral cannot be repeated before a larger numeral for subtraction
        (e.g., 'IIX' is invalid; it should be 'VIII').
    8.  After a subtractive pair, the subsequent numerals must not violate the
        established decreasing order or repetition rules (e.g., 'IXI' is invalid).

    Args:
        roman_numeral: The Roman numeral string to convert. Must be a non-empty string.

    Returns:
        The integer representation of the Roman numeral.

    Raises:
        TypeError: If `roman_numeral` is not a string.
        ValueError: If `roman_numeral` is empty or does not conform to
                    the complex validation rules of Roman numerals.
    """
    if not isinstance(roman_numeral, str):
        raise TypeError("Input 'roman_numeral' must be a string.")

    if not roman_numeral:
        raise ValueError("Input Roman numeral string cannot be empty.")

    # Validate the entire Roman numeral string against the complex rules.
    # The regex implicitly handles uppercase. If lowercase input like 'mcmxciv'
    # were to be supported, `roman_numeral.upper()` would be needed here.
    # For strict adherence to standard Roman numeral notation, we assume uppercase.
    if not _is_valid_roman_numeral_string(roman_numeral):
        raise ValueError(
            f"'{roman_numeral}' is not a valid Roman numeral according to "
            f"complex validation rules."
        )

    total_value = 0
    previous_char_value = 0

    # Iterate through the Roman numeral string from right to left.
    # This approach simplifies the conversion for *valid* Roman numerals,
    # as subtraction logic (e.g., IV = 5 - 1) naturally emerges.
    for char in reversed(roman_numeral):
        current_char_value = _ROMAN_CHAR_TO_INT_MAP[char] # Guaranteed to exist due to regex validation

        if current_char_value < previous_char_value:
            # If current numeral is smaller than the previous one, it's a subtraction.
            # Example: In 'IV', when processing 'I' after 'V', 1 < 5, so subtract 1.
            total_value -= current_char_value
        else:
            # Otherwise, add the numeral's value.
            # Example: In 'VI', when processing 'I' after 'V', 1 is not < 5 (no subtraction).
            total_value += current_char_value

        previous_char_value = current_char_value

    return total_value

# Add this at the end of the file as per the template
EXPORT_FUNCTION = roman_to_int