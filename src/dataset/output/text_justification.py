# necessary imports (use only the python standard libraries)
# No special imports are needed, only built-in types and functions.

# you can define other auxiliary functions

def text_justification(words: list[str], width: int) -> list[str]:
    """
    Takes a list of words and a width, and returns a list of fully justified text lines.

    The function first groups words into lines, ensuring no line exceeds the given width
    (unless a single word itself is longer than the width). Then, it justifies each line:
    - The last line, or any line with a single word, is left-justified.
    - All other lines are fully justified, distributing spaces as evenly as possible
      between words. If spaces cannot be distributed perfectly evenly, extra spaces
      are added to the gaps from left to right.

    Args:
        words: A list of strings, where each string is a word.
        width: An integer representing the maximum width of each line.

    Returns:
        A list of strings, where each string is a fully justified text line.
        Lines containing a single word longer than `width` will exceed `width`.
    """

    # Phase 1: Group words into lines based on the given width
    # Each item in 'lines' will be a list of words that belong on that line.
    lines: list[list[str]] = []
    current_line_words: list[str] = []
    
    # current_line_length tracks the total character length of words + minimum 1 space between words.
    # For example, if current_line_words = ["This", "is"], current_line_length = len("This") + 1 + len("is") = 4 + 1 + 2 = 7.
    current_line_length: int = 0 

    for word in words:
        if not current_line_words:
            # If it's the first word on a new line
            current_line_words.append(word)
            current_line_length = len(word)
        else:
            # Check if adding the word (plus a space) exceeds the width.
            # current_line_length already represents the length of the current line with its words and spaces.
            # Adding a new word requires 1 more space and the length of the new word.
            length_if_added = current_line_length + 1 + len(word)
            
            if length_if_added <= width:
                # The word fits on the current line
                current_line_words.append(word)
                current_line_length = length_if_added
            else:
                # The word does not fit, so we finalize the current line and start a new one.
                lines.append(current_line_words)
                current_line_words = [word]
                current_line_length = len(word)
    
    # After iterating through all words, add the last accumulated line if it's not empty.
    if current_line_words:
        lines.append(current_line_words)

    # Phase 2: Justify each line according to the rules
    justified_lines: list[str] = []
    num_lines = len(lines)

    for i, line_words in enumerate(lines):
        is_last_line = (i == num_lines - 1)
        num_words_on_line = len(line_words)
        total_chars_in_words = sum(len(w) for w in line_words)

        if num_words_on_line == 1 or is_last_line:
            # Rule: Single word lines or the very last line are left-justified.
            justified_line = " ".join(line_words)
            justified_lines.append(justified_line.ljust(width))
        else:
            # Rule: Multiple words, not the last line - fully justify.
            total_spaces_to_distribute = width - total_chars_in_words
            num_gaps = num_words_on_line - 1 # Number of spaces to fill between words

            # Calculate base spaces for each gap and any extra spaces that need to be distributed.
            base_spaces = total_spaces_to_distribute // num_gaps
            extra_spaces_count = total_spaces_to_distribute % num_gaps

            current_justified_line_parts: list[str] = []
            for j, word in enumerate(line_words):
                current_justified_line_parts.append(word)
                if j < num_gaps: # If it's not the last word on the line
                    # Determine spaces for the current gap: base spaces plus one extra space if available.
                    spaces_for_this_gap = base_spaces + (1 if j < extra_spaces_count else 0)
                    current_justified_line_parts.append(" " * spaces_for_this_gap)
            
            justified_lines.append("".join(current_justified_line_parts))
            
    return justified_lines

# add this at the end of the file
EXPORT_FUNCTION = text_justification
