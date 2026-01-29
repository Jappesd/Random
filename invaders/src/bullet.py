import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=-10, color=(255, 0, 0), width=4, height=10):
        super().__init__()
        # if speed is negative it goes upward, positive(enemy) goes down
        # Bullet class can be used for both player and enemy bullets.
        # Just set `speed` negative for player (upwards) and positive for enemy (downwards).

        self.img = pygame.Surface((width, height))
        self.img.fill(color)
        self.rect = self.img.get_rect(center=(x, y))
        self.speed = speed
        # Optionally, change `color` to distinguish player bullets (red) from enemy bullets (white).

    def update(self):
        self.rect.y += self.speed
        # remove bullet if it goes off-screen
        if self.rect.bottom < 0 or self.rect.top > 800:
            self.kill()
