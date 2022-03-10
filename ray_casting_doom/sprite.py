import pygame
from settings import *
from resources_system import collect_sprites
from collections import deque


class Sprites:
    def __init__(self):
        # self.sprite_types = collect_sprites(SpritesConfig.PATH)
        self.sprite_parameters = {
            'barrel': {
                'sprite': pygame.image.load('sprites/barrel/base/0.png'),
                'viewing_angles': False,
                'shift': 1.8,
                'scale': 0.4,
                'animation': deque(
                    [pygame.image.load(f'sprites/barrel/anim/{i}.png').convert_alpha() for i in range(12)]
                ),
                'animation_dist': 800,
                'animation_speed': 10,
            },
            'pin': {
                'sprite': pygame.image.load('sprites/pin/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.6,
                'scale': 0.6,
                'animation': deque([pygame.image.load(f'sprites/pin/anim/{i}.png').convert_alpha() for i in range(8)]),
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
            },
            'kakodemon': {
                'sprite': [pygame.image.load(f'sprites/kakodemon/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': -0.2,
                'scale': 1.1,
                'animation': deque(
                    [pygame.image.load(f'sprites/kakodemon/anim/{i}.png').convert_alpha() for i in range(9)]),
                'animation_dist': 150,
                'animation_speed': 10,
                'blocked': True,
            },
            'flame': {
                'sprite': pygame.image.load('sprites/flame/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.7,
                'scale': 0.6,
                'animation': deque(
                    [pygame.image.load(f'sprites/flame/anim/{i}.png').convert_alpha() for i in range(16)]),
                'animation_dist': 800,
                'animation_speed': 5,
                'blocked': None,
            },
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_parameters['barrel'], (7.1, 2.1)),
            SpriteObject(self.sprite_parameters['barrel'], (5.9, 2.1)),
            SpriteObject(self.sprite_parameters['pin'], (8.7, 2.5)),
            SpriteObject(self.sprite_parameters['kakodemon'], (7, 4)),
            SpriteObject(self.sprite_parameters['flame'], (8.6, 5.6))
            #SpriteObject(self.sprite_types['pedestal'][0], True, (8.8, 2.6), 1.6, 0.5),
            #SpriteObject(self.sprite_types['pedestal'][0], True, (8.8, 5.6), 1.6, 0.5),
            #SpriteObject(self.sprite_types['kakodemon'], False, (7, 4), -0.2, 0.7),
            #SpriteObject(self.sprite_types['kakodemon'], False, (5, 4), -0.2, 0.7),
        ]


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation']
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.animation_count = 0
        self.pos = self.x, self.y = pos[0] * ScreenConfig.TILE, pos[1] * ScreenConfig.TILE

        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
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
            # choosing sprite for angle
            if self.viewing_angles:
                if theta < 0:
                    theta += SpritesConfig.DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            #sprite animation
            sprite_object = self.object
            if self.animation and distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            # sprite scale and pos
            sprite_pos = (current_ray * RayCastingConfig.SCALE - half_proj_height, ScreenConfig.HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)
