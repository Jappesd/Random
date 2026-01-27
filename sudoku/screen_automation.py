# This stage WILL:
# Locate the Sudoku board on screen
# Calculate cell positions
# Click cells
# Type numbers
import pyautogui
import time

pyautogui.FAILSAFE = True  # move mouse to top-left to abort
pyautogui.PAUSE = 0.05  # delay between actions


def get_mouse_position(prompt):
    print(prompt)
    time.sleep(3)
    return pyautogui.position()


def compute_cell_centers(top_left, bottom_right):
    x1, y1 = top_left
    x2, y2 = bottom_right

    board_width = x2 - x1
    board_height = y2 - y1

    cell_width = board_width / 9
    cell_height = board_height / 9
    cells = []

    for row in range(9):
        row_cells = []
        for col in range(9):
            center_x = int(x1 + col * cell_width + cell_width / 2)
            center_y = int(y1 + row * cell_height + cell_height / 2)
            row_cells.append((center_x, center_y))
        cells.append(row_cells)
    return cells


def fill_cell(x, y, number):
    pyautogui.click(x, y)
    pyautogui.press(str(number))


def fill_sudoku(cells, original_grid, solved_grid):
    for row in range(9):
        for col in range(9):
            if original_grid[row][col] == 0:
                x, y = cells[row][col]
                number = solved_grid[row][col]

                pyautogui.click(x, y)
                pyautogui.press(str(number))
                time.sleep(0.001)


if __name__ == "__main__":
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
    top_left = get_mouse_position("in 3 seconds top right")
    bottom_right = get_mouse_position("in 3 secs bottom right")
    cells = compute_cell_centers(top_left, bottom_right)
    fill_sudoku(cells, original_grid, solved_grid)
