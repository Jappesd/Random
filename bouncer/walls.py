import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, width, height=600, deadly=False):
        super().__init__()
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "wall.png")).convert()

        self.deadly = deadly
        if deadly:
            self.image = pygame.image.load(
                os.path.join(ASSETS_DIR, "bottom_spike.png")
            ).convert_alpha()

        self.rect = self.image.get_rect(topleft=(x, 0))
