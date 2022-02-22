import pygame
import math

from settings import *
from player import Player
from render import Render
from map import world_map

pygame.init()
sc = pygame.display.set_mode((ScreenConfig.WIDTH, ScreenConfig.HEIGHT))
sc_mini_map = pygame.Surface((ScreenConfig.WIDTH // MinimapConfig.SCALE, ScreenConfig.HEIGHT // MinimapConfig.SCALE))
clock = pygame.time.Clock()
player = Player(PlayerConfig.player_pos, PlayerConfig.player_angle, PlayerConfig.player_speed)
render = Render(sc)

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
    render.draw_world(player.get_pos, player.angle, texture_is_enabled=render_type)
    if world_2d_is_enabled:
        render.draw_world_2d(player.get_pos, player)

    render.show_fps(clock)
    render.show_minimap(sc_mini_map, player)
    pygame.display.flip()
    clock.tick(ScreenConfig.FPS_60)