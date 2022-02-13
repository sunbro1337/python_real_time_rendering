import pygame
import math

from settings import *
from player import Player
from map import world_map
from ray_casting import ray_casting

pygame.init()
sc = pygame.display.set_mode((ScreenConfig.WIDTH, ScreenConfig.HEIGHT))
clock = pygame.time.Clock()
player = Player(PlayerConfig.player_pos, PlayerConfig.player_angle, PlayerConfig.player_speed)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.move()

    sc.fill(ColorRGB.BLACK)

    # Drawing sky and earth
    pygame.draw.rect(sc, ColorRGB.BLUE, (0, 0, ScreenConfig.WIDTH, ScreenConfig.HALF_HEIGHT))
    pygame.draw.rect(sc, ColorRGB.DARK_GREEN, (0, ScreenConfig.HALF_HEIGHT, ScreenConfig.WIDTH, ScreenConfig.HALF_HEIGHT))

    ray_casting(sc, player.get_pos, player.angle)

    # pygame.draw.circle(sc, ColorRGB.GREEN, player.get_pos, 12)
    # pygame.draw.line(sc, ColorRGB.GREEN, player.get_pos,
    #                  (
    #                      player.x + ScreenConfig.WIDTH * math.cos(player.angle),
    #                      player.y + ScreenConfig.WIDTH * math.sin(player.angle)
    #                  ),
    #                  )

    # for x,y in world_map:
    #     pygame.draw.rect(sc, ColorRGB.DARK_GRAY, (x, y, ScreenConfig.TILE, ScreenConfig.TILE), 2)

    pygame.display.flip()
    clock.tick(ScreenConfig.FPS_60)