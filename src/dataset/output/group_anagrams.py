# necessary imports (use only the python standard libraries)
from collections import defaultdict

# you can define other auxiliary functions

def group_anagrams(strings: list[str]) -> list[list[str]]:
    """
    Groups a list of strings into lists of anagrams.

    Args:
        strings: A list of strings to be grouped.

    Returns:
        A list of lists of strings, where each inner list contains strings
        that are anagrams of each other.
    """
    # A defaultdict is used to automatically create an empty list for a key
    # if it doesn't exist when we try to append to it.
    anagram_map: defaultdict[str, list[str]] = defaultdict(list)

    for word in strings:
        # Create a canonical representation for each word by sorting its characters.
        # For example, "eat", "tea", "ate" all become "aet".
        sorted_word_key = "".join(sorted(word))
        
        # Add the original word to the list corresponding to its sorted key.
        anagram_map[sorted_word_key].append(word)
    
    # Return the values of the dictionary, which are the lists of anagrams.
    return list(anagram_map.values())

# add this ad the end of the file
EXPORT_FUNCTION = group_anagrams