import pygame
import math

from configs.global_settings import SpritesConfig


class Player:
    def __init__(self, player_pos, player_angle, player_speed, sprites, collision_walls):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.player_speed = player_speed
        # collision parameters
        self.rect_side = 50
        self.rect = pygame.Rect(*player_pos, self.rect_side, self.rect_side)
        self.spites = sprites
        self.collision_list = collision_walls + self.spites.collision_sprites # TODO out collision_walls

        self.texture_is_enabled = True
        self.world_2d_is_enabled = False

    @property
    def get_pos(self):
        return (self.x, self.y)

    def detect_collisions(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx ,dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)
        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top
            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def move(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dx = self.player_speed * cos_a
            dy = self.player_speed * sin_a
            self.detect_collisions(dx, dy)
        if keys[pygame.K_s]:
            dx = -self.player_speed * cos_a
            dy = -self.player_speed * sin_a
            self.detect_collisions(dx, dy)
        if keys[pygame.K_a]:
            dx = self.player_speed * sin_a
            dy = -self.player_speed * cos_a
            self.detect_collisions(dx, dy)
        if keys[pygame.K_d]:
            dx = -self.player_speed * sin_a
            dy = self.player_speed * cos_a
            self.detect_collisions(dx, dy)
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
        self.angle %= SpritesConfig.DOUBLE_PI
        self.rect.center = self.x, self.y

    def mouse_control(self):
        # TODO Mouse control for camera and shots
        pass

    def gamepad_control(self):
        # TODO Gamepad control for camera, movements, shots etc.
        pass

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
