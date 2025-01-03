import sys
from binox_variation_board import BinoxVariationBoard
from binox_variation_generator import BinoxVariationGenerator

class BinoxVariationGame:
    def __init__(self):
        self.quit = False
        # Map input to corresponding methods
        self.actions = {
            'A': self.fill_cell,
            'S': self.check_answer,
            'D': self.return_to_last_step,
            'F': self.new_game,
            'Q': self.quit_game
        }
        self.solver = None

    def run_game(self) -> None:
        while not self.quit:
            print("* Action Menu")
            print("-------------------------------")
            for option, action in self.actions.items():
                print(option + ". " + " ".join(action.__name__.split('_')).capitalize())
            self.action_handle(input("Please select an action: "))
            print("-------------------------------")
    def fill_cell(self) -> None:
        if not self.solver:
            print("#################################")
            print("Please start a new game first!")
            print("#################################")
            return
        print("Filling a cell...")
        row = self.get_valid_input_coordinates("row ")
        print("  row ", row, " chosen")
        col = self.get_valid_input_coordinates("col ")
        print("  col ", col, " chosen")
        mark = self.get_valid_input_mark()
        self.solver.update_cell(row - 1, col - 1, mark)

        self.solver.print_board()
        if self.solver.check_solved():
            print("Congradulations! Puzzle solved!")
            print()
            self.solver = None

    def check_answer(self) -> None:
        print("Checking the answer...")
        if not self.solver:
            print("#################################")
            print("Please start a new game first!")
            print("#################################")
            return
        print()
        for row in self.solver.answer:
            print(" ".join(row))
        print()

    def return_to_last_step(self) -> None:
        print("Return to last step...")
        if not self.solver:
            print("#################################")
            print("Please start a new game first!")
            print("#################################")
            return
        self.solver.last_step()

    def new_game(self) -> None:
        print("Starting a new game...")
        size = 6
        while True:
            # Get input and remove leading/trailing whitespace
            user_input = input("Select a size from 6 to 12: ").strip()
            try:
                # Convert input to integer
                size = int(user_input)
                # Check if number is between 1 and 6 (inclusive)
                if 6 <= size <= 12:
                    break
                raise ValueError
            except ValueError:
                print(f"Invalid input! Should be number betwee 6 and 12")
        self.solver = BinoxVariationBoard(BinoxVariationGenerator(size))
        print()
        for row in self.solver.answer:
            print(" ".join(row))
        print()
    def quit_game(self) -> None:
        print("#################################")
        print("Quitting the game...")
        print("#################################")
        sys.exit()

    def action_handle(self, option: str) -> None:
        # Execute the corresponding method if valid input, otherwise show an error
        action = self.actions.get(option.upper())
        if action:
            action()
        else:
            print(f"Invalid option '{option}'. Please select from A, S, D, F, G.")

    def get_valid_input_coordinates(self, prompt: str) -> int:
        while True:
            # Get input and remove leading/trailing whitespace
            user_input = input(f"Please choose {prompt}: ").strip()
            try:
                # Convert input to integer
                number = int(user_input)
                # Check if number is between 1 and 6 (inclusive)
                if 1 <= number <= self.solver.size:
                    return number
                raise ValueError
            except ValueError:
                print(f"Invalid input! Should be number betwee 1 and {self.solver.size}")

    def get_valid_input_mark(self) -> int:
        while True:
            # Get input and remove leading/trailing whitespace
            user_input = input(f"Please choose 'O' or 'X': ").strip().upper()
            try:
                # Convert input to integer
                # Check if number is between 1 and 6 (inclusive)
                if user_input == 'O' or user_input == 'X':
                    return user_input
                raise ValueError
            except ValueError:
                print(f"Invalid input! Should be either 'O' or 'X'!")

if __name__ == "__main__":
    game = BinoxVariationGame()
    game.run_game()