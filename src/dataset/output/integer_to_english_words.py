# No external imports are necessary for this function, as it uses only built-in types and operations.

# Auxiliary data structures for number to word conversion
_units: list[str] = [
    "Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
    "Seventeen", "Eighteen", "Nineteen"
]

_tens: list[str] = [
    "", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"
]

_thousands_scales: list[str] = [
    "", "Thousand", "Million", "Billion", "Trillion", "Quadrillion", "Quintillion",
    "Sextillion", "Septillion", "Octillion", "Nonillion", "Decillion"
    # This list can be extended for even larger numbers if needed.
    # Python's integers support arbitrary precision, so the practical limit
    # is memory or the length of this list.
]

def _convert_less_than_thousand(num: int) -> str:
    """
    Auxiliary function to convert a number less than 1000 to its English word representation.
    Handles numbers from 1 to 999.
    """
    if num == 0:
        return "" # Special case: for blocks of 000, we return empty string

    parts: list[str] = []

    # Handle hundreds place
    if num >= 100:
        parts.append(_units[num // 100])
        parts.append("Hundred")
        num %= 100

    # Handle tens and units place
    if num > 0:
        if num < 20:
            # Numbers 1-19 have unique words
            parts.append(_units[num])
        else:
            # Numbers 20-99 (e.g., twenty, thirty-one)
            tens_digit = num // 10
            units_digit = num % 10
            
            tens_word = _tens[tens_digit]
            units_word = _units[units_digit] if units_digit > 0 else ""

            if units_word:
                # Add hyphen for numbers like twenty-one
                parts.append(f"{tens_word}-{units_word}")
            else:
                parts.append(tens_word)
    
    return " ".join(parts)


def integer_to_english_words(num: int) -> str:
    """
    Converts a non-negative integer to its English word representation.

    Args:
        num: A non-negative integer.

    Returns:
        A string representing the English word form of the integer.

    Raises:
        ValueError: If the input is not a non-negative integer.
    """
    if not isinstance(num, int) or num < 0:
        raise ValueError("Input must be a non-negative integer.")

    if num == 0:
        return "Zero"

    words: list[str] = []
    scale_index = 0

    # Process the number in blocks of three digits (hundreds, thousands, millions, etc.)
    while num > 0:
        # Check if the current three-digit block is non-zero
        if num % 1000 != 0:
            block_words = _convert_less_than_thousand(num % 1000)
            
            # Add the appropriate scale (Thousand, Million, etc.) if applicable
            if _thousands_scales[scale_index]:
                words.insert(0, _thousands_scales[scale_index])
            
            # Add the words for the current block to the beginning of the list
            words.insert(0, block_words)
        
        num //= 1000  # Move to the next three-digit block
        scale_index += 1 # Increment the scale index

    return " ".join(words)

# add this at the end of the file
EXPORT_FUNCTION = integer_to_english_words