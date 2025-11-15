# necessary imports (use only the python standard libraries)
from itertools import permutations as it_permutations
from typing import List, TypeVar

# Define a generic type variable for type hinting, allowing the list to contain any type of elements.
T = TypeVar('T')

# you can define other auxiliary functions

def permutations(input_list: List[T]) -> List[List[T]]:
    """
    Generates all possible permutations of a list.

    This function utilizes the `itertools.permutations` function from
    Python's standard library, which is an efficient way to generate
    all possible orderings (permutations) of the elements in the given
    input list.

    Args:
        input_list: The list for which to generate permutations.
                    Elements in the list can be of any type (T).

    Returns:
        A list of lists, where each inner list represents a unique
        permutation of the input_list. The order of permutations
        in the output list is not guaranteed to be stable.

    Examples:
        >>> permutations([1, 2])
        [[1, 2], [2, 1]]
        >>> permutations(['a', 'b', 'c'])
        [['a', 'b', 'c'], ['a', 'c', 'b'], ['b', 'a', 'c'],
         ['b', 'c', 'a'], ['c', 'a', 'b'], ['c', 'b', 'a']]
        >>> permutations([])
        [[]]
        >>> permutations([1])
        [[1]]
    """
    # itertools.permutations returns an iterator of tuples,
    # where each tuple is a permutation of the input_list.
    all_perms_tuples = it_permutations(input_list)

    # Convert each tuple permutation to a list and collect all of them
    # into a single list of lists, as specified by the return type hint.
    result = [list(p) for p in all_perms_tuples]

    return result

# add this ad the end of the file
EXPORT_FUNCTION = permutations