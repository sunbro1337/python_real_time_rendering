import pygame
from settings import *
from resources_system import collect_sprites


class Sprites:
    def __init__(self):
        self.sprite_types = collect_sprites(SpritesConfig.PATH)
        self.list_of_objects = [
            SpriteObject(self.sprite_types['barrel/0.png'], True, (7.1, 2.1), 1.8, 0.4),
        ]


class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static
        self.pos = self.x, self.y = pos[0] * ScreenConfig.TILE, pos[1] * ScreenConfig.TILE
        self.shift = shift
        self.scale = scale

    def object_locate(self, player, walls):
        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += SpritesConfig.DOUBLE_PI

        delta_rays = int(gamma / RayCastingConfig.DELTA_ANGLE)
        current_ray = SpritesConfig.CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(RayCastingConfig.HALF_FOV - current_ray * RayCastingConfig.DELTA_ANGLE)

        if 0 <- current_ray <= RayCastingConfig.NUM_RAYS - 1 and distance_to_sprite < walls[current_ray][0]:
            proj_height = int(RayCastingConfig.PROJ_COEF / distance_to_sprite * self.scale)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            sprite_pos = (current_ray * RayCastingConfig.SCALE - half_proj_height, ScreenConfig.HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)
