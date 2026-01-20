import pygame
from player import Player
from pipe import Pipe
from utils import resource_path


class Game:
    GROUND_HEIGHT = 50  # height of the ground from bottom
    GROUND_COLOR = (222, 184, 135)
    PIPE_SPACING = 200
    WIDTH = 400
    HEIGHT = 600
    PIPE_SPAWN_INTERVAL = 1500  # milliseconds

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Flappy Clone")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.highscore = self.load_highscore()
        # sky sprite
        self.bg_img = pygame.image.load(
            resource_path("assets/cloud.png")
        ).convert_alpha()
        self.bg_width = self.bg_img.get_width()
        self.bg_scroll = 0
        self.bg_scroll_speed = 1
        # load ground sprite
        self.ground_img = pygame.image.load(
            resource_path("assets/ground.png")
        ).convert_alpha()
        self.ground_img = pygame.transform.scale(
            self.ground_img, (self.WIDTH, self.GROUND_HEIGHT)
        )
        self.ground_scroll = 0
        self.ground_scroll_speed = 3
        self.reset()

    def reset(self):
        self.player = Player(100, self.HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.started = False
        # spawn first pipe immediately
        self.pipes.append(Pipe(self.WIDTH + 50, self.HEIGHT))

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_highscore(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.highscore))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.started:
                    self.started = True
                    self.player.flap()
            if self.started and not self.game_over:
                self.player.handle_input(event)

            if self.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()

    def update(self):
        if not self.started or self.game_over:
            return

        self.player.update()

        for pipe in self.pipes:
            pipe.update()

            # collision
            for rect in pipe.get_rects():
                if self.player.get_rect().colliderect(rect):
                    self.game_over = True
                    if self.score > self.highscore:
                        self.highscore = self.score
                        self.save_highscore()
            # score when passing pipe
            if not pipe.passed and pipe.x + pipe.WIDTH < self.player.x:
                pipe.passed = True
                self.score += 1

        # spawn new pipe based on distance from last pipe
        if self.pipes:
            last_pipe = self.pipes[-1]
            if last_pipe.x <= self.WIDTH - self.PIPE_SPACING:
                self.pipes.append(Pipe(self.WIDTH, self.HEIGHT))

        # remove off-screen pipes
        self.pipes = [p for p in self.pipes if not p.off_screen()]

        # floor collision
        if self.player.y + self.player.height // 2 >= self.HEIGHT - self.GROUND_HEIGHT:
            self.player.y = self.HEIGHT - self.GROUND_HEIGHT - self.player.height // 2
            self.game_over = True
            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore()
        # ground stuff
        if self.started and not self.game_over:
            self.bg_scroll -= self.bg_scroll_speed
            if self.bg_scroll <= -self.bg_width:
                self.bg_scroll = 0
            self.ground_scroll -= self.ground_scroll_speed
            if self.ground_scroll <= -self.WIDTH:
                self.ground_scroll = 0  # loops back to start

    def draw(self):
        ground_y = self.HEIGHT - self.GROUND_HEIGHT
        self.screen.blit(self.bg_img, (self.bg_scroll, 0))
        self.screen.blit(self.bg_img, (self.bg_scroll + self.bg_width, 0))

        for pipe in self.pipes:  # handles pipe drawing
            pipe.draw(self.screen)

        self.player.draw(self.screen)
        # score drawing
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        highscore_text = font.render(f"HI: {self.highscore}", True, (255, 255, 255))
        self.screen.blit(highscore_text, (10, 40))
        if not self.started:  # if game not started draws text instructions
            font = pygame.font.SysFont(None, 40)
            text = font.render("Press SPACE to start", True, (0, 0, 0))
            rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(text, rect)
        if self.game_over:  # if gg then gg
            self.draw_game_over()
        # draw the scrolling ground
        self.screen.blit(self.ground_img, (self.ground_scroll, ground_y))
        self.screen.blit(self.ground_img, (self.ground_scroll + self.WIDTH, ground_y))

        pygame.display.flip()

    def draw_game_over(self):
        font = pygame.font.SysFont(None, 36)
        text = font.render("Game Over! Press R to restart", True, (255, 0, 0))
        rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(text, rect)
