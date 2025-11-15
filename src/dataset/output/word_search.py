# No specific imports are needed for this problem as it uses basic data structures and recursion.

def word_search(board: list[list[str]], word: str) -> bool:
    """
    Finds a word in a 2D grid of characters using a backtracking (Depth-First Search) approach.

    The word can be constructed from letters of sequentially adjacent cells, where
    "adjacent" cells are those horizontally or vertically neighboring. The same
    letter cell may not be used more than once within the same word search path.

    Args:
        board: A 2D list of characters representing the grid.
        word: The string word to search for in the grid.

    Returns:
        True if the word is found in the grid, False otherwise.
    """
    if not word:
        return True  # An empty word is always considered found

    if not board or not board[0]:
        return False  # Cannot find a non-empty word in an empty or malformed board

    ROWS, COLS = len(board), len(board[0])
    
    # Define a helper recursive function for DFS backtracking
    def _dfs(r: int, c: int, k: int) -> bool:
        """
        Performs a Depth-First Search (DFS) starting from (r, c) to find the k-th
        character of the word.

        Args:
            r: Current row index.
            c: Current column index.
            k: Current index of the character in `word` that we are trying to match.

        Returns:
            True if the remaining part of the word is found from this position,
            False otherwise.
        """
        # Base case 1: If we have successfully matched all characters in the word
        if k == len(word):
            return True

        # Base case 2: If current position is out of bounds, or
        # the character at board[r][c] does not match word[k], or
        # the cell has already been visited in the current path (marked as '#')
        if not (0 <= r < ROWS and 0 <= c < COLS) or board[r][c] != word[k]:
            return False

        # Mark the current cell as visited by temporarily changing its character.
        # This prevents using the same cell twice in the same path.
        original_char = board[r][c]
        board[r][c] = '#'  # Use a sentinel character to mark as visited

        # Explore all four adjacent directions (up, down, left, right)
        found = (_dfs(r + 1, c, k + 1) or  # Move down
                 _dfs(r - 1, c, k + 1) or  # Move up
                 _dfs(r, c + 1, k + 1) or  # Move right
                 _dfs(r, c - 1, k + 1))    # Move left

        # Backtrack: Restore the original character of the cell.
        # This is crucial so that other potential paths can use this cell.
        board[r][c] = original_char

        return found

    # Iterate through each cell in the grid to find a potential starting point
    # for the word (i.e., the first character of the word).
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == word[0]:
                if _dfs(r, c, 0):  # Start DFS from this cell
                    return True

    # If no starting point leads to finding the word, return False
    return False

# add this ad the end of the file
EXPORT_FUNCTION = word_search