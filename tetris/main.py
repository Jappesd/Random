# game loop and initialization
import pygame
from piece import Piece
from random import choice
from pieces import TETROMINOES as tetros
from scorepop import ScorePop

# constants
screen_width = 390
screen_height = 750
block_size = 30
# playing field
grid_width = screen_width // block_size
grid_height = screen_height // block_size
# sidebar margin
sidebar_width = 150
playfield_x = sidebar_width  # leave space on the left
playfield_y = 0  # top margin

left_sidebar_x = 30  # padding inside left margin
right_sidebar_x = playfield_x + screen_width + 20  # starts after playfield
# total window
window_width = screen_width + sidebar_width * 2
next_box_x = right_sidebar_x
next_box_y = 150
box_width = 4 * block_size  # Tetris pieces are at most 4 blocks wide
box_height = 4 * block_size  # 4 blocks tall
score_pops = []
locked_positions = {}
# colors for the blocks
colors = {
    "I": (0, 255, 255),
    "O": (255, 255, 0),
    "T": (128, 0, 128),
    "S": (0, 255, 0),
    "Z": (255, 0, 0),
    "J": (0, 0, 255),
    "L": (255, 165, 0),
}


# helper functions
def draw_sidebar(surface, score, level):
    font = pygame.font.SysFont("comicsans", 24)

    # level (left sidebar)
    level_label = font.render(f"Level: {level}", True, (255, 255, 255))
    surface.blit(level_label, (left_sidebar_x, 50))

    # score (right sidebar)
    score_label = font.render(f"Score: {score}", True, (255, 255, 255))
    surface.blit(score_label, (right_sidebar_x, 50))


def get_piece_bounding_box(piece):
    """
    Returns (min_x, max_x, min_y, max_y) of occupied cells in the current rotation.
    """
    shape_format = piece.shape[piece.rotation % len(piece.shape)]
    min_x = min_y = 4
    max_x = max_y = -1

    for y, row in enumerate(shape_format):
        for x, cell in enumerate(row):
            if cell:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

    return min_x, max_x, min_y, max_y


def draw_next_piece(surface, next_piece):
    box_size = 4  # 4x4 preview box
    box_pixel = box_size * block_size
    # Draw preview box outline
    pygame.draw.rect(
        surface,
        (255, 255, 255),  # white outline
        (next_box_x, next_box_y, box_pixel, box_pixel),
        2,  # thickness of the border
    )
    # piece dimensions
    min_x, max_x, min_y, max_y = get_piece_bounding_box(next_piece)
    piece_width = max_x - min_x + 1
    piece_height = max_y - min_y + 1

    # compute offsets to center the piece
    x_offset = (box_size - piece_width) // 2 - min_x
    y_offset = (box_size - piece_height) // 2 - min_y

    # Draw each block of the piece
    shape_format = next_piece.shape[next_piece.rotation % len(next_piece.shape)]
    for i, row in enumerate(shape_format):
        for j, cell in enumerate(row):
            if cell:
                color = colors[next_piece.shape_key]
                pygame.draw.rect(
                    surface,
                    color,
                    (
                        next_box_x + (j + x_offset) * block_size,
                        next_box_y + (i + y_offset) * block_size,
                        block_size,
                        block_size,
                    ),
                )
                pygame.draw.rect(
                    surface,
                    (128, 128, 128),
                    (
                        next_box_x + (j + x_offset) * block_size,
                        next_box_y + (i + y_offset) * block_size,
                        block_size,
                        block_size,
                    ),
                    1,
                )


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(grid_width)] for _ in range(grid_height)]
    for (x, y), color in locked_positions.items():
        if y >= 0:
            grid[y][x] = color
    return grid


def draw_grid(surface, grid):
    for y in range(grid_height):
        for x in range(grid_width):
            color = grid[y][x]
            pygame.draw.rect(
                surface,
                color,
                (
                    playfield_x + x * block_size,
                    playfield_y + y * block_size,
                    block_size,
                    block_size,
                ),
            )
            pygame.draw.rect(
                surface,
                (128, 128, 128),
                (
                    playfield_x + x * block_size,
                    playfield_y + y * block_size,
                    block_size,
                    block_size,
                ),
                1,
            )


