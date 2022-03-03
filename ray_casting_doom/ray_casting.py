import math

import pygame

from settings import *
from map import world_map

# Old low performance but simple
# def ray_cast(sc, player_pos, player_angle):
#     current_angle = player_angle - RayCastingConfig.HALF_FOV
#     xo, yo = player_pos
#     for ray in range(RayCastingConfig.NUM_RAYS):
#         sin_a = math.sin(current_angle)
#         cos_a = math.cos(current_angle)
#         for depth in range(RayCastingConfig.MAX_DEPTH):
#             x = xo + depth * cos_a
#             y = yo + depth * sin_a
#             # pygame.draw.line(sc, ColorRGB.DARK_GRAY, player_pos, (x, y), 2)
#             if (x // ScreenConfig.TILE * ScreenConfig.TILE, y // ScreenConfig.TILE * ScreenConfig.TILE) in world_map:
#                 depth *= math.cos(player_angle - current_angle) # fix fish eye effect
#                 if depth <= 0:
#                     depth = 1
#                 proj_height = RayCastingConfig.PROJ_COEF / depth
#                 color_element = 255 / (1 + depth * depth * 0.00002)
#                 final_color = (color_element, color_element // 2, color_element // 3)
#                 pygame.draw.rect(sc, final_color, (ray * RayCastingConfig.SCALE, ScreenConfig.HALF_HEIGHT - proj_height // 2, RayCastingConfig.SCALE, proj_height))
#                 break
#         current_angle += RayCastingConfig.DELTA_ANGLE


def mapping(a, b):
    return (a // ScreenConfig.TILE) * ScreenConfig.TILE, (b // ScreenConfig.TILE) * ScreenConfig.TILE


def ray_cast_texture(player, textures):
    walls = []
    ox, oy = player.get_pos
    xm, ym = mapping(ox, oy)
    current_angle = player.angle - RayCastingConfig.HALF_FOV
    for ray in range(RayCastingConfig.NUM_RAYS):
        sin_a = math.sin(current_angle)
        cos_a = math.cos(current_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        # verticals
        x, dx = (xm + ScreenConfig.TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, ScreenConfig.WIDTH, ScreenConfig.TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * ScreenConfig.TILE

        # horizontals
        y, dy = (ym + ScreenConfig.TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, ScreenConfig.HEIGHT, ScreenConfig.TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * ScreenConfig.TILE

        # projection
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % ScreenConfig.TILE
        depth *= math.cos(player.angle - current_angle)  # fix fish eye effect
        depth = max(depth, 0.00001)
        proj_height = min(int(RayCastingConfig.PROJ_COEF / depth), 2 * ScreenConfig.HEIGHT)

        wall_column = textures[texture].subsurface(offset * TextureConfig.SCALE, 0, TextureConfig.SCALE, TextureConfig.HEIGHT)
        wall_column = pygame.transform.scale(wall_column, (RayCastingConfig.SCALE, proj_height))
        wall_position = (ray * RayCastingConfig.SCALE, ScreenConfig.HALF_HEIGHT - proj_height // 2)
        walls.append((depth, wall_column, wall_position))

        current_angle += RayCastingConfig.DELTA_ANGLE

    return walls


def ray_cast_color(sc, player_pos, player_angle):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    current_angle = player_angle - RayCastingConfig.HALF_FOV
    for ray in range(RayCastingConfig.NUM_RAYS):
        sin_a = math.sin(current_angle)
        cos_a = math.cos(current_angle)

        # verticals
        x, dx = (xm + ScreenConfig.TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, ScreenConfig.WIDTH, ScreenConfig.TILE):
            depth_h = (x - ox) / cos_a
            y = oy + depth_h * sin_a
            if mapping(x + dx, y) in world_map:
                break
            x += dx * ScreenConfig.TILE

        # horizontals
        y, dy = (ym + ScreenConfig.TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, ScreenConfig.HEIGHT, ScreenConfig.TILE):
            depth_v = (y - oy) / sin_a
            x = ox + depth_v * cos_a
            if mapping(x, y + dy) in world_map:
                break
            y += dy * ScreenConfig.TILE

        # projection
        depth = depth_v if depth_v < depth_h else depth_h
        depth *= math.cos(player_angle - current_angle)  # fix fish eye effect
        depth = max(depth, 0.00001)
        proj_height = min(int(RayCastingConfig.PROJ_COEF / depth), 2 * ScreenConfig.HEIGHT)
        color_element = 255 / (1 + depth * depth * 0.00002)
        final_color = (color_element, color_element // 2, color_element // 3)
        pygame.draw.rect(sc, final_color, (ray * RayCastingConfig.SCALE, ScreenConfig.HALF_HEIGHT - proj_height // 2, RayCastingConfig.SCALE, proj_height))
        current_angle += RayCastingConfig.DELTA_ANGLE

