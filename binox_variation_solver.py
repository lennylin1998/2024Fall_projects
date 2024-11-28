
class BinoxVariationSolver:
    def __init__(self, puzzle: dict) -> None:
        self.puzzle = puzzle
        self.size = len(puzzle['board'][0])
        self.curr_circle = {
            "row": [0] * self.size,
            "col": [0] * self.size,
        }
        self.curr_cross = {
            "row": [0] * self.size,
            "col": [0] * self.size,
        }
    def print_board(self) -> None:
        # Separate the cues and board
        board = self.puzzle['board']
        col_cues = self.puzzle['col_cues']
        row_cues = self.puzzle['row_cues']
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 1:
                    self.curr_circle["row"][row] += 1
                    self.curr_circle["col"][col] += 1
                elif board[row][col] == -1:
                    self.curr_cross["row"][row] += 1
                    self.curr_cross["col"][col] += 1

        # Calculate spacing for alignment
        cell_width = 3
        col_cue_str = "O/X " + " ".join(f"{x}/{self.size - x}" for x in col_cues)
        horizontal_separator = "    +" + "+".join(["-" * cell_width] * (self.size)) + "+"

        print("circle:", self.curr_circle)
        print("cross:", self.curr_cross)
        # Print the board with column and row cues
        print("     " + " ".join([ f"{i:^{cell_width}}" for i in range(1, self.size + 1)]) + "  O/X")
        print(horizontal_separator)  # Separator after cues
        for i, row in enumerate(board):
            formatted_row = f"  {i + 1} |" + "|".join(
                f"{'O' if x == 1 else 'X' if x == -1 else '.':^{cell_width}}" for x in row
            ) + "|" + f" {row_cues[i]}/{self.size - row_cues[i]}"
            print(formatted_row)
            print(horizontal_separator)  # Separator after each row
            # print(f"{'':>{len(horizontal_separator)-4}} {}")  # Row cue aligned
        print(f" {col_cue_str}")  # Top row for column cues



if __name__ == "__main__":
    from easy import puzzle_1
    solver = BinoxVariationSolver(puzzle_1)
    solver.print_board()