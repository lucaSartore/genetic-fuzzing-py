# no necessary imports needed from standard libraries for this problem

def letter_combinations_of_phone_number(digits: str) -> list[str]:
    """
    Generates all possible letter combinations that the number could represent
    from a given string of digits (2-9 inclusive) using a backtracking approach.

    Args:
        digits: A string containing digits from '2' through '9'.

    Returns:
        A list of all possible letter combinations. If the input `digits` string
        is empty, an empty list is returned.
    """
    if not digits:
        return []

    # Mapping of digits to letters on a phone keypad
    mapping = {
        '2': "abc",
        '3': "def",
        '4': "ghi",
        '5': "jkl",
        '6': "mno",
        '7': "pqrs",
        '8': "tuv",
        '9': "wxyz"
    }

    result: list[str] = []
    # current_combination will store the letters for the current path being explored
    current_combination: list[str] = []

    def backtrack(index: int) -> None:
        """
        Recursive helper function to explore combinations using backtracking.

        Args:
            index: The current digit index being processed in the `digits` string.
        """
        # Base case: If the current combination length equals the input digit string length,
        # a complete combination has been formed.
        if index == len(digits):
            result.append("".join(current_combination))
            return

        # Get the digit at the current index
        digit = digits[index]
        # Get the corresponding letters for this digit
        letters = mapping[digit]

        # Iterate through each letter for the current digit
        for char in letters:
            # Choose: Add the character to the current combination
            current_combination.append(char)
            # Explore: Recursively call backtrack for the next digit
            backtrack(index + 1)
            # Unchoose (Backtrack): Remove the character to explore other possibilities
            current_combination.pop()

    # Start the backtracking process from the first digit (index 0)
    backtrack(0)
    return result

# add this at the end of the file
EXPORT_FUNCTION = letter_combinations_of_phone_number