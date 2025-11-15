# necessary imports (use only the python standard libraries)
# No special imports are needed as 'list' and 'set' are built-in types.

def n_queens_solver(n: int) -> list[list[str]]:
    """
    Finds all distinct solutions to the N-Queens puzzle using backtracking.

    A solution is represented as a list of strings, where each string represents a row
    of the N x N chessboard. 'Q' denotes a queen, and '.' denotes an empty space.

    Args:
        n: The size of the chessboard (N x N) and the number of queens to place.

    Returns:
        A list of all distinct solutions. Each solution is itself a list of N strings.
        Returns an empty list if n < 1 (no valid board or queens).
        For n = 0, it returns [[]] representing an empty board with 0 queens placed.
    """
    if n < 0:
        return []
    if n == 0:
        return [[]] # Represents an empty board with 0 queens

    results: list[list[str]] = []

    # current_placement[r] = c means a queen is placed at (row r, column c)
    # Initialized to -1 to indicate no queen is placed yet in any row.
    current_placement: list[int] = [-1] * n

    # Sets for O(1) conflict checking:
    # occupied_cols: stores column indices that are already taken.
    # occupied_diag1: stores (row - col) values for cells that are on a main diagonal (top-left to bottom-right).
    # occupied_diag2: stores (row + col) values for cells that are on an anti-diagonal (top-right to bottom-left).
    occupied_cols: set[int] = set()
    occupied_diag1: set[int] = set() # r - c
    occupied_diag2: set[int] = set() # r + c

    def backtrack(row: int) -> None:
        """
        Recursive helper function to place queens row by row.

        Args:
            row: The current row we are trying to place a queen in.
        """
        # Base case: If we have successfully placed queens in all N rows (0 to N-1),
        # we have found a valid solution.
        if row == n:
            solution: list[str] = []
            for r in range(n):
                col_index = current_placement[r]
                row_str_list: list[str] = ["."] * n
                row_str_list[col_index] = "Q"
                solution.append("".join(row_str_list))
            results.append(solution)
            return

        # Recursive step: Try to place a queen in the current 'row'
        # by iterating through all possible columns 'col'.
        for col in range(n):
            # Check for conflicts:
            # 1. Is the column already occupied?
            # 2. Is the main diagonal (row - col) already occupied?
            # 3. Is the anti-diagonal (row + col) already occupied?
            if col in occupied_cols or \
               (row - col) in occupied_diag1 or \
               (row + col) in occupied_diag2:
                # If there's a conflict, this position is not safe,
                # so move to the next column.
                continue

            # If the position (row, col) is safe, place the queen:
            current_placement[row] = col
            occupied_cols.add(col)
            occupied_diag1.add(row - col)
            occupied_diag2.add(row + col)

            # Recurse: Try to place a queen in the next row.
            backtrack(row + 1)

            # Backtrack: After the recursive call returns (either a solution was found
            # or all possibilities for subsequent rows were explored from this state),
            # remove the queen from (row, col) to explore other possibilities
            # for the current 'row'.
            occupied_cols.remove(col)
            occupied_diag1.remove(row - col)
            occupied_diag2.remove(row + col)
            current_placement[row] = -1 # Reset the placement for this row

    # Start the backtracking process from the first row (row 0).
    backtrack(0)
    return results

# add this ad the end of the file
EXPORT_FUNCTION = n_queens_solver