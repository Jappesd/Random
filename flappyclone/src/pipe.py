import pygame
import random
import os


class Pipe:
    # All caps for class global variables
    GAP = 160
    SPEED = 3
    WIDTH = 52
    MIN_GAP_Y = 50

    def __init__(self, x, screen_height):
        self.x = x
        self.screen_height = screen_height
        self.passed = False
        self.CAP_HEIGHT = 12  # sprite height
        # random gap position
        self.gap_y = random.randint(
            self.MIN_GAP_Y, screen_height - self.GAP - self.MIN_GAP_Y
        )

        # top and bottom heights
        self.top_shaft_height = self.gap_y - 12  # take away the cap height
        self.bottom_shaft_height = (
            screen_height - self.gap_y - self.GAP - 12
        )  # bottom cap height

        # load pipe img
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, "..", "assets")

        self.cap_img = pygame.image.load(
            os.path.join(assets_dir, "pipecap.png")
        ).convert_alpha()
        self.shaft_img = pygame.image.load(
            os.path.join(assets_dir, "pipeshaft.png")
        ).convert_alpha()

        # scale shaft to top/bottom heights
        self.top_shaft_img = pygame.transform.scale(
            self.shaft_img, (self.WIDTH, self.top_shaft_height)
        )
        self.bottom_shaft_img = pygame.transform.scale(
            self.shaft_img, (self.WIDTH, self.bottom_shaft_height)
        )

        # top cap flipped vertically
        self.top_cap_img = pygame.transform.flip(self.cap_img, False, True)
        self.bottom_cap_img = self.cap_img

        # collision rects shaft+cap
        # top rect
        self.top_rect = pygame.Rect(
            self.x,
            0,  # top-left corner
            self.WIDTH,
            self.top_shaft_height + self.CAP_HEIGHT,  # include at the bottom of shaft
        )
        # bottom pipe rect
        bottom_shaft_y = self.screen_height - self.bottom_shaft_height - self.CAP_HEIGHT
        self.bottom_rect = pygame.Rect(
            self.x,
            bottom_shaft_y - self.CAP_HEIGHT,  # moves rect so it includes cap
            self.WIDTH,
            self.bottom_shaft_height + self.CAP_HEIGHT,
        )

    def update(self):
        # update position of the pipe
        self.x -= self.SPEED
        self.top_rect.topleft = (self.x, 0)
        bottom_shaft_y = self.screen_height - self.bottom_shaft_height - self.CAP_HEIGHT
        self.bottom_rect.topleft = (self.x, bottom_shaft_y - self.CAP_HEIGHT)

    def draw(self, screen):
        # top pipe
        top_cap_y = self.top_shaft_height  # cap is at the bottom of the shaft
        screen.blit(self.top_shaft_img, (self.x, 0))
        # cap flipped
        screen.blit(self.top_cap_img, (self.x, top_cap_y))
        # bottom pipe
        bottom_y = self.screen_height - self.bottom_shaft_height - 12
        screen.blit(self.bottom_shaft_img, (self.x, bottom_y))
        bottom_cap_y = bottom_y - 12
        screen.blit(self.bottom_cap_img, (self.x, bottom_cap_y))

    def get_rects(self):
        return [self.top_rect, self.bottom_rect]

    def off_screen(self):
        return self.x + self.WIDTH < 0
