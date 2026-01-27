# helper prints the board nicely for debugging
def print_board(grid):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")

            value = grid[i][j]
            print(value if value != 0 else ".", end=" ")

        print()


def find_empty(grid):
    # find the next empty cell in the grid.
    # returns (row,col) or None if the grid is full
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return None


def is_valid(grid, number, position):
    # check whether placing "number" at "position" is valid

    # position = (row,col)
    row, col = position

    # check row
    for c in range(9):
        if grid[row][c] == number and c != col:
            return False
    # check column
    for r in range(9):
        if grid[r][col] == number and r != row:
            return False
    # check 3x3 box
    box_x = col // 3
    box_y = row // 3

    for r in range(box_y * 3, box_y * 3 + 3):
        for c in range(box_x * 3, box_x * 3 + 3):
            if grid[r][c] == number and (r, c) != position:
                return False
    return True


# solver
def solve_sudoku(grid):
    """
    solve the sudoku using backtracking.
    modifies the grid in-place.
    returns true if solved, False otherwise
    """
    find = find_empty(grid)

    # no empty cells equals solved
    if not find:
        return True

    row, col = find

    # try numbers 1 to 9
    for number in range(1, 10):
        if is_valid(grid, number, (row, col)):
            grid[row][col] = number

            # recursively attempt to solve
            if solve_sudoku(grid):
                return True

            # backtrack
            grid[row][col] = 0
    return False


if __name__ == "__main__":
    # 0 means empty
    grid2 = [
        [2, 9, 0, 0, 0, 5, 0, 0, 0],
        [5, 0, 0, 7, 0, 3, 4, 0, 9],
        [0, 0, 0, 9, 0, 8, 5, 6, 1],
        [0, 0, 0, 0, 4, 0, 6, 1, 0],
        [9, 0, 0, 8, 0, 0, 0, 0, 7],
        [0, 0, 3, 6, 7, 2, 0, 8, 0],
        [6, 4, 0, 0, 5, 0, 8, 0, 0],
        [8, 2, 0, 3, 0, 6, 0, 4, 5],
        [3, 0, 5, 2, 0, 0, 1, 0, 0],
    ]
    grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    original_grid = [
        [6, 0, 3, 0, 0, 4, 0, 0, 1],
        [4, 2, 0, 9, 1, 3, 0, 6, 5],
        [0, 1, 0, 0, 0, 7, 0, 0, 0],
        [0, 3, 0, 0, 7, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 8, 0, 0, 2],
        [0, 0, 8, 1, 6, 0, 0, 0, 7],
        [8, 7, 0, 3, 0, 5, 0, 2, 9],
        [3, 4, 9, 7, 0, 0, 1, 0, 0],
        [2, 0, 6, 8, 0, 0, 3, 0, 4],
    ]
    print("OG board:")
    print_board(original_grid)

    if solve_sudoku(original_grid):
        print("\nSolved Board:")
        print_board(original_grid)
    else:
        print("how about no!")
    solved_grid = [
        [6, 8, 3, 2, 5, 4, 7, 9, 1],
        [4, 2, 7, 9, 1, 3, 8, 6, 5],
        [9, 1, 5, 6, 8, 7, 2, 4, 3],
        [1, 3, 2, 4, 7, 9, 5, 8, 6],
        [7, 6, 4, 5, 3, 8, 9, 1, 2],
        [5, 9, 8, 1, 6, 2, 4, 3, 7],
        [8, 7, 1, 3, 4, 5, 6, 2, 9],
        [3, 4, 9, 7, 2, 6, 1, 5, 8],
        [2, 5, 6, 8, 9, 1, 3, 7, 4],
    ]
