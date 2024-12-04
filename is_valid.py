def apply_constraints(grid, row_hints):
    """
    根据已有的约束条件处理网格，尽量填充棋子。
    """
    n = len(grid)

    # 处理每一行的约束
    for row in range(n):
        if row in row_hints:  # 如果这一行有约束
            x_count = sum(1 for cell in grid[row] if cell == 1)  # 计算该行X的数量
            o_count = sum(1 for cell in grid[row] if cell == -1)  # 计算该行O的数量
            max_x, max_o = row_hints[row]

            # 如果已经达到提示数量，跳过
            if x_count == max_x and o_count == max_o:
                continue

            # 1. 处理两个同色棋子相邻的情况
            for col in range(1, n):
                if grid[row][col] == grid[row][col - 1] and grid[row][col] != 0:
                    if grid[row][col] == 1:  # 如果是两个X
                        if col - 2 >= 0 and grid[row][col - 2] == 0:
                            grid[row][col - 2] = -1  # 填入O
                    elif grid[row][col] == -1:  # 如果是两个O
                        if col - 2 >= 0 and grid[row][col - 2] == 0:
                            grid[row][col - 2] = 1  # 填入X

            # 2. 处理两个同色棋子之间隔着一个空格的情况
            for col in range(2, n):
                if grid[row][col] == grid[row][col - 2] and grid[row][col] != 0:
                    if grid[row][col] == 1:  # 如果是X
                        if grid[row][col - 1] == 0:
                            grid[row][col - 1] = -1  # 填入O
                    elif grid[row][col] == -1:  # 如果是O
                        if grid[row][col - 1] == 0:
                            grid[row][col - 1] = 1  # 填入X

            # 3. 根据每行的约束条件去增加子
            x_needed = max_x - x_count
            o_needed = max_o - o_count

            for col in range(n):
                if grid[row][col] == 0:  # 如果当前位置为空
                    if x_needed > 0:
                        grid[row][col] = 1  # 填入X
                        x_needed -= 1
                    elif o_needed > 0:
                        grid[row][col] = -1  # 填入O
                        o_needed -= 1

    return grid


def is_valid_move(grid, row, col, num):
    """
    检查在grid的(row, col)位置填入数字num（1为X，-1为O）是否有效
    包括检查同行、同列是否有重复的数字。
    """
    n = len(grid)

    # 检查同行是否有相同的数字
    for i in range(n):
        if grid[row][i] == num:
            return False

    # 检查同列是否有相同的数字
    for i in range(n):
        if grid[i][col] == num:
            return False

    return True


def solve_binox(grid, row_hints):
    """
    根据上述逻辑解决Binox游戏，先应用约束，填充棋盘。
    """
    n = len(grid)

    # 首先尝试通过约束填充棋盘
    grid = apply_constraints(grid, row_hints)

    # 检查是否还有未填充的空位
    for row in range(n):
        for col in range(n):
            if grid[row][col] == 0:
                return False  # 还有空位，未解决

    return True  # 所有空位都已填充，解已找到


def print_grid(grid):
    """
    打印出解决后的网格
    """
    for row in grid:
        print(' '.join(['X' if x == 1 else 'O' if x == -1 else '_' for x in row]))


# 示例用法
grid = [
    [0, 0, -1, 0, 0, 1],  # _ _ O _ _ X
    [-1, 0, 0, 0, 0, 0],  # O _ _ _ _ _
    [1, -1, 0, -1, -1, 0],  # X O _ O O _
    [0, 0, 0, 0, 0, 0],  # _ _ _ _ _ _
    [-1, 0, 0, 0, 0, 0],  # O _ _ _ _ _
    [0, -1, 0, -1, -1, 0],  # _ O _ O O _
]

# 给定的行提示（Row Hints）
row_hints = {
    0: (3, 3),  # Row 1: 3 X, 3 O
    1: (3, 3),  # Row 2: 3 X, 3 O
    2: (3, 3),  # Row 3: 3 X, 3 O
    3: (3, 3),  # Row 4: 3 X, 3 O
    4: (3, 3),  # Row 5: 3 X, 3 O
    5: (3, 3),  # Row 6: 3 X, 3 O
}

if solve_binox(grid, row_hints):
    print("Solved:")
    print_grid(grid)
else:
    print("No solution exists.")
