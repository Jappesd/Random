import pygame
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


class Hazard(pygame.sprite.Sprite):
    def __init__(self, screen_width=400, screen_height=600):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(ASSETS_DIR, "hazard.png")
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20, screen_width - 40)
        self.rect.y = -20  # start above screen
        self.scroll_speed = random.uniform(2, 5)  # random speed

    def update(self):
        self.rect.y += self.scroll_speed
        if self.rect.top > 600:
            self.kill()
