from easy import puzzle_1
from colorama import Fore, Style

class BinoxVariationSolver:
    def __init__(self, puzzle: dict) -> None:
        self.board = puzzle['board']
        self.col_cues = puzzle['col_cues']
        self.row_cues = puzzle['row_cues']
        self.size = len(puzzle['board'][0])
        self.curr_circle = {
            "row": [0] * self.size,
            "col": [0] * self.size,
        }
        self.curr_cross = {
            "row": [0] * self.size,
            "col": [0] * self.size,
        }
        self.preset_cells = set()
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] != 0:
                    self.preset_cells.add((i, j))
        self.moves = []
        self.print_board()

    def check_solved(self) -> bool:
        for i in range(self.size):
            if self.curr_circle['row'][i] != self.row_cues[i]:
                return False
            if self.curr_circle['col'][i] != self.col_cues[i]:
                return False
            if self.curr_cross['row'][i] != self.size - self.row_cues[i]:
                return False
            if self.curr_cross['col'][i] != self.size - self.col_cues[i]:
                return False
        return True
    def update_cell(self, row: int, col: int, mark: str) -> None:
        if (row, col) in self.preset_cells:
            print("This cell is given and can not be changed!")
            return
        print("updated cell!!")
        val = 1 if mark == 'O' else -1 if mark == 'X' else 0
        self.moves.append(tuple([row, col, self.board[row][col]]))
        self.board[row][col] = val
        print(self.moves)

    def last_step(self) -> None:
        if len(self.moves) == 0:
            return
        last_row, last_col, last_mark = self.moves[-1]
        self.board[last_row][last_col] = last_mark
        self.moves.pop()
        self.print_board()

    def print_board(self) -> None:
        # Separate the cues and board
        board = self.board
        col_cues = self.col_cues
        row_cues = self.row_cues
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
        col_cue_str = "    " + " ".join(f"{x}/{self.size - x}" for x in col_cues) + "  O/X"
        horizontal_separator = "    +" + "+".join(["-" * cell_width] * (self.size)) + "+"

        print("=" * (cell_width + 1) * (self.size + 3))
        print("circle:", self.curr_circle)
        print("cross:", self.curr_cross)
        # Print the board with column and row cues
        print("     " + " ".join([ f"{i:^{cell_width}}" for i in range(1, self.size + 1)]))
        print(horizontal_separator)  # Separator after cues
        for i, row in enumerate(board):
            print(f"  {i + 1} |", end="")
            for j in range(len(row)):
                if (i, j) in self.preset_cells:
                    print(f"{Fore.BLUE}{'O' if board[i][j] == 1 else 'X' if board[i][j] == -1 else '.':^{cell_width}}{Style.RESET_ALL}", end = '|')
                else:
                    print(f"{'O' if board[i][j] == 1 else 'X' if board[i][j] == -1 else '.':^{cell_width}}", end = '|')

            print(f" {row_cues[i]}/{self.size - row_cues[i]}")
            print(horizontal_separator)  # Separator after each row
            # print(f"{'':>{len(horizontal_separator)-4}} {}")  # Row cue aligned
        print(f" {col_cue_str}")  # Top row for column cues
        print("=" * (cell_width + 1) * (self.size + 3))


if __name__ == "__main__":
    solver = BinoxVariationSolver(puzzle_1)
    # solver.print_board()
