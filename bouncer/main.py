import pygame
import random
from player import Player
from walls import Wall
from hazards import Hazard
import os

# Get folder of main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
highscore_file = os.path.join(BASE_DIR, "highscore.txt")
asset_dir = os.path.join(BASE_DIR, "assets")


def save_highscore(score):
    with open(highscore_file, "w") as f:
        f.write(f"{score:.2f}")


def load_highscore():
    if os.path.exists(highscore_file):
        with open(highscore_file, "r") as f:
            try:
                return float(f.read())
            except:
                return 0.0
    else:
        return 0.0


pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncer")
clock = pygame.time.Clock()
FPS = 60
# Load background
bg_image = pygame.image.load(os.path.join(asset_dir, "bg.png")).convert()
# Sprite groups
all_sprites = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
hazard_group = pygame.sprite.Group()

# Create player
player = Player(WIDTH // 2, HEIGHT - 100)
all_sprites.add(player)

# Create walls
left_wall = Wall(0, 20)
right_wall = Wall(WIDTH - 20, 20)
bottom_wall = Wall(0, WIDTH, height=20, deadly=True)  # full width, redspikke
bottom_wall.rect.top = HEIGHT - 20  # position at bottom
walls_group.add(left_wall, right_wall, bottom_wall)
all_sprites.add(left_wall, right_wall, bottom_wall)

# Game variables
scroll_speed = 5
hazard_timer = 0
hazard_interval = 60
running = True
game_started = False
game_over = False
font = pygame.font.SysFont(None, 36)
start_time = 0
score = 0.0
highscore = load_highscore()


def reset_game():
    global all_sprites, hazard_group, player, game_started, game_over
    all_sprites.empty()
    hazard_group.empty()
    player = Player(WIDTH // 2, HEIGHT - 100)
    all_sprites.add(player)
    all_sprites.add(left_wall, right_wall, bottom_wall)
    game_started = False
    game_over = False
    score = 0
    start_time = 0


# Main loop
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started:
                    game_started = True  # start the game
                    start_time = pygame.time.get_ticks()  # gets current time in ms
                if not game_over:
                    player.flap()
            if event.key == pygame.K_r and game_over:
                reset_game()  # restart game

    # Update
    if game_started and not game_over:
        all_sprites.update()
        current_time = pygame.time.get_ticks()
        score = (current_time - start_time) / 1000

        # Spawn hazards

        hazard_timer += 1
        if hazard_timer >= hazard_interval:
            hazard_timer = 0
            wall = random.choice([left_wall, right_wall])
            hazard = Hazard()
            hazard_group.add(hazard)
            all_sprites.add(hazard)

        # Check collisions with hazards
        hit_hazards = pygame.sprite.spritecollide(
            player, hazard_group, False, pygame.sprite.collide_mask
        )
        if hit_hazards:
            player.take_dmg()
            for hazard in hit_hazards:
                hazard.kill()  # optional: remove hazard on hit

        deadly_hit = pygame.sprite.spritecollide(player, walls_group, False)
        for wall in deadly_hit:
            if getattr(wall, "deadly", False):
                game_over = True
        if player.hp <= 0:
            game_over = True
    # Draw
    screen.blit(bg_image)
    heart_image = pygame.image.load(
        os.path.join(asset_dir, "heart.png")
    ).convert_alpha()
    for i in range(player.hp):
        screen.blit(heart_image, (30 + i * (heart_image.get_width() + 2), 50))
    all_sprites.draw(screen)

    score_text = font.render(f"Time: {score:.2f}s", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if not game_started and not game_over:
        text = font.render("Press SPACE to start", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    if game_over:
        if score > highscore:
            highscore = score
            save_highscore(highscore)
        over_text = font.render("Game Over!", True, (255, 0, 0))
        restart_text = font.render("Press R to restart", True, (255, 255, 255))
        final_score_text = font.render(
            f"Time survived: {score:.2f}s", True, (255, 255, 255)
        )
        # Always show current highscore
        highscore_text = font.render(
            f"Highscore: {highscore:.2f}s", True, (255, 255, 255)
        )
        screen.blit(highscore_text, (WIDTH - highscore_text.get_width() - 10, 10))
        screen.blit(
            over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 20)
        )
        screen.blit(
            restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20)
        )
        screen.blit(
            final_score_text,
            (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 0),
        )
    pygame.display.flip()

pygame.quit()
