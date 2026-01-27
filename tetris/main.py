# game loop and initialization
import pygame
from piece import Piece
from random import choice
from pieces import TETROMINOES as tetros

# constants
screen_width = 390
screen_height = 750
block_size = 30
grid_width = screen_width // block_size
grid_height = screen_height // block_size
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
def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(grid_width)] for _ in range(grid_height)]
    for (x, y), color in locked_positions.items():
        if y >= 0:
            grid[y][x] = color
    return grid


def draw_grid(surface, grid):
    for y in range(grid_height):
        for x in range(grid_width):
            pygame.draw.rect(
                surface,
                grid[y][x],
                (x * block_size, y * block_size, block_size, block_size),
            )
            pygame.draw.rect(
                surface,
                (128, 128, 128),
                (x * block_size, y * block_size, block_size, block_size),
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


def draw_stats(surface, score, level):
    font = pygame.font.SysFont("comicsans", 30)
    score_label = font.render(f"Score: {score}", True, (255, 255, 255))
    level_label = font.render(f"Level: {level}", True, (255, 255, 255))
    surface.blit(score_label, (10, 10))
    surface.blit(level_label, (10, 40))  # below the score


# main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tetromina")
    clock = pygame.time.Clock()
    score = 0
    grid = create_grid(locked_positions)
    key, shape = choice(list(tetros.items()))
    current_piece = Piece(3, 0, shape, key)
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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            current_speed = soft_drop_speed
        else:
            current_speed = fall_speed
        # piece falls automagically
        if fall_time / 1000 > current_speed:
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                # lock the piece
                for x, y in convert_shape_format(current_piece):
                    if y >= 0:
                        locked_positions[(x, y)] = colors[current_piece.shape_key]
                temp_grid = create_grid(locked_positions)
                # clear any full rows
                rows = clear_rows(temp_grid, locked_positions)
                if rows > 0:
                    points = calculate_score(rows)
                    score += points
                    lines_cleared += rows

                    # level up every 5 lines
                    new_level = (lines_cleared // 2) + 1
                    if new_level != level:
                        level = new_level
                        # decrease falls speed sligthly
                        fall_speed = max(0.1, 0.5 - (level - 1) * 0.05)
                        print(
                            f"level up! level:{level}, new fall speed: {fall_speed:.2f}s"
                        )
                    print(f"Cleared {rows} row(s)! current score:{score}")
                # generate new piece
                key, shape = choice(list(tetros.items()))
                current_piece = Piece(3, 0, shape, key)
                grid = create_grid(locked_positions)
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
                    # lock piece
                    for x, y in convert_shape_format(current_piece):
                        if y >= 0:
                            locked_positions[(x, y)] = colors[current_piece.shape_key]
                    # clear any full rows
                    temp_grid = create_grid(locked_positions)
                    rows = clear_rows(temp_grid, locked_positions)
                    if rows > 0:
                        points = calculate_score(rows)
                        score += points
                        lines_cleared += rows

                        # level up every 5 lines
                        new_level = (lines_cleared // 2) + 1
                        if new_level != level:
                            level = new_level
                            # decrease falls speed sligthly
                            fall_speed = max(0.1, 0.5 - (level - 1) * 0.05)
                            print(
                                f"level up! level:{level}, new fall speed: {fall_speed:.2f}s"
                            )
                        print(f"Cleared {rows} row(s)! current score:{score}")

                    key, shape = choice(list(tetros.items()))
                    current_piece = Piece(3, 0, shape, key)

                    # Check game over
                    if not valid_space(current_piece, grid):
                        print("Game Over!")
                        running = False

        # draw current piece on grid
        # Rebuild a separate grid for the ghost piece
        ghost_piece = get_ghost_piece(current_piece, grid)
        for x, y in convert_shape_format(ghost_piece):
            if y >= 0:
                r, g, b = colors[ghost_piece.shape_key]
                ghost_color = (r // 2, g // 2, b // 2)
                grid[y][x] = ghost_color  # temporarily overwrite grid color
        # First, update grid with current piece (like you have)
        for x, y in convert_shape_format(current_piece):
            if y >= 0:
                grid[y][x] = colors[current_piece.shape_key]

        # Draw everything
        screen.fill((0, 0, 0))
        draw_grid(screen, grid)

        # Reset the current piece color in grid so it’s not permanently overwritten
        for x, y in convert_shape_format(current_piece):
            if y >= 0:
                grid[y][x] = colors[current_piece.shape_key]
        draw_stats(screen, score, level)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
