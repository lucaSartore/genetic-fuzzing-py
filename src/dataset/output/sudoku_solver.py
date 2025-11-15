# necessary imports (use only the python standard libraries)
# No special imports needed for this function, as it uses basic list operations.

def sudoku_solver(board: list[list[int]]) -> bool:
    """
    Solves a Sudoku puzzle using the backtracking algorithm.

    Modifies the input `board` in-place to contain the solution.
    A 0 in the board represents an empty cell.

    Args:
        board: A 9x9 list of lists representing the Sudoku board.
               Each inner list represents a row.
               Numbers 1-9 represent filled cells, 0 represents empty cells.

    Returns:
        True if a solution is found and the board is modified in-place,
        False if no solution exists for the given board.
    """

    def find_empty(current_board: list[list[int]]) -> tuple[int, int] | None:
        """
        Finds the next empty cell (represented by 0) on the board.

        Args:
            current_board: The current state of the Sudoku board.

        Returns:
            A tuple (row, col) of the empty cell, or None if no empty cells are found.
        """
        for r in range(9):
            for c in range(9):
                if current_board[r][c] == 0:
                    return (r, c)
        return None

    def is_valid(current_board: list[list[int]], num: int, pos: tuple[int, int]) -> bool:
        """
        Checks if placing 'num' at 'pos' (row, col) is valid according to Sudoku rules.

        Args:
            current_board: The current state of the Sudoku board.
            num: The number (1-9) to check for placement.
            pos: A tuple (row, col) representing the position to check.

        Returns:
            True if 'num' can be placed at 'pos', False otherwise.
        """
        row, col = pos

        # Check row
        for c in range(9):
            if current_board[row][c] == num and col != c:
                return False

        # Check column
        for r in range(9):
            if current_board[r][col] == num and row != r:
                return False

        # Check 3x3 box
        # Determine the start of the 3x3 box
        box_start_row = (row // 3) * 3
        box_start_col = (col // 3) * 3

        for r_offset in range(3):
            for c_offset in range(3):
                current_r = box_start_row + r_offset
                current_c = box_start_col + c_offset
                if current_board[current_r][current_c] == num and (current_r, current_c) != pos:
                    return False

        return True

    # Main backtracking logic
    empty_pos = find_empty(board)

    # Base case: If no empty position is found, the puzzle is solved.
    if not empty_pos:
        return True

    row, col = empty_pos

    # Try numbers from 1 to 9
    for num_to_try in range(1, 10):
        if is_valid(board, num_to_try, (row, col)):
            board[row][col] = num_to_try  # Place the number

            # Recursively try to solve the rest of the board
            if sudoku_solver(board):
                return True  # If a solution is found, propagate True

            # If the recursive call returns False, it means 'num_to_try'
            # at (row, col) didn't lead to a solution. Backtrack.
            board[row][col] = 0  # Reset the cell to empty

    # If no number from 1 to 9 works for the current empty cell,
    # then this path is invalid, so return False.
    return False

# add this ad the end of the file
EXPORT_FUNCTION = sudoku_solver