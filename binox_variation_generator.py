import random
import copy
from collections import Counter


class BinoxVariationGenerator:
    def __init__(self, size):
        self.size = size
        self.board = self.binox_generator(size)
        # Initialize dictionaries to store counters for rows and columns
        self.row_hints = [Counter() for _ in range(self.size)]
        self.col_hints = [Counter() for _ in range(self.size)]
        self.hints_used = {"row": set(), "col": set()}

        # Iterate through the board and update counters
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                self.row_hints[i][cell] += 1
                self.col_hints[j][cell] += 1
        # print(self.row_hints)
        # print(self.col_hints)
        self.create_partial_solved_puzzle()
        while sum([counter["_"] for counter in self.row_counters]) > 0:
            stat = self.gather_statistics()
            print(stat)
            # print("Before modify: ")
            # for row in self.final_puzzle:
            #     print(" ".join(row))
            self.modify_puzzle(stat)
            print("After modify: ")
            self.print_puzzle()
            self.partial_solver()
            print()
            print("After trying solving modified version:")
            self.print_puzzle()

        print("FINAL:")
        print(self.hints_used)
        for row in self.final_puzzle:
            print(" ".join(row))

        # self.row_counters = [Counter() for _ in range(self.size)]
        # self.col_counters = [Counter() for _ in range(self.size)]
        # for i, row in enumerate(self.final_puzzle):
        #     for j, cell in enumerate(row):
        #         self.row_counters[i][cell] += 1
        #         self.col_counters[j][cell] += 1
        # self.game_solver()
        # for row in self.final_puzzle:
        #     print(" ".join(row))
    # Binox Generator Function
    def binox_generator(self, size=6):
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
    def remove_pieces(self, fraction=2 / 3):
        """
        Randomly remove more than `fraction` of the pieces from the board.
        """

        new_board = copy.deepcopy(self.board)
        total_pieces = self.size * self.size
        pieces_to_remove = int(total_pieces * fraction) + 1  # Ensure more than fraction is removed

        # Flatten the board to get all positions
        positions = [(row, col) for row in range(self.size) for col in range(self.size)]
        random.shuffle(positions)

        # Remove pieces
        for _ in range(pieces_to_remove):
            row, col = positions.pop()
            new_board[row][col] = "_"

        return new_board
    def print_puzzle(self):
        for i, row in enumerate(self.puzzle):
            print(" ".join(row) + f" {self.row_hints[i]}")

    def update_counter(self, row, col, mark):
        # print("Counter before: ", self.row_counters, self.col_counters)
        self.row_counters[row][mark] += 1
        self.col_counters[col][mark] += 1

        self.row_counters[row]["_"] -= 1
        self.col_counters[col]["_"] -= 1
        # print("Counter after: ", self.row_counters, self.col_counters)
    
    def create_partial_solved_puzzle(self):
        while True:
            self.puzzle = self.remove_pieces()
            self.final_puzzle = copy.deepcopy(self.puzzle)
            self.row_counters = [Counter() for _ in range(self.size)]
            self.col_counters = [Counter() for _ in range(self.size)]
            for i, row in enumerate(self.puzzle):
                for j, cell in enumerate(row):
                    self.row_counters[i][cell] += 1
                    self.col_counters[j][cell] += 1

            for row in self.board:
                print(" ".join(row))
            # print()
            # self.print_puzzle()
            self.partial_solver()
            # print()
            # self.print_puzzle()
            if self.size * 2 < sum([counter["_"] for counter in self.row_counters]) < self.size * 2.5:
                return

    def game_solver(self):
        can_solve = True
        run_time = 1
        while can_solve:
            can_solve = self.two_adjacent_fill(self.final_puzzle) or self.in_between_fill(self.final_puzzle) or self.hint_fill_with_partial_hints()
            print()
            print("run times: ", run_time)
            print()  
            run_time += 1


    def partial_solver(self):
        run_time = 1
        can_solve = True
        while can_solve:
            can_solve = self.two_adjacent_fill(self.puzzle) or self.in_between_fill(self.puzzle) or self.hint_fill()
            print()
            print("run times: ", run_time)
            print()
            # print("After fill: ")
            # for row in self.puzzle:
            #     print(" ".join(row))
            run_time += 1

    def two_adjacent_fill(self, puzzle) -> bool:
        changes_made = 0
        for i in range(self.size - 2):
            for j in range(self.size):
                k = self.size - 1 - i
                # col
                if (puzzle[i][j] == '_') and (puzzle[i + 1][j] != '_') and (puzzle[i + 1][j] == puzzle[i + 2][j]):
                    puzzle[i][j] = 'X' if puzzle[i + 1][j] == 'O' else 'O'
                    self.update_counter(i, j, puzzle[i][j])
                    changes_made += 1
                    # print(1, (i, j))
                if (puzzle[k][j] == '_') and (puzzle[k - 1][j] != '_') and (puzzle[k - 1][j] == puzzle[k - 2][j]):
                    puzzle[k][j] = 'X' if puzzle[k - 1][j] == 'O' else 'O'
                    self.update_counter(k, j, puzzle[k][j])
                    changes_made += 1
                    # print(2, (k, j))
                # row
                # print(f"j: {j}, i:{i}")
                if (puzzle[j][i] == '_') and (puzzle[j][i + 1] != '_') and (puzzle[j][i + 1] == puzzle[j][i + 2]):
                    puzzle[j][i] = 'X' if puzzle[j][i + 1] == 'O' else 'O'
                    self.update_counter(j, i, puzzle[j][i])
                    changes_made += 1
                    # print(3, (j, i))
                if (puzzle[j][k] == '_') and (puzzle[j][k - 1] != '_') and (puzzle[j][k - 1] == puzzle[j][k - 2]):
                    puzzle[j][k] = 'X' if puzzle[j][k - 1] == 'O' else 'O'
                    self.update_counter(j, k, puzzle[j][k])
                    changes_made += 1
                    # print(4, (j, k))
        # print(self.row_counters)
        # print(self.col_counters)
        return changes_made > 0

    def in_between_fill(self, puzzle) -> bool:
        changes_made = 0
        for i in range(self.size):
            for j in range(1, self.size - 1):
                # col
                if (puzzle[i][j] == '_') and (puzzle[i][j - 1] != '_') and (puzzle[i][j - 1] == puzzle[i][j + 1]):
                    puzzle[i][j] = 'X' if puzzle[i][j - 1] == 'O' else 'O'
                    self.update_counter(i, j, puzzle[i][j])
                    changes_made += 1
                    # print((i, j))
                # row
                if (puzzle[j][i] == '_') and (puzzle[j - 1][i] != '_') and (puzzle[j - 1][i] == puzzle[j + 1][i]):
                    puzzle[j][i] = 'X' if puzzle[j - 1][i] == 'O' else 'O'
                    self.update_counter(j, i, puzzle[j][i])
                    changes_made += 1
                    # print((j, i))
        return changes_made > 0

    def hint_fill(self) -> bool:
        changes_made = 0
        for i in range(self.size):
            if self.row_counters[i]['_'] > 0:
                if self.row_counters[i]['O'] == self.row_hints[i]['O']:
                    for j in range(self.size):
                        if self.puzzle[i][j] == '_':
                            self.puzzle[i][j] = 'X'
                            self.update_counter(i, j, 'X')
                    changes_made += 1
                    self.hints_used["row"].add(i)
                    print(f"last blank on row {i}!")
                elif self.row_counters[i]['X'] == self.row_hints[i]['X']:
                    for j in range(self.size):
                        if self.puzzle[i][j] == '_':
                            self.puzzle[i][j] = 'O'
                            self.update_counter(i, j, 'O')
                    changes_made += 1
                    self.hints_used["row"].add(i)
                    print(f"last blank on row {i}!")
            if self.col_counters[i]['_'] > 0:
                if self.col_counters[i]['O'] == self.col_hints[i]['O']:
                    for j in range(self.size):
                        if self.puzzle[j][i] == '_':
                            self.puzzle[j][i] = 'X'
                            self.update_counter(j, i, 'X')
                    changes_made += 1
                    self.hints_used["col"].add(i)
                    print(f"last blank on col {i}!")
                elif self.col_counters[i]['X'] == self.col_hints[i]['X']:
                    for j in range(self.size):
                        if self.puzzle[j][i] == '_':
                            self.puzzle[j][i] = 'O'
                            self.update_counter(j, i, 'O')
                    changes_made += 1
                    self.hints_used["col"].add(i)
                    print(f"last blank on col {i}!")
        return changes_made > 0

    def hint_fill_with_partial_hints(self):
        changes_made = 0
        for i in range(self.size):
            if self.row_counters[i]['_'] > 0 and (i in self.hints_used["row"]):
                if self.row_counters[i]['O'] == self.row_hints[i]['O']:
                    for j in range(self.size):
                        if self.final_puzzle[i][j] == '_':
                            self.final_puzzle[i][j] = 'X'
                            self.update_counter(i, j, 'X')
                    changes_made += 1
                    print(f"last blank on row {i}!")
                elif self.row_counters[i]['X'] == self.row_hints[i]['X'] and (i in self.hints_used["row"]):
                    for j in range(self.size):
                        if self.final_puzzle[i][j] == '_':
                            self.final_puzzle[i][j] = 'O'
                            self.update_counter(i, j, 'O')
                    changes_made += 1
                    print(f"last blank on row {i}!")
            if self.col_counters[i]['_'] > 0:
                if self.col_counters[i]['O'] == self.col_hints[i]['O'] and (i in self.hints_used["col"]):
                    for j in range(self.size):
                        if self.final_puzzle[j][i] == '_':
                            self.final_puzzle[j][i] = 'X'
                            self.update_counter(j, i, 'X')
                    changes_made += 1
                    print(f"last blank on col {i}!")
                elif self.col_counters[i]['X'] == self.col_hints[i]['X'] and (i in self.hints_used["col"]):
                    for j in range(self.size):
                        if self.final_puzzle[j][i] == '_':
                            self.final_puzzle[j][i] = 'O'
                            self.update_counter(j, i, 'O')
                    changes_made += 1
                    print(f"last blank on col {i}!")
        return changes_made > 0

    def gather_statistics(self):
        """
        Gathers statistics for each empty cell, determining how many solutions assign 'O' or 'X'.
        """
        stats = {}

        def is_valid_partial(board):
            """
            Validates the board against the Binox rules. Returns True if valid.
            """
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j] != "_":
                        # Validate row
                        if j > 1 and board[i][j] == board[i][j - 1] == board[i][j - 2]:
                            return False
                        # Validate column
                        if i > 1 and board[i][j] == board[i - 1][j] == board[i - 2][j]:
                            return False
            return True

        def backtrack(row, col):
            """
            Backtracking function to fill the puzzle and gather statistics.
            """
            # If we reached the end of the board, count the current solution
            if row == self.size:
                return

            next_row, next_col = (row, col + 1) if col + 1 < self.size else (row + 1, 0)

            if self.puzzle[row][col] == "_":
                for mark in ("O", "X"):
                    self.puzzle[row][col] = mark
                    if is_valid_partial(self.puzzle):
                        if (row, col) not in stats:
                            stats[(row, col)] = {"O": 0, "X": 0}
                        stats[(row, col)][mark] += 1
                        backtrack(next_row, next_col)
                    self.puzzle[row][col] = "_"
            else:
                backtrack(next_row, next_col)

        backtrack(0, 0)
        return stats

    def modify_puzzle(self, stat):
        # self.print_puzz
        for cor, data in stat.items():
            if data["O"] - data["X"] == 0:
                self.final_puzzle[cor[0]][cor[1]] = self.board[cor[0]][cor[1]]
                self.update_counter(cor[0], cor[1], self.board[cor[0]][cor[1]])
                break
        self.puzzle = copy.deepcopy(self.final_puzzle)
        self.row_counters = [Counter() for _ in range(self.size)]
        self.col_counters = [Counter() for _ in range(self.size)]
        for i, row in enumerate(self.puzzle):
            for j, cell in enumerate(row):
                self.row_counters[i][cell] += 1
                self.col_counters[j][cell] += 1
        self.hints_used = {"row": set(), "col": set()}
    # # Function to generate row hints from the original board
    # def row_hints(self, num_hints=3):
    #     """
    #     Provide hints for a few rows, indicating the number of 'X' and 'O' in those rows.
    #     """
    #     size = len(self.board)
    #     chosen_rows = random.sample(range(size), num_hints)
    #     hints = {}
    #     for row in chosen_rows:
    #         x_count = self.board[row].count("X")
    #         o_count = self.board[row].count("O")
    #         hints[row] = (x_count, o_count)
        
    #     return hints


