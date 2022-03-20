import math
import pygame
from numba import njit

from settings import *
import njit_settings
from map import world_map, WORLD_HEIGHT, WORLD_WIDTH


@njit(fastmath=True)
def mapping(a, b):
    return (a // njit_settings.TILE) * njit_settings.TILE, (b // njit_settings.TILE) * njit_settings.TILE


@njit(fastmath=True)
def ray_cast_walls(player_pos, player_angle, world_map):
    # TODO
    #  Traceback (most recent call last):
    #   File "D:/CodeProjects/python_real_time_rendering/ray_casting_doom/main.py", line 31, in <module>
    #     walls = ray_cast_texture(player, render.textures)
    #   File "D:\CodeProjects\python_real_time_rendering\ray_casting_doom\ray_casting.py", line 76, in ray_cast_texture
    #     wall_column = textures[texture].subsurface(offset * TextureConfig.SCALE, 0, TextureConfig.SCALE, TextureConfig.HEIGHT)
    #  KeyError: 1
    casted_walls = []
    ox, oy = player_pos
    texture_h, texture_v = 852, 853
    xm, ym = mapping(ox, oy)
    current_angle = player_angle - njit_settings.HALF_FOV
    for ray in range(njit_settings.NUM_RAYS):
        sin_a = math.sin(current_angle)
        cos_a = math.cos(current_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        # verticals
        x, dx = (xm + njit_settings.TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WORLD_WIDTH, njit_settings.TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * njit_settings.TILE

        # horizontals
        y, dy = (ym + njit_settings.TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, WORLD_HEIGHT, njit_settings.TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * njit_settings.TILE

        # projection
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % njit_settings.TILE
        depth *= math.cos(player_angle - current_angle)  # fix fish eye effect
        depth = max(depth, 0.00001)
        proj_height = min(int(njit_settings.PROJ_COEF / depth), njit_settings.PENTA_HEIGHT)
        casted_walls.append((depth, offset, proj_height, texture))
        current_angle += njit_settings.DELTA_ANGLE

    return casted_walls


def texture_walls(player, textures):
    casted_walls = ray_cast_walls(player.get_pos, player.angle, world_map)
    walls = []
    for ray, casted_values in enumerate(casted_walls):
        depth, offset, proj_height, texture = casted_values
        wall_column = textures[texture].subsurface(offset * TextureConfig.SCALE, 0, TextureConfig.SCALE, TextureConfig.HEIGHT)
        wall_column = pygame.transform.scale(wall_column, (RayCastingConfig.SCALE, proj_height))
        wall_position = (ray * RayCastingConfig.SCALE, ScreenConfig.HALF_HEIGHT - proj_height // 2)
        walls.append((depth, wall_column, wall_position))
    return walls


# deprecated
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

