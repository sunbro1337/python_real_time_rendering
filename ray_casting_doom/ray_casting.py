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


def ray_cast(sc, player_pos, player_angle):
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
        if depth <= 0:
            depth = 1
        proj_height = RayCastingConfig.PROJ_COEF / depth
        color_element = 255 / (1 + depth * depth * 0.00002)
        final_color = (color_element, color_element // 2, color_element // 3)
        pygame.draw.rect(sc, final_color, (ray * RayCastingConfig.SCALE, ScreenConfig.HALF_HEIGHT - proj_height // 2, RayCastingConfig.SCALE, proj_height))
        current_angle += RayCastingConfig.DELTA_ANGLE

