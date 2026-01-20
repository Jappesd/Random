import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(ASSETS_DIR, "player.png")
        ).convert_alpha()

        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.vel_y = 0
        self.gravity = 0.5
        self.flap_strength = -10
        self.vel_x = 3
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, 400)
        self.hp = 3

    def take_dmg(self):
        self.hp -= 1

    def update(self):

        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
        if self.rect.left <= 20 or self.rect.right >= 380:
            self.vel_x *= -1.1  # increase speed 10%

            # Cap speed immediately
            max_speed = 10
            if self.vel_x > max_speed:
                self.vel_x = max_speed
            elif self.vel_x < -max_speed:
                self.vel_x = -max_speed

    def flap(self):
        self.vel_y = self.flap_strength
