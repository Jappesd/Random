# game loop and initialization
import pygame
from piece import Piece
from random import choice, random
from pieces import TETROMINOES as tetros
from pieces import WILD_CARDS as WILD
from scorepop import ScorePop
from pieces import COLORS as colors

# constants
screen_width = 390
screen_height = 750
block_size = 30
game_state = "menu"
# GAME STATES
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
PAUSED = "paused"
# playing field
grid_width = screen_width // block_size
grid_height = screen_height // block_size
# sidebar margin (left shows score and level and right shows next piece)
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


# draws the text to sidebars
def draw_sidebar(surface, score, level):
    font = pygame.font.SysFont("comicsans", 24)
    big_font = pygame.font.SysFont("comicsans", 30)
    # level (left sidebar)
    level_label = big_font.render(f"Level: {level}", True, (255, 255, 255))
    surface.blit(level_label, (left_sidebar_x - 20, 40))

    # score (right sidebar)
    score_label = font.render(f"Score: {score}", True, (255, 255, 0))
    surface.blit(score_label, (left_sidebar_x - 20, 80))


# gets pieces dimension
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


# draws next piece preview to the right sidebar
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


# creates the grid while taking into account the currently locked pieces
def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(grid_width)] for _ in range(grid_height)]
    for (x, y), color in locked_positions.items():
        if y >= 0:
            grid[y][x] = color
    return grid


# draws the grid to the play area
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


# checks if the space for the current block is valid
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


# gives out the "ghost piece" that shows a shadow of where the block will go
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


# computes score per rows cleared
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


# draws pause menu
def draw_pause(screen):
    """
    Draws the pause menu with multiple lines of text, with keys highlighted as buttons.
    """
    font = pygame.font.SysFont("comicsans", 48)
    small_font = pygame.font.SysFont("comicsans", 32)

    # lines to display: (text before key, key, text after key)
    lines = [
        ("PAUSED", None, None),
        ("Press ", "R", " to Restart"),
        ("Press ", "M", " for Menu"),
    ]

    # calculate total height for centering
    total_height = 0
    rendered_lines = []
    for pre, key, post in lines:
        if key:
            pre_surf = small_font.render(pre, True, (255, 255, 255))
            key_surf = small_font.render(
                key, True, (255, 255, 0)
            )  # highlight key in yellow
            post_surf = small_font.render(post, True, (255, 255, 255))
            rendered_lines.append((pre_surf, key_surf, post_surf))
            total_height += (
                max(
                    pre_surf.get_height(), key_surf.get_height(), post_surf.get_height()
                )
                + 10
            )
        else:
            surf = font.render(pre, True, (255, 255, 255))
            rendered_lines.append((surf,))
            total_height += surf.get_height() + 10

    start_y = screen_height // 2 - total_height // 2
    y = start_y

    # draw each line
    for parts in rendered_lines:
        if len(parts) == 1:
            surf = parts[0]
            x = window_width // 2 - surf.get_width() // 2
            screen.blit(surf, (x, y))
            y += surf.get_height() + 10
        else:
            pre_surf, key_surf, post_surf = parts
            line_width = (
                pre_surf.get_width() + key_surf.get_width() + post_surf.get_width()
            )
            x = window_width // 2 - line_width // 2
            screen.blit(pre_surf, (x, y))
            x += pre_surf.get_width()
            # optional: draw a rectangle behind key to look like a button
            padding = 4
            pygame.draw.rect(
                screen,
                (50, 50, 50),
                (
                    x - padding,
                    y - padding,
                    key_surf.get_width() + padding * 2,
                    key_surf.get_height() + padding * 2,
                ),
            )
            screen.blit(key_surf, (x, y))
            x += key_surf.get_width()
            screen.blit(post_surf, (x, y))
            y += (
                max(
                    pre_surf.get_height(), key_surf.get_height(), post_surf.get_height()
                )
                + 10
            )


# draws all game components
def draw_game(screen, grid, current_piece, next_piece, score, level, game_state):
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
    if game_state == "paused":
        draw_pause(screen)
    pygame.display.update()


# flashes the row that is cleared
def flasher(screen, grid, locked, rows_to_flash, flash_times=4, flash_speed=80):
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


