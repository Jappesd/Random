import pygame
from player import Player
from bullet import Bullet
from enemy import Enemy
from random import random
import math

# initialization and constants
pygame.init()
pygame.font.init()
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Invaders")
font = pygame.font.SysFont("Impact", 24)
clock = pygame.time.Clock()
# Constants
FPS = 60
current_wave = 1
enemy_speed = 1
enemy_direction = 1  # 1 = right, -1 = left # initial direction

# --- Sprite groups ---
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# -- Create player --
player = Player(
    x=screen_width // 2, y=screen_height - 50
)  # player centered and slightly off bottom
all_sprites.add(player)  # add player to the sprite group


# -- Create enemies --
def make_enemies():
    for row in range(4):
        for col in range(10):
            enemy = Enemy(x=100 + col * 70, y=50 + row * 50)
            enemies.add(enemy)
            all_sprites.add(enemy)


# -- Event handling --
def handle_event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            player.shoot()
            for bullet in player.bullets:
                all_sprites.add(bullet)
                player_bullets.add(bullet)


# -- Enemy shooting
def get_shooting_enemies(enemies):
    bottom_enemies = {}
    for enemy in enemies:
        col = enemy.rect.x
        if col not in bottom_enemies or enemy.rect.y > bottom_enemies[col].rect.y:
            bottom_enemies[col] = enemy
    return list(bottom_enemies.values())


# -- Enemy Movement --
def enemy_movement(enemies, direction, enemy_speed):
    """
    Move enemies as a group.
    Speed increases each time they hit a wall.
    Returns new direction and updated enemy_speed.
    """
    if not enemies:
        return direction, enemy_speed

    move_down = False

    # Check if any enemy hits a wall
    for enemy in enemies:
        if direction == 1 and enemy.rect.right >= screen_width - 1:
            move_down = True
            break
        if direction == -1 and enemy.rect.left <= 1:
            move_down = True
            break

    if move_down:
        direction *= -1
        for enemy in enemies:
            enemy.rect.y += 40
    else:
        for enemy in enemies:
            enemy.rect.x += enemy_speed * direction
    return direction, enemy_speed


