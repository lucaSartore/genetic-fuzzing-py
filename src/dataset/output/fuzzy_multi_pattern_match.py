# necessary imports (use only the python standard libraries)
import collections
import functools
from typing import Any, List, Tuple, Callable

# you can define other auxiliary functions

def _levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculates the Levenshtein distance (edit distance) between two strings.
    This is a standard dynamic programming approach optimized for space.
    """
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    # Initialize the previous row of the DP table
    prev_row: List[int] = list(range(len(s2) + 1))

    for i in range(1, len(s1) + 1):
        current_row: List[int] = [i] * (len(s2) + 1) # First element is dist(s1[0..i-1], "") = i
        for j in range(1, len(s2) + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            current_row[j] = min(
                current_row[j-1] + 1,  # Deletion (s1[i-1] deleted from s1 to match s2[0..j-1])
                prev_row[j] + 1,       # Insertion (s2[j-1] inserted into s1[0..i-1] to match s2[0..j-1])
                prev_row[j-1] + cost   # Substitution or Match
            )
        prev_row = current_row
    
    return prev_row[len(s2)]


class _Match:
    """
    Internal class to represent a potential match with all relevant details
    for fuzzy matching and overlap resolution.
    """
    def __init__(self,
                 pattern_string: str,
                 pattern_id: Any,
                 pattern_index: int, # Original index of pattern in the input list
                 matched_string: str,
                 start: int,
                 end: int,
                 distance: int):
        self.pattern_string = pattern_string
        self.pattern_id = pattern_id
        self.pattern_index = pattern_index
        self.matched_string = matched_string
        self.start = start
        self.end = end
        self.distance = distance
        self.length = len(matched_string)
        self.is_exact = (distance == 0)

    def __repr__(self) -> str:
        return (f"_Match(id={self.pattern_id!r}, matched='{self.matched_string}', "
                f"[{self.start}:{self.end}], dist={self.distance}, "
                f"pattern_str='{self.pattern_string}')")

    def overlaps_with(self, other: '_Match') -> bool:
        """
        Checks if this match's interval overlaps with another match's interval.
        [start, end) where end is exclusive.
        """
        # Overlap exists if the start of one interval is before the end of the other,
        # AND the end of the one is after the start of the other.
        return max(self.start, other.start) < min(self.end, other.end)

    def to_output_format(self) -> Tuple[str, Any, int, int, int]:
        """
        Converts the internal match object to the required output format.
        """
        return (self.matched_string, self.pattern_id, self.start, self.end, self.distance)


def _compare_matches_priority(m1: '_Match', m2: '_Match', priority_rules: List[str]) -> int:
    """
    Compares two _Match objects based on a list of priority rules.
    This function is intended to be used with `functools.cmp_to_key` for sorting.

    Args:
        m1: The first _Match object to compare.
        m2: The second _Match object to compare.
        priority_rules: A list of rule strings specifying the order of precedence.

    Returns:
        1 if m1 has higher priority than m2 (m1 should come before m2 in a descending sort).
        -1 if m2 has higher priority than m1 (m2 should come before m1).
        0 if their priorities are equal based on the given rules.
    """
    for rule in priority_rules:
        if rule == "exact_first":
            if m1.is_exact and not m2.is_exact: return 1
            if not m1.is_exact and m2.is_exact: return -1
        elif rule == "min_distance":
            if m1.distance < m2.distance: return 1
            if m1.distance > m2.distance: return -1
        elif rule == "longest_match":
            if m1.length > m2.length: return 1
            if m1.length < m2.length: return -1
        elif rule == "shortest_match":
            if m1.length < m2.length: return 1
            if m1.length > m2.length: return -1
        elif rule == "pattern_order":
            # Patterns that appeared earlier in the input list have higher priority
            if m1.pattern_index < m2.pattern_index: return 1
            if m1.pattern_index > m2.pattern_index: return -1
        elif rule == "text_occurrence_first":
            # Match that starts earliest in the text has higher priority
            if m1.start < m2.start: return 1
            if m1.start > m2.start: return -1
        elif rule == "text_occurrence_last":
            # Match that starts latest in the text has higher priority
            if m1.start > m2.start: return 1
            if m1.start < m2.start: return -1
        # If no distinction is made by the current rule, continue to the next rule.
    
    # If all explicit priority rules result in a tie, use stable tie-breakers
    # to ensure deterministic output when patterns have truly identical properties
    # according to the given rules.
    if m1.length < m2.length: return 1 # Prefer shorter to allow more surrounding matches
    if m1.length > m2.length: return -1
    if m1.start < m2.start: return 1   # Prefer earlier occurrence
    if m1.start > m2.start: return -1
    if m1.end < m2.end: return 1       # Prefer earlier end if start is same
    if m1.end > m2.end: return -1
    if m1.pattern_index < m2.pattern_index: return 1 # Fallback to original pattern order
    if m1.pattern_index > m2.pattern_index: return -1

    return 0 # The matches are considered equal by all rules and tie-breakers.


def fuzzy_multi_pattern_match(
    text: str,
    patterns: List[Tuple[str, Any, int]],
    priority_rules: List[str]
) -> List[Tuple[str, Any, int, int, int]]:
    """
    Matches multiple patterns in a text with edit distance thresholds and applies
    priority rules to resolve overlapping matches, returning a set of non-overlapping
    matches.

    This function generates all possible fuzzy matches for each pattern within the text,
    then sorts these potential matches based on user-defined priority rules. Finally,
    it applies a greedy algorithm to select a non-overlapping set of matches,
    prioritizing higher-ranked matches.

    Args:
        text: The input string to search within.
        patterns: A list of patterns, where each pattern is a tuple:
                  (pattern_string: str, pattern_id: Any, max_edit_distance: int).
                  `pattern_string` is the string to be matched (e.g., "apple").
                  `pattern_id` is an identifier or payload associated with the pattern
                  (e.g., "FRUIT_APPLE", 123).
                  `max_edit_distance` is the maximum allowed Levenshtein distance
                  for this specific pattern (e.g., 1 for "apple" to match "aple").
        priority_rules: A list of strings defining the precedence for resolving
                        overlapping matches. Rules are applied in the order they
                        appear in this list (first rule has highest priority).
                        If a tie occurs at one rule, the next rule is considered.
                        Supported rule strings:
                        - "exact_first": Prioritizes matches with an edit distance of 0
                                         over fuzzy matches.
                        - "min_distance": Prioritizes matches with the smallest
                                          edit distance.
                        - "longest_match": Prioritizes matches that cover a longer
                                           segment of the text.
                        - "shortest_match": Prioritizes matches that cover a shorter
                                            segment of the text.
                        - "pattern_order": Prioritizes patterns that appeared earlier
                                           in the input `patterns` list.
                        - "text_occurrence_first": Prioritizes matches that start
                                                   at an earlier index in the text.
                        - "text_occurrence_last": Prioritizes matches that start
                                                  at a later index in the text.
                        If all specified rules result in a tie, additional internal
                        tie-breakers (shorter length, earlier start index, earlier
                        end index, original pattern index) are used to ensure
                        deterministic output.

    Returns:
        A list of tuples, each representing a selected non-overlapping match.
        Matches are ordered by their starting position in the text.
        Each tuple contains:
        (matched_string: str, pattern_id: Any, start_index: int, end_index: int, edit_distance: int).
        `matched_string` is the actual substring from `text` that was matched.
        `pattern_id` is the identifier of the pattern that matched.
        `start_index` is the 0-based starting position of the match in `text`.
        `end_index` is the exclusive ending position of the match in `text`.
        `edit_distance` is the calculated Levenshtein distance for this match.
    """
    if not text or not patterns:
        return []

    all_candidate_matches: List[_Match] = []
    text_len = len(text)

    # 1. Generate all potential matches that satisfy the edit distance thresholds
    for pattern_idx, (pattern_str, pattern_id, max_dist) in enumerate(patterns):
        if not pattern_str: # Skip empty pattern strings
            continue

        # Iterate through possible substring lengths. A substring's length must be
        # within `max_dist` of the pattern's length for a match to be possible.
        min_len_to_check = max(1, len(pattern_str) - max_dist)
        max_len_to_check = len(pattern_str) + max_dist

        for start_idx in range(text_len):
            for length in range(min_len_to_check, max_len_to_check + 1):
                end_idx = start_idx + length
                if end_idx > text_len:
                    break # Substring would go out of bounds

                substring = text[start_idx:end_idx]
                distance = _levenshtein_distance(pattern_str, substring)

                if distance <= max_dist:
                    match = _Match(pattern_str, pattern_id, pattern_idx,
                                   substring, start_idx, end_idx, distance)
                    all_candidate_matches.append(match)
    
    if not all_candidate_matches:
        return []

    # 2. Sort all candidate matches by the defined priority rules.
    # We use functools.cmp_to_key with our custom comparison function.
    # _compare_matches_priority returns 1 if m1 has higher priority.
    # To get higher priority items first in the sorted list, we use `reverse=True`.
    all_candidate_matches.sort(key=functools.cmp_to_key(
        lambda m1, m2: _compare_matches_priority(m1, m2, priority_rules)
    ), reverse=True)

    # 3. Resolve overlaps using a greedy approach:
    # Iterate through the sorted candidates (highest priority first).
    # Add a candidate to final matches if it does not overlap with any
    # already accepted (and thus higher or equally prioritized) matches.
    final_matches: List[_Match] = []
    
    for candidate in all_candidate_matches:
        is_overlapping = False
        for final_match in final_matches:
            if candidate.overlaps_with(final_match):
                is_overlapping = True
                break
        
        if not is_overlapping:
            final_matches.append(candidate)
    
    # 4. Sort the final selected matches by their start index for consistent output order.
    final_matches.sort(key=lambda m: m.start)

    # 5. Convert the internal _Match objects to the required output format.
    return [m.to_output_format() for m in final_matches]

# add this at the end of the file
EXPORT_FUNCTION = fuzzy_multi_pattern_match