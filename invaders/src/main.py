import pygame
from player import Player
from bullet import Bullet
from enemy import Enemy
from random import random

# initialization and constants
pygame.init()
pygame.font.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Invaders")
font = pygame.font.SysFont("Impact", 24)
clock = pygame.time.Clock()
# Constants
FPS = 60


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
    for row in range(3):
        for col in range(8):
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
            enemy.rect.y += 20
    else:
        for enemy in enemies:
            enemy.rect.x += enemy_speed * direction
    return direction, enemy_speed


# -- Draw everything --
def draw_all(screen, current_wave):
    # text
    health_text = font.render(f"Health: {player.health}", True, (255, 0, 0))
    score_text = font.render(f"Score: {player.score}", True, (255, 255, 0))
    wave_text = font.render(f"Wave: {current_wave+1}", True, (0, 200, 255))
    bar_width = 200
    bar_height = 20
    health_ratio = max(player.health / player.max_health, 0)  # normalize 0-1
    screen.fill((0, 0, 0))
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


def main():
    running = True
    current_wave = 0
    enemy_speed = 1
    enemy_direction = 1  # 1 = right, -1 = left # initial direction
    make_enemies()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # else:
            #     handle_event(event)

        enemy_hits = pygame.sprite.groupcollide(
            enemies, player_bullets, dokilla=True, dokillb=True
        )
        player_hits = pygame.sprite.spritecollide(player, enemy_bullets, dokill=True)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.shoot()
            for bullet in player.bullets:
                all_sprites.add(bullet)
                player_bullets.add(bullet)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.move(dx=-1)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.move(dx=1)
        # -- Enemy movement
        prev_direction = enemy_direction
        enemy_direction, enemy_speed = enemy_movement(
            enemies, enemy_direction, enemy_speed
        )
        if enemy_direction != prev_direction:
            enemy_speed += 0.5
            enemy_speed = min(enemy_speed, 5)
        for enemy in enemies:
            if enemy.rect.bottom >= 550:
                print(f"Game over! Score: {player.score}")
                running = False
                break

        # -- Enemy shooting
        base_shoot_chance = 0.005

        shoot_chance = min(base_shoot_chance + 0.005 * (current_wave), 0.2)
        for enemy in get_shooting_enemies(enemies):
            enemy.shoot(enemy_bullets, shoot_chance)

        # -- Update sprites
        all_sprites.update()
        enemy_bullets.update()
        for hit in enemy_hits:
            player.score += 10
        if player_hits:
            player.health -= len(player_hits)  # decrease hp by number of hits
            print("Health:", player.health)
            if player.health <= 0:
                print("Game Over! Score:", player.score)
                running = False
        # -- Respawn enemies if none left
        if len(enemies) == 0:
            make_enemies()
            current_wave += 1
            enemy_direction = 1
            enemy_speed = 1 + current_wave  # reset enemy speed and add wave speed

        # -- Draw
        draw_all(screen, current_wave)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
