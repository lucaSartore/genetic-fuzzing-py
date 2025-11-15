# necessary imports (use only the python standard libraries)
from collections import deque
from typing import List, Set

# you can define other auxiliary functions (none needed for this problem)

def word_ladder(begin_word: str, end_word: str, word_list: List[str]) -> List[str]:
    """
    Finds the shortest transformation sequence from 'begin_word' to 'end_word' using BFS.

    A transformation sequence is a sequence of words begin_word -> s1 -> s2 -> ... -> sk -> end_word
    such that:
    1. Every adjacent pair of words differs by a single letter.
    2. Every s_i for 1 <= i <= k is in word_list. Note that begin_word does not need to be in word_list.
    3. end_word is in word_list.

    Args:
        begin_word: The starting word of the transformation sequence.
        end_word: The target word of the transformation sequence.
        word_list: A list of valid words that can be used for transformations.

    Returns:
        A list of strings representing the shortest transformation sequence.
        Returns an empty list if no such sequence exists.
    """
    # Convert word_list to a set for O(1) average time lookup.
    word_set: Set[str] = set(word_list)

    # Edge case: If the end_word is not in the word_set, it's impossible to reach.
    if end_word not in word_set:
        return []

    # Edge case: If begin_word is the same as end_word, the path is just the word itself.
    # This also handles the case where begin_word might not be in word_set, but is the target.
    if begin_word == end_word:
        return [begin_word]

    # Initialize the BFS queue. Each element is a tuple: (current_word, current_path_list)
    # The path_list stores the sequence of words from begin_word to current_word.
    queue: deque = deque([(begin_word, [begin_word])])

    # Initialize a set to keep track of visited words to avoid cycles and redundant processing.
    # Add begin_word to visited as it's the starting point.
    visited: Set[str] = {begin_word}

    # BFS traversal
    while queue:
        current_word, current_path = queue.popleft()

        # Generate all possible one-letter transformations from current_word
        for i in range(len(current_word)):
            # Try replacing the character at position 'i' with every letter from 'a' to 'z'
            for char_code in range(ord('a'), ord('z') + 1):
                next_char = chr(char_code)

                # Skip if the character is the same as the original, no change.
                if next_char == current_word[i]:
                    continue

                # Form the next_word by replacing the character at index 'i'
                next_word = current_word[:i] + next_char + current_word[i+1:]

                # If the next_word is the end_word, we have found the shortest path.
                # BFS guarantees the first time we find end_word, it's the shortest path.
                if next_word == end_word:
                    return current_path + [end_word]

                # If next_word is a valid word from word_set AND hasn't been visited yet
                if next_word in word_set and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, current_path + [next_word]))

    # If the queue becomes empty and end_word was never reached, no transformation sequence exists.
    return []

# add this at the end of the file
EXPORT_FUNCTION = word_ladder