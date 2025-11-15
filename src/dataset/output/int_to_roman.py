# necessary imports (use only the python standard libraries)

def int_to_roman(num: int) -> str:
    """
    Converts an integer (1-3999) to its Roman numeral representation.
    This implementation uses complex branching logic to handle the different patterns
    for thousands, hundreds, tens, and units places, including subtractive rules (e.g., IV, IX, XL, XC, CD, CM).

    Args:
        num: An integer between 1 and 3999 (inclusive).

    Returns:
        A string representing the Roman numeral of the input integer.

    Raises:
        ValueError: If the input integer is not within the valid range [1, 3999].
    """
    if not 1 <= num <= 3999:
        raise ValueError("Input integer must be between 1 and 3999.")

    roman_parts = []

    # Process the thousands place
    # Thousands are represented by 'M's. Max is 3 (MMM = 3000).
    thousands = num // 1000
    if thousands > 0:
        roman_parts.append("M" * thousands)
    num %= 1000  # Update num to the remainder for the next place value

    # Process the hundreds place
    # Roman numerals for hundreds follow patterns:
    # 900: CM
    # 400: CD
    # 500-800: D + C's (e.g., 600=DC, 700=DCC, 800=DCCC)
    # 100-300: C's (e.g., 100=C, 200=CC, 300=CCC)
    hundreds = num // 100
    if hundreds == 9:
        roman_parts.append("CM")
    elif hundreds == 4:
        roman_parts.append("CD")
    elif hundreds >= 5: # 5, 6, 7, 8
        roman_parts.append("D" + "C" * (hundreds - 5))
    elif hundreds > 0: # 1, 2, 3
        roman_parts.append("C" * hundreds)
    num %= 100 # Update num for tens place

    # Process the tens place
    # Roman numerals for tens follow similar patterns:
    # 90: XC
    # 40: XL
    # 50-80: L + X's (e.g., 60=LX, 70=LXX, 80=LXXX)
    # 10-30: X's (e.g., 10=X, 20=XX, 30=XXX)
    tens = num // 10
    if tens == 9:
        roman_parts.append("XC")
    elif tens == 4:
        roman_parts.append("XL")
    elif tens >= 5: # 5, 6, 7, 8
        roman_parts.append("L" + "X" * (tens - 5))
    elif tens > 0: # 1, 2, 3
        roman_parts.append("X" * tens)
    num %= 10 # Update num for units place

    # Process the units place
    # Roman numerals for units follow similar patterns:
    # 9: IX
    # 4: IV
    # 5-8: V + I's (e.g., 6=VI, 7=VII, 8=VIII)
    # 1-3: I's (e.g., 1=I, 2=II, 3=III)
    units = num
    if units == 9:
        roman_parts.append("IX")
    elif units == 4:
        roman_parts.append("IV")
    elif units >= 5: # 5, 6, 7, 8
        roman_parts.append("V" + "I" * (units - 5))
    elif units > 0: # 1, 2, 3
        roman_parts.append("I" * units)

    return "".join(roman_parts)

# add this ad the end of the file
EXPORT_FUNCTION = int_to_roman