def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, row in enumerate(format):
        for j, cell in enumerate(row):
            if cell:
                positions.append((piece.x + j, piece.y + i))
    return positions


def valid_space(piece, grid):
    for x, y in convert_shape_format(piece):
        if x < 0 or x >= grid_width or y >= grid_height:
            return False
        if y >= 0 and grid[y][x] != (0, 0, 0):
            return False
    return True


# row clearerer
def clear_rows(grid, locked):
    """
    Clears all full rows in the grid and moves above blocks down.
    Returns the number of rows cleared.
    """
    rows_to_clear = []

    for y in range(len(grid)):
        if all(grid[y][x] != (0, 0, 0) for x in range(len(grid[0]))):
            rows_to_clear.append(y)
    num_cleared = len(rows_to_clear)
    if num_cleared > 0:
        # Remove blocks from locked positions in cleared rows
        for y in rows_to_clear:
            for x in range(len(grid[0])):
                if (x, y) in locked:
                    del locked[(x, y)]

        # Shift all rows above down by the number of cleared rows below
        # Process rows from bottom to top
        rows_to_clear.sort()
        for y in reversed(range(len(grid))):
            shift = 0
            for cleared_y in rows_to_clear:
                if y < cleared_y:
                    shift += 1
            if shift > 0:
                for x in range(len(grid[0])):
                    if (x, y) in locked:
                        locked[(x, y + shift)] = locked.pop((x, y))

    return num_cleared


def get_ghost_piece(piece, grid):
    """
    Returns the coordinates where the piece would land if hard dropped.
    """
    ghost = Piece(piece.x, piece.y, piece.shape, piece.shape_key)
    ghost.rotation = piece.rotation

    while valid_space(ghost, grid):
        ghost.y += 1
    ghost.y -= 1  # last valid position

    return ghost


def calculate_score(rows_cleared):
    # returns points based on number of rows cleared
    if rows_cleared == 1:
        return 100
    elif rows_cleared == 2:
        return 300
    elif rows_cleared == 3:
        return 500
    elif rows_cleared >= 4:
        return 800
    else:
        return 0


def draw_game(screen, grid, current_piece, next_piece, score, level):
    """
    Draws the entire game state: Grid, ghostpiece, current piece, sidebar, next piece
    """
    global score_pops
    screen.fill((0, 0, 0))  # clears screen

    # --- Draw ghost piece ---
    ghost_piece = get_ghost_piece(current_piece, grid)
    for x, y in convert_shape_format(ghost_piece):
        if y >= 0:
            r, g, b = colors[ghost_piece.shape_key]
            ghost_color = (r // 2, g // 2, b // 2)
            grid[y][x] = ghost_color

    # --- Draw current piece ---
    for x, y in convert_shape_format(current_piece):
        if y >= 0:
            grid[y][x] = colors[current_piece.shape_key]

    # --- Draw grid ---
    draw_grid(screen, grid)

    # --- Draw next piece  and sidebars---
    draw_sidebar(screen, score, level)
    draw_next_piece(screen, next_piece)

    # --- Reset current piece color in grid ---
    for x, y in convert_shape_format(current_piece):
        if y >= 0:
            grid[y][x] = colors[current_piece.shape_key]

    for pop in score_pops[:]:
        pop.update()
        pop.draw(screen)
        if pop.is_ded():
            score_pops.remove(pop)

    pygame.display.update()


def flasher(screen, grid, locked, rows_to_flash, flash_times=3, flash_speed=100):
    """
    Temporarily flash the rows that are to be cleared.
    - rows_to_flash: list of row indices (indexes)
    - flash_times: how many on/off flashes
    - flash_speed: time per flash in milliseconds
    """
    clock = pygame.time.Clock()
    for _ in range(flash_times):
        # flash on
        for y in rows_to_flash:
            for x in range(len(grid[0])):
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),  # flash color
                    (
                        playfield_x + x * block_size,
                        playfield_y + y * block_size,
                        block_size,
                        block_size,
                    ),
                )
        pygame.display.update()
        pygame.time.delay(flash_speed)
        # flash off (draw normal grid)
        draw_grid(screen, grid)
        pygame.display.update()
        pygame.time.delay(flash_speed)


