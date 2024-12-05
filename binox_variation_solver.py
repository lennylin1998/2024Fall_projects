from easy import puzzle_1
from colorama import Fore, Style


class BinoxVariationSolver:
    def __init__(self, generator) -> None:
        self.board = generator.final_puzzle
        self.size = generator.size
        self.col_hints = [generator.row_hints[i]["O"] if i in generator.hints_used["col"] else 0 for i in range(self.size)]
        self.row_hints = [generator.row_hints[i]["O"] if i in generator.hints_used["row"] else 0 for i in range(self.size)]
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
                if self.board[i][j] != "_":
                    self.preset_cells.add((i, j))
        self.moves = []
        self.print_board()

    def get_clues(self) -> None:
        return

    def check_solved(self) -> bool:
        for i in range(self.size):
            if self.row_hints[i] > 0 and self.curr_circle['row'][i] != self.row_hints[i]:
                return False
            if self.col_hints[i] > 0 and self.curr_circle['col'][i] != self.col_hints[i]:
                return False
            if self.row_hints[i] > 0 and self.curr_cross['row'][i] != self.size - self.row_hints[i]:
                return False
            if self.col_hints[i] > 0 and self.curr_cross['col'][i] != self.size - self.col_hints[i]:
                return False
        return True
    def update_cell(self, row: int, col: int, mark: str) -> None:
        if (row, col) in self.preset_cells:
            print("This cell is given and can not be changed!")
            return
        print("updated cell!!")
        self.moves.append(tuple([row, col, self.board[row][col]]))
        self.board[row][col] = mark
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
        col_hints = self.col_hints
        row_hints = self.row_hints
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == "O":
                    self.curr_circle["row"][row] += 1
                    self.curr_circle["col"][col] += 1
                elif board[row][col] == "X":
                    self.curr_cross["row"][row] += 1
                    self.curr_cross["col"][col] += 1

        # Calculate spacing for alignment
        cell_width = 3
        col_cue_str = "    " + " ".join(f"{x}/{self.size - x}" if x > 0 else "   " for x in col_hints) + "  O/X"
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
                    print(f"{Fore.BLUE}{'.' if board[i][j] == "_" else board[i][j]:^{cell_width}}{Style.RESET_ALL}", end = '|')
                else:
                    print(f"{'.' if board[i][j] == "_" else board[i][j]:^{cell_width}}", end = '|')
            if row_hints[i] > 0:
                print(f" {row_hints[i]}/{self.size - row_hints[i]}")
            else:
                print("   ")
            print(horizontal_separator)  # Separator after each row
            # print(f"{'':>{len(horizontal_separator)-4}} {}")  # Row cue aligned
        print(f" {col_cue_str}")  # Top row for column cues
        print("=" * (cell_width + 1) * (self.size + 3))


if __name__ == "__main__":
    solver = BinoxVariationSolver(puzzle_1)
    # solver.print_board()
