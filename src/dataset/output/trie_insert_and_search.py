# necessary imports (use only the python standard libraries)
# No specific imports are needed for this implementation, as it relies on
# built-in dictionary and list operations.

def trie_insert_and_search(words: list[str], prefixes: list[str]) -> list[bool]:
    """
    Builds a Trie (as a nested dictionary) from a list of 'words'
    and then checks if a list of 'prefixes' exist within that Trie.

    The Trie is represented as a nested dictionary where each key is a character,
    and its value is another dictionary representing the next level in the Trie.
    The existence of a path from the root to a certain node signifies a prefix.

    Args:
        words: A list of strings (words) to be inserted into the Trie.
               Each character in a word will form a node in the Trie.
        prefixes: A list of strings (prefixes) to check for their existence
                  within the built Trie.

    Returns:
        A list of booleans. Each boolean corresponds to a prefix in the
        'prefixes' list, indicating whether that prefix exists in the Trie.
        True means the prefix exists, False means it does not.
    """
    trie: dict = {}  # The root of the Trie, an empty dictionary.

    # 1. Build the Trie from the 'words' list
    for word in words:
        current_node = trie
        for char in word:
            # If the character is not a key in the current node, create a new sub-dictionary for it
            if char not in current_node:
                current_node[char] = {}
            # Move deeper into the Trie
            current_node = current_node[char]
        # For the purpose of checking prefix existence, we don't strictly need to
        # mark the end of a word. The path's existence is sufficient.
        # However, if this Trie were to also support checking for full words,
        # a marker like current_node['__is_word__'] = True would be added here.

    # 2. Check if each 'prefix' exists in the built Trie
    results: list[bool] = []
    for prefix in prefixes:
        current_node = trie
        found_prefix = True
        for char in prefix:
            # If the character is not found in the current node, the prefix does not exist
            if char not in current_node:
                found_prefix = False
                break  # No need to check further characters for this prefix
            # Move deeper into the Trie to follow the prefix path
            current_node = current_node[char]
        
        # After iterating through all characters of the prefix (or breaking early),
        # 'found_prefix' indicates whether the full prefix path was found.
        results.append(found_prefix)

    return results

# add this ad the end of the file
EXPORT_FUNCTION = trie_insert_and_search