def lock_piece(
    current_piece,
    next_piece,
    locked_positions,
    grid,
    score,
    lines_cleared,
    level,
    fall_speed,
    screen=None,
):
    """
    Locks the current piece into the grid,clears rows,updates score/level,
    generates next piece, and rebuilds the grid.
    returns updated (current_piece,next_piece,grid,score,lines_cleared, level,fall_speed)
    """
    global score_pops
    # lock the current piece into locked_positions
    for x, y in convert_shape_format(current_piece):
        if y >= 0:
            locked_positions[(x, y)] = colors[current_piece.shape_key]
    grid = create_grid(locked_positions)
    rows_to_clear = []
    for y in range(len(grid)):
        if all(grid[y][x] != (0, 0, 0) for x in range(len(grid[0]))):
            rows_to_clear.append(y)
    if rows_to_clear:
        flasher(screen, grid, locked_positions, rows_to_clear)
    # Clear rows and update score/level
    rows = clear_rows(grid, locked_positions)
    if rows > 0:
        points = calculate_score(rows)
        score += points
        lines_cleared += rows
        # spawn pop at the bottom of the screen
        score_pops.append(ScorePop(f"+{points}", window_width // 2, screen_height - 50))
        # levels up every 2 lines
        new_level = (lines_cleared // 2) + 1
        if new_level != level:
            level = new_level
            fall_speed = max(0.1, 0.5 - (level - 1) * 0.05)
            print(f"Level Up! Level: {level}, new falls speed: {fall_speed:.2f}s")
        print(f"Cleared {rows} row(s)! Current score: {score}")

    # shift next_piece to current piece
    current_piece = Piece(3, 0, next_piece.shape, next_piece.shape_key)

    # generate next_piece
    key, shape = choice(list(tetros.items()))
    next_piece = Piece(3, 0, shape, key)
    # rebuild grid for drawing
    grid = create_grid(locked_positions)

    # return all updated values
    return current_piece, next_piece, grid, score, lines_cleared, level, fall_speed


# main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((window_width, screen_height))
    pygame.display.set_caption("Tetromina")
    clock = pygame.time.Clock()

    score = 0
    grid = create_grid(locked_positions)

    # initial pieces
    key, shape = choice(list(tetros.items()))
    current_piece = Piece(3, 0, shape, key)
    next_key, next_shape = choice(list(tetros.items()))
    next_piece = Piece(0, 0, next_shape, next_key)
    # variables
    level = 1
    lines_cleared = 0
    fall_time = 0
    fall_speed = 0.5  # seconds
    soft_drop_speed = 0.05
    running = True
    while running:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # soft drop
        keys = pygame.key.get_pressed()
        current_speed = soft_drop_speed if keys[pygame.K_DOWN] else fall_speed

        # piece falls automagically
        if fall_time / 1000 > current_speed:
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                # lock the piece using helper
                (
                    current_piece,
                    next_piece,
                    grid,
                    score,
                    lines_cleared,
                    level,
                    fall_speed,
                ) = lock_piece(
                    current_piece,
                    next_piece,
                    locked_positions,
                    grid,
                    score,
                    lines_cleared,
                    level,
                    fall_speed,
                    screen,
                )
                # gameover check
                if not valid_space(current_piece, grid):
                    print("Game Over!")
                    running = False

            fall_time = 0

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1
                elif event.key == pygame.K_SPACE:
                    # hard drop
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1  # step back to valid position
                    # lock the piece using helper
                    (
                        current_piece,
                        next_piece,
                        grid,
                        score,
                        lines_cleared,
                        level,
                        fall_speed,
                    ) = lock_piece(
                        current_piece,
                        next_piece,
                        locked_positions,
                        grid,
                        score,
                        lines_cleared,
                        level,
                        fall_speed,
                        screen,
                    )

                    # Check game over
                    if not valid_space(current_piece, grid):
                        print("Game Over!")
                        running = False

        # --- Draw everything ---
        draw_game(screen, grid, current_piece, next_piece, score, level)
    pygame.quit()


if __name__ == "__main__":
    main()