# -- Draw everything --
def draw_all(screen, current_wave, current_time):
    # text
    screen.fill((0, 0, 0))
    if not player.shield_used and not player.shield_active:
        cooldown_ratio = 1
        cdbar_width = 100
        cdbar_height = 10
        pygame.draw.rect(
            screen, (100, 100, 100), (10, 40, cdbar_width, cdbar_height)
        )  # full bg
        pygame.draw.rect(
            screen, (0, 200, 255), (10, 40, cdbar_width * cooldown_ratio, cdbar_height)
        )
    else:
        if player.shield_active:
            pulse = 5 * math.sin(pygame.time.get_ticks() / 100)
            bubble_radius = max(player.rect.width, player.rect.height) // 2 + 10 + pulse
            glow_surf = pygame.Surface(
                (bubble_radius * 2, bubble_radius * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                glow_surf,
                (0, 200, 255, 100),
                (bubble_radius, bubble_radius),
                int(bubble_radius),
            )
            screen.blit(
                glow_surf,
                (
                    player.rect.centerx - bubble_radius,
                    player.rect.centery - bubble_radius,
                ),
            )
            pygame.draw.circle(
                screen, (0, 200, 255), player.rect.center, int(bubble_radius), 3
            )  # outlin
        cooldown_ratio = min(
            (current_time - player.shield_timer) / player.shield_cooldown, 1
        )
        cdbar_width = 100
        cdbar_height = 10
        pygame.draw.rect(
            screen, (100, 100, 100), (10, 40, cdbar_width, cdbar_height)
        )  # full cd bar bg
        pygame.draw.rect(
            screen, (0, 200, 255), (10, 40, cdbar_width * cooldown_ratio, cdbar_height)
        )
    health_text = font.render(f"Health: {player.health}", True, (255, 0, 0))
    score_text = font.render(f"Score: {player.score}", True, (255, 255, 0))
    wave_text = font.render(f"Wave: {current_wave}", True, (0, 200, 255))
    bar_width = 200
    bar_height = 20
    health_ratio = max(player.health / player.max_health, 0)  # normalize 0-1

    all_sprites.draw(screen)
    enemy_bullets.draw(screen)
    # screen.blit(health_text, (10, 10))  # top left corner
    # pygame.draw.rect(screen,())
    pygame.draw.rect(screen, (255, 0, 0), (10, 20, bar_width, bar_height))  # full bar
    pygame.draw.rect(
        screen, (0, 255, 0), (10, 20, bar_width * health_ratio, bar_height)
    )  # current health
    screen.blit(score_text, (screen_width - 120, 10))  # top right corner
    screen.blit(wave_text, (screen_width // 2 - wave_text.get_width() // 2, 10))


def handle_menu():
    # somewhere global or in your handle_menu()
    start_button_rect = pygame.Rect(
        screen_width // 2 - 100,  # x
        screen_height // 2 + 200,  # y
        200,  # width
        50,  # height
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_game()
                pygame.time.wait(200)
                return "playing"
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if start_button_rect.collidepoint(event.pos):
                reset_game()
                pygame.time.wait(100)
                return "playing"
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 200, 255), start_button_rect)  # button bg
    start_text = font.render("START", True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    title = font.render("Spake invander", True, (255, 255, 255))
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 200))
    screen.blit(start_text, start_text_rect)
    pygame.display.update()
    return "menu"


def handle_game_over():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return "menu"
    screen.fill((0, 0, 0))
    over_text = font.render("GAME OVER", True, (255, 50, 50))
    score_text = font.render(f"Final Score: {player.score}", True, (255, 255, 255))
    prompt = font.render("Press R to return to menu", True, (200, 200, 200))

    screen.blit(over_text, (screen_width // 2 - over_text.get_width() // 2, 200))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 240))
    screen.blit(prompt, (screen_width // 2 - prompt.get_width() // 2, 280))

    pygame.display.update()
    return "over"


def reset_game():
    global enemies, enemy_bullets, player_bullets
    global current_wave, enemy_speed, score, state
    state = "playing"
    player.reset()
    enemies.empty()
    all_sprites.empty()
    enemy_bullets.empty()
    player_bullets.empty()
    current_wave = 1
    all_sprites.add(player)
    enemy_speed = 2
    score = 0
    make_enemies()


def handle_playing():
    global enemy_direction, enemy_speed, current_wave, score, state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # player inputs move,shoot
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pressed = pygame.mouse.get_pressed()[0]  # left mouse
    mouse_pos = pygame.mouse.get_pos()  # returns x,y
    current_time = pygame.time.get_ticks()
    if mouse_buttons[2]:
        # only active if not currently active and not on cooldown
        if not player.shield_active:
            if (
                not player.shield_used
                or current_time - player.shield_timer >= player.shield_cooldown
            ):
                player.shield_active = True
                player.shield_used = True
                player.shield_timer = current_time
    if (
        player.shield_active
        and current_time - player.shield_timer >= player.shield_duration
    ):
        player.shield_active = False
    player.rect.centerx = mouse_pos[0]
    player.rect.centery = mouse_pos[1]
    # keep withing screen bounds
    player.rect.x = max(0, min(player.rect.x, screen_width - player.rect.width))
    player.rect.y = max(0, min(player.rect.y, screen_height - player.rect.height))
    if mouse_pressed:
        player.shoot()
        for bullet in player.bullets:
            all_sprites.add(bullet)
            player_bullets.add(bullet)
    # collisions
    enemy_hits = pygame.sprite.groupcollide(
        enemies, player_bullets, dokilla=True, dokillb=True
    )
    enemy_collision = pygame.sprite.spritecollide(player, enemies, dokill=True)
    player_hits = pygame.sprite.spritecollide(player, enemy_bullets, dokill=True)
    # -- Enemy movement
    prev_direction = enemy_direction
    enemy_direction, enemy_speed = enemy_movement(enemies, enemy_direction, enemy_speed)
    if enemy_direction != prev_direction:
        enemy_speed += 1
        enemy_speed = min(enemy_speed, 10)
    for enemy in enemies:
        if enemy.rect.bottom >= 750:
            print(f"Game over! Score: {player.score}")
            state = "over"
            break

    # -- Enemy shooting
    base_shoot_chance = 0.005
    wave_multiplier = max(1, current_wave)
    shoot_chance = min(base_shoot_chance * wave_multiplier, 0.2)
    for enemy in get_shooting_enemies(enemies):
        enemy.shoot(enemy_bullets, shoot_chance)
    # -- Update sprites
    all_sprites.update()
    enemy_bullets.update()
    if enemy_collision:
        state = "over"
    for hit in enemy_hits:
        player.score += 10 * current_wave
    if player_hits and not player.shield_active:
        player.health -= len(player_hits)  # decrease hp by number of hits
        print("Health:", player.health)
        if player.health <= 0:
            print("Game Over! Score:", player.score)
            state = "over"
    # -- Respawn enemies if none left
    if len(enemies) == 0:
        make_enemies()
        current_wave += 1
        enemy_direction = 1
        enemy_speed = 1 + current_wave  # reset enemy speed and add wave speed

    # -- Draw
    draw_all(screen, current_wave, current_time)
    pygame.display.update()


def main():
    running = True
    global state
    state = "menu"
    while running:
        if state == "menu":
            pygame.mouse.set_visible(True)
            state = handle_menu()
        elif state == "playing":
            pygame.mouse.set_visible(False)
            handle_playing()
            clock.tick(FPS)
        elif state == "over":
            pygame.mouse.set_visible(True)
            state = handle_game_over()
    pygame.quit()


if __name__ == "__main__":
    main()