# # Function to check if the board has a unique solution based on hints
# # Function to check if the board has a unique solution based on hints
# # Function to check if the board has a unique solution based on hints
# def is_unique(board, size, hints):
#     #print("1")
#     """
#     Check if a valid and unique solution exists based on the hints and partially removed board.
#     This function tries to restore the board and checks if there's more than one valid solution.
#     """

#     # Helper function to check if the current board satisfies the row constraints
#     def satisfies_constraints(board):
#         for row in range(size):
#             x_count = board[row].count("X")
#             o_count = board[row].count("O")
#             # Check row hints
#             if row in hints and (x_count != hints[row][0] or o_count != hints[row][1]):
#                 return False
#         return True

#     # Backtracking to restore the board with the available hints
#     def backtrack(board, row, col):
#         # If we've reached the end of the board
#         if row == size:
#             print("\nFound a valid solution:")
#             for r in board:
#                 print(" ".join(r))  # Print the current valid solution
#             return [copy.deepcopy(board)]  # Found a valid solution

#         # Move to the next row if we're at the end of a column
#         if col == size:
#             return backtrack(board, row + 1, 0)

#         # Skip filled cells
#         if board[row][col] != "_":
#             return backtrack(board, row, col + 1)

#         solutions = []

#         # Try placing 'X' and 'O' at the current position
#         for symbol in ["X", "O"]:
#             board[row][col] = symbol
#             if satisfies_constraints(board):  # Check constraints after placing symbol
#                 solutions.extend(backtrack(board, row, col + 1))  # Explore next cells
#                 print(f"Solution found: {solutions}")
#             board[row][col] = "_"

