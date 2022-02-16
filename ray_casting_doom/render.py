import pygame
from settings import *
from ray_casting import ray_cast
from map import world_map



class Render:
    def __init__(self, sc):
        self.sc = sc
        self.font = pygame.font.SysFont('Arial', 36, bold=True)

    def draw_background(self):
        # Drawing sky and earth
        pygame.draw.rect(self.sc, ColorRGB.SKY_BLUE, (0, 0, ScreenConfig.WIDTH, ScreenConfig.HALF_HEIGHT))
        pygame.draw.rect(self.sc, ColorRGB.DARK_GREEN,
                         (0, ScreenConfig.HALF_HEIGHT, ScreenConfig.WIDTH, ScreenConfig.HALF_HEIGHT))

    def draw_world(self, plater_pos, player_angle):
        ray_cast(self.sc, plater_pos, player_angle)

    def show_fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render_font = self.font.render(display_fps, 0, ColorRGB.GREEN)
        self.sc.blit(render_font, (ScreenConfig.FPS_POSITION))

    def show_minimap(self, sc_mini_map, player):
        sc_mini_map.fill(ColorRGB.BLACK)
        map_x, map_y = player.x // MinimapConfig.SCALE, player.y // MinimapConfig.SCALE
        pygame.draw.circle(sc_mini_map, ColorRGB.GREEN, (int(map_x), int(map_y)), 5)
        pygame.draw.line(sc_mini_map, ColorRGB.GREEN, (map_x, map_y),
                         (
                             map_x + 12 * math.cos(player.angle),
                             map_y + 12 * math.sin(player.angle)
                         ),
                         2,
                         )
        for x, y in world_map:
            pygame.draw.rect(sc_mini_map, ColorRGB.DARK_GRAY, (x // MinimapConfig.SCALE, y // MinimapConfig.SCALE, MinimapConfig.TILE, MinimapConfig.TILE), 0)
        self.sc.blit(sc_mini_map, MinimapConfig.POSITION)