# handles piece locking in place and generating the next pieces
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
        # levels up every 5 lines
        new_level = (lines_cleared // 5) + 1
        if new_level != level:
            level = new_level
            fall_speed = max(0.1, 0.5 - (level - 1) * 0.08)  # 8% faster per level
        # print(f"Level Up! Level: {level}, new falls speed: {fall_speed:.2f}s")
    # print(f"Cleared {rows} row(s)! Current score: {score}")

    # shift next_piece to current piece
    current_piece = spawn_piece(next_piece.shape_key, next_piece.shape)

    # generate next_piece
    key, shape = choose_piece()
    next_piece = spawn_piece(key, shape)
    # rebuild grid for drawing
    grid = create_grid(locked_positions)

    # return all updated values
    return current_piece, next_piece, grid, score, lines_cleared, level, fall_speed


# start menu screen
def draw_menu(screen):
    screen.fill((126, 140, 84))
    font_big = pygame.font.SysFont("comicsans", 60)
    font_small = pygame.font.SysFont("comicsans", 30)

    title = font_big.render("Tetros", True, (255, 255, 255))
    prompt = font_small.render("Press ENTER to Start", True, (0, 0, 0))

    screen.blit(title, (window_width // 2 - title.get_width() // 2, 250))
    screen.blit(prompt, (window_width // 2 - prompt.get_width() // 2, 350))

    pygame.display.update()


# game over screen
def draw_game_over(screen, score):
    screen.fill((0, 0, 0))
    font_big = pygame.font.SysFont("comicsans", 50)
    font_small = pygame.font.SysFont("comicsans", 30)

    over = font_big.render("GAME OVER", True, (255, 50, 50))
    score_text = font_small.render(f"SCORE: {score}", True, (255, 255, 255))
    prompt = font_small.render("Press R to Restart", True, (200, 200, 200))
    prompt2 = font_small.render("Press M for Menu", True, (200, 200, 200))

    screen.blit(over, (window_width // 2 - over.get_width() // 2, 240))
    screen.blit(score_text, (window_width // 2 - score_text.get_width() // 2, 320))
    screen.blit(prompt, (window_width // 2 - prompt.get_width() // 2, 380))
    screen.blit(prompt2, (window_width // 2 - prompt2.get_width() // 2, 440))
    pygame.display.update()


# piece generator returns key,shape tuple
def choose_piece():
    # wild chance is 10% for a shape from "WILD" dict U shape, 1x1 and 3x3
    wild_chance = 0.1  # 10% chance for a wild card
    global tetros, WILD
    if random() < wild_chance:
        key, shape = choice(list(WILD.items()))
    else:
        key, shape = choice(list(tetros.items()))
    return key, shape


# generates the piece and centers it horizontally
def spawn_piece(shape_key, shape):
    piece = Piece(0, 0, shape, shape_key)
    min_x, max_x, min_y, max_y = get_piece_bounding_box(piece)
    # center horizontally
    piece.x = (grid_width - (max_x - min_x + 1)) // 2 - min_x
    piece.y = 0 - min_y
    return piece


# main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((window_width, screen_height))
    pygame.display.set_caption("Tetromina")
    clock = pygame.time.Clock()
    game_state = MENU  # changes from "menu" | "paused" | "game_over" | "playing"
    score = 0
    grid = create_grid(locked_positions)

    # initial pieces
    key, shape = choose_piece()
    current_piece = spawn_piece(key, shape)
    # initial next piece for preview
    next_key, next_shape = choose_piece()
    next_piece = spawn_piece(next_key, next_shape)
    # variables
    level = 1
    lines_cleared = 0
    fall_time = 0
    fall_speed = 0.5  # seconds
    soft_drop_speed = 0.05  # speed of the drop when holding downkey
    running = True  # turns False when quitting the game. ends operation
    while running:
        clock.tick()
        grid = create_grid(locked_positions)  # recreates the grid at the start of loop

        if game_state == "paused":
            fall_time = 0
        # soft drop
        keys = pygame.key.get_pressed()
        current_speed = soft_drop_speed if keys[pygame.K_DOWN] else fall_speed
        if game_state == "playing":
            fall_time += clock.get_rawtime()  # ticks ++ for fall time
            # piece falls automagically after enought ticks
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
                        game_state = GAME_OVER

                fall_time = 0  # reset fall time at the end of the loop

        # event handling
        for event in pygame.event.get():  # gets all events
            if event.type == pygame.QUIT:  # pressing X to close the gamescreen
                running = False

            if event.type == pygame.KEYUP:  # when releasing a key
                if game_state == "paused":
                    if (
                        event.key == pygame.K_r
                    ):  # restart current game/ clears everything
                        locked_positions.clear()
                        grid = create_grid(locked_positions)
                        score = 0
                        level = 1
                        lines_cleared = 0
                        fall_speed = 0.5

                        key, shape = choice(list(tetros.items()))
                        current_piece = Piece(3, 0, shape, key)
                        next_key, next_shape = choice(list(tetros.items()))
                        next_piece = Piece(0, 0, next_shape, next_key)

                        game_state = PLAYING

                    elif event.key == pygame.K_m:  # go back to menu from pause
                        game_state = MENU

                if event.key == pygame.K_ESCAPE:  # pressing esc pauses/resumes
                    if game_state == "playing":
                        game_state = "paused"
                    elif game_state == "paused":
                        game_state = "playing"
                if (
                    game_state == MENU and event.key == pygame.K_RETURN
                ):  # if game is in menu and presses Enter
                    # reset errythin
                    locked_positions.clear()
                    grid = create_grid(locked_positions)
                    score = 0
                    level = 1
                    lines_cleared = 0
                    fall_speed = 0.5

                    key, shape = choose_piece()
                    current_piece = spawn_piece(key, shape)
                    next_key, next_shape = choose_piece()
                    next_piece = spawn_piece(next_key, next_shape)

                    game_state = PLAYING
                elif (
                    game_state == GAME_OVER and event.key == pygame.K_r
                ):  # gameover screen and pressing R
                    # reset errythin
                    locked_positions.clear()
                    grid = create_grid(locked_positions)
                    score = 0
                    level = 1
                    lines_cleared = 0
                    fall_speed = 0.5

                    key, shape = choose_piece()
                    current_piece = spawn_piece(key, shape)
                    next_key, next_shape = choose_piece()
                    next_piece = spawn_piece(next_key, next_shape)

                    game_state = PLAYING
                elif (
                    game_state == GAME_OVER and event.key == pygame.K_m
                ):  # gameover screen and pressing M
                    game_state = MENU  # goes to menu
            if event.type == pygame.KEYDOWN and game_state == "playing":

                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1  # negative x goes left, positive -> right
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1  # reverse logic from left
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1  # pressing up rotates piece 90 degrees
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1  # checks if piece is able to rotate within the current space
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
                        game_state = GAME_OVER
        # draws menu
        if game_state == MENU:
            draw_menu(screen)
            clock.tick(15)
            continue
        # draws game over screen
        if game_state == GAME_OVER:
            draw_game_over(screen, score)
            clock.tick(15)
            continue
        # --- Draw everything ---
        draw_game(screen, grid, current_piece, next_piece, score, level, game_state)
    pygame.quit()


if __name__ == "__main__":
    main()
