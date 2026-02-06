import pygame, random, math
from pygame.math import Vector2

# --------------------
# Config
# --------------------
WIDTH, HEIGHT = 800, 800
FPS = 60

ARENA_RADIUS = 200
BALL_RADIUS = 10
BALL_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
SPEED_INCREMENT = 1.1
MAX_SPEED = 10000


# --------------------
# Ball class
# --------------------
class Ball:
    def __init__(self, pos, vel):
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.radius = BALL_RADIUS
        self.color = random.choice(BALL_COLORS)

    def update(self, dt):
        # move
        self.pos += self.vel * dt

        # bounce off circular boundary
        to_center = self.pos - Vector2(WIDTH // 2, HEIGHT // 2)
        if to_center.length() + self.radius > ARENA_RADIUS:
            # reflect velocity
            normal = to_center.normalize()
            self.vel = self.vel.reflect(normal) * SPEED_INCREMENT  # speed up a bit
            # push inside
            self.pos = Vector2(WIDTH // 2, HEIGHT // 2) + normal * (
                ARENA_RADIUS - self.radius
            )

    def draw(self, surface):
        pygame.draw.circle(
            surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius
        )


# --------------------
# Init Pygame
# --------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

balls = []

# --------------------
# Main loop
# --------------------
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click → spawn ball
                pos = pygame.mouse.get_pos()
                # random initial velocity
                vel = Vector2(random.uniform(-200, 200), random.uniform(-200, 200))
                balls.append(Ball(pos, vel))

    # update balls
    for ball in balls[:]:
        ball.update(dt)
        if ball.vel.length() > MAX_SPEED:
            balls.remove(ball)

    # simple ball collisions
    for i, b1 in enumerate(balls):
        for b2 in balls[i + 1 :]:
            offset = b2.pos - b1.pos
            dist = offset.length()
            if dist < b1.radius + b2.radius:
                # basic elastic collision
                normal = offset.normalize()
                b1.vel, b2.vel = b2.vel.reflect(normal), b1.vel.reflect(-normal)

    # draw
    screen.fill((0, 0, 0))
    # draw arena
    pygame.draw.circle(screen, (50, 50, 50), (WIDTH // 2, HEIGHT // 2), ARENA_RADIUS, 2)
    for ball in balls:
        ball.draw(screen)
    pygame.display.flip()

pygame.quit()
