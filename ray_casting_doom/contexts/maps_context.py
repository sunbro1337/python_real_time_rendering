import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32

from configs.global_settings import *


class Maps():
    def __init__(self):
        _ = False
        self.matrix_map = [
            [1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
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
        self.WORLD_WIDTH = len(self.matrix_map[0]) * ScreenConfig.TILE
        self.WORLD_HEIGHT = len(self.matrix_map) * ScreenConfig.TILE

    def create_maps(self):
        self.mini_map = set()
        self.world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        self.collision_walls = []
        for j, row in enumerate(self.matrix_map):
            for i, char in enumerate(row):
                if char:
                    self.mini_map.add((i * MapConfig.TILE, j * MapConfig.TILE))
                    self.collision_walls.append(pygame.Rect(i * ScreenConfig.TILE, j * ScreenConfig.TILE, ScreenConfig.TILE, ScreenConfig.TILE))
                    if char == 1:
                        self.world_map[(i * ScreenConfig.TILE, j * ScreenConfig.TILE)] = 852
                    elif char == 2:
                        self.world_map[(i * ScreenConfig.TILE, j * ScreenConfig.TILE)] = 853
