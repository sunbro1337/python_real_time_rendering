import pygame
import math
from settings import *


class Player:
    def __init__(self, player_pos, player_angle, player_speed):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.player_speed = player_speed
        self.texture_is_enabled = True
        self.world_2d_is_enabled = False

    @property
    def get_pos(self):
        return (self.x, self.y)

    def move(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += self.player_speed * cos_a
            self.y += self.player_speed * sin_a
        if keys[pygame.K_s]:
            self.x += -self.player_speed * cos_a
            self.y += -self.player_speed * sin_a
        if keys[pygame.K_a]:
            self.x += self.player_speed * sin_a
            self.y += -self.player_speed * cos_a
        if keys[pygame.K_d]:
            self.x += -self.player_speed * sin_a
            self.y += self.player_speed * cos_a
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

    def change_render_type(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.texture_is_enabled = False
        elif keys[pygame.K_2]:
            self.texture_is_enabled = True
        return self.texture_is_enabled

    def change_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_3]:
            self.world_2d_is_enabled = True
        elif keys[pygame.K_4]:
            self.world_2d_is_enabled = False
        return self.world_2d_is_enabled