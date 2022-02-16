import pygame
import math

from settings import *
from player import Player
from render import Render
from map import world_map

pygame.init()
sc = pygame.display.set_mode((ScreenConfig.WIDTH, ScreenConfig.HEIGHT))
sc_mini_map = pygame.Surface((ScreenConfig.WIDTH // 5, ScreenConfig.HEIGHT // 5))
clock = pygame.time.Clock()
player = Player(PlayerConfig.player_pos, PlayerConfig.player_angle, PlayerConfig.player_speed)
render = Render(sc)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.move()

    sc.fill(ColorRGB.BLACK)

    render.draw_background()
    render.draw_world(player.get_pos, player.angle)

    #pygame.draw.circle(sc, ColorRGB.GREEN, player.get_pos, 12)
    #pygame.draw.line(sc, ColorRGB.GREEN, player.get_pos,
    #                 (
    #                     player.x + ScreenConfig.WIDTH * math.cos(player.angle),
    #                     player.y + ScreenConfig.WIDTH * math.sin(player.angle)
    #                 ),
    #                 )
    #for x,y in world_map:
    #    pygame.draw.rect(sc, ColorRGB.DARK_GRAY, (x, y, ScreenConfig.TILE, ScreenConfig.TILE), 2)

    render.show_minimap(sc_mini_map, player)
    render.show_fps(clock)

    pygame.display.flip()
    clock.tick(ScreenConfig.FPS_60)