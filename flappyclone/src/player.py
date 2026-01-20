import pygame
import os
import sys
from utils import resource_path


class Player:
    def __init__(self, x, y, width=34, height=24):
        self.x = x  # x position of player
        self.y = y  # y position of player
        self.width = width  # player hitbox width
        self.height = height  # player hitbox height
        self.velocity = 0  # how fast the player currently falls
        self.max_fall_speed = 10  # maximum fall speed
        self.gravity = 0.5  # how fast player accelerates due to gravity
        self.flap_power = (
            -10
        )  # if velocity is downward speed the flapping reduces it/reverses it
        self.rotation = 0  # degrees, 0 = flat, positive = nosedown, negative = nose up
        self.max_rotation = 25  # tilt down max
        self.min_rotation = -75  # tilt up max
        self.rotation_factor = 3  # how much velocity affects rotation

        # load birb sprite

        self.sprite = pygame.image.load(
            (resource_path("assets/birb.png"))
        ).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

    def flap(self):
        # makes the player jump
        self.velocity = self.flap_power

    def update(self):
        # updates player position and velocity
        self.velocity += self.gravity
        self.velocity = min(self.velocity, self.max_fall_speed)
        self.y += self.velocity
        # prevent player from leaving top of the screen
        if self.y < 0:  # going upwards
            self.y = 0
            self.velocity = 0
        # rotation based on velocity
        target_rotation = self.velocity * self.rotation_factor
        self.rotation = max(self.min_rotation, min(self.max_rotation, target_rotation))

    def draw(self, screen):
        # draws player to screen
        radius = self.width // 2
        bird_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(
            bird_surface, (255, 255, 0), (radius, self.height // 2), radius
        )

        # rotate the bird surface
        rotated_sprite = pygame.transform.rotate(
            self.sprite, -self.rotation
        )  # negative rotation cuz pygame rotates counter-clockwize
        rect = rotated_sprite.get_rect(center=(self.x, self.y))
        screen.blit(rotated_sprite, rect)

    def get_rect(self):
        # return collision rectangle aka hitbox
        return pygame.Rect(
            self.x - self.width // 2, self.y - self.height // 2, self.width, self.height
        )

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:  # kun painaa jotain nappia
            if event.key == pygame.K_SPACE:  # kun painaa spacebaria
                self.flap()
