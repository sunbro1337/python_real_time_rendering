from settings import *

text_map = [
    '111111111111',
    '1....22....1',
    '1.2....2...1',
    '1..........1',
    '1...2.....21',
    '1.....22..21',
    '1.........21',
    '111111111111',
]

mini_map = set()
world_map = {}
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char != '.':
            mini_map.add((i * MinimapConfig.TILE, j * MinimapConfig.TILE))
            if char == '1':
                world_map[(i * ScreenConfig.TILE, j * ScreenConfig.TILE)] = '1'
            elif char == '2':
                world_map[(i * ScreenConfig.TILE, j * ScreenConfig.TILE)] = '2'