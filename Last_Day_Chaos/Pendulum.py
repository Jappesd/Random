import pygame, math, random
from pygame.math import Vector2

# --------------------
# Config
# --------------------
WIDTH, HEIGHT = 900, 900
FPS = 60
TRAIL_ALPHA = 3
NUM_PENDULUMS = 40

# Mouse interaction
MOUSE_FORCE_RADIUS = 100
MOUSE_FORCE_STRENGTH = 2  # overall scale
MAX_OMEGA = 2

# Auto pull
AUTO_PULL_INTERVAL = 2  # seconds between pulls
AUTO_PULL_DURATION = 0.2  # seconds of pull
AUTO_PULL_STRENGTH = 0.2


# --------------------
# Pendulum class
# --------------------
class Pendulum:
    def __init__(self):
        self.theta1 = math.pi / 2 + random.uniform(-0.05, 0.05)
        self.theta2 = math.pi / 2 + random.uniform(-0.05, 0.05)
        self.omega1 = 0
        self.omega2 = 0
        self.l1 = random.randint(150, 200)
        self.l2 = random.randint(150, 200)
        self.m1 = 10
        self.m2 = 10
        self.hue = random.uniform(0, 360)

    def update(
        self,
        dt,
        mouse_pos=None,
        mouse_dir=0,
        mouse_radius=MOUSE_FORCE_RADIUS,
        auto_pull=False,
        origin=(WIDTH // 2, HEIGHT // 4),
    ):
        g = 0.8
        DAMPING = 0.995  # gradual slow-down

        # --- Physics (Euler integration) ---
        num1 = -g * (2 * self.m1 + self.m2) * math.sin(self.theta1)
        num2 = -self.m2 * g * math.sin(self.theta1 - 2 * self.theta2)
        num3 = (
            -2
            * math.sin(self.theta1 - self.theta2)
            * self.m2
            * (
                self.omega2**2 * self.l2
                + self.omega1**2 * self.l1 * math.cos(self.theta1 - self.theta2)
            )
        )
        den = self.l1 * (
            2 * self.m1
            + self.m2
            - self.m2 * math.cos(2 * self.theta1 - 2 * self.theta2)
        )
        alpha1 = (num1 + num2 + num3) / den

        num1 = 2 * math.sin(self.theta1 - self.theta2)
        num2 = self.omega1**2 * self.l1 * (self.m1 + self.m2)
        num3 = g * (self.m1 + self.m2) * math.cos(self.theta1)
        num4 = self.omega2**2 * self.l2 * self.m2 * math.cos(self.theta1 - self.theta2)
        den = self.l2 * (
            2 * self.m1
            + self.m2
            - self.m2 * math.cos(2 * self.theta1 - 2 * self.theta2)
        )
        alpha2 = num1 * (num2 + num3 + num4) / den

        self.omega1 += alpha1 * dt * 60
        self.omega2 += alpha2 * dt * 60
        self.theta1 += self.omega1 * dt * 60
        self.theta2 += self.omega2 * dt * 60

        # --- Mouse interaction ---
        if mouse_pos and mouse_dir != 0:
            tip = self.get_tip(origin)
            dist = tip.distance_to(mouse_pos)
            if dist < mouse_radius:
                direction = (tip - mouse_pos).normalize()
                force = mouse_dir * MOUSE_FORCE_STRENGTH * dt * 60 * 0.05
                self.omega2 += force * direction.length()

        # --- Auto pull to center ---
        if auto_pull:
            tip = self.get_tip(origin)
            center = Vector2(WIDTH // 2, HEIGHT // 4)
            direction = (center - tip).normalize()
            self.omega2 += AUTO_PULL_STRENGTH * dt * 60 * 0.05

        # --- Damping (gradual slow down) ---
        self.omega1 *= DAMPING
        self.omega2 *= DAMPING

        # --- Clamp angular velocity ---
        self.omega1 = max(min(self.omega1, MAX_OMEGA), -MAX_OMEGA)
        self.omega2 = max(min(self.omega2, MAX_OMEGA), -MAX_OMEGA)

        # --- Update hue for color shift ---
        self.hue += 0.5
        if self.hue > 360:
            self.hue -= 360

    def get_positions(self, origin):
        x1 = origin[0] + self.l1 * math.sin(self.theta1)
        y1 = origin[1] + self.l1 * math.cos(self.theta1)
        x2 = x1 + self.l2 * math.sin(self.theta2)
        y2 = y1 + self.l2 * math.cos(self.theta2)
        return (x1, y1), (x2, y2)

    def get_tip(self, origin=(WIDTH // 2, HEIGHT // 4)):
        _, (x2, y2) = self.get_positions(origin)
        return Vector2(x2, y2)


# --------------------
# Helper
# --------------------
def color_from_hue(h):
    color = pygame.Color(0)
    color.hsva = (h % 360, 80, 100, 100)
    return color


# --------------------
# Init Pygame
# --------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
trail_surface = pygame.Surface((WIDTH, HEIGHT))
trail_surface.set_alpha(TRAIL_ALPHA)
trail_surface.fill((0, 0, 0))
clock = pygame.time.Clock()
running = True
# pygame.mouse.set_visible(False)

# Pendulums
pendulums = [Pendulum() for _ in range(NUM_PENDULUMS)]
origin = (WIDTH // 2, HEIGHT // 2)

# Mouse
mouse_dir = 0
mouse_pos = Vector2(0, 0)

# Auto pull timer
auto_pull_timer = 0
auto_pull_active = False
auto_pull_counter = 0

# --------------------
# Main loop
# --------------------
while running:
    dt = clock.tick(FPS) / 1000
    mouse_pos = Vector2(pygame.mouse.get_pos())

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_f:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left → repel
                mouse_dir = 1
            if event.button == 3:  # right → attract
                mouse_dir = -1
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_dir = 0

    # --- Update auto-pull ---
    auto_pull_timer += dt
    if not auto_pull_active and auto_pull_timer >= AUTO_PULL_INTERVAL:
        auto_pull_active = True
        auto_pull_timer = 0
        auto_pull_counter = 0

    # --- Update pendulums ---
    for p in pendulums:
        p.update(
            dt, mouse_pos=mouse_pos, mouse_dir=mouse_dir, auto_pull=auto_pull_active
        )

    if auto_pull_active:
        auto_pull_counter += dt
        if auto_pull_counter >= AUTO_PULL_DURATION:
            auto_pull_active = False

    # --- Draw trails ---
    trail_surface.fill((0, 0, 0, TRAIL_ALPHA))
    screen.blit(trail_surface, (0, 0))

    # --- Draw pendulums ---
    for p in pendulums:
        (x1, y1), (x2, y2) = p.get_positions(origin)
        pygame.draw.line(screen, (255, 255, 255), origin, (x1, y1), 1)
        pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 1)
        pygame.draw.circle(screen, color_from_hue(p.hue), (int(x2), int(y2)), 3)

    pygame.display.flip()

pygame.quit()
