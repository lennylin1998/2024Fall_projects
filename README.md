# Binox Original Game Rule Introduction
An online interactive version can be found on [KrazyDad's Website](https://krazydad.com/binox/)
1. The puzzle is filled with Xs and Os.
2. Horizontally and vertically, there can be no more than 2 of the same symbol touching.
3. There are an equal number of Xs and Os in each row and column.
4. Each row must be unique. Each column must be unique

We suggest those who hear Binox for the first time try to play some original games!

# Modification of This Version
We remove rules #3 and #4. 

Basically, it means the number of cross and circle are not necessary the same for each row and each column.

Plus, the puzzle will hide some of the row/ column hints.

Other rules stay the same.

# How to Play a Game
Please ensure python3 version 3.12 and package colorama is installed first and run:

`python3 binox_variation_game.py`

Then follow the instructions in the game menu to play a game. Have fun!

# Design of Generator
First, we generate a random "completed" puzzle based on the first and second rules.

Second, we randomly remove some portion of the cells to create the first version of our playable puzzle.

Then, we try to solve it using 3 basic strategies a human would use to solve a Binox game. 

1. Place an opposite mark whenever the program detects adjacent cells of the same marks.
2. Place an opposite mark whenever the program detects the left(up) cells and right(down) cells of the same marks.
3. Fill the cell according to row/ column hints when the above strategies are exhausted, and one of the marks is completed for that row/ column.

After reaching this step, we will have a partially solved puzzle. This puzzle is guaranteed to have multiple solutions. So now we try to use backtrack to find all possible solutions.

When doing backtracking, we collect data on each cell. Our goal is to find the cell that can cause multiple solutions. An intuitive way is to find the cells where "O" and "X" are equally likely to be in the solution space.

After gathering statistics, we fill the "equally likely" empty cell one at a time(as given hints at the very beginning), and try to use the human strategies to solve the puzzle again.

We repeat this process until the solution is left to only one.

# Challenges
The inner function `is_valid_partial` in `BinoxVariationGenerator.backtrack` used to take a long time to run since we try to verify the whole board every time we fill a cell.

We try to improve the time complexity by checking the neighboring cells only. The complexity is reduced from O(n) (where n is the total number of cells) to O(1).

# Runtime Complexity Analysis
The n here denotes the number of cells in a puzzle.
## Generate random completed puzzle
This step is hard to find a boundary, since we randomly choose "O" or "X" at each cell, and try the other one when the chosen one violate the rule.

But we can be certain that the lowest boundary would be Ω(n), and the upper bound would never exceed O(2^n) (This case actually will never happen).
## Partial solver
This is again hard to estimate, since this function ends only when human strategies are exhausted. The number of iterations would depend on the size of the board, the number of cells removed, and even the "positions" where those cells are removed. Let's say if we remove 2/3 of the cells, then the runtime will be O(2/3 * n) or O(n) in the worst case.

(The time complexity depends solely on the number of iterations because we use a dictionary to store counts of currently filled marks, and this makes `hint_fill` O(1))
## Backtrack
This step is similar to generating a random completed puzzle, but differs in that in this step we will try to fill every possible mark instead of randomly choosing.
The estimated runtime would be O(2^(2/3 * n)) in worst case. Since the number of empty cell depends on the previous partial solver, theoretically the worst case would be none of the empty cells are filled during the previous step.

## Overall
Since we don't call any of the functions in one another above, the runtime would be the worst of them.

In this case it would be backtrack

# Contributor
This is an IS 597 DS&A Fall 2024 final project completed by Zhiyuan And Yu-Liang.

Yu-Liang did the game interface part and Zhiyuan did the generator part.

# Further Resources
- Demonstration Slides: https://docs.google.com/presentation/d/1CLr-WksrBFl-GMQIUY9IzFVhMINUpelq/edit?usp=sharing&ouid=104473100857823900915&rtpof=true&sd=true
