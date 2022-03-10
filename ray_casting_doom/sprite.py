import pygame
from settings import *
from resources_system import collect_sprites


class Sprites:
    def __init__(self):
        self.sprite_types = collect_sprites(SpritesConfig.PATH)
        self.list_of_objects = [
            SpriteObject(self.sprite_types['barrel'][0], True, (7.1, 2.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['barrel'][0], True, (5.9, 2.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['pedestal'][0], True, (8.8, 2.6), 1.6, 0.5),
            SpriteObject(self.sprite_types['pedestal'][0], True, (8.8, 5.6), 1.6, 0.5),
            SpriteObject(self.sprite_types['kakodemon'], False, (7, 4), -0.2, 0.7),
            SpriteObject(self.sprite_types['kakodemon'], False, (5, 4), -0.2, 0.7),
        ]


class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static
        self.pos = self.x, self.y = pos[0] * ScreenConfig.TILE, pos[1] * ScreenConfig.TILE
        self.shift = shift
        self.scale = scale

        if not static:
            self.sprite_angles = [frozenset(range(i, i +45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player, walls=None):
        # fake_walls0 = [walls[0] for i in range(SpritesConfig.FAKE_RAYS)]
        # fake_walls1 = [walls[-1] for i in range(SpritesConfig.FAKE_RAYS)]
        # fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += SpritesConfig.DOUBLE_PI

        delta_rays = int(gamma / RayCastingConfig.DELTA_ANGLE)
        current_ray = SpritesConfig.CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(RayCastingConfig.HALF_FOV - current_ray * RayCastingConfig.DELTA_ANGLE)

        fake_ray = current_ray + SpritesConfig.FAKE_RAYS
        if 0 <= fake_ray <= SpritesConfig.FAKE_RAYS_RANGE and distance_to_sprite > 30:
            # for fake walls use < fake_walls[fake_ray][0]; instead > 30
            # pygame.error: Out of memory proj_height = int(RayCastingConfig.PROJ_COEF / distance_to_sprite * self.scale)
            proj_height = min(int(RayCastingConfig.PROJ_COEF / distance_to_sprite * self.scale), ScreenConfig.DOUBLE_HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            if not self.static:
                if theta < 0:
                    theta += SpritesConfig.DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            sprite_pos = (current_ray * RayCastingConfig.SCALE - half_proj_height, ScreenConfig.HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)
