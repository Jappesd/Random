import pygame
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5, color=(0, 255, 0), width=50, height=30):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.bullets = pygame.sprite.Group()
        self.max_health = 3
        self.health = 3
        self.score = 0
        self.shoot_cooldown = 200
        self.last_shot = 0

    def move(self, dx=0, dy=0):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    # screen bounds

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)
            self.last_shot = now
