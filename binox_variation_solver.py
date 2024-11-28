

class BinoxVariationSolver:
    def __init__(self, puzzle: dict) -> None:
        self.puzzle = puzzle
        self.size = len(puzzle['board'][0])
    def print_board(self) -> None:
        # Separate the cues and board
        board = self.puzzle['board']
        col_cues = self.puzzle['col_cues']
        row_cues = self.puzzle['row_cues']

        # Calculate spacing for alignment
        cell_width = 3
        col_cue_str = " " + " ".join(f"{x:^{cell_width}}" for x in col_cues)
        horizontal_separator = "+" + "+".join(["-" * cell_width] * 6) + "+"

        # Print the board with column and row cues
        print(f"{col_cue_str}")  # Top row for column cues
        print(horizontal_separator)  # Separator after cues
        for i, row in enumerate(board):
            formatted_row = "|" + "|".join(
                f"{'O' if x == 1 else 'X' if x == -1 else '.':^{cell_width}}" for x in row
            ) + "|" + f" {row_cues[i]}"
            print(formatted_row)
            print(horizontal_separator)  # Separator after each row
            # print(f"{'':>{len(horizontal_separator)-4}} {}")  # Row cue aligned


if __name__ == "__main__":
    from easy import puzzle_1
    solver = BinoxVariationSolver(puzzle_1)
    solver.print_board()