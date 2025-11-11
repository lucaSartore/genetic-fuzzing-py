# necessary inputs (use only the python standard libraries)

def roman_to_int(s: str) -> int:
    """
    Converts a Roman numeral string (e.g., 'MCMXCIV') to an integer,
    applying complex validation rules.

    The validation rules implemented include:
    1.  Valid Roman numeral characters: Only 'I', 'V', 'X', 'L', 'C', 'D', 'M' are allowed.
    2.  Repetition rules:
        *   'V', 'L', 'D' can never be repeated consecutively (e.g., 'VV', 'LL', 'DD' are invalid).
        *   'I', 'X', 'C', 'M' can be repeated up to three times consecutively (e.g., 'III', 'XXX').
            'IIII', 'XXXX' are invalid.
    3.  Subtractive notation rules:
        *   Only specific combinations are allowed: 'IV' (4), 'IX' (9), 'XL' (40), 'XC' (90), 'CD' (400), 'CM' (900).
            Other combinations like 'IL', 'IC', 'XD', 'XM' are invalid.
        *   'V', 'L', 'D' cannot be used in subtractive notation (e.g., 'VX', 'VL', 'VD' are invalid).
        *   A numeral cannot be repeated and then immediately used for subtraction (e.g., 'IIX', 'XXL' are invalid).
        *   A numeral involved in a subtraction cannot be immediately followed by another numeral
            of the same value as the *subtracted* numeral (e.g., 'IXI' is invalid because 'I' is subtracted,
            then another 'I' follows; 'CMCM' is invalid).
    4.  Ordering rules:
        *   Numerals must generally appear in descending order of value, except for allowed subtractive cases.
        *   The "dominant" value of any Roman numeral group (either a single numeral or the larger part of a
            subtractive pair) must not be greater than the dominant value of the preceding group.
            This prevents sequences like 'VX' (V then X), 'MDM' (M then D, then M again), or 'LCM' (L then C then M).

    Args:
        s: The Roman numeral string to convert.

    Returns:
        The integer representation of the Roman numeral.

    Raises:
        TypeError: If the input `s` is not a string.
        ValueError: If the input string is empty or not a valid Roman numeral
                    according to the complex validation rules.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
    if not s:
        raise ValueError("Input Roman numeral string cannot be empty.")

    roman_map = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }
    
    # Valid subtractive pairs and their integer values
    subtractive_pairs = {
        'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900
    }

    # Numerals that cannot be repeated consecutively
    non_repeatable_chars = {'V', 'L', 'D'}

    # Maximum consecutive repetitions for other numerals
    repeatable_max_counts = {'I': 3, 'X': 3, 'C': 3, 'M': 3}

    total = 0
    i = 0
    
    # max_allowed_char_in_segment tracks the largest *dominant* value (either a single numeral's value
    # or the value of the larger numeral in a subtractive pair) seen so far in the string, moving left-to-right.
    # This helps enforce the general descending order rule (V4).
    # Initialized to float('inf') to allow any value for the first numeral/group.
    max_allowed_char_in_segment: float = float('inf') 

    # Track consecutive repetitions for V2
    prev_char: str = ''
    consecutive_count: int = 0

    while i < len(s):
        current_char: str = s[i]

        # V1: Valid Characters
        if current_char not in roman_map:
            raise ValueError(f"Invalid Roman numeral character '{current_char}' found at position {i}.")
        
        current_value: int = roman_map[current_char]

        # V2: Repetition Rules (primary check for 'V', 'L', 'D' and 'I', 'X', 'C', 'M')
        if current_char == prev_char:
            consecutive_count += 1
            if current_char in non_repeatable_chars:
                raise ValueError(f"Invalid repetition: '{current_char}' cannot be repeated at position {i}.")
            if consecutive_count > repeatable_max_counts.get(current_char, 0): # Handles I, X, C, M
                raise ValueError(f"Invalid repetition: '{current_char}' cannot be repeated more than "
                                 f"{repeatable_max_counts[current_char]} times at position {i}.")
        else:
            consecutive_count = 1
        
        prev_char = current_char

        # Look ahead for potential subtraction
        next_char: str | None = s[i+1] if i + 1 < len(s) else None
        next_value: int = roman_map[next_char] if next_char else 0

        # Subtraction logic and validation
        if next_char and current_value < next_value:
            # Potential subtraction `current_char` from `next_char`
            pair: str = current_char + next_char

            # V3a: Check if it's an allowed subtractive pair (covers 'IL', 'IC', 'XD', 'XM' etc.)
            if pair not in subtractive_pairs:
                raise ValueError(f"Invalid subtraction combination '{pair}' at position {i}. "
                                 "Only IV, IX, XL, XC, CD, CM are allowed.")
            
            # V3b: 'V', 'L', 'D' cannot be used in subtractive notation (e.g., 'VX').
            # This is implicitly covered by `subtractive_pairs` keys, but explicit check for safety:
            if current_char in non_repeatable_chars:
                raise ValueError(f"Invalid subtraction: '{current_char}' cannot be used to subtract at position {i}.")

            # V3c: A numeral cannot be repeated and then immediately used for subtraction (e.g., 'IIX', 'XXL')
            if consecutive_count > 1:
                raise ValueError(f"Invalid form: '{s[i-1]}{current_char}{next_char}'. A numeral cannot be repeated and "
                                 f"then immediately used for subtraction at position {i}.")
            
            # V3d: A numeral involved in subtraction cannot be immediately followed by another numeral
            # of the same value as the *subtracted* numeral (e.g., 'IXI', 'CMCM').
            # s[i] is the subtractor, s[i+1] is the target. Check if s[i+2] exists and is s[i].
            if i + 2 < len(s) and s[i+2] == current_char:
                raise ValueError(f"Invalid sequence: '{current_char}{next_char}{s[i+2]}'. "
                                 f"A numeral used for subtraction ('{current_char}') cannot be immediately followed by itself "
                                 f"after the subtraction, at position {i+2}.")

            # V4: General Ordering check for the dominant value.
            # `next_value` (the value being subtracted from) is the dominant value for this group.
            # It must not be greater than `max_allowed_char_in_segment`.
            if next_value > max_allowed_char_in_segment:
                 raise ValueError(f"Invalid order: Numeral '{next_char}' (value {next_value}) cannot appear "
                                  f"after a segment that ended with a dominant value of {int(max_allowed_char_in_segment)} at position {i+1}. "
                                  f"Roman numerals should generally be in descending order.")
            
            total += subtractive_pairs[pair]
            # After a subtraction (e.g., CM), the next group's dominant character cannot exceed the value of the
            # *subtracted* character (C's value, 100). This enforces correct ordering like MCMXCIV.
            max_allowed_char_in_segment = current_value 
            i += 2  # Skip both current and next char

        else: # Standard addition
            # V4: General Ordering check for the dominant value.
            # `current_value` is the dominant value for this group.
            # It must not be greater than `max_allowed_char_in_segment`.
            if current_value > max_allowed_char_in_segment:
                raise ValueError(f"Invalid order: Numeral '{current_char}' (value {current_value}) cannot appear "
                                 f"after a segment that ended with a dominant value of {int(max_allowed_char_in_segment)} at position {i}. "
                                 f"Roman numerals should generally be in descending order.")

            total += current_value
            # For additive numerals, `current_value` sets the new limit for `max_allowed_char_in_segment`.
            # This ensures e.g., M (1000) followed by D (500) is okay, but M followed by M (1000) is okay,
            # but M followed by C (100) is okay. MDM (M then D then M again) is invalid because the second M (1000)
            # would be greater than max_allowed_char_in_segment (D=500).
            max_allowed_char_in_segment = current_value 
            i += 1  # Move to next char

    return total

# add this ad the end of the file
EXPORT_FUNCTION = roman_to_int