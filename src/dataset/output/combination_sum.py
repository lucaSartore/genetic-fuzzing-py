# necessary imports (use only the python standard libraries)

def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """
    Finds all unique combinations from 'candidates' that sum to 'target'.
    Numbers in 'candidates' can be reused.

    Args:
        candidates: A list of unique integers (can be positive).
                    Note: Even if candidates contains duplicates, this function
                    will still produce unique combinations of values.
        target: The target sum (a positive integer).

    Returns:
        A list of lists of integers, where each inner list is a unique
        combination of numbers from 'candidates' that sums to 'target'.
        The combinations are sorted in non-decreasing order.
    """
    results = []
    current_combination = []

    # Sort candidates to handle potential duplicates in the input (if any)
    # and to ensure combinations are generated in non-decreasing order.
    # This also helps in pruning duplicate combinations effectively.
    candidates.sort()

    def backtrack(remaining_target: int, start_index: int):
        """
        Recursive helper function for backtracking.

        Args:
            remaining_target: The remaining sum we need to achieve.
            start_index: The index in 'candidates' from which we can start picking numbers.
                         This is crucial to avoid duplicate combinations
                         (e.g., [2,3] vs [3,2]) and allows reusing numbers
                         by passing 'i' instead of 'i + 1'.
        """
        # Base case 1: If the remaining target is 0, we found a valid combination.
        if remaining_target == 0:
            results.append(list(current_combination))  # Append a copy of the current combination
            return

        # Base case 2: If the remaining target is negative, this path is invalid.
        if remaining_target < 0:
            return

        # Explore possible candidates
        for i in range(start_index, len(candidates)):
            candidate = candidates[i]

            # Optimization (pruning): If the current candidate is already greater
            # than the remaining target, then all subsequent candidates (since
            # the list is sorted) will also be greater. So, we can stop this branch.
            if candidate > remaining_target:
                break

            # Choose: Add the current candidate to our combination
            current_combination.append(candidate)

            # Recurse: Call backtrack with the updated remaining target and
            # allow reusing the current candidate by passing `i` as the
            # next start_index. If each number could be used at most once,
            # we would pass `i + 1`.
            backtrack(remaining_target - candidate, i)

            # Unchoose (Backtrack): Remove the candidate to explore other possibilities
            current_combination.pop()

    # Start the backtracking process from the beginning of the candidates list
    backtrack(target, 0)
    return results

# add this ad the end of the file
EXPORT_FUNCTION = combination_sum