#         return solutions

#     # Initialize board for backtracking
#     board_copy = copy.deepcopy(board)
#     solutions = backtrack(board_copy, 0, 0)
#     print(f"Solution found: {solutions}")

#     # If more than one solution is found, return False (i.e., multiple solutions found)
#     if len(solutions) > 1:
#         print("\nMultiple solutions found.")
#         return False  # Multiple solutions found
#     else:
#         print("\nUnique solution found.")
#         return True  # Only one solution found


# # Main Function to generate a board and verify its uniqueness
# def main():
#     # Generate a Binox board
#     original_board = binox_generator(size=6)
#     print("Original Board:")
#     for row in original_board:
#         print(" ".join(row))

#     # Remove pieces and display the new board
#     modified_board = remove_pieces(original_board, fraction=2 / 3)
#     print("\nBoard with Removed Pieces:")
#     for row in modified_board:
#         print(" ".join(row))

#     # Provide hints for a few rows from the original (correct) board
#     hints = row_hints(original_board, num_hints=3)
#     print("\nRow Hints (from the correct board):")
#     for row, (x_count, o_count) in hints.items():
#         print(f"Row {row + 1}: {x_count} X, {o_count} O")

#     # Check if the board with removed pieces and hints has a unique solution
#     valid = is_unique(modified_board, 6, hints)
#     if valid:
#         print("\nA unique solution exists!")
#     else:
#         print("\nMultiple or no solutions exist!")


if __name__ == "__main__":
    ins = BinoxVariationGenerator(6)
    # for i in range(1000):
    #     instance = BinoxVariationGenerator(12)
    #     for i in range(instance.size):
    #         if (abs(instance.row_hints[i][0] - instance.row_hints[i][1]) > 3) or (abs(instance.col_hints[i][0] - instance.col_hints[i][1]) > 3):
    #             for row in instance.board:
    #                 print(" ".join(row))
    #             print(instance.row_hints)
    #             print(instance.col_hints)
            


