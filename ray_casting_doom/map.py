import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32, char

from settings import *

_ = False
matrix_map = [
    [1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 2, 2, 2, 2, 2, 2, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 2, 2, 2, 2, 2, 2, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 2, 2, 2, 2, 2, 2, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 2, 2, 2, 2, 2, 2, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 2, 2, 2, 2, 2, 2, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 2, 2, 2, 2, 2, 2, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

WORLD_WIDTH = len(matrix_map[0]) * ScreenConfig.TILE
WORLD_HEIGHT = len(matrix_map) * ScreenConfig.TILE
mini_map = set()
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
collision_walls = []
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            mini_map.add((i * MapConfig.TILE, j * MapConfig.TILE))
            collision_walls.append(pygame.Rect(i * ScreenConfig.TILE, j * ScreenConfig.TILE, ScreenConfig.TILE, ScreenConfig.TILE))
            if char == 1:
                world_map[(i * ScreenConfig.TILE, j * ScreenConfig.TILE)] = char
            elif char == 2:
                world_map[(i * ScreenConfig.TILE, j * ScreenConfig.TILE)] = char