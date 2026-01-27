import pygame
from random import choice


class ScorePop:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.vy = -12  # initial upward velocity
        self.vx = 0  # horizontal velocity, set randomly later
        self.gravity = 0.2  # fall speed
        self.font = pygame.font.SysFont("comicsans", 30)
        self.alpha = 255
        # decide horizontal fall direction
        self.vx = choice([-2, -1, 1, 2])

    def update(self):
        # move the pop
        self.y += self.vy
        self.x += self.vx
        # gravity starts pulling down
        self.vy += self.gravity
        # fade out slowly
        self.alpha -= 2

    def draw(self, surface):
        text_surf = self.font.render(self.text, True, (255, 255, 0))
        text_surf.set_alpha(max(self.alpha, 0))
        surface.blit(text_surf, (self.x, self.y))

    def is_ded(self):
        return self.alpha <= 0
