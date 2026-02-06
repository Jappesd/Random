import pygame, random

# --------------------
# Config
# --------------------
WIDTH, HEIGHT = 800, 600
FPS = 60

PLAYER_RADIUS = 15
PLAYER_SPEED = 500  # pixels/sec

GOAL_RADIUS = 20
NUM_GOALS = 5
GOAL_MAX_SPEED = 100
GOAL_SPEED_TWEAK = 10  # small random tweak to velocity

ROUND_TIME = 30  # seconds

# --------------------
# Init Pygame
# --------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
running = True

# --------------------
# Game State
# --------------------
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
score = 0
timer = ROUND_TIME

# Goals and velocities
goals = []
goal_velocities = []
for _ in range(NUM_GOALS):
    pos = pygame.Vector2(
        random.randint(GOAL_RADIUS, WIDTH - GOAL_RADIUS),
        random.randint(GOAL_RADIUS, HEIGHT - GOAL_RADIUS),
    )
    goals.append(pos)
    vel = pygame.Vector2(
        random.uniform(-GOAL_MAX_SPEED, GOAL_MAX_SPEED),
        random.uniform(-GOAL_MAX_SPEED, GOAL_MAX_SPEED),
    )
    goal_velocities.append(vel)

# Trail surface
trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
last_goal_milestone = 0
# --------------------
# Main loop
# --------------------
while running:
    dt = clock.tick(FPS) / 1000
    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click → spawn new goal
                pos = pygame.mouse.get_pos()
                goals.append(pygame.Vector2(pos))
                vel = pygame.Vector2(
                    random.uniform(-GOAL_MAX_SPEED, GOAL_MAX_SPEED),
                    random.uniform(-GOAL_MAX_SPEED, GOAL_MAX_SPEED),
                )
                goal_velocities.append(vel)

    # --- Player movement ---
    keys = pygame.key.get_pressed()
    move = pygame.Vector2(0, 0)
    if keys[pygame.K_w]:
        move.y -= 1
    if keys[pygame.K_s]:
        move.y += 1
    if keys[pygame.K_a]:
        move.x -= 1
    if keys[pygame.K_d]:
        move.x += 1
    if move.length() > 0:
        move = move.normalize() * PLAYER_SPEED * dt
        player_pos += move

    # Keep player inside screen
    player_pos.x = max(PLAYER_RADIUS, min(WIDTH - PLAYER_RADIUS, player_pos.x))
    player_pos.y = max(PLAYER_RADIUS, min(HEIGHT - PLAYER_RADIUS, player_pos.y))

    # --- Goal collision with player ---
    for i, goal in enumerate(goals):
        if player_pos.distance_to(goal) < PLAYER_RADIUS + GOAL_RADIUS:
            score += 1
            # reset goal position and velocity
            goal.x = random.randint(GOAL_RADIUS, WIDTH - GOAL_RADIUS)
            goal.y = random.randint(GOAL_RADIUS, HEIGHT - GOAL_RADIUS)
            goal_velocities[i] = pygame.Vector2(
                random.uniform(-GOAL_MAX_SPEED, GOAL_MAX_SPEED),
                random.uniform(-GOAL_MAX_SPEED, GOAL_MAX_SPEED),
            )
    # --- Check milestone for adding new goal ---
    milestone = (score // 10) * 10
    if milestone > last_goal_milestone:
        # Add a new goal
        pos = pygame.Vector2(
            random.randint(GOAL_RADIUS, WIDTH - GOAL_RADIUS),
            random.randint(GOAL_RADIUS, HEIGHT - GOAL_RADIUS),
        )
        goals.append(pos)
        vel = pygame.Vector2(
            random.uniform(-GOAL_MAX_SPEED, GOAL_MAX_SPEED),
            random.uniform(-GOAL_MAX_SPEED, GOAL_MAX_SPEED),
        )
        goal_velocities.append(vel)
        last_goal_milestone = milestone  # upda

    # --- Move goals smoothly ---
    for i, goal in enumerate(goals):
        goal += goal_velocities[i] * dt
        # small random tweak
        tweak = (
            pygame.Vector2(
                random.uniform(-GOAL_SPEED_TWEAK, GOAL_SPEED_TWEAK),
                random.uniform(-GOAL_SPEED_TWEAK, GOAL_SPEED_TWEAK),
            )
            * dt
        )
        goal_velocities[i] += tweak
        if goal_velocities[i].length() > GOAL_MAX_SPEED:
            goal_velocities[i].scale_to_length(GOAL_MAX_SPEED)
        # bounce off screen edges
        if goal.x < GOAL_RADIUS or goal.x > WIDTH - GOAL_RADIUS:
            goal_velocities[i].x *= -1
            goal.x = max(GOAL_RADIUS, min(WIDTH - GOAL_RADIUS, goal.x))
        if goal.y < GOAL_RADIUS or goal.y > HEIGHT - GOAL_RADIUS:
            goal_velocities[i].y *= -1
            goal.y = max(GOAL_RADIUS, min(HEIGHT - GOAL_RADIUS, goal.y))

    # --- Elastic collisions between goals ---
    for i, g1 in enumerate(goals):
        for j, g2 in enumerate(goals[i + 1 :], start=i + 1):
            offset = g2 - g1
            dist = offset.length()
            if dist < GOAL_RADIUS * 2 and dist != 0:
                normal = offset / dist
                v1 = goal_velocities[i].dot(normal)
                v2 = goal_velocities[j].dot(normal)
                goal_velocities[i] += (v2 - v1) * normal
                goal_velocities[j] += (v1 - v2) * normal
                # separate goals
                overlap = 0.5 * (GOAL_RADIUS * 2 - dist)
                g1 -= normal * overlap
                g2 += normal * overlap

    # --- Timer ---
    timer -= dt
    if timer <= 0:
        running = False

    # --- Draw ---
    trail_surface.fill((0, 0, 0, 25))  # low alpha for trails
    trail_surface.blit(screen, (0, 0))
    screen.blit(trail_surface, (0, 0))

    screen.fill((30, 30, 30))  # background
    pygame.draw.circle(
        screen, (0, 255, 0), (int(player_pos.x), int(player_pos.y)), PLAYER_RADIUS
    )
    for goal in goals:
        pygame.draw.circle(screen, (255, 0, 0), (int(goal.x), int(goal.y)), GOAL_RADIUS)

    # Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    # Timer
    timer_text = font.render(f"Time: {int(timer)}", True, (255, 255, 255))
    screen.blit(timer_text, (WIDTH - 150, 10))

    pygame.display.flip()

pygame.quit()
print(f"Final score: {score}")
