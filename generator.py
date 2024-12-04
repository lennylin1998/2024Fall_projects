import random
import copy


# Binox Generator Function
def binox_generator(size=6):
    """
    Generate a Binox board that satisfies the rule:
    - No more than two consecutive identical symbols ("X" or "O") in any row or column.
    - Ensure no empty spaces ('_') remain.
    """

    def is_valid(board, row, col, symbol):
        """Check if placing the symbol at (row, col) is valid."""
        # Check row constraints
        if col > 1 and board[row][col - 1] == board[row][col - 2] == symbol:
            return False
        if col > 0 and col < size - 1 and board[row][col - 1] == board[row][col + 1] == symbol:
            return False

        # Check column constraints
        if row > 1 and board[row - 1][col] == board[row - 2][col] == symbol:
            return False
        if row > 0 and row < size - 1 and board[row - 1][col] == board[row + 1][col] == symbol:
            return False

        return True

    while True:  # Keep regenerating until we succeed
        # Initialize an empty board
        board = [["_" for _ in range(size)] for _ in range(size)]

        for row in range(size):
            for col in range(size):
                symbol = random.choice(["X", "O"])
                # Try to place a valid symbol
                if is_valid(board, row, col, symbol):
                    board[row][col] = symbol
                else:
                    # Try the other symbol
                    symbol = "O" if symbol == "X" else "X"
                    if is_valid(board, row, col, symbol):
                        board[row][col] = symbol

        # Check if the board is fully filled
        if all("_" not in row for row in board):
            return board  # Successfully generated a valid board


# Function to remove pieces from the board
def remove_pieces(board, fraction=2 / 3):
    """
    Randomly remove more than `fraction` of the pieces from the board.
    """

    new_board = copy.deepcopy(board)
    size = len(new_board)
    total_pieces = size * size
    pieces_to_remove = int(total_pieces * fraction) + 1  # Ensure more than fraction is removed

    # Flatten the board to get all positions
    positions = [(row, col) for row in range(size) for col in range(size)]
    random.shuffle(positions)

    # Remove pieces
    for _ in range(pieces_to_remove):
        row, col = positions.pop()
        new_board[row][col] = "_"

    return new_board


# Function to generate row hints from the original board
def row_hints(board, num_hints=3):
    """
    Provide hints for a few rows, indicating the number of 'X' and 'O' in those rows.
    """
    size = len(board)
    chosen_rows = random.sample(range(size), num_hints)
    hints = {}
    for row in chosen_rows:
        x_count = board[row].count("X")
        o_count = board[row].count("O")
        hints[row] = (x_count, o_count)
    return hints


# Function to check if the board has a unique solution based on hints
# Function to check if the board has a unique solution based on hints
# Function to check if the board has a unique solution based on hints
def is_unique(board, size, hints):
    #print("1")
    """
    Check if a valid and unique solution exists based on the hints and partially removed board.
    This function tries to restore the board and checks if there's more than one valid solution.
    """

    # Helper function to check if the current board satisfies the row constraints
    def satisfies_constraints(board):
        for row in range(size):
            x_count = board[row].count("X")
            o_count = board[row].count("O")
            # Check row hints
            if row in hints and (x_count != hints[row][0] or o_count != hints[row][1]):
                return False
        return True

    # Backtracking to restore the board with the available hints
    def backtrack(board, row, col):
        # If we've reached the end of the board
        if row == size:
            print("\nFound a valid solution:")
            for r in board:
                print(" ".join(r))  # Print the current valid solution
            return [copy.deepcopy(board)]  # Found a valid solution

        # Move to the next row if we're at the end of a column
        if col == size:
            return backtrack(board, row + 1, 0)

        # Skip filled cells
        if board[row][col] != "_":
            return backtrack(board, row, col + 1)

        solutions = []

        # Try placing 'X' and 'O' at the current position
        for symbol in ["X", "O"]:
            print("1")
            board[row][col] = symbol
            if satisfies_constraints(board):  # Check constraints after placing symbol
                solutions.extend(backtrack(board, row, col + 1))  # Explore next cells
                print(f"Solution found: {solutions}")
            board[row][col] = "_"

        return solutions

    # Initialize board for backtracking
    board_copy = copy.deepcopy(board)
    solutions = backtrack(board_copy, 0, 0)
    print(f"Solution found: {solutions}")

    # If more than one solution is found, return False (i.e., multiple solutions found)
    if len(solutions) > 1:
        print("\nMultiple solutions found.")
        return False  # Multiple solutions found
    else:
        print("\nUnique solution found.")
        return True  # Only one solution found


# Main Function to generate a board and verify its uniqueness
def main():
    # Generate a Binox board
    original_board = binox_generator(size=6)
    print("Original Board:")
    for row in original_board:
        print(" ".join(row))

    # Remove pieces and display the new board
    modified_board = remove_pieces(original_board, fraction=2 / 3)
    print("\nBoard with Removed Pieces:")
    for row in modified_board:
        print(" ".join(row))

    # Provide hints for a few rows from the original (correct) board
    hints = row_hints(original_board, num_hints=3)
    print("\nRow Hints (from the correct board):")
    for row, (x_count, o_count) in hints.items():
        print(f"Row {row + 1}: {x_count} X, {o_count} O")

    # Check if the board with removed pieces and hints has a unique solution
    valid = is_unique(modified_board, 6, hints)
    if valid:
        print("\nA unique solution exists!")
    else:
        print("\nMultiple or no solutions exist!")


if __name__ == "__main__":
    main()

