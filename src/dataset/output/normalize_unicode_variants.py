# necessary imports (use only the python standard libraries)
import unicodedata
import re

# A custom map for common homoglyphs and typographic variants not fully handled
# by standard NFKC normalization. This map is illustrative and not exhaustive;
# real-world applications might require a much larger, domain-specific mapping.
HOMOGLYPH_MAP = {
    # Greek script characters that often resemble Latin ones
    'ο': 'o',  # Greek small letter omicron
    'Α': 'A',  # Greek capital letter Alpha
    'Ε': 'E',  # Greek capital letter Epsilon
    'Η': 'H',  # Greek capital letter Eta
    'Ι': 'I',  # Greek capital letter Iota
    'Κ': 'K',  # Greek capital letter Kappa
    'Μ': 'M',  # Greek capital letter Mu
    'Ν': 'N',  # Greek capital letter Nu
    'Ο': 'O',  # Greek capital letter Omicron
    'Ρ': 'P',  # Greek capital letter Rho
    'Τ': 'T',  # Greek capital letter Tau
    'Χ': 'X',  # Greek capital letter Chi
    'У': 'Y',  # Cyrillic capital letter U, visually similar to Latin Y

    # Cyrillic script characters that often resemble Latin ones
    'а': 'a',  # Cyrillic small letter a
    'е': 'e',  # Cyrillic small letter ie
    'і': 'i',  # Cyrillic small letter dotted i
    'р': 'p',  # Cyrillic small letter er
    'с': 'c',  # Cyrillic small letter es
    'х': 'x',  # Cyrillic small letter ha
    'А': 'A',  # Cyrillic capital letter A
    'В': 'B',  # Cyrillic capital letter VE, visually similar to Latin B
    'Е': 'E',  # Cyrillic capital letter IE
    'Н': 'H',  # Cyrillic capital letter EN
    'К': 'K',  # Cyrillic capital letter KA
    'М': 'M',  # Cyrillic capital letter EM
    'О': 'O',  # Cyrillic capital letter O
    'Р': 'P',  # Cyrillic capital letter ER
    'С': 'C',  # Cyrillic capital letter ES
    'Т': 'T',  # Cyrillic capital letter TE
    'Х': 'X',  # Cyrillic capital letter HA

    # Common typographic variations and symbols to standard ASCII equivalents
    # Roman Numerals (handled by NFKC for many, but some might remain or be useful to map explicitly)
    'Ⅰ': 'I', 'Ⅱ': 'II', 'Ⅲ': 'III', 'Ⅳ': 'IV', 'Ⅴ': 'V',
    'Ⅵ': 'VI', 'Ⅶ': 'VII', 'Ⅷ': 'VIII', 'Ⅸ': 'IX', 'Ⅹ': 'X',
    'Ⅼ': 'L', 'Ⅽ': 'C', 'Ⅾ': 'D', 'Ⅿ': 'M',

    # Dash variations
    '‐': '-',  # Hyphen (non-breaking)
    '–': '-',  # En dash
    '—': '-',  # Em dash

    # Quote variations
    '‘': "'", '’': "'",  # Left/Right single quotation marks to straight single quote
    '“': '"', '”': '"',  # Left/Right double quotation marks to straight double quote

    # Prime symbols
    '′': "'", '″': '"',  # Prime and double prime to standard quotes

    # Zero-width spaces and non-breaking space
    '​': '',   # Zero Width Space (U+200B) - effectively removes it
    ' ': ' ',  # Non-breaking space (U+00A0) to regular space
}

# Pre-compile the translation table for efficiency with str.translate()
HOMOGLYPH_TRANSLATION_TABLE = str.maketrans(HOMOGLYPH_MAP)

def normalize_unicode_variants(text: str) -> str:
    """
    Normalizes text handling multiple unicode forms, homoglyphs, and bidirectional text.

    This function performs a series of transformations to bring text to a more
    consistent and standardized form, useful for tasks like search indexing,
    comparison, or data cleaning. The steps include:

    1.  **Unicode Normalization (NFKC)**: Applies `unicodedata.normalize('NFKC')`.
        This handles canonical and compatibility decompositions, converting
        characters like full-width ASCII forms (ｅ.ｇ., 'Ａ' to 'A'), superscripts
        and subscripts (e.g., '¹' to '1'), and some ligatures (e.g., 'ﬃ' to 'ffi')
        to their base components.

    2.  **Case Folding**: Converts all characters to their case-folded form using
        `.casefold()`. This is more robust than `.lower()` for caseless matching
        across different scripts.

    3.  **Homoglyph and Common Symbol Mapping**: Applies a custom translation table
        (`HOMOGLYPH_TRANSLATION_TABLE`) to replace specific visually similar
        characters (homoglyphs) from different scripts (e.g., Cyrillic 'а' to
        Latin 'a') and common typographic variations (like various dash or quote
        styles) with their preferred ASCII or common Unicode equivalent.

    4.  **Removal of Bidirectional and Unicode Format Characters**: Iterates through
        the text and removes characters belonging to the 'Cf' (Format) Unicode
        category. This includes bidirectional control characters (e.g., RLM, LRM),
        zero-width joiners/non-joiners, and other invisible characters that affect
        text rendering but not its logical content.

    5.  **Whitespace Normalization**: Replaces any sequence of Unicode whitespace
        characters (including tabs, newlines, and various Unicode space characters)
        with a single ASCII space. Finally, it strips any leading or trailing
        whitespace.

    Args:
        text (str): The input string to normalize.

    Returns:
        str: The normalized string.

    Raises:
        TypeError: If the input 'text' is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string.")

    # Step 1: NFKC Unicode Normalization
    # This step handles canonical and compatibility decompositions.
    normalized_text = unicodedata.normalize('NFKC', text)

    # Step 2: Case Folding
    # Converts text to a common case for caseless matching.
    normalized_text = normalized_text.casefold()

    # Step 3: Homoglyph and Common Symbol Mapping
    # Applies the custom translation table for specific visual similarities and
    # typographic replacements not fully covered by NFKC.
    normalized_text = normalized_text.translate(HOMOGLYPH_TRANSLATION_TABLE)

    # Step 4: Remove Bidirectional and other Unicode Format Characters
    # These characters (Unicode category 'Cf') are primarily for display formatting
    # and should be removed for consistent text processing.
    filtered_chars = [
        char for char in normalized_text
        if unicodedata.category(char) != 'Cf'
    ]
    normalized_text = "".join(filtered_chars)

    # Step 5: Normalize Whitespace
    # Replaces any sequence of one or more whitespace characters (including
    # various Unicode spaces, tabs, newlines) with a single ASCII space,
    # then strips leading/trailing spaces.
    normalized_text = re.sub(r'\s+', ' ', normalized_text).strip()

    return normalized_text

# add this ad the end of the file
EXPORT_FUNCTION = normalize_unicode_variants