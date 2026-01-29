import pygame
from bullet import Bullet
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=2, color=(255, 255, 0), width=40, height=30):
        super().__init__()
        self.img = pygame.Surface((width, height))
        self.img.fill(color)
        self.rect = self.img.get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = 1  # 1 = right, -1 = left

    def update(self):
        self.rect.x += self.speed * self.direction

    def shift_down(self, amount=10):
        self.rect.y += amount
        self.direction *= -1

    def shoot(self, bullet_group):
        if random.random() < 0.01:  # 1% chance per frame to shoot
            bullet = Bullet(
                self.rect.centerx, self.rect.bottom, speed=5, color=(255, 255, 255)
            )
            bullet_group.add(bullet)
