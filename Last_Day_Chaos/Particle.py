import pygame
from random import uniform, randint
from pygame.math import Vector2
import math

# Config
WIDTH, HEIGHT = 1200, 800
FPS = 60
BG_COLOR = (10, 10, 15)
PARTICLE_COUNT = 320
MAX_LINE_DIST = 150
BASE_FORCE_RADIUS = 150
BOOSTED_FORCE = 350
mouse_force_dir = 0  # 1 =repel, -1 = attract, 0 = none
# Init(de beniggign)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Drift")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
running = True
mouse_force_radius = BASE_FORCE_RADIUS
fullscreen = False

# Trail surface
trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


# halpers
def hsv_to_rgp(h, s, v):
    return tuple(
        round(i * 255)
        for i in pygame.Color(0).hsva.__setitem__(0, h)
        or pygame.Color(0).hsva.__setitem__(1, s)
        or pygame.Color(0).hsva.__setitem__(2, v)
        or pygame.Color(0).normalize()
    )


def color_from_hue(h):
    color = pygame.Color(0)
    color.hsva = (h % 360, 80, 100, 100)
    return color


# Particle class
class Particle:
    def __init__(self):
        self.pos = Vector2(uniform(0, WIDTH), uniform(0, HEIGHT))
        self.vel = Vector2(uniform(-2, 2), uniform(-2, 2))
        self.radius = randint(2, 10)
        # self.color = (randint(150, 255), randint(150, 255), randint(150, 255))
        self.hue = uniform(0, 360)

    def update(self, mouse_pos):
        self.pos += self.vel

        # bounce on edges
        if self.pos.x <= 0 or self.pos.x >= WIDTH:
            self.vel.x *= -1
        if self.pos.y <= 0 or self.pos.y >= HEIGHT:
            self.vel.y *= -1
        # mouse repel
        dist = self.pos.distance_to(mouse_pos)
        if dist < mouse_force_radius and dist != 0 and mouse_force_dir != 0:
            direction = (self.pos - mouse_pos).normalize()
            strength = (1 - dist / mouse_force_radius) * 0.6
            self.vel += direction * strength * mouse_force_dir
        # slight damping
        self.vel *= 0.99
        # color shift
        self.hue += 0.2

    def draw(self, surface):
        pygame.draw.circle(surface, color_from_hue(self.hue), self.pos, self.radius)


AUTO_PULL_INTERVAL = 5
AUTO_PULL_DURATION = 0.5
auto_pull_timer = 0
auto_pull_active = False
auto_pull_counter = 0
# Create particles
particles = [Particle() for _ in range(122)]
counter = 0
# main loopy
while running:
    dt = clock.tick(FPS)
    dt_seconds = dt / 1000
    mouse_pos = Vector2(pygame.mouse.get_pos())
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    WIDTH, HEIGHT = screen.get_size()
                    trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    pygame.mouse.set_visible(False)
                else:
                    screen = pygame.display.set_mode((1200, 800))
                    WIDTH, HEIGHT = 1200, 800
                    trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    pygame.mouse.set_visible(True)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                mouse_force_dir = 1
                mouse_force_radius = BOOSTED_FORCE
            if event.button == 3:  # right click
                mouse_force_dir = -1
                mouse_force_radius = BOOSTED_FORCE * 3
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_force_dir = 0
            mouse_force_radius = BASE_FORCE_RADIUS
    auto_pull_timer += dt_seconds
    if not auto_pull_active and auto_pull_timer >= AUTO_PULL_INTERVAL:
        auto_pull_active = True
        auto_pull_timer = 0
        auto_pull_counter = 0
    center = Vector2(WIDTH / 2, HEIGHT / 2)
    # updater
    for p in particles:
        p.update(mouse_pos)
        if auto_pull_active:
            direction = (center - p.pos).normalize()
            strength = 1
            p.vel += direction * strength
    if auto_pull_active:
        auto_pull_counter += dt_seconds
        if auto_pull_counter >= AUTO_PULL_DURATION:
            auto_pull_active = False
    # draw trails
    trail_surface.fill((0, 0, 0, 25))  # low alpha = long trail
    screen.blit(trail_surface, (0, 0))
    for p in particles:
        p.draw(screen)
    pygame.display.flip()

pygame.quit()
