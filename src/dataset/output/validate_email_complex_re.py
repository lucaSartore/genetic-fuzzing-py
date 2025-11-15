import re

def validate_email_complex_re(email: str) -> bool:
    """
    Validates an email using a complex (but not perfect) regex.

    This function employs a regular expression designed to cover a wide range
    of common and valid email address formats, adhering to many practical
    email validation rules without attempting to be a 100% RFC-compliant parser.
    A truly RFC-compliant regex is extremely complex, verbose, and often
    impractical for general use.

    The regex generally enforces the following structure:
    - **Local part (before '@'):**
      Allows alphanumeric characters, dots (`.`), underscores (`_`),
      percent signs (`%`), plus signs (`+`), and hyphens (`-`).
      Must contain at least one character.
      Example: `john.doe`, `user_123`, `my+tag`, `test-email`
    - **Domain part (after '@'):**
      - Composed of one or more "labels" separated by dots (`.`).
      - Each label must start and end with an alphanumeric character
        (`a-z`, `A-Z`, `0-9`).
      - Labels can contain alphanumeric characters and hyphens (`-`) in the middle.
      - The Top-Level Domain (TLD) must consist of at least two alphabetic characters.

    Examples of email addresses it should typically validate as True:
    - `test@example.com`
    - `john.doe@sub.domain.co.uk`
    - `user-name+tag@email-provider.net`
    - `12345@mail.org`
    - `a@b.co`

    Examples of email addresses it might *not* validate (or might incorrectly
    validate) due to its "not perfect" nature:
    - Quoted local parts (e.g., `"john.doe"@example.com`)
    - Email addresses with an IP address as the domain (e.g., `user@[192.168.1.1]`)
    - Internationalized Domain Names (IDN) or email addresses with non-ASCII characters
      in the local part or domain.
    - Very specific RFC edge cases like consecutive dots or dots at the start/end
      of the local part (though this regex handles domain labels fairly well).
    - Email addresses with comments (e.g., `user(comment)@domain.com`)

    Args:
        email: The email address string to validate.

    Returns:
        True if the email address matches the complex regex pattern, False otherwise.
    """
    # The chosen regex is a common "complex" pattern that balances strictness
    # with real-world usability.
    #
    # Regex breakdown:
    # ^                             # Start of the string
    # [a-zA-Z0-9._%+-]+             # Local part:
    #                               #   - Allows alphanumeric, dot, underscore, percent, plus, hyphen.
    #                               #   - Must have at least one character.
    # @                             # Separator
    # [a-zA-Z0-9]                   # Domain label start: Must be alphanumeric.
    # (?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])? # Domain label middle/end (optional):
    #                               #   - [a-zA-Z0-9-]{0,61}: 0 to 61 alphanumeric or hyphen chars.
    #                               #   - [a-zA-Z0-9]: Ends with an alphanumeric char (not a hyphen).
    #                               #   - The entire non-starting part is optional to allow single-char labels.
    # (?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)* # Subdomains (optional, zero or more):
    #                               #   - \.: A literal dot separator.
    #                               #   - Followed by another domain label structure (as defined above).
    # \.                            # TLD separator: A literal dot.
    # [a-zA-Z]{2,}                  # TLD: At least 2 alphabetic characters.
    # $                             # End of the string
    #
    # re.compile is used for efficiency if the function is called multiple times.
    # re.fullmatch ensures that the *entire* string matches the pattern, not just a substring.
    email_regex_pattern = re.compile(
        r"^[a-zA-Z0-9._%+-]+"  # Local part
        r"@"                   # Separator
        r"[a-zA-Z0-9]"         # Domain label start
        r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?" # Domain label middle/end (optional, max 63 chars per label total)
        r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*" # Subdomains (zero or more)
        r"\."                  # TLD separator
        r"[a-zA-Z]{2,}$"       # TLD (at least 2 letters)
    )

    return bool(email_regex_pattern.fullmatch(email))

# add this ad the end of the file
EXPORT_FUNCTION = validate_email_complex_re