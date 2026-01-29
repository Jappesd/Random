import pygame
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5, color=(0, 255, 0), width=50, height=30):
        super().__init__()
        self.img = pygame.Surface((width, height))
        self.img.fill(color)
        self.rect = self.img.get_rect(center=(x, y))
        self.speed = speed
        self.bullets = pygame.sprite.Group()

    def move(self, dx=0, dy=0):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        # screen bounds

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.bullets.add(bullet)
