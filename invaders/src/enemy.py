import pygame
from bullet import Bullet
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type="standard"):
        super().__init__()
        self.type = type
        # define type properties
        if type == "fast":
            self.health = 1
            self.speed_multiplier = 1.5
            self.shoot_chance = 0.001
            self.color = (255, 100, 100)
        elif type == "tank":
            self.health = 5
            self.speed_multiplier = 0.5
            self.shoot_chance = 0.01
            self.color = (100, 255, 100)
        elif type == "shooter":
            self.health = 2
            self.speed_multiplier = 1
            self.shoot_chance = 0.02
            self.color = (200, 200, 0)
        else:  # standard
            self.health = 2
            self.speed_multiplier = 1
            self.shoot_chance = 0.005
            self.color = (255, 255, 255)
        self.image = pygame.image.load("assets/imgs/enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = float(self.rect.x)  # precise location

    def update(self):
        pass
        # self.rect.x += self.speed * self.direction

    def shift_down(self, amount=10):
        self.rect.y += amount
        self.direction *= -1

    def shoot(self, bullet_group, chance=None):
        shoot_chance = chance if chance is not None else self.shoot_chance
        if random.random() < shoot_chance:
            bullet = Bullet(
                self.rect.centerx, self.rect.bottom, speed=5, color=(255, 255, 255)
            )
            bullet_group.add(bullet)
