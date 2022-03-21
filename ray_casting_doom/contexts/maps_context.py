import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32


class Maps():
    def __init__(self, screen_config, map_config, matrix_map):
        self.screen_config = screen_config
        self.map_config = map_config
        self.matrix_map = matrix_map
        self.WORLD_WIDTH = len(self.matrix_map[0]) * self.screen_config.TILE
        self.WORLD_HEIGHT = len(self.matrix_map) * self.screen_config.TILE

    def create_maps(self):
        self.mini_map = set()
        self.world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        self.collision_walls = []
        for j, row in enumerate(self.matrix_map):
            for i, char in enumerate(row):
                if char:
                    self.mini_map.add((i * self.map_config.TILE, j * self.map_config.TILE))
                    self.collision_walls.append(pygame.Rect(i * self.screen_config.TILE, j * self.screen_config.TILE, self.screen_config.TILE, self.screen_config.TILE))
                    if char == 1:
                        self.world_map[(i * self.screen_config.TILE, j * self.screen_config.TILE)] = 852
                    elif char == 2:
                        self.world_map[(i * self.screen_config.TILE, j * self.screen_config.TILE)] = 853
