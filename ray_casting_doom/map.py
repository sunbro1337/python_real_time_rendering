from settings import *

text_map = [
    '111111111111',
    '1.....2....1',
    '1........2.1',
    '1..........1',
    '1..........1',
    '1........2.1',
    '1.....2....1',
    '111111111111',
]

mini_map = set()
world_map = {}
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char != '.':
            mini_map.add((i * MinimapConfig.TILE, j * MinimapConfig.TILE))
            if char == '1':
                world_map[(i * ScreenConfig.TILE, j * ScreenConfig.TILE)] = 'wall1.png'
            elif char == '2':
                world_map[(i * ScreenConfig.TILE, j * ScreenConfig.TILE)] = 'wall2.png'