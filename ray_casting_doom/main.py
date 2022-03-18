import pygame

import map
from settings import *
from player import Player
from render import Render
from sprite import *
from ray_casting import create_walls


pygame.init()
sc = pygame.display.set_mode((ScreenConfig.WIDTH, ScreenConfig.HEIGHT))
sc_mini_map = pygame.Surface(MapConfig.MINIMAP_RESOLUTION)
sprites = Sprites()
clock = pygame.time.Clock()
player = Player(PlayerConfig.player_pos, PlayerConfig.player_angle, PlayerConfig.player_speed, sprites)
render = Render(sc)

print(map.world_map)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.move()

    render_type = player.change_render_type()
    world_2d_is_enabled = player.change_direction()

    sc.fill(ColorRGB.BLACK)

    render.draw_sky(PlayerConfig.player_angle)
    render.draw_earth()
    walls = create_walls(player, render.textures_for_raycast)
    render.draw_world(walls + [obj.object_locate(player, walls) for obj in sprites.list_of_objects])
    render.show_fps(clock)
    render.show_minimap(sc_mini_map, player)
    pygame.display.flip()
    clock.tick(ScreenConfig.FPS_60)