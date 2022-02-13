import math

import pygame

from settings import *
from map import world_map


def ray_casting(sc, player_pos, player_angle):
    current_angle = player_angle - RayCastingConfig.HALF_FOV
    xo, yo = player_pos
    for ray in range(RayCastingConfig.NUM_RAYS):
        sin_a = math.sin(current_angle)
        cos_a = math.cos(current_angle)
        for depth in range(RayCastingConfig.MAX_DEPTH):
            x = xo + depth * cos_a
            y = yo + depth * sin_a
            # pygame.draw.line(sc, ColorRGB.DARK_GRAY, player_pos, (x, y), 2)
            if (x // ScreenConfig.TILE * ScreenConfig.TILE, y // ScreenConfig.TILE * ScreenConfig.TILE) in world_map:
                depth *= math.cos(player_angle - current_angle) # fix fish eye effect
                if depth <= 0:
                    depth = 1
                proj_height = RayCastingConfig.PROJ_COEF / depth
                color_element = 255 / (1 + depth * depth * 0.0001)
                final_color = (color_element, color_element, color_element)
                pygame.draw.rect(sc, final_color, (ray * RayCastingConfig.SCALE, ScreenConfig.HALF_HEIGHT - proj_height // 2, RayCastingConfig.SCALE, proj_height))
                break
        current_angle += RayCastingConfig.DELTA_ANGLE
