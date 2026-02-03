import pygame
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5, color=(0, 255, 0), width=35, height=30):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.bullets = pygame.sprite.Group()
        self.max_health = 3
        self.health = 3
        self.score = 0
        self.shoot_cooldown = 200  # ms time between shots
        self.last_shot = 0
        # shield ability
        self.shield_active = False
        self.shield_duration = 2000  # ms active per usage (2 seconds)
        self.shield_cooldown = 10000  # ms cooldown after usage
        self.shield_timer = 0  # tracks when shield was last used
        self.shield_used = False

    def move(self, dx=0, dy=0):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        # bounds
        self.rect.x = max(0, min(self.rect.x, 1200 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 800 - self.rect.height))

    def reset(self):
        self.rect.midbottom = (600, 750)
        self.speed = 5
        self.health = self.max_health
        self.score = 0
        self.shield_active = False
        self.shield_used = False

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)
            self.last_shot = now
